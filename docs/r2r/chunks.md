## Chunks

### Overview

A **Chunk** in R2R represents a processed segment of text derived from a parent Document. Chunks are optimized for semantic retrieval, knowledge graph construction, and vector-based operations. Each chunk contains text content, metadata, and optional vector embeddings, facilitating efficient search and analysis.

### Core Features of Chunks

1. **Semantic Retrieval & Search**
    - Enables semantic similarity searches across document contents.
    - Supports vector-based retrieval methods.

2. **Knowledge Graph Integration**
    - Serves as the basis for extracting and linking Entities and Relationships.
    - Facilitates retrieval-augmented generation (RAG) operations.

3. **Metadata Management**
    - Stores additional information and custom fields for enhanced filtering and organization.

### Available Endpoints

| Method | Endpoint                     | Description                                                           |
| :---- | :--------------------------- | :-------------------------------------------------------------------- |
| GET    | `/chunks`                   | List chunks with pagination and filtering options                     |
| POST   | `/chunks/search`            | Perform semantic search across chunks with complex filtering          |
| GET    | `/chunks/{id}`              | Retrieve a specific chunk by ID                                       |
| POST   | `/chunks/{id}`              | Update an existing chunk’s content or metadata                        |
| DELETE | `/chunks/{id}`              | Delete a specific chunk                                               |

### Endpoint Details

#### 1. List Chunks

```http
GET /v3/chunks
```

**Description:**
Lists chunks with pagination, optionally filtering by metadata or including vectors.

**Query Parameters:**

| Parameter         | Type      | Required | Description                                      |
| :---------------- | :-------- | :------ | :----------------------------------------------- |
| `metadata_filter`  | `string` | No      | Filter chunks based on metadata fields.          |
| `include_vectors`  | `boolean`| No      | Include vector embeddings in the response (`true` or `false`). |
| `offset`           | `integer`| No      | Number of chunks to skip. Defaults to `0`.        |
| `limit`            | `integer`| No      | Number of chunks to return (`1–100`). Defaults to `100`. |

**Successful Response:**

```json
{
  "results": [
    {
      "id": "id",
      "document_id": "document_id",
      "owner_id": "owner_id",
      "collection_ids": ["collection_ids"],
      "text": "text",
      "metadata": { "key": "value" },
      "vector": [1.1, 2.2, 3.3]
    }
  ],
  "total_entries": 1
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X GET "https://api.example.com/v3/chunks?limit=10&include_vectors=true" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---

#### 2. Search Chunks

```http
POST /v3/chunks/search
```

**Description:**
Performs a semantic search query over all stored chunks. This endpoint allows for complex filtering of search results using PostgreSQL-based queries, supporting various operators and advanced search configurations.

**Allowed Operators:**

- `eq`: Equals
- `neq`: Not equals
- `gt`: Greater than
- `gte`: Greater than or equal
- `lt`: Less than
- `lte`: Less than or equal
- `like`: Pattern matching
- `ilike`: Case-insensitive pattern matching
- `in`: In list
- `nin`: Not in list

**Request Body:**

A JSON object containing the search query and optional search settings.

**Example Request Body:**

```json
{
  "query": "Find documents related to machine learning",
  "search_settings": {
    "use_semantic_search": true,
    "filters": {
      "document_type": { "$eq": "pdf" }
    },
    "limit": 20
  }
}
```

**Successful Response:**

```json
{
  "results": [
    {
      "id": "chunk-id",
      "document_id": "document_id",
      "collection_ids": ["collection_id1", "collection_id2"],
      "score": 0.95,
      "text": "Relevant chunk text.",
      "metadata": { "title": "example.pdf" },
      "owner_id": "owner_id"
    }
  ]
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X POST "https://api.example.com/v3/chunks/search" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "query": "machine learning",
           "search_settings": {
             "use_semantic_search": true,
             "filters": { "document_type": { "$eq": "pdf" } },
             "limit": 10
           }
         }'
```

---

#### 3. Retrieve a Chunk

```http
GET /v3/chunks/:id
```

**Description:**
Retrieves a specific chunk by its ID, including its content, metadata, and associated document/collection information.

**Path Parameters:**

| Parameter | Type   | Required | Description           |
| :-------- | :----- | :------ | :-------------------- |
| `id`      | `string` | Yes      | The Chunk ID to retrieve. |

**Successful Response:**

```json
{
  "results": {
    "id": "chunk-id",
    "document_id": "document-id",
    "owner_id": "owner-id",
    "collection_ids": ["collection-id"],
    "text": "Chunk content",
    "metadata": { "key": "value" },
    "vector": [1.1, 2.2, 3.3]
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X GET "https://api.example.com/v3/chunks/chunk_id" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---

#### 4. Update Chunk

```http
POST /v3/chunks/:id
```

**Description:**
Updates an existing chunk’s content and/or metadata. Upon updating, the chunk’s vectors are automatically recomputed based on the new content.

**Path Parameters:**

| Parameter | Type   | Required | Description           |
| :-------- | :----- | :------ | :-------------------- |
| `id`      | `string` | Yes      | The Chunk ID to update. |

**Request Body:**

A JSON object containing the updated chunk details.

**Example Request Body:**

```json
{
  "id": "chunk-id",
  "text": "Updated chunk content.",
  "metadata": { "newKey": "newValue" }
}
```

**Successful Response:**

```json
{
  "results": {
    "id": "chunk-id",
    "document_id": "document-id",
    "owner_id": "owner-id",
    "collection_ids": ["collection-id"],
    "text": "Updated chunk content.",
    "metadata": { "newKey": "newValue" },
    "vector": [4.4, 5.5, 6.6]
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X POST "https://api.example.com/v3/chunks/chunk_id" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "id": "chunk_id",
           "text": "Updated chunk content.",
           "metadata": { "newKey": "newValue" }
         }'
```

---

#### 5. Delete Chunk

```http
DELETE /v3/chunks/:id
```

**Description:**
Deletes a specific chunk by its ID. The parent document remains intact.

**Path Parameters:**

| Parameter | Type   | Required | Description           |
| :-------- | :----- | :------ | :-------------------- |
| `id`      | `string` | Yes      | The Chunk ID to delete. |

**Successful Response:**

```json
{
  "results": {
    "success": true
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X DELETE "https://api.example.com/v3/chunks/chunk_id" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---