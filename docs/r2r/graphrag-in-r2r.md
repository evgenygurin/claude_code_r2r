## GraphRAG in R2R

GraphRAG extends traditional RAG by leveraging community detection and summarization within knowledge graphs. This approach provides richer context and more comprehensive answers by understanding how information is clustered and connected across your documents.

### Overview

GraphRAG enhances RAG by integrating community detection and summarization within knowledge graphs, enabling more contextual and clustered information retrieval.

#### Architecture

```
User Query
    |
QueryTransformPipe
    |
MultiSearchPipe
    |
VectorSearchPipe
    |
RAG-Fusion Process
    |
Reciprocal Rank Fusion
    |
RAG Generation
    |
Knowledge Graph DB
```

### Understanding Communities

**Communities** are automatically detected clusters of related information in your knowledge graph, providing:

1. **Higher-Level Understanding**: Grasp document themes.
2. **Summarized Context**: Concise summaries for related concepts.
3. **Improved Retrieval**: Topic-based organization enhances search relevance.

**Example Communities:**

| Domain           | Community Examples                                     |
|------------------|--------------------------------------------------------|
| Scientific Papers| Research methods, theories, research teams             |
| News Articles    | World events, industry sectors, key figures           |
| Technical Docs   | System components, APIs, user workflows                |
| Legal Documents  | Case types, jurisdictions, legal principles            |

### Implementation Guide

#### Prerequisites

Ensure you have:

- Documents ingested into a collection.
- Entities and relationships extracted.
- Graph synchronized.

**Python Example:**

```python
from r2r import R2RClient

client = R2RClient("http://localhost:7272")

# Setup collection and extract knowledge
collection_id = "your-collection-id"
client.collections.extract(collection_id)
client.graphs.pull(collection_id)
```

#### Building Communities

**Python Example:**

```python
# Generate a description for the collection
client.collections.update(
    collection_id,
    generate_description=True
)

# Build communities for your collection's graph
build_response = client.graphs.build(collection_id)
```

**Build Process Includes:**

1. Analyzes graph connectivity.
2. Identifies dense subgraphs.
3. Generates community summaries.
4. Creates findings and insights.

#### Using GraphRAG

Once communities are built, they integrate into search and RAG.

**Python Example:**

```python
# Search across all levels
search_response = client.retrieval.search(
    "What are the key theories?",
    search_settings={
        "graph_settings": {
            "enabled": True,
        }
    }
)

# RAG with community context
rag_response = client.retrieval.rag(
    "Explain the relationships between theories",
    graph_search_settings={
        "enabled": True
    }
)
```

### Understanding Results

GraphRAG returns three types of results:

#### 1. Document Chunks

```json
{
  "chunk_id": "70c96e8f-e5d3-5912-b79b-13c5793f17b5",
  "text": "Example document text...",
  "score": 0.78,
  "metadata": {
    "document_type": "txt",
    "associated_query": "query text"
  }
}
```

#### 2. Graph Elements

```json
{
  "content": {
    "name": "CONCEPT_NAME",
    "description": "Entity description..."
  },
  "result_type": "entity",
  "score": 0.74
}
```

#### 3. Communities

```json
{
  "content": {
    "name": "Community Name",
    "summary": "High-level community description...",
    "findings": [
      "Key insight 1 with supporting evidence...",
      "Key insight 2 with supporting evidence..."
    ],
    "rating": 9.0,
    "rating_explanation": "Explanation of importance..."
  },
  "result_type": "community",
  "score": 0.57
}
```

### Scaling GraphRAG

#### Using Orchestration

For large collections, utilize R2R’s orchestration capabilities via Hatchet UI.

**Access Hatchet UI:**

- **URL**: [http://localhost:7274](http://localhost:7274)
- **Login Credentials**:
  - **Email**: admin@example.com
  - **Password**: Admin123!!

**Features:**

- Monitor document extraction progress.
- Track community detection status.
- Handle errors and workflow retries.

**Example Diagram:**

![Monitoring GraphRAG workflows in Hatchet](https://files.buildwithfern.com/https://sciphi.docs.buildwithfern.com/2024-12-13T18:29:49.890Z/images/hatchet_workflow.png)

### Best Practices

1. **Development**:
   - Start with small document sets.
   - Test with single documents first.
   - Scale gradually to larger collections.

2. **Performance**:
   - Monitor community size and complexity.
   - Use pagination for large result sets.
   - Consider breaking very large collections.

3. **Quality**:
   - Review community summaries.
   - Validate findings accuracy.
   - Monitor retrieval relevance.

### Troubleshooting

**Common Issues and Solutions:**

1. **Poor Community Quality**:
   - Check entity extraction quality.
   - Review relationship connections.
   - Adjust collection scope.

2. **Performance Issues**:
   - Monitor graph size.
   - Check community complexity.
   - Use orchestration for large graphs.

3. **Integration Problems**:
   - Verify extraction completion.
   - Check collection synchronization.
   - Review API configurations.

### Next Steps

- Explore [hybrid search](https://r2r-docs.sciphi.ai/cookbooks/hybrid-search) integration.
- Learn about [collection management](https://r2r-docs.sciphi.ai/cookbooks/collections).
- Discover more about [observability](https://r2r-docs.sciphi.ai/cookbooks/observability).

### Conclusion

GraphRAG enhances R2R’s RAG capabilities by integrating community detection and summarization within knowledge graphs. This results in richer, more contextualized responses, improving the overall quality of information retrieval and generation.

---