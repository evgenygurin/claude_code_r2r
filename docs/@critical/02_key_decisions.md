# Ключевые архитектурные решения

> **Документ**: Критические decision points и их обоснование
>
> **Дата**: 2025-11-19
>
> **Цель**: Объяснить WHY, а не только WHAT

---

## Executive Summary

Этот документ описывает **7 ключевых архитектурных решений**, которые определяют success интеграции R2R + Claude Code.

Каждое решение включает:
- **Context**: Почему это решение важно?
- **Options**: Какие были альтернативы?
- **Decision**: Что выбрали?
- **Rationale**: Почему именно это?
- **Trade-offs**: Что gained, что lost?
- **Consequences**: Какие implications?

---

## Decision #1: Hybrid Architecture (5-layer)

### Context

Нужно выбрать architecture pattern для интеграции. Есть 4 варианта:
1. MCP-Centric (все через MCP tools)
2. Hook-Driven (все через hooks automation)
3. Subagent Delegation (специализированные агенты)
4. Hybrid (комбинация всех подходов)

### Options Evaluated

| Option | Pros | Cons | Score |
|--------|------|------|-------|
| MCP-Centric | Simple, unified interface | No automation, manual calls | 6/10 |
| Hook-Driven | Full automation, no user action | Less control, magic behavior | 7/10 |
| Subagent Delegation | Specialized, optimized | Complexity, coordination | 7/10 |
| **Hybrid** | Best of all worlds | Higher complexity | **9/10** |

### Decision

✅ **Hybrid Architecture (5-layer)**

```
Layer 1: MCP Foundation (tools + resources)
Layer 2: Hook Automation (SessionStart, PostToolUse, Stop)
Layer 3: Specialized Subagents (search, RAG, docs-manager)
Layer 4: Auto-Selected Skills (contextual triggering)
Layer 5: Slash Commands (user interface)
```

### Rationale

**Why Hybrid?**

1. **Flexibility**: Supports multiple use cases
   - Automatic (hooks)
   - Manual (commands)
   - Contextual (skills)

2. **Optimization**: Right tool для right job
   - Fast search → Haiku subagent
   - Deep analysis → Sonnet subagent
   - Background work → Hooks

3. **User Control**: Balance automation vs control
   - Auto-ingest for convenience
   - Manual commands when needed
   - Explicit control available

4. **Extensibility**: Easy to add new capabilities
   - New tool → add to MCP
   - New automation → add hook
   - New workflow → add subagent

### Trade-offs

**Gained:**
- ✅ Maximum flexibility
- ✅ Optimized performance (model selection)
- ✅ User control + automation
- ✅ Easy to extend

**Lost:**
- ❌ Higher complexity (5 layers vs 1)
- ❌ More code to maintain
- ❌ Steeper learning curve
- ❌ More potential failure points

### Consequences

**Implementation:**
- Development time: +2 weeks (vs MCP-only)
- Code size: ~2x larger
- Testing: More integration tests needed

**Operations:**
- Debugging: Need to trace через layers
- Monitoring: More metrics to track
- Documentation: More to explain

**Decision**: Trade-offs acceptable, benefits outweigh costs

---

## Decision #2: Service Account Authentication

### Context

Нужно решить как authenticate с R2R API. Есть 2 подхода:
1. Service Account (один R2R user для всех Claude Code operations)
2. Per-User Mapping (каждый Claude Code user → свой R2R user)

### Options Evaluated

**Option A: Service Account**
```
Pros:
- Simple setup (один account)
- Centralized credential management
- No user onboarding needed
- Easy to audit (all actions под one account)

Cons:
- No per-user permissions
- All operations logged под service account
- Can't track individual user actions в R2R
```

**Option B: Per-User Mapping**
```
Pros:
- Per-user permissions possible
- Audit trail by user
- Finer-grained access control

Cons:
- Complex setup (create R2R account для каждого user)
- Credential management nightmare
- Onboarding friction
- Mapping maintenance overhead
```

### Decision

✅ **Service Account** (with optional per-user mapping для future)

**Configuration:**
```bash
R2R_SERVICE_EMAIL=claude-code-service@example.com
R2R_SERVICE_PASSWORD=<stored in vault>
```

### Rationale

**Why Service Account?**

1. **Simplicity**: One-time setup vs continuous maintenance
2. **Claude Code Context**: В большинстве сценариев Claude Code = single user tool
3. **Isolation через Collections**: Per-project isolation достигается через collections, не через users
4. **Low Friction**: No user onboarding process
5. **Sufficient для MVP**: Can add per-user mapping later если нужно

**When Per-User Mapping Makes Sense:**
- Multi-user Claude Code deployment
- Требуется audit trail по users
- Compliance требует user-level permissions
- Shared projects с different access levels

### Trade-offs

**Gained:**
- ✅ Simple setup и maintenance
- ✅ Low friction для users
- ✅ Centralized credential management
- ✅ Easy to audit (one place)

**Lost:**
- ❌ No per-user permissions в R2R
- ❌ Can't differentiate users в R2R logs
- ❌ All users = same access level

### Consequences

**Implementation:**
- `R2RAuthManager` class с auto token refresh
- Environment variables для credentials
- Secret management (Vault, etc.) для production

**Migration Path:**
Если нужно per-user mapping в будущем:
```python
# Easy to extend
class PerUserAuthManager(R2RAuthManager):
    def get_credentials_for_user(self, user_id):
        # Lookup user-specific credentials
        pass
```

**Decision**: Service Account для MVP, per-user as optional enhancement

---

## Decision #3: Queue-Based Update System

### Context

Нужно решить problem of race conditions при file modifications. Есть несколько подходов:
1. File Locks
2. Timestamps
3. Queue + Versioning
4. Event Sourcing

### Options Evaluated

**Option A: File Locks**
```python
with file_lock(file_path):
    upload_to_r2r(file_path)

Pros:
- Simple concept
- Prevents concurrent access

Cons:
- ❌ Doesn't work с async operations
- ❌ Lock released before R2R upload completes
- ❌ No protection against network delays
- ❌ Deadlock риски
```

**Option B: Timestamps**
```python
if file_modified_at > last_upload_at:
    upload_to_r2r(file_path)

Pros:
- Simple implementation
- No locks needed

Cons:
- ❌ Unreliable with network delays
- ❌ Clock skew issues
- ❌ Race window still exists
- ❌ No ordering guarantees
```

**Option C: Queue + Versioning** ⭐
```python
queue.enqueue(
    file=file_path,
    operation=update,
    version=increment(),
    hash=sha256(content)
)

Pros:
- ✅ Serializes updates
- ✅ Version ordering
- ✅ Content-based deduplication
- ✅ Works with async

Cons:
- More complex implementation
- Requires background worker
- Requires state database
```

**Option D: Event Sourcing**
```
Pros:
- Complete audit trail
- Time travel possible
- Event replay

Cons:
- ❌ Massive complexity
- ❌ Overkill для use case
- ❌ Storage overhead
```

### Decision

✅ **Queue + Versioning** (Option C)

**Architecture:**
```
File Modified
  ↓
Compute Hash (SHA-256)
  ↓
Enqueue (file, operation, version, hash)
  ↓
UpdateWorker (background)
  ↓
Process Serially (check hash, execute, verify)
  ↓
Update StateTracker
```

### Rationale

**Why Queue + Versioning?**

1. **Solves Race Conditions**: Queue serialization = no concurrent updates
2. **Ordering Guarantee**: Version numbers = correct order даже при network delays
3. **Idempotency**: Content hashing = skip if not changed
4. **Session Continuity**: State tracking = resume после restart
5. **Proven Pattern**: Queue = well-understood solution

**Why Not Others?**
- File Locks: Can't handle async operations
- Timestamps: Unreliable с network
- Event Sourcing: Too complex

### Trade-offs

**Gained:**
- ✅ Complete race condition elimination
- ✅ Idempotent operations
- ✅ Audit trail (версии)
- ✅ Session persistence

**Lost:**
- ❌ Added complexity (queue + worker + state DB)
- ❌ More code to maintain
- ❌ Potential bottleneck (serial processing)

### Consequences

**Components to Implement:**
- `UpdateQueue` (priority queue class)
- `UpdateWorker` (background task)
- `StateTracker` (SQLite database)
- Content hashing utility

**Performance Implications:**
- Serial processing = potential bottleneck
- Mitigated by: content hashing (skip unchanged)
- Mitigated by: priority queue (urgent first)

**Testing Requirements:**
- Unit tests для queue operations
- Integration tests для race scenarios
- Load tests для bottleneck assessment

**Decision**: Benefits (correctness) outweigh costs (complexity)

---

## Decision #4: Redis Caching (with In-Memory Fallback)

### Context

Нужно выбрать caching solution для performance optimization.

### Options Evaluated

| Option | Pros | Cons | Score |
|--------|------|------|-------|
| No Cache | Simple | Poor performance | 2/10 |
| In-Memory | Simple, fast | Lost on restart | 6/10 |
| Redis | Persistent, scalable | External dependency | 9/10 |
| Memcached | Fast, simple | No persistence | 7/10 |

### Decision

✅ **Redis (Production) + In-Memory (Development)**

**Configuration:**
```yaml
cache:
  type: "redis"  # or "memory" for dev
  redis:
    url: "redis://localhost:6379"
    db: 0
  ttl:
    search: 300  # 5 minutes
    rag: 120     # 2 minutes
    list: 60     # 1 minute
```

### Rationale

**Why Redis?**

1. **Persistence**: Cache survives restarts
2. **Scalability**: Can add Redis cluster если нужно
3. **Standard**: Industry-standard solution
4. **Features**: TTL, eviction policies, pub/sub

**Why In-Memory для Dev?**

1. **Zero Dependencies**: Разработчики не нужно setup Redis
2. **Fast Iteration**: Быстрее для local testing
3. **Same Interface**: Code работает с обоими

**Why Not Memcached?**

- No persistence (lost on restart)
- Redis = superset of features

### Trade-offs

**Gained:**
- ✅ 50%+ requests served from cache
- ✅ <10ms latency для cache hits
- ✅ Reduced R2R API load
- ✅ Persistent cache (Redis)

**Lost:**
- ❌ External dependency (Redis)
- ❌ Memory usage
- ❌ Potential stale data

### Mitigation

**Stale Data:**
- Short TTL (2-5 minutes)
- Cache invalidation on updates

**Memory Usage:**
- Eviction policy (LRU)
- Max memory limit
- Monitor usage

---

## Decision #5: Circuit Breaker Pattern

### Context

R2R API может быть temporarily unavailable. Нужно handle gracefully.

### Options Evaluated

**Option A: Naive Retries**
```python
for i in range(10):
    try:
        return r2r_api.search(query)
    except:
        time.sleep(5)  # Try again
```
❌ Waste resources, poor UX

**Option B: Exponential Backoff**
```python
for i in range(5):
    try:
        return r2r_api.search(query)
    except:
        time.sleep(2 ** i)  # 2, 4, 8, 16, 32s
```
⚠️ Better, но still wastes time

**Option C: Circuit Breaker** ⭐
```python
circuit_breaker.call(r2r_api.search, query)
# Fails fast if OPEN
# Auto-recovery when available
```
✅ Best pattern

### Decision

✅ **Circuit Breaker (3-state)**

**States:**
- CLOSED: Normal (all requests through)
- OPEN: Failing (reject immediately)
- HALF_OPEN: Testing (1 request at a time)

**Configuration:**
```python
CircuitBreaker(
    failure_threshold=5,      # 5 failures → OPEN
    timeout_seconds=60,       # Wait 60s before test
    success_threshold=2       # 2 successes → CLOSED
)
```

### Rationale

**Why Circuit Breaker?**

1. **Fast Failure**: No waiting 30s для timeout
2. **Auto-Recovery**: Tests periodically
3. **User Feedback**: "R2R unavailable, retry in 30s"
4. **Prevent Cascade**: Stops failures propagating
5. **Standard Pattern**: Well-understood, proven

### Consequences

**Must Implement в Phase 1:**
- Critical для any production use
- Easy to add early, hard to retrofit

**User Experience:**
```
Without CB:
- Request 1: timeout (30s)
- Request 2: timeout (30s)
- Request 3: timeout (30s)
Total: 90s wasted

With CB:
- Request 1: timeout (30s) → OPEN
- Request 2: fail fast (<1ms) "R2R unavailable"
- Request 3: fail fast (<1ms)
Total: 30s, clear feedback
```

---

## Decision #6: SQLite for State Tracking

### Context

Нужно persistent storage для file → document_id mapping.

### Options Evaluated

**Option A: JSON File**
```json
{
  "docs/api.md": {
    "document_id": "123",
    "hash": "abc...",
    "version": 5
  }
}
```
❌ No transactions, race conditions

**Option B: SQLite**
```sql
CREATE TABLE file_state (
  file_path TEXT PRIMARY KEY,
  document_id TEXT,
  content_hash TEXT,
  version INTEGER
);
```
✅ ACID, transactions, queries

**Option C: PostgreSQL**
```
Too heavy for local state
```

### Decision

✅ **SQLite**

**Location:**
```
~/.claude/r2r_sync_state.db
```

### Rationale

**Why SQLite?**

1. **ACID Transactions**: No race conditions
2. **Zero Setup**: Single file, no server
3. **SQL Queries**: Powerful querying
4. **Reliable**: Battle-tested
5. **Lightweight**: Perfect для local state

**Why Not JSON?**
- No transactions
- Race conditions
- Manual locking needed

**Why Not PostgreSQL?**
- Too heavy для local state
- Requires server setup
- Overkill

### Schema

```sql
CREATE TABLE file_state (
    file_path TEXT PRIMARY KEY,
    document_id TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    version INTEGER NOT NULL,
    last_synced TEXT NOT NULL,
    sync_status TEXT NOT NULL CHECK (
        sync_status IN ('pending', 'synced', 'failed')
    )
);

CREATE INDEX idx_sync_status ON file_state(sync_status);
CREATE INDEX idx_last_synced ON file_state(last_synced);
```

---

## Decision #7: Complexity Re-assessment

### Context

Initial estimate: MCP Server = Medium complexity, 1 week

After detailed design: Actually HIGH complexity

### Decision

✅ **Re-assess to HIGH, extend timeline to 3-4 weeks**

### Rationale

**Why Re-assess?**

**Full scope includes:**
1. HTTP server (FastAPI)
2. JSON-RPC 2.0 protocol
3. 6 tools implementation
4. Auth manager с auto-refresh
5. Caching layer (Redis integration)
6. Circuit breaker (3-state machine)
7. Error handling framework
8. Structured logging
9. Prometheus metrics
10. Comprehensive testing
11. Docker deployment

**Lesson Learned:**
- Initial estimates often underestimate non-functional requirements
- "Simple HTTP server" = deceptive
- Testing + deployment = significant effort

**Impact:**
- Timeline: +2-3 weeks
- Resources: Requires experienced developer
- Quality: More time = better quality

**Decision**: Honesty > optimism

Better to revise estimate early than slip timeline later

---

## Summary Table

| Decision | Chosen Option | Alternative | Key Reason |
|----------|---------------|-------------|------------|
| #1 Architecture | Hybrid (5-layer) | MCP-only | Flexibility + Optimization |
| #2 Authentication | Service Account | Per-User | Simplicity для MVP |
| #3 Data Consistency | Queue + Versioning | File Locks | Handles async correctly |
| #4 Caching | Redis + In-Memory | Memcached | Persistence + Dev ease |
| #5 Resilience | Circuit Breaker | Naive Retry | Fast failure + auto-recovery |
| #6 State Storage | SQLite | JSON File | ACID transactions |
| #7 Estimation | HIGH (3-4 weeks) | Medium (1 week) | Realistic assessment |

---

## Decision Process

### How Were Decisions Made?

1. **Identify Options**: List all reasonable alternatives
2. **Evaluate Pros/Cons**: Honest assessment
3. **Score**: Quantitative comparison
4. **Prototype**: Test critical assumptions (Phase 0)
5. **Decide**: Choose best option
6. **Document**: Capture rationale
7. **Review**: Validate with team

### Decision Criteria

**Weighted Priorities:**
1. **Correctness** (40%): Does it work reliably?
2. **Simplicity** (20%): Easy to understand/maintain?
3. **Performance** (15%): Fast enough?
4. **Extensibility** (15%): Can it grow?
5. **Cost** (10%): Resource efficient?

---

## Lessons Learned

### What Worked Well

1. **Critical Thinking**: Questioning assumptions
2. **Gap Analysis**: Finding missing pieces
3. **Trade-off Analysis**: Honest pros/cons
4. **Prototype Plan**: Validate before commit
5. **Timeline Honesty**: Revise estimates early

### What to Improve

1. **Earlier Prototyping**: Should test assumptions earlier
2. **Stakeholder Input**: Get feedback on key decisions
3. **Documentation**: Document decisions as made, not after

---

## Метаданные

- **Version:** 1.0
- **Last Updated:** 2025-11-19
- **Total Decisions:** 7 major, 15+ minor
- **Consensus:** Team review recommended
- **Next Review:** After Phase 0 prototype
