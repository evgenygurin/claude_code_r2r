## RAG

### RAG Customization

RAG (Retrieval-Augmented Generation) in R2R can be extensively customized to suit various use cases. The main components for customization are:

1. **Generation Configuration**: Control the language model’s behavior.
2. **Search Settings**: Fine-tune the retrieval process.
3. **Task Prompt Override**: Customize the system prompt for specific tasks.

#### LLM Provider Configuration

Refer to the [LLM Configuration](https://r2r-docs.sciphi.ai/documentation/configuration/llm) page for detailed information.

#### Retrieval Configuration

Refer to the [Retrieval Configuration](https://r2r-docs.sciphi.ai/documentation/configuration/retrieval/overview) page for detailed information.

### Combining LLM and Retrieval Configuration for RAG

The `rag_generation_config` parameter allows you to customize the language model’s behavior. Default settings are set on the server-side using `r2r.toml`. These settings can be overridden at runtime.

**Python Example:**

```python
from r2r import R2RClient

client = R2RClient()

response = client.retrieval.rag(
    "Who was Aristotle?",
    rag_generation_config={
        "model": "anthropic/claude-3-haiku-20240307",
        "temperature": 0.7,
    },
    search_settings={
        "use_semantic_search": True,
        "limit": 20,
        "use_hybrid_search": True
    }
)
```

### RAG Prompt Override

For specialized tasks, override the default RAG task prompt at runtime.

**Python Example:**

```python
task_prompt_override = """You are an AI assistant specializing in quantum computing.

Your task is to provide a concise summary of the latest advancements in the field,
focusing on practical applications and breakthroughs from the past year."""

response = client.retrieval.rag(
    "What are the latest advancements in quantum computing?",
    rag_generation_config=rag_generation_config,
    task_prompt_override=task_prompt_override
)
```

### Agent-based Interaction

R2R supports multi-turn conversations and complex query processing through its agent endpoint.

**Python Example:**

```python
from r2r import R2RClient

client = R2RClient("http://localhost:7272")

messages = [
    {"role": "system", "content": "You are a helpful AI assistant."},
    {"role": "user", "content": "What are the key differences between quantum and classical computing?"}
]

response = client.retrieval.agent(
    messages=messages,
    vector_search_settings=vector_search_settings,
    graph_settings=graph_settings,
    rag_generation_config=rag_generation_config,
)
```

### Conclusion

By leveraging R2R’s RAG customization options, you can fine-tune retrieval and generation processes to best suit your specific use case and requirements, enhancing the overall performance and relevance of your AI-powered features.

---