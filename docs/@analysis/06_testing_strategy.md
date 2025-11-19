# Testing Strategy

> **Phase 4.3**: Comprehensive testing strategy for R2R + Claude Code integration
>
> **Дата**: 2025-11-19
>
> **Цель**: Определить testing approach, coverage targets, и quality gates для всех фаз

---

## Оглавление

1. [Executive Summary](#executive-summary)
2. [Testing Pyramid](#testing-pyramid)
3. [Unit Testing](#unit-testing)
4. [Integration Testing](#integration-testing)
5. [End-to-End Testing](#end-to-end-testing)
6. [Performance Testing](#performance-testing)
7. [Security Testing](#security-testing)
8. [Test Data Management](#test-data-management)
9. [CI/CD Integration](#cicd-integration)
10. [Quality Gates](#quality-gates)
11. [Testing Tools](#testing-tools)
12. [Test Coverage Goals](#test-coverage-goals)

---

## Executive Summary

### Testing Philosophy

**Principle**: Test early, test often, test realistically

**Goals**:
- ✅ Catch bugs before production
- ✅ Enable confident refactoring
- ✅ Document expected behavior
- ✅ Prevent regressions
- ✅ Validate performance requirements

### Overall Testing Coverage Target

| Component | Unit Tests | Integration Tests | E2E Tests | Performance Tests |
|-----------|-----------|-------------------|-----------|-------------------|
| **MCP Server** | >80% | >70% | 100% critical paths | Key scenarios |
| **Hooks** | >70% | >80% | 100% workflows | All hooks |
| **Queue System** | >90% | >80% | Critical flows | Load testing |
| **State Tracker** | >90% | >70% | Recovery scenarios | N/A |
| **Auth Manager** | >85% | >70% | Token refresh | N/A |
| **Cache Layer** | >80% | >60% | Hit/miss scenarios | Performance |
| **Circuit Breaker** | >90% | >80% | Failure scenarios | N/A |

**Overall Target**: >80% code coverage across all components

---

## Testing Pyramid

### Structure

```
              ┌─────────────────┐
              │   E2E Tests     │  ← 10-15% of tests
              │   (Slow, Few)   │
              └─────────────────┘
                      △
                     ╱ ╲
                    ╱   ╲
        ┌──────────────────────┐
        │ Integration Tests    │    ← 25-30% of tests
        │ (Medium Speed)       │
        └──────────────────────┘
                  △
                 ╱ ╲
                ╱   ╲
      ┌──────────────────────────┐
      │    Unit Tests            │      ← 55-65% of tests
      │    (Fast, Many)          │
      └──────────────────────────┘
```

### Rationale

**Unit Tests (55-65%)**:
- Fast feedback (< 1s per test)
- Test isolated components
- Enable TDD (Test-Driven Development)
- Easy to debug

**Integration Tests (25-30%)**:
- Test component interactions
- Validate contracts between modules
- Catch integration bugs
- Medium speed (1-5s per test)

**E2E Tests (10-15%)**:
- Test complete user workflows
- Validate system behavior
- Slow but valuable (10-60s per test)
- Brittle but necessary

---

## Unit Testing

### MCP Server Unit Tests

#### 1. JSON-RPC Handler Tests

**File**: `tests/unit/test_jsonrpc_handler.py`

```python
import pytest
from mcp_server import handle_jsonrpc

class TestJSONRPCHandler:
    """Test JSON-RPC 2.0 request/response handling"""

    def test_valid_initialize_request(self):
        """Test valid initialize request"""
        request = {
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {"protocolVersion": "1.0"},
            "id": "1"
        }

        response = await handle_jsonrpc(request)

        assert response["jsonrpc"] == "2.0"
        assert "result" in response
        assert response["id"] == "1"
        assert response["result"]["serverInfo"]["name"] == "r2r-mcp-server"

    def test_invalid_jsonrpc_version(self):
        """Test invalid JSON-RPC version"""
        request = {
            "jsonrpc": "1.0",  # Wrong version
            "method": "initialize",
            "id": "1"
        }

        response = await handle_jsonrpc(request)

        assert "error" in response
        assert response["error"]["code"] == -32600
        assert "Invalid Request" in response["error"]["message"]

    def test_unknown_method(self):
        """Test unknown method handling"""
        request = {
            "jsonrpc": "2.0",
            "method": "unknown_method",
            "id": "1"
        }

        response = await handle_jsonrpc(request)

        assert "error" in response
        assert response["error"]["code"] == -32601
        assert "Method not found" in response["error"]["message"]

    def test_missing_required_params(self):
        """Test missing required parameters"""
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {"name": "r2r_search"},  # Missing 'arguments'
            "id": "1"
        }

        response = await handle_jsonrpc(request)

        assert "error" in response
        assert response["error"]["code"] == -32602
```

**Coverage Target**: >85%

#### 2. Tool Input Validation Tests

**File**: `tests/unit/test_tool_validation.py`

```python
import pytest
from mcp_server.tools import r2r_search_tool, r2r_rag_query_tool

class TestToolValidation:
    """Test tool input validation"""

    def test_r2r_search_valid_input(self):
        """Test valid search input"""
        result = await r2r_search_tool(
            query="test query",
            collection_id="test-collection",
            limit=10
        )

        assert "results" in result
        assert "count" in result

    def test_r2r_search_missing_query(self):
        """Test search with missing query"""
        with pytest.raises(ValueError, match="query is required"):
            await r2r_search_tool(query="")

    def test_r2r_search_invalid_limit(self):
        """Test search with invalid limit"""
        with pytest.raises(ValueError, match="limit must be between 1 and 100"):
            await r2r_search_tool(
                query="test",
                limit=200  # Too high
            )

    def test_r2r_rag_query_invalid_temperature(self):
        """Test RAG query with invalid temperature"""
        with pytest.raises(ValueError, match="temperature must be between 0.0 and 2.0"):
            await r2r_rag_query_tool(
                question="test",
                temperature=3.0  # Too high
            )
```

**Coverage Target**: >90%

#### 3. Authentication Manager Tests

**File**: `tests/unit/test_auth_manager.py`

```python
import pytest
from unittest.mock import AsyncMock, patch
from datetime import datetime, timedelta
from mcp_server.auth import R2RAuthManager

class TestAuthManager:
    """Test authentication manager"""

    @pytest.fixture
    def auth_manager(self):
        return R2RAuthManager(
            email="test@example.com",
            password="test-password",
            api_url="http://localhost:7272"
        )

    async def test_login_success(self, auth_manager):
        """Test successful login"""
        mock_response = {
            "results": {
                "access_token": {"token": "access-token-123"},
                "refresh_token": {"token": "refresh-token-456"}
            }
        }

        with patch.object(auth_manager, "_call_api", return_value=mock_response):
            await auth_manager._login()

        assert auth_manager.access_token == "access-token-123"
        assert auth_manager.refresh_token == "refresh-token-456"
        assert auth_manager.token_expiry is not None

    async def test_token_refresh(self, auth_manager):
        """Test token refresh"""
        # Set up initial state
        auth_manager.access_token = "old-token"
        auth_manager.refresh_token = "refresh-token"
        auth_manager.token_expiry = datetime.utcnow() + timedelta(minutes=1)

        mock_response = {
            "results": {
                "access_token": {"token": "new-access-token"},
                "refresh_token": {"token": "new-refresh-token"}
            }
        }

        with patch.object(auth_manager, "_call_api", return_value=mock_response):
            await auth_manager._refresh_access_token()

        assert auth_manager.access_token == "new-access-token"
        assert auth_manager.refresh_token == "new-refresh-token"

    async def test_auto_refresh_on_expiry(self, auth_manager):
        """Test automatic token refresh when expired"""
        # Set token to expire soon
        auth_manager.access_token = "old-token"
        auth_manager.refresh_token = "refresh-token"
        auth_manager.token_expiry = datetime.utcnow() + timedelta(minutes=2)

        with patch.object(auth_manager, "_refresh_access_token") as mock_refresh:
            token = await auth_manager.get_access_token()

            # Should trigger refresh (5 min buffer)
            mock_refresh.assert_called_once()

    async def test_login_failure_handling(self, auth_manager):
        """Test login failure handling"""
        with patch.object(auth_manager, "_call_api", side_effect=Exception("Auth failed")):
            with pytest.raises(Exception, match="Auth failed"):
                await auth_manager._login()

        assert auth_manager.access_token is None
```

**Coverage Target**: >85%

#### 4. Cache Layer Tests

**File**: `tests/unit/test_cache.py`

```python
import pytest
from mcp_server.cache import InMemoryCache, RedisCache
from unittest.mock import AsyncMock, patch

class TestInMemoryCache:
    """Test in-memory cache"""

    @pytest.fixture
    def cache(self):
        return InMemoryCache()

    async def test_get_set(self, cache):
        """Test basic get/set"""
        await cache.set("key1", "value1")
        result = await cache.get("key1")

        assert result == "value1"

    async def test_ttl_expiry(self, cache):
        """Test TTL expiration"""
        await cache.set("key1", "value1", ttl=1)  # 1 second TTL

        # Immediate get should work
        assert await cache.get("key1") == "value1"

        # Wait for expiry
        await asyncio.sleep(1.1)

        # Should be expired
        assert await cache.get("key1") is None

    async def test_delete(self, cache):
        """Test cache deletion"""
        await cache.set("key1", "value1")
        await cache.delete("key1")

        assert await cache.get("key1") is None

    async def test_clear_pattern(self, cache):
        """Test pattern-based clearing"""
        await cache.set("search:query1", "result1")
        await cache.set("search:query2", "result2")
        await cache.set("rag:query1", "result3")

        await cache.clear_pattern("search:*")

        assert await cache.get("search:query1") is None
        assert await cache.get("search:query2") is None
        assert await cache.get("rag:query1") == "result3"  # Not cleared

class TestRedisCache:
    """Test Redis cache (integration-like)"""

    @pytest.fixture
    async def cache(self):
        cache = RedisCache(redis_url="redis://localhost:6379/1")  # Test DB
        await cache.redis.flushdb()  # Clean test DB
        yield cache
        await cache.redis.close()

    async def test_redis_get_set(self, cache):
        """Test Redis get/set"""
        await cache.set("key1", "value1")
        result = await cache.get("key1")

        assert result == "value1"

    async def test_redis_ttl(self, cache):
        """Test Redis TTL"""
        await cache.set("key1", "value1", ttl=60)

        ttl = await cache.redis.ttl("key1")
        assert 55 < ttl <= 60  # Allow some time passage
```

**Coverage Target**: >80%

#### 5. Circuit Breaker Tests

**File**: `tests/unit/test_circuit_breaker.py`

```python
import pytest
from mcp_server.circuit_breaker import CircuitBreaker, CircuitState

class TestCircuitBreaker:
    """Test circuit breaker pattern"""

    @pytest.fixture
    def breaker(self):
        return CircuitBreaker(
            failure_threshold=3,
            timeout_seconds=5,
            success_threshold=2
        )

    async def test_closed_state_normal(self, breaker):
        """Test normal operation in CLOSED state"""
        async def success_func():
            return "success"

        result = await breaker.call(success_func)

        assert result == "success"
        assert breaker.state == CircuitState.CLOSED
        assert breaker.failure_count == 0

    async def test_open_on_threshold_failures(self, breaker):
        """Test circuit opens after threshold failures"""
        async def failing_func():
            raise Exception("Failure")

        # Trigger 3 failures
        for i in range(3):
            with pytest.raises(Exception):
                await breaker.call(failing_func)

        # Circuit should be OPEN
        assert breaker.state == CircuitState.OPEN
        assert breaker.failure_count == 3

        # Next call should fail immediately without calling function
        with pytest.raises(Exception, match="Circuit breaker is OPEN"):
            await breaker.call(failing_func)

    async def test_half_open_transition(self, breaker):
        """Test transition to HALF_OPEN after timeout"""
        async def failing_func():
            raise Exception("Failure")

        # Open the circuit
        for i in range(3):
            with pytest.raises(Exception):
                await breaker.call(failing_func)

        assert breaker.state == CircuitState.OPEN

        # Wait for timeout
        await asyncio.sleep(5.1)

        # Should transition to HALF_OPEN
        async def success_func():
            return "success"

        # First success in HALF_OPEN
        result = await breaker.call(success_func)
        assert breaker.state == CircuitState.HALF_OPEN

        # Second success should close circuit
        result = await breaker.call(success_func)
        assert breaker.state == CircuitState.CLOSED

    async def test_half_open_failure_reopens(self, breaker):
        """Test failure in HALF_OPEN reopens circuit"""
        # Open circuit
        async def failing_func():
            raise Exception("Failure")

        for i in range(3):
            with pytest.raises(Exception):
                await breaker.call(failing_func)

        # Wait for timeout
        await asyncio.sleep(5.1)

        # Fail in HALF_OPEN
        with pytest.raises(Exception):
            await breaker.call(failing_func)

        # Should be OPEN again
        assert breaker.state == CircuitState.OPEN
```

**Coverage Target**: >90%

#### 6. Update Queue Tests

**File**: `tests/unit/test_update_queue.py`

```python
import pytest
from mcp_server.queue import UpdateQueue, UpdateQueueEntry, Operation

class TestUpdateQueue:
    """Test update queue"""

    @pytest.fixture
    def queue(self):
        return UpdateQueue()

    async def test_enqueue_dequeue(self, queue):
        """Test basic enqueue/dequeue"""
        entry = await queue.enqueue(
            file_path="/test/file.md",
            operation=Operation.CREATE,
            content=b"test content"
        )

        assert entry.version == 1

        dequeued = await queue.dequeue()

        assert dequeued.file_path == "/test/file.md"
        assert dequeued.operation == Operation.CREATE
        assert dequeued.version == 1

    async def test_version_incrementing(self, queue):
        """Test version counter increments"""
        entry1 = await queue.enqueue(
            file_path="/test/file1.md",
            operation=Operation.CREATE,
            content=b"content1"
        )

        entry2 = await queue.enqueue(
            file_path="/test/file2.md",
            operation=Operation.CREATE,
            content=b"content2"
        )

        assert entry2.version == entry1.version + 1

    async def test_duplicate_detection(self, queue):
        """Test duplicate entry detection"""
        content = b"test content"

        entry1 = await queue.enqueue(
            file_path="/test/file.md",
            operation=Operation.CREATE,
            content=content
        )

        # Same file, same operation, same content
        entry2 = await queue.enqueue(
            file_path="/test/file.md",
            operation=Operation.CREATE,
            content=content
        )

        # Should return same entry (not create new)
        assert entry2.version == entry1.version

        # Queue size should be 1, not 2
        assert await queue.size() == 1

    async def test_superseding_versions(self, queue):
        """Test newer versions supersede older ones"""
        await queue.enqueue(
            file_path="/test/file.md",
            operation=Operation.CREATE,
            content=b"version 1"
        )

        await queue.enqueue(
            file_path="/test/file.md",
            operation=Operation.UPDATE,
            content=b"version 2"
        )

        # Dequeue should return only the latest version
        dequeued = await queue.dequeue()
        assert dequeued.operation == Operation.UPDATE
        assert dequeued.content_hash == hashlib.sha256(b"version 2").hexdigest()

        # Queue should be empty now
        assert await queue.size() == 0

    async def test_priority_ordering(self, queue):
        """Test priority queue ordering"""
        # Low priority
        await queue.enqueue(
            file_path="/test/file1.md",
            operation=Operation.CREATE,
            content=b"content1",
            priority=1
        )

        # High priority
        await queue.enqueue(
            file_path="/test/file2.md",
            operation=Operation.CREATE,
            content=b"content2",
            priority=10
        )

        # High priority should be dequeued first
        dequeued = await queue.dequeue()
        assert dequeued.file_path == "/test/file2.md"
```

**Coverage Target**: >90%

#### 7. State Tracker Tests

**File**: `tests/unit/test_state_tracker.py`

```python
import pytest
from mcp_server.state_tracker import StateTracker, FileState
from datetime import datetime

class TestStateTracker:
    """Test state tracker database"""

    @pytest.fixture
    async def tracker(self, tmp_path):
        db_path = tmp_path / "test_state.db"
        tracker = StateTracker(db_path=str(db_path))
        await tracker.init_db()
        return tracker

    async def test_update_and_get(self, tracker):
        """Test basic update and get"""
        await tracker.update(
            file_path="/test/file.md",
            document_id="doc-123",
            content_hash="abc123",
            version=1,
            sync_status="synced"
        )

        state = await tracker.get("/test/file.md")

        assert state is not None
        assert state.file_path == "/test/file.md"
        assert state.document_id == "doc-123"
        assert state.content_hash == "abc123"
        assert state.version == 1
        assert state.sync_status == "synced"

    async def test_update_replaces_existing(self, tracker):
        """Test update replaces existing entry"""
        await tracker.update(
            file_path="/test/file.md",
            document_id="doc-123",
            content_hash="abc123",
            version=1,
            sync_status="pending"
        )

        await tracker.update(
            file_path="/test/file.md",
            document_id="doc-123",
            content_hash="def456",
            version=2,
            sync_status="synced"
        )

        state = await tracker.get("/test/file.md")

        assert state.content_hash == "def456"
        assert state.version == 2
        assert state.sync_status == "synced"

    async def test_set_sync_status(self, tracker):
        """Test updating only sync status"""
        await tracker.update(
            file_path="/test/file.md",
            document_id="doc-123",
            content_hash="abc123",
            version=1,
            sync_status="pending"
        )

        await tracker.set_sync_status("/test/file.md", "synced")

        state = await tracker.get("/test/file.md")
        assert state.sync_status == "synced"

    async def test_delete(self, tracker):
        """Test delete"""
        await tracker.update(
            file_path="/test/file.md",
            document_id="doc-123",
            content_hash="abc123",
            version=1,
            sync_status="synced"
        )

        await tracker.delete("/test/file.md")

        state = await tracker.get("/test/file.md")
        assert state is None

    async def test_get_all_pending(self, tracker):
        """Test get all pending files"""
        await tracker.update("/test/file1.md", "doc-1", "hash1", 1, "pending")
        await tracker.update("/test/file2.md", "doc-2", "hash2", 2, "synced")
        await tracker.update("/test/file3.md", "doc-3", "hash3", 3, "pending")

        pending = await tracker.get_all_pending()

        assert len(pending) == 2
        assert all(state.sync_status == "pending" for state in pending)
```

**Coverage Target**: >90%

---

## Integration Testing

### MCP Server Integration Tests

#### 1. Full Tool Workflow Tests

**File**: `tests/integration/test_mcp_tools_integration.py`

```python
import pytest
from mcp_server import MCPServer
from r2r import R2RClient

class TestMCPToolsIntegration:
    """Integration tests for MCP tools with real R2R"""

    @pytest.fixture
    async def mcp_server(self):
        """Set up MCP server with test R2R instance"""
        server = MCPServer(
            r2r_url=os.getenv("TEST_R2R_URL", "http://localhost:7272"),
            service_email="test@example.com",
            service_password="test-password"
        )
        await server.start()
        yield server
        await server.stop()

    @pytest.fixture
    async def test_collection(self, mcp_server):
        """Create test collection"""
        collection_id = await mcp_server.r2r_client.collections.create(
            name="test-collection",
            description="Test collection"
        )
        yield collection_id
        await mcp_server.r2r_client.collections.delete(collection_id)

    async def test_ingest_and_search_workflow(self, mcp_server, test_collection, tmp_path):
        """Test complete ingest → search workflow"""
        # Create test document
        test_file = tmp_path / "test.md"
        test_file.write_text("# Test Document\n\nThis is a test document about Python programming.")

        # Step 1: Ingest document
        ingest_result = await mcp_server.tools["r2r_ingest_document"](
            file_path=str(test_file),
            collection_id=test_collection
        )

        assert "document_id" in ingest_result
        document_id = ingest_result["document_id"]

        # Step 2: Wait for ingestion to complete
        max_wait = 60  # 60 seconds
        elapsed = 0
        status = "pending"

        while elapsed < max_wait and status == "pending":
            await asyncio.sleep(5)
            elapsed += 5

            status_result = await mcp_server.tools["r2r_monitor_task"](
                document_id=document_id
            )
            status = status_result["ingestion_status"]

        assert status == "success", f"Ingestion failed or timed out: {status}"

        # Step 3: Search for document
        search_result = await mcp_server.tools["r2r_search"](
            query="Python programming",
            collection_id=test_collection,
            limit=5
        )

        assert search_result["count"] > 0
        assert any("Python" in result["text"] for result in search_result["results"])

    async def test_search_with_cache(self, mcp_server, test_collection):
        """Test search caching"""
        query = "test query"

        # First search (cache miss)
        result1 = await mcp_server.tools["r2r_search"](
            query=query,
            collection_id=test_collection
        )

        assert result1["cached"] == False

        # Second search (cache hit)
        result2 = await mcp_server.tools["r2r_search"](
            query=query,
            collection_id=test_collection
        )

        assert result2["cached"] == True

    async def test_rag_query_workflow(self, mcp_server, test_collection, tmp_path):
        """Test RAG query workflow"""
        # Ingest document first
        test_file = tmp_path / "faq.md"
        test_file.write_text("""
        # FAQ

        ## What is Python?
        Python is a high-level programming language.

        ## Why use Python?
        Python is easy to learn and has great libraries.
        """)

        await mcp_server.tools["r2r_ingest_document"](
            file_path=str(test_file),
            collection_id=test_collection
        )

        # Wait for ingestion
        await asyncio.sleep(10)

        # Ask question
        rag_result = await mcp_server.tools["r2r_rag_query"](
            question="What is Python?",
            collection_id=test_collection
        )

        assert "answer" in rag_result
        assert "programming language" in rag_result["answer"].lower()
        assert len(rag_result["sources"]) > 0

    async def test_list_documents(self, mcp_server, test_collection, tmp_path):
        """Test list documents"""
        # Ingest multiple documents
        for i in range(3):
            test_file = tmp_path / f"doc{i}.md"
            test_file.write_text(f"# Document {i}\n\nContent {i}")

            await mcp_server.tools["r2r_ingest_document"](
                file_path=str(test_file),
                collection_id=test_collection
            )

        # Wait for ingestion
        await asyncio.sleep(15)

        # List documents
        list_result = await mcp_server.tools["r2r_list_documents"](
            collection_id=test_collection
        )

        assert list_result["total"] == 3
```

**Coverage Target**: >70%

#### 2. Authentication Flow Tests

**File**: `tests/integration/test_auth_integration.py`

```python
import pytest
from mcp_server.auth import R2RAuthManager

class TestAuthIntegration:
    """Integration tests for authentication"""

    @pytest.fixture
    def auth_manager(self):
        return R2RAuthManager(
            email=os.getenv("TEST_R2R_EMAIL"),
            password=os.getenv("TEST_R2R_PASSWORD"),
            api_url=os.getenv("TEST_R2R_URL", "http://localhost:7272")
        )

    async def test_login_flow(self, auth_manager):
        """Test complete login flow"""
        token = await auth_manager.get_access_token()

        assert token is not None
        assert len(token) > 20  # JWT tokens are long
        assert auth_manager.refresh_token is not None

    async def test_token_refresh_flow(self, auth_manager):
        """Test token refresh"""
        # First login
        token1 = await auth_manager.get_access_token()

        # Force token to be "old" (set expiry to past)
        auth_manager.token_expiry = datetime.utcnow() - timedelta(hours=1)

        # Get token again (should trigger refresh)
        token2 = await auth_manager.get_access_token()

        assert token2 != token1  # Should be new token

    async def test_authenticated_api_call(self, auth_manager):
        """Test making authenticated API call"""
        token = await auth_manager.get_access_token()

        # Make API call with token
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{auth_manager.api_url}/v3/users/me",
                headers={"Authorization": f"Bearer {token}"}
            )

        assert response.status_code == 200
```

**Coverage Target**: >70%

#### 3. Circuit Breaker Integration Tests

**File**: `tests/integration/test_circuit_breaker_integration.py`

```python
import pytest
from mcp_server.circuit_breaker import CircuitBreaker
from mcp_server import MCPServer

class TestCircuitBreakerIntegration:
    """Integration tests for circuit breaker"""

    @pytest.fixture
    async def mcp_server_with_breaker(self):
        """MCP server with circuit breaker"""
        server = MCPServer(
            r2r_url=os.getenv("TEST_R2R_URL"),
            service_email="test@example.com",
            service_password="test-password",
            circuit_breaker_config={
                "failure_threshold": 3,
                "timeout_seconds": 10
            }
        )
        await server.start()
        yield server
        await server.stop()

    async def test_circuit_opens_on_r2r_failure(self, mcp_server_with_breaker):
        """Test circuit opens when R2R fails"""
        # Stop R2R or use invalid URL to simulate failure
        mcp_server_with_breaker.r2r_client.api_url = "http://invalid-url:9999"

        # Trigger failures
        for i in range(3):
            with pytest.raises(Exception):
                await mcp_server_with_breaker.tools["r2r_search"](
                    query="test",
                    collection_id="test"
                )

        # Circuit should be open
        assert mcp_server_with_breaker.circuit_breaker.state == CircuitState.OPEN

        # Next call should fail immediately
        start_time = time.time()
        with pytest.raises(Exception, match="Circuit breaker is OPEN"):
            await mcp_server_with_breaker.tools["r2r_search"](
                query="test",
                collection_id="test"
            )
        elapsed = time.time() - start_time

        assert elapsed < 1.0  # Should fail immediately, not wait for R2R

    async def test_circuit_recovers(self, mcp_server_with_breaker):
        """Test circuit recovers after R2R is back"""
        # Simulate failure
        original_url = mcp_server_with_breaker.r2r_client.api_url
        mcp_server_with_breaker.r2r_client.api_url = "http://invalid:9999"

        for i in range(3):
            with pytest.raises(Exception):
                await mcp_server_with_breaker.tools["r2r_search"](query="test")

        # Wait for timeout
        await asyncio.sleep(11)

        # Restore R2R URL
        mcp_server_with_breaker.r2r_client.api_url = original_url

        # Should recover
        result = await mcp_server_with_breaker.tools["r2r_search"](query="test")
        assert "results" in result

        # Circuit should be closed after 2 successes
        result = await mcp_server_with_breaker.tools["r2r_search"](query="test2")
        assert mcp_server_with_breaker.circuit_breaker.state == CircuitState.CLOSED
```

**Coverage Target**: >80%

---

## End-to-End Testing

### E2E Test Scenarios

#### Scenario 1: Developer Asks Question

**File**: `tests/e2e/test_developer_workflow.py`

```python
import pytest
from claude_code_testing import ClaudeCodeSession

class TestDeveloperWorkflow:
    """End-to-end tests for developer workflows"""

    @pytest.fixture
    async def claude_session(self, tmp_path):
        """Set up Claude Code session"""
        # Create test project
        project_dir = tmp_path / "test-project"
        project_dir.mkdir()

        (project_dir / "README.md").write_text("""
        # Test Project

        This is a test project for R2R integration.

        ## Setup
        Run `npm install` to install dependencies.
        """)

        # Start Claude Code session
        session = ClaudeCodeSession(working_dir=project_dir)
        await session.start()

        yield session

        await session.stop()

    async def test_ask_question_workflow(self, claude_session):
        """
        Test complete workflow:
        1. User asks question
        2. SessionStart hook loads context from R2R
        3. Claude answers using context
        """
        # Send question
        response = await claude_session.send_message(
            "How do I install dependencies for this project?"
        )

        # Verify R2R context was loaded
        assert claude_session.last_hook_executed == "UserPromptSubmit"
        assert "r2r_search" in claude_session.tools_used

        # Verify correct answer
        assert "npm install" in response.lower()

    async def test_file_modification_sync(self, claude_session):
        """
        Test file modification sync:
        1. User modifies file
        2. PostToolUse hook triggers
        3. File synced to R2R
        4. State tracker updated
        """
        # Modify file
        await claude_session.send_message(
            'Create a file docs/api.md with content "# API Documentation"'
        )

        # Wait for PostToolUse hook
        await asyncio.sleep(2)

        # Check state tracker
        state = await claude_session.mcp_server.state_tracker.get(
            str(claude_session.working_dir / "docs" / "api.md")
        )

        assert state is not None
        assert state.sync_status in ["pending", "synced"]

        # Wait for ingestion to complete
        await asyncio.sleep(10)

        # Verify in R2R
        search_result = await claude_session.mcp_server.tools["r2r_search"](
            query="API Documentation",
            collection_id=claude_session.collection_id
        )

        assert search_result["count"] > 0
```

**Coverage Target**: 100% of critical user workflows

#### Scenario 2: Session Restart Recovery

**File**: `tests/e2e/test_session_recovery.py`

```python
import pytest
from claude_code_testing import ClaudeCodeSession

class TestSessionRecovery:
    """Test session restart and recovery"""

    async def test_pending_updates_resume(self, tmp_path):
        """
        Test pending updates resume after restart:
        1. Start session
        2. Modify files
        3. Stop session before sync completes
        4. Restart session
        5. Verify pending updates resume
        """
        project_dir = tmp_path / "test-project"
        project_dir.mkdir()

        # First session
        session1 = ClaudeCodeSession(working_dir=project_dir)
        await session1.start()

        # Create file
        await session1.send_message(
            'Create file docs/test.md with content "Test"'
        )

        # Get pending state
        state_before = await session1.mcp_server.state_tracker.get(
            str(project_dir / "docs" / "test.md")
        )

        # Stop session immediately (before ingestion completes)
        await session1.stop()

        # Start new session
        session2 = ClaudeCodeSession(working_dir=project_dir)
        await session2.start()

        # SessionStart hook should resume pending updates
        assert session2.last_hook_executed == "SessionStart"

        # Wait for completion
        await asyncio.sleep(15)

        # Check state
        state_after = await session2.mcp_server.state_tracker.get(
            str(project_dir / "docs" / "test.md")
        )

        assert state_after.sync_status == "synced"

        await session2.stop()
```

#### Scenario 3: Multi-File Batch Operation

**File**: `tests/e2e/test_batch_operations.py`

```python
import pytest

class TestBatchOperations:
    """Test batch file operations"""

    async def test_bulk_documentation_ingest(self, claude_session, tmp_path):
        """
        Test bulk documentation ingestion:
        1. Create multiple docs
        2. Trigger bulk sync
        3. Verify all synced
        """
        # Create 10 documentation files
        docs_dir = claude_session.working_dir / "docs"
        docs_dir.mkdir()

        for i in range(10):
            (docs_dir / f"doc{i}.md").write_text(f"# Document {i}\n\nContent {i}")

        # Trigger bulk sync via slash command
        response = await claude_session.send_message("/r2r-update-docs")

        # Wait for completion
        await asyncio.sleep(30)

        # Verify all synced
        for i in range(10):
            state = await claude_session.mcp_server.state_tracker.get(
                str(docs_dir / f"doc{i}.md")
            )
            assert state.sync_status == "synced"
```

---

## Performance Testing

### Performance Test Suite

**File**: `tests/performance/test_performance.py`

```python
import pytest
import time
from locust import HttpUser, task, between

class TestMCPServerPerformance:
    """Performance tests for MCP server"""

    async def test_search_latency(self, mcp_server, test_collection):
        """Test search latency under load"""
        latencies = []

        for i in range(100):
            start = time.time()

            await mcp_server.tools["r2r_search"](
                query=f"test query {i}",
                collection_id=test_collection
            )

            latency = time.time() - start
            latencies.append(latency)

        # Calculate percentiles
        p50 = sorted(latencies)[50]
        p95 = sorted(latencies)[95]
        p99 = sorted(latencies)[99]

        # Performance assertions
        assert p50 < 0.5, f"P50 latency too high: {p50}s"
        assert p95 < 1.0, f"P95 latency too high: {p95}s"
        assert p99 < 2.0, f"P99 latency too high: {p99}s"

    async def test_cache_hit_rate(self, mcp_server, test_collection):
        """Test cache effectiveness"""
        queries = ["query1", "query2", "query3"] * 10  # 30 queries, many repeats

        cache_hits = 0
        cache_misses = 0

        for query in queries:
            result = await mcp_server.tools["r2r_search"](
                query=query,
                collection_id=test_collection
            )

            if result["cached"]:
                cache_hits += 1
            else:
                cache_misses += 1

        hit_rate = cache_hits / (cache_hits + cache_misses)

        assert hit_rate > 0.5, f"Cache hit rate too low: {hit_rate}"

    async def test_concurrent_requests(self, mcp_server, test_collection):
        """Test handling concurrent requests"""
        async def make_request(i):
            return await mcp_server.tools["r2r_search"](
                query=f"concurrent query {i}",
                collection_id=test_collection
            )

        # Send 50 concurrent requests
        import asyncio
        tasks = [make_request(i) for i in range(50)]

        start = time.time()
        results = await asyncio.gather(*tasks)
        elapsed = time.time() - start

        # All should succeed
        assert len(results) == 50
        assert all("results" in r for r in results)

        # Should not take too long (with circuit breaker, should be fast even if R2R slow)
        assert elapsed < 10, f"Concurrent requests too slow: {elapsed}s"

class R2RLoadTest(HttpUser):
    """Locust load test for MCP server"""

    wait_time = between(1, 3)
    host = "http://localhost:8080"

    @task(3)
    def search(self):
        """Search task (most common)"""
        self.client.post("/mcp", json={
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "r2r_search",
                "arguments": {
                    "query": "test query",
                    "collection_id": "test-collection"
                }
            },
            "id": "1"
        })

    @task(1)
    def rag_query(self):
        """RAG query task"""
        self.client.post("/mcp", json={
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "r2r_rag_query",
                "arguments": {
                    "question": "What is this?",
                    "collection_id": "test-collection"
                }
            },
            "id": "2"
        })

# Run with: locust -f tests/performance/test_performance.py --host=http://localhost:8080 --users=50 --spawn-rate=10
```

### Performance Benchmarks

| Operation | Target | Acceptable | Bad |
|-----------|--------|------------|-----|
| **Search (cached)** | < 10ms | < 50ms | > 100ms |
| **Search (uncached)** | < 500ms | < 1s | > 2s |
| **RAG query (cached)** | < 10ms | < 50ms | > 100ms |
| **RAG query (uncached)** | < 2s | < 5s | > 10s |
| **Document ingest (async)** | < 100ms | < 500ms | > 1s |
| **List documents** | < 200ms | < 500ms | > 1s |
| **Cache hit rate** | > 50% | > 30% | < 20% |
| **Concurrent requests (50)** | < 5s | < 10s | > 20s |

---

## Security Testing

### Security Test Suite

**File**: `tests/security/test_security.py`

```python
import pytest
from mcp_server import MCPServer

class TestSecurity:
    """Security tests"""

    async def test_no_credentials_in_logs(self, mcp_server, caplog):
        """Test credentials not logged"""
        await mcp_server.start()

        # Check logs
        for record in caplog.records:
            assert "password" not in record.message.lower()
            assert mcp_server.auth_manager.password not in record.message

    async def test_sql_injection_protection(self, mcp_server):
        """Test SQL injection protection in state tracker"""
        malicious_path = "'; DROP TABLE file_state; --"

        await mcp_server.state_tracker.update(
            file_path=malicious_path,
            document_id="doc-123",
            content_hash="hash",
            version=1,
            sync_status="synced"
        )

        # Should not break database
        state = await mcp_server.state_tracker.get(malicious_path)
        assert state is not None
        assert state.file_path == malicious_path

    async def test_path_traversal_protection(self, mcp_server, tmp_path):
        """Test path traversal protection"""
        malicious_path = "../../etc/passwd"

        with pytest.raises(ValueError, match="Invalid file path"):
            await mcp_server.tools["r2r_ingest_document"](
                file_path=malicious_path,
                collection_id="test"
            )

    async def test_unauthorized_collection_access(self, mcp_server):
        """Test unauthorized collection access prevention"""
        # Try to access collection that doesn't belong to user
        with pytest.raises(Exception, match="Unauthorized"):
            await mcp_server.tools["r2r_search"](
                query="test",
                collection_id="someone-elses-collection"
            )

    async def test_rate_limiting(self, mcp_server):
        """Test rate limiting (if implemented)"""
        # Make many requests quickly
        for i in range(200):
            try:
                await mcp_server.tools["r2r_search"](
                    query=f"test {i}",
                    collection_id="test"
                )
            except Exception as e:
                if "rate limit" in str(e).lower():
                    # Rate limiting working
                    return

        pytest.fail("Rate limiting not working")
```

---

## Test Data Management

### Test Fixtures

**File**: `tests/fixtures.py`

```python
import pytest
from pathlib import Path

@pytest.fixture
def sample_markdown_files(tmp_path):
    """Create sample markdown files"""
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()

    files = {
        "README.md": "# Project\n\nMain readme",
        "API.md": "# API Docs\n\nAPI documentation",
        "GUIDE.md": "# User Guide\n\nHow to use this"
    }

    for name, content in files.items():
        (docs_dir / name).write_text(content)

    return docs_dir

@pytest.fixture
def sample_code_files(tmp_path):
    """Create sample code files"""
    src_dir = tmp_path / "src"
    src_dir.mkdir()

    files = {
        "main.py": "def main():\n    print('Hello')",
        "utils.py": "def helper():\n    return 42",
        "config.py": "CONFIG = {'key': 'value'}"
    }

    for name, content in files.items():
        (src_dir / name).write_text(content)

    return src_dir

@pytest.fixture
async def test_r2r_collection(r2r_client):
    """Create and cleanup test R2R collection"""
    collection_id = await r2r_client.collections.create(
        name=f"test-{uuid.uuid4()}",
        description="Test collection"
    )

    yield collection_id

    # Cleanup
    try:
        await r2r_client.collections.delete(collection_id)
    except:
        pass  # Collection may have been deleted by test
```

### Test Data Generation

**File**: `tests/test_data_generator.py`

```python
def generate_test_documents(count: int, tmp_path: Path) -> list[Path]:
    """Generate test documents"""
    docs = []

    for i in range(count):
        doc_path = tmp_path / f"doc{i}.md"
        doc_path.write_text(f"""
# Document {i}

## Section 1
Content for section 1 of document {i}.

## Section 2
Content for section 2 of document {i}.
        """)
        docs.append(doc_path)

    return docs

def generate_large_document(tmp_path: Path, size_mb: float) -> Path:
    """Generate large document for testing"""
    doc_path = tmp_path / "large_doc.md"

    content = "# Large Document\n\n"
    content += "Lorem ipsum " * 100000  # ~1MB

    # Scale to desired size
    target_size = int(size_mb * 1024 * 1024)
    current_size = len(content.encode())
    multiplier = target_size // current_size + 1

    doc_path.write_text(content * multiplier)

    return doc_path
```

---

## CI/CD Integration

### GitHub Actions Workflow

**File**: `.github/workflows/test.yml`

```yaml
name: Test Suite

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.10, 3.11]

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-test.txt

    - name: Run unit tests
      run: |
        pytest tests/unit/ -v --cov=mcp_server --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  integration-tests:
    runs-on: ubuntu-latest
    services:
      redis:
        image: redis:7
        ports:
          - 6379:6379
      r2r:
        image: r2r-test:latest
        ports:
          - 7272:7272
        env:
          POSTGRES_HOST: postgres
          POSTGRES_DB: r2r_test
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: r2r_test
        ports:
          - 5432:5432

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-test.txt

    - name: Wait for services
      run: |
        sleep 10

    - name: Run integration tests
      env:
        TEST_R2R_URL: http://localhost:7272
        TEST_R2R_EMAIL: test@example.com
        TEST_R2R_PASSWORD: test-password
      run: |
        pytest tests/integration/ -v

  e2e-tests:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install Claude Code
      run: |
        curl -fsSL https://claude.ai/install.sh | bash

    - name: Set up test environment
      run: |
        docker-compose -f docker-compose.test.yml up -d
        sleep 15

    - name: Run E2E tests
      run: |
        pytest tests/e2e/ -v --timeout=300

    - name: Cleanup
      if: always()
      run: |
        docker-compose -f docker-compose.test.yml down

  performance-tests:
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'

    steps:
    - uses: actions/checkout@v3

    - name: Set up environment
      run: |
        docker-compose -f docker-compose.test.yml up -d

    - name: Run performance tests
      run: |
        pip install locust
        locust -f tests/performance/test_performance.py --host=http://localhost:8080 --users=50 --spawn-rate=10 --run-time=5m --headless

    - name: Upload results
      uses: actions/upload-artifact@v3
      with:
        name: performance-results
        path: locust_report.html
```

---

## Quality Gates

### Quality Gates Definition

| Gate | Criteria | Block Merge? |
|------|----------|--------------|
| **Unit Test Coverage** | > 80% | ✅ YES |
| **Integration Test Pass** | 100% pass | ✅ YES |
| **E2E Test Pass** | 100% critical paths pass | ✅ YES |
| **Performance Regression** | < 20% degradation | ⚠️  Warning |
| **Security Scan** | No critical vulnerabilities | ✅ YES |
| **Linting** | No errors, < 10 warnings | ⚠️  Warning |
| **Type Checking** | No type errors | ✅ YES |

### Pre-commit Hooks

**File**: `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
      - id: black

  - repo: https://github.com/PyCQA/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: ['--max-line-length=100']

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.0.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]

  - repo: local
    hooks:
      - id: unit-tests
        name: Unit Tests
        entry: pytest tests/unit/ -v
        language: system
        pass_filenames: false
        always_run: true
```

---

## Testing Tools

### Tool Stack

| Tool | Purpose | Version |
|------|---------|---------|
| **pytest** | Test framework | ≥ 7.0 |
| **pytest-asyncio** | Async test support | ≥ 0.21 |
| **pytest-cov** | Coverage reporting | ≥ 4.0 |
| **pytest-mock** | Mocking | ≥ 3.10 |
| **pytest-timeout** | Test timeouts | ≥ 2.1 |
| **httpx** | HTTP client testing | ≥ 0.24 |
| **locust** | Load testing | ≥ 2.14 |
| **faker** | Test data generation | ≥ 18.0 |
| **freezegun** | Time mocking | ≥ 1.2 |

### pytest Configuration

**File**: `pytest.ini`

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --verbose
    --strict-markers
    --disable-warnings
    --cov=mcp_server
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
    --asyncio-mode=auto
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    performance: Performance tests
    security: Security tests
    slow: Slow running tests
timeout = 300
```

---

## Test Coverage Goals

### Coverage Targets by Phase

**Phase 0 (Prototype)**:
- Unit tests: > 60%
- Integration tests: Key workflows only
- E2E tests: Happy path

**Phase 1 (MCP Foundation)**:
- Unit tests: > 80%
- Integration tests: > 70%
- E2E tests: All critical paths

**Phase 2 (Core Automation)**:
- Unit tests: > 85%
- Integration tests: > 75%
- E2E tests: All workflows

**Phase 5 (Production)**:
- Unit tests: > 90%
- Integration tests: > 80%
- E2E tests: 100% user scenarios
- Performance tests: Comprehensive
- Security tests: Complete

### Coverage Reporting

**Generate coverage report**:

```bash
# HTML report
pytest --cov=mcp_server --cov-report=html
open htmlcov/index.html

# Terminal report
pytest --cov=mcp_server --cov-report=term-missing

# XML report (for CI)
pytest --cov=mcp_server --cov-report=xml
```

---

## Summary

### Testing Completeness

| Component | Documented | Implementation Ready |
|-----------|-----------|---------------------|
| **Unit Tests** | ✅ Complete | ✅ Ready to implement |
| **Integration Tests** | ✅ Complete | ✅ Ready to implement |
| **E2E Tests** | ✅ Complete | ✅ Ready to implement |
| **Performance Tests** | ✅ Complete | ✅ Ready to implement |
| **Security Tests** | ✅ Complete | ✅ Ready to implement |
| **CI/CD** | ✅ Complete | ✅ Ready to implement |
| **Quality Gates** | ✅ Complete | ✅ Ready to implement |

### Next Steps

1. ✅ Testing Strategy завершена
2. ⏭️ Implementation Roadmap (Phase 4.4)
3. ⏭️ Code Examples (Phase 4.5)

**Готовность к Phase 0 (Prototyping)**: ✅ **10/10**

---

## Метаданные

- **Версия документа**: 1.0
- **Статус**: Testing Strategy завершена
- **Coverage Target**: >80% overall
- **Следующий документ**: Implementation Roadmap
- **Готовность**: ✅ YES - полная testing стратегия определена
