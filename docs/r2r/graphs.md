## Graphs

### Graphs

R2R supports robust knowledge graph functionality to enhance document understanding and retrieval. By extracting entities and relationships from documents and organizing them into collections, R2R enables advanced graph-based analysis and search capabilities.

**Note**: Refer to the [Knowledge Graph Cookbook](https://r2r-docs.sciphi.ai/cookbooks/knowledge-graphs) and [GraphRAG Cookbook](https://r2r-docs.sciphi.ai/cookbooks/graphrag) for detailed guides.

### Knowledge Graph Operations

#### Entity Management

- **Add Entities**: Add new entities to the knowledge graph.
- **Update Entities**: Modify existing entities.
- **Retrieve Entities**: Fetch entities based on criteria.

#### Relationship Management

- **Create Relationships**: Define relationships between entities.
- **Query Relationships**: Fetch relationships based on criteria.

#### Batch Import

Efficiently import large amounts of data using batched operations.

#### Vector Search

Perform similarity searches on entity embeddings to find related entities.

#### Community Detection

Identify and manage communities within the graph to understand clusters of related information.

### Customization

Customize knowledge graph extraction and search processes by modifying `kg_triples_extraction_prompt` and adjusting model configurations in `kg_extraction_settings` and `graph_settings`.

### Conclusion

R2R’s knowledge graph capabilities enhance document understanding and improve search and RAG operations by providing structured and interconnected information from your documents.

# HTTP API of R2R Library

Welcome to the **R2R (Retrieve to Retrieve) API** documentation. This guide provides an exhaustive overview of all available API endpoints, organized into logical sections with detailed descriptions, request and response schemas, error codes, and usage examples. Whether you're integrating R2R into your application or developing workflows around it, this documentation will serve as your essential reference.

---