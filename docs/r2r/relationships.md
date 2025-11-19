## Relationships

### Overview

**Relationships** define the connections between **Entities** within a graph, establishing how different entities relate to one another. They are pivotal for understanding the structure and interconnections within your knowledge graph, enabling complex queries and insights.

### Core Features of Relationships

1. **Connection Building**
    - Links between entities to represent interactions, hierarchies, or associations.

2. **Metadata and Weighting**
    - Stores additional information and weightings to signify the strength or importance of the relationship.

3. **Semantic Navigation**
    - Facilitates multi-hop traversal and semantic queries within the graph.

### Available Endpoints

| Method | Endpoint                                      | Description                                    |
| :---- | :-------------------------------------------- | :--------------------------------------------- |
| GET    | `/graphs/{collection_id}/relationships`       | List relationships                            |
| POST   | `/graphs/{collection_id}/relationships`       | Create relationship                           |
| GET    | `/graphs/{collection_id}/relationships/{relationship_id}` | Get relationship                  |
| POST   | `/graphs/{collection_id}/relationships/{relationship_id}` | Update relationship           |
| DELETE | `/graphs/{collection_id}/relationships/{relationship_id}` | Delete relationship           |

### Endpoint Details

#### 1. List Relationships

```http
GET /v3/graphs/:collection_id/relationships
```

**Description:**
Lists all relationships within a specific graph, supporting pagination.

**Path Parameters:**

| Parameter      | Type   | Required | Description                        |
| :------------- | :----- | :------ | :--------------------------------- |
| `collection_id`| `string` | Yes      | The Collection ID associated with the graph. |

**Query Parameters:**

| Parameter | Type      | Required | Description                    |
| :-------- | :-------- | :------ | :----------------------------- |
| `offset`  | `integer` | No      | Number of relationships to skip. Defaults to `0`. |
| `limit`   | `integer` | No      | Number of relationships to return (`1–100`). Defaults to `100`. |

**Successful Response:**

```json
{
  "results": [
    {
      "subject": "John Doe",
      "predicate": "WorksAt",
      "object": "OpenAI",
      "id": "relationship_id",
      "description": "John Doe works at OpenAI.",
      "subject_id": "entity_id1",
      "object_id": "entity_id2",
      "weight": 1.1,
      "chunk_ids": ["chunk_id1", "chunk_id2"],
      "parent_id": "parent_relationship_id",
      "description_embedding": [1.1, 2.2, 3.3],
      "metadata": { "department": "Research" }
    }
  ],
  "total_entries": 1
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X GET "https://api.example.com/v3/graphs/collection_id/relationships?limit=10" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---

#### 2. Create Relationship

```http
POST /v3/graphs/:collection_id/relationships
```

**Description:**
Creates a new relationship within a specified graph, linking two entities.

**Path Parameters:**

| Parameter      | Type   | Required | Description                        |
| :------------- | :----- | :------ | :--------------------------------- |
| `collection_id`| `string` | Yes      | The Collection ID associated with the graph. |

**Request Body:**

A JSON object containing the details of the relationship to be created.

**Example Request Body:**

```json
{
  "subject": "John Doe",
  "subject_id": "entity_id1",
  "predicate": "WorksAt",
  "object": "OpenAI",
  "object_id": "entity_id2",
  "description": "John Doe works at OpenAI.",
  "weight": 1.1,
  "metadata": {
    "department": "Research"
  }
}
```

**Successful Response:**

```json
{
  "results": {
    "subject": "John Doe",
    "predicate": "WorksAt",
    "object": "OpenAI",
    "id": "relationship_id",
    "description": "John Doe works at OpenAI.",
    "subject_id": "entity_id1",
    "object_id": "entity_id2",
    "weight": 1.1,
    "chunk_ids": ["chunk_id1", "chunk_id2"],
    "parent_id": "parent_relationship_id",
    "description_embedding": [1.1, 2.2, 3.3],
    "metadata": {
      "department": "Research"
    }
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X POST "https://api.example.com/v3/graphs/collection_id/relationships" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "subject": "John Doe",
           "subject_id": "entity_id1",
           "predicate": "WorksAt",
           "object": "OpenAI",
           "object_id": "entity_id2",
           "description": "John Doe works at OpenAI.",
           "weight": 1.1,
           "metadata": { "department": "Research" }
         }'
```

---

#### 3. Get Relationship

```http
GET /v3/graphs/:collection_id/relationships/:relationship_id
```

**Description:**
Retrieves detailed information about a specific relationship within a graph.

**Path Parameters:**

| Parameter          | Type   | Required | Description                                |
| :----------------- | :----- | :------ | :----------------------------------------- |
| `collection_id`    | `string` | Yes      | The Collection ID associated with the graph. |
| `relationship_id`  | `string` | Yes      | The Relationship ID to retrieve.           |

**Successful Response:**

```json
{
  "results": {
    "subject": "John Doe",
    "predicate": "WorksAt",
    "object": "OpenAI",
    "id": "relationship_id",
    "description": "John Doe works at OpenAI.",
    "subject_id": "entity_id1",
    "object_id": "entity_id2",
    "weight": 1.1,
    "chunk_ids": ["chunk_id1", "chunk_id2"],
    "parent_id": "parent_relationship_id",
    "description_embedding": [1.1, 2.2, 3.3],
    "metadata": {
      "department": "Research"
    }
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X GET "https://api.example.com/v3/graphs/collection_id/relationships/relationship_id" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---

#### 4. Update Relationship

```http
POST /v3/graphs/:collection_id/relationships/:relationship_id
```

**Description:**
Updates the details of an existing relationship within a graph.

**Path Parameters:**

| Parameter          | Type   | Required | Description                                |
| :----------------- | :----- | :------ | :----------------------------------------- |
| `collection_id`    | `string` | Yes      | The Collection ID associated with the graph. |
| `relationship_id`  | `string` | Yes      | The Relationship ID to update.             |

**Request Body:**

A JSON object containing the updated details of the relationship.

**Example Request Body:**

```json
{
  "subject": "Jane Doe",
  "subject_id": "entity_id3",
  "predicate": "CollaboratesWith",
  "object": "OpenAI Research",
  "object_id": "entity_id4",
  "description": "Jane Doe collaborates with OpenAI Research.",
  "weight": 2.0,
  "metadata": {
    "project": "AI Development"
  }
}
```

**Successful Response:**

```json
{
  "results": {
    "subject": "Jane Doe",
    "predicate": "CollaboratesWith",
    "object": "OpenAI Research",
    "id": "relationship_id",
    "description": "Jane Doe collaborates with OpenAI Research.",
    "subject_id": "entity_id3",
    "object_id": "entity_id4",
    "weight": 2.0,
    "chunk_ids": ["chunk_id3", "chunk_id4"],
    "parent_id": "parent_relationship_id",
    "description_embedding": [2.2, 4.4, 6.6],
    "metadata": {
      "project": "AI Development"
    }
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X POST "https://api.example.com/v3/graphs/collection_id/relationships/relationship_id" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "subject": "Jane Doe",
           "subject_id": "entity_id3",
           "predicate": "CollaboratesWith",
           "object": "OpenAI Research",
           "object_id": "entity_id4",
           "description": "Jane Doe collaborates with OpenAI Research.",
           "weight": 2.0,
           "metadata": { "project": "AI Development" }
         }'
```

---

#### 5. Delete Relationship

```http
DELETE /v3/graphs/:collection_id/relationships/:relationship_id
```

**Description:**
Deletes a specific relationship from the graph.

**Path Parameters:**

| Parameter          | Type   | Required | Description                                |
| :----------------- | :----- | :------ | :----------------------------------------- |
| `collection_id`    | `string` | Yes      | The Collection ID associated with the graph. |
| `relationship_id`  | `string` | Yes      | The Relationship ID to delete.             |

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
curl -X DELETE "https://api.example.com/v3/graphs/collection_id/relationships/relationship_id" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---