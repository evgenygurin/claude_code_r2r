# Infrastructure Decisions: Deferred Components

> **Документ**: Решения об отложении monitoring и caching инфраструктуры
>
> **Дата**: 2025-11-19
>
> **Статус**: APPROVED - Deferred to Phase 5

---

## Executive Summary

### Decision: Defer Production Infrastructure to Phase 5

**Components deferred:**
- 🔒 **Redis** - deferred to Phase 5 (use in-memory cache for Phases 0-4)
- 🔒 **Prometheus** - deferred to Phase 5 (use structured logging)
- 🔒 **Grafana** - deferred to Phase 5 (use structured logging)

**Rationale:**
- ✅ Reduces complexity during development and prototyping
- ✅ Faster iteration without external dependencies
- ✅ Lower infrastructure costs for Phases 0-4 ($0 vs $200-500/month)
- ✅ Same code interface - easy migration to production infrastructure
- ✅ Focus on core functionality first, add production hardening later

---

## Infrastructure Phasing Strategy

### Phase Breakdown

| Component | Phases 0-4 (Dev) | Phase 5 (Production) |
|-----------|-----------------|---------------------|
| **Cache** | In-memory cache | Redis cluster |
| **Monitoring** | Structured JSON logging | Prometheus + Grafana |
| **Metrics** | Basic counters | Full dashboards |
| **Cost** | $0/month | $200-500/month |

---

## Component Details

### 1. Redis Cache

**Status:** 🔒 DEFERRED to Phase 5

**Phases 0-4 Implementation:**
- Use **InMemoryCache** class (Python dict with TTL)
- Same interface as RedisCache
- Sufficient for development and testing
- No external dependencies

**Phase 5 Migration:**
- Switch to **RedisCache** class
- Minimal code changes (same interface)
- Configuration change: `CACHE_TYPE=redis`
- Add Redis to docker-compose.yml

**Code Example:**

```python
# Phases 0-4: In-memory cache
cache = InMemoryCache()

# Phase 5: Redis cache (same interface)
cache = RedisCache(redis_url="redis://localhost:6379")
```

**Benefits of deferring:**
- ✅ No Redis setup required for development
- ✅ Faster Docker startup (one less container)
- ✅ Simpler debugging (no network calls)
- ✅ Still validates caching logic

**Drawbacks:**
- ⚠️ Cache doesn't persist across restarts (acceptable for dev)
- ⚠️ Not suitable for multi-instance deployment (only Phase 5 needs this)

---

### 2. Prometheus Metrics

**Status:** 🔒 DEFERRED to Phase 5

**Phases 0-4 Implementation:**
- Use **structured JSON logging** to track metrics
- Basic counters in memory
- No metrics endpoint (`/metrics` not exposed)

**Phase 5 Implementation:**
- Add `prometheus_client` library
- Expose `/metrics` endpoint
- Collect metrics: request_count, latency_histogram, error_rate, cache_hit_rate
- Scrape interval: 15s

**Example Metrics (Phase 5):**

```python
from prometheus_client import Counter, Histogram

# Request metrics
request_count = Counter(
    'r2r_mcp_requests_total',
    'Total requests by tool',
    ['tool_name', 'status']
)

# Latency metrics
request_latency = Histogram(
    'r2r_mcp_request_duration_seconds',
    'Request latency in seconds',
    ['tool_name']
)
```

**Benefits of deferring:**
- ✅ No Prometheus server setup required
- ✅ Simpler codebase for Phases 0-4
- ✅ Structured logging sufficient for debugging

**Drawbacks:**
- ⚠️ No real-time dashboards (but not needed for dev)
- ⚠️ Manual log analysis required (acceptable for dev)

---

### 3. Grafana Dashboards

**Status:** 🔒 DEFERRED to Phase 5

**Phases 0-4 Implementation:**
- Use **log files** for debugging
- Basic health checks only (`/health` endpoint)

**Phase 5 Implementation:**
- Set up Grafana server
- Create dashboards:
  - MCP Server Overview (requests, latency, errors)
  - R2R API Health (circuit breaker status, API latency)
  - Cache Performance (hit rate, size)
  - Data Consistency (queue size, pending syncs)

**Example Dashboard Panels:**
- Request rate (requests/sec)
- P50, P95, P99 latency
- Error rate
- Cache hit rate
- Circuit breaker state
- Queue size over time

**Benefits of deferring:**
- ✅ No Grafana server setup required
- ✅ No dashboard configuration needed
- ✅ Simpler infrastructure for Phases 0-4

**Drawbacks:**
- ⚠️ No visual monitoring (but not needed for dev)
- ⚠️ Manual log analysis (acceptable for dev)

---

## Migration Path (Phase 4 → Phase 5)

### Step 1: Add Redis

**Docker Compose Changes:**

```yaml
# Add to docker-compose.yml
services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    restart: unless-stopped

  r2r-mcp-server:
    environment:
      - CACHE_TYPE=redis  # Change from 'memory'
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis
```

**Code Changes:**
- Update configuration to use `RedisCache`
- Test cache behavior with Redis
- Verify performance improvement

---

### Step 2: Add Prometheus

**Docker Compose Changes:**

```yaml
services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    restart: unless-stopped

  r2r-mcp-server:
    ports:
      - "9091:9091"  # Metrics endpoint
```

**Code Changes:**
- Add `prometheus_client` to requirements.txt
- Implement `/metrics` endpoint
- Add instrumentation to tools

**Prometheus Config:**

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'r2r-mcp-server'
    static_configs:
      - targets: ['r2r-mcp-server:9091']
```

---

### Step 3: Add Grafana

**Docker Compose Changes:**

```yaml
services:
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-storage:/var/lib/grafana
    restart: unless-stopped

volumes:
  grafana-storage:
```

**Configuration:**
- Add Prometheus as data source
- Import dashboards (JSON configs)
- Set up alerts

---

## Cost Analysis

### Development (Phases 0-4)

**Infrastructure:**
- Local Docker: $0
- No Redis: $0
- No Prometheus: $0
- No Grafana: $0

**Total:** **$0/month** ✅

---

### Production (Phase 5)

**Infrastructure (AWS):**
- EC2 (t3.large): $60/month
- ElastiCache Redis: $50/month
- CloudWatch (alternative to Prometheus/Grafana): $30/month
- Load Balancer: $20/month

**Alternative (self-hosted monitoring):**
- EC2 (t3.large): $60/month
- ElastiCache Redis: $50/month
- Prometheus + Grafana (same EC2): $0 extra
- Load Balancer: $20/month

**Total:** **$130-160/month** (vs $200-500 estimated)

---

## Decision Summary

### What we're NOT doing in Phases 0-4:

1. ❌ Setting up Redis server
2. ❌ Setting up Prometheus server
3. ❌ Setting up Grafana dashboards
4. ❌ Implementing `/metrics` endpoint
5. ❌ Creating monitoring dashboards
6. ❌ Setting up alerts

### What we ARE doing in Phases 0-4:

1. ✅ In-memory caching (same interface as Redis)
2. ✅ Structured JSON logging
3. ✅ Basic health checks (`/health` endpoint)
4. ✅ Error tracking in logs
5. ✅ Manual log analysis for debugging
6. ✅ Testing caching logic (unit tests)

### What we WILL do in Phase 5:

1. ✅ Migrate to Redis cache
2. ✅ Add Prometheus metrics
3. ✅ Set up Grafana dashboards
4. ✅ Configure alerts
5. ✅ Production-grade monitoring
6. ✅ Performance optimization based on metrics

---

## Documentation Updates

### Files updated:

1. ✅ `docs/@analysis/README.md`
   - Added "Deferred" section
   - Explained rationale

2. ✅ `docs/@analysis/04_mcp_server_specification.md`
   - Marked Redis as "Phase 5 only"
   - Added infrastructure decision section
   - Updated docker-compose.yml examples

3. ✅ `docs/@analysis/07_implementation_roadmap.md`
   - Updated infrastructure requirements
   - Added phasing strategy table
   - Updated cost estimates

4. ✅ `docs/@critical/05_infrastructure_decisions.md` (this document)
   - Comprehensive decision record
   - Migration path
   - Cost analysis

---

## Approval and Sign-off

**Decision Made By:** Technical Specification Team

**Date:** 2025-11-19

**Approval Status:** ✅ APPROVED

**Effective Date:** Immediate (all Phases 0-4)

**Review Date:** Before Phase 5 starts

---

## Next Steps

### Immediate (Phases 0-4):

1. ✅ Use InMemoryCache in all code
2. ✅ Use structured logging for metrics
3. ✅ Focus on core functionality
4. ✅ Test caching logic thoroughly

### Before Phase 5:

1. ⏭️ Review this decision
2. ⏭️ Plan Redis migration
3. ⏭️ Design Prometheus metrics
4. ⏭️ Create Grafana dashboard configs
5. ⏭️ Update cost estimates

---

## Метаданные

- **Версия документа**: 1.0
- **Статус**: APPROVED
- **Дата решения**: 2025-11-19
- **Reviewed by**: Technical Specification Team
- **Next Review**: Before Phase 5 (Week 12)

---

## Appendix: Quick Reference

### Configuration Flag

```bash
# Phases 0-4
CACHE_TYPE=memory

# Phase 5
CACHE_TYPE=redis
REDIS_URL=redis://localhost:6379
```

### Docker Compose

```bash
# Phases 0-4
docker-compose -f docker-compose.dev.yml up

# Phase 5
docker-compose -f docker-compose.prod.yml up
```

### Code Interface (unchanged)

```python
# Works with both InMemoryCache and RedisCache
await cache.get(key)
await cache.set(key, value, ttl=300)
await cache.delete(key)
```

---

**Decision finalized and documented.** ✅
