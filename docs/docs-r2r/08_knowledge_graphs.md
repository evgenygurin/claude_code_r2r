# Knowledge Graphs in R2R

Knowledge graphs enhance search accuracy and context understanding by extracting and connecting information from your documents. R2R uses a two-level architecture:

1. **Document Level**: Entities and relationships are first extracted and stored with their source documents.
2. **Collection Level**: Collections act as soft containers that include documents and maintain corresponding graphs.

## Overview

R2R supports robust knowledge graph functionality to enhance document understanding and retrieval. By extracting entities and relationships from documents and organizing them into collections, R2R enables advanced graph-based analysis and search capabilities.

**Note**: Refer to the [Knowledge Graph Cookbook](https://r2r-docs.sciphi.ai/cookbooks/knowledge-graphs) and [GraphRAG Cookbook](https://r2r-docs.sciphi.ai/cookbooks/graphrag) for detailed guides.

## System Architecture

```bash
Collection (Soft Container)
    |
Documents
    |--> Extracted Entities & Relationships
Knowledge Graph
    |
Permissions
    |
User
```

**Collections Provide:**

- Flexible document organization (documents can belong to multiple collections)
- Access control and sharing
- Graph synchronization and updates

## Getting Started

### Document-Level Extraction

Extract entities and relationships from documents.

#### Python Example

```python
from r2r import R2RClient

client = R2RClient("http://localhost:7272")

# Extract entities and relationships
document_id = "your-document-id"
extract_response = client.documents.extract(document_id)
```

### Creating Collection Graphs

Create and manage collection-level knowledge graphs.

#### Python Example

```python
# Create a collection
collection_response = client.collections.create(
    name="shakespeare_works",
    description="Collection of Shakespeare's works"
)

# Add documents to collection
client.collections.add_document(
    collection_id=collection_response["collection_id"],
    document_id="hamlet_id"
)
```

### Managing Collection Graphs

Manage and query collection-level knowledge graphs.

#### Python Example

```python
# Get collection graph
graph = client.collections.get_graph(collection_id="your_collection_id")

# Query the graph
results = client.collections.query_graph(
    collection_id="your_collection_id",
    query="MATCH (p:Person)-[:WROTE]->(w:Work) RETURN p, w"
)
```

#### Example Output

```json
{
  "nodes": [...],
  "relationships": [...],
  "metadata": {
    "node_count": 42,
    "relationship_count": 67
  }
}
```

## Graph-Collection Relationship

Collections serve as logical containers for documents and their associated knowledge graphs. This relationship enables:

- Flexible organization of related documents
- Shared knowledge context
- Access control at the collection level
- Graph synchronization across documents

## Knowledge Graph Workflow

### Step 1: Extract Document Knowledge

Extract entities and relationships from individual documents.

### Step 2: Initialize and Populate Graph

Create and populate collection-level graphs.

### Step 3: View Entities and Relationships

Explore the extracted knowledge graph.

### Step 4: Build Graph Communities

Identify and analyze graph communities.

### Step 5: KG-Enhanced Search

Use the knowledge graph to enhance search results.

### Step 6: Reset Graph

Reset or update the graph as needed.

## Graph Synchronization

### Document Updates

Automatically synchronize graphs when documents are updated.

### Cross-Collection Updates

Manage updates across multiple collections.

## Access Control

Manage access to knowledge graphs through collection permissions.

### Python Example

```python
# Set collection permissions
client.collections.set_permissions(
    collection_id="your_collection_id",
    user_id="user_id",
    permissions=["read", "write"]
)
```

## Using Knowledge Graphs

### Search Integration

Enhance search results with knowledge graph data.

#### Curl Example

```bash
curl -X POST http://localhost:7272/v3/retrieval/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Who wrote Hamlet?",
    "graph_search_settings": {
      "use_graph_search": true
    }
  }'
```

### RAG Integration

Use knowledge graphs to enhance RAG responses.

#### Python Example

```python
rag_response = client.retrieval.rag(
    query="What are the relationships between characters in Hamlet?",
    search_settings={
        "use_graph_search": true,
        "graph_search_settings": {
            "kg_search_type": "local"
        }
    }
)
```

## Best Practices

### Document Management

- Keep documents organized in logical collections
- Maintain clear document metadata

### Collection Management

- Create focused collections
- Use meaningful collection names and descriptions

### Performance Optimization

- Monitor graph size and complexity
- Use appropriate indexing strategies

### Access Control

- Implement proper permission settings
- Regularly audit access controls

## Troubleshooting

Common issues and solutions for knowledge graph management.

## Conclusion

Knowledge graphs in R2R provide powerful capabilities for understanding and connecting information across documents. By properly managing collections and their associated graphs, you can enhance search accuracy and provide more contextual responses in your applications.

## Next Steps

1. Explore the [Knowledge Graph Cookbook](https://r2r-docs.sciphi.ai/cookbooks/knowledge-graphs)
2. Try the [GraphRAG Cookbook](https://r2r-docs.sciphi.ai/cookbooks/graphrag)
3. Experiment with different graph queries and search configurations
