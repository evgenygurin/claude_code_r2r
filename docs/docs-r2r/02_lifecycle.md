# R2R Application Lifecycle

R2R's application lifecycle encompasses customization, configuration, deployment, implementation, and interaction. The lifecycle is designed to provide flexibility and scalability for various use cases.

## Developer Workflow

- **Customize**: Developers tailor R2R applications using R2RConfig and the R2R SDK.
- **Configure**: Adjust settings via configuration files (`r2r.toml`) or runtime overrides.
- **Deploy**: Launch R2R using Docker, cloud platforms, or local installations.
- **Implement**: Integrate R2R into applications using provided APIs and SDKs.
- **Interact**: Users engage with the R2R application through interfaces like dashboards or APIs to perform RAG queries or search documents.

## User Interaction

- **Users** interact with the R2R application, typically over an HTTP interface, to run RAG queries or search documents.
- Access the **R2R Dashboard** for managing documents, collections, and performing searches.

## Hello R2R (Code Example)

**Python Example** at `core/examples/hello_r2r.py`:

```python
from r2r import R2RClient

client = R2RClient("http://localhost:7272")

# Create a test document
with open("test.txt", "w") as file:
    file.write("John is a person that works at Google.")

client.documents.create(file_path="test.txt")

# Call RAG directly
rag_response = client.retrieval.rag(
    query="Who is John",
    rag_generation_config={"model": "openai/gpt-4o-mini", "temperature": 0.0},
)

results = rag_response["results"]

print(f"Search Results:\n{results['search_results']}")
print(f"Completion:\n{results['completion']}")
```

**Sample Output:**

```json
{
  "results": {
    "search_results": {
      "chunk_search_results": [
        {
          "chunk_id": "b9f40dbd-2c8e-5c0a-8454-027ac45cb0ed",
          "document_id": "7c319fbe-ca61-5770-bae2-c3d0eaa8f45c",
          "score": 0.6847735847465275,
          "text": "John is a person that works at Google.",
          "metadata": {
            "version": "v0",
            "chunk_order": 0,
            "document_type": "txt",
            "associated_query": "Who is John"
          }
        }
      ],
      "kg_search_results": []
    },
    "completion": {
      "id": "chatcmpl-AV1Sc9DORfHvq7yrmukxfJPDV5dCB",
      "choices": [
        {
          "finish_reason": "stop",
          "index": 0,
          "message": {
            "content": "John is a person that works at Google [1].",
            "role": "assistant"
          }
        }
      ],
      "created": 1731957146,
      "model": "gpt-4o-mini",
      "object": "chat.completion",
      "usage": {
        "completion_tokens": 11,
        "prompt_tokens": 145,
        "total_tokens": 156
      }
    }
  }
}
```

This snippet:

1. Creates a file with simple text.
2. Ingests it to R2R.
3. Runs a **Retrieval-Augmented Generation** query.
4. Prints the context matched ("search_results") and the generated answer ("completion").
