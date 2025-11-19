## Indices

### Overview

An **Index** in R2R represents a vector index structure optimized for similarity search operations across chunks or entities. Indices are crucial for efficient retrieval in Retrieval-Augmented Generation (RAG) applications, supporting various similarity measures and index types tailored to different use cases.

### Core Features of Indices

1. **Fast Similarity Search**
    - Enables rapid retrieval of similar vectors based on specified measures.

2. **Multiple Index Methods**
    - Supports various indexing methods like Hierarchical Navigable Small World (HNSW) and Inverted File (IVF-Flat) for different performance and recall needs.

3. **Configurable Similarity Measures**
    - Allows selection of similarity measures such as cosine distance, L2 distance, and inner product distance.

4. **Concurrent Index Building**
    - Supports concurrent operations to prevent downtime during index construction.

5. **Performance Optimization**
    - Tailors indices for optimized vector operations and query performance.

### Available Endpoints

| Method | Endpoint            | Description                               |
| :---- | :------------------ | :---------------------------------------- |
| POST   | `/indices`          | Create a new vector index                 |
| GET    | `/indices`          | List available indices with pagination    |
| GET    | `/indices/{id}`     | Get details of a specific index           |
| PUT    | `/indices/{id}`     | Update an existing index’s configuration  |
| DELETE | `/indices/{id}`     | Delete an existing index                  |
| GET    | `/indices/{table_name}/{index_name}` | Get vector index details  |
| DELETE | `/indices/{table_name}/{index_name}` | Delete a vector index      |

### Endpoint Details

#### 1. List Vector Indices

```http
GET /v3/indices
```

**Description:**
Lists existing vector similarity search indices with pagination support. Returns details about each index including name, table name, indexing method, parameters, size, and performance statistics.

**Query Parameters:**

| Parameter | Type      | Required | Description                                       |
| :-------- | :-------- | :------ | :------------------------------------------------ |
| `filters` | `string` | No      | Filter based on table name, index method, etc.    |
| `offset`  | `integer`| No      | Number of indices to skip. Defaults to `0`.        |
| `limit`   | `integer`| No      | Number of indices to return (`1–100`). Defaults to `100`. |

**Successful Response:**

```json
{
  "results": {
    "indices": [
      {
        "id": "index_id",
        "name": "ai_research_vectors",
        "table_name": "vectors",
        "index_method": "HNSW",
        "index_measure": "cosine_distance",
        "index_arguments": {
          "m": 16,
          "ef_construction": 200,
          "ef": 50
        },
        "status": "active",
        "size_in_bytes": 500000000,
        "row_count": 100000,
        "created_at": "2024-01-15T09:30:00Z",
        "updated_at": "2024-01-15T09:30:00Z",
        "performance_statistics": {
          "average_query_time_ms": 5,
          "memory_usage_mb": 250,
          "cache_hit_rate_percent": 90
        }
      }
    ]
  },
  "total_entries": 1
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X GET "https://api.example.com/v3/indices?limit=10" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---

#### 2. Create Vector Index

```http
POST /v3/indices
```

**Description:**
Creates a new vector similarity search index over the target table. Supported tables include `vectors`, `entity`, `document_collections`, etc. This process is resource-intensive and supports concurrent building to prevent downtime.

**Supported Index Methods:**

1. **HNSW (Hierarchical Navigable Small World)**
    - **Best for:** High-dimensional vectors requiring fast approximate nearest neighbor search.
    - **Pros:** Very fast search, good recall, memory-resident for speed.
    - **Cons:** Slower index construction, higher memory usage.
    - **Key Parameters:**
        - `m`: Number of connections per layer (higher = better recall but more memory).
        - `ef_construction`: Build-time search width (higher = better recall but slower build).
        - `ef`: Query-time search width (higher = better recall but slower search).

2. **IVF-Flat (Inverted File with Flat Storage)**
    - **Best for:** Balance between build speed, search speed, and recall.
    - **Pros:** Faster index construction, less memory usage.
    - **Cons:** Slightly slower search than HNSW.
    - **Key Parameters:**
        - `lists`: Number of clusters (usually sqrt(n) where n is number of vectors).
        - `probe`: Number of nearest clusters to search.

**Supported Similarity Measures:**

- `cosine_distance`: Best for comparing semantic similarity.
- `l2_distance`: Best for comparing absolute distances.
- `ip_distance`: Best for comparing raw dot products.

**Notes:**

- Index creation can be resource-intensive for large datasets.
- Use `run_with_orchestration=true` for large indices to prevent timeouts.
- The `concurrently` option allows other operations while building.
- Index names must be unique per table.

**Request Body:**

A JSON object containing the configuration for the index.

**Example Request Body:**

```json
{
  "config": {
    "name": "ai_research_vectors",
    "table_name": "vectors",
    "index_method": "HNSW",
    "index_measure": "cosine_distance",
    "index_arguments": {
      "m": 16,
      "ef_construction": 200,
      "ef": 50
    },
    "concurrently": true,
    "run_with_orchestration": true
  }
}
```

**Successful Response:**

```json
{
  "results": {
    "message": "Index creation started."
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X POST "https://api.example.com/v3/indices" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "config": {
             "name": "ai_research_vectors",
             "table_name": "vectors",
             "index_method": "HNSW",
             "index_measure": "cosine_distance",
             "index_arguments": {
               "m": 16,
               "ef_construction": 200,
               "ef": 50
             },
             "concurrently": true,
             "run_with_orchestration": true
           }
         }'
```

---

#### 3. Get Vector Index Details

```http
GET /v3/indices/:table_name/:index_name
```

**Description:**
Retrieves detailed information about a specific vector index, including its configuration, size, performance statistics, and maintenance information.

**Path Parameters:**

| Parameter    | Type   | Required | Description                                     |
| :----------: | :---- | :------ | :---------------------------------------------- |
| `table_name` | `string` | Yes      | The table of vector embeddings (`vectors`, `entity`, `document_collections`). |
| `index_name` | `string` | Yes      | The name of the index to retrieve details for.   |

**Successful Response:**

```json
{
  "results": {
    "configuration": {
      "method": "HNSW",
      "measure": "cosine_distance",
      "parameters": {
        "m": 16,
        "ef_construction": 200,
        "ef": 50
      }
    },
    "size_in_bytes": 500000000,
    "row_count": 100000,
    "build_progress": "Completed",
    "performance_statistics": {
      "average_query_time_ms": 5,
      "memory_usage_mb": 250,
      "cache_hit_rate_percent": 90,
      "recent_query_patterns": ["nearest neighbor", "range search"]
    },
    "maintenance_information": {
      "last_vacuum": "2024-02-01T10:00:00Z",
      "fragmentation_level": "Low",
      "recommended_optimizations": ["Increase ef parameter for better recall."]
    }
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X GET "https://api.example.com/v3/indices/vectors/ai_research_vectors" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---

#### 4. Delete Vector Index

```http
DELETE /v3/indices/:table_name/:index_name
```

**Description:**
Deletes an existing vector similarity search index. Deletion is permanent and cannot be undone. Underlying vector data remains intact, but queries will fall back to sequential scan, potentially slowing down search operations.

**Notes:**

- Deletion may affect dependent operations; ensure index dependencies are managed before deletion.
- Use `run_with_orchestration=true` for large indices to prevent timeouts.

**Path Parameters:**

| Parameter    | Type   | Required | Description                                     |
| :----------: | :---- | :------ | :---------------------------------------------- |
| `table_name` | `string` | Yes      | The table of vector embeddings (`vectors`, `entity`, `document_collections`). |
| `index_name` | `string` | Yes      | The name of the index to delete.                |

**Successful Response:**

```json
{
  "results": {
    "message": "Index deletion initiated."
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X DELETE "https://api.example.com/v3/indices/vectors/ai_research_vectors" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---