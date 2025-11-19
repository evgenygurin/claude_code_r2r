## Documents

### Overview

A **Document** in R2R represents an ingested piece of content such as text files, PDFs, images, or audio files. Documents undergo processing to generate **Chunks**, extract **Entities** & **Relationships**, and facilitate the construction of knowledge graphs. They are central to R2R’s content management system and are associated with metadata and collections for organized access control.

### Core Features of Documents

1. **Ingestion & Processing**
    - Upload new content or update existing documents.
    - Automatic chunking and optional summarization.
    - Metadata storage and advanced filtering capabilities.

2. **Knowledge Graph Extraction**
    - Extract Entities and Relationships for building knowledge graphs.
    - Maintain ingestion and extraction status.

3. **Collections & Access Control**
    - Organize documents into Collections.
    - Manage user access to documents at a collection level.

### Available Endpoints

| Method | Endpoint                           | Description                                                                                         |
| :---- | :---------------------------------- | :-------------------------------------------------------------------------------------------------- |
| POST   | `/documents`                         | Ingest a new document from a file or text content. Supports `multipart/form-data`.                  |
| POST   | `/documents/{id}`                    | Update an existing document with new content or metadata.                                           |
| GET    | `/documents`                         | List documents with pagination. Can filter by IDs.                                                  |
| GET    | `/documents/{id}`                    | Get details of a specific document.                                                                 |
| GET    | `/documents/{id}/chunks`             | Retrieve the chunks generated from a document.                                                      |
| GET    | `/documents/{id}/download`           | Download the original document file.                                                                |
| DELETE | `/documents/{id}`                    | Delete a specific document.                                                                         |
| DELETE | `/documents/by-filter`               | Delete multiple documents using filters.                                                            |
| GET    | `/documents/{id}/collections`        | List collections containing a document (**superuser only**).                                        |
| POST   | `/documents/{id}/extract`            | Extract entities and relationships from a document for knowledge graph creation.                     |
| GET    | `/documents/{id}/entities`           | Retrieve entities extracted from the document.                                                      |
| GET    | `/documents/{id}/relationships`      | List relationships between entities found in the document.                                          |

### Endpoint Details

#### 1. List Documents

```http
GET /v3/documents
```

**Description:**
Returns a paginated list of documents accessible to the authenticated user. Regular users see only their own documents or those shared through collections, while superusers see all documents.

**Query Parameters:**

| Parameter                   | Type     | Required | Description                                                                 |
| :-------------------------- | :------- | :------ | :-------------------------------------------------------------------------- |
| `ids`                       | `string` | No      | A comma-separated list of document IDs to retrieve.                         |
| `offset`                    | `integer`| No      | Number of objects to skip. Defaults to `0`.                                 |
| `limit`                     | `integer`| No      | Max number of objects to return, `1–1000`. Defaults to `100`.               |
| `include_summary_embeddings`| `integer`| No      | Whether to include embeddings of each document summary (`1` for true, `0` for false). |

**Successful Response:**

```json
{
  "results": [
    {
      "id": "id",
      "collection_ids": ["collection_ids"],
      "owner_id": "owner_id",
      "document_type": "mp3",
      "metadata": { "key": "value" },
      "version": "version",
      "title": "title",
      "size_in_bytes": 1,
      "ingestion_status": "pending",
      "extraction_status": "pending",
      "created_at": "2024-01-15T09:30:00Z",
      "updated_at": "2024-01-15T09:30:00Z",
      "ingestion_attempt_number": 1,
      "summary": "summary",
      "summary_embedding": [1.1]
    }
  ],
  "total_entries": 1
}
```

**Error Response:**

- **422 Unprocessable Entity**

---

#### 2. Create a New Document

```http
POST /v3/documents
```

**Description:**
Creates a new Document object from an input file, text content, or pre-processed chunks. The ingestion process can be configured using an `ingestion_mode` or a custom `ingestion_config`.

**Ingestion Modes:**

- `hi-res`: Comprehensive parsing and enrichment, including summaries and thorough processing.
- `fast`: Speed-focused ingestion that skips certain enrichment steps like summaries.
- `custom`: Provide a full `ingestion_config` to customize the entire ingestion process.

**Note:**
Either a file or text content must be provided, but not both. Documents are shared through `Collections`, allowing for specified cross-user interactions. The ingestion process runs asynchronously, and its progress can be tracked using the returned `task_id`.

**Request (Multipart Form):**

| Parameter                 | Type     | Required | Description                                                          |
| :------------------------ | :------- | :------ | :------------------------------------------------------------------- |
| `file`                    | `string` | No      | The file to ingest. Exactly one of `file`, `raw_text`, or `chunks` must be provided. |
| `raw_text`                | `string` | No      | Raw text content to ingest. Exactly one of `file`, `raw_text`, or `chunks` must be provided. |
| `chunks`                  | `string` | No      | Pre-processed text chunks to ingest. Exactly one of `file`, `raw_text`, or `chunks` must be provided. |
| `id`                      | `string` | No      | Document ID. If omitted, a new ID will be generated.                 |
| `collection_ids`          | `string` | No      | Collection IDs to associate with the document. Defaults to the user’s default collection if not provided. |
| `metadata`                | `string` | No      | Metadata such as title, description, or custom fields in JSON format. |
| `ingestion_mode`          | `enum`   | No      | `hi-res`, `fast`, or `custom`.                                       |
| `ingestion_config`        | `string` | No      | Custom ingestion settings if `ingestion_mode` is `custom`.           |
| `run_with_orchestration`  | `boolean`| No      | Whether ingestion runs with orchestration. Default is `true`.         |

**Successful Response:**

```json
{
  "results": {
    "message": "Document ingestion started.",
    "document_id": "generated_document_id",
    "task_id": "ingestion_task_id"
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X POST "https://api.example.com/v3/documents" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -F "file=@/path/to/document.pdf" \
     -F "metadata={\"title\": \"Sample Document\", \"description\": \"A sample document for ingestion.\"}"
```

---

#### 3. Retrieve a Document

```http
GET /v3/documents/:id
```

**Description:**
Retrieves detailed information about a specific document by its ID. This includes metadata and processing status. The document’s content is **not** returned here; use `/documents/{id}/download` to retrieve the file itself.

**Path Parameters:**

| Parameter | Type   | Required | Description                     |
| :-------- | :----- | :------ | :------------------------------ |
| `id`      | `string` | Yes      | The Document ID to retrieve.    |

**Successful Response:**

```json
{
  "results": {
    "id": "id",
    "collection_ids": ["collection_ids"],
    "owner_id": "owner_id",
    "document_type": "pdf",
    "metadata": { "key": "value" },
    "version": "version",
    "title": "title",
    "size_in_bytes": 1024,
    "ingestion_status": "success",
    "extraction_status": "enriched",
    "created_at": "2024-01-15T09:30:00Z",
    "updated_at": "2024-01-15T09:30:00Z",
    "ingestion_attempt_number": 1,
    "summary": "document summary",
    "summary_embedding": [1.1, 2.2, 3.3]
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X GET "https://api.example.com/v3/documents/document_id" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---

#### 4. Delete a Document

```http
DELETE /v3/documents/:id
```

**Description:**
Deletes a specific document, including its associated chunks and references. **Note:** This action does not currently affect the knowledge graph or other derived data.

**Path Parameters:**

| Parameter | Type   | Required | Description        |
| :-------- | :----- | :------ | :----------------- |
| `id`      | `string` | Yes      | The Document ID to delete. |

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
curl -X DELETE "https://api.example.com/v3/documents/document_id" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---

#### 5. Delete Documents by Filter

```http
DELETE /v3/documents/by-filter
```

**Description:**
Deletes multiple documents based on provided filters. Only the user’s own documents can be deleted using this method.

**Request Body:**

A JSON object containing filter criteria using operators like `$eq`, `$neq`, `$gt`, `$gte`, `$lt`, `$lte`, `$like`, `$ilike`, `$in`, and `$nin`.

**Example Request Body:**

```json
{
  "filters": {
    "document_type": { "$eq": "pdf" },
    "size_in_bytes": { "$gte": 100000 }
  }
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
curl -X DELETE "https://api.example.com/v3/documents/by-filter" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"filters": {"document_type": {"$eq": "pdf"}}}'
```

---

#### 6. List Document Chunks

```http
GET /v3/documents/:id/chunks
```

**Description:**
Retrieves the text chunks generated from a document during ingestion. Chunks represent semantic sections of the document and are used for retrieval and analysis.

**Path Parameters:**

| Parameter | Type   | Required | Description                          |
| :-------- | :----- | :------ | :----------------------------------- |
| `id`      | `string` | Yes      | The Document ID to retrieve chunks for. |

**Query Parameters:**

| Parameter         | Type      | Required | Description                                       |
| :---------------- | :-------- | :------ | :------------------------------------------------ |
| `offset`          | `integer` | No      | Number of chunks to skip. Defaults to `0`.        |
| `limit`           | `integer` | No      | Number of chunks to return (`1–1000`). Defaults to `100`. |
| `include_vectors` | `boolean` | No      | Whether to include vector embeddings in the response (`true` or `false`). |

**Successful Response:**

```json
{
  "results": [
    {
      "id": "chunk-id",
      "document_id": "document-id",
      "owner_id": "owner-id",
      "collection_ids": ["collection-id"],
      "text": "Chunk content",
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
curl -X GET "https://api.example.com/v3/documents/document_id/chunks?limit=10" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---

#### 7. Download Document Content

```http
GET /v3/documents/:id/download
```

**Description:**
Downloads the original file content of a document. For uploaded files, it returns the file with its proper MIME type. For text-only documents, it returns the content as plain text.

**Path Parameters:**

| Parameter | Type   | Required | Description        |
| :-------- | :----- | :------ | :----------------- |
| `id`      | `string` | Yes      | The Document ID to download. |

**Successful Response:**

- Returns the file content with appropriate headers.

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X GET "https://api.example.com/v3/documents/document_id/download" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -o downloaded_document.pdf
```

---

#### 8. List Document Collections (Superuser Only)

```http
GET /v3/documents/:id/collections
```

**Description:**
Lists all collections containing the specified document. **Superuser only**.

**Path Parameters:**

| Parameter | Type   | Required | Description        |
| :-------- | :----- | :------ | :----------------- |
| `id`      | `string` | Yes      | The Document ID.    |

**Query Parameters:**

| Parameter | Type      | Required | Description                           |
| :-------- | :-------- | :------ | :------------------------------------ |
| `offset`  | `integer` | No      | Number of collections to skip. Defaults to `0`. |
| `limit`   | `integer` | No      | Number of collections to return (`1–100`). Defaults to `100`. |

**Successful Response:**

```json
{
  "results": [
    {
      "id": "collection-id",
      "name": "Collection Name",
      "graph_cluster_status": "string",
      "graph_sync_status": "string",
      "created_at": "2024-01-15T09:30:00Z",
      "updated_at": "2024-01-15T09:30:00Z",
      "user_count": 10,
      "document_count": 50,
      "owner_id": "owner_id",
      "description": "A sample collection."
    }
  ],
  "total_entries": 1
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X GET "https://api.example.com/v3/documents/document_id/collections" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---

#### 9. Extract Entities and Relationships

```http
POST /v3/documents/:id/extract
```

**Description:**
Extracts entities and relationships from a document for knowledge graph creation. This process involves parsing the document into chunks, extracting entities and relationships using LLMs, and storing them in the knowledge graph.

**Path Parameters:**

| Parameter | Type   | Required | Description                                                   |
| :-------- | :----- | :------ | :------------------------------------------------------------ |
| `id`      | `string` | Yes      | The Document ID to extract entities and relationships from.   |

**Query Parameters:**

| Parameter                  | Type     | Required | Description                                                                  |
| :------------------------- | :------- | :------ | :--------------------------------------------------------------------------- |
| `run_type`                 | `string` | No      | `"estimate"` or `"run"`. Determines whether to return an estimate or execute extraction. |
| `run_with_orchestration`   | `boolean`| No      | Whether to run the extraction process with orchestration. Defaults to `true`. |

**Request Body:**

An optional JSON object containing various extraction settings.

| Parameter                          | Type     | Required | Description                                                   |
| :---------------------------------- | :------- | :------ | :------------------------------------------------------------ |
| `graph_extraction` | `string` | No | The prompt to use for knowledge graph extraction. Defaults to `graph_extraction`. |
| `graph_entity_description_prompt` | `string` | No | The prompt to use for entity description generation. Defaults to `graph_entity_description`. |
| `entity_types`                     | `array`  | No       | The types of entities to extract.                            |
| `relation_types`                   | `array`  | No       | The types of relations to extract.                           |
| `chunk_merge_count`                | `integer`| No       | Number of extractions to merge into a single KG extraction. Defaults to `4`. |
| `max_knowledge_relationships`      | `integer`| No       | Maximum number of knowledge relationships to extract from each chunk. Defaults to `100`. |
| `max_description_input_length`     | `integer`| No       | Maximum length of the description for a node in the graph. Defaults to `65536`. |
| `generation_config`                | `object` | No       | Configuration for text generation during graph enrichment.    |
| `model`                            | `string` | No       | Model to use for text generation.                            |
| `temperature`                      | `double` | No       | Temperature setting for generation.                         |
| `top_p`                            | `double` | No       | Top-p setting for generation.                               |
| `max_tokens_to_sample`             | `integer`| No       | Maximum tokens to sample during generation.                 |
| `stream`                           | `boolean`| No       | Whether to stream the generation output.                    |
| `functions`                        | `array`  | No       | List of functions for generation.                           |
| `tools`                            | `array`  | No       | List of tools for generation.                               |
| `add_generation_kwargs`            | `object` | No       | Additional generation keyword arguments.                    |
| `api_base`                         | `string` | No       | API base URL for generation.                                |
| `response_format`                  | `object` | No       | Response format configuration.                              |
| `graphrag_map_system`              | `string` | No       | System prompt for graphrag map prompt. Defaults to `graphrag_map_system`. |
| `graphrag_reduce_system`            | `string` | No       | System prompt for graphrag reduce prompt. Defaults to `graphrag_reduce_system`. |
| `max_community_description_length` | `integer`| No       | Maximum community description length. Defaults to `65536`.   |
| `max_llm_queries_for_global_search`| `integer`| No       | Maximum LLM queries for global search. Defaults to `250`.    |
| `limits`                           | `object` | No       | Limits for graph search.                                    |
| `enabled`                          | `boolean`| No       | Whether to enable graph search.                             |
| `rag_generation_config`            | `object` | No       | Configuration for RAG generation.                           |
| `task_prompt_override`             | `string` | No       | Optional custom prompt to override default.                 |
| `include_title_if_available`       | `boolean`| No       | Include document titles in responses when available.        |

**Example Request Body:**

```json
{
  "run_type": "run",
  "settings": {
    "entity_types": ["Person", "Location"],
    "relation_types": ["BornIn", "WorksAt"],
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
    "message": "Entity and relationship extraction started."
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X POST "https://api.example.com/v3/documents/document_id/extract" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "run_type": "run",
           "settings": {
             "entity_types": ["Person", "Location"],
             "relation_types": ["BornIn", "WorksAt"],
             "chunk_merge_count": 5,
             "max_knowledge_relationships": 150
           }
         }'
```

---

#### 10. Get Document Entities

```http
GET /v3/documents/:id/entities
```

**Description:**
Retrieves entities extracted from the specified document.

**Path Parameters:**

| Parameter | Type   | Required | Description                |
| :-------- | :----- | :------ | :------------------------- |
| `id`      | `string` | Yes      | The Document ID.           |

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
curl -X GET "https://api.example.com/v3/documents/document_id/entities" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---

#### 11. Get Document Relationships

```http
GET /v3/documents/:id/relationships
```

**Description:**
Retrieves relationships extracted from the specified document.

**Path Parameters:**

| Parameter | Type   | Required | Description                |
| :-------- | :----- | :------ | :------------------------- |
| `id`      | `string` | Yes      | The Document ID.           |

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
curl -X GET "https://api.example.com/v3/documents/document_id/relationships" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---