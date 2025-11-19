## Retrieval

### Overview

R2R’s **Retrieval** system offers advanced search and generation capabilities powered by vector search, knowledge graphs, and large language models (LLMs). The system provides multiple ways to interact with your data, including:

- **Semantic Search**: Direct semantic similarity searches across documents and chunks.
- **Retrieval-Augmented Generation (RAG)**: Combines retrieval with language model generation to produce informative responses grounded in your content.
- **Conversational Agents**: Multi-turn conversational interfaces powered by RAG for complex queries.
- **Completions**: Direct access to language model generation without retrieval.
- **Embeddings**: Generate vector embeddings for provided text.

### Core Features of Retrieval

1. **Vector Search**
    - Semantic similarity matching using document/chunk embeddings.
    - Hybrid search combining vector and keyword approaches.
    - Complex filtering with Postgres-style operators.
    - Configurable search limits and thresholds.

2. **Knowledge Graph Search**
    - Entity and relationship-based retrieval.
    - Multi-hop traversal for connected information.
    - Local and global search strategies.
    - Community-aware knowledge structures.

3. **RAG Generation**
    - Context-aware responses using retrieved content.
    - Customizable generation parameters.
    - Source attribution and citations.
    - Streaming support for real-time responses.

4. **RAG Agent**
    - Multi-turn conversational capabilities.
    - Complex query decomposition.
    - Context maintenance across interactions.
    - Branch management for conversation trees.

5. **Completion**
    - Direct access to language model generation capabilities.
    - Supports both single-turn and multi-turn conversations.

6. **Embeddings**
    - Generate numerical embedding vectors for provided text using specified models.

### Available Endpoints

| Method | Endpoint                  | Description                                                                               |
| :---- | :------------------------ | :---------------------------------------------------------------------------------------- |
| POST   | `/retrieval/search`     | Perform semantic/hybrid/graph search.                                                     |
| POST   | `/retrieval/rag`        | Generate RAG-based responses.                                                             |
| POST   | `/retrieval/agent`      | Engage a RAG-powered conversational agent.                                                |
| POST   | `/retrieval/completion` | Generate text completions using a language model.                                         |
| POST   | `/retrieval/embedding`  | Generate embeddings for the provided text using a specified model.                        |

### Endpoint Details

#### 1. Search R2R

```http
POST /v3/retrieval/search
```

**Description:**
Performs a search query against vector and/or graph-based databases, supporting various search modes and complex filtering.

**Search Modes:**

- `basic`: Defaults to semantic search. Simple and easy to use.
- `advanced`: Combines semantic search with full-text search for more comprehensive results.
- `custom`: Complete control over how search is performed. Provide a full `SearchSettings` object.

**Note:**
If `filters` or `limit` are provided alongside `basic` or `advanced`, they will override the default settings for that mode.

**Allowed Operators:**

- `eq`: Equals
- `neq`: Not equals
- `gt`: Greater than
- `gte`: Greater than or equal
- `lt`: Less than
- `lte`: Less than or equal
- `like`: Pattern matching
- `ilike`: Case-insensitive pattern matching
- `in`: In list
- `nin`: Not in list

**Request Body:**

A JSON object containing the search query and optional search settings.

**Example Request Body:**

```json
{
  "query": "machine learning advancements",
  "search_mode": "advanced",
  "search_settings": {
    "use_semantic_search": true,
    "use_fulltext_search": true,
    "filters": { "document_type": { "$eq": "pdf" } },
    "limit": 20
  }
}
```

**Successful Response:**

```json
{
  "results": {
    "chunk_search_results": [
      {
        "id": "3f3d47f3-8baf-58eb-8bc2-0171fb1c6e09",
        "document_id": "3e157b3a-8469-51db-90d9-52e7d896b49b",
        "collection_ids": ["collection_id1"],
        "score": 0.23943702876567796,
        "text": "Example text from the document",
        "metadata": {
          "associated_query": "What is the capital of France?",
          "title": "example_document.pdf"
        },
        "owner_id": "2acb499e-8428-543b-bd85-0d9098718220"
      }
    ],
    "graph_search_results": [
      {
        "content": {
          "name": "Entity Name",
          "description": "Entity Description",
          "metadata": { "key": "value" }
        },
        "result_type": "entity",
        "chunk_ids": ["c68dc72e-fc23-5452-8f49-d7bd46088a96"],
        "metadata": {
          "associated_query": "What is the capital of France?"
        }
      }
    ]
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X POST "https://api.example.com/v3/retrieval/search" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "query": "machine learning advancements",
           "search_mode": "advanced",
           "search_settings": {
             "use_semantic_search": true,
             "use_fulltext_search": true,
             "filters": { "document_type": { "$eq": "pdf" } },
             "limit": 20
           }
         }'
```

---

#### 2. RAG Query

```http
POST /v3/retrieval/rag
```

**Description:**
Executes a Retrieval-Augmented Generation (RAG) query. This endpoint combines search results with language model generation, allowing for context-based answers. It supports the same filtering capabilities as the search endpoint and can be customized using the `rag_generation_config` parameter.

**Request Body:**

A JSON object containing the query, search settings, and optional generation configurations.

**Example Request Body:**

```json
{
  "query": "Latest trends in AI",
  "search_mode": "custom",
  "search_settings": {
    "use_semantic_search": true,
    "filters": { "publication_year": { "$gte": 2020 } },
    "limit": 5
  },
  "rag_generation_config": {
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 150
  }
}
```

**Successful Response:**

```json
{
  "results": {
    "chunk_search_results": [
      {
        "id": "chunk_id",
        "document_id": "document_id",
        "collection_ids": ["collection_id1"],
        "score": 0.95,
        "text": "Latest trends in AI include deep learning advancements...",
        "metadata": {
          "associated_query": "Latest trends in AI",
          "title": "ai_trends_2024.pdf"
        },
        "owner_id": "owner_id"
      }
    ],
    "graph_search_results": [
      {
        "content": {
          "name": "Deep Learning",
          "description": "A subset of machine learning involving neural networks.",
          "metadata": { "field": "Artificial Intelligence" }
        },
        "result_type": "entity",
        "chunk_ids": ["chunk_id1"],
        "metadata": {
          "associated_query": "Latest trends in AI"
        }
      }
    ],
    "generated_answer": "Recent advancements in AI include the development of more efficient neural network architectures, improvements in reinforcement learning algorithms, and enhanced capabilities in natural language understanding and generation. These innovations are driving progress in various fields such as healthcare, autonomous vehicles, and personalized education."
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X POST "https://api.example.com/v3/retrieval/rag" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "query": "Latest trends in AI",
           "search_mode": "custom",
           "search_settings": {
             "use_semantic_search": true,
             "filters": { "publication_year": { "$gte": 2020 } },
             "limit": 5
           },
           "rag_generation_config": {
             "model": "gpt-4",
             "temperature": 0.7,
             "max_tokens": 150
           }
         }'
```

---

#### 3. RAG-powered Conversational Agent

```http
POST /v3/retrieval/agent
```

**Description:**
Engages with an intelligent RAG-powered conversational agent for complex information retrieval and analysis. This advanced endpoint combines retrieval-augmented generation (RAG) with a conversational AI agent to provide detailed, context-aware responses based on your document collection.

**Key Features:**

- Hybrid search combining vector and knowledge graph approaches.
- Contextual conversation management with `conversation_id` tracking.
- Customizable generation parameters for response style and length.
- Source document citation with optional title inclusion.
- Streaming support for real-time responses.
- Branch management for exploring different conversation paths.

**Use Cases:**

- Research assistance and literature review.
- Document analysis and summarization.
- Technical support and troubleshooting.
- Educational Q&A and tutoring.
- Knowledge base exploration.

**Request Body:**

A JSON object containing the message, search settings, and optional conversation parameters.

**Example Request Body:**

```json
{
  "message": {
    "role": "user",
    "content": "Can you summarize the latest AI research?",
    "name": "User"
  },
  "search_mode": "advanced",
  "search_settings": {
    "use_semantic_search": true,
    "use_fulltext_search": true,
    "filters": { "publication_year": { "$gte": 2023 } },
    "limit": 3
  },
  "conversation_id": "conversation_id",
  "branch_id": "branch_id"
}
```

**Successful Response:**

```json
{
  "results": {
    "messages": [
      {
        "role": "assistant",
        "content": "Certainly! The latest AI research focuses on advancements in deep learning, reinforcement learning, and natural language processing. Notable projects include the development of more efficient neural network architectures and improved model interpretability techniques.",
        "name": "Assistant",
        "function_call": {},
        "tool_calls": [],
        "conversation_id": "conversation_id",
        "branch_id": "branch_id"
      }
    ]
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X POST "https://api.example.com/v3/retrieval/agent" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "message": {
             "role": "user",
             "content": "Can you summarize the latest AI research?",
             "name": "User"
           },
           "search_mode": "advanced",
           "search_settings": {
             "use_semantic_search": true,
             "use_fulltext_search": true,
             "filters": { "publication_year": { "$gte": 2023 } },
             "limit": 3
           },
           "conversation_id": "conversation_id",
           "branch_id": "branch_id"
         }'
```

---

#### 4. Generate Message Completions

```http
POST /v3/retrieval/completion
```

**Description:**
Generates completions for a list of messages using the language model. The generation process can be customized using the `generation_config` parameter.

**Request Body:**

A JSON object containing the messages and optional generation configurations.

**Example Request Body:**

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Tell me about the advancements in AI."
    }
  ],
  "generation_config": {
    "model": "gpt-4",
    "temperature": 0.7,
    "top_p": 0.9,
    "max_tokens_to_sample": 150,
    "stream": false
  },
  "response_model": "gpt-4"
}
```

**Successful Response:**

```json
{
  "results": {
    "messages": [
      {
        "role": "assistant",
        "content": "Recent advancements in AI include the development of more efficient neural network architectures, improvements in reinforcement learning algorithms, and enhanced capabilities in natural language understanding and generation. These innovations are driving progress in various fields such as healthcare, autonomous vehicles, and personalized education.",
        "conversation_id": "conversation_id",
        "branch_id": "branch_id"
      }
    ]
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X POST "https://api.example.com/v3/retrieval/completion" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "messages": [
             {
               "role": "user",
               "content": "Tell me about the advancements in AI."
             }
           ],
           "generation_config": {
             "model": "gpt-4",
             "temperature": 0.7,
             "top_p": 0.9,
             "max_tokens_to_sample": 150,
             "stream": false
           },
           "response_model": "gpt-4"
         }'
```

---

#### 5. Generate Embeddings

```http
POST /v3/retrieval/embedding
```

**Description:**
Generates numerical embedding vectors for the provided text using a specified model.

**Request Body:**

A JSON object containing the text to generate embeddings for.

**Example Request Body:**

```json
{
  "text": "Artificial Intelligence is transforming the world."
}
```

**Successful Response:**

```json
{
  "results": {
    "embeddings": [0.123, 0.456, 0.789]
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X POST "https://api.example.com/v3/retrieval/embedding" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "text": "Artificial Intelligence is transforming the world."
         }'
```

---