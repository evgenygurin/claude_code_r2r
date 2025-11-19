## Entities

### Overview

**Entities** are the fundamental building blocks of a knowledge graph in R2R. They represent distinct concepts, objects, or individuals extracted from documents. Entities are linked through **Relationships**, forming a comprehensive network of interconnected information.

### Core Features of Entities

1. **Extraction & Creation**
    - Automatically extracted from document chunks.
    - Manual creation and editing through API endpoints.

2. **Metadata Management**
    - Stores detailed metadata for each entity.
    - Supports categorization and classification.

3. **Relationship Linking**
    - Connected to other entities via Relationships.
    - Facilitates multi-hop traversal and semantic queries.

### Available Endpoints

| Method | Endpoint                                   | Description                           |
| :---- | :----------------------------------------- | :------------------------------------ |
| GET    | `/graphs/{collection_id}/entities`         | List entities                         |
| POST   | `/graphs/{collection_id}/entities`         | Create entity                         |
| GET    | `/graphs/{collection_id}/entities/{entity_id}` | Get entity                      |
| POST   | `/graphs/{collection_id}/entities/{entity_id}` | Update entity                  |
| DELETE | `/graphs/{collection_id}/entities/{entity_id}` | Delete entity                  |

### Endpoint Details

#### 1. List Entities in a Graph

```http
GET /v3/graphs/:collection_id/entities
```

**Description:**
Lists all entities within a specific graph, supporting pagination.

**Path Parameters:**

| Parameter      | Type   | Required | Description                        |
| :------------- | :----- | :------ | :--------------------------------- |
| `collection_id`| `string` | Yes      | The Collection ID associated with the graph. |

**Query Parameters:**

| Parameter | Type      | Required | Description                    |
| :-------- | :-------- | :------ | :----------------------------- |
| `offset`  | `integer` | No      | Number of entities to skip. Defaults to `0`. |
| `limit`   | `integer` | No      | Number of entities to return (`1–100`). Defaults to `100`. |

**Successful Response:**

```json
{
  "results": [
    {
      "id": "entity_id",
      "name": "Entity Name",
      "description": "Entity Description",
      "category": "Category",
      "metadata": { "key": "value" },
      "description_embedding": [1.2, 3.4, 5.6],
      "chunk_ids": ["chunk_id1", "chunk_id2"],
      "parent_id": "parent_entity_id"
    }
  ],
  "total_entries": 1
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X GET "https://api.example.com/v3/graphs/collection_id/entities?limit=10" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---

#### 2. Create Entity in Graph

```http
POST /v3/graphs/:collection_id/entities
```

**Description:**
Creates a new entity within a specified graph.

**Path Parameters:**

| Parameter      | Type   | Required | Description                        |
| :------------- | :----- | :------ | :--------------------------------- |
| `collection_id`| `string` | Yes      | The Collection ID associated with the graph. |

**Request Body:**

A JSON object containing the details of the entity to be created.

**Example Request Body:**

```json
{
  "name": "John Doe",
  "description": "A software engineer.",
  "category": "Person",
  "metadata": {
    "role": "Developer"
  }
}
```

**Successful Response:**

```json
{
  "results": {
    "id": "entity_id",
    "name": "John Doe",
    "description": "A software engineer.",
    "category": "Person",
    "metadata": {
      "role": "Developer"
    },
    "description_embedding": [1.2, 3.4, 5.6],
    "chunk_ids": ["chunk_id1", "chunk_id2"],
    "parent_id": "parent_entity_id"
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X POST "https://api.example.com/v3/graphs/collection_id/entities" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "name": "John Doe",
           "description": "A software engineer.",
           "category": "Person",
           "metadata": { "role": "Developer" }
         }'
```

---

#### 3. Get Entity

```http
GET /v3/graphs/:collection_id/entities/:entity_id
```

**Description:**
Retrieves detailed information about a specific entity within a graph.

**Path Parameters:**

| Parameter      | Type   | Required | Description                                |
| :------------- | :----- | :------ | :----------------------------------------- |
| `collection_id`| `string` | Yes      | The Collection ID associated with the graph. |
| `entity_id`     | `string` | Yes      | The Entity ID to retrieve.                  |

**Successful Response:**

```json
{
  "results": {
    "id": "entity_id",
    "name": "John Doe",
    "description": "A software engineer.",
    "category": "Person",
    "metadata": {
      "role": "Developer"
    },
    "description_embedding": [1.2, 3.4, 5.6],
    "chunk_ids": ["chunk_id1", "chunk_id2"],
    "parent_id": "parent_entity_id"
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X GET "https://api.example.com/v3/graphs/collection_id/entities/entity_id" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---

#### 4. Update Entity

```http
POST /v3/graphs/:collection_id/entities/:entity_id
```

**Description:**
Updates the details of an existing entity within a graph.

**Path Parameters:**

| Parameter      | Type   | Required | Description                                |
| :------------- | :----- | :------ | :----------------------------------------- |
| `collection_id`| `string` | Yes      | The Collection ID associated with the graph. |
| `entity_id`     | `string` | Yes      | The Entity ID to update.                   |

**Request Body:**

A JSON object containing the updated details of the entity.

**Example Request Body:**

```json
{
  "name": "Jane Doe",
  "description": "A senior software engineer.",
  "category": "Person",
  "metadata": {
    "role": "Lead Developer"
  }
}
```

**Successful Response:**

```json
{
  "results": {
    "id": "entity_id",
    "name": "Jane Doe",
    "description": "A senior software engineer.",
    "category": "Person",
    "metadata": {
      "role": "Lead Developer"
    },
    "description_embedding": [2.3, 4.5, 6.7],
    "chunk_ids": ["chunk_id3", "chunk_id4"],
    "parent_id": "parent_entity_id"
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X POST "https://api.example.com/v3/graphs/collection_id/entities/entity_id" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "name": "Jane Doe",
           "description": "A senior software engineer.",
           "category": "Person",
           "metadata": { "role": "Lead Developer" }
         }'
```

---

#### 5. Delete Entity

```http
DELETE /v3/graphs/:collection_id/entities/:entity_id
```

**Description:**
Deletes a specific entity from the graph.

**Path Parameters:**

| Parameter      | Type   | Required | Description                                |
| :------------- | :----- | :------ | :----------------------------------------- |
| `collection_id`| `string` | Yes      | The Collection ID associated with the graph. |
| `entity_id`     | `string` | Yes      | The Entity ID to delete.                   |

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
curl -X DELETE "https://api.example.com/v3/graphs/collection_id/entities/entity_id" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---