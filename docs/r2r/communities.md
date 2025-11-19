## Communities

### Overview

**Communities** are clusters of related **Entities** within a graph, representing groupings of interconnected information. They are generated through clustering algorithms and can be manually managed to reflect domain-specific knowledge structures.

### Core Features of Communities

1. **Automatic Generation**
    - Built using clustering algorithms based on entity relationships and similarities.

2. **Manual Management**
    - Allows manual creation, editing, and deletion of communities to reflect specific organizational needs.

3. **Hierarchical Organization**
    - Supports hierarchical structures, enabling nested communities for detailed knowledge organization.

4. **Metadata Integration**
    - Stores metadata and descriptions for each community, facilitating better understanding and navigation.

### Available Endpoints

| Method | Endpoint                                      | Description                                         |
| :---- | :-------------------------------------------- | :-------------------------------------------------- |
| POST   | `/graphs/{collection_id}/communities/build`   | Build communities from existing graph data          |
| GET    | `/graphs/{collection_id}/communities`         | List communities                                    |
| POST   | `/graphs/{collection_id}/communities`         | Create community                                    |
| GET    | `/graphs/{collection_id}/communities/{community_id}` | Get community                             |
| POST   | `/graphs/{collection_id}/communities/{community_id}` | Update community                        |
| DELETE | `/graphs/{collection_id}/communities/{community_id}` | Delete community                        |

### Endpoint Details

#### 1. Build Communities

```http
POST /v3/graphs/:collection_id/communities/build
```

**Description:**
Builds communities within the graph by analyzing entity relationships and similarities. This process utilizes clustering algorithms to identify and group related entities.

**Path Parameters:**

| Parameter      | Type   | Required | Description                        |
| :------------- | :----- | :------ | :--------------------------------- |
| `collection_id`| `string` | Yes      | The Collection ID associated with the graph. |

**Request Body:**

A JSON object containing settings for the community building process.

**Example Request Body:**

```json
{
  "run_type": "run",
  "graph_enrichment_settings": {
    "algorithm": "Leiden",
    "parameters": {
      "resolution": 1.0
    }
  },
  "run_with_orchestration": true
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
curl -X POST "https://api.example.com/v3/graphs/collection_id/communities/build" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "run_type": "run",
           "graph_enrichment_settings": { "algorithm": "Leiden", "parameters": { "resolution": 1.0 } },
           "run_with_orchestration": true
         }'
```

---

#### 2. List Communities

```http
GET /v3/graphs/:collection_id/communities
```

**Description:**
Lists all communities within a specific graph, supporting pagination.

**Path Parameters:**

| Parameter      | Type   | Required | Description                        |
| :------------- | :----- | :------ | :--------------------------------- |
| `collection_id`| `string` | Yes      | The Collection ID associated with the graph. |

**Query Parameters:**

| Parameter | Type      | Required | Description                    |
| :-------- | :-------- | :------ | :----------------------------- |
| `offset`  | `integer` | No      | Number of communities to skip. Defaults to `0`. |
| `limit`   | `integer` | No      | Number of communities to return (`1–100`). Defaults to `100`. |

**Successful Response:**

```json
{
  "results": [
    {
      "name": "AI Researchers",
      "summary": "Community of AI researchers focused on machine learning.",
      "level": 1,
      "findings": ["Research papers", "Collaborative projects"],
      "id": 1,
      "community_id": "community_id",
      "collection_id": "collection_id",
      "rating": 9.5,
      "rating_explanation": "High engagement and output.",
      "description_embedding": [2.2, 4.4, 6.6],
      "attributes": { "key": "value" },
      "created_at": "2024-01-15T09:30:00Z",
      "updated_at": "2024-01-15T09:30:00Z"
    }
  ],
  "total_entries": 1
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X GET "https://api.example.com/v3/graphs/collection_id/communities?limit=10" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---

#### 3. Create Community

```http
POST /v3/graphs/:collection_id/communities
```

**Description:**
Creates a new community within a graph. While communities are typically built automatically via the `/communities/build` endpoint, this endpoint allows for manual creation to reflect specific organizational needs.

**Path Parameters:**

| Parameter      | Type   | Required | Description                        |
| :------------- | :----- | :------ | :--------------------------------- |
| `collection_id`| `string` | Yes      | The Collection ID associated with the graph. |

**Request Body:**

A JSON object containing the details of the community to be created.

**Example Request Body:**

```json
{
  "name": "AI Researchers",
  "summary": "Community of AI researchers focused on machine learning.",
  "findings": ["Research papers", "Collaborative projects"],
  "rating": 9.5,
  "rating_explanation": "High engagement and output."
}
```

**Successful Response:**

```json
{
  "results": {
    "name": "AI Researchers",
    "summary": "Community of AI researchers focused on machine learning.",
    "level": 1,
    "findings": ["Research papers", "Collaborative projects"],
    "id": 1,
    "community_id": "community_id",
    "collection_id": "collection_id",
    "rating": 9.5,
    "rating_explanation": "High engagement and output.",
    "description_embedding": [2.2, 4.4, 6.6],
    "attributes": { "key": "value" },
    "created_at": "2024-01-15T09:30:00Z",
    "updated_at": "2024-01-15T09:30:00Z"
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X POST "https://api.example.com/v3/graphs/collection_id/communities" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "name": "AI Researchers",
           "summary": "Community of AI researchers focused on machine learning.",
           "findings": ["Research papers", "Collaborative projects"],
           "rating": 9.5,
           "rating_explanation": "High engagement and output."
         }'
```

---

#### 4. Get Community

```http
GET /v3/graphs/:collection_id/communities/:community_id
```

**Description:**
Retrieves detailed information about a specific community within a graph.

**Path Parameters:**

| Parameter      | Type   | Required | Description                                |
| :------------- | :----- | :------ | :----------------------------------------- |
| `collection_id`| `string` | Yes      | The Collection ID associated with the graph. |
| `community_id` | `string` | Yes      | The Community ID to retrieve.              |

**Successful Response:**

```json
{
  "results": {
    "name": "AI Researchers",
    "summary": "Community of AI researchers focused on machine learning.",
    "level": 1,
    "findings": ["Research papers", "Collaborative projects"],
    "id": 1,
    "community_id": "community_id",
    "collection_id": "collection_id",
    "rating": 9.5,
    "rating_explanation": "High engagement and output.",
    "description_embedding": [2.2, 4.4, 6.6],
    "attributes": { "key": "value" },
    "created_at": "2024-01-15T09:30:00Z",
    "updated_at": "2024-02-20T10:45:00Z"
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X GET "https://api.example.com/v3/graphs/collection_id/communities/community_id" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---

#### 5. Update Community

```http
POST /v3/graphs/:collection_id/communities/:community_id
```

**Description:**
Updates the details of an existing community within a graph.

**Path Parameters:**

| Parameter      | Type   | Required | Description                                |
| :------------- | :----- | :------ | :----------------------------------------- |
| `collection_id`| `string` | Yes      | The Collection ID associated with the graph. |
| `community_id` | `string` | Yes      | The Community ID to update.                |

**Request Body:**

A JSON object containing the updated details of the community.

**Example Request Body:**

```json
{
  "name": "Senior AI Researchers",
  "summary": "Community of senior AI researchers with a focus on deep learning.",
  "findings": ["Advanced research papers", "International collaborations"],
  "rating": 9.8,
  "rating_explanation": "Exceptional contribution and leadership."
}
```

**Successful Response:**

```json
{
  "results": {
    "name": "Senior AI Researchers",
    "summary": "Community of senior AI researchers with a focus on deep learning.",
    "level": 2,
    "findings": ["Advanced research papers", "International collaborations"],
    "id": 1,
    "community_id": "community_id",
    "collection_id": "collection_id",
    "rating": 9.8,
    "rating_explanation": "Exceptional contribution and leadership.",
    "description_embedding": [3.3, 6.6, 9.9],
    "attributes": { "key": "new_value" },
    "created_at": "2024-01-15T09:30:00Z",
    "updated_at": "2024-02-20T10:45:00Z"
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X POST "https://api.example.com/v3/graphs/collection_id/communities/community_id" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "name": "Senior AI Researchers",
           "summary": "Community of senior AI researchers with a focus on deep learning.",
           "findings": ["Advanced research papers", "International collaborations"],
           "rating": 9.8,
           "rating_explanation": "Exceptional contribution and leadership."
         }'
```

---

#### 6. Delete Community

```http
DELETE /v3/graphs/:collection_id/communities/:community_id
```

**Description:**
Deletes a specific community from the graph.

**Path Parameters:**

| Parameter      | Type   | Required | Description                                |
| :------------- | :----- | :------ | :----------------------------------------- |
| `collection_id`| `string` | Yes      | The Collection ID associated with the graph. |
| `community_id` | `string` | Yes      | The Community ID to delete.                |

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
curl -X DELETE "https://api.example.com/v3/graphs/collection_id/communities/community_id" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---