# Agent

R2R's agentic capabilities allow for intelligent systems that formulate their own questions, search for information, and provide informed responses based on retrieved context. Agents can be customized on the fly to suit various tasks.

**Note**: Agents in R2R are in beta. Feedback is encouraged at [founders@sciphi.ai](mailto:founders@sciphi.ai).

## Understanding R2R's RAG Agent

The RAG Agent is a specialized component that combines RAG capabilities with autonomous decision-making. It can:

1. Formulate relevant questions
2. Search for information
3. Synthesize findings
4. Generate comprehensive responses

### Planned Extensions

Future updates will include:

- Multi-agent collaboration
- Tool usage capabilities
- Memory and state management
- Custom agent behaviors

## Configuration

### Default Configuration

Configure the agent in your `r2r.toml`:

```toml
[agent]
rag_agent_static_prompt = "rag_agent"
tools = ["search_file_knowledge", "web_search"]
```

### Enable Web Search

Allow agents to search the web for additional context:

```toml
[agent]
enable_web_search = true
web_search_provider = "google"
```

## Using the RAG Agent

### Python Example

```python
from r2r import R2RClient

client = R2RClient()

# Create an agent instance
response = client.agent.create(
    query="Explain the impact of climate change",
    agent_config={
        "tools": ["search_file_knowledge", "web_search"],
        "temperature": 0.7
    }
)

print(response.completion)
```

### Streaming Responses

Get real-time updates as the agent works:

```python
for response in client.agent.create_stream(
    query="Analyze recent AI developments",
    agent_config={"stream": True}
):
    print(response.delta)
```

## Context-Aware Responses

The agent maintains context across interactions:

```python
# First query
response1 = client.agent.create(
    query="What is machine learning?"
)

# Follow-up query
response2 = client.agent.create(
    query="How does it compare to deep learning?",
    conversation_id=response1.conversation_id
)
```

## Working with Files

### Python Example

```python
# Process a specific file
response = client.agent.create(
    query="Summarize this document",
    document_id="doc_123",
    agent_config={
        "focus_on_document": True
    }
)
```

## Advanced Features

### Combined Search Capabilities

#### Example

```python
response = client.agent.create(
    query="Research quantum computing advances",
    agent_config={
        "search_settings": {
            "use_hybrid_search": True,
            "use_web_search": True
        }
    }
)
```

### Custom Search Settings

#### Example

```python
response = client.agent.create(
    query="Find specific examples",
    agent_config={
        "search_settings": {
            "filters": {
                "date": {"$gt": "2023-01-01"}
            }
        }
    }
)
```

## Best Practices

### Conversation Management

- Use conversation IDs for related queries
- Clear context when starting new topics
- Monitor conversation length

### Search Optimization

- Configure appropriate search settings
- Balance between local and web search
- Use filters effectively

### Response Handling

- Process streaming responses efficiently
- Handle errors gracefully
- Validate agent outputs

## Error Handling

### Python Example

```python
try:
    response = client.agent.create(
        query="Complex analysis task",
        agent_config={
            "timeout": 30,
            "max_retries": 3
        }
    )
except Exception as e:
    print(f"Agent error: {e}")
```

## Limitations

Current limitations include:

- Beta status of certain features
- Processing time for complex queries
- Tool usage restrictions
- Memory constraints

## Future Developments

Planned improvements:

- Enhanced tool integration
- Better memory management
- Multi-agent coordination
- Custom agent behaviors

## Conclusion

R2R's Agent capabilities provide a powerful way to automate information gathering and analysis. While still in beta, the system offers robust features for building intelligent applications.

## Security Considerations

- Monitor agent actions
- Set appropriate rate limits
- Review tool access permissions
- Validate agent outputs
