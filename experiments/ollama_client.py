"""
Ollama REST API client. Zero external dependencies (uses urllib only).
Handles retries, timeouts, and structured response parsing.
"""

import json
import time
import logging
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from typing import Optional

from config import OLLAMA_BASE_URL, OLLAMA_TIMEOUT, OLLAMA_RETRIES

logger = logging.getLogger("iot_experiments")


class OllamaClient:
    """Thin wrapper over Ollama's /api/generate endpoint."""

    def __init__(
        self,
        base_url: str = OLLAMA_BASE_URL,
        timeout: int = OLLAMA_TIMEOUT,
        retries: int = OLLAMA_RETRIES,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.retries = retries

    def generate(
        self,
        model: str,
        prompt: str,
        system: str = "",
        temperature: float = 0.7,
        num_predict: int = 1024,
        stream: bool = False,
    ) -> dict:
        """
        Generate a completion from Ollama.

        Returns dict with keys:
            - response: str (the generated text)
            - model: str
            - total_duration: int (nanoseconds)
            - eval_count: int (tokens generated)
            - prompt_eval_count: int (tokens in prompt)
        """
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream,
            "options": {
                "temperature": temperature,
                "num_predict": num_predict,
            },
        }
        if system:
            payload["system"] = system

        return self._post("/api/generate", payload)

    def list_models(self) -> list:
        """List available models."""
        try:
            result = self._get("/api/tags")
            return [m["name"] for m in result.get("models", [])]
        except Exception as e:
            logger.error(f"Failed to list models: {e}")
            return []

    def is_available(self, model: str) -> bool:
        """Check if a specific model is available."""
        available = self.list_models()
        return any(model in m for m in available)

    def _post(self, endpoint: str, payload: dict) -> dict:
        """POST request with retries."""
        url = f"{self.base_url}{endpoint}"
        data = json.dumps(payload).encode("utf-8")

        for attempt in range(self.retries):
            try:
                req = Request(
                    url,
                    data=data,
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with urlopen(req, timeout=self.timeout) as resp:
                    return json.loads(resp.read().decode("utf-8"))

            except (URLError, HTTPError, TimeoutError) as e:
                wait = 2 ** attempt
                logger.warning(
                    f"Attempt {attempt + 1}/{self.retries} failed for {payload.get('model', 'unknown')}: "
                    f"{e}. Retrying in {wait}s..."
                )
                if attempt < self.retries - 1:
                    time.sleep(wait)
                else:
                    raise RuntimeError(
                        f"Ollama request failed after {self.retries} attempts: {e}"
                    ) from e

    def _get(self, endpoint: str) -> dict:
        """GET request."""
        url = f"{self.base_url}{endpoint}"
        req = Request(url, method="GET")
        with urlopen(req, timeout=self.timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))


def extract_response_text(result: dict) -> str:
    """Extract clean response text from Ollama result."""
    return result.get("response", "").strip()


def get_token_counts(result: dict) -> dict:
    """Extract token usage from Ollama result."""
    return {
        "prompt_tokens": result.get("prompt_eval_count", 0),
        "completion_tokens": result.get("eval_count", 0),
        "total_duration_ms": result.get("total_duration", 0) / 1_000_000,
    }
