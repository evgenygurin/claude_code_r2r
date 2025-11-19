## Retrieval-Augmented Generation (RAG)

R2R couples its powerful retrieval capabilities with large language models (LLMs) to provide comprehensive Q&A and content generation based on ingested documents.

### Basic RAG

**Example:**

```bash
curl -X POST http://localhost:7272/v3/retrieval/rag \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What was Uber'\''s profit in 2020?"
  }'
```

**Sample Output:**

```json
{
  "results": [
    "ChatCompletion(...)"
  ]
}
```

### RAG with Hybrid Search

Combine hybrid search logic with RAG for enhanced results.

**Example:**

```bash
curl -X POST http://localhost:7272/v3/retrieval/rag \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Who is Jon Snow?",
    "search_settings": {
      "use_hybrid_search": true,
      "limit": 10
    }
  }'
```

### Streaming RAG

Stream RAG responses in real-time, providing partial results as they are generated.

**Example:**

```bash
r2r retrieval rag --query="who was aristotle" --use-hybrid-search=True --stream
```

It streams real-time tokens.

### Customizing RAG

You can control various aspects of RAG, including search settings, generation config, and LLM providers.

**Example:**

```bash
curl -X POST http://localhost:7272/v3/retrieval/rag \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Who is Jon Snow?",
    "rag_generation_config": {
      "model": "claude-3-haiku-20240307",
      "temperature": 0.7
    }
  }'
```

### Advanced RAG Techniques

R2R supports advanced RAG techniques, currently in beta, including HyDE and RAG-Fusion.

#### HyDE (Hypothetical Document Embeddings)

HyDE enhances retrieval by generating and embedding hypothetical documents based on the query.

**Workflow:**

1. **Query Expansion**: Generates hypothetical answers or documents using an LLM.
2. **Enhanced Embedding**: Embeds these hypothetical documents to create a richer semantic search space.
3. **Similarity Search**: Uses the embeddings to find the most relevant actual documents in the database.
4. **Informed Generation**: Combines retrieved documents and the original query to generate the final response.

**Python Example:**

```python
from r2r import R2RClient

client = R2RClient()

hyde_response = client.retrieval.rag(
    "What are the main themes in Shakespeare's plays?",
    search_settings={
        "search_strategy": "hyde",
        "limit": 10
    }
)

print('hyde_response = ', hyde_response)
```

**Sample Output:**

```json
{
  "results": {
    "completion": "...",
    "search_results": {
      "chunk_search_results": [
        {
          "score": 0.7715058326721191,
          "text": "## Paragraph from the Chapter...",
          "metadata": {
            "associated_query": "The fundamental theorem of calculus..."
          }
        }
      ]
    }
  }
}
```

#### RAG-Fusion

RAG-Fusion improves retrieval quality by combining results from multiple search iterations.

**Workflow:**

1. **Query Expansion**: Generates multiple related queries.
2. **Multiple Retrievals**: Each query retrieves relevant documents.
3. **Reciprocal Rank Fusion (RRF)**: Re-ranks documents using RRF.
4. **Enhanced RAG**: Uses re-ranked documents to generate the final response.

**Python Example:**

```python
from r2r import R2RClient

client = R2RClient()

rag_fusion_response = client.retrieval.rag(
    "Explain the theory of relativity",
    search_settings={
        "search_strategy": "rag_fusion",
        "limit": 20
    }
)

print('rag_fusion_response = ', rag_fusion_response)
```

**Sample Output:**

```json
{
  "results": {
    "completion": "...",
    "search_results": {
      "chunk_search_results": [
        {
          "score": 0.04767399003253049,
          "text": "18. The theory of relativity, proposed by Albert Einstein in 1905...",
          "metadata": {
            "associated_queries": ["What is the theory of relativity?", ...]
          }
        }
      ]
    }
  }
}
```

### Combining with Other Settings

You can combine advanced RAG techniques with other search and RAG settings for enhanced performance.

**Example:**

```python
custom_rag_response = client.retrieval.rag(
    "Describe the impact of climate change on biodiversity",
    search_settings={
        "search_strategy": "hyde",
        "limit": 15,
        "use_hybrid_search": True
    },
    rag_generation_config={
        "model": "anthropic/claude-3-opus-20240229",
        "temperature": 0.7
    }
)
```

### Customization and Server-Side Defaults

While R2R allows runtime configuration of advanced techniques, server-side defaults can also be modified for consistent behavior. This includes updating prompts used for techniques like HyDE and RAG-Fusion.

- **General Configuration**: Refer to the [R2R Configuration Documentation](https://r2r-docs.sciphi.ai/documentation/configuration/overview).
- **Customizing Prompts**: Learn about customizing prompts [here](https://r2r-docs.sciphi.ai/documentation/configuration/retrieval/prompts).

**Example:**

```toml
[rag_generation_config]
model = "anthropic/claude-3-opus-20240229"
temperature = 0.7
```

### Conclusion

By leveraging advanced RAG techniques and customizing their underlying prompts, you can significantly enhance the quality and relevance of your retrieval and generation processes. Experiment with different strategies, settings, and prompt variations to find the optimal configuration for your specific use case. R2R's flexibility allows iterative improvement and adaptation to changing requirements.

---