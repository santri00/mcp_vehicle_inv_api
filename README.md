# mcp-vehicle-inv-api

An MCP (Model Context Protocol) server that adapts the [golang-api-example](../golang-api-example) vehicle inventory REST API into tools an MCP client (Claude Code, Claude Desktop) can call.

## Tools exposed

| Tool | Maps to |
|---|---|
| `add_vehicle` | `POST /inventory/v1/vehicles` |
| `list_vehicles` | `GET /inventory/v1/vehicles?offset=&limit=` |
| `get_vehicle_by_stock_id` | `GET /inventory/v1/vehicles/{stock_id}` |

## Setup

```bash
uv sync
```

Configure the target API (defaults to `http://localhost:3001/inventory/v1`, matching the golang-api-example docker-compose setup):

```bash
cp .env.example .env
# edit .env if the Go API runs elsewhere
```

## Run standalone / inspect with MCP Inspector

Make sure the Go API is running first (from the `golang-api-example` repo):

```bash
make up
```

Then, from this project:

```bash
uv run mcp dev src/mcp_vehicle_inv_api/server.py
```

This opens the MCP Inspector where each tool can be called manually to verify it talks to the Go API correctly.

## Wire into Claude Code / Claude Code Desktop

Add an entry to `.mcp.json` in the project you'll chat from (`../.mcp.json` for an example already set up):

```json
{
  "mcpServers": {
    "vehicle-inventory": {
      "command": "uv",
      "args": ["run", "--directory", "/absolute/path/to/mcp-vehicle-inv-api", "mcp-vehicle-inv-api"],
      "env": {
        "GOLANG_API_BASE_URL": "http://localhost:3001/inventory/v1"
      }
    }
  }
}
```

Restart Claude Code / Claude Code Desktop so it picks up the new server, then ask Claude to add, list, or look up a vehicle by stock ID.
