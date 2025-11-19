## Agent

R2R’s agentic capabilities allow for intelligent systems that formulate their own questions, search for information, and provide informed responses based on retrieved context. Agents can be customized on the fly to suit various tasks.

**Note**: Agents in R2R are in beta. Feedback is encouraged at [founders@sciphi.ai](mailto:founders@sciphi.ai).

### Understanding R2R’s RAG Agent

R2R’s RAG agent combines large language models with search capabilities over ingested documents to provide powerful, context-aware responses. When initializing an R2R application, it automatically creates a RAG assistant ready for use.

**Planned Extensions:**

- Multiple tool support (e.g., code interpreter, file search)
- Persistent conversation threads
- Complete end-to-end observability of agent interactions
- Local RAG capabilities for offline AI agents

### Configuration

The RAG agent is configured through the `r2r.toml` file. By default, it uses local search.

**Default Configuration:**

```toml
[agent]
rag_agent_static_prompt = "rag_agent"
tools = ["search_file_knowledge"]
```

**Enable Web Search:**

```toml
[agent]
rag_agent_static_prompt = "rag_agent"
tools = ["search_file_knowledge", "web_search"]
```

### Using the RAG Agent

Access the agent through the R2R API via the `agent` endpoint.

**Python Example:**

```python
from r2r import R2RClient

# Initialize the client
client = R2RClient("http://localhost:7272")

# Make a simple query
first_reply = client.retrieval.agent(
    message={"role": "user", "content": "Who was Aristotle?"},
    search_settings={"limit": 5, "filters": {}},
)

# Save the conversation ID for continued interaction
conversation_id = first_reply["results"]["conversation_id"]

# Make a follow-up query using the conversation context
second_reply = client.retrieval.agent(
    message={"role": "user", "content": "What were his contributions to philosophy?"},
    search_settings={"limit": 5, "filters": {}},
    conversation_id=conversation_id,
)
```

**Streaming Responses:**

```python
streaming_response = client.agent(
    message={"role": "user", "content": "Who was Aristotle?"},
    search_settings={"limit": 5, "filters": {}},
    rag_generation_config={"max_tokens": 300, "stream": True},
    conversation_id=conversation_id,
)

print("Streaming RAG Assistant Response:")
for chunk in streaming_response:
    print(chunk, end="", flush=True)
```

### Context-Aware Responses

The agent maintains conversation context, enabling it to handle follow-up questions intelligently based on conversation history.

### Working with Files

The Conversation API allows the agent to be aware of specific files within a conversation.

**Python Example:**

```python
# Create a new conversation
conversation = client.conversations.create("results")

# Inform the agent about available files
client.conversations.add_message(
    conversation_id=conversation["id"],
    role="system",
    content="You have access to the following file: {document_info['title']}"
)

# Query with file context
response = client.retrieval.agent(
    message={
        "role": "user",
        "content": "Summarize the main points of the document"
    },
    search_settings={"limit": 5, "filters": {}},
    conversation_id=conversation["id"]
)
```

### Advanced Features

#### Combined Search Capabilities

When both local and web search are enabled, the agent can:

- Search through your local document store.
- Perform web searches for additional context.
- Maintain conversation context.
- Synthesize information from multiple sources.

**Example:**

```python
response = client.retrieval.agent(
    message={
        "role": "user",
        "content": "Compare historical and modern interpretations"
    },
    search_settings={
        "limit": 5,
        "filters": {},
        "use_web_search": True  # requires `Serper` API key
    },
    conversation_id=conversation_id
)
```

#### Custom Search Settings

Customize search behavior using the `search_settings` parameter.

**Example:**

```python
response = client.retrieval.agent(
    message={"role": "user", "content": "Query"},
    search_settings={
        "limit": 5,  # Number of results to return
        "filters": {
            "date": "2023",  # Example filter
            "category": "technology"
        }
    }
)
```

### Best Practices

1. **Conversation Management**:
   - Maintain conversation IDs for related queries.
   - Use the system role to provide context about available files.
   - Clear conversation context when starting new topics.

2. **Search Optimization**:
   - Adjust the `limit` parameter based on needed context.
   - Use filters to narrow search scope.
   - Consider enabling web search for broader context.

3. **Response Handling**:
   - Use streaming for long responses.
   - Process response chunks appropriately in streaming mode.
   - Check for error messages in responses.

### Error Handling

The agent may return error messages in the response. Always check for errors.

**Python Example:**

```python
from r2r import R2RException

try:
    await client.retrieval.agent(...)
except R2RException as e:
    if e.status_code == 401:
        print("Invalid credentials")
    elif e.status_code == 400:
        print("Email not verified")
```

### Limitations

- **Beta Feature**: The agent is currently in beta.
- **Web Search Requirements**: Requires additional configuration.
- **Streaming Response Structure**: May differ from non-streaming responses.
- **Offline Mode Limitations**: Some features may not be available offline.

### Future Developments

R2R plans to enhance the agent system with:

- Enhanced tool integration.
- Improved conversation management.
- Better search capabilities.
- More customization options.

Stay updated with the latest developments by checking the R2R documentation regularly.

### Conclusion

R2R’s agent system provides powerful, context-aware interactions by combining LLMs with advanced search capabilities. By leveraging these features, you can create intelligent assistants that offer comprehensive and accurate responses based on your document corpus.

---