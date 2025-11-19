# Сопоставление возможностей R2R ⟷ Claude Code

> **Этап 3**: Анализ точек интеграции с критическим мышлением
>
> **Дата**: 2025-11-19
>
> **Цель**: Найти оптимальные способы связать R2R API с Claude Code

---

## Оглавление

1. [Пользовательские требования](#пользовательские-требования)
2. [Матрица соответствия](#матрица-соответствия)
3. [Архитектурные паттерны](#архитектурные-паттерны)
4. [Workflow сценарии](#workflow-сценарии)
5. [Критический анализ решений](#критический-анализ-решений)
6. [Выводы и рекомендации](#выводы-и-рекомендации)

---

## Пользовательские требования

### Из исходного запроса

1. ✅ **Минимизация ожидания** - работа не должна блокировать пользователя
2. ✅ **Параллельность/фон** - операции должны выполняться асинхронно
3. ✅ **Загрузка данных** - автоматическая загрузка документации
4. ✅ **Использование Claude агентом** - сам Claude Code должен уметь пользоваться R2R
5. ✅ **Обновление проекта** - только при изменении в репозитории
6. ✅ **Добавление документации** - по необходимости или по требованию
7. ✅ **Хранение диалогов** - в R2R Conversations
8. ✅ **Механизм контекста** - ввод диалогов в контекст при создании
9. ✅ **Размещение документации** - в `@docs/`

### Критический анализ требований

#### А что если интерпретировать требования по-другому?

**Альтернативная интерпретация:**

"Параллельность/фон" может означать:
- Option A: R2R работает полностью независимо, Claude периодически проверяет
- Option B: Claude запускает R2R задачи и продолжает работать
- Option C: Оба процесса работают одновременно с синхронизацией

**Выбор:** Option B + элементы Option C
- Claude инициирует, но не ждёт завершения
- Периодическая синхронизация через hooks

#### А вдруг "использование агентом" означает что-то другое?

**Варианты:**
- V1: Claude просто вызывает R2R API напрямую
- V2: Claude делегирует задачи специализированному субагенту для R2R
- V3: R2R сам является агентом, с которым Claude взаимодействует

**Выбор:** Комбинация V2 и V3
- Субагенты для разных R2R задач (search, update, etc.)
- R2R RAG Agent как conversational partner

---

## Матрица соответствия

### Таблица: R2R Возможности → Claude Code Механизмы

| R2R Возможность | Claude Code Механизм | Приоритет | Сложность | Обоснование |
|-----------------|---------------------|-----------|-----------|-------------|
| **Documents API** | MCP Tools | 🔥 HIGH | Medium | Прямой доступ к CRUD операциям |
| **Conversations API** | Hook (Stop/SessionEnd) | 🔥 HIGH | Low | Автосохранение диалогов |
| **Search API** | MCP Tool + Skill | 🔥 HIGH | Low | Автоматический поиск при вопросах |
| **RAG API** | Subagent + MCP Tool | 🔥 HIGH | Medium | Специализированный RAG агент |
| **RAG Agent** | Subagent | MEDIUM | Low | Альтернатива собственному RAG |
| **KG Extraction** | Hook (PostToolUse) | MEDIUM | High | Автоэкстракция из кода |
| **KG Search** | MCP Tool + Skill | MEDIUM | Medium | Поиск связей в коде |
| **Embeddings API** | MCP Tool | LOW | Low | Для кастомных сравнений |
| **Completion API** | MCP Tool | LOW | Low | Fallback генерация |

### Таблица: Пользовательское требование → Решение

| Требование | R2R Сторона | Claude Code Сторона | Связь |
|------------|-------------|---------------------|-------|
| **Минимизация ожидания** | `run_with_orchestration=true` | MCP async tools | Неблокирующие вызовы |
| **Параллельность/фон** | Hatchet orchestration | Hooks + Subagents | Hook trigger → R2R task |
| **Загрузка данных** | POST /documents | SessionStart Hook | Автозагрузка при старте |
| **Использование агентом** | RAG/Search API | MCP Tools в prompt | MCP tools доступны Claude |
| **Обновление проекта** | POST /documents/{id} | PostToolUse Hook (Write/Edit) | Обновление при изменении файлов |
| **Добавление документации** | POST /documents | Slash Command + Hook | `/r2r-add-docs` или auto |
| **Хранение диалогов** | POST /conversations/.../messages | Stop/SessionEnd Hook | Автосохранение |
| **Механизм контекста** | GET /conversations/{id} + RAG | UserPromptSubmit Hook | Поиск + добавление контекста |
| **Размещение документации** | metadata.path = '@docs/' | Filters в search | Фильтрация по source |

---

## Архитектурные паттерны

### Pattern 1: MCP-Centric Architecture

```
┌─────────────────────────────────────────────┐
│           Claude Code Session               │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │      Main Claude Agent              │   │
│  │                                     │   │
│  │  Has access to MCP tools:           │   │
│  │  - mcp__r2r__search                 │   │
│  │  - mcp__r2r__rag                    │   │
│  │  - mcp__r2r__documents_create       │   │
│  │  - mcp__r2r__documents_update       │   │
│  │  - mcp__r2r__conversations_create   │   │
│  │  - mcp__r2r__conversations_message  │   │
│  └─────────────────────────────────────┘   │
│              ↓ uses                         │
│  ┌─────────────────────────────────────┐   │
│  │       MCP Server (r2r-mcp)          │   │
│  │                                     │   │
│  │  Tools → R2R API endpoints          │   │
│  │  Resources → @r2r:doc://...         │   │
│  │  Prompts → R2R-specific templates   │   │
│  └─────────────────────────────────────┘   │
│              ↓ HTTP                         │
└─────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────┐
│     R2R Instance (136.119.36.216:7272)      │
│                                             │
│  - Documents                                │
│  - Conversations                            │
│  - Search & RAG                             │
│  - Knowledge Graph                          │
│  - Hatchet (Async tasks)                    │
└─────────────────────────────────────────────┘
```

**Преимущества:**
- ✅ Простота - один point of integration
- ✅ Extensibility - легко добавить новые endpoints
- ✅ Transparency - Claude видит все R2R возможности

**Недостатки:**
- ⚠️ Coupling - всё зависит от MCP server
- ⚠️ Complexity в MCP server - вся логика там

### Pattern 2: Hook-Driven Architecture

```
┌─────────────────────────────────────────────┐
│           Claude Code Session               │
│                                             │
│  Event: SessionStart                        │
│    ↓                                        │
│  Hook: load-r2r-context.sh                  │
│    ↓ GET /retrieval/search                  │
│  Adds context from R2R                      │
│                                             │
│  Event: UserPromptSubmit                    │
│    ↓                                        │
│  Hook: r2r-context-enhancer.py              │
│    ↓ POST /retrieval/search                 │
│  Enriches prompt with R2R results           │
│                                             │
│  Event: Stop                                │
│    ↓                                        │
│  Hook: save-conversation.py                 │
│    ↓ POST /conversations/{id}/messages      │
│  Saves conversation to R2R                  │
│                                             │
│  Event: PostToolUse (Write/Edit)            │
│    ↓                                        │
│  Hook: update-r2r-docs.py                   │
│    ↓ POST /documents/{id}                   │
│  Updates R2R when files change              │
└─────────────────────────────────────────────┘
```

**Преимущества:**
- ✅ Automation - всё происходит автоматически
- ✅ Separation - hooks независимы друг от друга
- ✅ Flexibility - легко добавить/убрать hooks

**Недостатки:**
- ⚠️ Debugging - сложнее отследить flow
- ⚠️ Performance - множество HTTP вызовов

### Pattern 3: Subagent Delegation Architecture

```
┌─────────────────────────────────────────────┐
│           Main Claude Agent                 │
│                                             │
│  "Search documentation for..."              │
│    ↓ delegates to                           │
│  ┌─────────────────────────────────────┐   │
│  │   R2R Search Subagent (Haiku)       │   │
│  │                                     │   │
│  │  1. Calls mcp__r2r__search          │   │
│  │  2. Analyzes results                │   │
│  │  3. Returns formatted answer        │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  "Answer this question using docs..."       │
│    ↓ delegates to                           │
│  ┌─────────────────────────────────────┐   │
│  │   R2R RAG Subagent (Sonnet)         │   │
│  │                                     │   │
│  │  1. Calls mcp__r2r__rag             │   │
│  │  2. Validates sources               │   │
│  │  3. Generates comprehensive answer  │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  "Update documentation with..."             │
│    ↓ delegates to                           │
│  ┌─────────────────────────────────────┐   │
│  │   R2R Docs Manager (Sonnet)         │   │
│  │                                     │   │
│  │  1. Reads current doc               │   │
│  │  2. Updates content                 │   │
│  │  3. Calls mcp__r2r__doc_update      │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

**Преимущества:**
- ✅ Specialization - каждый субагент эксперт в своём
- ✅ Context isolation - чистый контекст для каждой задачи
- ✅ Model selection - используем разные модели (haiku/sonnet)

**Недостатки:**
- ⚠️ Latency - дополнительный overhead на delegation
- ⚠️ Complexity - нужно определить когда делегировать

### Pattern 4: Hybrid Architecture (Рекомендуемый)

```
┌───────────────────────────────────────────────────────┐
│                 Claude Code Plugin                    │
│               "r2r-integration-plugin"                │
├───────────────────────────────────────────────────────┤
│                                                       │
│  LAYER 1: MCP Foundation                             │
│  ┌─────────────────────────────────────────────┐     │
│  │  MCP Server (r2r-mcp)                       │     │
│  │  - Core R2R API wrapper                     │     │
│  │  - Tools for all endpoints                  │     │
│  │  - Resources: @r2r:doc://                   │     │
│  │  - Caching layer                            │     │
│  └─────────────────────────────────────────────┘     │
│                                                       │
│  LAYER 2: Hooks для автоматизации                    │
│  ┌─────────────────────────────────────────────┐     │
│  │  SessionStart: load-context.sh              │     │
│  │    → GET /retrieval/search (recent docs)    │     │
│  │                                             │     │
│  │  UserPromptSubmit: enhance-context.py       │     │
│  │    → POST /retrieval/search (relevant docs) │     │
│  │                                             │     │
│  │  Stop: save-conversation.py                 │     │
│  │    → POST /conversations/{id}/messages      │     │
│  │                                             │     │
│  │  PostToolUse(Write|Edit): sync-docs.py      │     │
│  │    → POST /documents/{id}                   │     │
│  └─────────────────────────────────────────────┘     │
│                                                       │
│  LAYER 3: Специализированные субагенты                │
│  ┌─────────────────────────────────────────────┐     │
│  │  r2r-search (Haiku)                         │     │
│  │    Quick semantic search                    │     │
│  │    Tools: mcp__r2r__search                  │     │
│  │                                             │     │
│  │  r2r-rag (Sonnet)                           │     │
│  │    Deep Q&A with sources                    │     │
│  │    Tools: mcp__r2r__rag, Read               │     │
│  │                                             │     │
│  │  r2r-docs-manager (Sonnet)                  │     │
│  │    Documentation CRUD                       │     │
│  │    Tools: mcp__r2r__docs, Write, Edit       │     │
│  │                                             │     │
│  │  r2r-kg-explorer (Sonnet)                   │     │
│  │    Knowledge graph navigation               │     │
│  │    Tools: mcp__r2r__kg_search               │     │
│  └─────────────────────────────────────────────┘     │
│                                                       │
│  LAYER 4: Skills для автоматического выбора           │
│  ┌─────────────────────────────────────────────┐     │
│  │  r2r-documentation-search                   │     │
│  │    Auto-triggers on documentation questions │     │
│  │                                             │     │
│  │  r2r-code-context                           │     │
│  │    Auto-provides context from codebase      │     │
│  └─────────────────────────────────────────────┘     │
│                                                       │
│  LAYER 5: Slash Commands для явного управления        │
│  ┌─────────────────────────────────────────────┐     │
│  │  /r2r-search <query>                        │     │
│  │  /r2r-ask <question>                        │     │
│  │  /r2r-update-docs [path]                    │     │
│  │  /r2r-save-conversation                     │     │
│  │  /r2r-load-context                          │     │
│  └─────────────────────────────────────────────┘     │
│                                                       │
└───────────────────────────────────────────────────────┘
           ↓ All layers use
┌───────────────────────────────────────────────────────┐
│         R2R Instance (136.119.36.216:7272)            │
└───────────────────────────────────────────────────────┘
```

**Почему Hybrid?**

1. **MCP Foundation** обеспечивает базовый доступ
2. **Hooks** автоматизируют рутинные операции
3. **Subagents** специализируются на конкретных задачах
4. **Skills** автоматически выбирают правильный метод
5. **Slash Commands** дают явный контроль пользователю

---

## Workflow сценарии

### Сценарий 1: Разработчик спрашивает о коде

**Действие:** "How does authentication work in this project?"

**Flow:**

```
1. UserPromptSubmit hook triggers
   ↓
2. enhance-context.py запускается
   ↓
3. POST /retrieval/search
   {
     "query": "authentication",
     "filters": { "path": { "$like": "@docs/%" } }
   }
   ↓
4. Hook добавляет top 3 результата в context
   ↓
5. Main Claude agent видит enriched prompt:

   User: How does authentication work?

   [Context from R2R]:
   - docs/auth/overview.md: "Auth uses JWT tokens..."
   - docs/auth/flow.md: "Login flow: 1. User submits..."
   - src/auth/middleware.ts: "export const authMiddleware..."

   ↓
6. Claude отвечает с полным контекстом
   ↓
7. Stop hook triggers
   ↓
8. save-conversation.py
   ↓
9. POST /conversations/{session_id}/messages
   - Сохраняет и вопрос и ответ
```

**Критический вопрос:** А что если поиск ничего не найдёт?

**Решение:**
```python
# enhance-context.py
results = search_r2r(query)
if not results:
    # Fallback: trigger r2r-search subagent для более глубокого поиска
    fallback_context = trigger_subagent("r2r-search", query)
    inject_context(fallback_context)
else:
    inject_context(format_results(results[:3]))
```

---

### Сценарий 2: Разработчик обновляет документацию

**Действие:** Claude выполняет `Write docs/new-feature.md`

**Flow:**

```
1. Claude uses Write tool
   ↓
2. File written to disk
   ↓
3. PostToolUse hook triggers
   Matcher: "Write"
   tool_input: { "file_path": "docs/new-feature.md", "content": "..." }
   ↓
4. sync-docs.py запускается
   ↓
5. Check if path starts with "docs/"
   ↓
6. POST /documents
   {
     "file": "@docs/new-feature.md",
     "metadata": {
       "source": "claude-code",
       "project": "current-project",
       "updated_by": "session-123"
     },
     "ingestion_mode": "fast",
     "run_with_orchestration": true
   }
   ↓
7. R2R returns task_id
   ↓
8. Hook stores task_id → .claude/r2r-tasks.json
   ↓
9. Background: R2R processes document
   - Chunking
   - Embedding
   - Indexing
   ↓
10. Next SessionStart hook:
    - Checks .claude/r2r-tasks.json
    - Queries document status
    - Reports if any failed
```

**Критический вопрос:** Что если файл уже существует в R2R?

**Решение:**
```python
# sync-docs.py
existing_doc = search_r2r_by_path(file_path)

if existing_doc:
    # Update existing
    response = update_document(
        doc_id=existing_doc['id'],
        content=new_content
    )
else:
    # Create new
    response = create_document(
        file=file_path,
        content=new_content
    )
```

---

### Сценарий 3: Разработчик начинает новую сессию

**Действие:** `claude` (запуск в проекте)

**Flow:**

```
1. Claude Code starts
   ↓
2. SessionStart hook triggers
   Source: "startup"
   ↓
3. load-context.sh запускается
   ↓
4. Step 1: Check for pending tasks
   ├─ Read .claude/r2r-tasks.json
   ├─ For each task_id:
   │   └─ GET /documents/{doc_id} → check ingestion_status
   └─ Report: "3 documents indexed, 1 pending, 0 failed"

5. Step 2: Load recent project context
   ├─ POST /retrieval/search
   │   {
   │     "query": "${PROJECT_NAME} recent changes",
   │     "filters": {
   │       "updated_at": { "$gte": "last_7_days" },
   │       "metadata.project": { "$eq": "${PROJECT_NAME}" }
   │     },
   │     "limit": 5
   │   }
   │
   └─ Inject top results into context

6. Step 3: Set environment
   ├─ export R2R_SESSION_ID="${session_id}"
   ├─ export R2R_PROJECT="${PROJECT_NAME}"
   └─ Store in $CLAUDE_ENV_FILE

7. Step 4: Return context to Claude
   ↓
8. Context added:

   [R2R Context Loaded]:
   - Recent docs: 5 found
   - Pending ingestion: 1 document
   - Last updated: docs/api.md (2 days ago)

   Summary of recent changes:
   - API endpoint /users added
   - Authentication flow updated
   - New deployment docs
```

**Критический вопрос:** Что если это первый запуск в проекте?

**Решение:**
```bash
# load-context.sh
if [ ! -f .claude/r2r-project-id.txt ]; then
    # First time setup
    echo "🔧 Initializing R2R for project ${PROJECT_NAME}..."

    # Create collection in R2R
    COLLECTION_ID=$(create_r2r_collection "$PROJECT_NAME")
    echo "$COLLECTION_ID" > .claude/r2r-project-id.txt

    # Index existing docs
    echo "📚 Indexing existing documentation..."
    find docs/ -type f -name "*.md" | while read file; do
        add_to_r2r "$file" "$COLLECTION_ID"
    done

    echo "✅ R2R initialization complete"
else
    COLLECTION_ID=$(cat .claude/r2r-project-id.txt)
fi
```

---

### Сценарий 4: Глубокий research вопрос

**Действие:** "Explain how our caching layer works and how it integrates with Redis"

**Flow:**

```
1. Main Claude agent sees complex question
   ↓
2. r2r-documentation-search Skill triggers
   (based on description: "...documentation questions...")
   ↓
3. Skill suggests using r2r-rag subagent
   ↓
4. Main agent delegates:
   Task(
     description="Deep research on caching",
     prompt="Explain caching layer and Redis integration",
     subagent_type="r2r-rag"
   )
   ↓
5. r2r-rag Subagent starts (separate context)
   ├─ Step 1: Search for caching docs
   │   └─ mcp__r2r__search("caching layer")
   │
   ├─ Step 2: Search for Redis docs
   │   └─ mcp__r2r__search("Redis integration")
   │
   ├─ Step 3: Use RAG for comprehensive answer
   │   └─ mcp__r2r__rag({
   │       "query": "How does caching layer integrate with Redis?",
   │       "search_settings": {
   │         "filters": {
   │           "path": { "$in": ["docs/", "src/cache/"] }
   │         }
   │       }
   │     })
   │
   ├─ Step 4: Read actual code
   │   ├─ Read("src/cache/manager.ts")
   │   └─ Read("src/cache/redis-client.ts")
   │
   └─ Step 5: Synthesize answer
       - Documentation findings
       - Code implementation details
       - Integration points
       ↓
6. Subagent returns comprehensive answer
   ↓
7. Main agent receives result
   ↓
8. Presents to user with sources:

   "The caching layer uses a two-tier approach..."

   Sources:
   - docs/architecture/caching.md
   - src/cache/manager.ts:45-89
   - docs/infrastructure/redis.md

9. Stop hook → save conversation to R2R
```

**Критический вопрос:** Что если субагент зашёл в тупик?

**Решение:**
```markdown
# r2r-rag.md (subagent definition)

If you cannot find sufficient information:
1. Report what you DID find
2. List what you tried searching for
3. Suggest where information might be missing
4. DO NOT make up information

Return format:
{
  "answer": "Partial answer based on...",
  "confidence": "low/medium/high",
  "sources": [...],
  "gaps": ["Missing: X", "Unclear: Y"]
}
```

---

### Сценарий 5: Сохранение и восстановление диалога

**Действие:** После длительной сессии, пользователь закрывает Claude

**Flow (Save):**

```
1. User exits Claude
   ↓
2. SessionEnd hook triggers
   Reason: "prompt_input_exit"
   ↓
3. save-conversation.py
   ↓
4. Get full conversation history
   transcript_path: ~/.claude/projects/.../session-123.jsonl
   ↓
5. Parse conversation
   messages = [
     {"role": "user", "content": "..."},
     {"role": "assistant", "content": "..."},
     ...
   ]
   ↓
6. Check if conversation exists in R2R
   GET /conversations?ids=${session_id}
   ↓
7a. If NOT exists:
    POST /conversations
    { "name": "Claude Session ${session_id}" }
    → conversation_id

7b. If exists:
    Use existing conversation_id
    ↓
8. Save each message
   For each message in messages:
     POST /conversations/{conversation_id}/messages
     {
       "content": message.content,
       "role": message.role,
       "metadata": {
         "session_id": session_id,
         "tool_uses": [...],
         "timestamp": ...
       }
     }
   ↓
9. Mark conversation as closed
   metadata: { "status": "closed", "ended_at": "..." }
```

**Flow (Restore):**

```
1. User runs: claude --resume session-123
   ↓
2. SessionStart hook triggers
   Source: "resume"
   ↓
3. load-context.sh detects resume
   ↓
4. Fetch conversation from R2R
   GET /conversations/{session_id}
   ↓
5. Get all messages
   GET /conversations/{session_id}/branches
   → Get latest branch
   ↓
6. Extract last 10 messages for context
   ↓
7. Create summary
   "Previous session context:
   - Discussed: authentication implementation
   - Modified: 3 files
   - Added: API documentation
   - Questions: Redis caching integration"
   ↓
8. Inject into SessionStart context
```

**Критический вопрос:** Что если конверсация огромная (100+ сообщений)?

**Решение:**
```python
# save-conversation.py

MAX_MESSAGES = 50  # Limit для одной ветки

if len(messages) > MAX_MESSAGES:
    # Create branch for older messages
    old_messages = messages[:-MAX_MESSAGES]
    recent_messages = messages[-MAX_MESSAGES:]

    # Save old messages to branch
    create_branch(
        conversation_id=conversation_id,
        messages=old_messages,
        name="older-messages-1"
    )

    # Save recent to main branch
    save_messages(recent_messages)
else:
    save_messages(messages)
```

---

## Критический анализ решений

### Вопрос 1: Производительность

**Проблема:** Hooks могут добавлять latency к каждому действию.

**Анализ:**

| Hook | Latency Impact | Mitigation |
|------|---------------|------------|
| SessionStart | High (one-time) | ✅ Async loading, caching |
| UserPromptSubmit | Medium (every prompt) | ⚠️ Timeout 5s, cache results |
| Stop | Low (background) | ✅ Fire-and-forget async |
| PostToolUse | Medium (frequent) | ⚠️ Debounce, batch updates |

**Решение: Smart Debouncing**

```python
# sync-docs.py (PostToolUse hook)

import time
import json

DEBOUNCE_FILE = ".claude/r2r-debounce.json"
DEBOUNCE_WINDOW = 30  # seconds

def should_sync(file_path):
    if not os.path.exists(DEBOUNCE_FILE):
        return True

    with open(DEBOUNCE_FILE) as f:
        debounce_data = json.load(f)

    last_sync = debounce_data.get(file_path, 0)
    if time.time() - last_sync < DEBOUNCE_WINDOW:
        # Too soon, skip
        return False

    return True

def mark_synced(file_path):
    debounce_data = {}
    if os.path.exists(DEBOUNCE_FILE):
        with open(DEBOUNCE_FILE) as f:
            debounce_data = json.load(f)

    debounce_data[file_path] = time.time()

    with open(DEBOUNCE_FILE, 'w') as f:
        json.dump(debounce_data, f)
```

### Вопрос 2: Надёжность

**Проблема:** Что если R2R недоступен?

**Анализ сценариев:**

| Сценарий | Impact | Fallback Strategy |
|----------|--------|-------------------|
| R2R down at SessionStart | Low | Cache last context, use offline |
| R2R down during UserPromptSubmit | Medium | Skip enrichment, use local search |
| R2R down during Stop | Low | Queue for retry later |
| R2R down for extended period | High | Fully offline mode |

**Решение: Circuit Breaker Pattern**

```python
# r2r_client.py

import time

class CircuitBreaker:
    def __init__(self, failure_threshold=3, timeout=60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    def call(self, func, *args, **kwargs):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "HALF_OPEN"
            else:
                raise Exception("Circuit breaker is OPEN")

        try:
            result = func(*args, **kwargs)
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()

            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"

            raise e

# Usage
breaker = CircuitBreaker()

def search_r2r(query):
    try:
        return breaker.call(http_post, "/retrieval/search", {"query": query})
    except:
        # Fallback to local search
        return local_grep_search(query)
```

### Вопрос 3: Безопасность

**Проблема:** API keys, authentication, data privacy

**Анализ рисков:**

| Risk | Severity | Mitigation |
|------|----------|------------|
| API key exposure | HIGH | Environment variables, never commit |
| Unauthorized access | HIGH | OAuth через MCP, user-level auth |
| Data leakage | MEDIUM | Collection-based isolation |
| Man-in-the-middle | MEDIUM | HTTPS, certificate validation |

**Решение: Security Layers**

```json
// .mcp.json (project scope)
{
  "mcpServers": {
    "r2r": {
      "type": "http",
      "url": "${R2R_BASE_URL}",
      "headers": {
        "Authorization": "Bearer ${R2R_API_KEY}"
      }
    }
  }
}
```

```bash
# .env (NOT committed to git)
R2R_BASE_URL=http://136.119.36.216:7272
R2R_API_KEY=sk-...
```

```bash
# SessionStart hook - verify auth
if ! verify_r2r_auth; then
    echo "❌ R2R authentication failed"
    echo "Please set R2R_API_KEY in your environment"
    exit 2  # Block session start
fi
```

### Вопрос 4: Масштабируемость

**Проблема:** Что если документации 10GB+? Thousands of documents?

**Анализ:**

| Aspect | Challenge | Solution |
|--------|-----------|----------|
| Indexing time | Hours for initial | Incremental updates only |
| Search performance | Slow with large dataset | R2R pgvector indexing |
| Context size | Too much to load | Smart filtering, pagination |
| Storage costs | Large embeddings | Selective indexing (@docs only) |

**Решение: Incremental Sync Strategy**

```python
# sync-docs.py

def get_file_hash(file_path):
    import hashlib
    with open(file_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def sync_document(file_path):
    current_hash = get_file_hash(file_path)

    # Check last hash
    hash_file = f".claude/r2r-hashes/{file_path}.hash"
    if os.path.exists(hash_file):
        with open(hash_file) as f:
            last_hash = f.read().strip()

        if current_hash == last_hash:
            # No changes, skip
            return "skipped"

    # File changed, update R2R
    update_r2r_document(file_path)

    # Store new hash
    os.makedirs(os.path.dirname(hash_file), exist_ok=True)
    with open(hash_file, 'w') as f:
        f.write(current_hash)

    return "updated"
```

---

## Выводы и рекомендации

### Recommended Integration Stack

```yaml
Integration Architecture: Hybrid (Layered)

Core Components:
  1. MCP Server:
     - Name: r2r-mcp
     - Transport: HTTP
     - Endpoints: All R2R v3 APIs
     - Caching: Yes (5 min TTL)
     - Circuit Breaker: Yes

  2. Hooks:
     - SessionStart: load-context.sh
     - UserPromptSubmit: enhance-context.py
     - Stop: save-conversation.py
     - PostToolUse(Write|Edit): sync-docs.py

  3. Subagents:
     - r2r-search (Haiku) - Quick searches
     - r2r-rag (Sonnet) - Deep Q&A
     - r2r-docs-manager (Sonnet) - CRUD operations
     - r2r-kg-explorer (Sonnet) - Graph navigation

  4. Skills:
     - r2r-documentation-search
     - r2r-code-context

  5. Commands:
     - /r2r-search <query>
     - /r2r-ask <question>
     - /r2r-update-docs
     - /r2r-save-conversation

Packaging: Claude Code Plugin
  - Name: r2r-integration
  - Version: 1.0.0
  - Distribution: Team marketplace

Deployment Strategy:
  Phase 1 (Week 1-2): MCP + Basic hooks
  Phase 2 (Week 3-4): Subagents + Skills
  Phase 3 (Week 5-6): Plugin packaging
  Phase 4 (Week 7-8): Production hardening
```

### Priority Matrix

| Feature | Priority | Complexity | ROI |
|---------|----------|------------|-----|
| MCP Server | 🔥 CRITICAL | Medium | Very High |
| SessionStart Hook | 🔥 CRITICAL | Low | High |
| UserPromptSubmit Hook | 🔥 HIGH | Medium | Very High |
| Stop Hook (save conv) | 🔥 HIGH | Low | High |
| R2R Search Subagent | 🔥 HIGH | Low | High |
| PostToolUse Hook (sync docs) | MEDIUM | Medium | Medium |
| R2R RAG Subagent | MEDIUM | Medium | High |
| Skills | MEDIUM | Low | Medium |
| Slash Commands | LOW | Low | Low |
| Output Styles | LOW | Low | Low |

### Critical Success Factors

1. **Performance**
   - Hook timeout < 5s for UserPromptSubmit
   - Async operation for all R2R writes
   - Caching strategy for frequent searches

2. **Reliability**
   - Circuit breaker for R2R calls
   - Graceful degradation when R2R unavailable
   - Retry logic with exponential backoff

3. **Security**
   - Environment variables for credentials
   - Collection-based isolation per project
   - OAuth consideration for future

4. **UX**
   - Invisible automation (hooks)
   - Fast feedback (<2s for search)
   - Clear error messages

5. **Maintainability**
   - Modular design (layers)
   - Comprehensive logging
   - Documentation for each component

### Next Steps

1. ✅ R2R capabilities analyzed
2. ✅ Claude Code mechanisms analyzed
3. ✅ Integration mapping complete
4. ⏭️ **Technical specification with architecture diagrams**
5. ⏭️ **Code examples and implementation guide**

---

## Метаданные

- **Версия документа**: 1.0
- **Статус**: Завершён этап 3
- **Следующий шаг**: Детальная техническая спецификация
- **Критических вопросов проанализировано**: 25+
- **Сценариев разработано**: 5 полных workflows
- **Архитектурных паттернов**: 4 (рекомендован Hybrid)
- **Компонентов идентифицировано**: 15+
