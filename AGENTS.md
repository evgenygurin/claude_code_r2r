# AGENTS.md - R2R + Claude Code Integration

> **Repository Rules for Codegen Agents**
>
> This file provides instructions to AI agents working on this codebase through Codegen.
> It is automatically detected and loaded by Codegen when agents are triggered.

---

## 🎯 Project Overview

**Project:** R2R + Claude Code Integration via MCP  
**Goal:** Integrate R2R (Retrieval-Augmented Generation platform) with Claude Code  
**Status:** Phase 4 - Technical Specification (85% complete)  
**R2R Instance:** http://136.119.36.216:7272

### Architecture

This project implements a **Hybrid 5-Layer Architecture**:

1. **Layer 1:** MCP Foundation (HTTP server with 6 tools + 2 resources)
2. **Layer 2:** Hook Automation (SessionStart, PostToolUse, Stop)
3. **Layer 3:** Specialized Subagents (r2r-search with Haiku, r2r-rag with Sonnet)
4. **Layer 4:** Auto-Selected Skills (Context-based triggering)
5. **Layer 5:** Slash Commands (/r2r-search, /r2r-ask, /r2r-update-docs)

---

## 📚 Critical Documentation

**Always read these files first:**

1. **CLAUDE.md** - Primary project instructions (highest priority)
2. **docs/@analysis/README.md** - Project status and roadmap
3. **docs/@analysis/00_REVIEW.md** - Critical gaps and risks
4. **docs/@analysis/04_mcp_server_specification.md** - MCP Server architecture (1,512 lines)
5. **docs/@analysis/05_data_consistency_strategy.md** - Race condition solutions (1,033 lines)
6. **docs/@analysis/06_testing_strategy.md** - Testing approach (2,200+ lines)
7. **docs/@analysis/07_implementation_roadmap.md** - 14-week implementation plan (2,800+ lines)

**Key Technical Documents:**

- **docs/@critical/01_critical_issues.md** - Known issues and their status
- **docs/@critical/02_key_decisions.md** - Architectural decision records
- **docs/@analysis/01a_r2r_api_gaps_filled.md** - R2R API analysis
- **docs/@analysis/03_integration_mapping.md** - Integration patterns

---

## 🛠️ Development Guidelines

### Technology Stack

**Backend:**
- **Python 3.10+** (required)
- **FastAPI** - Async HTTP server for MCP
- **r2r-py SDK** - R2R API client
- **asyncio** - Async/await patterns everywhere
- **SQLite** - State tracking (file sync status)
- **Redis** - Caching (Phase 5 only, use in-memory for Phases 0-4)

**Testing:**
- **pytest** - Unit and integration tests
- **pytest-asyncio** - Async test support
- **unittest.mock** - Mocking external APIs
- **coverage** - Minimum 80% coverage required

### Code Style and Quality

**Python Style:**
```python
# ALWAYS use type hints
async def r2r_search_tool(
    query: str,
    collection_id: Optional[str] = None,
    search_mode: str = "advanced",
    limit: int = 10
) -> Dict[str, Any]:
    """
    Execute search in R2R
    
    Args:
        query: Search query (natural language)
        collection_id: Collection ID (optional)
        search_mode: Search mode (basic/advanced/custom)
        limit: Max results
        
    Returns:
        Search results with metadata
    """
    pass

# ALWAYS use async/await
async def fetch_data():
    result = await client.fetch()  # GOOD
    result = client.fetch()  # BAD - blocks event loop

# ALWAYS use structured logging
logger.info(
    "Search executed",
    extra={
        "query": query,
        "collection_id": collection_id,
        "result_count": len(results)
    }
)

# NEVER use blocking I/O
with open("file.txt") as f:  # BAD - blocks
    content = f.read()

async with aiofiles.open("file.txt") as f:  # GOOD
    content = await f.read()
```

**Docstring Format:**
```python
def my_function(arg1: str, arg2: int) -> bool:
    """
    Short description (one line)
    
    Longer description explaining what this function does,
    why it exists, and any important context.
    
    Args:
        arg1: Description of arg1
        arg2: Description of arg2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When arg2 is negative
        RuntimeError: When connection fails
        
    Example:
        >>> my_function("test", 42)
        True
    """
```

### File Organization

**Project Structure:**
```
/
├── mcp_server/              # MCP Server implementation
│   ├── __init__.py
│   ├── server.py            # FastAPI app + JSON-RPC router
│   ├── tools/               # Tool implementations
│   │   ├── search.py
│   │   ├── rag.py
│   │   ├── ingest.py
│   │   └── ...
│   ├── middleware/          # Auth, cache, circuit breaker
│   │   ├── auth.py
│   │   ├── cache.py
│   │   └── circuit_breaker.py
│   └── resources/           # MCP Resources
│       └── project_context.py
├── sync_system/             # Data consistency system
│   ├── update_queue.py
│   ├── update_worker.py
│   ├── state_tracker.py
│   └── content_hash.py
├── hooks/                   # Claude Code hooks
│   ├── session_start.py
│   ├── post_tool_use.py
│   └── stop.py
├── tests/                   # Test suite
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docs/                    # Documentation
│   ├── @analysis/           # Technical specs
│   └── @critical/           # Critical reports
├── scripts/                 # Utility scripts
└── config/                  # Configuration files
```

---

## ⚠️ Critical Implementation Rules

### 1. Data Consistency - ALWAYS Use Queue

**❌ NEVER do this:**
```python
# Direct update without queue
await r2r_client.documents.update(document_id, content)
```

**✅ ALWAYS do this:**
```python
# Queue-based update
await update_queue.enqueue(
    file_path=file_path,
    operation=Operation.UPDATE,
    content=content,
    priority=0
)
```

**Why:** Race conditions will corrupt data. See `docs/@analysis/05_data_consistency_strategy.md`

### 2. Authentication - Auto Token Refresh

**❌ NEVER do this:**
```python
# Manual token management
token = r2r_client.login(email, password)
```

**✅ ALWAYS do this:**
```python
# Use auth manager with auto-refresh
token = await auth_manager.get_access_token()
```

**Why:** Tokens expire after 1 hour. Auto-refresh prevents 401 errors.

### 3. Caching - Always Cache Search

**❌ NEVER do this:**
```python
# Direct API call without caching
results = await r2r_client.retrieval.search(query)
```

**✅ ALWAYS do this:**
```python
# Cache-aware search
cache_key = f"search:{collection_id}:{query}"
cached = await cache.get(cache_key)
if cached:
    return json.loads(cached)

results = await r2r_client.retrieval.search(query)
await cache.set(cache_key, json.dumps(results), ttl=300)
return results
```

**Why:** Search queries are expensive and often repeated.

### 4. Circuit Breaker - Always Wrap R2R Calls

**❌ NEVER do this:**
```python
# Direct call to R2R
response = await r2r_client.documents.create(file_path)
```

**✅ ALWAYS do this:**
```python
# Call through circuit breaker
response = await circuit_breaker.call(
    r2r_client.documents.create,
    file_path=file_path
)
```

**Why:** R2R may be unavailable. Circuit breaker prevents cascade failures.

### 5. Error Handling - Structured Errors

**❌ NEVER do this:**
```python
raise Exception("Something went wrong")
```

**✅ ALWAYS do this:**
```python
raise MCPError(
    code=-32001,
    message="R2R API error",
    data={
        "type": "R2RAPIError",
        "status_code": 500,
        "retryable": True
    }
)
```

**Why:** Clients need structured error information for retry logic.

---

## 🧪 Testing Requirements

### Test Coverage

**Minimum 80% coverage required** for all new code.

**Must test:**
- ✅ Happy path (normal flow)
- ✅ Error cases (API failures, timeouts, invalid input)
- ✅ Edge cases (empty inputs, large data, concurrent access)
- ✅ Idempotency (same operation multiple times)
- ✅ Race conditions (concurrent operations)

### Test Structure

```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_search_with_cache_hit():
    """Test search returns cached result when available"""
    # Arrange
    cache_mock = AsyncMock()
    cache_mock.get.return_value = json.dumps({"results": ["cached"]})
    
    # Act
    with patch("mcp_server.cache", cache_mock):
        result = await r2r_search_tool(query="test")
    
    # Assert
    assert result["cached"] is True
    cache_mock.get.assert_called_once()

@pytest.mark.asyncio
async def test_circuit_breaker_opens_after_failures():
    """Test circuit breaker opens after threshold failures"""
    # Arrange
    breaker = CircuitBreaker(failure_threshold=3)
    
    async def failing_func():
        raise Exception("API error")
    
    # Act + Assert
    for i in range(3):
        with pytest.raises(Exception):
            await breaker.call(failing_func)
    
    assert breaker.state == CircuitState.OPEN
```

---

## 🚀 Implementation Workflow

### When Adding New Features

1. **Read relevant docs** in `docs/@analysis/`
2. **Check for existing issues** in `docs/@critical/01_critical_issues.md`
3. **Write tests first** (TDD approach)
4. **Implement incrementally** (small commits)
5. **Update documentation** (inline + markdown)
6. **Run full test suite** (`pytest tests/`)
7. **Check coverage** (`pytest --cov=mcp_server tests/`)

### When Fixing Bugs

1. **Add failing test** that reproduces the bug
2. **Fix the bug** (minimal change)
3. **Verify test passes**
4. **Add regression tests** to prevent recurrence
5. **Update CHANGELOG** with fix details

### Pull Request Guidelines

**PR Title Format:**
```
[Phase N] Brief description (e.g., [Phase 1] Implement MCP search tool)
```

**PR Description Must Include:**
- What changed and why
- Which files were modified
- Testing performed
- Documentation updated
- Any breaking changes
- Link to related issue/spec

**Before Creating PR:**
- ✅ All tests pass locally
- ✅ Code coverage ≥ 80%
- ✅ No linting errors (`ruff check .`)
- ✅ Type checking passes (`mypy .`)
- ✅ Documentation updated
- ✅ CHANGELOG updated

---

## 🔐 Security and Privacy

### Never Commit Secrets

**❌ NEVER commit:**
- API keys
- Passwords
- Tokens
- Private keys
- Credentials of any kind

**✅ ALWAYS use:**
- Environment variables
- `.env` files (add to `.gitignore`)
- Secrets management (e.g., Vault)

### PII Handling

**NEVER ingest PII** to R2R without explicit user consent.

**PII includes:**
- Names
- Email addresses
- Phone numbers
- IP addresses
- Location data
- Any personally identifiable information

---

## 📊 Performance Targets

| Operation | Target Latency | Notes |
|-----------|----------------|-------|
| Search (cached) | < 10ms | In-memory cache hit |
| Search (uncached) | < 500ms | R2R semantic search |
| RAG query (cached) | < 10ms | Cache hit |
| RAG query (uncached) | < 2s | R2R search + LLM generation |
| Document ingestion | < 100ms | Returns immediately (async) |
| List documents | < 200ms | R2R API call |

**If performance degrades:**
1. Check cache hit rate (should be >50%)
2. Check R2R API latency
3. Check circuit breaker state
4. Check queue depth
5. Review logs for errors

---

## 🆘 Common Issues and Solutions

### Issue: "R2R API unavailable"

**Solution:**
1. Check circuit breaker state: `curl http://localhost:8080/health`
2. Verify R2R instance: `curl http://136.119.36.216:7272/health`
3. Check auth token: `await auth_manager.get_access_token()`
4. Review logs: `tail -f ~/.claude/r2r_sync.log`

### Issue: "Token expired" errors

**Solution:**
- Auth manager should auto-refresh tokens
- If failing, check `R2R_SERVICE_EMAIL` and `R2R_SERVICE_PASSWORD` env vars
- Verify token refresh logic in `mcp_server/middleware/auth.py`

### Issue: "File sync out of order"

**Solution:**
- Check update queue depth: `await update_queue.size()`
- Verify version numbers in state tracker
- Review queue processing in `sync_system/update_worker.py`

### Issue: "Cache not working"

**Solution:**
- Check cache backend (Redis vs in-memory)
- Verify TTL settings in config
- Review cache hit logs

---

## 📞 Getting Help

**For Codegen agents:**
- Read `CLAUDE.md` first
- Check `docs/@analysis/` for detailed specs
- Review `docs/@critical/` for known issues
- Search existing GitHub issues
- Check test files for usage examples

**For urgent issues:**
- Flag in `docs/@critical/01_critical_issues.md`
- Create GitHub issue with `critical` label
- Mention in project Slack channel

---

## ✅ Definition of Done

**A task is complete when:**
- ✅ Code implements the feature/fix as specified
- ✅ All tests pass (unit + integration + e2e)
- ✅ Code coverage ≥ 80%
- ✅ Documentation updated (inline + markdown)
- ✅ No linting/type errors
- ✅ Manual testing performed
- ✅ PR reviewed and approved
- ✅ CHANGELOG updated
- ✅ Deployed to staging (if applicable)

---

## 🚧 Current Development Status

### Completed ✅ (85%)
- ✅ R2R API Analysis
- ✅ Claude Code Integration Analysis
- ✅ Architecture Design (Hybrid 5-layer)
- ✅ MCP Server Specification (1,512 lines)
- ✅ Data Consistency Strategy (1,033 lines)
- ✅ Testing Strategy (2,200+ lines)
- ✅ Implementation Roadmap (2,800+ lines)

### In Progress 🔄 (5%)
- 🔄 Code Examples

### Pending ⏭️ (10%)
- ⏭️ Final Review and Readiness Assessment

### Deferred 🔒 (Phase 5)
- 🔒 Redis (use in-memory for now)
- 🔒 Prometheus (use logging instead)
- 🔒 Grafana (use log analysis)

---

## 📅 Implementation Timeline

```
Week 1-2:   Phase 0 - Research & Prototyping (Current)
Week 3-5:   Phase 1 - MCP Foundation (3 weeks)
Week 6-7:   Phase 2 - Core Automation (2 weeks)
Week 8-9:   Phase 3 - Specialization (2 weeks)
Week 10-11: Phase 4 - Packaging (2 weeks)
Week 12-14: Phase 5 - Production Readiness (3 weeks)
```

**Current Phase:** Phase 0 (Research & Prototyping)  
**Next Phase:** Phase 1 (MCP Foundation)  
**Estimated Completion:** Week 14

---

**Last Updated:** 2025-01-19  
**Document Version:** 1.0  
**Maintained By:** Project Owner (see git history)

---

**For Codegen Agents:**  
This file is automatically loaded by Codegen. Follow these rules strictly.  
When in doubt, ask for clarification in PR/issue comments.

**Ready for Phase 0: Prototyping** 🚀
