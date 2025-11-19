## Graphs

### Overview

A **Graph** in R2R is a knowledge graph associated with a specific **Collection**. It comprises **Entities**, **Relationships**, and **Communities** (groupings of related entities). Graphs facilitate the organization and retrieval of interconnected information, enabling advanced data analysis and exploration.

### Core Features of Graphs

1. **Git-like Model**
    - Each Collection has an associated Graph that can diverge independently.
    - The `pull` operation syncs document knowledge into the graph.
    - Changes can be experimental without affecting the base Collection and underlying documents.

2. **Knowledge Organization**
    - Automatic entity and relationship extraction from documents.
    - Community detection for hierarchical knowledge organization.
    - Support for manual creation and editing of entities, relationships, and communities.
    - Rich metadata and property management.

3. **Access Control**
    - Graph operations are tied to Collection permissions.
    - Superuser privileges required for certain operations like community building.
    - Document-level access checks when pulling content.

### Available Endpoints

| Method | Endpoint                                 | Description                                  |
| :---- | :--------------------------------------- | :------------------------------------------- |
| GET    | `/graphs/{collection_id}`                | Get graph details                           |
| POST   | `/graphs/{collection_id}/pull`           | Sync documents with graph                   |
| POST   | `/graphs/{collection_id}/communities/build` | Build graph communities                 |
| POST   | `/graphs/{collection_id}/reset`          | Reset graph to initial state                |
| GET    | `/graphs/{collection_id}/entities`                 | List entities                                |
| POST   | `/graphs/{collection_id}/entities`                 | Create entity                                |
| GET    | `/graphs/{collection_id}/entities/{entity_id}`     | Get entity                                   |
| POST   | `/graphs/{collection_id}/entities/{entity_id}`     | Update entity                                |
| DELETE | `/graphs/{collection_id}/entities/{entity_id}`     | Delete entity                                |
| GET    | `/graphs/{collection_id}/relationships`            | List relationships                           |
| POST   | `/graphs/{collection_id}/relationships`            | Create relationship                          |
| GET    | `/graphs/{collection_id}/relationships/{relationship_id}` | Get relationship                     |
| POST   | `/graphs/{collection_id}/relationships/{relationship_id}` | Update relationship                  |
| DELETE | `/graphs/{collection_id}/relationships/{relationship_id}` | Delete relationship                  |
| GET    | `/graphs/{collection_id}/communities`               | List communities                             |
| POST   | `/graphs/{collection_id}/communities`               | Create community                             |
| GET    | `/graphs/{collection_id}/communities/{community_id}` | Get community                            |
| POST   | `/graphs/{collection_id}/communities/{community_id}` | Update community                       |
| DELETE | `/graphs/{collection_id}/communities/{community_id}` | Delete community                       |

### Endpoint Details

#### 1. List Graphs

```http
GET /v3/graphs
```

**Description:**
Returns a paginated list of graphs accessible to the authenticated user. Filter by `collection_ids` if needed. Regular users see only their own collections' graphs, while superusers see all graphs.

**Query Parameters:**

| Parameter        | Type     | Required | Description                    |
| :--------------- | :------- | :------ | :----------------------------- |
| `collection_ids` | `string` | No      | Comma-separated list of collection IDs to filter graphs. |
| `offset`         | `integer`| No      | Number of graphs to skip. Defaults to `0`. |
| `limit`          | `integer`| No      | Number of graphs to return (`1–100`). Defaults to `100`. |

**Successful Response:**

```json
{
  "results": [
    {
      "id": "id",
      "collection_id": "collection_id",
      "name": "graph_name",
      "status": "status",
      "created_at": "2024-01-15T09:30:00Z",
      "updated_at": "2024-01-15T09:30:00Z",
      "document_ids": ["document_ids"],
      "description": "description"
    }
  ],
  "total_entries": 1
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X GET "https://api.example.com/v3/graphs?limit=10" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---

#### 2. Retrieve Graph Details

```http
GET /v3/graphs/:collection_id
```

**Description:**
Retrieves detailed information about a specific graph associated with a collection.

**Path Parameters:**

| Parameter      | Type   | Required | Description                        |
| :------------- | :----- | :------ | :--------------------------------- |
| `collection_id`| `string` | Yes      | The Collection ID associated with the graph. |

**Successful Response:**

```json
{
  "results": {
    "id": "id",
    "collection_id": "collection_id",
    "name": "name",
    "status": "status",
    "created_at": "2024-01-15T09:30:00Z",
    "updated_at": "2024-01-15T09:30:00Z",
    "document_ids": ["document_ids"],
    "description": "description"
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X GET "https://api.example.com/v3/graphs/collection_id" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---

#### 3. Update Graph

```http
POST /v3/graphs/:collection_id
```

**Description:**
Updates the configuration of a specific graph, including its name and description.

**Path Parameters:**

| Parameter      | Type   | Required | Description                        |
| :------------- | :----- | :------ | :--------------------------------- |
| `collection_id`| `string` | Yes      | The Collection ID associated with the graph. |

**Request Body:**

A JSON object containing the updated graph details.

**Example Request Body:**

```json
{
  "name": "new-name",
  "description": "updated description"
}
```

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
curl -X POST "https://api.example.com/v3/graphs/collection_id" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "name": "new-name",
           "description": "updated description"
         }'
```

---

#### 4. Reset Graph

```http
POST /v3/graphs/:collection_id/reset
```

**Description:**
Resets the graph to its initial state by deleting all associated data. This action does **not** delete the underlying source documents.

**Path Parameters:**

| Parameter      | Type   | Required | Description                        |
| :------------- | :----- | :------ | :--------------------------------- |
| `collection_id`| `string` | Yes      | The Collection ID associated with the graph. |

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
curl -X POST "https://api.example.com/v3/graphs/collection_id/reset" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---

#### 5. Pull Latest Entities to Graph

```http
POST /v3/graphs/:collection_id/pull
```

**Description:**
Synchronizes document entities and relationships into the graph, ensuring the graph reflects the latest document data.

**Path Parameters:**

| Parameter      | Type   | Required | Description                        |
| :------------- | :----- | :------ | :--------------------------------- |
| `collection_id`| `string` | Yes      | The Collection ID associated with the graph. |

**Request Body:**

Optional boolean parameters to control the pull operation.

**Example Request Body:**

```json
{
  "force": true
}
```

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
curl -X POST "https://api.example.com/v3/graphs/collection_id/pull" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -d '{"force": true}'
```

---