# Module 5: MCP (Model Context Protocol)

## What is MCP?

**Model Context Protocol (MCP)** is an open standard for connecting AI models to external tools and data sources. Think of it as a **universal adapter** — instead of building custom integrations for every tool an AI needs, MCP provides one standard way for AI to talk to the outside world.

Before MCP, if you wanted an LLM to check your database, you had to build a custom integration. If you also wanted it to search your files, that was a separate custom build. MCP says: "Let's create one protocol that works for everything."

> **The key idea:** MCP lets you go from an AI that _talks_ about doing things to an AI that _actually does_ things.

---

## Agentifying Processes

"Agentifying" means taking a workflow that a human does step-by-step and letting an AI agent control it by calling tools.

### Example: A Real Estate Workflow

**Before MCP (manual process):**
1. Client asks about homes in Kailua under $1.5M
2. You open the MLS, search for listings
3. You calculate mortgage estimates
4. You check weather/neighborhood info
5. You compile everything into an email

**After MCP (agentified process):**
1. Client asks GPT-4o about homes in Kailua under $1.5M
2. GPT-4o calls `search_listings` tool -> gets results
3. GPT-4o calls `calculate_mortgage` tool -> gets payment estimates
4. GPT-4o calls `get_weather` tool -> gets local conditions
5. GPT-4o composes a personalized response with all the data

The AI **decides which tools to call and in what order** based on the conversation. You are not scripting it step by step — the agent figures out the plan.

---

## How MCP Works

### The Three Players

| Component | What It Is | Example |
|-----------|-----------|---------|
| **MCP Server** | A program that exposes tools, resources, and prompts | A Python script that can search listings |
| **MCP Client** | An AI-powered app that connects to servers | Claude Desktop, Cursor, custom apps |
| **The AI Model** | The brain that decides what to do | GPT-4o, Claude, Gemini, etc. |

### What Servers Expose

MCP servers can provide three types of capabilities:

1. **Tools** — Actions the agent can take (search, calculate, send email, update database)
2. **Resources** — Data the agent can read (documents, database records, file contents)
3. **Prompts** — Pre-built prompt templates the server offers to the client

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     YOUR COMPUTER                           │
│                                                             │
│  ┌───────────────────┐       ┌────────────────────────┐     │
│  │   MCP Client      │       │   MCP Server A         │     │
│  │  (AI Application)  │◄────►│  (Real Estate Tools)   │     │
│  │                   │ stdio │  - search_listings     │     │
│  │  ┌─────────────┐ │       │  - calculate_mortgage  │     │
│  │  │  AI Model   │ │       └────────────────────────┘     │
│  │  │  (GPT-4o)   │ │                                       │
│  │  │             │ │       ┌────────────────────────┐     │
│  │  │ "I should   │ │       │   MCP Server B         │     │
│  │  │  call the   │ │◄────►│  (File System)         │     │
│  │  │  search     │ │ stdio │  - read_file           │     │
│  │  │  tool..."   │ │       │  - write_file          │     │
│  │  └─────────────┘ │       └────────────────────────┘     │
│  │                   │                                       │
│  │                   │       ┌────────────────────────┐     │
│  │                   │       │   MCP Server C         │     │
│  │                   │◄────►│  (Database)            │     │
│  │                   │ HTTP  │  - query               │     │
│  │                   │ (SSE) │  - insert              │     │
│  └───────────────────┘       └────────────────────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Communication Flow

```
User asks a question
        │
        ▼
┌──────────────────┐
│  GPT-4o (Model)  │  "I need to search listings to answer this"
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   MCP Client     │  Sends tool call to the right server
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   MCP Server     │  Executes the tool, returns results
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  GPT-4o (Model)  │  Uses results to form a response
└──────────────────┘
```

### Transport Methods

| Method | How It Works | Best For |
|--------|-------------|----------|
| **stdio** | Server runs as a subprocess, communicates via stdin/stdout | Local servers on your machine |
| **HTTP (SSE)** | Server runs as a web service, communicates over HTTP | Remote servers, shared team servers |

---

## Pros and Cons

### Pros

| Advantage | Why It Matters |
|-----------|---------------|
| **Standardized protocol** | Build once, works with any MCP-compatible client (Cursor, Claude Desktop, custom apps, and more) |
| **Real system access** | Agents can query databases, call APIs, read/write files — do real work |
| **Composable** | Mix and match servers. Need listings + weather + email? Add three servers. |
| **Secure by design** | You control exactly which tools the agent can access. Nothing hidden. |
| **Open source** | The protocol is open — anyone can build servers and clients |
| **Growing ecosystem** | Thousands of pre-built MCP servers already available |

### Cons

| Drawback | What to Watch For |
|----------|------------------|
| **Still evolving** | The protocol is under active development — things may change |
| **Setup complexity** | Configuring servers requires some technical comfort (JSON config, Python, etc.) |
| **Security power** | The agent has real power — a misconfigured tool could modify real data |
| **Debugging** | When something goes wrong, tracing the issue across client/server can be tricky |
| **Latency** | Each tool call adds time — complex workflows with many calls can feel slow |
| **Context window usage** | Tool definitions and results consume tokens from the model's context |

---

## Using MCP with a Desktop Client

Many AI desktop apps support MCP, including Claude Desktop and Cursor. Here we show the Claude Desktop configuration as an example, but the pattern is similar across clients.

### Step 1: Find Your Config File

The Claude Desktop configuration file lives at:

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

### Step 2: Edit the Config

Open the file and add your MCP servers. Here is the structure:

```json
{
  "mcpServers": {
    "my-server-name": {
      "command": "python",
      "args": ["/path/to/my_server.py"],
      "env": {
        "API_KEY": "your-key-here"
      }
    }
  }
}
```

### Step 3: Restart the Client

After saving the config, **completely quit and reopen** the desktop client. The servers will start automatically.

### Step 4: Verify

In a new conversation, you should see a small hammer/tools icon indicating available MCP tools. Click it to see which tools are connected.

### Walk-Through: Adding the Example Server from This Module

```json
{
  "mcpServers": {
    "real-estate-tools": {
      "command": "python",
      "args": ["/Users/yourname/hfa-ai-training/05-mcp/simple_mcp_server.py"]
    }
  }
}
```

> See `claude_desktop_config_example.json` in this folder for a more complete example.

---

## When to Use MCP

### Use MCP When...

- You want an AI agent to **DO things**, not just talk about them
- You are **automating workflows** that touch external systems (databases, APIs, file systems)
- You are building **internal tools** powered by AI for your team
- You want to give your LLM access to **your specific data** (company docs, CRM, listings)
- You need a **standardized approach** that works across multiple AI clients
- You want **composable capabilities** — add/remove tools without changing the AI

### Do NOT Use MCP When...

- You just need **simple Q&A** that does not require external data
- Your **security constraints** are extremely tight and you cannot allow any tool execution
- The task is a **one-off** that is faster to do manually than to set up a server
- You need **real-time streaming** of large datasets (MCP is better for request/response patterns)
- **Pre-built integrations** already exist (e.g., the LLM's built-in web search)

---

## Hands-On: Files in This Module

| File | What It Demonstrates |
|------|---------------------|
| `simple_mcp_server.py` | A basic MCP server with 3 tools (weather, listings, mortgage) |
| `mcp_with_resources.py` | An advanced server showing both tools AND resources |
| `claude_desktop_config_example.json` | How to configure a desktop MCP client to use these servers |

### Quick Start

```bash
# 1. Install the MCP Python SDK
pip install mcp

# 2. Run the simple server (for testing — your MCP client runs it automatically)
python simple_mcp_server.py

# 3. Or configure your MCP client to run it (see the config example)
```

---

## Key Takeaways

1. **MCP is the USB-C of AI tools** — one standard connector for everything
2. **Agentifying = giving AI control** of multi-step workflows via tools
3. **Servers expose tools and resources**, clients connect the AI to them
4. **You control the power** — only expose what the agent should access
5. **Use it when the AI needs to DO things** — not just when it needs to talk

---

## Further Reading

- [MCP Official Documentation](https://modelcontextprotocol.io)
- [MCP GitHub Repository](https://github.com/modelcontextprotocol)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Client Setup Guide](https://modelcontextprotocol.io/quickstart/user)
- [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers) — community directory of pre-built servers
