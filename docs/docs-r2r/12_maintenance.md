# Maintenance & Scaling

Effective maintenance and scaling are crucial for ensuring R2R operates optimally, especially as data volumes grow.

## Vector Indices

### Do You Need Vector Indices?

Vector indices are **not necessary for all deployments**, particularly in multi-user applications where queries are typically filtered by `user_id`, reducing the number of vectors searched.

**Consider implementing vector indices when:**

- Users search across hundreds of thousands of documents.
- Query latency becomes a bottleneck even with user-specific filtering.
- Supporting cross-user search functionality at scale.

For development or smaller deployments, the overhead of maintaining vector indices often outweighs their benefits.

### Vector Index Management

R2R supports multiple indexing methods, with HNSW (Hierarchical Navigable Small World) being recommended for most use cases.

#### Python Example: Creating and Deleting a Vector Index

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
            "m": 16,  # Number of connections per element
            "ef_construction": 64  # Size of dynamic candidate list
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

### Important Considerations

1. **Pre-warming Requirement**:
   - New indices start "cold" and require warming for optimal performance.
   - Initial queries will be slower until the index is loaded into memory.
   - Implement explicit pre-warming in production.
   - Warming must be repeated after system restarts.

2. **Resource Usage**:
   - Index creation is CPU and memory intensive.
   - Memory usage scales with dataset size and the `m` parameter.
   - Create indices during off-peak hours.

3. **Performance Tuning**:
   - **HNSW Parameters**:
     - `m`: 16-64 (higher = better quality, more memory)
     - `ef_construction`: 64-100 (higher = better quality, longer build time)
   - **Distance Measures**:
     - `cosine_distance`: Best for normalized vectors (most common)
     - `l2_distance`: Better for absolute distances
     - `max_inner_product`: Optimized for dot product similarity

## System Updates and Maintenance

### Version Management

**Check Current R2R Version:**

```bash
r2r version
```

### Update Process

1. **Prepare for Update**

```bash
# Check current versions
r2r version
r2r db current

# Generate system report (optional)
r2r generate-report
```

2. **Stop Running Services**

```bash
r2r docker-down
```

3. **Update R2R**

```bash
r2r update
```

4. **Update Database**

```bash
r2r db upgrade
```

5. **Restart Services**

```bash
r2r serve --docker [additional options]
```

### Database Migration Management

R2R uses database migrations to manage schema changes.

#### Check Current Migration

```bash
r2r db current
```

#### Apply Migrations

```bash
r2r db upgrade
```

## Managing Multiple Environments

Use different project names and schemas for different environments.

### Example with Environment Variables

```bash
# Development
export R2R_PROJECT_NAME=r2r_dev
r2r serve --docker --project-name r2r-dev

# Staging
export R2R_PROJECT_NAME=r2r_staging
r2r serve --docker --project-name r2r-staging

# Production
export R2R_PROJECT_NAME=r2r_prod
r2r serve --docker --project-name r2r-prod
```

## Troubleshooting

### Steps

If issues occur:

1. **Generate a System Report**

```bash
r2r generate-report
```

2. **Check Container Health**

```bash
r2r docker-down
r2r serve --docker
```

3. **Review Database State**

```bash
r2r db current
r2r db history
```

4. **Roll Back if Needed**

```bash
r2r db downgrade --revision <previous-working-version>
```

## Scaling Strategies

1. **Horizontal Scaling**
   - Implement load balancing
   - Use sharding for large datasets
   - Distribute processing across nodes

2. **Vertical Scaling**
   - Optimize resource allocation
   - Upgrade hardware as needed
   - Monitor system performance

3. **Performance Optimization**
   - Use appropriate indexing
   - Implement caching strategies
   - Regular maintenance and cleanup
