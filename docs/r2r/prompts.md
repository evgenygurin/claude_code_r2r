## Prompts

### Prompt Management in R2R

R2R provides a flexible system for managing prompts, allowing you to create, update, retrieve, and delete prompts dynamically. This system is crucial for customizing the behavior of language models and ensuring consistent interactions across your application.

### Default Prompts

R2R comes with a set of default prompts loaded from YAML files located in the [`py/core/providers/database/prompts`](https://github.com/SciPhi-AI/R2R/tree/main/py/core/providers/database/prompts) directory. These prompts serve as starting points for various tasks.

**Example: `rag.yaml`**

```yaml
rag:
  template: >
    ## Task:

    Answer the query given immediately below given the context which follows later. Use line item references like [1], [2], ... to refer to specifically numbered items in the provided context. Pay close attention to the title of each given source to ensure consistency with the query.

    ### Query:

    {query}

    ### Context:

    {context}

    ### Response:
```

#### Prompt Files

| Prompt File                                  | Purpose                                                                                       |
|----------------------------------------------|-----------------------------------------------------------------------------------------------|
| `rag.yaml`                           | Default prompt for Retrieval-Augmented Generation (RAG) tasks.                              |
| `graphrag_community_reports.yaml`             | Used in GraphRAG to generate reports about communities or clusters in the knowledge graph.   |
| `graph_entity_description.yaml`            | System prompt for the “map” phase in GraphRAG, used to process individual nodes or edges.     |
| `graphrag_map_system.yaml`                    | System prompt for the “map” phase in GraphRAG.                                              |
| `graphrag_reduce_system.yaml`                 | System prompt for the “reduce” phase in GraphRAG.                                           |
| `graphrag_triples_extraction_few_shot.yaml`   | Few-shot prompt for extracting subject-predicate-object triplets in GraphRAG.               |
| `hyde.yaml`                                  | Related to Hypothetical Document Embeddings (HyDE) for improving retrieval performance.      |
| `rag_agent.yaml`                             | Defines behavior and instructions for the RAG agent, coordinating retrieval and generation.  |
| `rag_context.yaml`                           | Used to process or format the context retrieved for RAG tasks.                               |
| `rag_fusion.yaml`                            | Used in RAG fusion techniques for combining information from multiple retrieved passages.    |
| `system.yaml`                                | Contains general system-level prompts or instructions for the R2R system.                    |

### Prompt Provider

R2R uses a Postgres class to manage prompts, enabling storage, retrieval, and manipulation of prompts. This leverages both a Postgres database and YAML files for flexibility and persistence.

**Key Features:**

1. **Database Storage**: Prompts are stored in a Postgres table for efficient querying and updates.
2. **YAML File Support**: Prompts can be loaded from YAML files, facilitating version control and distribution.
3. **In-Memory Cache**: Prompts are kept in memory for fast access during runtime.

### Prompt Structure

Each prompt in R2R consists of:

- **Name**: A unique identifier for the prompt.
- **Template**: The actual text of the prompt, which may include placeholders for dynamic content.
- **Input Types**: A dictionary specifying the expected types for any dynamic inputs to the prompt.

### Managing Prompts

R2R provides several endpoints and SDK methods for managing prompts:

#### Adding a Prompt

```python
from r2r import R2RClient

client = R2RClient()

response = client.prompts.add_prompt(
    name="my_new_prompt",
    template="Hello, {name}! Welcome to {service}.",
    input_types={"name": "str", "service": "str"}
)
```

#### Updating a Prompt

```python
response = client.prompts.update_prompt(
    name="my_existing_prompt",
    template="Updated template: {variable}",
    input_types={"variable": "str"}
)
```

#### Retrieving a Prompt

```python
response = client.prompts.get_prompt(
    prompt_name="my_prompt",
    inputs={"variable": "example"},
    prompt_override="Optional override text"
)
```

Refer to the [Prompt API Reference](https://r2r-docs.sciphi.ai/api-and-sdks/prompts) for more details.

### Security Considerations

Access to prompt management functions is restricted to superusers to prevent unauthorized modifications to system prompts. Ensure only trusted administrators have superuser access to your R2R deployment.

### Conclusion

R2R’s prompt management system offers powerful and flexible control over language model behavior. By effectively managing prompts, you can create dynamic, context-aware, and maintainable AI-powered features tailored to your application's needs.

---