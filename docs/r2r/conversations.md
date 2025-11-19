## Conversations

### Overview

A **Conversation** in R2R represents a threaded exchange of messages that can branch into multiple paths. Conversations provide a structured way to maintain dialogue history, support branching discussions, and manage message flows, enabling interactive and dynamic interactions with the system.

### Core Features of Conversations

1. **Threaded Message Management**
    - Maintains a history of messages exchanged within the conversation.

2. **Branching Paths**
    - Supports branching, allowing the conversation to explore different topics or directions.

3. **Message Editing**
    - Allows updating existing messages with history preservation.

4. **Metadata Attachment**
    - Stores additional information with messages for enhanced context.

5. **Context Maintenance**
    - Maintains conversational context across multiple interactions for coherent dialogue.

### Available Endpoints

| Method | Endpoint                                      | Description                                  |
| :---- | :-------------------------------------------- | :------------------------------------------- |
| POST   | `/conversations`                              | Create a new conversation                    |
| GET    | `/conversations`                              | List conversations with pagination           |
| GET    | `/conversations/{id}`                         | Get conversation details                     |
| DELETE | `/conversations/{id}`                         | Delete a conversation                        |
| POST   | `/conversations/{id}/messages`                 | Add a message to conversation                |
| PUT    | `/conversations/{id}/messages/{message_id}`    | Update an existing message                   |
| GET    | `/conversations/{id}/branches`                 | List conversation branches                   |

### Endpoint Details

#### 1. List Conversations

```http
GET /v3/conversations
```

**Description:**
Lists all conversations accessible to the authenticated user, supporting pagination and filtering.

**Query Parameters:**

| Parameter | Type      | Required | Description                           |
| :-------- | :-------- | :------ | :------------------------------------ |
| `ids`     | `string` | No      | A comma-separated list of conversation IDs to retrieve. If not provided, all accessible conversations will be returned. |
| `offset`  | `integer`| No      | Number of conversations to skip. Defaults to `0`. |
| `limit`   | `integer`| No      | Number of conversations to return (`1–100`). Defaults to `100`. |

**Successful Response:**

```json
{
  "results": [
    {
      "id": "conversation_id",
      "created_at": "2024-01-15T09:30:00Z",
      "user_id": "user_id",
      "name": "AI Chatbot Conversation"
    }
  ],
  "total_entries": 1
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X GET "https://api.example.com/v3/conversations?limit=10" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---

#### 2. Create a New Conversation

```http
POST /v3/conversations
```

**Description:**
Creates a new conversation for the authenticated user.

**Request Body:**

No parameters required.

**Successful Response:**

```json
{
  "results": {
    "id": "conversation_id",
    "created_at": "2024-01-15T09:30:00Z",
    "user_id": "user_id",
    "name": "AI Chatbot Conversation"
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X POST "https://api.example.com/v3/conversations" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---

#### 3. Get Conversation Details

```http
GET /v3/conversations/:id
```

**Description:**
Retrieves detailed information about a specific conversation. Can optionally retrieve details of a specific branch.

**Path Parameters:**

| Parameter | Type   | Required | Description                        |
| :-------- | :----- | :------ | :--------------------------------- |
| `id`      | `string` | Yes      | The Conversation ID to retrieve.    |

**Query Parameters:**

| Parameter   | Type      | Required | Description                                |
| :---------- | :-------- | :------ | :----------------------------------------- |
| `branch_id` | `string` | No      | The ID of the specific branch to retrieve. |

**Successful Response:**

```json
{
  "results": [
    {
      "id": "conversation_id",
      "message": {
        "role": "assistant",
        "content": "Hello! How can I assist you today?",
        "name": "Assistant",
        "function_call": {},
        "tool_calls": []
      },
      "metadata": {}
    }
  ]
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X GET "https://api.example.com/v3/conversations/conversation_id" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---

#### 4. Delete Conversation

```http
DELETE /v3/conversations/:id
```

**Description:**
Deletes an existing conversation, removing all associated messages and branches.

**Path Parameters:**

| Parameter | Type   | Required | Description                        |
| :-------- | :----- | :------ | :--------------------------------- |
| `id`      | `string` | Yes      | The Conversation ID to delete.      |

**Successful Response:**

```json
{
  "results": {}
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X DELETE "https://api.example.com/v3/conversations/conversation_id" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---

#### 5. Add Message to Conversation

```http
POST /v3/conversations/:id/messages
```

**Description:**
Adds a new message to an existing conversation.

**Path Parameters:**

| Parameter | Type   | Required | Description                        |
| :-------- | :----- | :------ | :--------------------------------- |
| `id`      | `string` | Yes      | The Conversation ID to add the message to. |

**Request Body:**

A JSON object containing the message details.

**Example Request Body:**

```json
{
  "content": "Hello, can you help me with AI research?",
  "role": "user",
  "parent_id": "parent_message_id",
  "metadata": {
    "topic": "AI Research"
  }
}
```

**Successful Response:**

```json
{
  "results": {
    "id": "message_id",
    "message": {
      "role": "user",
      "content": "Hello, can you help me with AI research?",
      "name": "User",
      "function_call": {},
      "tool_calls": []
    },
    "metadata": {
      "topic": "AI Research"
    }
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X POST "https://api.example.com/v3/conversations/conversation_id/messages" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "content": "Hello, can you help me with AI research?",
           "role": "user",
           "parent_id": "parent_message_id",
           "metadata": { "topic": "AI Research" }
         }'
```

---

#### 6. Update Message in Conversation

```http
PUT /v3/conversations/:id/messages/:message_id
```

**Description:**
Updates an existing message within a conversation.

**Path Parameters:**

| Parameter     | Type   | Required | Description                                |
| :------------ | :----- | :------ | :----------------------------------------- |
| `id`          | `string` | Yes      | The Conversation ID containing the message. |
| `message_id`  | `string` | Yes      | The Message ID to update.                  |

**Request Body:**

A JSON object containing the updated message details.

**Example Request Body:**

```json
{
  "content": "Hello, can you assist me with advanced AI research?",
  "metadata": {
    "topic": "Advanced AI Research"
  }
}
```

**Successful Response:**

```json
{
  "results": {
    "message": {
      "role": "user",
      "content": "Hello, can you assist me with advanced AI research?",
      "name": "User",
      "function_call": {},
      "tool_calls": []
    },
    "metadata": {
      "topic": "Advanced AI Research"
    }
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X PUT "https://api.example.com/v3/conversations/conversation_id/messages/message_id" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "content": "Hello, can you assist me with advanced AI research?",
           "metadata": { "topic": "Advanced AI Research" }
         }'
```

---

#### 7. List Conversation Branches

```http
GET /v3/conversations/:id/branches
```

**Description:**
Lists all branches within a specific conversation, supporting pagination.

**Path Parameters:**

| Parameter | Type   | Required | Description                        |
| :-------- | :----- | :------ | :--------------------------------- |
| `id`      | `string` | Yes      | The Conversation ID to retrieve branches for. |

**Query Parameters:**

| Parameter | Type      | Required | Description                           |
| :-------- | :-------- | :------ | :------------------------------------ |
| `offset`  | `integer` | No      | Number of branches to skip. Defaults to `0`. |
| `limit`   | `integer` | No      | Number of branches to return (`1–100`). Defaults to `100`. |

**Successful Response:**

```json
{
  "results": [
    {
      "branch_id": "branch_id",
      "created_at": "2024-01-16T10:00:00Z",
      "branch_point_id": "message_id",
      "content": "Branch content here.",
      "user_id": "user_id",
      "name": "Branch Name"
    }
  ],
  "total_entries": 1
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X GET "https://api.example.com/v3/conversations/conversation_id/branches?limit=10" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---