## **Building and Running the Deployment**

### **Step 1: Clone the Repository**

First, clone the R2R repository containing all necessary deployment files.

```bash
git clone https://github.com/SciPhi-AI/r2r.git
cd r2r
```

> **Note**: Replace the repository URL with the actual URL if different.

### **Step 2: Configure Environment Variables**

Ensure that all necessary environment variables are set. You can use the `.env` file method described earlier.

```bash
cp .env.example .env
# Edit the .env file with your specific configurations
nano .env
```

> **Tip**: Use a text editor of your choice (e.g., `vim`, `nano`) to edit the `.env` file.

### **Step 3: Build Docker Images**

Build the Docker images using the provided `Dockerfile` and `Dockerfile.unstructured`.

```bash
# Build the R2R application image
docker build -t r2r-app -f Dockerfile .

# Build the Unstructured service image
docker build -t unstructured-service -f Dockerfile.unstructured .
```

> **Note**: Ensure Docker is running before executing these commands. The build process may take several minutes.

### **Step 4: Deploy Services with Docker Compose**

Use Docker Compose to deploy all services as defined in `compose.full_with_replicas.yaml`.

```bash
docker-compose -f compose.full_with_replicas.yaml up -d
```

> **Flags Explained**:
> - `-f compose.full_with_replicas.yaml`: Specifies the Docker Compose file to use.
> - `up`: Builds, (re)creates, starts, and attaches to containers for a service.
> - `-d`: Runs containers in the background (detached mode).

> **Monitoring Deployment**:
> You can monitor the status of your services using:
> ```bash
> docker-compose -f compose.full_with_replicas.yaml ps
> ```

---