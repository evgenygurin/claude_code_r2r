## System

### Overview

The **System** section of the R2R API provides endpoints for monitoring and managing the overall health, logs, settings, and status of the R2R system. These tools are essential for administrators and superusers to ensure the system operates smoothly and efficiently.

### Core Features of System Endpoints

1. **Health Monitoring**
    - Check the overall health status of the R2R system.

2. **Log Retrieval**
    - Access system logs for monitoring and debugging purposes.

3. **Settings Management**
    - Retrieve and manage current configuration settings of the R2R system.

4. **Server Status**
    - Get real-time information about server uptime and resource usage.

### Available Endpoints

| Method | Endpoint               | Description                                                   |
| :---- | :--------------------- | :------------------------------------------------------------ |
| GET    | `/system/logs`         | Retrieve system logs for monitoring and debugging purposes.  |
| GET    | `/system/health`       | Check the overall health status of the R2R system.           |
| GET    | `/system/settings`     | Retrieve the current configuration settings of the R2R system. |
| GET    | `/system/status`       | Retrieve the current server status, including uptime and resource usage. |

### Endpoint Details

#### 1. R2R Logs

```http
GET /v3/system/logs
```

**Description:**
Retrieves system logs for monitoring and debugging purposes.

**Query Parameters:**

| Parameter        | Type      | Required | Description                                  |
| :--------------- | :-------- | :------ | :------------------------------------------- |
| `run_type_filter`| `string` | No      | Filter logs based on run type (e.g., "ingestion", "extraction"). |
| `offset`         | `integer`| No      | Number of log entries to skip. Defaults to `0`. |
| `limit`          | `integer`| No      | Number of log entries to return (`1–100`). Defaults to `100`. |

**Successful Response:**

```json
{
  "results": [
    {
      "run_id": "run_id",
      "run_type": "ingestion",
      "entries": [
        {
          "key": "event",
          "value": "Document ingested successfully.",
          "timestamp": "2024-01-15T09:30:00Z",
          "user_id": "user_id"
        }
      ],
      "timestamp": "2024-01-15T09:30:00Z",
      "user_id": "user_id"
    }
  ],
  "total_entries": 1
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X GET "https://api.example.com/v3/system/logs?limit=10" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---

#### 2. Check System Health

```http
GET /v3/system/health
```

**Description:**
Checks the overall health status of the R2R system, ensuring that all components are functioning correctly.

**Successful Response:**

```json
{
  "results": {
    "message": "System is healthy."
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**: System is experiencing issues.

**Example cURL:**

```bash
curl -X GET "https://api.example.com/v3/system/health" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---

#### 3. R2R Settings

```http
GET /v3/system/settings
```

**Description:**
Retrieves the current configuration settings of the R2R system, including prompt configurations and project name.

**Successful Response:**

```json
{
  "results": {
    "config": {
      "setting_key": "setting_value"
    },
    "prompts": {
      "prompt_name": "prompt_template"
    },
    "r2r_project_name": "R2R Project"
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**: Access denied or invalid request.

**Example cURL:**

```bash
curl -X GET "https://api.example.com/v3/system/settings" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---

#### 4. Server Status

```http
GET /v3/system/status
```

**Description:**
Retrieves the current server status, including uptime and resource usage statistics.

**Successful Response:**

```json
{
  "results": {
    "start_time": "2024-01-01T00:00:00Z",
    "uptime_seconds": 86400,
    "cpu_usage_percent": 75.5,
    "memory_usage_percent": 65.2
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**: Unable to retrieve server status.

**Example cURL:**

```bash
curl -X GET "https://api.example.com/v3/system/status" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---