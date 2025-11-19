---
name: r2r-knowledge-graph
description: Explore knowledge graph for entity relationships and connections extracted from documents. Use when user asks about relationships, entities, "how X relates to Y", entity exploration, or graph-based queries. Complements semantic search with structured knowledge.
allowed-tools: mcp__r2r__kg_search, mcp__r2r__search
---

# R2R Knowledge Graph Skill

## When to Use This Skill

Activate when:
- User asks about relationships between concepts/entities
- Exploring connections: "how does X relate to Y?"
- Finding entities: "who/what is mentioned in..."
- Graph-based queries: dependencies, hierarchies, networks
- Complement semantic search with structured knowledge
- User mentions: "relationship", "connected", "related to", "entities", "mentions of"

## Core Capabilities

1. **Entity Extraction** - Identify people, places, concepts from documents
2. **Relationship Discovery** - Find how entities are connected
3. **Graph Navigation** - Explore knowledge graph structure
4. **Contextual Search** - Combine entities with vector search

## Knowledge Graph Types

### Local Search (Entity-Centric)
Focus on specific entity and its immediate connections:
```json
{
  "query": "Aristotle",
  "kg_search_type": "local"
}
```

**Use for:**
- "Tell me about [entity]"
- "What is [person/place/concept]?"
- Direct entity lookups

### Global Search (Graph-Wide)
Explore broader patterns and relationships:
```json
{
  "query": "philosophy influences",
  "kg_search_type": "global"
}
```

**Use for:**
- "How are [concepts] connected?"
- "What patterns exist in [domain]?"
- Cross-document relationship discovery

## How to Use

### 1. Entity Lookup
```
User: "Who is mentioned in the documentation about databases?"

mcp__r2r__kg_search({
  query: "database mentions",
  kg_search_type: "local"
})
```

### 2. Relationship Exploration
```
User: "How does authentication relate to authorization?"

mcp__r2r__kg_search({
  query: "authentication authorization relationship",
  kg_search_type: "global"
})
```

### 3. Combined with Semantic Search
```
1. Start with KG search for entities
2. Use results to refine semantic search query
3. Get detailed content with r2r_search

Example:
- KG: Find entities related to "microservices"
- Search: Use entity names for targeted document search
- RAG: Generate comprehensive answer
```

## Example Workflows

### Research Entity Connections
```
User: "What technologies are mentioned with Kubernetes?"

Workflow:
1. mcp__r2r__kg_search({
     query: "Kubernetes",
     kg_search_type: "local"
   })
2. Extract related entities (Docker, containers, orchestration, etc.)
3. Optional: mcp__r2r__search for detailed docs on each entity
4. Synthesize findings with entity relationships
```

### Trace Concept Evolution
```
User: "How has our authentication approach evolved?"

Workflow:
1. mcp__r2r__kg_search({
     query: "authentication history",
     kg_search_type: "global"
   })
2. Identify authentication-related entities across time
3. Map connections and changes
4. Present chronological relationship graph
```

## Output Format

### Entity Results
```markdown
## Entity: [Name]

**Type**: [Person/Concept/Technology/etc.]

**Related Entities**:
- [Entity 1] - [Relationship type]
- [Entity 2] - [Relationship type]

**Mentioned in**:
- Document A (context: ...)
- Document B (context: ...)
```

### Relationship Results
```markdown
## Relationships for "[Query]"

### Direct Connections
- [Entity A] ←→ [Entity B]: [Relationship description]

### Indirect Connections
- [Entity A] → [Entity C] → [Entity B]

### Context
[Where these relationships appear in documents]
```

## Best Practices

1. **Start Local, Go Global**
   - Begin with specific entity (local search)
   - Expand to patterns (global search)

2. **Combine with Semantic Search**
   - KG finds entities
   - Semantic search finds detailed content
   - RAG synthesizes comprehensive answer

3. **Iterate Queries**
   - Use KG results to refine next search
   - Follow relationship chains

4. **Verify with Documents**
   - KG shows connections
   - Always verify with source documents
   - Use `r2r_search` to get context

## Limitations

- Requires documents to be processed for KG extraction
- Quality depends on entity extraction accuracy
- Best for factual content (people, places, concepts)
- Less effective for purely procedural documentation

## Tips for Better KG Queries

1. **Use Specific Names**: "Einstein" > "physicist"
2. **Include Context**: "Python programming" > "Python"
3. **Relationship Keywords**: "influenced by", "part of", "related to"
4. **Combine Entities**: "REST API authentication" finds their relationship

## Integration with Other Tools

| Tool | Purpose | When to Use After KG |
|------|---------|---------------------|
| `r2r_search` | Get detailed content | After finding entities |
| `r2r_rag` | Comprehensive answer | After mapping relationships |
| `Read` | Read specific docs | After identifying relevant files |
| `Grep` | Find mentions in code | After identifying tech entities |

## Example Queries

**Good KG Queries:**
- "Who are the authors mentioned in ML papers?"
- "Technologies used with Docker"
- "Relationships between microservices"
- "Influences on system design"

**Poor KG Queries (use r2r_search instead):**
- "How to install Docker" (procedural, not entity-based)
- "Best practices" (conceptual, not entity relationships)
- "Step by step guide" (procedural content)

## Troubleshooting

**No Results?**
- Documents may not be KG-processed yet
- Try semantic search instead (`r2r_search`)
- Rephrase query with entity names
- Check `r2r_list_documents` for KG status

**Too Many Results?**
- Use `local` search for specific entities
- Add more context to query
- Filter by document type

**Wrong Entities?**
- Be more specific in query
- Include domain context
- Try different phrasing
