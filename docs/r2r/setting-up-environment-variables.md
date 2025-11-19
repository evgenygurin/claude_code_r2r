## **Setting Up Environment Variables**

Environment variables are crucial for configuring services. You can set them directly in your shell or use a `.env` file for Docker Compose.

### **Creating a `.env` File**

Create a `.env` file in the root directory of your project with the following content:

```dotenv
# General R2R Settings
R2R_PORT=7272
R2R_HOST=0.0.0.0
R2R_CONFIG_NAME=
R2R_CONFIG_PATH=/app/config
R2R_PROJECT_NAME=r2r_default

# PostgreSQL Settings
R2R_POSTGRES_USER=postgres
R2R_POSTGRES_PASSWORD=postgres
R2R_POSTGRES_HOST=postgres
R2R_POSTGRES_PORT=5432
R2R_POSTGRES_DBNAME=postgres
R2R_POSTGRES_MAX_CONNECTIONS=1024
R2R_POSTGRES_STATEMENT_CACHE_SIZE=100

# Hatchet Settings
HATCHET_POSTGRES_USER=hatchet_user
HATCHET_POSTGRES_PASSWORD=hatchet_password
HATCHET_POSTGRES_DBNAME=hatchet
HATCHET_CLIENT_GRPC_MAX_RECV_MESSAGE_LENGTH=134217728
HATCHET_CLIENT_GRPC_MAX_SEND_MESSAGE_LENGTH=134217728

# RabbitMQ Settings
R2R_RABBITMQ_PORT=5673
R2R_RABBITMQ_MGMT_PORT=15673

# Graph Clustering Settings
R2R_GRAPH_CLUSTERING_PORT=7276

# R2R Dashboard Settings
R2R_DASHBOARD_PORT=7273

# Nginx Settings
R2R_NGINX_PORT=7280

# API Keys and External Services
OPENAI_API_KEY=your_openai_api_key
OPENAI_API_BASE=https://api.openai.com
ANTHROPIC_API_KEY=your_anthropic_api_key
AZURE_API_KEY=your_azure_api_key
AZURE_API_BASE=https://api.azure.com
AZURE_API_VERSION=2023-03-15-preview
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/google/credentials.json
VERTEX_PROJECT=your_vertex_project
VERTEX_LOCATION=your_vertex_location
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_REGION_NAME=your_aws_region
GROQ_API_KEY=your_groq_api_key
COHERE_API_KEY=your_cohere_api_key
ANYSCALE_API_KEY=your_anyscale_api_key
OLLAMA_API_BASE=http://host.docker.internal:11434
HUGGINGFACE_API_BASE=http://host.docker.internal:8080
HUGGINGFACE_API_KEY=your_huggingface_api_key
UNSTRUCTURED_API_KEY=your_unstructured_api_key
UNSTRUCTURED_API_URL=https://api.unstructured.io/general/v0/general
UNSTRUCTURED_SERVICE_URL=http://unstructured:7275
UNSTRUCTURED_NUM_WORKERS=10
CLUSTERING_SERVICE_URL=http://graph_clustering:7276
```

> **Note**: Replace placeholder values (e.g., `your_openai_api_key`) with your actual credentials and configurations. Ensure sensitive information like API keys and passwords are securely stored and managed.

---