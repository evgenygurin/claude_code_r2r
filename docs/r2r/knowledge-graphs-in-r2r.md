## Knowledge Graphs in R2R

Knowledge graphs enhance search accuracy and context understanding by extracting and connecting information from your documents. R2R uses a two-level architecture:

1. **Document Level**: Entities and relationships are first extracted and stored with their source documents.
2. **Collection Level**: Collections act as soft containers that include documents and maintain corresponding graphs.

### Overview

R2R supports robust knowledge graph functionality to enhance document understanding and retrieval. By extracting entities and relationships from documents and organizing them into collections, R2R enables advanced graph-based analysis and search capabilities.

**Note**: Refer to the [Knowledge Graph Cookbook](https://r2r-docs.sciphi.ai/cookbooks/knowledge-graphs) and [GraphRAG Cookbook](https://r2r-docs.sciphi.ai/cookbooks/graphrag) for detailed guides.

### System Architecture

```
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

### Getting Started

#### Document-Level Extraction

Extract entities and relationships from documents.

**Python Example:**

```python
from r2r import R2RClient

client = R2RClient("http://localhost:7272")

# Extract entities and relationships
document_id = "your-document-id"
extract_response = client.documents.extract(document_id)

# View extracted knowledge
entities = client.documents.list_entities(document_id)
relationships = client.documents.list_relationships(document_id)
```

#### Creating Collection Graphs

Each collection maintains its own graph.

**Python Example:**

```python
# Create collection
collection = client.collections.create(
    "Research Papers",
    "ML research papers with knowledge graph analysis"
)
collection_id = collection["results"]["id"]

# Add documents to collection
client.collections.add_document(collection_id, document_id)

# Generate description for the collection
client.collections.update(
    collection_id,
    generate_description=True
)

# Pull document knowledge into collection graph
client.graphs.pull(collection_id)
```

#### Managing Collection Graphs

**Python Example:**

```python
# List entities in collection graph
entities = client.graphs.list_entities(collection_id)

# List relationships in collection graph
relationships = client.graphs.list_relationships(collection_id)
```

**Example Output:**

- **Entity:**
  ```json
  {
    "name": "DEEP_LEARNING",
    "description": "A subset of machine learning using neural networks",
    "category": "CONCEPT",
    "id": "ce46e955-ed77-4c17-8169-e878baf3fbb9"
  }
  ```
- **Relationship:**
  ```json
  {
    "subject": "DEEP_LEARNING",
    "predicate": "IS_SUBSET_OF",
    "object": "MACHINE_LEARNING",
    "description": "Deep learning is a specialized branch of machine learning"
  }
  ```

### Graph-Collection Relationship

- Each collection has an associated graph.
- The `pull` operation syncs the graph with the collection.
- Allows experimental modifications without affecting the base data.

### Knowledge Graph Workflow

1. **Extract Document Knowledge**:
   ```bash
   curl -X POST http://localhost:7272/v3/documents/${document_id}/extract
   ```
2. **Initialize and Populate Graph**:
   ```bash
   curl -X POST http://localhost:7272/v3/graphs/${collection_id}/pull
   ```
3. **View Entities and Relationships**:
   ```bash
   curl -X GET http://localhost:7272/v3/graphs/${collection_id}/entities
   curl -X GET http://localhost:7272/v3/graphs/${collection_id}/relationships
   ```
4. **Build Graph Communities**:
   ```bash
   curl -X POST http://localhost:7272/v3/graphs/${collection_id}/communities/build
   curl -X GET http://localhost:7272/v3/graphs/${collection_id}/communities
   ```
5. **KG-Enhanced Search**:
   ```bash
   curl -X POST http://localhost:7272/v3/retrieval/search \
    -H "Content-Type: application/json" \
    -d '{
      "query": "who was aristotle?",
      "graph_search_settings": {
        "use_graph_search": true,
        "kg_search_type": "local"
      }
    }'
   ```
6. **Reset Graph**:
   ```bash
   curl -X POST http://localhost:7272/v3/graphs/${collection_id}/reset
   ```

### Graph Synchronization

#### Document Updates

When documents change:

```python
# Update document
client.documents.update(document_id, new_content)

# Re-extract knowledge
client.documents.extract(document_id)

# Update collection graphs
client.graphs.pull(collection_id)
```

#### Cross-Collection Updates

Documents can belong to multiple collections:

```python
# Add document to multiple collections
client.collections.add_document(document_id, collection_id_1)
client.collections.add_document(document_id, collection_id_2)

# Update all relevant graphs
client.graphs.pull(collection_id_1)
client.graphs.pull(collection_id_2)
```

### Access Control

Manage access to graphs through collection permissions.

**Python Example:**

```python
# Give user access to collection and its graph
client.collections.add_user(user_id, collection_id)

# Remove access
client.collections.remove_user(user_id, collection_id)

# List users with access
users = client.collections.list_users(collection_id)
```

### Using Knowledge Graphs

#### Search Integration

Graphs automatically enhance search for collection members.

**Curl Example:**

```bash
curl -X POST http://localhost:7272/v3/retrieval/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is deep learning?",
    "graph_search_settings": {
      "use_graph_search": true,
      "kg_search_type": "local"
    }
  }'
```

#### RAG Integration

Knowledge graphs enhance RAG responses.

**Python Example:**

```python
response = client.retrieval.rag(
    "Explain deep learning's relationship to ML",
    graph_search_settings={
        "enabled": True
    }
)
```

### Best Practices

#### Document Management

- Extract knowledge after document updates.
- Monitor extraction quality at the document level.
- Extractions stay with source documents.
- Consider document size and complexity when extracting.

#### Collection Management

- Keep collections focused on related documents.
- Use meaningful collection names and descriptions.
- Documents can belong to multiple collections.
- Pull changes when document extractions update.

#### Performance Optimization

- Start with small document sets to test extraction.
- Use collection-level operations for bulk processing.
- Monitor graph size and complexity.
- Consider using [orchestration](https://r2r-docs.sciphi.ai/cookbooks/orchestration) for large collections.

#### Access Control

- Plan collection structure around sharing needs.
- Review access permissions regularly.
- Document collection purposes and access patterns.
- Use collection metadata to track graph usage.

### Troubleshooting

**Common Issues and Solutions:**

1. **Missing Extractions**:
   - Verify document extraction completed successfully.
   - Check document format and content.
   - Ensure collection graph was pulled after extraction.

2. **Graph Sync Issues**:
   - Confirm all documents are properly extracted.
   - Check collection membership.
   - Try resetting and re-pulling collection graph.

3. **Performance Problems**:
   - Monitor collection size.
   - Check extraction batch sizes.
   - Consider splitting large collections.
   - Use pagination for large result sets.

### Conclusion

R2R’s knowledge graph capabilities enhance document understanding and improve search and RAG operations by providing structured and interconnected information from your documents.

### Next Steps

- Explore [GraphRAG](https://r2r-docs.sciphi.ai/cookbooks/graphrag) for advanced features.
- Learn about [hybrid search](https://r2r-docs.sciphi.ai/cookbooks/hybrid-search) integration.
- Discover more about [collections](https://r2r-docs.sciphi.ai/cookbooks/collections).
- Set up [orchestration](https://r2r-docs.sciphi.ai/cookbooks/orchestration) for large-scale processing.

---