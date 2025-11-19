# Data Ingestion

## Introduction

R2R provides a powerful and flexible ingestion pipeline to process and manage various types of documents. It supports a wide range of file formats—text, documents, PDFs, images, audio, and video—and transforms them into searchable, analyzable content. The ingestion process includes parsing, chunking, embedding, and optionally extracting entities and relationships for knowledge graph construction.

## Ingestion Modes

R2R supports different ingestion modes to balance between speed and quality:

- `fast`: Speed-oriented ingestion.
- `hi-res`: Comprehensive, high-quality ingestion.
- `custom`: Fine-grained control with a full `ingestion_config` dictionary.

## Ingesting Documents

The ingestion process can be configured through the `r2r.toml` file:

```toml
[ingestion]
provider = "r2r"
chunking_strategy = "recursive"
chunk_size = 1024
chunk_overlap = 512
excluded_parsers = ["mp4"]

[ingestion.chunk_enrichment_settings]
enable_chunk_enrichment = true
strategies = ["semantic", "neighborhood"]
forward_chunks = 3
backward_chunks = 3
semantic_neighbors = 10
semantic_similarity_threshold = 0.7
generation_config = { model = "openai/gpt-4o-mini" }
```

### Example Response

```python
response = client.documents.create(
    file_path="document.pdf",
    ingestion_mode="hi-res"
)
print(response)
```

## Ingesting Pre-Processed Chunks

For cases where you want to handle the chunking yourself, R2R supports ingesting pre-processed chunks.

### Example

```python
chunks = [
    {"text": "First chunk of content", "metadata": {"page": 1}},
    {"text": "Second chunk of content", "metadata": {"page": 1}},
]

response = client.documents.create_from_chunks(
    chunks=chunks,
    document_id="custom_doc_id",
    metadata={"source": "manual_chunks"}
)
```

## Deleting Documents and Chunks

R2R provides methods to manage your ingested content.

### Delete a Document

```python
response = client.documents.delete(document_id="doc_123")
```

### Sample Output

```json
{
    "status": "success",
    "message": "Document deleted successfully",
    "document_id": "doc_123"
}
```

### Key Features of Deletion
- Cascading deletion of associated chunks
- Cleanup of vector embeddings
- Removal from knowledge graphs
- Automatic collection updates

## Additional Configuration & Concepts

### Light vs. Full Deployments

- **Light**: Basic document processing without advanced features
- **Full**: Complete feature set including knowledge graphs and enrichment

### Provider Configuration

The ingestion provider can be configured with additional settings:

```toml
[ingestion]
provider = "r2r"
chunking_strategy = "recursive"
chunk_size = 1024
chunk_overlap = 512
excluded_parsers = ["mp4"]
```

## Conclusion

R2R's ingestion system is designed to be flexible and powerful, handling various document types and processing needs. Whether you need quick processing or detailed analysis, the system can be configured to meet your requirements. 