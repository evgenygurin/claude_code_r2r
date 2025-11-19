# R2R MCP Server

Model Context Protocol (MCP) server for R2R RAG system integration with Claude Code.

## Features

- ✅ **Async Document Ingestion** - Non-blocking file indexing
- ✅ **Vector Search** - Semantic and hybrid search capabilities
- ✅ **RAG Queries** - Retrieval-augmented generation with streaming
- ✅ **Knowledge Graph** - Entity and relationship exploration
- ✅ **Document Management** - List, delete, and status checking

## Installation

```bash
# Install dependencies
npm install

# Build TypeScript
npm run build

# Test server
node dist/server.js
```

## Usage with Claude Code

### Install MCP Server

```bash
# Add to Claude Code
claude mcp add --transport stdio r2r \
  -- node /absolute/path/to/dist/server.js

# With custom R2R URL
claude mcp add --transport stdio r2r \
  --env R2R_BASE_URL=http://custom:7272 \
  -- node /absolute/path/to/dist/server.js
```

### Verify Installation

```bash
# List MCP servers
claude mcp list

# Start Claude Code and test
claude
> /mcp
# Should show r2r tools
```

## Available Tools

### r2r_ingest
Ingest documents into R2R (async operation).

**Parameters:**
- `file_path` (string, required) - Absolute path to file
- `mode` (string) - Ingestion mode: `fast`, `hi-res`, `custom`
- `metadata` (object) - Optional metadata
- `chunks` (array) - Pre-processed chunks (alternative to file_path)

**Example:**
```json
{
  "file_path": "/path/to/document.pdf",
  "mode": "fast",
  "metadata": {
    "category": "api_docs",
    "version": "2.0"
  }
}
```

### r2r_search
Search indexed documents.

**Parameters:**
- `query` (string, required) - Search query
- `mode` (string) - Search mode: `basic`, `advanced`, `custom`
- `limit` (number) - Max results (default: 10)
- `use_hybrid_search` (boolean) - Enable hybrid search
- `filters` (object) - Optional filters

**Example:**
```json
{
  "query": "authentication API",
  "mode": "advanced",
  "limit": 10
}
```

### r2r_rag
Retrieval-augmented generation query.

**Parameters:**
- `query` (string, required) - Question to answer
- `stream` (boolean) - Enable streaming (default: false)
- `search_settings` (object) - Search configuration
- `rag_generation_config` (object) - LLM settings

**Example:**
```json
{
  "query": "Explain our authentication system",
  "stream": false,
  "search_settings": {
    "search_mode": "advanced",
    "limit": 10
  }
}
```

### r2r_kg_search
Knowledge graph search.

**Parameters:**
- `query` (string, required) - Entity or relationship query
- `kg_search_type` (string) - Type: `local` or `global`

**Example:**
```json
{
  "query": "authentication entities",
  "kg_search_type": "local"
}
```

### r2r_list_documents
List all indexed documents.

**Parameters:**
- `limit` (number) - Max documents (default: 100)
- `offset` (number) - Pagination offset (default: 0)

**Example:**
```json
{
  "limit": 50,
  "offset": 0
}
```

### r2r_delete_document
Delete a document from R2R.

**Parameters:**
- `document_id` (string, required) - UUID of document

**Example:**
```json
{
  "document_id": "9fbe403b-c11c-5aae-8ade-ef22980c3ad1"
}
```

## Configuration

### Environment Variables

- `R2R_BASE_URL` - R2R server URL (default: `http://136.119.36.216:7272`)

### Custom Configuration

```bash
# Set in shell
export R2R_BASE_URL="http://localhost:7272"
node dist/server.js

# Or pass via MCP
claude mcp add --transport stdio r2r \
  --env R2R_BASE_URL=http://custom:7272 \
  -- node dist/server.js
```

## Development

```bash
# Install dependencies
npm install

# Build
npm run build

# Watch mode
npm run watch

# Run directly
npm run dev
```

## Architecture

```
src/
├── server.ts          # MCP server implementation
├── r2r-client.ts      # R2R API client wrapper
└── types/
    └── r2r-types.ts   # TypeScript type definitions
```

## Error Handling

The server handles errors gracefully:
- Network errors → Returns error message to Claude
- File not found → Clear error with path
- API errors → Includes R2R status code and message
- Timeouts → Configurable per tool

## Performance

- **Ingestion**: Returns immediately (~50ms), actual indexing is async
- **Search**: 100-300ms for most queries
- **RAG**: 1-3s for generation
- **Streaming RAG**: Real-time token delivery

## Troubleshooting

### Server won't start
```bash
# Check Node version (need 18+)
node --version

# Rebuild
npm run build

# Check for errors
node dist/server.js
```

### R2R connection issues
```bash
# Test R2R directly
curl http://136.119.36.216:7272/v3/health

# Check environment
echo $R2R_BASE_URL
```

### Tools not appearing in Claude Code
```bash
# Remove and re-add
claude mcp remove r2r
claude mcp add --transport stdio r2r \
  -- node $(pwd)/dist/server.js

# Restart Claude Code
```

## License

MIT
