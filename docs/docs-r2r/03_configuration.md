# Configuration

R2R is highly configurable, allowing you to tailor its behavior to your specific needs. Configuration can be done at the server-side using configuration files (`r2r.toml`) or at runtime via API calls.

## Configuration Overview

R2R configurations are divided into two primary levels:

1. **Server-Side Configuration**: Managed through the `r2r.toml` file and environment variables.
2. **Runtime Overrides**: Passed directly in API calls to adjust settings dynamically.

## Server-Side Configuration (`r2r.toml`)

The `r2r.toml` file allows you to define server-side settings that govern the behavior of R2R. Below are the main configuration sections:

### Example: `r2r.toml`

```toml
[completion]
provider = "litellm"
concurrent_request_limit = 16

[completion.generation_config]
model = "openai/gpt-4o"
temperature = 0.5

[ingestion]
provider = "r2r"
chunking_strategy = "recursive"
chunk_size = 1024
chunk_overlap = 512
excluded_parsers = ["mp4"]

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
```

## Runtime Overrides

Runtime overrides allow you to adjust configuration settings on a per-request basis. These overrides take precedence over server-side configurations.

## Postgres Configuration

The Postgres configuration section defines database connection settings and other database-related parameters.

### Example Configuration

```toml
[database]
provider = "postgres"
user = "postgres"
password = "postgres"
host = "localhost"
port = "5432"
db_name = "r2r"
```

### Key Features

- Secure password storage
- Connection pooling
- Automatic reconnection
- Query optimization

## Embedding Configuration

Configure embedding models and settings for vector representations of text.

### Example Configuration

```toml
[embedding]
provider = "litellm"
base_model = "openai/text-embedding-3-small"
base_dimension = 512
batch_size = 512
rerank_model = "BAAI/bge-reranker-v2-m3"
```

## Auth & Users Configuration

Configure authentication and user management settings.

### Example Configuration

```toml
[auth]
provider = "r2r"
require_authentication = true
require_email_verification = false
default_admin_email = "admin@example.com"
default_admin_password = "change_me_immediately"
```

### Key Features

- User authentication
- Role-based access control
- Email verification
- Password policies

## Data Ingestion Configuration

Configure how documents are processed and stored.

### Example Configuration

```toml
[ingestion]
provider = "r2r"
chunking_strategy = "recursive"
chunk_size = 1024
chunk_overlap = 512
excluded_parsers = ["mp4"]
```

## Retrieval Configuration

Configure search and retrieval settings.

### Example Configuration

```toml
[retrieval]
provider = "r2r"
search_type = "hybrid"
reranking_enabled = true
max_results = 10
```

## RAG Configuration

Configure Retrieval-Augmented Generation settings.

### Example Configuration

```toml
[rag]
provider = "r2r"
model = "openai/gpt-4o"
temperature = 0.7
max_tokens = 1000
```

## Graphs Configuration

Configure knowledge graph settings.

### Example Configuration

```toml
[graphs]
provider = "r2r"
extraction_model = "openai/gpt-4o"
relationship_types = ["works_at", "located_in", "part_of"]
```

## Prompts Configuration

Configure system prompts and templates.

### Example Configuration

```toml
[prompts]
provider = "r2r"
template_dir = "prompts/"
default_system_prompt = "You are a helpful assistant."
```
