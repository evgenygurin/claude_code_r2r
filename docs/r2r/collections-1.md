## Collections

### Overview

A **Collection** in R2R is a logical grouping mechanism that organizes documents, enabling efficient access control and collaboration among users. Collections serve as the primary unit for managing permissions, sharing content, and organizing related documents across users and teams.

### Core Features of Collections

1. **Organizational Structure**
    - Groups related documents for better management and retrieval.

2. **Access Control & Permissions**
    - Manages user access at the collection level, allowing for granular permissions management.

3. **Content Sharing**
    - Facilitates sharing of documents and associated data among users within the collection.

4. **Collaboration Capabilities**
    - Enables multiple users to collaborate on document ingestion, management, and retrieval within a collection.

5. **Metadata Management**
    - Stores metadata and descriptions for each collection to provide context and organization.

### Available Endpoints

| Method | Endpoint                                         | Description                                                   |
| :---- | :----------------------------------------------- | :------------------------------------------------------------ |
| POST   | `/collections`                                   | Create a new collection                                       |
| GET    | `/collections`                                   | List collections with pagination and filtering               |
| GET    | `/collections/{id}`                              | Get details of a specific collection                          |
| POST   | `/collections/{id}`                              | Update an existing collection                                 |
| DELETE | `/collections/{id}`                              | Delete an existing collection                                 |
| GET    | `/collections/{id}/documents`                    | List documents in a collection                                |
| POST   | `/collections/{id}/documents/{document_id}`      | Add a document to a collection                                |
| POST   | `/collections/{id}/extract`                      | Extract entities and relationships for all unextracted documents in the collection |
| DELETE | `/collections/{id}/documents/{document_id}`      | Remove a document from a collection                           |
| GET    | `/collections/{id}/users`                        | List users with access to a collection                        |
| POST   | `/collections/{id}/users/{user_id}`              | Add a user to a collection                                    |
| DELETE | `/collections/{id}/users/{user_id}`              | Remove a user from a collection                               |

### Endpoint Details

#### 1. List Collections

```http
GET /v3/collections
```

**Description:**
Returns a paginated list of collections the authenticated user has access to. Results can be filtered by specific collection IDs. Regular users will see collections they own or have access to, while superusers can view all collections. Collections are ordered by last modification date, with the most recent first.

**Query Parameters:**

| Parameter | Type      | Required | Description                           |
| :-------- | :-------- | :------ | :------------------------------------ |
| `ids`     | `string` | No      | A comma-separated list of collection IDs to retrieve. If not provided, all accessible collections will be returned. |
| `offset`  | `integer`| No      | Number of collections to skip. Defaults to `0`. |
| `limit`   | `integer`| No      | Number of collections to return (`1–100`). Defaults to `100`. |

**Successful Response:**

```json
{
  "results": [
    {
      "id": "collection_id",
      "name": "AI Research Collection",
      "graph_cluster_status": "active",
      "graph_sync_status": "synchronized",
      "created_at": "2024-01-15T09:30:00Z",
      "updated_at": "2024-01-15T09:30:00Z",
      "user_count": 5,
      "document_count": 10,
      "owner_id": "owner_id",
      "description": "A collection of documents related to AI research."
    }
  ],
  "total_entries": 1
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X GET "https://api.example.com/v3/collections?limit=10" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---

#### 2. Create a New Collection

```http
POST /v3/collections
```

**Description:**
Creates a new collection and automatically adds the creating user to it.

**Request Body:**

A JSON object containing the name and optional description of the collection.

**Example Request Body:**

```json
{
  "name": "AI Research Collection",
  "description": "A collection of documents related to AI research."
}
```

**Successful Response:**

```json
{
  "results": {
    "id": "collection_id",
    "name": "AI Research Collection",
    "graph_cluster_status": "active",
    "graph_sync_status": "synchronized",
    "created_at": "2024-01-15T09:30:00Z",
    "updated_at": "2024-01-15T09:30:00Z",
    "user_count": 1,
    "document_count": 0,
    "owner_id": "user_id",
    "description": "A collection of documents related to AI research."
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X POST "https://api.example.com/v3/collections" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "name": "AI Research Collection",
           "description": "A collection of documents related to AI research."
         }'
```

---

#### 3. Get Collection Details

```http
GET /v3/collections/:id
```

**Description:**
Retrieves detailed information about a specific collection.

**Path Parameters:**

| Parameter | Type   | Required | Description                        |
| :-------- | :----- | :------ | :--------------------------------- |
| `id`      | `string` | Yes      | The Collection ID to retrieve details for. |

**Successful Response:**

```json
{
  "results": {
    "id": "collection_id",
    "name": "AI Research Collection",
    "graph_cluster_status": "active",
    "graph_sync_status": "synchronized",
    "created_at": "2024-01-15T09:30:00Z",
    "updated_at": "2024-01-15T09:30:00Z",
    "user_count": 10,
    "document_count": 50,
    "owner_id": "owner_id",
    "description": "A collection of documents related to AI research."
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X GET "https://api.example.com/v3/collections/collection_id" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---

#### 4. Update Collection

```http
POST /v3/collections/:id
```

**Description:**
Updates the configuration of an existing collection, including its name and description.

**Path Parameters:**

| Parameter | Type   | Required | Description                        |
| :-------- | :----- | :------ | :--------------------------------- |
| `id`      | `string` | Yes      | The Collection ID to update.        |

**Request Body:**

A JSON object containing the updated details of the collection.

**Example Request Body:**

```json
{
  "name": "Advanced AI Research Collection",
  "description": "An updated description for the AI research collection."
}
```

**Successful Response:**

```json
{
  "results": {
    "id": "collection_id",
    "name": "Advanced AI Research Collection",
    "graph_cluster_status": "active",
    "graph_sync_status": "synchronized",
    "created_at": "2024-01-15T09:30:00Z",
    "updated_at": "2024-02-20T10:45:00Z",
    "user_count": 10,
    "document_count": 50,
    "owner_id": "owner_id",
    "description": "An updated description for the AI research collection."
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X POST "https://api.example.com/v3/collections/collection_id" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "name": "Advanced AI Research Collection",
           "description": "An updated description for the AI research collection."
         }'
```

---

#### 5. Delete Collection

```http
DELETE /v3/collections/:id
```

**Description:**
Deletes an existing collection. This action removes all associations but does not delete the documents within it.

**Path Parameters:**

| Parameter | Type   | Required | Description                        |
| :-------- | :----- | :------ | :--------------------------------- |
| `id`      | `string` | Yes      | The Collection ID to delete.        |

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
curl -X DELETE "https://api.example.com/v3/collections/collection_id" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---

#### 6. Add Document to Collection

```http
POST /v3/collections/:id/documents/:document_id
```

**Description:**
Adds a document to a specific collection, enabling access to the document within that collection's context.

**Path Parameters:**

| Parameter      | Type   | Required | Description                        |
| :------------- | :----- | :------ | :--------------------------------- |
| `id`           | `string` | Yes      | The Collection ID to add the document to. |
| `document_id`  | `string` | Yes      | The Document ID to add.            |

**Successful Response:**

```json
{
  "results": {
    "message": "Document added to collection successfully."
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X POST "https://api.example.com/v3/collections/collection_id/documents/document_id" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---

#### 7. Remove Document from Collection

```http
DELETE /v3/collections/:id/documents/:document_id
```

**Description:**
Removes a document from a specific collection, revoking access to it within that collection's context. This action does not delete the document itself.

**Path Parameters:**

| Parameter      | Type   | Required | Description                        |
| :------------- | :----- | :------ | :--------------------------------- |
| `id`           | `string` | Yes      | The Collection ID to remove the document from. |
| `document_id`  | `string` | Yes      | The Document ID to remove.         |

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
curl -X DELETE "https://api.example.com/v3/collections/collection_id/documents/document_id" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---

#### 8. List Documents in Collection

```http
GET /v3/collections/:id/documents
```

**Description:**
Retrieves all documents within a specific collection, supporting pagination and sorting options.

**Path Parameters:**

| Parameter | Type   | Required | Description                        |
| :-------- | :----- | :------ | :--------------------------------- |
| `id`      | `string` | Yes      | The Collection ID to retrieve documents from. |

**Query Parameters:**

| Parameter | Type      | Required | Description                           |
| :-------- | :-------- | :------ | :------------------------------------ |
| `offset`  | `integer` | No      | Number of documents to skip. Defaults to `0`. |
| `limit`   | `integer` | No      | Number of documents to return (`1–100`). Defaults to `100`. |

**Successful Response:**

```json
{
  "results": [
    {
      "id": "document_id",
      "collection_ids": ["collection_id1", "collection_id2"],
      "owner_id": "owner_id",
      "document_type": "pdf",
      "metadata": {
        "title": "AI Research Paper",
        "description": "A comprehensive study on AI advancements."
      },
      "version": "1.0",
      "title": "AI Research Paper",
      "size_in_bytes": 102400,
      "ingestion_status": "success",
      "extraction_status": "success",
      "created_at": "2024-01-15T09:30:00Z",
      "updated_at": "2024-01-15T09:30:00Z",
      "ingestion_attempt_number": 1,
      "summary": "This paper explores recent advancements in artificial intelligence.",
      "summary_embedding": [1.1, 2.2, 3.3],
      "total_entries": 1
    }
  ],
  "total_entries": 1
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X GET "https://api.example.com/v3/collections/collection_id/documents?limit=10" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---

#### 9. List Users in Collection

```http
GET /v3/collections/:id/users
```

**Description:**
Retrieves all users with access to a specific collection, supporting pagination and sorting options.

**Path Parameters:**

| Parameter | Type   | Required | Description                        |
| :-------- | :----- | :------ | :--------------------------------- |
| `id`      | `string` | Yes      | The Collection ID to retrieve users from. |

**Query Parameters:**

| Parameter | Type      | Required | Description                           |
| :-------- | :-------- | :------ | :------------------------------------ |
| `offset`  | `integer` | No      | Number of users to skip. Defaults to `0`. |
| `limit`   | `integer` | No      | Number of users to return (`1–100`). Defaults to `100`. |

**Successful Response:**

```json
{
  "results": [
    {
      "id": "user_id",
      "email": "user@example.com",
      "is_active": true,
      "is_superuser": false,
      "created_at": "2024-01-15T09:30:00Z",
      "updated_at": "2024-01-15T09:30:00Z",
      "is_verified": true,
      "collection_ids": ["collection_id1"],
      "graph_ids": ["graph_id1"],
      "document_ids": ["document_id1"],
      "hashed_password": "hashed_password",
      "verification_code_expiry": "2024-01-16T09:30:00Z",
      "name": "John Doe",
      "bio": "A software developer.",
      "profile_picture": "https://example.com/profile.jpg",
      "total_size_in_bytes": 204800,
      "num_files": 10
    }
  ],
  "total_entries": 1
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X GET "https://api.example.com/v3/collections/collection_id/users?limit=10" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---

#### 10. Add User to Collection

```http
POST /v3/collections/:id/users/:user_id
```

**Description:**
Adds a user to a specific collection, granting them access to its documents and graphs. The authenticated user must have admin permissions for the collection to add new users.

**Path Parameters:**

| Parameter      | Type   | Required | Description                                |
| :------------- | :----- | :------ | :----------------------------------------- |
| `id`           | `string` | Yes      | The Collection ID to add the user to.       |
| `user_id`      | `string` | Yes      | The User ID to add to the collection.       |

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
curl -X POST "https://api.example.com/v3/collections/collection_id/users/user_id" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---

#### 11. Remove User from Collection

```http
DELETE /v3/collections/:id/users/:user_id
```

**Description:**
Removes a user from a specific collection, revoking their access to its documents and graphs. The authenticated user must have admin permissions for the collection to remove users.

**Path Parameters:**

| Parameter      | Type   | Required | Description                                |
| :------------- | :----- | :------ | :----------------------------------------- |
| `id`           | `string` | Yes      | The Collection ID to remove the user from.  |
| `user_id`      | `string` | Yes      | The User ID to remove from the collection.  |

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
curl -X DELETE "https://api.example.com/v3/collections/collection_id/users/user_id" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---

#### 12. Extract Entities and Relationships (Collection-level)

```http
POST /v3/collections/:id/extract
```

**Description:**
Extracts entities and relationships from all unextracted documents within a collection, facilitating comprehensive knowledge graph construction.

**Path Parameters:**

| Parameter | Type   | Required | Description                        |
| :-------- | :----- | :------ | :--------------------------------- |
| `id`      | `string` | Yes      | The Collection ID to extract from.  |

**Query Parameters:**

| Parameter                | Type      | Required | Description                                     |
| :----------------------- | :-------- | :------ | :---------------------------------------------- |
| `run_type`               | `string` | No      | `"estimate"` or `"run"`. Determines operation type. |
| `run_with_orchestration` | `boolean`| No      | Whether to run the extraction process with orchestration. |

**Request Body:**

An optional JSON object containing various extraction prompts and configurations.

**Example Request Body:**

```json
{
  "run_type": "run",
  "settings": {
    "entity_types": ["Person", "Organization"],
    "relation_types": ["EmployedBy", "CollaboratesWith"],
    "chunk_merge_count": 5,
    "max_knowledge_relationships": 150,
    "generation_config": {
      "model": "gpt-4",
      "temperature": 0.7,
      "top_p": 0.9,
      "max_tokens_to_sample": 100,
      "stream": false
    }
  }
}
```

**Successful Response:**

```json
{
  "results": {
    "message": "Entity and relationship extraction initiated for collection."
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X POST "https://api.example.com/v3/collections/collection_id/extract" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "run_type": "run",
           "settings": {
             "entity_types": ["Person", "Organization"],
             "relation_types": ["EmployedBy", "CollaboratesWith"],
             "chunk_merge_count": 5,
             "max_knowledge_relationships": 150
           }
         }'
```

---