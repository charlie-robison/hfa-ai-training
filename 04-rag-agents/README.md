# 04 - RAG Agents (Retrieval Augmented Generation)

## What is RAG?

**Retrieval Augmented Generation (RAG)** is a technique that gives LLMs access to external knowledge by retrieving relevant documents and injecting them into the prompt before the model generates a response.

In plain English: instead of hoping the LLM "knows" the answer, you **look up** the answer in your own data first, hand it to the LLM, and say _"answer based on this."_

---

## The Problem RAG Solves

LLMs have a fundamental limitation: **they only know what they were trained on.**

They do NOT know:
- Your company's internal policies
- Your product documentation
- Your customer data
- Anything that happened after their training cutoff
- Anything private or proprietary

Without RAG, you have two bad options:

| Approach | Problem |
|---|---|
| Ask the LLM directly | It hallucinates or gives generic answers |
| Paste everything into the prompt | Context windows have limits, and it's expensive |

RAG solves this by **selectively retrieving only the relevant pieces** of your data and adding them to the prompt. The LLM gets exactly what it needs -- nothing more, nothing less.

---

## The RAG Pipeline

Here is the high-level flow:

```
 USER QUESTION
      |
      v
 +-----------+       +----------------+       +------------------+
 |  Embed    | ----> |  Vector DB     | ----> |  Retrieved Docs  |
 |  Question |       |  Similarity    |       |  (Top K chunks)  |
 +-----------+       |  Search        |       +------------------+
                     +----------------+                |
                                                       v
                                              +------------------+
                                              |  Build Augmented |
                                              |  Prompt:         |
                                              |                  |
                                              |  "Given these    |
                                              |   documents...   |
                                              |   answer this    |
                                              |   question"      |
                                              +------------------+
                                                       |
                                                       v
                                              +------------------+
                                              |  LLM Generates   |
                                              |  Grounded Answer  |
                                              +------------------+
                                                       |
                                                       v
                                                  RESPONSE
```

---

## Step-by-Step Breakdown

### Step 1: User Asks a Question

Nothing fancy here. The user types a natural language question.

```
"What is our company's return policy for electronics?"
```

### Step 2: The Question Gets Embedded

The question is converted into a **vector embedding** -- a list of numbers that captures its semantic meaning. This is the same embedding process we covered in the Vector Databases module.

```
"What is our company's return policy for electronics?"
    --> [0.12, -0.45, 0.78, 0.33, ..., -0.21]   (e.g., 1536 dimensions)
```

### Step 3: Vector DB Finds Similar Documents

The question embedding is compared against all the document embeddings stored in the vector database. The DB returns the **top K most similar** chunks.

```
Query Vector: [0.12, -0.45, 0.78, ...]
                     |
                     v
    +-----------------------------------+
    |          VECTOR DATABASE           |
    |                                    |
    |  [0.11, -0.44, 0.79, ...] = 0.97  |  <-- Return Policy doc (HIGH match)
    |  [0.15, -0.40, 0.75, ...] = 0.93  |  <-- Electronics Warranty doc
    |  [0.88, 0.22, -0.15, ...] = 0.31  |  <-- HR Vacation Policy (LOW match)
    |  [0.05, -0.50, 0.80, ...] = 0.95  |  <-- Refund Process doc
    +-----------------------------------+
                     |
                     v
         Top 3 most relevant chunks returned
```

### Step 4: Retrieved Documents Get Added to the Prompt

The retrieved chunks are injected into the LLM prompt as **context**. This is the "augmented" part of RAG.

```
SYSTEM: You are a helpful assistant. Answer the user's question based ONLY
on the provided context. If the context doesn't contain the answer, say so.

CONTEXT:
---
Document: Return Policy (Updated Jan 2026)
Electronics may be returned within 30 days of purchase with original receipt.
Items must be in original packaging and include all accessories...
---
Document: Refund Process
Refunds for electronics are processed within 5-7 business days.
Store credit is issued immediately upon return approval...
---
Document: Electronics Warranty
All electronics come with a 1-year manufacturer warranty.
Extended warranties available for purchase at point of sale...
---

USER: What is our company's return policy for electronics?
```

### Step 5: LLM Generates a Grounded Answer

The LLM reads the context and generates an answer **based on the retrieved documents**, not on its general training data. This dramatically reduces hallucination.

```
"Based on our company policy, electronics may be returned within 30 days
of purchase. You'll need the original receipt, and the item must be in its
original packaging with all accessories included. Refunds are processed
within 5-7 business days, though store credit can be issued immediately
upon return approval."
```

---

## The Two Phases of RAG

RAG has two distinct phases that happen at different times:

### Phase 1: Indexing (Happens Once / Periodically)

This is the **offline** step where you prepare your knowledge base.

```
 RAW DOCUMENTS
 (PDFs, docs, web pages, databases)
      |
      v
 +-----------+
 |  CHUNKING |  Split documents into smaller pieces
 +-----------+
      |
      v
 +-----------+
 | EMBEDDING |  Convert each chunk into a vector
 +-----------+
      |
      v
 +-----------+
 |  STORE    |  Save vectors + metadata in vector DB
 +-----------+
```

### Phase 2: Querying (Happens Every Request)

This is the **online** step that runs every time a user asks a question.

```
 QUESTION --> EMBED --> SEARCH --> RETRIEVE --> AUGMENT --> GENERATE --> ANSWER
```

---

## Why RAG Beats Fine-Tuning (For Most Use Cases)

| Factor | RAG | Fine-Tuning |
|---|---|---|
| **Data freshness** | Update anytime -- just re-index | Must retrain the model |
| **Cost** | Cheap (just a vector DB) | Expensive (GPU training) |
| **Transparency** | Can cite exact sources | Black box -- no citations |
| **Accuracy** | Grounded in real documents | Can still hallucinate |
| **Setup time** | Hours | Days to weeks |
| **Data privacy** | Data stays in your DB | Data goes into model weights |
| **Flexibility** | Swap LLMs easily | Locked to one model |

Fine-tuning is better when you need to change the model's **behavior or style** (e.g., making it write in a specific tone). RAG is better when you need to give the model **access to specific knowledge**.

---

## When to Use RAG

RAG is the right choice when:

- **Company knowledge bases** -- Let employees ask questions about internal docs, policies, and procedures
- **Document Q&A systems** -- Upload PDFs, contracts, or manuals and ask questions about them
- **Customer support bots** -- Answer customer questions based on your actual help docs and FAQs
- **Legal/compliance tools** -- Search through regulations, case law, or compliance documents
- **Product assistants** -- Help users find information about your products and services
- **Research tools** -- Search through academic papers, reports, or datasets
- **Any time you need an LLM to answer based on YOUR data**

### The Litmus Test

> "Does the answer to this question live in a specific document or dataset that the LLM wouldn't know about?"

If yes --> use RAG.

---

## When NOT to Use RAG

RAG adds complexity. Skip it when:

- **General knowledge questions** -- "What is the capital of France?" (The LLM already knows)
- **Creative tasks** -- "Write me a poem about the ocean" (No documents to retrieve)
- **Code generation** -- "Write a Python function to sort a list" (Training data is sufficient)
- **Summarization of provided text** -- If the user already pastes the text in, there is nothing to retrieve
- **Conversational/chat use cases** -- Casual conversation does not need document retrieval

---

## RAG Best Practices

### 1. Chunking Strategies

How you split your documents matters a LOT. Bad chunking = bad retrieval = bad answers.

```
 WRONG: One giant chunk per document
 +-------------------------------------------------+
 | 10,000 word document as a single chunk           |
 | (too big -- contains too many topics)            |
 +-------------------------------------------------+

 WRONG: Tiny chunks
 +-----+  +-----+  +-----+  +-----+  +-----+
 | 2   |  | 2   |  | 2   |  | 2   |  | 2   |
 |words|  |words|  |words|  |words|  |words|
 +-----+  +-----+  +-----+  +-----+  +-----+
 (too small -- loses all context)

 RIGHT: Meaningful chunks with overlap
 +-------------------+
 | ~200-500 tokens   |
 | Overlap: 50 tokens|-----+
 +-------------------+     |
       +-------------------+
       | ~200-500 tokens   |
       | Overlap: 50 tokens|-----+
       +-------------------+     |
             +-------------------+
             | ~200-500 tokens   |
             +-------------------+
```

**Guidelines:**
- **Chunk size:** 200-500 tokens is a good starting point
- **Overlap:** Use 10-20% overlap between chunks so you don't split ideas in half
- **Respect boundaries:** Split on paragraphs or section headers, not mid-sentence
- **Include metadata:** Attach the document title, section, date, etc. to each chunk

### 2. Embedding Models

The embedding model determines how well your search works.

| Model | Dimensions | Notes |
|---|---|---|
| ChromaDB default | 384 | Good for prototyping, ships with ChromaDB |
| OpenAI `text-embedding-3-small` | 1536 | Great quality, widely used |
| OpenAI `text-embedding-3-large` | 3072 | Best quality from OpenAI |
| Cohere `embed-english-v3.0` | 1024 | Strong alternative |
| Voyage AI `voyage-3` | 1024 | Built for code + text |

For this training, we use ChromaDB's built-in embedding function to keep things simple.

### 3. Reranking

Initial retrieval (vector similarity) is fast but approximate. **Reranking** is a second pass that scores results more carefully.

```
 Vector Search (fast, approximate)
      |
      v
 Top 20 candidates
      |
      v
 Reranker (slower, more accurate)
      |
      v
 Top 5 final results
```

Reranking improves accuracy, especially when the initial retrieval returns borderline results.

### 4. Prompt Engineering for RAG

Your RAG prompt should:
- Tell the LLM to ONLY use the provided context
- Tell it to say "I don't know" if the context doesn't contain the answer
- Include clear delimiters between context documents
- Specify the desired response format

---

## Common Pitfalls

### 1. Chunks Too Big or Too Small
- **Too big:** The retrieved chunk contains irrelevant noise that confuses the LLM
- **Too small:** The retrieved chunk lacks enough context to be useful
- **Fix:** Experiment with chunk sizes. Start at 300 tokens with 50-token overlap.

### 2. Not Enough Context Retrieved
- Retrieving only 1-2 chunks might miss important information
- **Fix:** Retrieve 3-5 chunks and let the LLM synthesize across them

### 3. No "I Don't Know" Guardrail
- Without explicit instructions, the LLM will try to answer even when the context is irrelevant
- **Fix:** Always include instructions to decline answering when context is insufficient

### 4. Stale Data
- Your vector DB can get out of date if documents change
- **Fix:** Set up a re-indexing pipeline. Treat your vector DB like a search index.

### 5. Ignoring Metadata
- Metadata (dates, authors, categories) can dramatically improve retrieval
- **Fix:** Store metadata with your chunks and use it for filtering

---

## Files in This Module

| File | Description |
|---|---|
| `sample_documents.py` | Sample company documents (policies, FAQs, product info) |
| `simple_rag.py` | Basic end-to-end RAG pipeline with ChromaDB + Claude |
| `rag_with_sources.py` | Enhanced RAG with source citations, scores, and reranking |

### Running the Examples

```bash
# Install dependencies
pip install anthropic chromadb

# Set your API key
export ANTHROPIC_API_KEY="your-key-here"

# Run the simple RAG example
python simple_rag.py

# Run the enhanced RAG with sources
python rag_with_sources.py
```

---

## Key Takeaways

1. **RAG = Retrieve + Augment + Generate.** Look up relevant docs, add them to the prompt, then let the LLM answer.
2. **RAG solves the "LLMs don't know your data" problem** without fine-tuning.
3. **Chunking matters.** How you split documents directly impacts retrieval quality.
4. **Always ground the LLM.** Tell it to only use the provided context and to say "I don't know" when appropriate.
5. **RAG is not always the answer.** Use it when the answer lives in specific documents. Skip it for general knowledge and creative tasks.
