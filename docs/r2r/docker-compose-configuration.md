## **Docker Compose Configuration**

Docker Compose orchestrates the deployment of all services. There are three main Docker Compose files provided:

1. **compose.yaml**: Basic setup with PostgreSQL and R2R.
2. **compose.full.yaml**: Extends `compose.yaml` by adding Hatchet, RabbitMQ, and related services.
3. **compose.full_with_replicas.yaml**: Further extends `compose.full.yaml` with additional replicas and services.

For a comprehensive deployment, we'll focus on using `compose.full_with_replicas.yaml`.

### **Networks and Volumes**

#### **Networks**

- **r2r-network**: A bridge network facilitating communication between all services.

#### **Volumes**

- **hatchet_certs**: Stores Hatchet SSL certificates.
- **hatchet_config**: Configuration files for Hatchet.
- **hatchet_api_key**: Stores the Hatchet API key.
- **postgres_data**: Persistent storage for PostgreSQL data.
- **hatchet_rabbitmq_data**: Persistent storage for RabbitMQ data.
- **hatchet_rabbitmq_conf**: Configuration files for RabbitMQ.
- **hatchet_postgres_data**: Persistent storage for Hatchet PostgreSQL data.

> **Note**: Volumes ensure data persistence across container restarts and deployments.

### **Services Breakdown**

Below is a detailed overview of each service included in `compose.full_with_replicas.yaml`.

1. **PostgreSQL (`postgres`)**

   - **Image**: `pgvector/pgvector:pg16`
   - **Purpose**: Primary database with vector support for R2R.
   - **Environment Variables**:
     - `POSTGRES_USER`: Database username.
     - `POSTGRES_PASSWORD`: Database password.
     - `POSTGRES_HOST`: Hostname for the database service.
     - `POSTGRES_PORT`: Port number.
     - `POSTGRES_MAX_CONNECTIONS`: Maximum allowed connections.
   - **Volumes**: `postgres_data` for persistent storage.
   - **Ports**: Maps `${R2R_POSTGRES_PORT:-5432}` on the host to `5432` in the container.
   - **Healthcheck**: Ensures PostgreSQL is ready before other services depend on it.
   - **Restart Policy**: `on-failure`

2. **Hatchet PostgreSQL (`hatchet-postgres`)**

   - **Image**: `postgres:latest`
   - **Purpose**: Dedicated PostgreSQL instance for Hatchet.
   - **Environment Variables**:
     - `POSTGRES_DB`: Database name (default `hatchet`).
     - `POSTGRES_USER`: Database username (default `hatchet_user`).
     - `POSTGRES_PASSWORD`: Database password (default `hatchet_password`).
   - **Volumes**: `hatchet_postgres_data` for persistent storage.
   - **Healthcheck**: Ensures Hatchet PostgreSQL is ready.

3. **RabbitMQ (`hatchet-rabbitmq`)**

   - **Image**: `rabbitmq:3-management`
   - **Purpose**: Message broker for Hatchet orchestration.
   - **Environment Variables**:
     - `RABBITMQ_DEFAULT_USER`: Default RabbitMQ user (`user`).
     - `RABBITMQ_DEFAULT_PASS`: Default RabbitMQ password (`password`).
   - **Ports**:
     - `${R2R_RABBITMQ_PORT:-5673}` on the host to `5672` in the container.
     - `${R2R_RABBITMQ_MGMT_PORT:-15673}` on the host to `15672` in the container.
   - **Volumes**:
     - `hatchet_rabbitmq_data`: Persistent storage for RabbitMQ data.
     - `hatchet_rabbitmq_conf`: Configuration files for RabbitMQ.
   - **Healthcheck**: Ensures RabbitMQ is operational.

4. **Hatchet Create DB (`hatchet-create-db`)**

   - **Image**: `postgres:latest`
   - **Purpose**: Initializes the Hatchet database if it doesn't exist.
   - **Command**: Waits for PostgreSQL to be ready and creates the database if absent.
   - **Environment Variables**:
     - `DATABASE_URL`: Connection string for Hatchet PostgreSQL.
   - **Depends On**: `hatchet-postgres`
   - **Networks**: `r2r-network`

5. **Hatchet Migration (`hatchet-migration`)**

   - **Image**: `ghcr.io/hatchet-dev/hatchet/hatchet-migrate:latest`
   - **Purpose**: Applies database migrations for Hatchet.
   - **Environment Variables**:
     - `DATABASE_URL`: Connection string for Hatchet PostgreSQL.
   - **Depends On**: `hatchet-create-db`
   - **Networks**: `r2r-network`

6. **Hatchet Setup Config (`hatchet-setup-config`)**

   - **Image**: `ghcr.io/hatchet-dev/hatchet/hatchet-admin:latest`
   - **Purpose**: Configures Hatchet with initial settings.
   - **Command**: Runs Hatchet admin quickstart with specific options.
   - **Environment Variables**:
     - `DATABASE_URL`: Connection string for Hatchet PostgreSQL.
     - `HATCHET_CLIENT_GRPC_MAX_RECV_MESSAGE_LENGTH`: GRPC settings.
     - Other Hatchet-specific configurations.
   - **Volumes**:
     - `hatchet_certs`: SSL certificates.
     - `hatchet_config`: Configuration files.
   - **Depends On**:
     - `hatchet-migration`
     - `hatchet-rabbitmq`
   - **Networks**: `r2r-network`

7. **Hatchet Engine (`hatchet-engine`)**

   - **Image**: `ghcr.io/hatchet-dev/hatchet/hatchet-engine:latest`
   - **Purpose**: Core engine for Hatchet operations.
   - **Command**: Runs Hatchet engine with specified configuration.
   - **Environment Variables**:
     - `DATABASE_URL`: Connection string for Hatchet PostgreSQL.
     - GRPC settings.
   - **Ports**: Maps `${R2R_HATCHET_ENGINE_PORT:-7077}` on the host to `7077` in the container.
   - **Volumes**:
     - `hatchet_certs`: SSL certificates.
     - `hatchet_config`: Configuration files.
   - **Healthcheck**: Ensures the Hatchet engine is live.
   - **Depends On**: `hatchet-setup-config`
   - **Restart Policy**: `on-failure`

8. **Hatchet Dashboard (`hatchet-dashboard`)**

   - **Image**: `ghcr.io/hatchet-dev/hatchet/hatchet-dashboard:latest`
   - **Purpose**: Web interface for managing Hatchet.
   - **Command**: Runs Hatchet dashboard with specified configuration.
   - **Environment Variables**:
     - `DATABASE_URL`: Connection string for Hatchet PostgreSQL.
   - **Ports**: Maps `${R2R_HATCHET_DASHBOARD_PORT:-7274}` on the host to `80` in the container.
   - **Volumes**:
     - `hatchet_certs`: SSL certificates.
     - `hatchet_config`: Configuration files.
   - **Depends On**: `hatchet-setup-config`
   - **Networks**: `r2r-network`

9. **Setup Token (`setup-token`)**

   - **Image**: `ghcr.io/hatchet-dev/hatchet/hatchet-admin:latest`
   - **Purpose**: Generates and stores the Hatchet API token.
   - **Command**: Executes a shell script to create and validate the API token.
   - **Volumes**:
     - `hatchet_certs`: SSL certificates.
     - `hatchet_config`: Configuration files.
     - `hatchet_api_key`: Stores the generated API key.
   - **Depends On**: `hatchet-setup-config`
   - **Networks**: `r2r-network`

10. **Unstructured (`unstructured`)**

    - **Image**: `${UNSTRUCTURED_IMAGE:-ragtoriches/unst-prod}`
    - **Purpose**: Handles document parsing and processing.
    - **Healthcheck**: Ensures the Unstructured service is operational.
    - **Networks**: `r2r-network`

11. **Graph Clustering (`graph_clustering`)**

    - **Image**: `${GRAPH_CLUSTERING_IMAGE:-ragtoriches/cluster-prod}`
    - **Purpose**: Manages community detection within knowledge graphs.
    - **Ports**: Maps `${R2R_GRAPH_CLUSTERING_PORT:-7276}` on the host to `7276` in the container.
    - **Healthcheck**: Ensures the Graph Clustering service is operational.
    - **Networks**: `r2r-network`

12. **R2R (`r2r`)**

    - **Image**: `${R2R_IMAGE:-ragtoriches/prod:latest}`
    - **Build Context**: Current directory (`.`)
    - **Environment Variables**:
      - General R2R settings (`R2R_PORT`, `R2R_HOST`, etc.).
      - PostgreSQL connection details.
      - API keys for external services (OpenAI, Anthropic, Azure, etc.).
      - Hatchet and Graph Clustering settings.
    - **Command**: Sets the Hatchet API token and starts the R2R application using Uvicorn.
    - **Healthcheck**: Ensures the R2R application is operational.
    - **Restart Policy**: `on-failure`
    - **Volumes**:
      - `${R2R_CONFIG_PATH:-/}`: Configuration directory.
      - `hatchet_api_key`: Read-only access to the Hatchet API key.
    - **Extra Hosts**: Adds `host.docker.internal` to facilitate communication with host services.
    - **Depends On**:
      - `setup-token`
      - `unstructured`
    - **Networks**: `r2r-network`

13. **R2R Dashboard (`r2r-dashboard`)**

    - **Image**: `emrgntcmplxty/r2r-dashboard:latest`
    - **Environment Variables**:
      - `NEXT_PUBLIC_R2R_DEPLOYMENT_URL`: URL to the R2R API.
      - `NEXT_PUBLIC_HATCHET_DASHBOARD_URL`: URL to the Hatchet Dashboard.
    - **Ports**: Maps `${R2R_DASHBOARD_PORT:-7273}` on the host to `3000` in the container.
    - **Networks**: `r2r-network`

14. **Nginx (`nginx`)**

    - **Image**: `nginx:latest`
    - **Purpose**: Acts as a reverse proxy to route traffic to R2R and other services.
    - **Ports**: Maps `${R2R_NGINX_PORT:-7280}` on the host to `80` in the container.
    - **Volumes**: Mounts `nginx.conf` from the host to the container.
    - **Depends On**: `r2r`
    - **Deploy Resources**:
      - Limits CPU to `0.5`
      - Limits memory to `512M`
    - **Healthcheck**: Ensures Nginx is operational.
    - **Networks**: `r2r-network`

> **Note**: Ensure that `nginx.conf` is properly configured to proxy requests to the appropriate services.

---