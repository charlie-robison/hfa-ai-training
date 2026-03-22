# Module 2: Agent Pipelines

## Overview

An **agent pipeline** is a chain of multiple AI agents (or processing steps) where the output of one step becomes the input of the next. Think of it like an assembly line: each station has a specific job, and the work product moves forward through each stage until it's complete.

This is how production AI systems actually work. A single LLM call is rarely enough. Real applications chain together multiple agents, ML models, and evaluation steps to produce reliable results.

---

## Table of Contents

1. [What Is an Agent Pipeline?](#what-is-an-agent-pipeline)
2. [Inputs and Outputs Between Agents](#inputs-and-outputs-between-agents)
3. [Combining ML with LLMs](#combining-ml-with-llms)
4. [LLM as a Judge](#llm-as-a-judge)
5. [Evals with DeepEval](#evals-with-deepeval)
6. [Types of Evaluations](#types-of-evaluations)
7. [Pipeline Design Patterns](#pipeline-design-patterns)
8. [Error Handling in Pipelines](#error-handling-in-pipelines)
9. [Code Examples](#code-examples)

---

## What Is an Agent Pipeline?

A pipeline chains multiple agents or processing steps together in sequence (or in parallel). Each agent has a focused responsibility:

```
[Research Agent] --> [Analysis Agent] --> [Writing Agent] --> Final Output
```

**Why pipelines?**
- **Separation of concerns**: Each agent does one thing well
- **Debuggability**: You can inspect the output at each stage
- **Reliability**: If one stage fails, you know exactly where to look
- **Composability**: You can swap out or upgrade individual stages without rewriting the whole system

**Real-world analogy**: A real estate transaction pipeline might look like:
```
[Lead Scoring ML Model] --> [Property Matching Agent] --> [Email Draft Agent] --> [Quality Check Agent]
```

---

## Inputs and Outputs Between Agents

### The Core Principle

The output of Agent A becomes the input of Agent B. This is the fundamental concept.

```
Agent A produces output --> That output is formatted --> Agent B receives it as input
```

### JSON Is King

When passing data between agents, **JSON is the standard serialization format**. Why?

- **Structured**: Both humans and machines can read it
- **Universal**: Every programming language can parse it
- **LLM-friendly**: LLMs are very good at reading and producing JSON
- **Typed**: You can validate the shape of data between steps

```python
# Output from Stage 1 (Research Agent)
stage_1_output = {
    "topic": "Hawaii real estate market 2026",
    "key_findings": [
        "Median home price increased 4.2% YoY",
        "Inventory remains tight at 2.1 months supply",
        "Interest rates stabilized around 5.8%"
    ],
    "sources": ["HAR MLS Data", "Zillow Research", "Fed Reserve"],
    "confidence_score": 0.87
}

# This JSON becomes the input for Stage 2 (Analysis Agent)
```

### Serialization Best Practices

1. **Always use JSON between stages** -- not plain text, not XML
2. **Define a schema for each stage's output** -- know what shape to expect
3. **Include metadata** -- timestamps, confidence scores, source references
4. **Keep payloads focused** -- only pass what the next stage needs

---

## Combining ML with LLMs

### The Key Lesson

> **Use ML for scoring and classification. Use LLMs for reasoning about those scores.**

This is one of the most powerful patterns in production AI:

| ML Models | LLMs |
|-----------|------|
| Fast and cheap | Slower and more expensive |
| Great at classification | Great at reasoning |
| Deterministic outputs | Flexible, natural language outputs |
| Needs training data | Works with prompts |
| Produces scores/labels | Produces explanations/decisions |

### The Pattern

```
[Raw Data] --> [ML Model: scores/classifies] --> [LLM: reasons about scores] --> [Decision]
```

### Example: Lead Scoring Pipeline

1. **ML Model** (scikit-learn classifier) scores a lead 0-100 based on features:
   - Days since last contact: 3
   - Website visits this week: 7
   - Email open rate: 0.65
   - Property views: 12
   - **ML Score: 82/100 (Hot Lead)**

2. **LLM** receives the score and features, then reasons:
   > "This lead scores 82/100. They've visited the site 7 times this week and viewed 12 properties, suggesting active buying intent. Their high email engagement (65%) means they're responsive. Recommended action: Call today with the 3 new Kailua listings that match their search criteria."

The ML model does the math. The LLM does the thinking.

### Why Not Just Use the LLM for Everything?

- LLMs are **expensive** -- running a classifier on 10,000 leads costs pennies; 10,000 LLM calls costs dollars
- LLMs **hallucinate** -- a classifier gives you a real score based on real data
- ML models are **consistent** -- same input always produces same output
- LLMs add **reasoning** -- they explain the "why" behind the numbers

See `ml_plus_llm_pipeline.py` for a working example.

---

## LLM as a Judge

### What Is It?

Using one LLM to evaluate the output of another LLM. This is how you build quality control into your pipelines.

```
[LLM A: generates response] --> [LLM B: judges the response] --> [Score + Feedback]
```

### Why Use LLM as a Judge?

- **Scalable**: You can evaluate thousands of outputs automatically
- **Consistent criteria**: The judge uses the same rubric every time
- **Catches issues**: Hallucinations, irrelevance, incomplete answers
- **Cheaper than humans**: For initial quality gates, LLM judges are cost-effective

### Judge Prompt Structure

A good judge prompt includes:

1. **The original question/task**
2. **The generated response to evaluate**
3. **Scoring criteria** (explicit rubric)
4. **Output format** (structured scores)

```python
judge_prompt = """
You are evaluating an AI-generated response. Score it on these criteria:

CRITERIA:
- Accuracy (1-5): Are the facts correct?
- Relevance (1-5): Does it answer the actual question?
- Completeness (1-5): Does it cover all important aspects?
- Clarity (1-5): Is it well-written and easy to understand?

ORIGINAL QUESTION: {question}

RESPONSE TO EVALUATE: {response}

Provide scores and brief justification for each. Return as JSON.
"""
```

### Important Caveats

- LLM judges have biases (they tend to prefer longer, more verbose responses)
- Always validate your judge against human evaluations first
- Use specific, measurable criteria -- not vague ones like "is it good?"
- Consider using a stronger model as the judge (e.g., Claude Opus judging Claude Haiku outputs)

See `llm_as_judge.py` for a working example.

---

## Evals with DeepEval

### Strongly Recommended: DeepEval

**DeepEval** is the go-to framework for LLM evaluations. Think of it as "pytest for LLMs."

- GitHub: https://github.com/confident-ai/deepeval
- Docs: https://docs.confident-ai.com

### Why DeepEval?

1. **Pre-built metrics**: Hallucination, relevancy, faithfulness, toxicity, and more
2. **Works with any LLM**: Not locked to a specific provider
3. **Pytest integration**: Runs evals as part of your test suite
4. **Confident AI dashboard**: Visual tracking of eval results over time
5. **Production-ready**: Used by real companies in production

### Quick Start

```bash
pip install deepeval
```

```python
from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import HallucinationMetric, AnswerRelevancyMetric

# Create a test case
test_case = LLMTestCase(
    input="What is the median home price in Hawaii?",
    actual_output="The median home price in Hawaii is $750,000.",
    context=["The median home price in Hawaii as of 2025 is $742,500."]
)

# Run metrics
hallucination_metric = HallucinationMetric(threshold=0.5)
relevancy_metric = AnswerRelevancyMetric(threshold=0.7)

evaluate(test_cases=[test_case], metrics=[hallucination_metric, relevancy_metric])
```

See `deepeval_example.py` for a full working example.

---

## Types of Evaluations

### 1. Deterministic Evals

These are traditional software tests -- exact, reproducible, no ambiguity.

| Method | What It Checks | Example |
|--------|---------------|---------|
| **Exact match** | Output equals expected string | `output == "Yes"` |
| **Contains** | Output includes required text | `"Hawaii" in output` |
| **Regex** | Output matches a pattern | `re.match(r'\$[\d,]+', output)` |
| **JSON schema** | Output has correct structure | Validates keys and types |

**When to use**: Format validation, structured output checks, simple factual verification.

### 2. Hallucination Detection

Checking whether the LLM made something up that isn't supported by the provided context.

- **Faithfulness**: Does the output only contain info from the provided context?
- **Factual consistency**: Are the claims in the output consistent with known facts?
- **Source attribution**: Can every claim be traced back to a source?

**When to use**: Any time the LLM is supposed to answer based on provided documents or data. Critical for RAG systems.

### 3. Evidence-Based Evals

Does the LLM's output match the provided evidence/facts?

- Give the LLM specific facts (e.g., "The property is 2,400 sq ft, built in 1998, 4 bed/3 bath")
- Check that the output accurately reflects those facts
- Flag any additions, omissions, or contradictions

**When to use**: When the LLM is summarizing, reporting, or making decisions based on specific data.

### Summary Table

| Eval Type | Speed | Cost | Best For |
|-----------|-------|------|----------|
| Deterministic | Instant | Free | Format, structure, simple facts |
| Hallucination | Moderate | LLM call | RAG, document-based answers |
| Evidence-based | Moderate | LLM call | Data-driven outputs, reports |

---

## Pipeline Design Patterns

### 1. Sequential Pipeline

The simplest pattern. Each step runs after the previous one completes.

```
[Step 1] --> [Step 2] --> [Step 3] --> Output
```

**Use when**: Each step depends on the previous step's output.

### 2. Parallel Pipeline

Multiple steps run at the same time, then results are combined.

```
         /--> [Step A] --\
[Input] ----> [Step B] ----> [Combine] --> Output
         \--> [Step C] --/
```

**Use when**: Steps are independent and you want speed. Example: researching multiple topics simultaneously.

### 3. Branching Pipeline

Different paths based on conditions (like an if/else for agents).

```
                    /--> [Path A] --> Output A
[Input] --> [Router]
                    \--> [Path B] --> Output B
```

**Use when**: Different inputs need different processing. Example: routing customer inquiries to different specialist agents.

### 4. Loop Pipeline (Iterative Refinement)

Output is fed back in for improvement until quality threshold is met.

```
[Input] --> [Generate] --> [Evaluate] --[pass]--> Output
                ^              |
                |--[fail]------/
```

**Use when**: You need high-quality output and can iterate. Example: drafting and refining an email until it scores above 4/5.

---

## Error Handling in Pipelines

Pipelines fail. Plan for it.

### Best Practices

1. **Wrap each stage in try/except** -- don't let one stage crash the whole pipeline
2. **Log intermediate outputs** -- so you can debug where things went wrong
3. **Set timeouts** -- LLM calls can hang; always set a max wait time
4. **Validate between stages** -- check that Stage N's output is valid before passing to Stage N+1
5. **Have fallbacks** -- if the LLM call fails, have a default response or retry logic
6. **Retry with backoff** -- transient API errors happen; retry 2-3 times with exponential backoff

```python
import time

def run_stage_with_retry(stage_fn, input_data, max_retries=3):
    """Run a pipeline stage with retry logic."""
    for attempt in range(max_retries):
        try:
            result = stage_fn(input_data)
            # Validate output before returning
            if result is None:
                raise ValueError("Stage returned None")
            return result
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                print(f"Stage failed (attempt {attempt + 1}): {e}. Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"Stage failed after {max_retries} attempts: {e}")
                raise
```

---

## Code Examples

| File | What It Demonstrates |
|------|---------------------|
| `simple_pipeline.py` | A 3-stage sequential pipeline (Research -> Analysis -> Writing) |
| `ml_plus_llm_pipeline.py` | Combining scikit-learn ML scoring with LLM reasoning |
| `llm_as_judge.py` | Using one LLM to evaluate another LLM's output |
| `deepeval_example.py` | Production evaluation using the DeepEval framework |

### Running the Examples

```bash
# Install dependencies
pip install anthropic scikit-learn deepeval numpy

# Set your API key
export ANTHROPIC_API_KEY="your-key-here"

# Run individual examples
python simple_pipeline.py
python ml_plus_llm_pipeline.py
python llm_as_judge.py
python deepeval_example.py
```

---

## Key Takeaways

1. **Pipelines chain agents together** -- output of one becomes input of the next
2. **JSON is the glue** -- always pass structured data between stages
3. **ML + LLM is the power combo** -- ML scores, LLM reasons about the scores
4. **Always evaluate your outputs** -- LLM as a Judge + DeepEval for production
5. **Three types of evals**: Deterministic (exact), Hallucination (made up?), Evidence-based (matches facts?)
6. **Plan for failure** -- retries, timeouts, validation between stages
7. **Start simple, add complexity** -- begin with a sequential pipeline, then add parallelism and branching as needed
