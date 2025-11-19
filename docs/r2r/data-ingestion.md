## Data Ingestion

### Introduction

R2R provides a powerful and flexible ingestion pipeline to process and manage various types of documents. It supports a wide range of file formats—text, documents, PDFs, images, audio, and video—and transforms them into searchable, analyzable content. The ingestion process includes parsing, chunking, embedding, and optionally extracting entities and relationships for knowledge graph construction.

This section will guide you through:

- Ingesting files, raw text, or pre-processed chunks
- Choosing an ingestion mode (`fast`, `hi-res`, or `custom`)
- Updating and deleting documents and chunks

For more on configuring ingestion, see the [Ingestion Configuration Overview](https://r2r-docs.sciphi.ai/documentation/configuration/ingestion) and [Parsing & Chunking](https://r2r-docs.sciphi.ai/documentation/configuration/ingestion/parsing_and_chunking).

### Ingestion Modes

R2R offers three primary ingestion modes to tailor the process to your requirements:

| Mode    | Description                                                                                                          |
|---------|----------------------------------------------------------------------------------------------------------------------|
| `fast`  | Speed-oriented ingestion that prioritizes rapid processing with minimal enrichment. Ideal for quickly processing large volumes of documents. |
| `hi-res`| Comprehensive, high-quality ingestion that may leverage multimodal foundation models for parsing complex documents and PDFs. Suitable for documents requiring detailed analysis. |
| `custom`| Advanced mode offering fine-grained control. Users provide a full `ingestion_config` dict or object to specify parser options, chunking strategy, character limits, and more. |

**Example Usage:**

```python
file_path = 'path/to/file.txt'
metadata = {'key1': 'value1'}

# hi-res mode for thorough extraction
ingest_response = client.documents.create(
    file_path=file_path,
    metadata=metadata,
    ingestion_mode="hi-res"
)

# fast mode for quick processing
ingest_response = client.documents.create(
    file_path=file_path,
    ingestion_mode="fast"
)

# custom mode for full control
ingest_response = client.documents.create(
    file_path=file_path,
    ingestion_mode="custom",
    ingestion_config={
        "provider": "unstructured_local",
        "strategy": "auto",
        "chunking_strategy": "by_title",
        "new_after_n_chars": 256,
        "max_characters": 512,
        "combine_under_n_chars": 64,
        "overlap": 100,
    }
)
```

### Ingesting Documents

A `Document` represents ingested content in R2R. When you ingest a file, text, or chunks:

1. **Parsing**: Converts source files into text.
2. **Chunking**: Breaks text into manageable units.
3. **Embedding**: Generates embeddings for semantic search.
4. **Storing**: Persists chunks and embeddings for retrieval.
5. **Knowledge Graph Integration**: Optionally extracts entities and relationships.

In a **full** R2R installation, ingestion is asynchronous. Monitor ingestion status and confirm when documents are ready:

```bash
r2r documents list
```

**Example Response:**

```json
{
  "id": "9fbe403b-c11c-5aae-8ade-ef22980c3ad1",
  "title": "file.txt",
  "user_id": "2acb499e-8428-543b-bd85-0d9098718220",
  "type": "txt",
  "created_at": "2024-09-05T18:20:47.921933Z",
  "updated_at": "2024-09-05T18:20:47.921938Z",
  "ingestion_status": "success",
  "restructuring_status": "pending",
  "version": "v0",
  "summary": "The document contains a ....",
  "collection_ids": [],
  "metadata": {"version": "v0"}
}
```

An `ingestion_status` of `"success"` confirms the document is fully ingested. Also, check the R2R dashboard at [http://localhost:7273](http://localhost:7273/) for ingestion progress and status.

For more details on creating documents, refer to the [Create Document API](https://r2r-docs.sciphi.ai/api-and-sdks/documents/create-document).

### Ingesting Pre-Processed Chunks

If you have pre-processed chunks from your own pipeline, ingest them directly. Useful if content is already divided into logical segments.

**Example:**

```python
chunks = ["This is my first parsed chunk", "This is my second parsed chunk"]

ingest_response = client.documents.create(
    chunks=chunks,
    ingestion_mode="fast"  # use fast for quick chunk ingestion
)

print(ingest_response)
# {'results': [{'message': 'Document created and ingested successfully.', 'document_id': '7a0dad00-b041-544e-8028-bc9631a0a527'}]}
```

For more on ingesting chunks, see the [Create Chunks API](https://r2r-docs.sciphi.ai/api-and-sdks/chunks/create-chunks).

### Deleting Documents and Chunks

To remove documents or chunks, use their respective `delete` methods.

**Delete a Document:**

```bash
curl -X DELETE http://localhost:7272/v3/documents/9fbe403b-c11c-5aae-8ade-ef22980c3ad1 \
  -H "Content-Type: application/json"
```

**Sample Output:**

```json
{"results": {"success": true}}
```

**Key Features of Deletion:**

1. **Deletion by Document ID**: Remove specific documents.
2. **Cascading Deletion**: Deletes associated chunks and metadata.
3. **Deletion by Filter**: Delete documents based on criteria like text match or user ID using `documents/by-filter`.

This mechanism ensures precise control over document management within R2R.

For advanced document management and user authentication details, refer to the [User Auth Cookbook](https://r2r-docs.sciphi.ai/cookbooks/user-auth).

### Additional Configuration & Concepts

- **Light vs. Full Deployments**:
  - **Light**: Uses R2R’s built-in parser and supports synchronous ingestion.
  - **Full**: Orchestrates ingestion tasks asynchronously and integrates with complex providers like `unstructured_local`.

- **Provider Configuration**:
  - Settings in `r2r.toml` or at runtime (`ingestion_config`) adjust parsing and chunking strategies.
    - `fast` and `hi-res` modes influenced by strategies like `"auto"` or `"hi_res"`.
    - `custom` mode allows overriding chunk size, overlap, excluded parsers, and more at runtime.

For detailed configuration options, see:

- [Data Ingestion Configuration](https://r2r-docs.sciphi.ai/documentation/configuration/ingestion)
- [Parsing & Chunking Configuration](https://r2r-docs.sciphi.ai/documentation/configuration/ingestion/parsing_and_chunking)

### Conclusion

R2R’s ingestion pipeline is flexible and efficient, allowing you to tailor ingestion to your needs:

- Use `fast` for quick processing.
- Use `hi-res` for high-quality, multimodal analysis.
- Use `custom` for advanced, granular control.

Easily ingest documents or pre-processed chunks, update their content, and delete them when no longer needed. Combined with powerful retrieval and knowledge graph capabilities, R2R enables seamless integration of advanced document management into your applications.

---