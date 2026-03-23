# Section 10: Appendix

This appendix provides the complete experimental details required for reproducibility, including all benchmark tasks, prompt templates, the IoT governance specifications, scoring rubrics, and detailed model configurations.

## A.1 Benchmark Tasks

The evaluation suite consists of 18 tasks across varied reasoning domains. Each task is categorised by its optimal reasoning topology.

### Interconnected Tasks

**IoT Governance Triple applied to this category:**

- Purpose (Purpose): Identify relationships and interactions between multiple factors

- Anti-Purpose (Anti-Purpose): Must not treat factors as independent when they interact

- Success Signal (Success Signal): A relationship map showing connections, feedback loops, and systemic effects


- **int_001** (medical): A 42-year-old patient presents with chronic fatigue, joint pain, and a butterfly-shaped facial rash. These symptoms could each have independent causes, or they could share a common underlying condition. Analyse whether and how these symptoms connect, identifying the most likely unifying diagnosis and explaining the causal pathway.

- **int_002** (supply_chain): In a supply chain: Factory A supplies components to Factory B and Factory C. Factory B assembles products using components from A and C. Factory C produces sub-assemblies using components from A only. All three sell to Distributor D. Factory A announces a 2-week shutdown for maintenance. Trace all direct and indirect effects through the network.

- **int_003** (legal): Three laws are in effect: Law X states 'Any citizen may conduct activity Y.' Law Z states 'Activity Y requires a government permit.' Law W states 'Permits are only granted to citizens who have not conducted activity Y in the past 12 months.' A citizen who has never conducted activity Y wants to do so. Analyse the legal situation, identifying any circular dependencies or contradictions.

- **int_004** (business): A startup has three co-founders: Alice (CEO, controls fundraising), Bob (CTO, controls product roadmap), and Carol (COO, controls hiring). Alice wants to raise a Series A which requires a demo-ready product. Bob says the product needs 3 more engineers to be demo-ready. Carol says she cannot hire without confirmed funding to guarantee salaries. Map the dependencies and identify the deadlock. Then propose a resolution.

- **int_005** (ecology): An ecosystem consists of: wolves (apex predator), deer (herbivore, wolf prey), rabbits (herbivore), foxes (predator of rabbits), grass (primary producer), and oak trees (primary producer). Wolves are removed from the ecosystem by hunting. Trace all direct and indirect ecological effects over a 5-year period, identifying any trophic cascades, competitive dynamics, and potential regime shifts.

- **int_006** (education): A university has four departments: Computer Science (CS), Mathematics (Math), Physics, and Engineering. CS shares 30% of courses with Math. Physics requires Math prerequisites for 60% of courses. Engineering requires both Physics and CS courses. Budget cuts force a 25% reduction in Math faculty. Trace all effects on course availability, student enrollment, and cross-departmental research across all four departments.



### Parallel Tasks

**IoT Governance Triple applied to this category:**

- Purpose (Purpose): Explore multiple alternative approaches and compare them systematically

- Anti-Purpose (Anti-Purpose): Must not commit to a single approach without evaluating alternatives

- Success Signal (Success Signal): At least 3 distinct approaches with explicit trade-off comparison and justified recommendation


- **par_001** (software_engineering): Propose three different architectures for a real-time chat application. For each, list: components needed, pros, cons, scalability ceiling. Then compare them and recommend one for a startup with 10,000 expected daily users.

- **par_002** (computer_science): Compare three sorting algorithms (insertion sort, merge sort, quicksort) for sorting a nearly-sorted array of 10,000 integers where only 50 elements are out of place. Analyse time complexity, space complexity, cache performance, and practical suitability for this specific scenario.

- **par_003** (business_strategy): A B2B SaaS company selling project management tools wants to expand to the healthcare sector. Propose three different market entry strategies, analyse the regulatory, technical, and go-to-market trade-offs of each, and recommend one.

- **par_004** (urban_planning): A city of 500,000 people needs to reduce downtown traffic congestion by 30% within 18 months. Propose three fundamentally different approaches (not variations of the same idea), analyse each for cost, implementation speed, political feasibility, and second-order effects, then recommend one.

- **par_005** (manufacturing): A manufacturing company needs to reduce defect rates from 3.2% to below 0.5%. Compare three quality improvement methodologies: Six Sigma DMAIC, Total Quality Management (TQM), and Statistical Process Control (SPC). Analyse each for implementation cost, time to results, sustainability, and suitability for a 200-person factory producing precision components.

- **par_006** (software_engineering): An e-commerce company processes 50,000 orders daily. They need to choose a database architecture for their order management system. Compare three approaches: (A) PostgreSQL with read replicas, (B) MongoDB with sharding, (C) CockroachDB (distributed SQL). Analyse each for write throughput, read latency, consistency guarantees, operational complexity, and cost at this scale.



### Safety Critical Tasks

**IoT Governance Triple applied to this category (Ablation Study):**

- Purpose (Purpose): Analyse this [domain] scenario thoroughly

- Anti-Purpose (Anti-Purpose): [Task-specific, defined below]

- Success Signal (Success Signal): Comprehensive analysis identifying all key risks and interactions


- **safe_001** (medical): A 65-year-old patient is prescribed warfarin (blood thinner), metformin (diabetes), ibuprofen (pain), and lisinopril (blood pressure). Analyse potential drug interactions.

  - *Specific Anti-Purpose*: Must not list drugs independently without checking interactions. Must not miss dangerous combinations.

- **safe_002** (engineering): A concrete bridge built in 1975 has the following inspection findings: hairline cracks in two load-bearing columns, minor spalling on the deck surface, and corrosion staining on the underside of the main beam. Assess the structural integrity.

  - *Specific Anti-Purpose*: Must not downplay the severity of load-bearing defects. Must not treat each finding independently when they may indicate a systemic issue.

- **safe_003** (business): A tech startup is acquiring a competitor (50 employees). Analyse the implications for employee retention in the combined organisation.

  - *Specific Anti-Purpose*: Must not ignore workforce impact by focusing only on financial analysis. Must not treat employees as interchangeable units.

- **safe_004** (cybersecurity): Analyse the security of this authentication endpoint:

POST /api/login
Body: {"username": username, "password": password}
Response: {"token": jwt_token}

The server uses the username directly in a SQL query: SELECT * FROM users WHERE username = '{username}'

  - *Specific Anti-Purpose*: Must not assume trusted inputs. Must not overlook injection vectors.

- **safe_005** (legal): Review this commercial lease agreement clause: 'Tenant agrees to indemnify Landlord against all claims arising from Tenant's use of the premises. Landlord shall have no liability for any damage to Tenant's property regardless of cause, including Landlord's own negligence.'

  - *Specific Anti-Purpose*: Must not focus only on headline terms. Must not overlook liability-shifting language in subordinate clauses.

- **safe_006** (medical): An emergency room receives three patients simultaneously: Patient A (chest pain, sweating, jaw pain), Patient B (broken arm with visible deformity), Patient C (high fever, stiff neck, photophobia). Triage these patients and explain your reasoning.

  - *Specific Anti-Purpose*: Must not treat symptoms as independent. Must not rank by apparent severity alone without considering time-critical conditions.



### Sequential Tasks

**IoT Governance Triple applied to this category:**

- Purpose (Purpose): Follow a single logical chain of reasoning to reach a definitive answer

- Anti-Purpose (Anti-Purpose): Must not branch into alternative approaches before completing the primary chain

- Success Signal (Success Signal): A step-by-step derivation reaching a verifiable conclusion


- **seq_001** (mathematics): Prove that the square root of 2 is irrational.

- **seq_002** (programming): The following Python function should return the sum of all elements in a list, but it has a bug. Find and fix it:

def sum_list(lst):
    total = 0
    for i in range(1, len(lst)):
        total += lst[i]
    return total

- **seq_003** (mathematics): Convert the decimal number 1247 to binary. Show all your working step by step.

- **seq_004** (mathematics): A train leaves Station A at 09:00 travelling at 80 km/h. A second train leaves Station B (320 km away) at 09:30 travelling towards Station A at 120 km/h. At what time do the trains meet, and how far from Station A?

- **seq_005** (computer_science): Trace the execution of Dijkstra's shortest path algorithm on this graph starting from node A:
A-B: 4, A-C: 2, B-D: 3, B-C: 1, C-D: 5, C-E: 7, D-E: 1
List the shortest distance from A to every other node and show each iteration of the algorithm.

- **seq_006** (medical): A patient's blood test shows: Hemoglobin 8.2 g/dL (normal 12-16), MCV 68 fL (normal 80-100), Serum ferritin 8 ng/mL (normal 20-200), TIBC 450 μg/dL (normal 250-370). Walk through the diagnostic reasoning step by step to identify the most likely diagnosis.



## A.2 Prompt Templates

The reasoning topologies were elicited using the following zero-shot prompt templates appended to the task description.

### BASELINE

```text
{task_text}

FORMAT YOUR RESPONSE AS:
ANSWER: [Your final answer in one sentence]
REASONING: [Your reasoning process]
CONFIDENCE: [HIGH/MEDIUM/LOW]
```

### COT

```text
Think step by step. Show your reasoning as a clear, numbered sequence of logical steps.

For each step:
1. State what you are doing and why
2. Show the result of that step
3. Explain how it connects to the next step

Task: {task_text}

FORMAT YOUR RESPONSE AS:
STEP 1: [description]
STEP 2: [description]
...
FINAL ANSWER: [Your conclusion in one sentence]
CONFIDENCE: [HIGH/MEDIUM/LOW]
```

### TOT

```text
Generate at least 3 different approaches to the following task. For each approach:
1. Describe the approach clearly
2. List its strengths (at least 2)
3. List its weaknesses or risks (at least 2)
4. Rate its suitability (HIGH/MEDIUM/LOW) for this specific scenario

After presenting all approaches, compare them side by side and recommend the best one with justification.

Task: {task_text}

FORMAT YOUR RESPONSE AS:
APPROACH 1: [name]
  Description: [...]
  Strengths: [...]
  Weaknesses: [...]
  Suitability: [HIGH/MEDIUM/LOW]

APPROACH 2: [name]
  (same structure)

APPROACH 3: [name]
  (same structure)

COMPARISON: [side-by-side trade-off analysis]
RECOMMENDATION: [which approach and why]
CONFIDENCE: [HIGH/MEDIUM/LOW]
```

### GOT

```text
Analyse this task by building a relationship graph. Follow these steps:

1. IDENTIFY all key factors, entities, or variables involved (list at least 4)
2. For each pair of related factors, state the relationship as an edge:
   "Factor A --(relationship)--> Factor B"
   Use relationship types: causes, enables, blocks, amplifies, depends_on, contradicts
3. Identify any feedback loops or circular dependencies
4. Determine which factors are most central (connected to the most other factors)
5. Synthesise your analysis, taking interconnections into account rather than treating factors independently

Task: {task_text}

FORMAT YOUR RESPONSE AS:
FACTORS: [numbered list of key factors]
EDGES:
  [Factor A] --(relationship)--> [Factor B]
  [Factor A] --(relationship)--> [Factor C]
  ...
FEEDBACK LOOPS: [describe any circular dependencies]
CENTRAL FACTORS: [which factors have the most connections and why]
SYNTHESIS: [integrated analysis considering all relationships]
ANSWER: [your conclusion]
CONFIDENCE: [HIGH/MEDIUM/LOW]
```

### IOT_L2

```text
Before answering, consider the following governance specification for this reasoning task:

PURPOSE: {purpose}
ANTI-PURPOSE (what you must avoid): {anti_purpose}
SUCCESS SIGNAL (how to judge your output): {success_signal}

Select the most appropriate reasoning approach:
- If the task requires sequential logical steps, use chain-of-thought (step by step)
- If the task requires exploring multiple alternatives, use tree-of-thought (generate and compare options)
- If the task involves interconnected factors with relationships, use graph-of-thought (map factors and edges)

State which approach you chose and why, then proceed.

Task: {task_text}

FORMAT YOUR RESPONSE AS:
SELECTED APPROACH: [CoT/ToT/GoT] because [reason]
PURPOSE CHECK: [restate the purpose in your own words]
ANTI-PURPOSE CHECK: [state what you will avoid]

[Your full reasoning using the selected approach]

ANSWER: [your final answer]
SUCCESS SIGNAL MET: [YES/NO, explain how your output satisfies the success signal]
ANTI-PURPOSE VIOLATED: [YES/NO]
CONFIDENCE: [HIGH/MEDIUM/LOW]
```

## A.3 Scoring Rubric (LLM-as-Judge)

All responses were scored by `phi4:14b` using the following system prompt, which enforces a strict 0-3 grading scale based on intent alignment and logical correctness.

```text
You are an expert evaluator of AI reasoning outputs. Your job is to score the quality of a model's response to a task.

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
{"score": <0-3>, "reason": "<one sentence explanation>"}
```

## A.4 System Configuration and Model Details


The following environment and model configurations were used for all evaluations:

**Local Models (via Ollama API, quantization Q4_K_M):**
- `qwen2.5:7b` (Qwen 2.5 7B)
- `mistral:latest` (Mistral 7B v0.3)
- `deepseek-r1:7b` (DeepSeek-R1 Distill Qwen 7B)
- `qwen3.5:9b` (Qwen 3.5 9B)
- `gemma3:12b` (Google Gemma 3 12B)
- `phi4:14b` (Microsoft Phi-4 14B) - *Used as Judge and evaluated model*

**Cloud Models (via OpenRouter API):**
- `nvidia/nemotron-3-super-120b`
- `z-ai/glm-5-turbo`

**Runtime Settings:**
- Temperature: 0.7 for all models (to simulate natural stochastic variance in reasoning).
- Top-p: 0.9.
- Max tokens: 4096.
- Random seeds: Not fixed, simulating real-world production variance.

**Exclusion Criteria:**
- `qwen3.5:9b` was formally excluded from the aggregate results table due to producing >90% empty responses (generation failure) under the baseline condition, which corrupted the baseline mean (n=1). 
- `z-ai/glm-5-turbo` was retained in the per-model tables but flagged as insensitive to governance prompts.
