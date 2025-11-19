# MCP Server: Детальная спецификация

> **Phase 4.1**: Техническая спецификация MCP Server для R2R интеграции
>
> **Дата**: 2025-11-19
>
> **Цель**: Детально описать архитектуру и реализацию MCP Server

---

## Оглавление

1. [Executive Summary](#executive-summary)
2. [Architecture Overview](#architecture-overview)
3. [Tools Specification](#tools-specification)
4. [Resources Specification](#resources-specification)
5. [Authentication Strategy](#authentication-strategy)
6. [Caching Layer](#caching-layer)
7. [Circuit Breaker Implementation](#circuit-breaker-implementation)
8. [Error Handling](#error-handling)
9. [Configuration](#configuration)
10. [Testing Strategy](#testing-strategy)
11. [Deployment](#deployment)
12. [Performance](#performance)

---

## Executive Summary

### What is this MCP Server?

**R2R MCP Server** - это HTTP-based Model Context Protocol server, который:
- Предоставляет Claude Code доступ к R2R API
- Управляет аутентификацией и token refresh
- Кэширует результаты поиска
- Обеспечивает resilience через circuit breaker
- Трансформирует R2R API в MCP Tools и Resources

### Key Characteristics

| Aspect | Value |
|--------|-------|
| **Protocol** | MCP (Model Context Protocol) over HTTP |
| **Transport** | HTTP/HTTPS |
| **Authentication** | Bearer token (OAuth flow) |
| **Language** | Python 3.10+ |
| **Framework** | FastAPI (async) |
| **R2R SDK** | r2r-py |
| **Caching** | Redis (optional) or in-memory |
| **Monitoring** | Structured logging + Prometheus metrics |

### Complexity Assessment

**UPDATED Assessment:**
- **Original estimate**: Medium complexity
- **Actual complexity**: **HIGH** ⚠️
- **Reasons**:
  - Full HTTP server implementation
  - JSON-RPC 2.0 protocol compliance
  - OAuth authentication flow
  - Caching layer with TTL
  - Circuit breaker pattern
  - Request/response transformation
  - Comprehensive error handling
  - Logging and monitoring
  - Testing (unit + integration + E2E)

**Estimated Development Time:** 3-4 weeks (not 1 week)

---

## Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Claude Code                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              MCP Client                              │   │
│  │  - Discovers tools and resources                     │   │
│  │  - Makes JSON-RPC 2.0 requests                      │   │
│  └───────────────────┬─────────────────────────────────┘   │
└────────────────────────┼───────────────────────────────────┘
                         │ HTTP/HTTPS
                         │ JSON-RPC 2.0
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   R2R MCP Server                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  HTTP Server (FastAPI)                               │  │
│  │  - /mcp (JSON-RPC endpoint)                         │  │
│  │  - /health (health check)                           │  │
│  │  - /metrics (Prometheus metrics)                    │  │
│  └───────────────────┬──────────────────────────────────┘  │
│                      │                                      │
│  ┌───────────────────▼──────────────────────────────────┐  │
│  │  JSON-RPC 2.0 Router                                │  │
│  │  - initialize                                        │  │
│  │  - tools/list                                        │  │
│  │  - tools/call                                        │  │
│  │  - resources/list                                    │  │
│  │  - resources/read                                    │  │
│  └───────────────────┬──────────────────────────────────┘  │
│                      │                                      │
│  ┌───────────────────▼──────────────────────────────────┐  │
│  │  Tool Handlers                                       │  │
│  │  - r2r_search                                        │  │
│  │  - r2r_rag_query                                     │  │
│  │  - r2r_ingest_document                              │  │
│  │  - r2r_list_documents                               │  │
│  │  - r2r_monitor_task                                 │  │
│  │  - r2r_list_collections                             │  │
│  └───────────────────┬──────────────────────────────────┘  │
│                      │                                      │
│  ┌───────────────────▼──────────────────────────────────┐  │
│  │  Middleware Layer                                    │  │
│  │  ┌──────────┐  ┌────────────┐  ┌─────────────────┐ │  │
│  │  │  Auth    │  │   Cache    │  │  Circuit        │ │  │
│  │  │  Manager │  │   Layer    │  │  Breaker        │ │  │
│  │  └──────────┘  └────────────┘  └─────────────────┘ │  │
│  └───────────────────┬──────────────────────────────────┘  │
│                      │                                      │
│  ┌───────────────────▼──────────────────────────────────┐  │
│  │  R2R Client (r2r-py SDK)                            │  │
│  │  - Authenticated requests                            │  │
│  │  - Automatic token refresh                          │  │
│  │  - Retry logic                                       │  │
│  └───────────────────┬──────────────────────────────────┘  │
└────────────────────────┼───────────────────────────────────┘
                         │ HTTPS
                         │ REST API
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  R2R Instance                               │
│              http://136.119.36.216:7272                     │
│  - Documents API                                            │
│  - Collections API                                          │
│  - Retrieval API                                            │
│  - Users API                                                │
│  - Conversations API                                        │
└─────────────────────────────────────────────────────────────┘
```

### Component Breakdown

#### 1. HTTP Server (FastAPI)

**Responsibilities:**
- Accept HTTP requests from Claude Code MCP client
- Route to JSON-RPC handler
- Health checks and metrics

**Endpoints:**

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(title="R2R MCP Server", version="1.0.0")

@app.post("/mcp")
async def mcp_endpoint(request: Request):
    """Main JSON-RPC 2.0 endpoint"""
    body = await request.json()
    response = await handle_jsonrpc(body)
    return JSONResponse(response)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/metrics")
async def metrics():
    """Prometheus metrics"""
    return generate_prometheus_metrics()
```

#### 2. JSON-RPC 2.0 Router

**Responsibilities:**
- Parse JSON-RPC 2.0 requests
- Dispatch to appropriate handler
- Format responses

**Methods:**

| Method | Description | Request | Response |
|--------|-------------|---------|----------|
| `initialize` | Initialize MCP session | `{"jsonrpc": "2.0", "method": "initialize", "params": {...}}` | Server info and capabilities |
| `tools/list` | List available tools | `{"jsonrpc": "2.0", "method": "tools/list"}` | Array of tool definitions |
| `tools/call` | Call a specific tool | `{"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "...", "arguments": {...}}}` | Tool result |
| `resources/list` | List available resources | `{"jsonrpc": "2.0", "method": "resources/list"}` | Array of resource definitions |
| `resources/read` | Read a specific resource | `{"jsonrpc": "2.0", "method": "resources/read", "params": {"uri": "..."}}` | Resource content |

**Implementation:**

```python
import json
from typing import Dict, Any

async def handle_jsonrpc(request_body: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle JSON-RPC 2.0 request

    Args:
        request_body: JSON-RPC request object

    Returns:
        JSON-RPC response object
    """
    jsonrpc = request_body.get("jsonrpc")
    method = request_body.get("method")
    params = request_body.get("params", {})
    request_id = request_body.get("id")

    # Validate JSON-RPC 2.0
    if jsonrpc != "2.0":
        return {
            "jsonrpc": "2.0",
            "error": {
                "code": -32600,
                "message": "Invalid Request"
            },
            "id": request_id
        }

    # Route to handler
    try:
        if method == "initialize":
            result = await handle_initialize(params)
        elif method == "tools/list":
            result = await handle_tools_list()
        elif method == "tools/call":
            result = await handle_tools_call(params)
        elif method == "resources/list":
            result = await handle_resources_list()
        elif method == "resources/read":
            result = await handle_resources_read(params)
        else:
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32601,
                    "message": "Method not found"
                },
                "id": request_id
            }

        return {
            "jsonrpc": "2.0",
            "result": result,
            "id": request_id
        }

    except Exception as e:
        logger.exception(f"Error handling {method}")
        return {
            "jsonrpc": "2.0",
            "error": {
                "code": -32603,
                "message": "Internal error",
                "data": str(e)
            },
            "id": request_id
        }
```

---

## Tools Specification

### Tool 1: r2r_search

**Purpose:** Semantic/hybrid search across project documentation

**Input Schema:**

```json
{
  "name": "r2r_search",
  "description": "Search through project documentation using semantic or hybrid search. Returns relevant chunks with metadata.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "Search query (natural language)"
      },
      "collection_id": {
        "type": "string",
        "description": "Collection ID to search in (optional, defaults to current project)"
      },
      "search_mode": {
        "type": "string",
        "enum": ["basic", "advanced", "custom"],
        "default": "advanced",
        "description": "Search mode: basic (semantic only), advanced (hybrid), custom (full control)"
      },
      "limit": {
        "type": "integer",
        "default": 10,
        "minimum": 1,
        "maximum": 100,
        "description": "Maximum number of results to return"
      },
      "filters": {
        "type": "object",
        "description": "Additional filters (e.g., {\"document_type\": {\"$eq\": \"md\"}})"
      }
    },
    "required": ["query"]
  }
}
```

**Implementation:**

```python
async def r2r_search_tool(
    query: str,
    collection_id: Optional[str] = None,
    search_mode: str = "advanced",
    limit: int = 10,
    filters: Optional[Dict] = None
) -> Dict[str, Any]:
    """
    Execute search in R2R

    Returns:
        {
            "results": [...],
            "count": int,
            "cached": bool
        }
    """
    # Get current project collection if not specified
    if not collection_id:
        collection_id = await get_current_project_collection()

    # Check cache
    cache_key = f"search:{collection_id}:{query}:{search_mode}:{limit}"
    cached = await cache.get(cache_key)
    if cached:
        logger.info(f"Cache hit for search: {query}")
        return {"cached": True, **json.loads(cached)}

    # Build filters
    search_filters = filters or {}
    search_filters["collection_id"] = {"$eq": collection_id}

    # Execute search through circuit breaker
    try:
        response = await circuit_breaker.call(
            r2r_client.retrieval.search,
            query=query,
            search_settings={
                "use_semantic_search": True,
                "use_fulltext_search": search_mode == "advanced",
                "filters": search_filters,
                "limit": limit
            }
        )

        result = {
            "results": response["results"]["chunk_search_results"],
            "count": len(response["results"]["chunk_search_results"]),
            "cached": False
        }

        # Cache for 5 minutes
        await cache.set(cache_key, json.dumps(result), ttl=300)

        return result

    except Exception as e:
        logger.exception(f"Search failed: {query}")
        raise
```

### Tool 2: r2r_rag_query

**Purpose:** RAG-powered Q&A over project documentation

**Input Schema:**

```json
{
  "name": "r2r_rag_query",
  "description": "Ask a question and get an AI-generated answer based on project documentation. Uses retrieval-augmented generation.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "question": {
        "type": "string",
        "description": "Question to answer (natural language)"
      },
      "collection_id": {
        "type": "string",
        "description": "Collection ID to query (optional, defaults to current project)"
      },
      "model": {
        "type": "string",
        "default": "gpt-4",
        "description": "LLM model to use for generation"
      },
      "max_tokens": {
        "type": "integer",
        "default": 500,
        "description": "Maximum tokens in response"
      },
      "temperature": {
        "type": "number",
        "default": 0.7,
        "minimum": 0.0,
        "maximum": 2.0,
        "description": "Sampling temperature"
      },
      "include_sources": {
        "type": "boolean",
        "default": true,
        "description": "Include source document citations"
      }
    },
    "required": ["question"]
  }
}
```

**Implementation:**

```python
async def r2r_rag_query_tool(
    question: str,
    collection_id: Optional[str] = None,
    model: str = "gpt-4",
    max_tokens: int = 500,
    temperature: float = 0.7,
    include_sources: bool = True
) -> Dict[str, Any]:
    """
    Execute RAG query

    Returns:
        {
            "answer": str,
            "sources": [...] (if include_sources),
            "model_used": str,
            "cached": bool
        }
    """
    if not collection_id:
        collection_id = await get_current_project_collection()

    # Check cache (shorter TTL for RAG)
    cache_key = f"rag:{collection_id}:{question}:{model}"
    cached = await cache.get(cache_key)
    if cached:
        logger.info(f"Cache hit for RAG query: {question}")
        return {"cached": True, **json.loads(cached)}

    try:
        response = await circuit_breaker.call(
            r2r_client.retrieval.rag,
            query=question,
            search_settings={
                "filters": {"collection_id": {"$eq": collection_id}},
                "limit": 5
            },
            rag_generation_config={
                "model": model,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
        )

        result = {
            "answer": response["results"]["generated_answer"],
            "sources": [
                {
                    "text": chunk["text"],
                    "document": chunk["metadata"].get("title", "Unknown"),
                    "score": chunk["score"]
                }
                for chunk in response["results"]["chunk_search_results"]
            ] if include_sources else [],
            "model_used": model,
            "cached": False
        }

        # Cache for 2 minutes (RAG responses may vary)
        await cache.set(cache_key, json.dumps(result), ttl=120)

        return result

    except Exception as e:
        logger.exception(f"RAG query failed: {question}")
        raise
```

### Tool 3: r2r_ingest_document

**Purpose:** Upload documentation to R2R for indexing

**Input Schema:**

```json
{
  "name": "r2r_ingest_document",
  "description": "Upload a document to R2R for indexing. Supports markdown, text, PDF, and more. Returns immediately; ingestion happens asynchronously.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "file_path": {
        "type": "string",
        "description": "Absolute path to file to ingest"
      },
      "collection_id": {
        "type": "string",
        "description": "Collection ID to add document to (optional, defaults to current project)"
      },
      "metadata": {
        "type": "object",
        "description": "Custom metadata for the document"
      },
      "ingestion_mode": {
        "type": "string",
        "enum": ["hi-res", "fast", "custom"],
        "default": "fast",
        "description": "Ingestion mode: hi-res (full processing), fast (quick), custom"
      },
      "run_async": {
        "type": "boolean",
        "default": true,
        "description": "Run ingestion asynchronously (recommended)"
      }
    },
    "required": ["file_path"]
  }
}
```

**Implementation:**

```python
async def r2r_ingest_document_tool(
    file_path: str,
    collection_id: Optional[str] = None,
    metadata: Optional[Dict] = None,
    ingestion_mode: str = "fast",
    run_async: bool = True
) -> Dict[str, Any]:
    """
    Ingest document into R2R

    Returns:
        {
            "document_id": str,
            "status": "pending" | "success",
            "file_name": str,
            "collection_id": str
        }
    """
    if not collection_id:
        collection_id = await get_current_project_collection()

    # Validate file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Prepare metadata
    doc_metadata = metadata or {}
    doc_metadata["collection_id"] = collection_id
    doc_metadata["ingested_by"] = "claude-code-mcp"
    doc_metadata["ingested_at"] = datetime.utcnow().isoformat()

    try:
        # Ingest document
        response = await circuit_breaker.call(
            r2r_client.documents.create,
            file_path=file_path,
            metadata=doc_metadata,
            run_with_orchestration=run_async
        )

        document_id = response["results"]["document_id"]

        # Add to collection
        await r2r_client.collections.add_document(
            collection_id=collection_id,
            document_id=document_id
        )

        # Start background monitoring if async
        if run_async:
            asyncio.create_task(monitor_ingestion(document_id))

        return {
            "document_id": document_id,
            "status": "pending" if run_async else "success",
            "file_name": os.path.basename(file_path),
            "collection_id": collection_id
        }

    except Exception as e:
        logger.exception(f"Ingestion failed: {file_path}")
        raise
```

### Tool 4: r2r_list_documents

**Purpose:** List documents in current project collection

**Input Schema:**

```json
{
  "name": "r2r_list_documents",
  "description": "List all documents in the current project collection with their ingestion status.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "collection_id": {
        "type": "string",
        "description": "Collection ID (optional, defaults to current project)"
      },
      "offset": {
        "type": "integer",
        "default": 0,
        "minimum": 0,
        "description": "Pagination offset"
      },
      "limit": {
        "type": "integer",
        "default": 50,
        "minimum": 1,
        "maximum": 100,
        "description": "Number of documents to return"
      },
      "status_filter": {
        "type": "string",
        "enum": ["pending", "success", "failed", "all"],
        "default": "all",
        "description": "Filter by ingestion status"
      }
    }
  }
}
```

**Implementation:**

```python
async def r2r_list_documents_tool(
    collection_id: Optional[str] = None,
    offset: int = 0,
    limit: int = 50,
    status_filter: str = "all"
) -> Dict[str, Any]:
    """
    List documents in collection

    Returns:
        {
            "documents": [...],
            "total": int,
            "offset": int,
            "limit": int
        }
    """
    if not collection_id:
        collection_id = await get_current_project_collection()

    try:
        response = await circuit_breaker.call(
            r2r_client.collections.list_documents,
            collection_id=collection_id,
            offset=offset,
            limit=limit
        )

        documents = response["results"]

        # Filter by status if requested
        if status_filter != "all":
            documents = [
                doc for doc in documents
                if doc.get("ingestion_status") == status_filter
            ]

        return {
            "documents": [
                {
                    "document_id": doc["document_id"],
                    "title": doc.get("title", "Untitled"),
                    "ingestion_status": doc.get("ingestion_status", "unknown"),
                    "created_at": doc.get("created_at"),
                    "size_bytes": doc.get("size_in_bytes", 0)
                }
                for doc in documents
            ],
            "total": len(documents),
            "offset": offset,
            "limit": limit
        }

    except Exception as e:
        logger.exception("List documents failed")
        raise
```

### Tool 5: r2r_monitor_task

**Purpose:** Check status of async ingestion task

**Input Schema:**

```json
{
  "name": "r2r_monitor_task",
  "description": "Check the status of an asynchronous document ingestion task.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "document_id": {
        "type": "string",
        "description": "Document ID to check status for"
      }
    },
    "required": ["document_id"]
  }
}
```

**Implementation:**

```python
async def r2r_monitor_task_tool(document_id: str) -> Dict[str, Any]:
    """
    Monitor ingestion task status

    Returns:
        {
            "document_id": str,
            "ingestion_status": "pending" | "success" | "failed",
            "extraction_status": "pending" | "success" | "failed",
            "title": str,
            "progress": float (0.0-1.0)
        }
    """
    try:
        response = await circuit_breaker.call(
            r2r_client.documents.retrieve,
            document_id=document_id
        )

        doc = response["results"]

        # Calculate progress (heuristic)
        progress = 0.0
        if doc.get("ingestion_status") == "success":
            progress += 0.7
        elif doc.get("ingestion_status") == "pending":
            progress += 0.3

        if doc.get("extraction_status") == "success":
            progress += 0.3
        elif doc.get("extraction_status") == "pending":
            progress += 0.1

        return {
            "document_id": document_id,
            "ingestion_status": doc.get("ingestion_status", "unknown"),
            "extraction_status": doc.get("extraction_status", "unknown"),
            "title": doc.get("title", "Unknown"),
            "progress": min(progress, 1.0)
        }

    except Exception as e:
        logger.exception(f"Monitor task failed: {document_id}")
        raise
```

### Tool 6: r2r_list_collections

**Purpose:** List all available R2R collections

**Input Schema:**

```json
{
  "name": "r2r_list_collections",
  "description": "List all R2R collections accessible to the current user.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "offset": {
        "type": "integer",
        "default": 0,
        "minimum": 0
      },
      "limit": {
        "type": "integer",
        "default": 20,
        "minimum": 1,
        "maximum": 100
      }
    }
  }
}
```

**Implementation:**

```python
async def r2r_list_collections_tool(
    offset: int = 0,
    limit: int = 20
) -> Dict[str, Any]:
    """
    List R2R collections

    Returns:
        {
            "collections": [...],
            "total": int
        }
    """
    try:
        response = await circuit_breaker.call(
            r2r_client.collections.list,
            offset=offset,
            limit=limit
        )

        return {
            "collections": [
                {
                    "collection_id": c["collection_id"],
                    "name": c.get("name", "Unnamed"),
                    "description": c.get("description", ""),
                    "document_count": c.get("document_count", 0),
                    "user_count": c.get("user_count", 0)
                }
                for c in response["results"]
            ],
            "total": response.get("total_entries", len(response["results"]))
        }

    except Exception as e:
        logger.exception("List collections failed")
        raise
```

---

## Resources Specification

### Resource 1: current_project_context

**Purpose:** Provide current project metadata to Claude

**URI:** `r2r://current-project/context`

**Content:**

```json
{
  "project_name": "my-app",
  "project_path": "/home/user/my-app",
  "collection_id": "123e4567-...",
  "collection_name": "claude-code-my-app",
  "document_count": 42,
  "last_updated": "2025-11-19T10:00:00Z",
  "ingestion_status": {
    "pending": 2,
    "success": 38,
    "failed": 2
  }
}
```

### Resource 2: search_history

**Purpose:** Recent search queries for context

**URI:** `r2r://search/history`

**Content:** Last 10 search queries with timestamps

---

## Authentication Strategy

### Service Account Approach (Recommended)

**Configuration:**

```bash
# Environment variables
R2R_API_URL=http://136.119.36.216:7272
R2R_SERVICE_EMAIL=claude-code-service@example.com
R2R_SERVICE_PASSWORD=<secure-password>
```

**Implementation:**

```python
class R2RAuthManager:
    """Manages R2R authentication with automatic token refresh"""

    def __init__(self, email: str, password: str, api_url: str):
        self.email = email
        self.password = password
        self.api_url = api_url
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.token_expiry: Optional[datetime] = None
        self.lock = asyncio.Lock()

    async def get_access_token(self) -> str:
        """Get valid access token, refreshing if needed"""
        async with self.lock:
            if not self.access_token or self._is_token_expired():
                if self.refresh_token:
                    await self._refresh_access_token()
                else:
                    await self._login()

            return self.access_token

    async def _login(self):
        """Login and obtain tokens"""
        try:
            response = await r2r_client.users.login(
                email=self.email,
                password=self.password
            )

            self.access_token = response["results"]["access_token"]["token"]
            self.refresh_token = response["results"]["refresh_token"]["token"]

            # Assume 1 hour expiry (could decode JWT to get exact time)
            self.token_expiry = datetime.utcnow() + timedelta(hours=1)

            logger.info("R2R login successful")

        except Exception as e:
            logger.exception("R2R login failed")
            raise

    async def _refresh_access_token(self):
        """Refresh access token using refresh token"""
        try:
            response = await r2r_client.users.refresh_token(
                refresh_token=self.refresh_token
            )

            self.access_token = response["results"]["access_token"]["token"]
            self.refresh_token = response["results"]["refresh_token"]["token"]
            self.token_expiry = datetime.utcnow() + timedelta(hours=1)

            logger.info("R2R token refreshed")

        except Exception as e:
            logger.exception("Token refresh failed, re-logging in")
            await self._login()

    def _is_token_expired(self) -> bool:
        """Check if token is expired or about to expire"""
        if not self.token_expiry:
            return True

        # Refresh 5 minutes before expiry
        return datetime.utcnow() >= (self.token_expiry - timedelta(minutes=5))
```

---

## Caching Layer

### Redis-based Cache (Production)

**Configuration:**

```python
from redis.asyncio import Redis
import json

class RedisCache:
    """Redis-based caching with TTL support"""

    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis = Redis.from_url(redis_url, decode_responses=True)

    async def get(self, key: str) -> Optional[str]:
        """Get value from cache"""
        try:
            return await self.redis.get(key)
        except Exception as e:
            logger.warning(f"Cache get failed: {e}")
            return None

    async def set(self, key: str, value: str, ttl: int = 300):
        """Set value in cache with TTL (seconds)"""
        try:
            await self.redis.setex(key, ttl, value)
        except Exception as e:
            logger.warning(f"Cache set failed: {e}")

    async def delete(self, key: str):
        """Delete from cache"""
        try:
            await self.redis.delete(key)
        except Exception as e:
            logger.warning(f"Cache delete failed: {e}")

    async def clear_pattern(self, pattern: str):
        """Clear all keys matching pattern"""
        try:
            keys = await self.redis.keys(pattern)
            if keys:
                await self.redis.delete(*keys)
        except Exception as e:
            logger.warning(f"Cache clear failed: {e}")
```

### In-Memory Cache (Development)

```python
from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta

class InMemoryCache:
    """Simple in-memory cache with TTL"""

    def __init__(self):
        self.cache: Dict[str, Tuple[str, datetime]] = {}

    async def get(self, key: str) -> Optional[str]:
        """Get value from cache if not expired"""
        if key in self.cache:
            value, expiry = self.cache[key]
            if datetime.utcnow() < expiry:
                return value
            else:
                del self.cache[key]
        return None

    async def set(self, key: str, value: str, ttl: int = 300):
        """Set value in cache with TTL (seconds)"""
        expiry = datetime.utcnow() + timedelta(seconds=ttl)
        self.cache[key] = (value, expiry)

    async def delete(self, key: str):
        """Delete from cache"""
        self.cache.pop(key, None)

    async def clear_pattern(self, pattern: str):
        """Clear all keys matching pattern (simple prefix match)"""
        to_delete = [k for k in self.cache.keys() if k.startswith(pattern.replace("*", ""))]
        for k in to_delete:
            del self.cache[k]
```

---

## Circuit Breaker Implementation

### CircuitBreaker Class

```python
from enum import Enum
from datetime import datetime, timedelta
from typing import Callable, Any
import asyncio

class CircuitState(Enum):
    CLOSED = "closed"          # Normal operation
    OPEN = "open"              # Failing, reject requests
    HALF_OPEN = "half_open"    # Testing recovery

class CircuitBreaker:
    """Circuit breaker pattern for R2R API calls"""

    def __init__(
        self,
        failure_threshold: int = 5,
        timeout_seconds: int = 60,
        success_threshold: int = 2
    ):
        self.failure_count = 0
        self.success_count = 0
        self.failure_threshold = failure_threshold
        self.timeout_seconds = timeout_seconds
        self.success_threshold = success_threshold
        self.last_failure_time: Optional[datetime] = None
        self.state = CircuitState.CLOSED
        self.lock = asyncio.Lock()

    async def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute function through circuit breaker

        Args:
            func: Function to call
            *args, **kwargs: Arguments to pass to function

        Returns:
            Function result

        Raises:
            Exception: If circuit is OPEN or function fails
        """
        async with self.lock:
            # Check if circuit should transition to HALF_OPEN
            if self.state == CircuitState.OPEN:
                if self._should_attempt_reset():
                    logger.info("Circuit breaker: transitioning to HALF_OPEN")
                    self.state = CircuitState.HALF_OPEN
                    self.success_count = 0
                else:
                    raise Exception(
                        f"Circuit breaker is OPEN. "
                        f"R2R API unavailable. "
                        f"Retry in {self._seconds_until_reset()}s"
                    )

        # Execute function
        try:
            result = await func(*args, **kwargs)

            async with self.lock:
                if self.state == CircuitState.HALF_OPEN:
                    self.success_count += 1
                    if self.success_count >= self.success_threshold:
                        logger.info("Circuit breaker: recovered, transitioning to CLOSED")
                        self.state = CircuitState.CLOSED
                        self.failure_count = 0

                elif self.state == CircuitState.CLOSED:
                    # Reset failure count on success
                    self.failure_count = 0

            return result

        except Exception as e:
            async with self.lock:
                self.failure_count += 1
                self.last_failure_time = datetime.utcnow()

                if self.failure_count >= self.failure_threshold:
                    logger.error(
                        f"Circuit breaker: OPEN after {self.failure_count} failures"
                    )
                    self.state = CircuitState.OPEN

                if self.state == CircuitState.HALF_OPEN:
                    logger.warning("Circuit breaker: failed during HALF_OPEN, back to OPEN")
                    self.state = CircuitState.OPEN

            raise

    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset"""
        if not self.last_failure_time:
            return True

        elapsed = (datetime.utcnow() - self.last_failure_time).total_seconds()
        return elapsed >= self.timeout_seconds

    def _seconds_until_reset(self) -> int:
        """Calculate seconds until circuit can attempt reset"""
        if not self.last_failure_time:
            return 0

        elapsed = (datetime.utcnow() - self.last_failure_time).total_seconds()
        remaining = max(0, self.timeout_seconds - elapsed)
        return int(remaining)

    def get_status(self) -> Dict[str, Any]:
        """Get current circuit breaker status"""
        return {
            "state": self.state.value,
            "failure_count": self.failure_count,
            "success_count": self.success_count,
            "seconds_until_reset": self._seconds_until_reset() if self.state == CircuitState.OPEN else 0
        }
```

---

## Error Handling

### Error Response Format

```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32603,
    "message": "Internal error",
    "data": {
      "type": "R2RAPIError",
      "detail": "Connection timeout",
      "retryable": true,
      "retry_after": 30
    }
  },
  "id": "request-123"
}
```

### Error Categories

| Error Code | Category | Description | Retryable |
|------------|----------|-------------|-----------|
| -32600 | Invalid Request | Malformed JSON-RPC | No |
| -32601 | Method Not Found | Unknown method | No |
| -32602 | Invalid Params | Invalid tool arguments | No |
| -32603 | Internal Error | Server error | Maybe |
| -32001 | R2R API Error | R2R returned error | Maybe |
| -32002 | Authentication Error | Auth failed | No |
| -32003 | Circuit Breaker Open | R2R unavailable | Yes |
| -32004 | Rate Limit Exceeded | Too many requests | Yes |

### Error Handler Implementation

```python
class MCPError(Exception):
    """Base MCP error"""

    def __init__(self, code: int, message: str, data: Any = None):
        self.code = code
        self.message = message
        self.data = data
        super().__init__(message)

    def to_jsonrpc_error(self):
        """Convert to JSON-RPC error object"""
        error = {
            "code": self.code,
            "message": self.message
        }
        if self.data:
            error["data"] = self.data
        return error

class R2RAPIError(MCPError):
    """R2R API error"""
    def __init__(self, message: str, status_code: int, retryable: bool = False):
        super().__init__(
            code=-32001,
            message=f"R2R API error: {message}",
            data={
                "type": "R2RAPIError",
                "status_code": status_code,
                "retryable": retryable
            }
        )

class CircuitBreakerOpenError(MCPError):
    """Circuit breaker is open"""
    def __init__(self, retry_after: int):
        super().__init__(
            code=-32003,
            message="R2R API unavailable (circuit breaker open)",
            data={
                "type": "CircuitBreakerOpenError",
                "retryable": True,
                "retry_after": retry_after
            }
        )
```

---

## Configuration

### Configuration File (r2r_mcp_config.yaml)

```yaml
# R2R MCP Server Configuration

server:
  host: "0.0.0.0"
  port: 8080
  workers: 4
  reload: false  # Set to true for development

r2r:
  api_url: "http://136.119.36.216:7272"
  service_account:
    email: "claude-code-service@example.com"
    password: "${R2R_SERVICE_PASSWORD}"  # From environment variable

cache:
  type: "redis"  # or "memory"
  redis:
    url: "redis://localhost:6379"
    db: 0
  ttl:
    search: 300  # 5 minutes
    rag: 120     # 2 minutes
    list: 60     # 1 minute

circuit_breaker:
  failure_threshold: 5
  timeout_seconds: 60
  success_threshold: 2

logging:
  level: "INFO"
  format: "json"
  file: "/var/log/r2r_mcp/server.log"

monitoring:
  prometheus:
    enabled: true
    port: 9090
  sentry:
    enabled: false
    dsn: "${SENTRY_DSN}"

projects:
  # Auto-create collections for these projects
  auto_create_collections: true
  # Mapping file location
  collection_mapping_file: "/var/lib/r2r_mcp/project_collections.json"
```

---

## Testing Strategy

### Unit Tests

**Test Coverage:**
- ✅ JSON-RPC request/response handling
- ✅ Tool input validation
- ✅ Authentication manager (login, refresh)
- ✅ Cache layer (get, set, expiry)
- ✅ Circuit breaker state transitions
- ✅ Error handling and formatting

**Example Test:**

```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_r2r_search_tool_with_cache():
    """Test search tool with cache hit"""
    # Mock cache hit
    cache_mock = AsyncMock()
    cache_mock.get.return_value = json.dumps({
        "results": [{"text": "cached result"}],
        "count": 1,
        "cached": True
    })

    with patch("mcp_server.cache", cache_mock):
        result = await r2r_search_tool(
            query="test query",
            collection_id="test-collection"
        )

    assert result["cached"] is True
    assert result["count"] == 1
    cache_mock.get.assert_called_once()

@pytest.mark.asyncio
async def test_circuit_breaker_opens_after_failures():
    """Test circuit breaker opens after threshold failures"""
    breaker = CircuitBreaker(failure_threshold=3, timeout_seconds=60)

    async def failing_func():
        raise Exception("API error")

    # First 3 failures should go through
    for i in range(3):
        with pytest.raises(Exception):
            await breaker.call(failing_func)

    # Circuit should now be OPEN
    assert breaker.state == CircuitState.OPEN

    # Next call should fail immediately without calling function
    with pytest.raises(Exception, match="Circuit breaker is OPEN"):
        await breaker.call(failing_func)
```

### Integration Tests

**Test Scenarios:**
- ✅ Full workflow: search → cache → circuit breaker → R2R API
- ✅ Authentication flow: login → token refresh
- ✅ Document ingestion → monitoring → completion
- ✅ Error recovery scenarios

### E2E Tests

**Test Scenarios:**
- ✅ Claude Code → MCP Server → R2R → Response
- ✅ Multi-tool workflow (search → RAG → ingest)
- ✅ Session persistence across restarts

---

## Deployment

### Production Deployment (Docker)

**Dockerfile:**

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

# Run server
CMD ["uvicorn", "mcp_server:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "4"]
```

**docker-compose.yml:**

```yaml
version: '3.8'

services:
  r2r-mcp-server:
    build: .
    ports:
      - "8080:8080"
      - "9090:9090"  # Prometheus metrics
    environment:
      - R2R_API_URL=http://136.119.36.216:7272
      - R2R_SERVICE_EMAIL=claude-code-service@example.com
      - R2R_SERVICE_PASSWORD=${R2R_SERVICE_PASSWORD}
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    restart: unless-stopped
```

---

## Performance

### Expected Performance

| Operation | Target Latency | Notes |
|-----------|----------------|-------|
| Search (cached) | < 10ms | In-memory cache hit |
| Search (uncached) | < 500ms | R2R semantic search |
| RAG query (cached) | < 10ms | Cache hit |
| RAG query (uncached) | < 2s | R2R search + LLM generation |
| Document ingestion | < 100ms | Returns immediately (async) |
| List documents | < 200ms | R2R API call |

### Optimization Strategies

1. **Caching:**
   - Search results: 5 min TTL
   - RAG responses: 2 min TTL
   - Document lists: 1 min TTL

2. **Connection Pooling:**
   - Reuse HTTP connections to R2R
   - Async I/O for concurrent requests

3. **Batch Operations:**
   - Group multiple document ingestions
   - Parallel processing where possible

---

## Next Steps

1. ✅ MCP Server Specification завершён
2. ⏭️ Data Consistency Strategy
3. ⏭️ Comprehensive Testing Strategy
4. ⏭️ Implementation (Phase 5)

---

## Метаданные

- **Версия документа**: 1.0
- **Статус**: MCP Server Specification завершён
- **Complexity**: HIGH (3-4 weeks development)
- **Следующий документ**: Data Consistency Strategy
- **Готовность к implementation**: ✅ YES - спецификация полная и детальная
