# Contextual Enrichment

Enhance your RAG system chunks with rich contextual information to address the challenge of context loss in individual chunks.

## The Challenge of Context Loss

During ingestion, large documents are broken down into smaller chunks for efficient processing. However, isolated chunks may lack broader context, leading to incomplete or unclear responses.

**Example:**

Using Lyft's 2021 annual report:

- **Original Chunk:**

  ```
  storing unrented and returned vehicles. These impacts to the demand for and operations of the different rental programs have and may continue to adversely affect our business, financial condition and results of operation.
  ```

- **Questions Raised:**
  - What specific impacts are being discussed?
  - Which rental programs are affected?
  - What's the broader context of these business challenges?

## Introducing Contextual Enrichment

Contextual enrichment enhances chunks with relevant information from surrounding or semantically related content, giving each chunk a "memory" of related information.

## Enabling Enrichment

Configure your `r2r.toml` file with the following settings:

```toml
[ingestion.chunk_enrichment_settings]
enable_chunk_enrichment = true  # disabled by default
strategies = ["semantic", "neighborhood"]
forward_chunks = 3  # Look ahead 3 chunks
backward_chunks = 3  # Look behind 3 chunks
semantic_neighbors = 10  # Find 10 semantically similar chunks
semantic_similarity_threshold = 0.7  # Minimum similarity score
generation_config = { model = "openai/gpt-4o-mini" }
```

## Enrichment Strategies Explained

R2R implements two strategies for chunk enrichment:

### Neighborhood Strategy

- **Forward Looking**: Captures upcoming context (default: 3 chunks).
- **Backward Looking**: Incorporates previous context (default: 3 chunks).
- **Use Case**: Effective for narrative documents with linear context flow.

### Semantic Strategy

- **Vector Similarity**: Identifies chunks with similar meanings regardless of location.
- **Configurable Neighbors**: Customizable number of similar chunks.
- **Similarity Threshold**: Ensures relevance by setting minimum similarity scores.
- **Use Case**: Ideal for documents with recurring themes across sections.

## The Enrichment Process

R2R uses a prompt to guide the Language Model (LLM) during enrichment:

**Task:**

Enrich and refine the given chunk of text using information from the provided context chunks. The goal is to make the chunk more precise and self-contained.

**Context Chunks:**

```
{context_chunks}
```

**Chunk to Enrich:**

```
{chunk}
```

**Instructions:**

1. Rewrite the chunk in third person.
2. Replace all common nouns with appropriate proper nouns.
3. Use information from the context chunks to enhance clarity.

## Implementation and Results

The enrichment process happens during document ingestion when enabled in the configuration.

### Viewing Enriched Results

You can view the enriched chunks through the R2R API or SDK:

```python
# Get enriched chunks for a document
response = client.documents.get_chunks(document_id="your_doc_id")
for chunk in response["chunks"]:
    print(f"Original: {chunk['text']}")
    print(f"Enriched: {chunk['enriched_text']}")
```

## Metadata and Storage

Enriched chunks are stored alongside original chunks with additional metadata:

- Original text
- Enriched text
- Enrichment strategy used
- Context sources
- Timestamp of enrichment

## Best Practices

1. Enable enrichment for documents where context is crucial
2. Adjust neighborhood and semantic parameters based on document structure
3. Monitor enrichment quality and adjust thresholds as needed
4. Use appropriate LLM models for enrichment
5. Consider storage implications of enriched chunks

## Conclusion

Contextual enrichment significantly improves the quality of RAG responses by providing richer context to each chunk. By combining neighborhood and semantic strategies, R2R ensures that chunks maintain their contextual relevance while remaining efficient for retrieval and generation tasks.
