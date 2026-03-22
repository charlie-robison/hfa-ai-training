"""
mcp_with_resources.py — Advanced MCP Server with Tools AND Resources
=====================================================================

This server demonstrates the two main capabilities an MCP server can expose:

  TOOLS vs RESOURCES — What's the difference?
  ┌────────────────────────────────────────────────────────────────────┐
  │  TOOLS = Actions the agent can TAKE                               │
  │    - Search for something                                         │
  │    - Calculate a value                                            │
  │    - Update a record                                              │
  │    - Send a message                                               │
  │    Think of tools as VERBS — they DO things.                      │
  │                                                                    │
  │  RESOURCES = Data the agent can READ                              │
  │    - A document's contents                                        │
  │    - A database record                                            │
  │    - A configuration file                                         │
  │    Think of resources as NOUNS — they ARE things.                  │
  └────────────────────────────────────────────────────────────────────┘

  In this example, we build a server for a real estate company that has:
    - Resources: Company documents (buyer guide, seller checklist, market report)
    - Tools: Search documents, add a new document, get document stats

TO INSTALL DEPENDENCIES:
  pip install mcp

TO USE WITH CLAUDE DESKTOP:
  Add this to your claude_desktop_config.json:

  {
    "mcpServers": {
      "company-docs": {
        "command": "python",
        "args": ["/full/path/to/mcp_with_resources.py"]
      }
    }
  }
"""

from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types

# ---------------------------------------------------------------------------
# Create the server
# ---------------------------------------------------------------------------
server = Server("company-docs")

# ---------------------------------------------------------------------------
# Simulated Document Store
# ---------------------------------------------------------------------------
# In a real implementation, these would come from a database, file system,
# or CMS. For training purposes, we use an in-memory dictionary.

DOCUMENTS = {
    "buyer-guide": {
        "title": "Hawaii Home Buyer's Guide",
        "category": "guides",
        "last_updated": "2026-01-15",
        "content": (
            "Hawaii Home Buyer's Guide\n"
            "=========================\n\n"
            "Step 1: Get Pre-Approved\n"
            "  Contact a local lender familiar with Hawaii real estate.\n"
            "  Hawaii home prices are above the national average, so ensure\n"
            "  your pre-approval reflects the local market.\n\n"
            "Step 2: Choose Your Island and Neighborhood\n"
            "  Each island has a distinct character:\n"
            "  - Oahu: Urban amenities + beautiful beaches (Honolulu, Kailua)\n"
            "  - Maui: Resort lifestyle, great for vacation homes\n"
            "  - Big Island: Affordable, diverse climates\n"
            "  - Kauai: Quiet, lush, and scenic\n\n"
            "Step 3: Work with a Local Agent\n"
            "  Hawaii real estate has unique considerations: leasehold vs\n"
            "  fee simple ownership, hurricane insurance, lava zones, etc.\n"
            "  A local agent is essential.\n\n"
            "Step 4: Make an Offer\n"
            "  Competitive markets may require offers above asking price.\n"
            "  Your agent will guide you on local norms.\n\n"
            "Step 5: Close the Deal\n"
            "  Escrow in Hawaii typically takes 30-45 days.\n"
            "  Title insurance and escrow fees are customary.\n"
        )
    },
    "seller-checklist": {
        "title": "Seller's Pre-Listing Checklist",
        "category": "checklists",
        "last_updated": "2026-02-01",
        "content": (
            "Seller's Pre-Listing Checklist\n"
            "==============================\n\n"
            "Before listing your Hawaii property:\n\n"
            "[ ] Declutter and depersonalize the home\n"
            "[ ] Deep clean (inside and out — curb appeal matters!)\n"
            "[ ] Complete minor repairs (leaky faucets, chipped paint)\n"
            "[ ] Get a pre-listing inspection to avoid surprises\n"
            "[ ] Gather documents: title, survey, HOA docs, disclosures\n"
            "[ ] Stage the home (tropical plants, neutral decor)\n"
            "[ ] Professional photography (drone shots for ocean views!)\n"
            "[ ] Review comparable sales with your agent\n"
            "[ ] Set a competitive asking price\n"
            "[ ] Plan your showing schedule\n\n"
            "Hawaii-Specific Considerations:\n"
            "  - Disclose any knowledge of lava zones, flood zones\n"
            "  - Clarify leasehold vs fee simple ownership\n"
            "  - Note any hurricane/wind damage history\n"
            "  - Include termite inspection (wood-destroying organisms report)\n"
        )
    },
    "market-report-2026-q1": {
        "title": "Oahu Market Report — Q1 2026",
        "category": "reports",
        "last_updated": "2026-03-10",
        "content": (
            "Oahu Real Estate Market Report — Q1 2026\n"
            "==========================================\n\n"
            "SINGLE-FAMILY HOMES:\n"
            "  Median Price:        $1,050,000 (+3.2% YoY)\n"
            "  Days on Market:      22 (down from 28 in Q1 2025)\n"
            "  Active Listings:     487 (down 8% YoY)\n"
            "  Closed Sales:        612 (up 5% YoY)\n\n"
            "CONDOS:\n"
            "  Median Price:        $520,000 (+1.8% YoY)\n"
            "  Days on Market:      31 (down from 35 in Q1 2025)\n"
            "  Active Listings:     1,245 (down 3% YoY)\n"
            "  Closed Sales:        1,089 (up 7% YoY)\n\n"
            "KEY TRENDS:\n"
            "  - Inventory remains tight, especially for single-family homes\n"
            "  - Kailua and Hawaii Kai showing strongest price growth\n"
            "  - Remote workers continue to drive demand\n"
            "  - Interest rates holding steady around 6.25-6.5%\n"
            "  - New construction pipeline: 3 major projects in Kakaako\n"
        )
    },
}


# ===========================================================================
# RESOURCES — Data the agent can READ
# ===========================================================================
# Resources are identified by URIs (like web URLs, but for your data).
# The pattern is: protocol://path
# For our docs: docs://buyer-guide, docs://seller-checklist, etc.

@server.list_resources()
async def list_resources() -> list[types.Resource]:
    """
    List all available resources.

    The MCP client calls this to discover what data is available.
    The AI model can then decide to read specific resources based on
    the user's question.
    """
    resources = []
    for doc_id, doc in DOCUMENTS.items():
        resources.append(
            types.Resource(
                uri=f"docs://{doc_id}",
                name=doc["title"],
                description=f"Category: {doc['category']} | Last updated: {doc['last_updated']}",
                mimeType="text/plain"
            )
        )
    return resources


@server.read_resource()
async def read_resource(uri: str) -> str:
    """
    Read a specific resource by its URI.

    When the AI model wants to read a document, the client sends the URI
    and this function returns the content.
    """
    # Parse the URI to get the document ID
    # URI format: docs://document-id
    if uri.startswith("docs://"):
        doc_id = uri.replace("docs://", "")
    else:
        raise ValueError(f"Unknown resource URI scheme: {uri}")

    if doc_id not in DOCUMENTS:
        raise ValueError(f"Document not found: {doc_id}")

    doc = DOCUMENTS[doc_id]
    return doc["content"]


# ===========================================================================
# TOOLS — Actions the agent can TAKE
# ===========================================================================
# Unlike resources (which are passive data), tools let the agent DO things:
# search, filter, create, update, delete.

@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """Return the list of tools this server provides."""
    return [
        types.Tool(
            name="search_documents",
            description=(
                "Search through company documents by keyword. "
                "Returns matching documents with relevant excerpts. "
                "Use this when the user asks a question that might be "
                "answered by our company documents."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query (e.g., 'pre-approval', 'staging', 'market trends')"
                    }
                },
                "required": ["query"]
            }
        ),
        types.Tool(
            name="add_document",
            description=(
                "Add a new document to the company document store. "
                "Use this when the user wants to save new content as a company document."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "doc_id": {
                        "type": "string",
                        "description": "A unique identifier for the document (e.g., 'open-house-tips')"
                    },
                    "title": {
                        "type": "string",
                        "description": "The document title"
                    },
                    "category": {
                        "type": "string",
                        "description": "Document category (guides, checklists, reports, templates)",
                        "enum": ["guides", "checklists", "reports", "templates"]
                    },
                    "content": {
                        "type": "string",
                        "description": "The full text content of the document"
                    }
                },
                "required": ["doc_id", "title", "category", "content"]
            }
        ),
        types.Tool(
            name="get_document_stats",
            description=(
                "Get statistics about the company document library. "
                "Returns document count, categories, and recent updates. "
                "Use this when the user asks about what documents are available "
                "or wants an overview of the document library."
            ),
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Execute a tool and return results."""

    if name == "search_documents":
        return handle_search_documents(arguments)
    elif name == "add_document":
        return handle_add_document(arguments)
    elif name == "get_document_stats":
        return handle_get_document_stats(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")


def handle_search_documents(arguments: dict) -> list[types.TextContent]:
    """
    Search documents by keyword.

    This is a TOOL (not a resource) because it performs an ACTION (searching)
    rather than simply returning a known piece of data. The agent provides
    a query, and we return filtered, relevant results.
    """
    query = arguments["query"].lower()
    results = []

    for doc_id, doc in DOCUMENTS.items():
        # Simple keyword search across title and content
        if query in doc["title"].lower() or query in doc["content"].lower():
            # Find the most relevant line containing the query
            matching_lines = [
                line.strip()
                for line in doc["content"].split("\n")
                if query in line.lower() and line.strip()
            ]
            excerpt = matching_lines[0] if matching_lines else "Match found in document."

            results.append(
                f"Document: {doc['title']}\n"
                f"  URI:      docs://{doc_id}\n"
                f"  Category: {doc['category']}\n"
                f"  Updated:  {doc['last_updated']}\n"
                f"  Excerpt:  \"{excerpt}\""
            )

    if not results:
        return [types.TextContent(
            type="text",
            text=f"No documents found matching '{arguments['query']}'."
        )]

    header = f"Found {len(results)} document(s) matching '{arguments['query']}':\n\n"
    return [types.TextContent(type="text", text=header + "\n\n".join(results))]


def handle_add_document(arguments: dict) -> list[types.TextContent]:
    """
    Add a new document to the store.

    This is a TOOL because it MODIFIES state — it creates a new document.
    Resources are read-only; tools can make changes.
    """
    doc_id = arguments["doc_id"]
    title = arguments["title"]
    category = arguments["category"]
    content = arguments["content"]

    if doc_id in DOCUMENTS:
        return [types.TextContent(
            type="text",
            text=f"Error: A document with ID '{doc_id}' already exists. Choose a different ID."
        )]

    DOCUMENTS[doc_id] = {
        "title": title,
        "category": category,
        "last_updated": "2026-03-22",
        "content": content,
    }

    return [types.TextContent(
        type="text",
        text=(
            f"Document added successfully!\n"
            f"  ID:       {doc_id}\n"
            f"  Title:    {title}\n"
            f"  Category: {category}\n"
            f"  URI:      docs://{doc_id}\n"
            f"  Length:   {len(content)} characters"
        )
    )]


def handle_get_document_stats(arguments: dict) -> list[types.TextContent]:
    """
    Return statistics about the document library.

    This is a TOOL (not a resource) because it computes and aggregates
    information dynamically, rather than returning a static piece of data.
    """
    total = len(DOCUMENTS)

    # Count by category
    categories = {}
    for doc in DOCUMENTS.values():
        cat = doc["category"]
        categories[cat] = categories.get(cat, 0) + 1

    # Find most recently updated
    most_recent = max(DOCUMENTS.values(), key=lambda d: d["last_updated"])

    # Build category breakdown
    cat_lines = [f"    {cat}: {count}" for cat, count in sorted(categories.items())]

    result = (
        f"Document Library Stats:\n"
        f"  Total Documents: {total}\n"
        f"  Categories:\n"
        + "\n".join(cat_lines) + "\n"
        f"  Most Recently Updated: {most_recent['title']} ({most_recent['last_updated']})\n\n"
        f"  All Documents:\n"
    )

    for doc_id, doc in DOCUMENTS.items():
        result += f"    - {doc['title']} (docs://{doc_id})\n"

    return [types.TextContent(type="text", text=result)]


# ---------------------------------------------------------------------------
# Run the Server
# ---------------------------------------------------------------------------
async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
