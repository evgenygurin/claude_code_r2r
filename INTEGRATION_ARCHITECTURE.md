# R2R + Claude Code: Оптимальная Архитектура Интеграции

## Executive Summary

Данный документ описывает оптимальную стратегию интеграции R2R API с Claude Code через множественные механизмы для достижения параллельной/фоновой работы без длительных ожиданий.

## Ключевые Требования

1. ✅ **Нет длительных ожиданий** - асинхронные операции
2. ✅ **Параллельная/фоновая работа** - не блокирует основной поток
3. ✅ **Автоматическая загрузка данных** - фоновая индексация
4. ✅ **Доступность для Claude Agent** - нативная интеграция

## Архитектура Решения

### Уровень 1: MCP Server для R2R (ОСНОВНОЙ - Highest Priority)

**Почему MCP?**
- Нативная интеграция с Claude Code
- Поддержка HTTP транспорта (R2R уже HTTP API)
- Tools доступны Claude автоматически
- Асинхронные операции "из коробки"

**Компоненты:**

```
r2r-mcp-server/
├── src/
│   ├── server.ts          # MCP HTTP server
│   ├── r2r-client.ts      # R2R API wrapper
│   ├── tools/
│   │   ├── ingest.ts      # Document ingestion (async)
│   │   ├── search.ts      # Vector/hybrid search
│   │   ├── rag.ts         # RAG queries (streaming)
│   │   ├── kg-search.ts   # Knowledge graph search
│   │   └── status.ts      # Check ingestion status
│   └── types/
│       └── r2r-types.ts   # TypeScript types for R2R API
├── package.json
└── README.md
```

**Ключевые возможности:**
- ✅ Асинхронная загрузка документов (возвращает task_id)
- ✅ Streaming RAG для постепенных ответов
- ✅ Параллельный поиск (множественные запросы)
- ✅ Мониторинг статуса операций

### Уровень 2: Hooks для Автоматизации (ВТОРИЧНЫЙ)

**SessionStart Hook** - загрузка контекста
```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/r2r-load-context.sh"
      }]
    }]
  }
}
```

**PostToolUse Hook** - автоиндексация файлов
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/r2r-auto-index.sh"
      }]
    }]
  }
}
```

**UserPromptSubmit Hook** - обогащение запросов
```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "hooks": [{
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/r2r-enrich-prompt.sh"
      }]
    }]
  }
}
```

### Уровень 3: Agent Skills для R2R (ТРЕТИЧНЫЙ)

**Skills структура:**
```
.claude/skills/
├── r2r-rag/
│   ├── SKILL.md           # RAG query skill
│   └── examples.md
├── r2r-knowledge-graph/
│   ├── SKILL.md           # Knowledge graph exploration
│   └── reference.md
└── r2r-document-manager/
    ├── SKILL.md           # Document management
    └── scripts/
        └── batch-ingest.py
```

**Примеры Skills:**

**r2r-rag/SKILL.md:**
```yaml
---
name: r2r-rag-query
description: Query documents using R2R's RAG system. Use when user asks questions about indexed documents, needs semantic search, or wants to retrieve contextual information from the knowledge base.
allowed-tools: mcp__r2r__rag, mcp__r2r__search
---

# R2R RAG Query Skill

## When to Use
- User asks questions about indexed documents
- Need to find relevant information from knowledge base
- Semantic search across document collection
- Context-aware answers with citations

## How to Use
1. Use `mcp__r2r__search` for quick lookups
2. Use `mcp__r2r__rag` for detailed answers with context
3. Stream results for long responses
4. Include filters when searching specific document types

## Best Practices
- Always specify search_mode (basic/advanced/custom)
- Use hybrid search for best results
- Set appropriate limits (10-20 for quality)
- Request streaming for long RAG responses
```

### Уровень 4: Specialized Subagents (ОПЦИОНАЛЬНЫЙ)

**Research Agent** - глубокий анализ через R2R
```yaml
---
name: r2r-researcher
description: Deep research agent that uses R2R knowledge base to find comprehensive information. Use proactively when user needs detailed research or analysis of indexed content.
tools: mcp__r2r__search, mcp__r2r__rag, mcp__r2r__kg_search, Read, Write
model: sonnet
---

You are a research specialist with access to R2R knowledge base.

When invoked:
1. Understand research question thoroughly
2. Use R2R hybrid search to find relevant documents
3. Use knowledge graph search for entity relationships
4. Use RAG for detailed answers with citations
5. Synthesize findings into comprehensive report

Research process:
- Start broad with semantic search
- Narrow down with filters
- Explore entity relationships via KG
- Generate detailed summary with RAG
- Cite all sources with document IDs

Output format:
- Executive summary
- Key findings (bullet points)
- Detailed analysis
- Source citations
- Recommendations for further research
```

## Детальная Имплементация

### 1. MCP Server для R2R

**Installation:**
```bash
# Add R2R MCP server
claude mcp add --transport http r2r http://136.119.36.216:7272/mcp

# Or via project .mcp.json
cat > .mcp.json << 'EOF'
{
  "mcpServers": {
    "r2r": {
      "type": "http",
      "url": "http://136.119.36.216:7272/mcp",
      "description": "R2R RAG and search capabilities"
    }
  }
}
EOF
```

**Если нужно создать собственный MCP wrapper:**

```typescript
// src/server.ts
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { R2RClient } from './r2r-client.js';

const R2R_BASE_URL = process.env.R2R_BASE_URL || 'http://136.119.36.216:7272';
const r2rClient = new R2RClient(R2R_BASE_URL);

const server = new Server(
  {
    name: 'r2r-mcp-server',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'r2r_ingest',
        description: 'Ingest documents into R2R (async). Returns task_id for status tracking.',
        inputSchema: {
          type: 'object',
          properties: {
            file_path: { type: 'string', description: 'Path to file to ingest' },
            mode: {
              type: 'string',
              enum: ['fast', 'hi-res', 'custom'],
              default: 'fast',
              description: 'Ingestion mode'
            },
            metadata: {
              type: 'object',
              description: 'Optional metadata for the document'
            }
          },
          required: ['file_path']
        }
      },
      {
        name: 'r2r_search',
        description: 'Search documents using vector/hybrid search. Fast, synchronous operation.',
        inputSchema: {
          type: 'object',
          properties: {
            query: { type: 'string', description: 'Search query' },
            mode: {
              type: 'string',
              enum: ['basic', 'advanced', 'custom'],
              default: 'advanced'
            },
            limit: { type: 'number', default: 10 },
            filters: { type: 'object', description: 'Optional filters' }
          },
          required: ['query']
        }
      },
      {
        name: 'r2r_rag',
        description: 'Retrieval-Augmented Generation query. Returns AI-generated answer based on indexed documents.',
        inputSchema: {
          type: 'object',
          properties: {
            query: { type: 'string', description: 'Question to answer' },
            stream: { type: 'boolean', default: false },
            search_settings: { type: 'object' },
            rag_generation_config: { type: 'object' }
          },
          required: ['query']
        }
      },
      {
        name: 'r2r_kg_search',
        description: 'Knowledge graph search for entity relationships.',
        inputSchema: {
          type: 'object',
          properties: {
            query: { type: 'string' },
            kg_search_type: {
              type: 'string',
              enum: ['local', 'global'],
              default: 'local'
            }
          },
          required: ['query']
        }
      },
      {
        name: 'r2r_check_status',
        description: 'Check status of async operations (ingestion, etc).',
        inputSchema: {
          type: 'object',
          properties: {
            task_id: { type: 'string', description: 'Task ID from async operation' }
          },
          required: ['task_id']
        }
      },
      {
        name: 'r2r_list_documents',
        description: 'List all indexed documents with their status.',
        inputSchema: {
          type: 'object',
          properties: {
            limit: { type: 'number', default: 100 },
            offset: { type: 'number', default: 0 }
          }
        }
      }
    ]
  };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case 'r2r_ingest':
        return await r2rClient.ingestDocument(args);

      case 'r2r_search':
        return await r2rClient.search(args);

      case 'r2r_rag':
        return await r2rClient.rag(args);

      case 'r2r_kg_search':
        return await r2rClient.kgSearch(args);

      case 'r2r_check_status':
        return await r2rClient.checkStatus(args.task_id);

      case 'r2r_list_documents':
        return await r2rClient.listDocuments(args);

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    return {
      content: [{
        type: 'text',
        text: `Error: ${error.message}`
      }],
      isError: true
    };
  }
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('R2R MCP Server running on stdio');
}

main().catch((error) => {
  console.error('Server error:', error);
  process.exit(1);
});
```

```typescript
// src/r2r-client.ts
import fetch from 'node-fetch';

export class R2RClient {
  constructor(private baseUrl: string) {}

  async ingestDocument(args: any) {
    const formData = new FormData();
    formData.append('file', args.file_path);
    formData.append('ingestion_mode', args.mode || 'fast');

    if (args.metadata) {
      formData.append('metadata', JSON.stringify(args.metadata));
    }

    const response = await fetch(`${this.baseUrl}/v3/documents`, {
      method: 'POST',
      body: formData
    });

    const data = await response.json();

    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          status: 'success',
          message: 'Document ingestion started (async)',
          document_id: data.results[0]?.document_id,
          task_info: 'Ingestion is processing in background. Use r2r_list_documents to check status.'
        }, null, 2)
      }]
    };
  }

  async search(args: any) {
    const response = await fetch(`${this.baseUrl}/v3/retrieval/search`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: args.query,
        search_settings: {
          search_mode: args.mode || 'advanced',
          limit: args.limit || 10,
          filters: args.filters || {}
        }
      })
    });

    const data = await response.json();

    return {
      content: [{
        type: 'text',
        text: JSON.stringify(data.results, null, 2)
      }]
    };
  }

  async rag(args: any) {
    const endpoint = args.stream
      ? `${this.baseUrl}/v3/retrieval/rag?stream=true`
      : `${this.baseUrl}/v3/retrieval/rag`;

    const response = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: args.query,
        search_settings: args.search_settings || {},
        rag_generation_config: args.rag_generation_config || {}
      })
    });

    if (args.stream) {
      // Handle streaming response
      let fullText = '';
      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        fullText += decoder.decode(value, { stream: true });
      }

      return {
        content: [{ type: 'text', text: fullText }]
      };
    } else {
      const data = await response.json();
      return {
        content: [{
          type: 'text',
          text: JSON.stringify(data.results, null, 2)
        }]
      };
    }
  }

  async kgSearch(args: any) {
    const response = await fetch(`${this.baseUrl}/v3/retrieval/search`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: args.query,
        graph_search_settings: {
          use_graph_search: true,
          kg_search_type: args.kg_search_type || 'local'
        }
      })
    });

    const data = await response.json();
    return {
      content: [{
        type: 'text',
        text: JSON.stringify(data.results, null, 2)
      }]
    };
  }

  async listDocuments(args: any) {
    const response = await fetch(
      `${this.baseUrl}/v3/documents?limit=${args.limit || 100}&offset=${args.offset || 0}`
    );

    const data = await response.json();
    return {
      content: [{
        type: 'text',
        text: JSON.stringify(data.results, null, 2)
      }]
    };
  }

  async checkStatus(taskId: string) {
    // Implementation depends on R2R's status endpoint
    return {
      content: [{
        type: 'text',
        text: 'Status checking not yet implemented. Use r2r_list_documents to see ingestion status.'
      }]
    };
  }
}
```

**package.json:**
```json
{
  "name": "r2r-mcp-server",
  "version": "1.0.0",
  "type": "module",
  "main": "dist/server.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/server.js"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^0.5.0",
    "node-fetch": "^3.3.2"
  },
  "devDependencies": {
    "@types/node": "^20.10.0",
    "typescript": "^5.3.0"
  }
}
```

### 2. Hooks Implementation

**r2r-load-context.sh** (SessionStart):
```bash
#!/bin/bash
# Load relevant R2R documents at session start

INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id')
PROJECT_DIR=$(echo "$INPUT" | jq -r '.cwd')

# Quick search for project-related docs
curl -s -X POST http://136.119.36.216:7272/v3/retrieval/search \
  -H "Content-Type: application/json" \
  -d "{
    \"query\": \"project overview $(basename $PROJECT_DIR)\",
    \"search_settings\": {
      \"search_mode\": \"advanced\",
      \"limit\": 5
    }
  }" | jq -r '.results.chunk_search_results[]? | "📄 \(.metadata.title // "Unknown"): \(.text | .[0:200])..."'

exit 0
```

**r2r-auto-index.sh** (PostToolUse on Write/Edit):
```bash
#!/bin/bash
# Auto-index newly created/edited files in background

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name')
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path')

# Only process Write/Edit tools
if [[ "$TOOL_NAME" != "Write" && "$TOOL_NAME" != "Edit" ]]; then
  exit 0
fi

# Only index documentation files
if [[ ! "$FILE_PATH" =~ \.(md|txt|py|ts|js|json)$ ]]; then
  exit 0
fi

# Background ingestion (fire and forget)
(
  curl -s -X POST http://136.119.36.216:7272/v3/documents \
    -F "file=@$FILE_PATH" \
    -F "ingestion_mode=fast" \
    -F "metadata={\"source\":\"claude_code_auto\",\"file\":\"$FILE_PATH\"}" \
    > /dev/null 2>&1
) &

# Return success immediately (don't wait for ingestion)
echo "Background indexing started for: $FILE_PATH"
exit 0
```

**r2r-enrich-prompt.sh** (UserPromptSubmit):
```bash
#!/bin/bash
# Enrich user prompts with relevant context from R2R

INPUT=$(cat)
USER_PROMPT=$(echo "$INPUT" | jq -r '.prompt')

# Quick semantic search for relevant docs
RESULTS=$(curl -s -X POST http://136.119.36.216:7272/v3/retrieval/search \
  -H "Content-Type: application/json" \
  -d "{
    \"query\": \"$USER_PROMPT\",
    \"search_settings\": {
      \"search_mode\": \"advanced\",
      \"limit\": 3
    }
  }")

# Extract relevant snippets
CONTEXT=$(echo "$RESULTS" | jq -r '.results.chunk_search_results[]? | "- \(.metadata.title // "Doc"): \(.text | .[0:150])..."' | head -5)

if [ -n "$CONTEXT" ]; then
  cat << EOF
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "📚 Relevant documents from R2R knowledge base:\n$CONTEXT"
  }
}
EOF
fi

exit 0
```

### 3. Skills Implementation

**Complete skill files готовы к созданию:**

`.claude/skills/r2r-rag/SKILL.md` - см. выше
`.claude/skills/r2r-knowledge-graph/SKILL.md`
`.claude/skills/r2r-document-manager/SKILL.md`

### 4. Plugin Bundle (РЕКОМЕНДУЕТСЯ для team distribution)

```
r2r-integration-plugin/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── r2r-search.md
│   └── r2r-ingest.md
├── agents/
│   └── r2r-researcher.md
├── skills/
│   ├── r2r-rag/
│   │   └── SKILL.md
│   └── r2r-knowledge-graph/
│       └── SKILL.md
├── hooks/
│   └── hooks.json
├── .mcp.json              # MCP server config
└── README.md
```

**plugin.json:**
```json
{
  "name": "r2r-integration",
  "description": "Complete R2R integration for Claude Code with MCP, hooks, skills, and agents",
  "version": "1.0.0",
  "author": {
    "name": "Your Team"
  }
}
```

## Workflow Examples

### Example 1: Automatic Document Indexing

```bash
# User writes a new document
> Write a comprehensive guide about our API

# Claude creates the file
# PostToolUse hook automatically triggers
# File is sent to R2R for indexing in background
# No waiting - continues immediately
```

### Example 2: RAG-Enhanced Coding

```bash
# User asks a question
> How do we handle authentication in this codebase?

# UserPromptSubmit hook enriches prompt with R2R context
# Claude receives both the question AND relevant docs
# Provides more accurate answer with citations
```

### Example 3: Deep Research with Subagent

```bash
> Use the r2r-researcher agent to analyze our security architecture

# Research agent spawned with dedicated context
# Performs multiple R2R searches in parallel
# Explores knowledge graph for entity relationships
# Compiles comprehensive report
# Returns to main thread with findings
```

### Example 4: Headless Batch Processing

```bash
#!/bin/bash
# Batch index all documentation

for file in docs/**/*.md; do
  claude -p "Index this file: $file" \
    --allowedTools "mcp__r2r__ingest" \
    --output-format json \
    --no-interactive
done
```

## Performance Characteristics

| Operation | Mode | Latency | Blocking? |
|-----------|------|---------|-----------|
| Document Ingest | Async | ~50ms | ❌ No (returns immediately) |
| Vector Search | Sync | ~100-300ms | ✅ Yes (but fast) |
| RAG Query | Sync/Stream | ~1-3s | ⚠️ Optional (use stream) |
| KG Search | Sync | ~200-500ms | ✅ Yes (but fast) |
| Auto-indexing (hook) | Background | N/A | ❌ No (fire & forget) |

## Security Considerations

1. **API Authentication**: Store R2R credentials in environment variables
2. **Hook validation**: Use `allowed-tools` in skills to restrict capabilities
3. **Rate limiting**: Implement backoff in hooks for bulk operations
4. **Data privacy**: Be careful with sensitive documents

## Deployment Checklist

- [ ] Install R2R MCP server (`claude mcp add`)
- [ ] Configure project hooks in `.claude/settings.json`
- [ ] Create skills in `.claude/skills/`
- [ ] Test MCP tools with `/mcp` command
- [ ] Verify hooks with `claude --debug`
- [ ] Document team workflows in README

## Next Steps

1. **Phase 1 (MVP)**: MCP Server only
2. **Phase 2**: Add SessionStart + PostToolUse hooks
3. **Phase 3**: Create RAG skills
4. **Phase 4**: Bundle as plugin for team distribution
5. **Phase 5**: Add specialized subagents

---

**Author**: Claude + User Collaboration
**Date**: 2025-01-19
**Status**: Architecture Complete ✅
