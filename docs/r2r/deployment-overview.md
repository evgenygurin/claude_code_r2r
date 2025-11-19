## **Deployment Overview**

The deployment consists of the following key components:

1. **PostgreSQL with pgvector**: Database for storing relational and vector data.
2. **Hatchet Services**: Includes Hatchet Postgres, RabbitMQ, Migration, Setup Config, Engine, and Dashboard.
3. **Unstructured Service**: Handles document processing and parsing.
4. **Graph Clustering Service**: Manages community detection within knowledge graphs.
5. **R2R Application**: The core application providing Retrieval-Augmented Generation (RAG) functionalities.
6. **R2R Dashboard**: User interface for managing R2R.
7. **Nginx**: Acts as a reverse proxy to route traffic to R2R and other services.

The deployment is managed using Docker Compose, orchestrating the interaction between these services.

---