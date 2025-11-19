# Анализ возможностей Claude Code

> **Этап 2**: Изучение механизмов расширения Claude Code с критическим мышлением
>
> **Дата**: 2025-11-19
>
> **Цель**: Понять, какие механизмы Claude Code можно использовать для интеграции с R2R

---

## Оглавление

1. [Общее описание Claude Code](#общее-описание-claude-code)
2. [Механизмы расширения](#механизмы-расширения)
3. [Model Context Protocol (MCP)](#model-context-protocol-mcp)
4. [Hooks](#hooks)
5. [Subagents](#subagents)
6. [Plugins](#plugins)
7. [Skills](#skills)
8. [Output Styles](#output-styles)
9. [Headless Mode](#headless-mode)
10. [Критический анализ](#критический-анализ)
11. [Выводы для интеграции](#выводы-для-интеграции)

---

## Общее описание Claude Code

**Claude Code** - это официальный CLI для Claude от Anthropic, предназначенный для помощи в задачах software engineering.

### Основные характеристики
- Интерактивный CLI
- Доступ к файловой системе
- Выполнение bash команд
- Контекстное понимание проекта
- Расширяемая архитектура

---

## Механизмы расширения

Claude Code предоставляет **7 основных механизмов расширения**:

| Механизм | Описание | User-invoked | Model-invoked |
|----------|----------|--------------|---------------|
| **MCP** | Подключение внешних tools/services | - | ✅ |
| **Hooks** | Автоматизация через события | - | ✅ |
| **Subagents** | Специализированные AI агенты | ✅/✅ | ✅ |
| **Plugins** | Комплексные расширения | ✅ | - |
| **Skills** | Модульные capabilities | - | ✅ |
| **Output Styles** | Адаптация поведения | ✅ | - |
| **Headless Mode** | Программное выполнение | ✅ | - |

---

## Model Context Protocol (MCP)

### Что это?

MCP - это открытый стандарт для AI-tool интеграций, позволяющий Claude Code подключаться к внешним сервисам и инструментам.

### Типы транспортов

1. **HTTP** - для удалённых сервисов (рекомендуется)
2. **SSE** - Server-Sent Events (deprecated)
3. **stdio** - локальные процессы

### Установка MCP сервера

```bash
# HTTP transport
claude mcp add --transport http <name> <url>

# Stdio transport
claude mcp add --transport stdio <name> -- <command>
```

### Scopes (области видимости)

| Scope | Хранилище | Доступность | Приоритет |
|-------|-----------|-------------|-----------|
| **local** | `.claude/user-settings.json` | Только в текущем проекте | Highest |
| **project** | `.mcp.json` | Для всей команды через git | Middle |
| **user** | `~/.claude/settings.json` | Все проекты пользователя | Lowest |

### Возможности

- ✅ OAuth 2.0 аутентификация
- ✅ Resources (@mentions)
- ✅ Prompts (как slash commands)
- ✅ Tools (новые инструменты для Claude)
- ✅ Environment variable expansion в `.mcp.json`
- ✅ Plugin-provided MCP servers

### Пример конфигурации

```json
{
  "mcpServers": {
    "r2r-server": {
      "type": "http",
      "url": "http://136.119.36.216:7272",
      "headers": {
        "Authorization": "Bearer ${R2R_API_KEY}"
      }
    }
  }
}
```

### Критический вопрос: Как это применимо к R2R?

**Ответ:** MCP - это **ИДЕАЛЬНЫЙ механизм** для интеграции R2R!

**Преимущества:**
- HTTP transport для удалённого R2R API
- Можно создать MCP server, который обёртывает R2R endpoints
- Claude сможет автоматически использовать R2R tools
- Поддержка OAuth для безопасности
- Можно создать resources для документов

**А что если...?**
- А что если R2R API изменится? → Environment variables и конфигурация решают
- А что если нужна аутентификация? → OAuth 2.0 поддержка
- А что если нужно несколько инстансов R2R? → Разные MCP серверы с разными именами

---

## Hooks

### Что это?

Hooks - это система автоматизации на основе событий. Shell команды выполняются при определённых событиях в жизненном цикле Claude Code.

### Типы событий

| Событие | Когда происходит | Matcher поддержка |
|---------|------------------|-------------------|
| **PreToolUse** | Перед вызовом tool | ✅ |
| **PostToolUse** | После выполнения tool | ✅ |
| **PermissionRequest** | При запросе разрешения | ✅ |
| **Notification** | При отправке уведомлений | ✅ |
| **UserPromptSubmit** | При отправке prompt пользователем | ❌ |
| **Stop** | После завершения ответа main agent | ❌ |
| **SubagentStop** | После завершения subagent | ❌ |
| **PreCompact** | Перед compaction | ✅ (`manual`, `auto`) |
| **SessionStart** | При старте/resume сессии | ✅ (`startup`, `resume`, `clear`, `compact`) |
| **SessionEnd** | При завершении сессии | ❌ |

### Типы hooks

#### 1. Command hooks

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/script.sh",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

#### 2. Prompt-based hooks (LLM evaluation)

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate if Claude should stop: $ARGUMENTS",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### Hook Input/Output

**Input:** JSON через stdin с информацией о сессии и событии

**Output:**
- Exit code 0 → success
- Exit code 2 → blocking error
- JSON в stdout для advanced control

### Специальные возможности

#### SessionStart - Environment Persistence

```bash
#!/bin/bash
if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=production' >> "$CLAUDE_ENV_FILE"
  echo 'export R2R_API_KEY=...' >> "$CLAUDE_ENV_FILE"
fi
```

#### UserPromptSubmit - Context Injection

```python
#!/usr/bin/env python3
import json
import sys

# Add context from R2R
context = fetch_from_r2r(prompt)
print(context)  # Добавится в контекст Claude
sys.exit(0)
```

### Критический вопрос: Как это применимо к R2R?

**Потенциальные use cases:**

1. **SessionStart** → Загрузка свежей документации из R2R
2. **UserPromptSubmit** → Поиск релевантного контекста в R2R
3. **Stop** → Сохранение диалога в R2R Conversations
4. **SubagentStop** → Сохранение результата работы субагента
5. **PostToolUse** (Write/Edit) → Обновление знаний в R2R

**А что если...?**
- А что если R2R медленный? → Асинхронность + timeout настройки
- А что если сессия прервётся? → SessionEnd hook для cleanup
- А что если нужно добавить контекст? → UserPromptSubmit с stdout

---

## Subagents

### Что это?

Subagents - это специализированные AI ассистенты с:
- Собственным контекстом (отдельное context window)
- Кастомным system prompt
- Ограниченным набором tools
- Выбором модели (sonnet, opus, haiku)

### Конфигурация

```markdown
---
name: r2r-search-agent
description: Expert in searching R2R knowledge base. Use proactively when user asks questions about code or documentation.
tools: Read, Grep, Bash, mcp__r2r__search, mcp__r2r__rag
model: sonnet
permissionMode: default
skills: r2r-search-skill
---

You are an expert at searching the R2R knowledge base.

When the user asks a question:
1. First search R2R using semantic search
2. If needed, use RAG for detailed answers
3. Always cite your sources
```

### Типы

| Тип | Расположение | Scope | Приоритет |
|-----|--------------|-------|-----------|
| **Project** | `.claude/agents/` | Проект | Highest |
| **User** | `~/.claude/agents/` | Все проекты | Middle |
| **Plugin** | Plugin's `agents/` | С плагином | Variable |
| **CLI** | `--agents` flag | Сессия | Between project and user |
| **Built-in** | - | Всегда | Lowest |

### Built-in subagents

#### Plan subagent
- Используется в plan mode
- Модель: Sonnet
- Tools: Read, Glob, Grep, Bash
- Для research перед планированием

### Advanced: Resumable subagents

```bash
# Initial invocation
> Use the r2r-search-agent to find information about authentication
[Returns agentId: "abc123"]

# Resume later
> Resume agent abc123 and now check authorization patterns
```

### Критический вопрос: Как это применимо к R2R?

**Мощный инструмент для интеграции!**

**Use cases:**

1. **R2R Search Agent** - для поиска в документации
2. **R2R RAG Agent** - для ответов на вопросы с контекстом
3. **Knowledge Graph Agent** - для работы с графами знаний
4. **Documentation Updater** - для обновления документов в R2R

**А что если...?**
- А что если нужен длительный research? → Resumable agents!
- А что если нужно ограничить инструменты? → tools field
- А что если нужна более быстрая модель? → model: haiku

---

## Plugins

### Что это?

Plugins - это комплексные расширения, которые могут включать:
- Slash commands
- Subagents
- Skills
- Hooks
- MCP servers

### Структура плагина

```
my-r2r-plugin/
├── .claude-plugin/
│   └── plugin.json          # Metadata
├── commands/                 # Slash commands
│   ├── search-docs.md
│   └── update-docs.md
├── agents/                   # Subagents
│   └── r2r-assistant.md
├── skills/                   # Skills
│   └── r2r-search/
│       └── SKILL.md
├── hooks/                    # Hooks
│   └── hooks.json
└── .mcp.json                # MCP servers
```

### plugin.json

```json
{
  "name": "r2r-integration",
  "description": "Complete R2R integration for Claude Code",
  "version": "1.0.0",
  "author": {
    "name": "Your Name"
  }
}
```

### Распространение

#### Via Marketplace

```
marketplace/
├── .claude-plugin/
│   └── marketplace.json
└── plugins/
    └── r2r-integration/
```

#### Team Marketplaces

В `.claude/settings.json`:

```json
{
  "pluginMarketplaces": [
    {
      "name": "team-plugins",
      "source": "https://github.com/company/claude-plugins"
    }
  ],
  "plugins": [
    {
      "name": "r2r-integration",
      "marketplace": "team-plugins"
    }
  ]
}
```

### Критический вопрос: Как это применимо к R2R?

**Plugins - это ЛУЧШИЙ способ упаковать полную интеграцию!**

**Что включить:**
- MCP server для R2R API
- Subagents для разных задач
- Skills для специфичных операций
- Hooks для автоматизации
- Slash commands для быстрого доступа

**А что если...?**
- А что если нужно обновить? → Версионирование плагинов
- А что если разные команды? → Team marketplaces
- А что если конфликт? → Namespacing в MCP

---

## Skills

### Что это?

Skills - это модульные capabilities, которые Claude **автоматически** выбирает на основе контекста.

### Отличие от slash commands

| Aspect | Skills | Slash Commands |
|--------|--------|----------------|
| **Invocation** | Model-invoked | User-invoked |
| **Trigger** | По description | По имени команды |
| **Visibility** | Автоматическая | Явная (`/command`) |

### Структура

```
r2r-search-skill/
├── SKILL.md (required)
├── reference.md (optional)
├── examples.md (optional)
└── scripts/
    └── r2r_client.py
```

### SKILL.md

```yaml
---
name: r2r-documentation-search
description: Search R2R documentation and codebase. Use when user asks about R2R features, APIs, or needs examples from documentation.
allowed-tools: Read, Grep, Glob, mcp__r2r__search
---

# R2R Documentation Search

## Instructions

When the user asks about R2R:
1. Use semantic search to find relevant documentation
2. Check code examples in the codebase
3. Provide specific, actionable answers with code snippets

## Examples

- "How do I create a document in R2R?" → Search for document creation APIs
- "What's the conversation API?" → Search for conversation endpoints
```

### Типы

| Тип | Расположение | Scope |
|-----|--------------|-------|
| **Personal** | `~/.claude/skills/` | Все проекты |
| **Project** | `.claude/skills/` | Текущий проект |
| **Plugin** | Plugin's `skills/` | С плагином |

### Tool Restrictions

```yaml
---
name: safe-r2r-reader
description: Read-only access to R2R. Use when you only need to search, not modify.
allowed-tools: Read, Grep, mcp__r2r__search, mcp__r2r__rag
---
```

### Критический вопрос: Как это применимо к R2R?

**Skills идеальны для автоматического выбора правильного R2R функционала!**

**Use cases:**
1. **r2r-search-skill** - автоматический поиск при вопросах
2. **r2r-document-update** - обновление документации
3. **r2r-conversation-save** - сохранение диалогов
4. **r2r-knowledge-graph** - работа с KG

**А что если...?**
- А что если Skills конфликтуют? → Чёткие descriptions
- А что если нужно ограничить? → allowed-tools
- А что если несколько подходят? → Claude выбирает наиболее релевантный

---

## Output Styles

### Что это?

Output Styles адаптируют system prompt Claude Code для разных use cases.

### Built-in styles

1. **Default** - standard software engineering
2. **Explanatory** - с образовательными "Insights"
3. **Learning** - collaborative с TODO(human) markers

### Custom Output Style

```markdown
---
name: R2R Documentation Assistant
description: Specialized mode for working with R2R documentation and knowledge base
keep-coding-instructions: true
---

# R2R Documentation Assistant

You are a specialized assistant for R2R documentation.

When helping users:
- Always search R2R first before answering
- Cite specific documentation
- Provide code examples from R2R docs
- Keep answers concise and actionable
```

### Критический вопрос: Как это применимо к R2R?

**Можно создать специализированный режим для работы с R2R!**

**А что если...?**
- А что если пользователь работает только с R2R? → Custom output style
- А вдруг нужны и coding instructions? → keep-coding-instructions: true

---

## Headless Mode

### Что это?

Headless mode позволяет запускать Claude Code программно без интерактивного UI.

### Основные флаги

```bash
claude -p "query" \
  --output-format json \
  --allowedTools "Bash,Read,mcp__r2r" \
  --permission-mode acceptEdits \
  --append-system-prompt "Always search R2R first"
```

### Output formats

- **text** - plain text (default)
- **json** - structured data с метаданными
- **stream-json** - streaming messages

### Multi-turn conversations

```bash
# Start
session_id=$(claude -p "First query" --output-format json | jq -r '.session_id')

# Continue
claude -p --resume "$session_id" "Next query"
```

### Input formats

- **text** - простой текст
- **stream-json** - JSON lines для multi-turn без перезапуска

### Критический вопрос: Как это применимо к R2R?

**Headless mode критичен для автоматизации!**

**Use cases:**
1. **CI/CD** - автоматическое обновление документации в R2R
2. **Scheduled tasks** - периодическая синхронизация
3. **Webhooks** - реакция на события
4. **Batch processing** - массовая обработка документов

**Пример:**

```bash
#!/bin/bash
# Update R2R docs on git push

files=$(git diff --name-only HEAD~1 HEAD | grep '\.md$')

for file in $files; do
  claude -p "Update R2R with $file" \
    --output-format json \
    --allowedTools "Read,mcp__r2r__document_update" \
    --permission-mode bypassPermissions
done
```

**А что если...?**
- А что если нужна аутентификация? → Environment variables
- А что если нужно отслеживать прогресс? → JSON output с task_id
- А что если ошибка? → Exit codes + stderr

---

## Критический анализ

### Матрица применимости к R2R

| Механизм | Применимость | Сложность | Приоритет | Комментарий |
|----------|--------------|-----------|-----------|-------------|
| **MCP** | ⭐⭐⭐⭐⭐ | Medium | **🔥 HIGH** | Основной механизм интеграции |
| **Hooks** | ⭐⭐⭐⭐⭐ | Medium | **🔥 HIGH** | Автоматизация sync с R2R |
| **Subagents** | ⭐⭐⭐⭐⭐ | Low | **🔥 HIGH** | Специализированные R2R агенты |
| **Plugins** | ⭐⭐⭐⭐⭐ | High | **🔥 HIGH** | Упаковка всей интеграции |
| **Skills** | ⭐⭐⭐⭐ | Low | MEDIUM | Автоматический выбор R2R функций |
| **Output Styles** | ⭐⭐ | Low | LOW | Nice-to-have для спец. режимов |
| **Headless** | ⭐⭐⭐⭐ | Low | MEDIUM | Для автоматизации и CI/CD |

### Сценарии использования

#### Сценарий 1: Минимальная интеграция
- MCP server для R2R API
- 1-2 простых субагента
- Complexity: Low

#### Сценарий 2: Полная интеграция
- MCP server
- Hooks для автоматизации
- Несколько субагентов
- Skills для автовыбора
- Plugin для упаковки
- Complexity: High

#### Сценарий 3: Production-ready
- Всё из Сценария 2
- Headless mode для CI/CD
- Custom output styles
- Мониторинг и логирование
- Complexity: Very High

### Критические вопросы

#### 1. Параллельность
**Q:** Как работать параллельно с R2R, чтобы не блокировать Claude?

**A:**
- MCP async tools
- Hooks с timeout
- R2R orchestration (`run_with_orchestration=true`)
- Polling статусов в background hooks

#### 2. Производительность
**Q:** Что если R2R медленный?

**A:**
- Caching в MCP server
- Async operations в R2R
- Timeout настройки в hooks
- Haiku model для быстрых субагентов

#### 3. Надёжность
**Q:** Что если R2R недоступен?

**A:**
- Graceful degradation в MCP
- Fallback в hooks (exit code handling)
- Error handling в субагентах
- Retry logic

#### 4. Безопасность
**Q:** Как защитить API keys?

**A:**
- Environment variables
- Claude Code secure settings
- OAuth через MCP
- Scope-based access control

---

## Выводы для интеграции

### Рекомендуемый стек

```
┌─────────────────────────────────────┐
│         Claude Code Plugin          │
│      "r2r-integration-plugin"       │
├─────────────────────────────────────┤
│                                     │
│  📦 Components:                     │
│                                     │
│  1. MCP Server                      │
│     └─ R2R API wrapper              │
│     └─ Tools: search, rag, docs     │
│     └─ Resources: @r2r:doc://...    │
│                                     │
│  2. Hooks                           │
│     └─ SessionStart → Load context  │
│     └─ UserPromptSubmit → Search    │
│     └─ Stop → Save conversation     │
│     └─ PostToolUse → Update docs    │
│                                     │
│  3. Subagents                       │
│     └─ r2r-search (haiku, fast)     │
│     └─ r2r-rag (sonnet, quality)    │
│     └─ r2r-knowledge-graph (sonnet) │
│                                     │
│  4. Skills                          │
│     └─ r2r-document-search          │
│     └─ r2r-conversation-management  │
│                                     │
│  5. Commands                        │
│     └─ /r2r-search                  │
│     └─ /r2r-update-docs             │
│     └─ /r2r-save-conversation       │
│                                     │
└─────────────────────────────────────┘
```

### Этапы внедрения

#### Phase 1: MVP (Week 1-2)
- ✅ MCP server с базовыми R2R endpoints
- ✅ 1 субагент для search
- ✅ SessionStart hook для загрузки контекста

#### Phase 2: Core Features (Week 3-4)
- ✅ Полный набор MCP tools
- ✅ Hooks для автоматизации
- ✅ 3-4 специализированных субагента
- ✅ Skills для автовыбора

#### Phase 3: Polish (Week 5-6)
- ✅ Plugin упаковка
- ✅ Marketplace для команды
- ✅ Документация и примеры
- ✅ Headless mode примеры

#### Phase 4: Production (Week 7-8)
- ✅ Мониторинг и логирование
- ✅ Error handling и retry logic
- ✅ Performance optimizations
- ✅ Security audit

### Следующие шаги

1. ✅ Анализ R2R API
2. ✅ Анализ Claude Code механизмов
3. ⏭️ **Сопоставление требований и возможностей**
4. ⏭️ Детальная техническая спецификация
5. ⏭️ Примеры кода и имплементация

---

## Метаданные

- **Версия документа**: 1.0
- **Статус**: Завершён этап 2
- **Следующий шаг**: Сопоставление и архитектура
- **Критических вопросов**: 15+ проанализировано
- **Механизмов изучено**: 7
- **Рекомендуемый подход**: Plugin-based с MCP core
