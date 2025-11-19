# R2R + Claude Code - Quick Start Guide

## 5-Minute Setup

### 1. Install MCP Server
```bash
cd r2r-mcp-server
npm install && npm run build
claude mcp add --transport stdio r2r -- node $(pwd)/dist/server.js
```

### 2. Verify Installation
```bash
claude mcp list  # Should show "r2r"
```

### 3. Test It!
```bash
cd /path/to/your/project
claude

# In Claude:
> /mcp
# You should see: r2r_search, r2r_rag, r2r_ingest, etc.

> Use r2r_search to find documentation about "authentication"
```

### 4. Enable Background Features (Optional)
Hooks and skills are already configured in `.claude/`!

## Your First R2R Queries

### Search Documents
```
> Search R2R for "API documentation" and show top 5 results
```

### Ask Questions (RAG)
```
> Use r2r_rag to explain how authentication works based on our docs
```

### Index New Documents
```
> Index the file docs/api-guide.md using r2r_ingest in fast mode
```

## What Happens Automatically

✅ **SessionStart**: Loads relevant docs when you start Claude
✅ **PostToolUse**: Auto-indexes files you create/edit
✅ **UserPromptSubmit**: Enriches prompts with R2R context

## Next Steps

1. Read [README.md](README.md) for detailed usage
2. Check [INTEGRATION_ARCHITECTURE.md](INTEGRATION_ARCHITECTURE.md) for technical details
3. Explore skills in `.claude/skills/`

## Common Issues

**"r2r tools not found"**
```bash
claude mcp remove r2r
claude mcp add --transport stdio r2r -- node /absolute/path/to/r2r-mcp-server/dist/server.js
```

**"R2R API error"**
```bash
curl http://136.119.36.216:7272/v3/health
# Verify R2R server is running
```

Happy R2Ring! 🚀
