---
name: r2r-rag-query
description: Query indexed documents using R2R's RAG (Retrieval-Augmented Generation) system. Use when user asks questions about documentation, needs semantic search across knowledge base, wants context-aware answers with citations, or requires information retrieval from indexed content.
allowed-tools: mcp__r2r__rag, mcp__r2r__search
---

# R2R RAG Query Skill

## When to Use This Skill

Activate this skill when:
- User asks questions about indexed documents or knowledge base
- Need to find and synthesize information from multiple sources
- Semantic search is required (meaning-based, not just keywords)
- User wants answers with source citations
- Exploring documentation, API references, or technical content
- User mentions: "search docs", "find information", "what does the documentation say", "look up"

## Core Capabilities

1. **Semantic Search** - Find contextually relevant documents
2. **Hybrid Search** - Combine keyword + semantic search for best results
3. **RAG Queries** - Get AI-generated answers grounded in indexed content
4. **Source Citations** - Provide references for all information

## How to Use

### Quick Search (Fast)
Use `mcp__r2r__search` for quick lookups:
```json
{
  "query": "user's question",
  "mode": "advanced",
  "limit": 10
}
```

### Detailed Answer (RAG)
Use `mcp__r2r__rag` for comprehensive answers:
```json
{
  "query": "user's question",
  "stream": false,
  "search_settings": {
    "search_mode": "advanced",
    "limit": 10
  }
}
```

### Streaming Response
For long-form answers, use streaming:
```json
{
  "query": "explain in detail...",
  "stream": true
}
```

## Search Modes

| Mode | Use Case | Performance |
|------|----------|-------------|
| `basic` | Simple semantic search | Fastest |
| `advanced` | Hybrid search (recommended) | Balanced |
| `custom` | Full control over parameters | Flexible |

## Best Practices

1. **Start with Search**: Use `r2r_search` first to find relevant documents
2. **Then RAG**: If user needs detailed answer, follow up with `r2r_rag`
3. **Set Appropriate Limits**: 10-20 results for quality, 3-5 for speed
4. **Use Filters**: When searching specific document types:
   ```json
   {
     "filters": {
       "title": {"$in": ["api_docs.pdf", "guide.md"]}
     }
   }
   ```
5. **Cite Sources**: Always mention which documents informed your answer
6. **Stream Long Responses**: Use `stream: true` for detailed explanations

## Example Workflows

### Research Question
```
User: "How does authentication work in our system?"

1. r2r_search({query: "authentication system", mode: "advanced", limit: 10})
2. Review search results
3. r2r_rag({query: "explain authentication flow", search_settings: {limit: 10}})
4. Provide answer with citations
```

### Documentation Lookup
```
User: "Find API endpoints for user management"

1. r2r_search({query: "user management API endpoints", mode: "advanced"})
2. Present top results with scores
3. If user wants details: r2r_rag for comprehensive answer
```

## Output Format

When providing answers:
```markdown
## Answer
[AI-generated response from RAG]

## Sources
- **Document Title** (relevance: 0.85)
  - [Relevant excerpt]
- **Another Doc** (relevance: 0.72)
  - [Another excerpt]

## Confidence
Based on [X] documents with average relevance score of [Y]
```

## Limitations

- Only searches indexed documents (use `r2r_list_documents` to see what's available)
- Quality depends on indexing quality
- Very recent documents may still be processing (check with `r2r_list_documents`)
- Complex queries may need rephrasing for better results

## Tips for Better Results

1. **Specific Queries**: "API authentication flow" > "how to login"
2. **Use Keywords**: Include technical terms user mentioned
3. **Multi-Step Search**: Broad search → narrow down → detailed RAG
4. **Check Document Status**: Verify documents are fully indexed
5. **Combine with Code Search**: Use `Grep` for code, `r2r_search` for docs

## See Also

- `r2r-knowledge-graph` skill for entity-based exploration
- `r2r-document-manager` skill for ingestion and management
- Built-in `Grep` and `Read` tools for code-level search
