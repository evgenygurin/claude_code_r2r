## Maintenance & Scaling

Effective maintenance and scaling are crucial for ensuring R2R operates optimally, especially as data volumes grow.

### Vector Indices

#### Do You Need Vector Indices?

Vector indices are **not necessary for all deployments**, particularly in multi-user applications where queries are typically filtered by `user_id`, reducing the number of vectors searched.

**Consider implementing vector indices when:**

- Users search across hundreds of thousands of documents.
- Query latency becomes a bottleneck even with user-specific filtering.
- Supporting cross-user search functionality at scale.

For development or smaller deployments, the overhead of maintaining vector indices often outweighs their benefits.

#### Vector Index Management

R2R supports multiple indexing methods, with HNSW (Hierarchical Navigable Small World) being recommended for most use cases.

**Python Example: Creating and Deleting a Vector Index**

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

#### Important Considerations

1. **Pre-warming Requirement**:
   - New indices start “cold” and require warming for optimal performance.
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

### System Updates and Maintenance

#### Version Management

**Check Current R2R Version:**

```bash
r2r version
```

#### Update Process

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

#### Database Migration Management

R2R uses database migrations to manage schema changes.

**Check Current Migration:**

```bash
r2r db current
```

**Apply Migrations:**

```bash
r2r db upgrade
```

### Managing Multiple Environments

Use different project names and schemas for different environments.

**Example:**

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

### Troubleshooting

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

### Scaling Strategies

#### Horizontal Scaling

For applications serving many users:

1. **Load Balancing**
   - Deploy multiple R2R instances behind a load balancer.
   - Each instance handles a subset of users.

2. **Sharding**
   - Shard by `user_id` for large multi-user deployments.
   - Each shard handles a subset of users, maintaining performance with millions of documents.

#### Vertical Scaling

For applications requiring large single-user searches:

1. **Cloud Provider Solutions**
   - **AWS RDS**: Supports up to 1 billion vectors per instance.
   - **Example Instance Types**:
     - `db.r6g.16xlarge`: Suitable for up to 100M vectors.
     - `db.r6g.metal`: Can handle 1B+ vectors.

2. **Memory Optimization**

```python
# Optimize for large vector collections
client.indices.create(
    table_name="vectors",
    index_method="hnsw",
    index_arguments={
        "m": 32,  # Increased for better performance
        "ef_construction": 80  # Balanced for large collections
    }
)
```

#### Multi-User Considerations

1. **Filtering Optimization**

```python
# Efficient per-user search
response = client.retrieval.search(
    "query",
    search_settings={
        "filters": {
            "user_id": {"$eq": "current_user_id"}
        }
    }
)
```

2. **Collection Management**
   - Group related documents into collections.
   - Enable efficient access control.
   - Optimize search scope.

3. **Resource Allocation**
   - Monitor per-user resource usage.
   - Implement usage quotas if needed.
   - Consider dedicated instances for power users.

#### Performance Monitoring

Monitor the following metrics to inform scaling decisions:

1. **Query Performance**
   - Average query latency per user.
   - Number of vectors searched per query.
   - Cache hit rates.

2. **System Resources**
   - Memory usage per instance.
   - CPU utilization.
   - Storage growth rate.

3. **User Patterns**
   - Number of active users.
   - Query patterns and peak usage times.
   - Document count per user.

### Performance Considerations

When configuring embeddings in R2R, consider these optimization strategies:

1. **Batch Size Optimization**:
   - Larger batch sizes improve throughput but increase latency.
   - Consider provider-specific rate limits when setting batch size.
   - Balance memory usage with processing speed.

2. **Concurrent Requests**:
   - Adjust `concurrent_request_limit` based on provider capabilities.
   - Monitor API usage and adjust limits accordingly.
   - Implement local caching for frequently embedded texts.

3. **Model Selection**:
   - Balance embedding dimension size with accuracy requirements.
   - Consider cost per token for different providers.
   - Evaluate multilingual requirements when choosing models.

4. **Resource Management**:
   - Monitor memory usage with large batch sizes.
   - Implement appropriate error handling and retry strategies.
   - Consider implementing local model fallbacks for critical systems.

### Additional Resources

- [Python SDK Ingestion Documentation](https://r2r-docs.sciphi.ai/documentation/python-sdk/ingestion)
- [CLI Maintenance Documentation](https://r2r-docs.sciphi.ai/documentation/cli/maintenance)
- [Ingestion Configuration Documentation](https://r2r-docs.sciphi.ai/documentation/configuration/ingestion)

### Best Practices

1. **Optimize Indexing**: Ensure proper indexing for both full-text and vector searches.
2. **Monitor Resources**: Keep track of CPU, memory, and storage usage.
3. **Regular Maintenance**: Perform regular vacuuming and updates to maintain database performance.
4. **Plan Scaling Ahead**: Anticipate growth and implement scaling strategies proactively.

### Conclusion

Effective maintenance and scaling strategies ensure that R2R remains performant and reliable as your data and user base grow. By optimizing vector indices, managing system updates, and employing robust scaling strategies, you can maintain an efficient and scalable R2R deployment.

---