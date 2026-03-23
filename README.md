# HFA AI Training

**A comprehensive seminar on building with AI — from agents to pipelines to vision.**

This repository contains all materials, code examples, and guides for the HFA AI Training seminar. Each section builds on the previous one, taking you from foundational agent building through advanced vision-language models.

---

## Table of Contents

| Section | Topic |
|---------|-------|
| [01 - Building Agents](./01-building-agents/) | Prompting, TDD, context windows, model selection, few-shot examples |
| [02 - Agent Pipelines](./02-agent-pipelines/) | Chaining agents, ML + LLMs, LLM as a judge, evals with DeepEval |
| [03 - Vector Databases](./03-vector-databases/) | Embeddings, semantic search, Pinecone |
| [04 - RAG Agents](./04-rag-agents/) | Retrieval Augmented Generation, grounding LLMs in your data |
| [05 - MCP](./05-mcp/) | Model Context Protocol, giving agents tools and real-world capabilities |
| [06 - VLMs](./06-vlms/) | Vision Language Models, Gemini, robotics, VLM + MCP architectures |
| [07 - Summary](./07-summary/) | Recap, key takeaways, learning path, and what to build next |

---

## Prerequisites

Before the seminar, make sure you have the following set up:

### Software
- **Python 3.10+** (check with `python --version` or `python3 --version`)
- **pip** (comes with Python)
- **Git** (to clone this repo)
- A code editor (VS Code recommended)

### API Keys
You will need API keys for at least one of the following providers. We will use both during the seminar:

| Provider | Sign Up | Used For |
|----------|---------|----------|
| OpenAI (GPT-4o) | [platform.openai.com](https://platform.openai.com/) | Code generation, analysis, agent building, reasoning, embeddings, evals |
| Google AI (Gemini) | [aistudio.google.com](https://aistudio.google.com/) | Vision, multimodal tasks |
| Pinecone | [app.pinecone.io](https://app.pinecone.io/) | Vector database for semantic search and RAG |

Set your keys as environment variables:

```bash
export OPENAI_API_KEY="your-key-here"
export GOOGLE_API_KEY="your-key-here"
export PINECONE_API_KEY="your-key-here"
```

Or create a `.env` file in the repo root (already in `.gitignore`):

```
OPENAI_API_KEY=your-key-here
GOOGLE_API_KEY=your-key-here
PINECONE_API_KEY=your-key-here
```

---

## Quick Setup

```bash
# Clone the repository
git clone https://github.com/charlie-robison/hfa-ai-training.git
cd hfa-ai-training

# Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt
```

---

## Section Descriptions

### 01 - Building Agents
The foundation of everything that follows. Learn how to write effective prompts, structure agent interactions with few-shot examples, choose the right model for the task, and apply test-driven development to AI. The core principle: agents reason well but need evidence to make good decisions.

### 02 - Agent Pipelines
Single agents have limits. Pipelines break complex tasks into stages where each agent handles one responsibility. Learn to chain agents together, combine traditional ML with LLMs, use one model to judge another, and measure quality with DeepEval's deterministic, hallucination, and evidence-based evaluations.

### 03 - Vector Databases
Before you can do retrieval, you need to understand how machines represent meaning. Explore embeddings for words, sentences, and images. Build semantic search with Pinecone that finds results by meaning, not just keywords. Learn when vector databases are the right choice and when they are not.

### 04 - RAG Agents
Retrieval Augmented Generation is the pattern that connects LLMs to your actual data. Build agents that search a knowledge base, retrieve relevant context, and generate grounded answers with citations. This is the most practical pattern for making AI useful in a business context.

### 05 - MCP (Model Context Protocol)
MCP gives agents the ability to act, not just think. Learn to wrap existing tools and APIs behind a standardized protocol, give agents controlled access to real systems, and manage the security and permission tradeoffs that come with autonomous tool use.

### 06 - VLMs (Vision Language Models)
Vision is the next frontier. Explore Gemini's capabilities as the leading VLM, understand the robotics potential of visual AI, and build architectures that pair VLMs with MCP tools to create agents that can both see and act — the "Brain" pattern.

### 07 - Summary
A complete recap of all six topics, the eight key principles that tie everything together, a recommended learning path, useful resources, and project ideas for what to build next.

---

## How to Follow Along

During the seminar, we will work through each section in order. Here is how to get the most out of it:

1. **Have the repo open** in your editor alongside the presentation.
2. **Run the examples** as we go through them. Each section folder contains code you can execute.
3. **Modify and experiment.** The best way to learn is to change something and see what happens.
4. **Ask questions.** If something is unclear, stop me. If it is unclear to you, it is probably unclear to someone else too.
5. **Take notes in context.** Add comments directly in the code files so your notes live next to the examples.

Each section's README contains the concepts and walkthrough. Code files in each folder are labeled and ordered for easy reference.

---

## Repository Structure

```
hfa-ai-training/
├── README.md                  # You are here
├── requirements.txt           # Python dependencies
├── 01-building-agents/        # Prompting, TDD, model selection
├── 02-agent-pipelines/        # Chaining agents, evals, ML + LLMs
├── 03-vector-databases/       # Embeddings, semantic search, Pinecone
├── 04-rag-agents/             # Retrieval Augmented Generation
├── 05-mcp/                    # Model Context Protocol
├── 06-vlms/                   # Vision Language Models
└── 07-summary/                # Recap and next steps
```

---

## Credits

**HFA AI Training Seminar**

Created by Charlie Robison.

For questions, issues, or follow-up after the seminar, open an issue in this repository or reach out directly.
