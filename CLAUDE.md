# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🎯 Проект: R2R + Claude Code Integration

**Цель**: Интегрировать R2R (Retrieval-Augmented Generation платформу) с Claude Code через Model Context Protocol (MCP) для:
- Автоматической индексации документации проекта
- Семантического поиска по кодовой базе и документации
- RAG-powered ответов на вопросы о проекте
- Работы в фоновом режиме без блокировки пользователя

**Статус**: Phase 4 - Technical Specification (85% завершено)

**R2R Instance**: http://136.119.36.216:7272

## 🏗️ Архитектура: Hybrid 5-Layer

```text
Layer 1: MCP Foundation → HTTP server с 6 tools + 2 resources
Layer 2: Hook Automation → SessionStart, PostToolUse, Stop
Layer 3: Specialized Subagents → r2r-search (Haiku), r2r-rag (Sonnet)
Layer 4: Auto-Selected Skills → Контекстное срабатывание
Layer 5: Slash Commands → /r2r-search, /r2r-ask, /r2r-update-docs
```

## 📚 Структура документации

```text
docs/
├── @analysis/              # Техническая спецификация (11,500+ строк)
│   ├── README.md           # Статус проекта и roadmap
│   ├── 00_REVIEW.md        # Критический обзор (15 gaps, 5 рисков)
│   ├── 01_r2r_capabilities.md          # R2R API анализ
│   ├── 01a_r2r_api_gaps_filled.md      # Заполненные пробелы API
│   ├── 02_claude_code_capabilities.md  # 7 механизмов расширения
│   ├── 03_integration_mapping.md       # Архитектурные паттерны
│   ├── 04_mcp_server_specification.md  # MCP Server (1,512 строк)
│   ├── 05_data_consistency_strategy.md # Race conditions (1,033 строк)
│   ├── 06_testing_strategy.md          # Testing approach (2,200+ строк)
│   └── 07_implementation_roadmap.md    # 14-week plan (2,800+ строк)
├── @critical/              # Критические отчеты
│   ├── 01_critical_issues.md    # Проблемы и их статус
│   └── 02_key_decisions.md      # Ключевые архитектурные решения
├── r2r/                    # R2R документация (официальная)
├── docs-r2r/               # R2R документация (структурированная)
└── claude_code/            # Claude Code документация
```

## 🛠️ Команды разработки

### Работа с документацией

```bash
# Скачать документацию Claude Code
python scripts/download_claude_docs.py

# Разделить документацию R2R на секции
python scripts/split_r2r_docs.py

# Переименовать секции для лучшей навигации
python scripts/rename_sections.py
```

### Навигация по проекту

```bash
# Быстрый поиск по документации
rg "keyword" docs/@analysis/

# Найти файлы по паттерну
fd -e md -e py "pattern"

# Проверить статус проекта
cat docs/@analysis/README.md
```

## 🔑 Ключевые технические решения

### 1. MCP Server (Layer 1)

**6 Core Tools**:
- `r2r_search` - Семантический/гибридный поиск
- `r2r_rag_query` - RAG-powered Q&A
- `r2r_ingest_document` - Загрузка документов
- `r2r_list_documents` - Просмотр документов в коллекции
- `r2r_monitor_task` - Мониторинг статуса задач
- `r2r_list_collections` - Управление коллекциями

**2 Resources**:
- `r2r://current-project/context` - Метаданные проекта
- `r2r://search/history` - История поиска

**Stack**:
- FastAPI (async HTTP server)
- JSON-RPC 2.0 protocol
- r2r-py SDK для коммуникации с R2R
- Redis для кэширования (опционально, fallback на in-memory)

**Спецификация**: @docs/@analysis/04_mcp_server_specification.md

### 2. Authentication: Service Account

```bash
# Environment Variables
R2R_SERVICE_EMAIL=claude-code-service@example.com
R2R_SERVICE_PASSWORD=<stored in vault>
R2R_API_BASE_URL=http://136.119.36.216:7272
```

**Механизм**:
- Автоматический login при старте MCP сервера
- Auto-refresh токенов перед истечением
- Централизованное управление credentials

### 3. Data Consistency: Queue-Based Strategy

**Проблема**: Race conditions при быстрых модификациях файлов

**Решение**:
```text
File Modification → PostToolUse Hook → UpdateQueue → UpdateWorker → R2R API → StateTracker
```

**Компоненты**:
- **UpdateQueue**: Priority queue с версионированием
- **UpdateWorker**: Фоновый процессор с retry logic
- **StateTracker**: SQLite DB (file_path → document_id → hash → sync_status)
- **Content Hashing**: SHA-256 для idempotency

**Спецификация**: @docs/@analysis/05_data_consistency_strategy.md

### 4. Caching Strategy

**TTL (Time-To-Live)**:
- Search results: 5 минут
- RAG responses: 2 минуты
- Document lists: 1 минута

**Backends**:
- Production: Redis
- Development: In-memory

### 5. Circuit Breaker Pattern

**Конфигурация**:
- Failure threshold: 5 последовательных ошибок
- Timeout: 60 секунд перед попыткой восстановления
- Success threshold: 2 успеха для полного восстановления

**States**: CLOSED (норма) → OPEN (R2R недоступен) → HALF_OPEN (тестирование)

## 📖 Критические документы для чтения

### Для начала работы (читать в порядке):

1. **docs/@analysis/README.md** - Текущий статус и roadmap проекта
2. **docs/@analysis/00_REVIEW.md** - Критический обзор: gaps, риски, возможности
3. **docs/@analysis/04_mcp_server_specification.md** - MCP Server архитектура
4. **docs/@analysis/05_data_consistency_strategy.md** - Решение race conditions
5. **docs/@analysis/06_testing_strategy.md** - Comprehensive testing approach
6. **docs/@analysis/07_implementation_roadmap.md** - 14-week phase-by-phase plan

### Для глубокого понимания:

7. **docs/@analysis/01a_r2r_api_gaps_filled.md** - Заполненные пробелы R2R API
8. **docs/@analysis/03_integration_mapping.md** - 4 архитектурных паттерна
9. **docs/@critical/02_key_decisions.md** - Обоснование ключевых решений

## 🚧 Текущий статус разработки

### Completed ✅ (85%)

- ✅ R2R API Analysis
- ✅ Claude Code Integration Analysis (7 механизмов)
- ✅ Architecture Design (Hybrid 5-layer)
- ✅ MCP Server Specification (1,512 строк)
- ✅ Data Consistency Strategy (1,033 строк)
- ✅ Critical Review (15 gaps заполнено)
- ✅ Testing Strategy (2,200+ строк)
- ✅ Implementation Roadmap (2,800+ строк)

### In Progress 🔄 (5%)

- 🔄 Code Examples

### Pending ⏭️ (10%)

- ⏭️ Final Review and Readiness Assessment

### Deferred 🔒 (Infrastructure - Phase 5 Only)

**Monitoring & Caching Infrastructure (postponed to Phase 5):**
- 🔒 **Redis** - deferred to Phase 5 (use in-memory cache for Phases 0-4)
- 🔒 **Prometheus** - deferred to Phase 5 (use structured logging instead)
- 🔒 **Grafana** - deferred to Phase 5 (use log analysis instead)

**Rationale:**
- ✅ Reduced complexity during development (Phases 0-4)
- ✅ Faster iteration without external dependencies
- ✅ Lower infrastructure costs ($0 vs $200-500/month)
- ✅ Same code interface - easy migration to Redis in Phase 5
- ✅ Focus on core functionality first

**See:** `docs/@critical/05_infrastructure_decisions.md` for details

## 📋 Roadmap (14 недель)

```text
Week 1-2:  Phase 0 - Research & Prototyping
Week 3-5:  Phase 1 - MCP Foundation (3 недели)
Week 6-7:  Phase 2 - Core Automation (2 недели)
Week 8-9:  Phase 3 - Specialization (2 недели)
Week 10-11: Phase 4 - Packaging (2 недели)
Week 12-14: Phase 5 - Production Readiness (3 недели)
```

### Success Criteria по фазам:

**Phase 0 (Prototype)**:
- ✅ Поиск в R2R из Claude Code работает
- ✅ Ingestion документов функционален
- ✅ E2E flow verified

**Phase 1 (MCP Foundation)**:
- ✅ Все 6 tools реализованы
- ✅ Auth auto-refresh работает
- ✅ Cache hit rate >50%
- ✅ Circuit breaker предотвращает cascade failures
- ✅ Test coverage >80%

## 🎓 Ключевые концепции

### R2R (Retrieval to Riches)

**R2R** - это enterprise-ready RAG платформа с:
- Documents API (CRUD, chunking, summarization)
- Conversations API (branching support)
- Retrieval API (search, RAG, agent, embeddings)
- Async orchestration через Hatchet
- Collections для data isolation
- Knowledge Graph extraction

### Model Context Protocol (MCP)

**MCP** - это протокол для расширения Claude Code:
- **Tools**: Функции, которые Claude может вызывать (например, `r2r_search`)
- **Resources**: Контекстные данные (например, `r2r://current-project/context`)
- **Prompts**: Готовые шаблоны запросов
- **Transport**: HTTP, SSE, stdio

### Claude Code Extension Mechanisms

**7 механизмов расширения**:
1. **MCP** - Основной интерфейс (Tools + Resources)
2. **Hooks** - Автоматизация (SessionStart, PostToolUse, Stop)
3. **Subagents** - Специализированные агенты (Haiku/Sonnet)
4. **Plugins** - Упаковка для distribution
5. **Skills** - Auto-selection на основе контекста
6. **Output Styles** - Кастомизация форматов вывода
7. **Headless** - CI/CD интеграция

## ⚠️ Критические моменты

### Data Consistency

- **ВСЕГДА используй queue-based подход** для модификаций файлов
- **НИКОГДА не полагайся на file locks** - они не работают с async
- **ВСЕГДА проверяй content hash** перед ingestion
- **ОБЯЗАТЕЛЬНО используй версионирование** для ordering

### Authentication

- **Храни credentials в .env** и НИКОГДА не коммить
- **Используй auto token refresh** с запасом времени (5 минут до expiry)
- **Проверяй token validity** перед каждым запросом

### Performance

- **Cache aggressively** - search queries повторяются часто
- **Batch operations** - группируй multiple ingestions
- **Use collection filters** - уменьшает search space
- **Monitor circuit breaker** - detect R2R unavailability early

### Security & Privacy

- **NO PII in R2R** без explicit consent
- **Collection-based isolation** для multi-project
- **Encryption in transit** (HTTPS) и at rest
- **Audit logging** всех operations

## 🔗 Полезные ссылки

### R2R Resources

- R2R Instance: http://136.119.36.216:7272
- Hatchet Dashboard: http://localhost:7274 (orchestration monitoring)
- R2R Docs: `docs/r2r/` и `docs/docs-r2r/`

### Claude Code Resources

- Claude Code Docs: `docs/claude_code/`
- MCP Protocol: `docs/claude_code/mcp.md`
- Hooks Guide: `docs/claude_code/hooks-guide.md`

### Project Analysis

- Technical Specs: `docs/@analysis/`
- Critical Reports: `docs/@critical/`
- Complete Analysis: `docs/R2R_Complete_Documentation_Analysis.md`

## 💡 Tips for Development

### При работе с MCP Server:

1. **Начни с простого** - Prototype с 2-3 базовыми tools
2. **Тестируй инкрементально** - Unit → Integration → E2E
3. **Логируй всё** - Structured JSON logs для debugging
4. **Мониторь метрики** - Request latency, cache hit rate, error rate

### При работе с R2R API:

1. **ВСЕГДА используй collection filtering** - Reduces search scope
2. **Limit search results** - Top 3-5 достаточно для context
3. **Monitor ingestion status** - Polling каждые 30s
4. **Handle async gracefully** - Не блокируй user на ingestion

### При работе с Hooks:

1. **SessionStart** - Initialize collections, resume pending tasks
2. **PostToolUse** - Enqueue file updates (НЕ блокируй tool execution)
3. **Stop** - Graceful shutdown с drain timeout (30s)

## 📞 Контакты и поддержка

**Git Branch**: `claude/r2r-claude-mcp-integration-012EZn1c5khRLQbNi1gHqShh`

**Project Owner**: Указан в git history

**Last Updated**: 2025-11-19

---

**Ready for Phase 0: Prototyping** 🚀
