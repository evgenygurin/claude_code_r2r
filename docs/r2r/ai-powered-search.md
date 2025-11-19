## AI Powered Search

R2R supports advanced search capabilities, including vector search, hybrid search (keyword + vector), and knowledge graph-enhanced search. This section covers the understanding of search modes, configuration, and best practices.

### Introduction

R2R’s hybrid search blends keyword-based full-text search with semantic vector search, delivering results that are both contextually relevant and precise. This unified approach excels at handling complex queries where both exact terms and overall meaning matter.

### Understanding Search Modes

R2R supports multiple search modes to simplify or customize your search configuration:

| Mode      | Description                                                                                                          |
|-----------|----------------------------------------------------------------------------------------------------------------------|
| `basic`   | Primarily semantic search. Suitable for straightforward scenarios where semantic understanding is key.              |
| `advanced`| Combines semantic and full-text search by default, enabling hybrid search with well-tuned default parameters.         |
| `custom`  | Allows full control over search settings, including toggling semantic and full-text search independently.            |

- **`advanced` Mode**: Automatically configures hybrid search with balanced parameters.
- **`custom` Mode**: Manually set `use_hybrid_search=True` or enable both `use_semantic_search` and `use_fulltext_search` for a hybrid setup.

### How R2R Hybrid Search Works

1. **Full-Text Search**:
   - Utilizes Postgres’s `ts_rank_cd` and `websearch_to_tsquery` for exact term matches.

2. **Semantic Search**:
   - Employs vector embeddings to locate contextually related documents, even without exact keyword matches.

3. **Reciprocal Rank Fusion (RRF)**:
   - Merges results from both full-text and semantic searches using a formula to ensure balanced ranking.

4. **Result Ranking**:
   - Orders results based on the combined RRF score, providing balanced and meaningful search outcomes.

### Vector Search

Vector search leverages semantic embeddings to find documents that are contextually similar to the query, even if they don't contain the exact keywords.

**Example:**

```bash
curl -X POST http://localhost:7272/v3/retrieval/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What was Uber'\''s profit in 2020?",
    "search_settings": {
      "use_semantic_search": true,
      "search_settings": {
        "chunk_settings": {
          "index_measure": "l2_distance",
          "limit": 10
        }
      }
    }
  }'
```

**Sample Output:**

Includes chunk-based results with text, metadata, etc.

### Hybrid Search

Hybrid search combines keyword-based full-text search with semantic vector search to deliver more relevant results.

**Example:**

```bash
curl -X POST http://localhost:7272/v3/retrieval/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What was Uber'\''s profit in 2020?",
    "search_settings": {
      "use_hybrid_search": true,
      "hybrid_settings": {
        "full_text_weight": 1.0,
        "semantic_weight": 5.0,
        "full_text_limit": 200,
        "rrf_k": 50
      },
      "filters": {
        "title": {
          "$in": ["lyft_2021.pdf", "uber_2021.pdf"]
        }
      },
      "limit": 10,
      "chunk_settings": {
        "index_measure": "l2_distance",
        "probes": 25,
        "ef_search": 100
      }
    }
  }'
```

### Knowledge Graph Search

Knowledge graph search enhances retrieval by leveraging relationships and entities extracted from documents.

**Example:**

```bash
curl -X POST http://localhost:7272/v3/retrieval/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Who was Aristotle?",
    "graph_search_settings": {
      "use_graph_search": true,
      "kg_search_type": "local"
    }
  }'
```

### Reciprocal Rank Fusion (RRF)

RRF is a technique used to merge results from different search strategies, ensuring balanced and relevant ranking.

### Result Ranking

Results are ranked based on the combined RRF score, providing a balanced mix of exact term matches and semantic relevance.

### Configuration

**Choosing a Search Mode:**

| Mode      | Description                                               | Example Configuration                                                 |
|-----------|-----------------------------------------------------------|-----------------------------------------------------------------------|
| `basic`   | Semantic-only search                                      | `search_mode = "basic"`                                                |
| `advanced`| Hybrid search with well-tuned defaults                    | `search_mode = "advanced"`                                             |
| `custom`  | Manually configure hybrid search settings                 | ```python<br>search_mode = "custom"<br>search_settings = {<br> "use_semantic_search": True,<br> "use_fulltext_search": True,<br> "hybrid_settings": {<br> "full_text_weight": 1.0,<br> "semantic_weight": 5.0,<br> "full_text_limit": 200,<br> "rrf_k": 50<br> }<br> }``` |

For detailed runtime configuration and combining `search_mode` with custom `search_settings`, refer to the [Search API Documentation](https://r2r-docs.sciphi.ai/api-and-sdks/retrieval/search-app).

### Best Practices

1. **Optimize Database and Embeddings**:
   - Ensure Postgres indexing and vector store configurations are optimized for performance.

2. **Adjust Weights and Limits**:
   - Tweak `full_text_weight`, `semantic_weight`, and `rrf_k` values in `custom` mode.

3. **Regular Updates**:
   - Keep embeddings and indexes up-to-date to maintain search quality.

4. **Choose Appropriate Embeddings**:
   - Select an embedding model that fits your content domain for the best semantic results.

### Conclusion

R2R’s hybrid search delivers robust, context-aware retrieval by merging semantic and keyword-driven approaches. Whether you choose `basic` mode for simplicity, `advanced` mode for out-of-the-box hybrid search, or `custom` mode for granular control, R2R ensures you can tailor the search experience to your unique needs.

---