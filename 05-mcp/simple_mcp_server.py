"""
simple_mcp_server.py — A Basic MCP Server with 3 Tools
=======================================================

This is a simple MCP (Model Context Protocol) server that exposes three tools:
  1. get_weather      — Returns simulated weather for a Hawaii location
  2. search_listings  — Returns simulated real estate listings
  3. calculate_mortgage — Calculates monthly mortgage payments

HOW IT WORKS:
  - This server communicates over stdio (standard input/output).
  - An MCP client (like Claude Desktop or Claude Code) launches this script
    as a subprocess and sends JSON-RPC messages to it.
  - The AI model (Claude) sees the tool definitions and decides when to call them.

TO INSTALL DEPENDENCIES:
  pip install mcp

TO USE WITH CLAUDE DESKTOP:
  Add this to your claude_desktop_config.json:

  {
    "mcpServers": {
      "real-estate-tools": {
        "command": "python",
        "args": ["/full/path/to/simple_mcp_server.py"]
      }
    }
  }

  Then restart Claude Desktop. The tools will appear in the tools menu.

TO TEST STANDALONE (for development):
  python simple_mcp_server.py
"""

from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types

# ---------------------------------------------------------------------------
# Create the MCP server instance
# ---------------------------------------------------------------------------
# The name "real-estate-tools" is what clients will see as the server identity.
server = Server("real-estate-tools")


# ---------------------------------------------------------------------------
# Tool Definitions
# ---------------------------------------------------------------------------
# The @server.list_tools() decorator tells the MCP client what tools are
# available. Each tool has a name, description, and input schema (JSON Schema).
# The AI model reads these descriptions to decide WHEN and HOW to call them.

@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """Return the list of tools this server provides."""
    return [
        types.Tool(
            name="get_weather",
            description=(
                "Get the current weather for a location in Hawaii. "
                "Returns temperature, conditions, and humidity. "
                "Use this when the user asks about weather or climate in a specific area."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The location to get weather for (e.g., 'Kailua', 'Waikiki', 'Maui')"
                    }
                },
                "required": ["location"]
            }
        ),
        types.Tool(
            name="search_listings",
            description=(
                "Search for residential real estate listings in Hawaii. "
                "Returns matching properties with price, bedrooms, and details. "
                "Use this when the user asks about available homes, properties, or listings."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The area to search (e.g., 'Kailua', 'Honolulu', 'North Shore')"
                    },
                    "max_price": {
                        "type": "number",
                        "description": "Maximum price in dollars (e.g., 1500000)"
                    },
                    "min_bedrooms": {
                        "type": "integer",
                        "description": "Minimum number of bedrooms (default: 1)"
                    }
                },
                "required": ["location"]
            }
        ),
        types.Tool(
            name="calculate_mortgage",
            description=(
                "Calculate the estimated monthly mortgage payment for a home. "
                "Takes into account loan amount, interest rate, and loan term. "
                "Use this when the user wants to know monthly payments or affordability."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "home_price": {
                        "type": "number",
                        "description": "The price of the home in dollars"
                    },
                    "down_payment_percent": {
                        "type": "number",
                        "description": "Down payment as a percentage (e.g., 20 for 20%). Default: 20"
                    },
                    "interest_rate": {
                        "type": "number",
                        "description": "Annual interest rate as a percentage (e.g., 6.5). Default: 6.5"
                    },
                    "loan_term_years": {
                        "type": "integer",
                        "description": "Loan term in years (e.g., 30). Default: 30"
                    }
                },
                "required": ["home_price"]
            }
        ),
    ]


# ---------------------------------------------------------------------------
# Tool Implementations
# ---------------------------------------------------------------------------
# The @server.call_tool() decorator handles the actual execution when
# the AI model decides to call a tool. The client sends the tool name
# and arguments, and this function returns the result.

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Execute a tool and return the result."""

    if name == "get_weather":
        return handle_get_weather(arguments)
    elif name == "search_listings":
        return handle_search_listings(arguments)
    elif name == "calculate_mortgage":
        return handle_calculate_mortgage(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")


# ---------------------------------------------------------------------------
# Tool Handler Functions
# ---------------------------------------------------------------------------

def handle_get_weather(arguments: dict) -> list[types.TextContent]:
    """
    Simulated weather data for Hawaii locations.

    In a real implementation, this would call a weather API like OpenWeatherMap.
    For training purposes, we return realistic simulated data.
    """
    location = arguments.get("location", "Honolulu")

    # Simulated weather data for various Hawaii locations
    weather_data = {
        "kailua": {"temp": 82, "conditions": "Partly Cloudy", "humidity": 65, "wind": "12 mph NE"},
        "waikiki": {"temp": 85, "conditions": "Sunny", "humidity": 60, "wind": "8 mph E"},
        "honolulu": {"temp": 84, "conditions": "Sunny", "humidity": 62, "wind": "10 mph NE"},
        "north shore": {"temp": 80, "conditions": "Light Showers", "humidity": 72, "wind": "15 mph N"},
        "maui": {"temp": 83, "conditions": "Mostly Sunny", "humidity": 58, "wind": "11 mph NE"},
        "kona": {"temp": 86, "conditions": "Clear", "humidity": 55, "wind": "6 mph SW"},
        "hilo": {"temp": 79, "conditions": "Rainy", "humidity": 80, "wind": "5 mph E"},
    }

    # Look up weather (case-insensitive), default to generic data
    data = weather_data.get(location.lower(), {
        "temp": 83,
        "conditions": "Partly Cloudy",
        "humidity": 65,
        "wind": "10 mph NE"
    })

    result = (
        f"Weather for {location}, Hawaii:\n"
        f"  Temperature: {data['temp']}F\n"
        f"  Conditions:  {data['conditions']}\n"
        f"  Humidity:    {data['humidity']}%\n"
        f"  Wind:        {data['wind']}"
    )

    return [types.TextContent(type="text", text=result)]


def handle_search_listings(arguments: dict) -> list[types.TextContent]:
    """
    Simulated real estate listing search.

    In a real implementation, this would query an MLS API or database.
    For training purposes, we return realistic simulated listings.
    """
    location = arguments.get("location", "Honolulu")
    max_price = arguments.get("max_price", float("inf"))
    min_bedrooms = arguments.get("min_bedrooms", 1)

    # Simulated listing database
    all_listings = [
        {
            "address": "123 Kailua Rd, Kailua",
            "area": "kailua",
            "price": 1_250_000,
            "bedrooms": 3,
            "bathrooms": 2,
            "sqft": 1_650,
            "description": "Charming single-family home steps from Kailua Beach. Updated kitchen, tropical garden."
        },
        {
            "address": "456 Lanikai Loop, Kailua",
            "area": "kailua",
            "price": 2_100_000,
            "bedrooms": 4,
            "bathrooms": 3,
            "sqft": 2_400,
            "description": "Stunning Lanikai home with ocean views. Open floor plan, pool, and lush landscaping."
        },
        {
            "address": "789 Ala Moana Blvd #2105, Honolulu",
            "area": "honolulu",
            "price": 890_000,
            "bedrooms": 2,
            "bathrooms": 2,
            "sqft": 1_100,
            "description": "Luxury condo in Ala Moana with panoramic ocean views. Building amenities include pool and gym."
        },
        {
            "address": "321 Kam Hwy, North Shore",
            "area": "north shore",
            "price": 1_450_000,
            "bedrooms": 3,
            "bathrooms": 2,
            "sqft": 1_800,
            "description": "Plantation-style home near Pipeline. Large lot with fruit trees. Surf lifestyle living."
        },
        {
            "address": "555 Waialae Ave, Kahala",
            "area": "honolulu",
            "price": 3_200_000,
            "bedrooms": 5,
            "bathrooms": 4,
            "sqft": 3_500,
            "description": "Elegant Kahala estate with pool, guest house, and mature gardens. Minutes to beach."
        },
        {
            "address": "88 Kihei Rd, Maui",
            "area": "maui",
            "price": 975_000,
            "bedrooms": 2,
            "bathrooms": 2,
            "sqft": 1_200,
            "description": "Ocean-view condo in South Maui. Turn-key furnished, strong vacation rental history."
        },
    ]

    # Filter listings based on criteria
    matches = [
        listing for listing in all_listings
        if (location.lower() in listing["area"].lower() or
            location.lower() in listing["address"].lower())
        and listing["price"] <= max_price
        and listing["bedrooms"] >= min_bedrooms
    ]

    if not matches:
        return [types.TextContent(
            type="text",
            text=f"No listings found in {location} matching your criteria (max ${max_price:,.0f}, {min_bedrooms}+ beds)."
        )]

    # Format results
    lines = [f"Found {len(matches)} listing(s) in {location}:\n"]
    for i, listing in enumerate(matches, 1):
        lines.append(
            f"{i}. {listing['address']}\n"
            f"   Price:    ${listing['price']:,.0f}\n"
            f"   Beds/Bath: {listing['bedrooms']}bd / {listing['bathrooms']}ba\n"
            f"   Sq Ft:    {listing['sqft']:,}\n"
            f"   Details:  {listing['description']}\n"
        )

    return [types.TextContent(type="text", text="\n".join(lines))]


def handle_calculate_mortgage(arguments: dict) -> list[types.TextContent]:
    """
    Calculate monthly mortgage payment using the standard amortization formula.

    Formula: M = P * [r(1+r)^n] / [(1+r)^n - 1]
    Where:
      M = monthly payment
      P = loan principal
      r = monthly interest rate
      n = total number of payments
    """
    home_price = arguments["home_price"]
    down_payment_pct = arguments.get("down_payment_percent", 20)
    annual_rate = arguments.get("interest_rate", 6.5)
    term_years = arguments.get("loan_term_years", 30)

    # Calculate loan details
    down_payment = home_price * (down_payment_pct / 100)
    loan_amount = home_price - down_payment
    monthly_rate = (annual_rate / 100) / 12
    num_payments = term_years * 12

    # Monthly payment formula
    if monthly_rate == 0:
        monthly_payment = loan_amount / num_payments
    else:
        monthly_payment = loan_amount * (
            (monthly_rate * (1 + monthly_rate) ** num_payments)
            / ((1 + monthly_rate) ** num_payments - 1)
        )

    # Total cost over loan lifetime
    total_paid = monthly_payment * num_payments
    total_interest = total_paid - loan_amount

    result = (
        f"Mortgage Estimate:\n"
        f"  Home Price:      ${home_price:,.0f}\n"
        f"  Down Payment:    ${down_payment:,.0f} ({down_payment_pct}%)\n"
        f"  Loan Amount:     ${loan_amount:,.0f}\n"
        f"  Interest Rate:   {annual_rate}%\n"
        f"  Loan Term:       {term_years} years\n"
        f"  ────────────────────────────\n"
        f"  Monthly Payment: ${monthly_payment:,.2f}\n"
        f"  ────────────────────────────\n"
        f"  Total Interest:  ${total_interest:,.0f}\n"
        f"  Total Cost:      ${total_paid:,.0f}"
    )

    return [types.TextContent(type="text", text=result)]


# ---------------------------------------------------------------------------
# Run the Server
# ---------------------------------------------------------------------------
# This starts the server using stdio transport. When Claude Desktop launches
# this script, it communicates with it through stdin/stdout using the MCP
# JSON-RPC protocol.

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
