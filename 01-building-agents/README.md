# 01 - Building Agents

## HFA AI Training Seminar

---

## Table of Contents

1. [What Is an Agent?](#what-is-an-agent)
2. [Prompting](#prompting)
3. [TDD Approach](#tdd-approach-test-driven-development-with-agents)
4. [Context Window](#context-window)
5. [Referencing Files](#referencing-files)
6. [Drawing Pipelines in Excalidraw](#drawing-pipelines-in-excalidraw)
7. [Reviewing Code](#reviewing-code)
8. [Claude.md](#claudemd)
9. [Rules and Skills](#rules-and-skills)
10. [Saving Conversations](#saving-conversations)
11. [Knowing Your Inputs and Outputs](#knowing-your-inputs-and-outputs)
12. [Few-Shot Examples](#few-shot-examples)
13. [Make Prompts Evidence-Based](#make-prompts-evidence-based)
14. [Choosing Your Model](#choosing-your-model)
15. [Token Limits](#token-limits)
16. [Multi-Threaded Calls](#multi-threaded-calls)
17. [Key Lesson: Evidence vs. Reasoning](#key-lesson-agents-are-not-great-at-decisions-without-evidence-but-are-great-at-reasoning)

---

## What Is an Agent?

An **agent** is a system where an LLM (Large Language Model) operates in a loop, using tools and making decisions to accomplish a task. Unlike a simple chat interaction where you ask one question and get one answer, an agent can:

- Read and write files
- Execute code
- Search the web
- Call APIs
- Make decisions about what to do next based on intermediate results

Think of it this way: a **chat** is like asking someone a question. An **agent** is like hiring someone to go do a job. They'll figure out the steps, use whatever tools they need, and come back with the result.

**Key distinction:** The agent operates in a loop. It takes an action, observes the result, and decides what to do next. This loop continues until the task is complete.

```
User gives task --> Agent thinks --> Agent takes action --> Agent observes result --> Agent thinks again --> ... --> Task complete
```

---

## Prompting

Prompting is the foundation of working with agents. There are three layers to understand:

### System Prompts

The **system prompt** is the instruction set that defines how the agent behaves. It runs before any user input. Think of it as the agent's "job description."

```
You are a real estate data analyst. You specialize in Hawaii residential
properties. When given MLS data, you analyze trends, identify opportunities,
and provide actionable insights. Always cite specific numbers from the data.
```

**Best practices for system prompts:**
- Be specific about the role
- Define the output format you want
- Set boundaries (what the agent should NOT do)
- Include domain context the agent needs

### User Prompts

The **user prompt** is the specific task or question. This is what changes with each interaction.

```
Analyze the attached CSV of Oahu home sales from Q4 2025. What neighborhoods
showed the highest price appreciation?
```

### Structured Prompts

Structured prompts use clear formatting (XML tags, markdown headers, numbered lists) to organize complex instructions. Agents parse structured prompts far more reliably than wall-of-text prompts.

```xml
<role>You are a real estate listing description writer.</role>

<rules>
- Keep descriptions under 200 words
- Highlight ocean views, lanai space, and proximity to beaches
- Use professional but warm tone
- Never exaggerate square footage or features
</rules>

<input>
Property: 3BR/2BA in Kailua, 1,450 sqft, ocean view from master, renovated kitchen
</input>

<output_format>
Return the listing description as a single paragraph.
</output_format>
```

**Why structured prompts matter:** When you give an agent a clear structure, it follows the structure. When you give it ambiguous instructions, it guesses. Guessing is where agents go wrong.

---

## TDD Approach (Test-Driven Development with Agents)

**TDD with agents** is one of the most powerful workflows you can adopt. The concept is simple:

1. **Write the tests first** -- define exactly what the code should do
2. **Give the tests to the agent** -- let it implement the code to pass them
3. **Run the tests** -- verify the agent's implementation
4. **Iterate** -- if tests fail, give the agent the error output and let it fix

### Why This Works So Well

- Tests are **unambiguous specifications**. They tell the agent exactly what "correct" looks like.
- You catch errors immediately instead of discovering them later.
- The agent has a clear goal: make the tests pass.

### Example Workflow

```
Step 1: You write test_calculator.py with tests for add(), subtract(), multiply()
Step 2: You tell the agent: "Implement calculator.py to pass all tests in test_calculator.py"
Step 3: The agent writes the code
Step 4: You run pytest -- if something fails, paste the error back to the agent
Step 5: Repeat until all tests pass
```

**The key insight:** You don't need to know how to write the implementation. You just need to know what the correct behavior looks like. Define that in tests, and let the agent do the rest.

See `tdd_example.py` in this directory for a working example.

---

## Context Window

The **context window** is the total amount of text (measured in tokens) that an LLM can "see" at once. Everything in the conversation -- system prompt, previous messages, files, tool results -- all of it lives in the context window.

### Why It Matters

- **If it's not in the context window, the agent doesn't know about it.** There is no persistent memory between conversations unless you explicitly provide it.
- **When the context window fills up, old content gets dropped.** The agent loses track of earlier instructions or data.
- **Larger context windows cost more** in both time and money.

### How to Manage It

1. **Keep system prompts concise.** Don't dump your entire knowledge base into the system prompt.
2. **Reference files instead of pasting them.** If you're using Claude Code or a similar tool, point the agent to a file path rather than pasting 10,000 lines into the chat.
3. **Break large tasks into smaller ones.** Instead of "analyze this entire codebase," do "analyze the authentication module, then we'll move on."
4. **Summarize intermediate results.** If you're in a long conversation, periodically ask the agent to summarize what it knows so far, then start a new conversation with that summary.
5. **Be aware of token counts.** A rough rule: 1 token is about 4 characters in English. A 200K context window is roughly 150,000 words -- a lot, but not infinite.

### Context Window Sizes (as of early 2026)

| Model | Context Window |
|-------|---------------|
| Claude Opus/Sonnet | 200K tokens |
| Claude Haiku | 200K tokens |
| GPT-4o | 128K tokens |
| GPT-o1/o3 | 200K tokens |

---

## Referencing Files

Agents that can read and write files (like Claude Code) are far more powerful than chat-only agents. Understanding how file referencing works is critical.

### How Agents Read Files

When you tell an agent to read a file, the file contents get loaded into the context window. The agent can then reason about the contents, modify them, or use them as input for other tasks.

### Best Practices

1. **Point to specific files, not entire directories.** "Read `src/api/auth.py`" is better than "read the src directory."
2. **Tell the agent what to look for.** "Read `config.yaml` and find the database connection settings" focuses the agent's attention.
3. **Be aware of file sizes.** A 5,000-line file takes a significant chunk of context. If you only need lines 100-150, say so.
4. **Use file references in prompts.** When building agent pipelines, pass file paths as variables rather than hardcoding content.

### Writing Files

When agents write files:
- Always review the output before committing
- Use version control (git) so you can revert bad changes
- Be specific about where files should be saved
- Tell the agent the expected format (JSON, CSV, Python, etc.)

---

## Drawing Pipelines in Excalidraw

Before you write a single line of code, **draw your agent pipeline.**

### What Is a Pipeline?

A pipeline is the sequence of steps your agent (or multiple agents) will follow to accomplish a task. For example:

```
[User Input] --> [Data Fetcher Agent] --> [Analyzer Agent] --> [Report Writer Agent] --> [Output]
```

### Why Excalidraw?

[Excalidraw](https://excalidraw.com) is a free, simple whiteboard tool that's perfect for sketching pipelines. It's not about making pretty diagrams -- it's about thinking through the flow before coding.

### What to Include in Your Pipeline Drawing

1. **Inputs** -- What data comes in? From where?
2. **Processing steps** -- What does each agent/step do?
3. **Decision points** -- Where does the pipeline branch?
4. **Outputs** -- What gets produced at the end?
5. **Error handling** -- What happens when something fails?
6. **Data flow** -- How does data move between steps? What format?

### Example Pipeline Sketch

```
[MLS CSV Upload]
       |
       v
[Parse & Validate Data]
       |
       v
[Agent: Analyze Price Trends] -----> [Agent: Identify Comparable Properties]
       |                                        |
       v                                        v
[Agent: Generate Market Summary] <----- [Merge Results]
       |
       v
[Format as PDF Report]
       |
       v
[Email to Client]
```

**The key insight:** If you can't draw the pipeline, you don't understand the problem well enough to build it. Drawing forces clarity.

---

## Reviewing Code

Agents are excellent code reviewers. They can catch bugs, suggest improvements, identify security issues, and verify that code follows conventions.

### How to Use Agents for Code Review

1. **Provide the code** -- either paste it or reference the file
2. **Tell the agent what to look for** -- "Check for security vulnerabilities," "Verify error handling," "Look for performance issues"
3. **Give context** -- "This is a Flask API endpoint that handles user authentication"
4. **Ask for specific output** -- "List issues as bullet points with severity ratings"

### What Agents Are Good At in Code Review

- Finding syntax errors and typos
- Identifying common security patterns (SQL injection, XSS, etc.)
- Checking for edge cases you might have missed
- Suggesting more idiomatic code
- Verifying that code matches a specification

### What Agents Are NOT Good At in Code Review

- Understanding your full business context (unless you provide it)
- Making subjective architectural decisions
- Knowing about undocumented side effects in your specific codebase
- Replacing the need for human review of critical systems

---

## Claude.md

A `CLAUDE.md` file is a configuration file that sits in your project root and tells Claude Code how to behave when working in that project. Think of it as a project-specific system prompt.

### What Goes in CLAUDE.md

- **Project description** -- What is this project? What does it do?
- **Tech stack** -- Languages, frameworks, libraries in use
- **Coding conventions** -- Naming conventions, file structure, patterns to follow
- **Common commands** -- How to run tests, start the dev server, deploy
- **Things to avoid** -- Anti-patterns, deprecated APIs, files not to modify
- **Domain knowledge** -- Business rules, terminology, constraints

### Why It Matters

Without a `CLAUDE.md`, the agent has to infer everything from the code itself. With one, the agent starts every task with the right context. It's the difference between hiring someone and giving them no onboarding vs. handing them a detailed orientation guide.

### Example

See `example_claude_md` in this directory for a complete example.

---

## Rules and Skills

### Rules

Rules are persistent instructions that apply across all conversations in a project. They live in your Claude configuration and are automatically injected into every interaction.

**Examples of good rules:**
- "Always use TypeScript, never JavaScript"
- "Format all dates as ISO 8601"
- "Never modify files in the /legacy directory"
- "Use pytest for all Python tests"

### Skills (Slash Commands)

Skills are reusable prompt templates that you can invoke with a slash command. They're useful for tasks you repeat often.

**Example skill:** `/review-pr` could be a skill that:
1. Reads the current git diff
2. Analyzes the changes
3. Provides a structured code review with severity ratings

**Why skills matter:** They standardize your workflows. Instead of rewriting the same complex prompt every time, you define it once as a skill and invoke it with a command.

---

## Saving Conversations

### Why Save Conversations

- **Resume later** -- Pick up where you left off without re-explaining context
- **Reference** -- Look back at how a problem was solved
- **Debugging** -- If an agent produced bad output, review the conversation to understand why
- **Training** -- Use past conversations to improve your prompting

### How to Save

In Claude Code, conversations are automatically saved and can be resumed. For API-based agents, you need to manage conversation history yourself:

1. **Store message arrays** -- Save the full list of messages (system + user + assistant) to a file or database
2. **Include metadata** -- Timestamp, task description, outcome (success/failure)
3. **Trim when resuming** -- If the conversation was long, summarize older messages before resuming to save context window space

### Best Practice

Keep a log of your agent interactions, especially when building new pipelines. The conversation history often contains insights about edge cases and decisions that aren't captured anywhere else.

---

## Knowing Your Inputs and Outputs

This is a fundamental principle: **before you build anything, define exactly what goes in and what comes out.**

### For Every Agent Step, Answer:

1. **What is the input?**
   - What format? (JSON, CSV, plain text, file path)
   - What fields/data does it contain?
   - What are the constraints? (required fields, max size, valid ranges)

2. **What is the output?**
   - What format?
   - What fields/data does it contain?
   - What does "success" look like?
   - What does "failure" look like?

### Example

```
AGENT: Property Value Estimator

INPUT:
- Address (string, required)
- Square footage (integer, required)
- Bedrooms (integer, required)
- Bathrooms (float, required)
- Recent comparable sales (list of objects, optional)

OUTPUT (success):
- Estimated value (float)
- Confidence score (float, 0-1)
- Comparable properties used (list)
- Reasoning (string)

OUTPUT (failure):
- Error type (string)
- Error message (string)
- Suggested fix (string)
```

**Why this matters:** When you clearly define inputs and outputs, you can test each step independently, compose steps into pipelines, and debug failures quickly.

---

## Few-Shot Examples

**Few-shot prompting** means giving the agent examples of the input/output pattern you want before asking it to handle new input. It's one of the most effective prompting techniques.

### Why It Works

Instead of describing what you want in abstract terms, you **show** the agent. Models are excellent pattern matchers. Give them 2-3 examples, and they'll follow the pattern precisely.

### Structure

```
Here are examples of how to format property descriptions:

Example 1:
Input: 3BR/2BA, Kailua, ocean view, 1200 sqft
Output: "Stunning 3-bedroom, 2-bath Kailua retreat with breathtaking ocean views. 1,200 sq ft of island living at its finest."

Example 2:
Input: 2BR/1BA, Manoa, garden, 800 sqft
Output: "Charming 2-bedroom, 1-bath Manoa hideaway surrounded by lush garden views. A cozy 800 sq ft sanctuary in one of Honolulu's most beloved valleys."

Now format this property:
Input: 4BR/3BA, Hawaii Kai, marina view, 2100 sqft
```

### Best Practices

- Use 2-5 examples (more than 5 usually has diminishing returns and wastes context)
- Make examples representative of the real data
- Include edge cases if they matter
- Keep the format consistent across all examples

See `few_shot_example.py` for a working implementation.

---

## Make Prompts Evidence-Based

**Never ask an agent to guess. Give it data and ask it to reason.**

### Bad (No Evidence)

```
What's a good listing price for a 3-bedroom house in Kailua?
```

The agent will give you a generic answer based on its training data, which may be outdated or wrong.

### Good (Evidence-Based)

```
Based on the following recent sales data for 3-bedroom homes in Kailua:

- 123 Kailua Rd: $1,250,000 (sold 2026-01-15, 1,400 sqft)
- 456 Oneawa St: $1,180,000 (sold 2026-02-01, 1,350 sqft)
- 789 Kuulei Rd: $1,320,000 (sold 2026-01-28, 1,500 sqft)

My property is at 321 Hamakua Dr, 1,425 sqft, recently renovated kitchen.

Based on this data, what would be a competitive listing price and why?
```

Now the agent has specific, current data to reason about. Its answer will be grounded in evidence, not guesses.

### The Rule

**Agents are reasoning engines, not knowledge databases.** Feed them data, and they'll give you excellent analysis. Ask them to pull facts from memory, and they'll often be wrong or outdated.

---

## Choosing Your Model

Not all models are equal for all tasks. Here's a practical guide:

### Claude (Anthropic) -- Best for Coding

- **Strengths:** Code generation, code review, following complex instructions, working with files, structured output, long context handling
- **Best for:** Building agents, writing code, analyzing codebases, generating structured data
- **Models:** Opus (most capable), Sonnet (best balance), Haiku (fastest/cheapest)

### GPT (OpenAI) -- Best for Reasoning

- **Strengths:** Complex reasoning chains, mathematical problems, multi-step logic, creative problem solving
- **Best for:** Analysis tasks, decision-making workflows, research synthesis
- **Models:** o3 (best reasoning), GPT-4o (best balance), GPT-4o-mini (fastest/cheapest)

### When to Use Which

| Task | Recommended |
|------|------------|
| Write a Python script | Claude |
| Analyze sales data and draw conclusions | GPT (o-series) |
| Review code for bugs | Claude |
| Plan a marketing strategy from data | GPT |
| Build an API integration | Claude |
| Summarize and compare research papers | GPT |
| Generate structured JSON from text | Claude |
| Complex multi-step math/logic | GPT (o-series) |

### Practical Tip

Many production pipelines use **both** models at different stages. For example: use Claude to build the data processing code, then use GPT o3 to do the analytical reasoning on the processed data.

---

## Token Limits

Every model has a maximum number of tokens it can handle in a single interaction. Understanding this prevents silent failures and unexpected behavior.

### What Counts as Tokens

- **Input tokens:** Your system prompt + conversation history + any files/data you provide
- **Output tokens:** The response the model generates
- **Total must fit within the context window**

### Token Limits by Model (as of early 2026)

| Model | Context Window | Max Output Tokens |
|-------|---------------|-------------------|
| Claude Opus | 200K | 32K |
| Claude Sonnet | 200K | 16K |
| Claude Haiku | 200K | 8K |
| GPT-4o | 128K | 16K |
| GPT-o3 | 200K | 100K |

### Practical Implications

1. **A 200K context window is about 150,000 words** -- roughly 500 pages of text
2. **Max output limits matter.** If you ask for a very long response, it may get truncated.
3. **Longer contexts are slower and more expensive.** Don't use 200K tokens if 10K will do.
4. **Watch for the "lost in the middle" effect.** Models pay more attention to the beginning and end of long contexts. Put important instructions at the start or end, not buried in the middle.

### How to Estimate Token Usage

- English text: ~1 token per 4 characters
- Code: ~1 token per 3 characters (more special characters)
- Simple math: a 100-line Python file is roughly 1,000-2,000 tokens

---

## Multi-Threaded Calls

When you need to process multiple items, you don't have to do them one at a time. **Multi-threaded (concurrent) API calls** let you run multiple agent tasks in parallel.

### When to Use

- Processing a list of items (e.g., analyzing 20 property listings)
- Running the same analysis with different parameters
- Fetching data from multiple sources simultaneously
- Any task where the items are independent of each other

### When NOT to Use

- When step B depends on the result of step A
- When you need to stay under API rate limits
- When the order of processing matters

### How It Works

Using Python's `asyncio` library with the Anthropic async client, you can fire off multiple API calls simultaneously:

```python
# Instead of this (sequential - slow):
for listing in listings:
    result = analyze(listing)  # Each waits for the previous to finish

# Do this (concurrent - fast):
results = await asyncio.gather(
    analyze(listing_1),
    analyze(listing_2),
    analyze(listing_3),
)  # All run at the same time
```

If you have 10 items and each takes 3 seconds, sequential processing takes 30 seconds. Concurrent processing takes about 3 seconds.

See `multi_threaded_agent.py` for a working implementation.

---

## Key Lesson: Agents Are NOT Great at Decisions Without Evidence, but ARE Great at Reasoning!

This is the single most important takeaway from this entire section.

### What This Means

**WITHOUT evidence:**
> "Should I list my property at $1.2M or $1.3M?"

The agent will give you an answer, but it's essentially guessing. It has no current market data, no knowledge of your specific property's condition, no awareness of recent comparable sales. The answer might sound confident, but it's not grounded in anything real.

**WITH evidence:**
> "Here are 15 comparable sales from the last 90 days in my neighborhood, my property's features, and the current days-on-market trend. Based on this data, should I list at $1.2M or $1.3M?"

Now the agent can reason brilliantly. It will analyze the comparables, weigh the factors, consider the market trend, and give you a well-reasoned recommendation with specific justifications.

### The Pattern

1. **You provide the evidence** (data, context, constraints, examples)
2. **The agent provides the reasoning** (analysis, synthesis, recommendations)

### Applied to Building Agents

When you build an agent pipeline:
- **Don't** ask the agent to make decisions based on its training data
- **Do** feed the agent real, current data and ask it to analyze
- **Don't** expect the agent to know things about your specific situation
- **Do** provide all relevant context and let the agent reason about it
- **Don't** treat the agent as an oracle
- **Do** treat the agent as an extremely fast, thorough analyst who needs to be briefed

### Remember

**Data in, reasoning out.** That's the formula. The quality of an agent's output is directly proportional to the quality and relevance of the evidence you provide.

---

## Files in This Section

| File | Description |
|------|-------------|
| `README.md` | This teaching guide |
| `basic_agent.py` | Simple agent with tools, system prompt, and few-shot examples |
| `multi_threaded_agent.py` | Concurrent API calls with asyncio |
| `tdd_example.py` | Test-driven development workflow with agents |
| `few_shot_example.py` | Few-shot prompting patterns |
| `example_claude_md` | Example CLAUDE.md project configuration |

---

## Next Up

In the next section, we'll dive into **Agent Pipelines** -- chaining multiple agents together to solve complex, multi-step problems.
