## Embedding

### Embedding System

R2R uses embeddings as the foundation for semantic search and similarity matching capabilities. The embedding system converts text into high-dimensional vectors that capture semantic meaning, enabling powerful search and retrieval operations.

R2R leverages **LiteLLM** to route embedding requests due to their provider flexibility. Read more about [LiteLLM here](https://docs.litellm.ai/).

### Embedding Configuration

Customize the embedding system through the `embedding` section in your `r2r.toml` file, along with corresponding environment variables for sensitive information.

**Example: `r2r.toml`**

```toml
[embedding]
provider = "litellm"  # defaults to "litellm"
base_model = "openai/text-embedding-3-small"  # defaults to "openai/text-embedding-3-large"
base_dimension = 512  # defaults to 3072
batch_size = 512  # defaults to 128
rerank_model = "BAAI/bge-reranker-v2-m3"  # defaults to None
concurrent_request_limit = 256  # defaults to 256
```

**Environment Variables:**

- `OPENAI_API_KEY`
- `OPENAI_API_BASE`
- `HUGGINGFACE_API_KEY`
- `HUGGINGFACE_API_BASE`
- `ANTHROPIC_API_KEY`
- `COHERE_API_KEY`
- `OLLAMA_API_KEY`
- `BEDROCK_API_KEY`
- `VERTEX_AI_API_KEY`
- `VOYAGE_AI_API_KEY`

### Advanced Embedding Features in R2R

#### Batched Processing

R2R implements intelligent batching for embedding operations to optimize throughput and, in some cases, cost.

**Python Example:**

```python
class EmbeddingProvider:
    async def embed_texts(self, texts: List[str]) -> List[List[float]]:
        batches = [texts[i:i + self.batch_size] for i in range(0, len(texts), self.batch_size)]
        embeddings = []
        for batch in batches:
            batch_embeddings = await self._process_batch(batch)
            embeddings.extend(batch_embeddings)
        return embeddings
```

#### Concurrent Request Management

The system manages requests with rate limiting and concurrency control.

1. **Rate Limiting**: Prevents API throttling through intelligent request scheduling.
2. **Concurrent Processing**: Manages multiple embedding requests efficiently.
3. **Error Handling**: Implements retry logic with exponential backoff.

### Performance Considerations

When configuring embeddings in R2R, consider these optimization strategies:

1. **Batch Size Optimization**:
   - Larger batch sizes improve throughput but increase latency.
   - Consider provider-specific rate limits when setting batch size.
   - Balance memory usage with processing speed.

2. **Concurrent Requests**:
   - Adjust `concurrent_request_limit` based on provider capabilities.
   - Monitor API usage and adjust limits accordingly.
   - Implement local caching for frequently embedded texts.

3. **Model Selection**:
   - Balance embedding dimension size with accuracy requirements.
   - Consider cost per token for different providers.
   - Evaluate multilingual requirements when choosing models.

4. **Resource Management**:
   - Monitor memory usage with large batch sizes.
   - Implement appropriate error handling and retry strategies.
   - Consider implementing local model fallbacks for critical systems.

### Supported LiteLLM Providers

R2R supports multiple LiteLLM providers:

- **OpenAI**
- **Azure**
- **Anthropic**
- **Cohere**
- **Ollama**
- **HuggingFace**
- **Bedrock**
- **Vertex AI**
- **Voyage AI**

**Example Configuration:**

```toml
[embedding]
provider = "litellm"
base_model = "openai/text-embedding-3-small"
base_dimension = 512

# Environment Variables
export OPENAI_API_KEY=your_openai_key
# Set other environment variables as needed
```

**Supported Models:**

- `openai/text-embedding-3-small`
- `openai/text-embedding-3-large`
- `openai/text-embedding-ada-002`

### Performance Considerations

1. **Batch Size Optimization**:
   - Larger batches improve throughput but may increase latency.
   - Balance batch size with memory and processing speed.

2. **Concurrent Requests**:
   - Adjust based on provider capabilities.
   - Monitor and optimize based on API usage.

3. **Model Selection**:
   - Choose models that fit your domain and accuracy needs.
   - Consider cost implications of different models.

### Conclusion

R2R’s embedding system, powered by LiteLLM, offers flexible and powerful semantic search capabilities. By optimizing batch sizes, managing concurrent requests, and selecting appropriate models, you can ensure efficient and accurate embeddings tailored to your application's needs.

---