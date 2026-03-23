"""
grocery_mcp_server.py — MCP Server for Grocery Product Lookup

Exposes three tools over stdio:
  1. search_products  — Search products by keyword
  2. get_nutrition     — Get nutrition facts for a product by ID
  3. check_stock       — Check if a product is in stock at a store

Run with:  python grocery_mcp_server.py

Configure in Claude Desktop (claude_desktop_config.json):
  {
    "mcpServers": {
      "grocery": {
        "command": "python",
        "args": ["/full/path/to/grocery_mcp_server.py"]
      }
    }
  }

Dependencies: pip install mcp
"""

from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types

server = Server("grocery-tools")

# --- Product database (simulated) ---

PRODUCTS = {
    "egg-001": {
        "name": "Organic Free-Range Large Brown Eggs 12ct",
        "category": "eggs",
        "price": 6.99,
        "calories": 70,
        "protein_g": 6,
        "fat_g": 5,
        "organic": True,
        "description": "Pasture-raised hens, non-GMO diet, USDA Organic. 12 count.",
    },
    "egg-002": {
        "name": "Cage-Free Large White Eggs 18ct",
        "category": "eggs",
        "price": 4.49,
        "calories": 70,
        "protein_g": 6,
        "fat_g": 5,
        "organic": False,
        "description": "Open barn housing, American Humane Certified. 18 count value pack.",
    },
    "egg-003": {
        "name": "Liquid Egg Whites 32oz",
        "category": "eggs",
        "price": 4.99,
        "calories": 25,
        "protein_g": 5,
        "fat_g": 0,
        "organic": False,
        "description": "Pasteurized, fat-free, cholesterol-free. 32oz carton.",
    },
    "milk-001": {
        "name": "Organic Whole Milk 1 Gallon",
        "category": "milk",
        "price": 7.49,
        "calories": 150,
        "protein_g": 8,
        "fat_g": 8,
        "organic": True,
        "description": "Grass-fed cows, ultra-pasteurized, no antibiotics or hormones.",
    },
    "milk-002": {
        "name": "Oat Milk Original 64oz",
        "category": "milk",
        "price": 5.49,
        "calories": 120,
        "protein_g": 3,
        "fat_g": 5,
        "organic": False,
        "description": "Plant-based, gluten-free, dairy-free. Froths well for lattes.",
    },
    "milk-003": {
        "name": "2% Reduced Fat Milk Half Gallon",
        "category": "milk",
        "price": 3.29,
        "calories": 120,
        "protein_g": 8,
        "fat_g": 5,
        "organic": False,
        "description": "Pasteurized, homogenized, fortified with vitamins A and D.",
    },
    "bread-001": {
        "name": "Organic Sourdough Loaf",
        "category": "bread",
        "price": 6.49,
        "calories": 120,
        "protein_g": 4,
        "fat_g": 1,
        "organic": True,
        "description": "50-year-old starter, 24hr ferment, no preservatives. Baked daily.",
    },
    "bread-002": {
        "name": "Whole Wheat Sandwich Bread 20oz",
        "category": "bread",
        "price": 3.99,
        "calories": 110,
        "protein_g": 4,
        "fat_g": 1,
        "organic": False,
        "description": "100% whole wheat, no HFCS, 3g fiber per slice. Pre-sliced.",
    },
    "bread-003": {
        "name": "Gluten-Free Multigrain Bread 15oz",
        "category": "bread",
        "price": 6.99,
        "calories": 100,
        "protein_g": 2,
        "fat_g": 2,
        "organic": False,
        "description": "Brown rice flour, millet, quinoa. Certified gluten-free.",
    },
}

# Simulated stock levels per store
STOCK = {
    "downtown":  {"egg-001": 24, "egg-002": 36, "egg-003": 12, "milk-001": 8,  "milk-002": 15, "milk-003": 20, "bread-001": 6,  "bread-002": 18, "bread-003": 4},
    "westside":  {"egg-001": 0,  "egg-002": 48, "egg-003": 8,  "milk-001": 12, "milk-002": 0,  "milk-003": 30, "bread-001": 10, "bread-002": 22, "bread-003": 0},
    "eastside":  {"egg-001": 18, "egg-002": 24, "egg-003": 0,  "milk-001": 6,  "milk-002": 20, "milk-003": 15, "bread-001": 0,  "bread-002": 14, "bread-003": 8},
}


# --- Tool definitions ---

@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="search_products",
            description="Search grocery products by keyword. Returns matching products with price and description.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search term (e.g. 'organic', 'gluten-free', 'eggs')"},
                    "category": {"type": "string", "description": "Filter by category: eggs, milk, or bread", "enum": ["eggs", "milk", "bread"]},
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="get_nutrition",
            description="Get detailed nutrition facts for a product by its ID (e.g. 'egg-001', 'milk-002').",
            inputSchema={
                "type": "object",
                "properties": {
                    "product_id": {"type": "string", "description": "The product ID"},
                },
                "required": ["product_id"],
            },
        ),
        types.Tool(
            name="check_stock",
            description="Check if a product is in stock at a specific store location. Stores: downtown, westside, eastside.",
            inputSchema={
                "type": "object",
                "properties": {
                    "product_id": {"type": "string", "description": "The product ID"},
                    "store": {"type": "string", "description": "Store location", "enum": ["downtown", "westside", "eastside"]},
                },
                "required": ["product_id", "store"],
            },
        ),
    ]


# --- Tool implementations ---

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "search_products":
        query = arguments["query"].lower()
        category = arguments.get("category")
        matches = []
        for pid, p in PRODUCTS.items():
            if category and p["category"] != category:
                continue
            if query in p["name"].lower() or query in p["description"].lower() or query in p["category"]:
                matches.append(f"  {pid}: {p['name']} — ${p['price']:.2f}\n    {p['description']}")
        if not matches:
            return [types.TextContent(type="text", text=f"No products found for '{arguments['query']}'.")]
        return [types.TextContent(type="text", text=f"Found {len(matches)} product(s):\n\n" + "\n\n".join(matches))]

    elif name == "get_nutrition":
        pid = arguments["product_id"]
        p = PRODUCTS.get(pid)
        if not p:
            return [types.TextContent(type="text", text=f"Product '{pid}' not found.")]
        return [types.TextContent(type="text", text=(
            f"{p['name']}\n"
            f"  Calories:  {p['calories']} per serving\n"
            f"  Protein:   {p['protein_g']}g\n"
            f"  Fat:       {p['fat_g']}g\n"
            f"  Organic:   {'Yes' if p['organic'] else 'No'}\n"
            f"  Price:     ${p['price']:.2f}"
        ))]

    elif name == "check_stock":
        pid = arguments["product_id"]
        store = arguments["store"]
        if store not in STOCK:
            return [types.TextContent(type="text", text=f"Unknown store '{store}'. Valid: downtown, westside, eastside.")]
        if pid not in PRODUCTS:
            return [types.TextContent(type="text", text=f"Product '{pid}' not found.")]
        qty = STOCK[store].get(pid, 0)
        name_str = PRODUCTS[pid]["name"]
        status = f"IN STOCK ({qty} units)" if qty > 0 else "OUT OF STOCK"
        return [types.TextContent(type="text", text=f"{name_str} at {store}: {status}")]

    raise ValueError(f"Unknown tool: {name}")


# --- Run ---

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
