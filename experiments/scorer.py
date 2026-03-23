"""
LLM-as-Judge Scorer: Uses one model to score outputs from other models.

Scoring rubric (0-3):
  0: Wrong answer or irrelevant output
  1: Partially correct, missing key elements
  2: Correct answer, adequate reasoning
  3: Correct answer, excellent reasoning, no drift

Self-consistency: each output scored twice; disagreements flagged.
"""

import json
import logging
from typing import Optional
from pathlib import Path

from ollama_client import OllamaClient, extract_response_text
from config import JUDGE_MODEL, JUDGE_TEMPERATURE, JUDGE_NUM_PREDICT, PROMPTS_DIR

logger = logging.getLogger("iot_experiments")

JUDGE_SYSTEM_PROMPT = """You are an expert evaluator of AI reasoning outputs. Your job is to score the quality of a model's response to a task.

SCORING RUBRIC (you MUST output exactly one integer 0-3):
  0 = Wrong answer or irrelevant output. The response does not address the task or produces incorrect results.
  1 = Partially correct. Some relevant content but missing key elements or contains significant errors.
  2 = Correct answer with adequate reasoning. The response addresses the task and produces valid results.
  3 = Excellent. Correct answer with thorough reasoning, no drift from the task purpose, and well-structured output.

ADDITIONAL CRITERIA (if provided):
- Check if the specified ground truth was reached
- Check if the anti-purpose was violated (if provided)
- Check if the success signal was satisfied (if provided)

OUTPUT FORMAT:
You must respond with ONLY a JSON object, nothing else:
{"score": <0-3>, "reason": "<one sentence explanation>"}"""


class Scorer:
    """LLM-as-judge scorer with self-consistency checking."""

    def __init__(
        self,
        client: Optional[OllamaClient] = None,
        judge_model: str = JUDGE_MODEL,
    ):
        self.client = client or OllamaClient()
        self.judge_model = judge_model

    def score(
        self,
        task_text: str,
        model_output: str,
        ground_truth: str = "",
        anti_purpose: str = "",
        success_signal: str = "",
        topology_used: str = "",
        custom_rubric: str = "",
    ) -> dict:
        """
        Score a model output using LLM-as-judge.

        Returns dict with:
            - score: int (0-3)
            - reason: str
            - consistent: bool (True if two independent scores agree)
            - scores: list[int] (both scores for transparency)
        """
        judge_prompt = self._build_judge_prompt(
            task_text, model_output, ground_truth,
            anti_purpose, success_signal, topology_used, custom_rubric,
        )

        # Score twice for self-consistency
        score1 = self._get_score(judge_prompt)
        score2 = self._get_score(judge_prompt)

        consistent = abs(score1["score"] - score2["score"]) <= 1
        final_score = round((score1["score"] + score2["score"]) / 2)

        if not consistent:
            logger.warning(
                f"Score inconsistency: {score1['score']} vs {score2['score']} "
                f"for task: {task_text[:50]}..."
            )

        return {
            "score": final_score,
            "reason": score1["reason"],
            "consistent": consistent,
            "scores": [score1["score"], score2["score"]],
        }

    def _build_judge_prompt(
        self,
        task_text: str,
        model_output: str,
        ground_truth: str,
        anti_purpose: str,
        success_signal: str,
        topology_used: str,
        custom_rubric: str,
    ) -> str:
        parts = [f"TASK:\n{task_text}\n"]

        if ground_truth:
            parts.append(f"GROUND TRUTH:\n{ground_truth}\n")
        if anti_purpose:
            parts.append(f"ANTI-PURPOSE (must NOT be violated):\n{anti_purpose}\n")
        if success_signal:
            parts.append(f"SUCCESS SIGNAL:\n{success_signal}\n")
        if topology_used:
            parts.append(f"TOPOLOGY USED: {topology_used}\n")
        if custom_rubric:
            parts.append(f"ADDITIONAL SCORING CRITERIA:\n{custom_rubric}\n")

        parts.append(f"MODEL OUTPUT TO EVALUATE:\n{model_output}\n")
        parts.append("Score this output 0-3. Respond with ONLY a JSON object: {\"score\": <0-3>, \"reason\": \"<explanation>\"}")

        return "\n".join(parts)

    def _get_score(self, prompt: str) -> dict:
        """Get a single score from the judge model."""
        try:
            result = self.client.generate(
                model=self.judge_model,
                prompt=prompt,
                system=JUDGE_SYSTEM_PROMPT,
                temperature=JUDGE_TEMPERATURE,
                num_predict=JUDGE_NUM_PREDICT,
            )
            text = extract_response_text(result)
            return self._parse_score(text)
        except Exception as e:
            logger.error(f"Scoring failed: {e}")
            return {"score": -1, "reason": f"Scoring error: {e}"}

    @staticmethod
    def _parse_score(text: str) -> dict:
        """Parse score JSON from judge output, with fallback heuristics."""
        # Strip markdown code fences if present
        import re
        cleaned = re.sub(r'```(?:json)?\s*', '', text).strip()
        cleaned = re.sub(r'```\s*$', '', cleaned).strip()

        # Try direct JSON parse
        try:
            start = cleaned.index("{")
            end = cleaned.rindex("}") + 1
            data = json.loads(cleaned[start:end])
            score = int(data.get("score", -1))
            reason = data.get("reason", "")
            if 0 <= score <= 3:
                return {"score": score, "reason": reason}
        except (ValueError, json.JSONDecodeError, KeyError):
            pass

        # Fallback: look for a digit 0-3
        for char in text:
            if char in "0123":
                return {"score": int(char), "reason": f"Extracted from: {text[:100]}"}

        return {"score": -1, "reason": f"Could not parse score from: {text[:200]}"}
