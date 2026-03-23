# HFA AI Training

**A hands-on seminar on building with AI — from agents to pipelines to vision.**

---

## Table of Contents

| Section | Topic |
|---------|-------|
| [01 - Coding With Claude](./01-coding-with-claude/) | CLAUDE.md, rules, and skills for Claude Code |
| [02 - Building Agents](./02-building-agents/) | LLM calls, system prompts, few-shot examples, structured output, parallel execution |
| [03 - Vector Databases](./03-vector-databases/) | Embeddings, Pinecone, semantic search with metadata filters |
| [04 - RAG Agents](./04-rag-agents/) | Retrieval Augmented Generation — ground LLM answers in real data |
| [05 - MCP](./05-mcp/) | Model Context Protocol — give LLMs tools they can call |
| [06 - VLMs](./06-vlms/) | Vision Language Models — depth maps and distance estimation with Gemini |
| [07 - Pipelines](./07-pipelines/) | Multi-stage agent pipelines |

---

## Prerequisites

- **Python 3.10+**
- **pip**
- API keys for OpenAI, Google AI (Gemini), and Pinecone

Create a `.env` file in the repo root (already in `.gitignore`):

```
OPENAI_API_KEY=your-key-here
GOOGLE_API_KEY=your-key-here
PINECONE_API_KEY=your-key-here
```


## Quick Setup

# Clone the repository
git clone https://github.com/charlie-robison/hfa-ai-training.git
python3 -m venv .venv
source .venv/bin/activate
# Install all dependencies
pip install -r requirements.txt
```

---

## Section Descriptions

### 01 - Coding With Claude

Examples of how to configure Claude Code for a project. No notebooks — just reference files you can copy into your own projects.

**Files:**
- `example-claude-md.md` — A complete CLAUDE.md for a Python analytics project. Covers tech stack, coding conventions, common commands, domain knowledge, and things to avoid.
- `example-rules/code-style.md` — Python style rules (naming, type hints, formatting). Loaded every session.
- `example-rules/testing.md` — Test commands and conventions (`pytest`, unit vs integration). Loaded every session.
- `example-rules/api-endpoints.md` — API conventions scoped to `src/api/**/*.py` only. Uses `paths` frontmatter so it only loads when Claude works on API files.
- `example-skills/deploy/SKILL.md` — A manual-only deploy skill (`/deploy`). `disable-model-invocation: true` prevents Claude from triggering it automatically.
- `example-skills/review-pr/SKILL.md` — A PR review skill that runs in a forked Explore subagent. Claude can invoke it automatically or you can call `/review-pr 123`.
- `example-skills/fix-issue/SKILL.md` — Fix a GitHub issue by number (`/fix-issue 456`). Reads the issue, implements the fix, writes tests, commits.

---

### 02 - Building Agents

One notebook (`basic_agent.ipynb`) that demonstrates the core pattern: pass evidence into a prompt and get structured output back. Uses a grocery promotional lift analysis example.

**What it covers:**
- **System prompt** with few-shot examples — two complete input/output examples (one profitable promo → repeat, one unprofitable → discontinue) that teach GPT-4o the exact JSON schema and reasoning depth
- **Evidence-based prompting** — real promotion data (SKU, baseline units, lift %, margin, cannibalization, post-promo demand) injected into the user prompt via f-string
- **Structured JSON output** — `response_format={"type": "json_object"}` guarantees valid JSON with fields: `sku`, `profitable`, `incremental_profit`, `recommendation`, `next_steps`, `future_changes`, `reasoning`
- **`max_completion_tokens`** — caps output length to control cost
- **Token usage tracking** — prints prompt/completion/total tokens after each call
- **Reusable method** — `analyze_promotion(promo)` takes a dict, returns structured JSON
- **Parallel execution** — `analyze_promotion_async()` + `asyncio.gather()` runs 5 promotions concurrently (~5x faster than sequential)

**Three cells:**
1. Method definitions (sync + async) with system prompt and few-shot examples
2. Single call with one granola promotion
3. Parallel call with 5 different promotions (granola, ground beef, kettle chips, cold brew, baby spinach)

---

### 03 - Vector Databases

One notebook (`vector_search.ipynb`) that embeds grocery product documents into Pinecone and runs semantic search.

**What it covers:**
- **12 products** across 3 categories: eggs (4), milk (4), bread (4) — each with detailed descriptions, prices, nutrition info, and an organic flag
- **OpenAI embeddings** — `text-embedding-3-small` (1536 dimensions) generates vectors for all product descriptions in one batch
- **Pinecone index** — create a serverless index, upsert vectors with metadata (name, category, price, organic, text)
- **Semantic search** — `search()` helper embeds a query and returns top-k results ranked by cosine similarity
- **Meaning-based matching** — "high protein low fat for working out" finds liquid egg whites and oat milk even though "workout" doesn't appear in the text
- **Metadata filters** — combine semantic search with structured filters: organic-only, bread under $5, eggs-only
- **Cleanup** — deletes the index at the end to avoid charges

---

### 04 - RAG Agents

One notebook (`rag_agent.ipynb`) that uses the same 12 grocery products but adds an LLM generation step on top of retrieval.

**What it covers:**
- **Same product catalog** as the vector search notebook — identical data, same Pinecone setup
- **`ask()` method** — the RAG core in one function:
  1. Embed the question with OpenAI
  2. Query Pinecone for the top-4 most relevant products
  3. Build an augmented prompt with the retrieved product data
  4. Send to GPT-4o with a system prompt that says "answer using ONLY the provided products"
  5. Print which products were retrieved and the LLM's answer
- **5 example questions** that show RAG in action:
  - "I'm training for a marathon and need high-protein, low-fat options"
  - "My kid has a gluten allergy and is lactose intolerant. What can they eat for breakfast?"
  - "I want to make a nice brunch. What eggs and bread would pair well together?"
  - "What's the cheapest option in each category?"
  - "Compare the organic products — are they worth the extra cost?"
- **Grounded answers** — the LLM cites specific product names, prices, and nutrition facts from the retrieved context instead of making things up

---

### 05 - MCP (Model Context Protocol)

One MCP server (`grocery_mcp_server.py`) and one notebook (`mcp_overview.ipynb`) that explains how it works.

**The server exposes 3 tools:**
- **`search_products`** — keyword search across 9 grocery products with optional category filter (eggs/milk/bread)
- **`get_nutrition`** — returns calories, protein, fat, organic status, and price for a product by ID
- **`check_stock`** — checks inventory at 3 store locations (downtown, westside, eastside) — some products are out of stock at certain stores

**The notebook:**
- Reads and prints the full server source code so you can study it
- Simulates each tool call by importing the server's data and running the logic directly
- Shows how to configure Claude Desktop to use the server (JSON config + full Python path)

**How to use it for real:**
Add this to `~/Library/Application Support/Claude/claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "grocery": {
      "command": "/path/to/your/.venv/bin/python",
      "args": ["/path/to/hfa-ai-training/05-mcp/grocery_mcp_server.py"]
    }
  }
}
```
Restart Claude Desktop. The LLM can now search products, check nutrition, and look up stock levels.

---

### 06 - VLMs (Vision Language Models)

One notebook (`vision_distance.ipynb`) that generates a depth map from an image and passes both the original and depth map to Gemini to estimate box distances.

**What it covers:**
- **Depth-Anything-V2** — runs the `depth-anything/Depth-Anything-V2-Small-hf` model locally via `transformers` pipeline to generate a depth map from any image
- **Side-by-side display** — matplotlib shows the original image and depth map (bright = close, dark = far) next to each other
- **Gemini 2.5 Flash** — receives BOTH images (original + depth map) and a prompt asking it to identify every box/pallet, using the depth map to improve distance estimates
- **Structured JSON output** — returns `box_count`, per-box `distance_ft`, `size`, `position`, `labels`, `description`, and a `scene_description`
- **New `google-genai` SDK** — uses `from google import genai` (the old `google.generativeai` package is deprecated)

---

### 07 - Pipelines

Multi-stage agent pipelines (coming soon).

---

## Repository Structure

```
hfa-ai-training/
├── .env                          # API keys (not committed)
├── README.md                     # This file
├── requirements.txt              # Python dependencies
├── 01-coding-with-claude/        # CLAUDE.md, rules, and skills examples
├── 02-building-agents/           # LLM agent with structured output
│   └── basic_agent.ipynb
├── 03-vector-databases/          # Embeddings + Pinecone semantic search
│   └── vector_search.ipynb
├── 04-rag-agents/                # Retrieval Augmented Generation
│   └── rag_agent.ipynb
├── 05-mcp/                       # Model Context Protocol
│   ├── grocery_mcp_server.py
│   └── mcp_overview.ipynb
├── 06-vlms/                      # Vision Language Models + depth estimation
│   └── vision_distance.ipynb
└── 07-pipelines/                 # Agent pipelines
```

---

## Credits

**HFA AI Training Seminar** — Created by Charlie Robison.
