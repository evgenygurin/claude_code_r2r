## Configuration

R2R is highly configurable, allowing you to tailor its behavior to your specific needs. Configuration can be done at the server-side using configuration files (`r2r.toml`) or at runtime via API calls.

### Configuration Overview

R2R configurations are divided into two primary levels:
1. **Server-Side Configuration**: Managed through the `r2r.toml` file and environment variables.
2. **Runtime Overrides**: Passed directly in API calls to adjust settings dynamically.

### Server-Side Configuration (`r2r.toml`)

The `r2r.toml` file allows you to define server-side settings that govern the behavior of R2R. Below are the main configuration sections:

#### Example: `r2r.toml`

```toml
[completion]
provider = "litellm"
concurrent_request_limit = 16

[completion.generation_config]
model = "openai/gpt-4.1"
temperature = 0.5

[ingestion]
provider = "r2r"
chunking_strategy = "recursive"
chunk_size = 1024
chunk_overlap = 512
excluded_parsers = []

[database]
provider = "postgres"
user = "your_postgres_user"
password = "your_postgres_password"
host = "your_postgres_host"
port = "your_postgres_port"
db_name = "your_database_name"
project_name = "your_project_name"

[embedding]
provider = "litellm"
base_model = "openai/text-embedding-3-small"
base_dimension = 512
batch_size = 512
rerank_model = "BAAI/bge-reranker-v2-m3"
concurrent_request_limit = 256

[auth]
provider = "r2r"
require_authentication = true
require_email_verification = false
default_admin_email = "admin@example.com"
default_admin_password = "change_me_immediately"
access_token_lifetime_in_minutes = 60
refresh_token_lifetime_in_days = 7
secret_key = "your-secret-key"

[ingestion.chunk_enrichment_settings]
enable_chunk_enrichment = true
strategies = ["semantic", "neighborhood"]
forward_chunks = 3
backward_chunks = 3
semantic_neighbors = 10
semantic_similarity_threshold = 0.7
generation_config = { model = "openai/gpt-4.1-mini" }

[agent]
rag_agent_static_prompt = "rag_agent"
tools = ["search_file_knowledge", "web_search"]

[database.graph_creation_settings]
entity_types = []
relation_types = []
max_knowledge_triples = 100
fragment_merge_count = 4
generation_config = { model = "openai/gpt-4.1-mini" }

[database.graph_enrichment_settings]
max_description_input_length = 65536
max_summary_input_length = 65536
generation_config = { model = "openai/gpt-4.1-mini" }
leiden_params = {}

[database.graph_settings]
generation_config = { model = "openai/gpt-4.1-mini" }
```

### Runtime Overrides

Runtime overrides allow you to adjust configurations dynamically without modifying the `r2r.toml` file. This is useful for temporary changes or testing different settings on the fly.

**Example: Customizing RAG Query at Runtime**

```python
rag_response = client.retrieval.rag(
    query="Who is Jon Snow?",
    rag_generation_config={
        "model": "anthropic/claude-3-haiku-20240307",
        "temperature": 0.7
    },
    search_settings={
        "use_semantic_search": True,
        "limit": 20,
        "use_hybrid_search": True
    }
)
```

### Postgres Configuration

R2R uses Postgres for relational and vector data storage, leveraging the `pgvector` extension for vector indexing.

#### Example Configuration

```toml
[database]
provider = "postgres"
user = "your_postgres_user"
password = "your_postgres_password"
host = "your_postgres_host"
port = "your_postgres_port"
db_name = "your_database_name"
project_name = "your_project_name"
```

**Key Features:**
- **pgvector**: Enables efficient vector operations.
- **Full-Text Indexing**: Utilizes Postgres’s `ts_rank` for full-text search.
- **JSONB**: Stores flexible metadata.

### Embedding Configuration

R2R uses **LiteLLM** to manage embedding providers, allowing flexibility in selecting different LLM providers.

#### Example Configuration

```toml
[embedding]
provider = "litellm"
base_model = "openai/text-embedding-3-small"
base_dimension = 512
batch_size = 512
rerank_model = "BAAI/bge-reranker-v2-m3"
concurrent_request_limit = 256
```

**Environment Variables:**
- `OPENAI_API_KEY`
- `HUGGINGFACE_API_KEY`
- `ANTHROPIC_API_KEY`
- `COHERE_API_KEY`
- `OLLAMA_API_KEY`
- etc.

**Supported Providers:**
- OpenAI
- Azure
- Anthropic
- Cohere
- Ollama
- HuggingFace
- Bedrock
- Vertex AI
- Voyage AI

### Auth & Users Configuration

R2R’s authentication system supports secure user registration, login, session management, and access control.

#### Example Configuration

```toml
[auth]
provider = "r2r"
require_authentication = true
require_email_verification = false
default_admin_email = "admin@example.com"
default_admin_password = "change_me_immediately"
access_token_lifetime_in_minutes = 60
refresh_token_lifetime_in_days = 7
secret_key = "your-secret-key"
```

**Key Features:**
- **JWT-Based Authentication**: Utilizes access and refresh tokens.
- **Email Verification**: Optional, recommended for production.
- **Superuser Management**: Default admin creation and superuser capabilities.

### Data Ingestion Configuration

Configure how R2R ingests documents, including parsing, chunking, and embedding strategies.

#### Example Configuration

```toml
[ingestion]
provider = "r2r"
chunking_strategy = "recursive"
chunk_size = 1024
chunk_overlap = 512
excluded_parsers = []

[ingestion.chunk_enrichment_settings]
enable_chunk_enrichment = true
strategies = ["semantic", "neighborhood"]
forward_chunks = 3
backward_chunks = 3
semantic_neighbors = 10
semantic_similarity_threshold = 0.7
generation_config = { model = "openai/gpt-4.1-mini" }
```

**Modes:**
- `fast`: Speed-oriented ingestion.
- `hi-res`: Comprehensive, high-quality ingestion.
- `custom`: Fine-grained control with a full `ingestion_config` dictionary.

### Retrieval Configuration

Focuses on search settings, combining vector and knowledge-graph search capabilities.

#### Example Configuration

```json
{
  "search_settings": {
    "use_semantic_search": true,
    "limit": 20,
    "use_hybrid_search": true,
    "graph_search_settings": {
      "use_graph_search": true,
      "kg_search_type": "local"
    }
  }
}
```

### RAG Configuration

Customize RAG (Retrieval-Augmented Generation) settings, including the language model's behavior.

#### Example Configuration

```python
rag_generation_config = {
    "model": "anthropic/claude-3-haiku-20240307",
    "temperature": 0.7,
    "top_p": 0.95,
    "max_tokens_to_sample": 1500,
    "stream": True
}
```

### Graphs Configuration

Defines settings related to knowledge graph creation and enrichment.

#### Example Configuration

```toml
[database.graph_creation_settings]
entity_types = []
relation_types = []
max_knowledge_triples = 100
fragment_merge_count = 4
generation_config = { model = "openai/gpt-4.1-mini" }

[database.graph_enrichment_settings]
max_description_input_length = 65536
max_summary_input_length = 65536
generation_config = { model = "openai/gpt-4.1-mini" }
leiden_params = {}

[database.graph_settings]
generation_config = { model = "openai/gpt-4.1-mini" }
```

### Prompts Configuration

Manages prompt templates used for various tasks within R2R.

#### Example Configuration

Prompts are stored in Postgres and can be managed via the SDK.

**Example: Adding a Prompt**

```python
response = client.prompts.add_prompt(
    name="my_new_prompt",
    template="Hello, {name}! Welcome to {service}.",
    input_types={"name": "str", "service": "str"}
)
```

---