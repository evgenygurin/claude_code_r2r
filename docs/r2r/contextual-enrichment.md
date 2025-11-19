## Contextual Enrichment

Enhance your RAG system chunks with rich contextual information to address the challenge of context loss in individual chunks.

### The Challenge of Context Loss

During ingestion, large documents are broken down into smaller chunks for efficient processing. However, isolated chunks may lack broader context, leading to incomplete or unclear responses.

**Example:**

Using Lyft’s 2021 annual report:

- **Original Chunk:**
  ```
  storing unrented and returned vehicles. These impacts to the demand for and operations of the different rental programs have and may continue to adversely affect our business, financial condition and results of operation.
  ```

- **Questions Raised:**
  - What specific impacts are being discussed?
  - Which rental programs are affected?
  - What’s the broader context of these business challenges?

### Introducing Contextual Enrichment

Contextual enrichment enhances chunks with relevant information from surrounding or semantically related content, giving each chunk a “memory” of related information.

### Enabling Enrichment

Configure your `r2r.toml` file with the following settings:

```toml
[ingestion.chunk_enrichment_settings]
enable_chunk_enrichment = true  # disabled by default
strategies = ["semantic", "neighborhood"]
forward_chunks = 3  # Look ahead 3 chunks
backward_chunks = 3  # Look behind 3 chunks
semantic_neighbors = 10  # Find 10 semantically similar chunks
semantic_similarity_threshold = 0.7  # Minimum similarity score
generation_config = { model = "openai/gpt-4.1-mini" }
```

### Enrichment Strategies Explained

R2R implements two strategies for chunk enrichment:

#### 1. Neighborhood Strategy

- **Forward Looking**: Captures upcoming context (default: 3 chunks).
- **Backward Looking**: Incorporates previous context (default: 3 chunks).
- **Use Case**: Effective for narrative documents with linear context flow.

#### 2. Semantic Strategy

- **Vector Similarity**: Identifies chunks with similar meanings regardless of location.
- **Configurable Neighbors**: Customizable number of similar chunks.
- **Similarity Threshold**: Ensures relevance by setting minimum similarity scores.
- **Use Case**: Ideal for documents with recurring themes across sections.

### The Enrichment Process

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
4. Ensure the enriched chunk remains independent and self-contained.
5. Maintain original scope without bleeding information.
6. Focus on precision and informativeness.
7. Preserve original meaning while improving clarity.
8. Output only the enriched chunk.

**Enriched Chunk:**

```
[Enriched Chunk Output]
```

### Implementation and Results

To process documents with enrichment:

```bash
r2r documents create --file_path path/to/lyft_2021.pdf
```

#### Viewing Enriched Results

Access enriched chunks through the API:

```bash
curl -X GET http://localhost:7272/v3/document/{document_id}/chunks
```

**Before Enrichment:**

```
storing unrented and returned vehicles. These impacts to the demand for and operations of the different rental programs have and may continue to adversely affect our business, financial condition and results of operation.
```

**After Enrichment:**

```
The impacts of the COVID-19 pandemic on the demand for and operations of the various vehicle rental programs, including Lyft Rentals and the Express Drive program, have resulted in challenges regarding the storage of unrented and returned vehicles. These adverse conditions are anticipated to continue affecting Lyft's overall business performance, financial condition, and operational results.
```

**Enhancements in Enriched Chunk:**

- Specifies the cause (COVID-19 pandemic).
- Names specific programs (Lyft Rentals, Express Drive).
- Provides clearer context about the business impact.
- Maintains professional, third-person tone.

### Metadata and Storage

R2R maintains both enriched and original versions:

```json
{
  "results": [
    {
      "text": "enriched_version",
      "metadata": {
        "original_text": "original_version",
        "chunk_enrichment_status": "success"
        // ... additional metadata ...
      }
    }
  ]
}
```

This dual storage ensures transparency and allows for version comparison when needed.

### Best Practices

1. **Tune Your Parameters**: Adjust `forward_chunks`, `backward_chunks`, and `semantic_neighbors` based on document structure.
2. **Monitor Enrichment Quality**: Regularly review enriched chunks to ensure accuracy.
3. **Consider Document Type**: Different documents may benefit from different enrichment strategies.
4. **Balance Context Size**: More context isn’t always better; find the optimal size for your use case.

---