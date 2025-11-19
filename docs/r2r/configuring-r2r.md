## **Configuring R2R**

R2R's behavior is controlled via the `r2r.toml` file. Ensure this file is correctly configured before starting the services.

### **Sample `r2r.toml`**

Below is a sample `r2r.toml` with essential configurations:

```toml
[app]
default_max_documents_per_user = 100
default_max_chunks_per_user = 10000
default_max_collections_per_user = 10

[agent]
rag_agent_static_prompt = "rag_agent"
tools = ["search_file_knowledge"]

  [agent.generation_config]
  model = "openai/gpt-4.1"

[auth]
provider = "r2r"
access_token_lifetime_in_minutes = 60
refresh_token_lifetime_in_days = 7
require_authentication = false
require_email_verification = false
default_admin_email = "admin@example.com"
default_admin_password = "change_me_immediately"

[completion]
provider = "litellm"
concurrent_request_limit = 64

  [completion.generation_config]
  model = "openai/gpt-4.1"
  temperature = 0.1
  top_p = 1
  max_tokens_to_sample = 1024
  stream = false
  add_generation_kwargs = { }

[crypto]
provider = "bcrypt"

[database]
provider = "postgres"
default_collection_name = "Default"
default_collection_description = "Your default collection."
batch_size = 256

  [database.graph_creation_settings]
    graph_entity_description_prompt = "graph_entity_description"
    entity_types = []
    relation_types = []
    fragment_merge_count = 1
    max_knowledge_relationships = 100
    max_description_input_length = 65536
    generation_config = { model = "openai/gpt-4.1-mini" }

  [database.graph_enrichment_settings]
    max_summary_input_length = 65536
    generation_config = { model = "openai/gpt-4.1-mini" }
    leiden_params = {}

  [database.graph_search_settings]
    generation_config = { model = "openai/gpt-4.1-mini" }

  [database.limits]
    global_per_min = 300
    monthly_limit = 10000

  [database.route_limits]
    "/v3/retrieval/search" = { route_per_min = 120 }
    "/v3/retrieval/rag" = { route_per_min = 30 }

[embedding]
provider = "litellm"
base_model = "openai/text-embedding-3-small"
base_dimension = 512
batch_size = 128
concurrent_request_limit = 256
quantization_settings = { quantization_type = "FP32" }

[file]
provider = "postgres"

[ingestion]
provider = "r2r"
chunking_strategy = "recursive"
chunk_size = 1024
chunk_overlap = 512
excluded_parsers = []
document_summary_model = "openai/gpt-4.1-mini"

  [ingestion.chunk_enrichment_settings]
    enable_chunk_enrichment = false
    strategies = ["semantic", "neighborhood"]
    forward_chunks = 3
    backward_chunks = 3
    semantic_neighbors = 10
    semantic_similarity_threshold = 0.7
    generation_config = { model = "openai/gpt-4.1-mini" }

  [ingestion.extra_parsers]
    pdf = "zerox"

[orchestration]
provider = "simple"

[prompt]
provider = "r2r"

[email]
provider = "console_mock"
```

### **Key Configuration Sections**

- **[app]**: Sets default limits for documents, chunks, and collections per user.
- **[agent]**: Configures the RAG agent, specifying tools and generation models.
- **[auth]**: Authentication settings, including token lifetimes and default admin credentials.
- **[completion]**: Settings for text completion, including provider and generation configurations.
- **[crypto]**: Cryptographic provider.
- **[database]**: PostgreSQL settings, knowledge graph configurations, and rate limits.
- **[embedding]**: Embedding provider configurations.
- **[file]**: File storage provider.
- **[ingestion]**: Data ingestion settings, including chunking strategies and enrichment configurations.
- **[logging]**: Logging provider and tables.
- **[orchestration]**: Orchestration provider settings.
- **[prompt]**: Prompt management provider.
- **[email]**: Email provider settings.

> **Customization**: Adjust the `r2r.toml` file according to your specific requirements. Ensure that all paths, models, and service URLs match your deployment environment.

---