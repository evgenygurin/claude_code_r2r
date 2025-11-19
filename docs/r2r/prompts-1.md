## Prompts

### Overview

A **Prompt** in R2R represents a templated instruction or query pattern managed by superusers. Prompts provide a consistent and reusable way to structure interactions with language models and other AI components, ensuring standardized outputs and interactions across the system.

### Core Features of Prompts

1. **Templated Instruction Management**
    - Centralizes prompt templates for consistent usage.

2. **Type-safe Input Handling**
    - Defines input types for dynamic prompt generation.

3. **Centralized Governance**
    - Managed by superusers to maintain standardization.

4. **Dynamic Prompt Generation**
    - Supports dynamic insertion of input values into templates.

5. **Version Control**
    - Maintains versions of prompts for historical reference and rollback.

### Available Endpoints

| Method | Endpoint         | Description                                 |
| :---- | :--------------- | :------------------------------------------ |
| POST   | `/prompts`       | Create a new prompt template                |
| GET    | `/prompts`       | List all available prompts                  |
| GET    | `/prompts/{name}`| Get a specific prompt with optional inputs  |
| PUT    | `/prompts/{name}`| Update an existing prompt                   |
| DELETE | `/prompts/{name}`| Delete a prompt template                    |

### Endpoint Details

#### 1. List All Prompts

```http
GET /v3/prompts
```

**Description:**
Lists all available prompts. Accessible only by superusers.

**Successful Response:**

```json
{
  "results": [
    {
      "id": "prompt_id",
      "name": "greeting_prompt",
      "template": "Hello, {name}!",
      "created_at": "2024-01-15T09:30:00Z",
      "updated_at": "2024-02-20T10:45:00Z",
      "input_types": {
        "name": "string",
        "age": "integer"
      }
    }
  ],
  "total_entries": 1
}
```

**Error Response:**

- **422 Unprocessable Entity**: Access denied or invalid request.

**Example cURL:**

```bash
curl -X GET "https://api.example.com/v3/prompts" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---

#### 2. Create a New Prompt

```http
POST /v3/prompts
```

**Description:**
Creates a new prompt with the provided configuration. Only superusers can create prompts.

**Request Body:**

A JSON object containing the prompt's name, template, and input types.

**Example Request Body:**

```json
{
  "name": "greeting_prompt",
  "template": "Hello, {name}! You are {age} years old.",
  "input_types": {
    "name": "string",
    "age": "integer"
  }
}
```

**Successful Response:**

```json
{
  "results": {
    "message": "Prompt created successfully."
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**: Invalid input or access denied.

**Example cURL:**

```bash
curl -X POST "https://api.example.com/v3/prompts" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "name": "greeting_prompt",
           "template": "Hello, {name}! You are {age} years old.",
           "input_types": { "name": "string", "age": "integer" }
         }'
```

---

#### 3. Get an Existing Prompt

```http
GET /v3/prompts/:name
```

**Description:**
Retrieves a specific prompt by name, optionally with input values and overrides.

**Path Parameters:**

| Parameter | Type   | Required | Description                |
| :-------- | :----- | :------ | :------------------------- |
| `name`    | `string` | Yes      | The name of the prompt.    |

**Query Parameters:**

| Parameter         | Type      | Required | Description                             |
| :---------------- | :-------- | :------ | :-------------------------------------- |
| `prompt_override` | `string` | No      | Optional custom prompt override.        |

**Request Body:**

A JSON object containing input values for the prompt.

**Example Request Body:**

```json
{
  "inputs": {
    "name": "Alice",
    "age": 30
  }
}
```

**Successful Response:**

```json
{
  "results": {
    "id": "prompt_id",
    "name": "greeting_prompt",
    "template": "Hello, Alice! You are 30 years old.",
    "created_at": "2024-01-15T09:30:00Z",
    "updated_at": "2024-02-20T10:45:00Z",
    "input_types": {
      "name": "string",
      "age": "integer"
    }
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**: Invalid prompt name or access denied.

**Example cURL:**

```bash
curl -X GET "https://api.example.com/v3/prompts/greeting_prompt" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "inputs": { "name": "Alice", "age": 30 }
         }'
```

---

#### 4. Update an Existing Prompt

```http
PUT /v3/prompts/:name
```

**Description:**
Updates an existing prompt’s template and/or input types. Only superusers can update prompts.

**Path Parameters:**

| Parameter | Type   | Required | Description                |
| :-------- | :----- | :------ | :------------------------- |
| `name`    | `string` | Yes      | The name of the prompt.    |

**Request Body:**

A JSON object containing the updated template and input types.

**Example Request Body:**

```json
{
  "template": "Greetings, {name}! You are {age} years old.",
  "input_types": {
    "name": "string",
    "age": "integer",
    "location": "string"
  }
}
```

**Successful Response:**

```json
{
  "results": {
    "message": "Prompt updated successfully."
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**: Invalid prompt name or update parameters.

**Example cURL:**

```bash
curl -X PUT "https://api.example.com/v3/prompts/greeting_prompt" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "template": "Greetings, {name}! You are {age} years old.",
           "input_types": { "name": "string", "age": "integer", "location": "string" }
         }'
```

---

#### 5. Delete a Prompt

```http
DELETE /v3/prompts/:name
```

**Description:**
Deletes a prompt by name. Only superusers can delete prompts.

**Path Parameters:**

| Parameter | Type   | Required | Description                |
| :-------- | :----- | :------ | :------------------------- |
| `name`    | `string` | Yes      | The name of the prompt.    |

**Successful Response:**

```json
{
  "results": {
    "success": true
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**: Invalid prompt name or access denied.

**Example cURL:**

```bash
curl -X DELETE "https://api.example.com/v3/prompts/greeting_prompt" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---