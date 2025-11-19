## **Maintenance and Scaling**

### **Vector Indices**

**Do You Need Vector Indices?**

Vector indices enhance search capabilities but are not necessary for all deployments, especially in multi-user environments with user-specific filtering.

**When to Implement Vector Indices:**

- Large-scale searches across hundreds of thousands of documents.
- When query latency becomes a bottleneck.
- Supporting cross-user search functionalities.

**Vector Index Management:**

R2R supports various indexing methods, with HNSW (Hierarchical Navigable Small World) recommended for most use cases.

**Example: Creating and Deleting a Vector Index**

```python
from r2r import R2RClient

client = R2RClient()

# Create vector index
create_response = client.indices.create(
    {
        "table_name": "vectors",
        "index_method": "hnsw",
        "index_measure": "cosine_distance",
        "index_arguments": {
            "m": 16,
            "ef_construction": 64
        },
    }
)

# List existing indices
indices = client.indices.list()

# Delete an index
delete_response = client.indices.delete(
    index_name="ix_vector_cosine_ops_hnsw__20241021211541",
    table_name="vectors",
)

print('delete_response = ', delete_response)
```

**Important Considerations:**

1. **Pre-warming**: New indices start "cold" and require warming for optimal performance.
2. **Resource Usage**: Index creation is CPU and memory-intensive. Perform during off-peak hours.
3. **Performance Tuning**:
   - **HNSW Parameters**:
     - `m`: 16-64 (higher = better quality, more memory)
     - `ef_construction`: 64-100 (higher = better quality, longer build time)
   - **Distance Measures**:
     - `cosine_distance`: Best for normalized vectors.
     - `l2_distance`: Better for absolute distances.
     - `max_inner_product`: Optimized for dot product similarity.

### **System Updates and Maintenance**

**Version Management**

Check the current R2R version:

```bash
docker-compose -f compose.full_with_replicas.yaml exec r2r r2r version
```

**Update Process**

1. **Prepare for Update**

   ```bash
   docker-compose -f compose.full_with_replicas.yaml exec r2r r2r version
   docker-compose -f compose.full_with_replicas.yaml exec r2r r2r db current
   docker-compose -f compose.full_with_replicas.yaml exec r2r r2r generate-report
   ```

2. **Stop Running Services**

   ```bash
   docker-compose -f compose.full_with_replicas.yaml down
   ```

3. **Update R2R**

   ```bash
   docker-compose -f compose.full_with_replicas.yaml pull
   docker-compose -f compose.full_with_replicas.yaml up -d --build
   ```

4. **Update Database**

   ```bash
   docker-compose -f compose.full_with_replicas.yaml exec r2r r2r db upgrade
   ```

5. **Restart Services**

   ```bash
   docker-compose -f compose.full_with_replicas.yaml up -d
   ```

**Database Migration Management**

Check current migration:

```bash
docker-compose -f compose.full_with_replicas.yaml exec r2r r2r db current
```

Apply migrations:

```bash
docker-compose -f compose.full_with_replicas.yaml exec r2r r2r db upgrade
```

Rollback if necessary:

```bash
docker-compose -f compose.full_with_replicas.yaml exec r2r r2r db downgrade --revision <previous-working-version>
```

### **Managing Multiple Environments**

Use different project names and schemas for development, staging, and production environments.

**Example:**

```bash
# Development
export R2R_PROJECT_NAME=r2r_dev
docker-compose -f compose.full_with_replicas.yaml up -d

# Staging
export R2R_PROJECT_NAME=r2r_staging
docker-compose -f compose.full_with_replicas.yaml up -d

# Production
export R2R_PROJECT_NAME=r2r_prod
docker-compose -f compose.full_with_replicas.yaml up -d
```

---