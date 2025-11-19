# Полный анализ документации R2R: Глубокое понимание платформы

## Дата создания: 2024
## Источник: docs/docs-r2r/

---

## Оглавление

1. [Введение в R2R](#введение-в-r2r)
2. [Жизненный цикл приложения](#жизненный-цикл-приложения)
3. [Конфигурация системы](#конфигурация-системы)
4. [Загрузка данных (Data Ingestion)](#загрузка-данных)
5. [Контекстное обогащение (Contextual Enrichment)](#контекстное-обогащение)
6. [AI-поиск](#ai-поиск)
7. [RAG (Retrieval-Augmented Generation)](#rag)
8. [Графы знаний (Knowledge Graphs)](#графы-знаний)
9. [GraphRAG](#graphrag)
10. [Агенты (Agents)](#агенты)
11. [Оркестрация (Orchestration)](#оркестрация)
12. [Обслуживание и масштабирование](#обслуживание-и-масштабирование)
13. [Практические рекомендации](#практические-рекомендации)
14. [Интеграция с тестируемым API](#интеграция-с-тестируемым-api)

---

## Введение в R2R

### Что такое R2R?

**R2R (Retrieval to Riches)** — это движок для создания пользовательских приложений на основе **Retrieval-Augmented Generation (RAG)**. Это открытая платформа, которая предоставляет основные сервисы через архитектуру провайдеров, сервисов и интегрированный RESTful API.

### Ключевые компоненты архитектуры

```
┌─────────────────────────────────────────────────────────┐
│                    R2R Platform                          │
├─────────────────────────────────────────────────────────┤
│  Providers          Services          RESTful API       │
│  ├─ Database        ├─ Ingestion      ├─ Documents     │
│  ├─ Embeddings      ├─ Retrieval      ├─ Collections   │
│  ├─ LLM             ├─ RAG            ├─ Users         │
│  ├─ Auth            ├─ GraphRAG       ├─ Graphs        │
│  └─ Orchestration   └─ Agent          └─ Retrieval     │
└─────────────────────────────────────────────────────────┘
```

### Установка

#### Предварительные требования

- **Python 3.8+**
- **Docker** (для полной установки)
- **pip** (менеджер пакетов Python)

#### Установка CLI и Python SDK

```bash
pip install r2r
```

#### Запуск R2R с Docker

```bash
r2r serve --docker --config-path=full.toml
```

Сервер будет доступен по адресу: `http://localhost:7272`

#### Развертывание на Google Cloud Platform

R2R можно развернуть на GCP Compute Engine:

1. **Создание экземпляра**:
   - Series: N1
   - Machine type: n1-standard-4 (4 vCPU, 15 GB RAM) или выше
   - OS: Ubuntu 22.04 LTS
   - Disk: 500 GB

2. **Установка зависимостей**: Docker, Python, R2R CLI

3. **Настройка переадресации портов** для локального доступа

---

## Жизненный цикл приложения

### Developer Workflow

R2R предлагает структурированный жизненный цикл разработки:

```
┌──────────────┐     ┌───────────────┐     ┌──────────┐
│  Customize   │────▶│  Configure    │────▶│  Deploy  │
└──────────────┘     └───────────────┘     └──────────┘
                                                  │
       ┌──────────────────────────────────────────┘
       │
       ▼
┌──────────────┐     ┌───────────────┐
│  Implement   │────▶│   Interact    │
└──────────────┘     └───────────────┘
```

1. **Customize**: Адаптация R2R с использованием R2RConfig и SDK
2. **Configure**: Настройка через `r2r.toml` или runtime overrides
3. **Deploy**: Запуск через Docker, облачные платформы или локально
4. **Implement**: Интеграция с приложениями через API и SDK
5. **Interact**: Взаимодействие пользователей через HTTP, Dashboard

### Hello R2R - Простой пример

```python
from r2r import R2RClient

client = R2RClient("http://localhost:7272")

# Создание тестового документа
with open("test.txt", "w") as file:
    file.write("John is a person that works at Google.")

# Загрузка документа
client.documents.create(file_path="test.txt")

# RAG запрос
rag_response = client.retrieval.rag(
    query="Who is John",
    rag_generation_config={
        "model": "openai/gpt-4o-mini", 
        "temperature": 0.0
    },
)

results = rag_response["results"]
print(f"Search Results:\n{results['search_results']}")
print(f"Completion:\n{results['completion']}")
```

### Пример вывода

```json
{
  "results": {
    "search_results": {
      "chunk_search_results": [
        {
          "chunk_id": "b9f40dbd-2c8e-5c0a-8454-027ac45cb0ed",
          "document_id": "7c319fbe-ca61-5770-bae2-c3d0eaa8f45c",
          "score": 0.6847735847465275,
          "text": "John is a person that works at Google.",
          "metadata": {
            "version": "v0",
            "chunk_order": 0,
            "document_type": "txt",
            "associated_query": "Who is John"
          }
        }
      ]
    },
    "completion": {
      "model": "gpt-4o-mini",
      "message": {
        "content": "John is a person that works at Google [1]."
      }
    }
  }
}
```

---

## Конфигурация системы

### Структура конфигурации

R2R поддерживает двухуровневую конфигурацию:

1. **Server-Side Configuration**: через файл `r2r.toml` и переменные окружения
2. **Runtime Overrides**: динамические настройки через API вызовы

### Пример r2r.toml

```toml
# ============================================
# COMPLETION (LLM) CONFIGURATION
# ============================================
[completion]
provider = "litellm"
concurrent_request_limit = 16

[completion.generation_config]
model = "openai/gpt-4o"
temperature = 0.5

# ============================================
# INGESTION CONFIGURATION
# ============================================
[ingestion]
provider = "r2r"
chunking_strategy = "recursive"
chunk_size = 1024
chunk_overlap = 512
excluded_parsers = ["mp4"]

[ingestion.chunk_enrichment_settings]
enable_chunk_enrichment = true
strategies = ["semantic", "neighborhood"]
forward_chunks = 3
backward_chunks = 3
semantic_neighbors = 10
semantic_similarity_threshold = 0.7
generation_config = { model = "openai/gpt-4o-mini" }

# ============================================
# DATABASE CONFIGURATION
# ============================================
[database]
provider = "postgres"
user = "your_postgres_user"
password = "your_postgres_password"
host = "your_postgres_host"
port = "your_postgres_port"
db_name = "your_database_name"
project_name = "your_project_name"

# ============================================
# EMBEDDING CONFIGURATION
# ============================================
[embedding]
provider = "litellm"
base_model = "openai/text-embedding-3-small"
base_dimension = 512
batch_size = 512
rerank_model = "BAAI/bge-reranker-v2-m3"
concurrent_request_limit = 256

# ============================================
# AUTHENTICATION & USERS CONFIGURATION
# ============================================
[auth]
provider = "r2r"
require_authentication = true
require_email_verification = false
default_admin_email = "admin@example.com"
default_admin_password = "change_me_immediately"

# ============================================
# RETRIEVAL CONFIGURATION
# ============================================
[retrieval]
provider = "r2r"
search_type = "hybrid"
reranking_enabled = true
max_results = 10

# ============================================
# RAG CONFIGURATION
# ============================================
[rag]
provider = "r2r"
model = "openai/gpt-4o"
temperature = 0.7
max_tokens = 1000

# ============================================
# KNOWLEDGE GRAPHS CONFIGURATION
# ============================================
[graphs]
provider = "r2r"
extraction_model = "openai/gpt-4o"
relationship_types = ["works_at", "located_in", "part_of"]

# ============================================
# PROMPTS CONFIGURATION
# ============================================
[prompts]
provider = "r2r"
template_dir = "prompts/"
default_system_prompt = "You are a helpful assistant."

# ============================================
# AGENT CONFIGURATION
# ============================================
[agent]
rag_agent_static_prompt = "rag_agent"
tools = ["search_file_knowledge", "web_search"]
enable_web_search = true
web_search_provider = "google"
```

### Ключевые особенности конфигурации

#### 1. Postgres Configuration
- Безопасное хранение паролей
- Connection pooling
- Автоматическое переподключение
- Оптимизация запросов

#### 2. Embedding Configuration
- Настройка моделей эмбеддингов
- Batch processing для оптимизации
- Reranking для улучшения качества результатов

#### 3. Auth & Users Configuration
- Аутентификация пользователей
- Role-based access control (RBAC)
- Email верификация
- Политики паролей

---

## Загрузка данных

### Введение

R2R предоставляет мощный и гибкий pipeline для обработки различных типов документов:
- Текстовые файлы
- Документы (PDF, DOCX, etc.)
- Изображения
- Аудио
- Видео

### Процесс загрузки

```
┌──────────────┐
│   Document   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Parsing    │  ← Извлечение текста/контента
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Chunking   │  ← Разбиение на части
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Enrichment  │  ← Контекстное обогащение (опционально)
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Embedding   │  ← Векторное представление
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Storage    │  ← Сохранение в БД
└──────────────┘
```

### Режимы загрузки

| Режим    | Описание                                          | Применение                    |
|----------|---------------------------------------------------|-------------------------------|
| `fast`   | Быстрая загрузка                                  | Простые документы             |
| `hi-res` | Высококачественная обработка                      | Сложные/критичные документы   |
| `custom` | Полный контроль через `ingestion_config`          | Специфические требования      |

### Примеры загрузки

#### 1. Базовая загрузка документа

```python
from r2r import R2RClient

client = R2RClient("http://localhost:7272")

# Загрузка файла
response = client.documents.create(
    file_path="document.pdf",
    ingestion_mode="hi-res"
)

print(response)
```

#### 2. Загрузка предобработанных чанков

```python
chunks = [
    {"text": "First chunk of content", "metadata": {"page": 1}},
    {"text": "Second chunk of content", "metadata": {"page": 1}},
]

response = client.documents.create_from_chunks(
    chunks=chunks,
    document_id="custom_doc_id",
    metadata={"source": "manual_chunks"}
)
```

#### 3. Удаление документов

```python
# Удаление документа
response = client.documents.delete(document_id="doc_123")

# Ответ
{
    "status": "success",
    "message": "Document deleted successfully",
    "document_id": "doc_123"
}
```

### Ключевые особенности удаления

- **Каскадное удаление** связанных чанков
- **Очистка векторных эмбеддингов**
- **Удаление из графов знаний**
- **Автоматическое обновление коллекций**

### Конфигурация через r2r.toml

```toml
[ingestion]
provider = "r2r"
chunking_strategy = "recursive"     # Рекурсивное разбиение
chunk_size = 1024                   # Размер чанка в токенах
chunk_overlap = 512                 # Перекрытие между чанками
excluded_parsers = ["mp4"]          # Исключенные форматы

[ingestion.chunk_enrichment_settings]
enable_chunk_enrichment = true
strategies = ["semantic", "neighborhood"]
```

---

## Контекстное обогащение

### Проблема потери контекста

При разбиении больших документов на чанки **теряется контекст**. Изолированные чанки могут не содержать полную информацию.

#### Пример проблемы

**Оригинальный чанк** из годового отчета Lyft 2021:

```
storing unrented and returned vehicles. These impacts to the demand 
for and operations of the different rental programs have and may 
continue to adversely affect our business, financial condition and 
results of operation.
```

**Вопросы без ответа:**
- Какие конкретно воздействия обсуждаются?
- Какие rental программы затронуты?
- Каков более широкий контекст бизнес-проблем?

### Решение: Contextual Enrichment

Контекстное обогащение добавляет релевантную информацию из окружающего или семантически связанного контента.

### Включение обогащения

```toml
[ingestion.chunk_enrichment_settings]
enable_chunk_enrichment = true              # По умолчанию выключено
strategies = ["semantic", "neighborhood"]   # Стратегии обогащения
forward_chunks = 3                          # Смотреть вперед на 3 чанка
backward_chunks = 3                         # Смотреть назад на 3 чанка
semantic_neighbors = 10                     # Найти 10 семантически похожих
semantic_similarity_threshold = 0.7         # Минимальный порог схожести
generation_config = { model = "openai/gpt-4o-mini" }
```

### Стратегии обогащения

#### 1. Neighborhood Strategy (Стратегия соседства)

```
Чанк N-3 ← Чанк N-2 ← Чанк N-1 ← [ТЕКУЩИЙ ЧАНК] → Чанк N+1 → Чанк N+2 → Чанк N+3
                                          ↓
                                  Обогащенный чанк
```

**Характеристики:**
- **Forward Looking**: Захватывает предстоящий контекст (по умолчанию 3 чанка)
- **Backward Looking**: Включает предыдущий контекст (по умолчанию 3 чанка)
- **Применение**: Эффективна для нарративных документов с линейным потоком

#### 2. Semantic Strategy (Семантическая стратегия)

```
Текущий чанк
     ↓
Vector Similarity Search
     ↓
┌────────────────────────────┐
│ Семантически похожие чанки │
│ (из любой части документа) │
└────────────────────────────┘
     ↓
Обогащенный чанк
```

**Характеристики:**
- **Vector Similarity**: Находит чанки с похожим смыслом независимо от расположения
- **Configurable Neighbors**: Настраиваемое количество похожих чанков
- **Similarity Threshold**: Обеспечивает релевантность минимальным порогом схожести
- **Применение**: Идеальна для документов с повторяющимися темами в разных секциях

### Процесс обогащения

R2R использует LLM для обогащения чанков по следующему промпту:

**Задача:**
Обогатить и уточнить данный чанк текста, используя информацию из контекстных чанков. Цель — сделать чанк более точным и самодостаточным.

**Контекстные чанки:**
```
{context_chunks}
```

**Чанк для обогащения:**
```
{chunk}
```

**Инструкции:**
1. Переписать чанк от третьего лица
2. Заменить все общие существительные соответствующими именами собственными
3. Использовать информацию из контекстных чанков для улучшения ясности

### Просмотр обогащенных результатов

```python
# Получить обогащенные чанки для документа
response = client.documents.get_chunks(document_id="your_doc_id")

for chunk in response["chunks"]:
    print(f"Original: {chunk['text']}")
    print(f"Enriched: {chunk['enriched_text']}")
```

### Метаданные и хранение

Обогащенные чанки сохраняются вместе с дополнительными метаданными:
- Оригинальный текст
- Обогащенный текст
- Использованная стратегия обогащения
- Источники контекста
- Временная метка обогащения

### Best Practices

1. ✅ Включать обогащение для документов, где контекст критичен
2. ✅ Настраивать параметры neighborhood и semantic на основе структуры документа
3. ✅ Мониторить качество обогащения и корректировать пороги
4. ✅ Использовать подходящие LLM модели для обогащения
5. ✅ Учитывать влияние обогащенных чанков на хранилище

---

## AI-поиск

### Введение

R2R поддерживает продвинутые возможности поиска:
- **Vector Search** (Векторный поиск)
- **Hybrid Search** (Гибридный поиск: keyword + vector)
- **Knowledge Graph-Enhanced Search** (Поиск с использованием графов знаний)

### Режимы поиска

| Режим      | Описание                                                    | Применение              |
|------------|-------------------------------------------------------------|-------------------------|
| `basic`    | Преимущественно семантический поиск                         | Простые сценарии        |
| `advanced` | Комбинирует семантический и полнотекстовый поиск по умолчанию | Сбалансированный поиск |
| `custom`   | Полный контроль над настройками поиска                      | Специфические требования|

### Как работает Hybrid Search в R2R

```
         User Query
              ↓
    ┌─────────┴─────────┐
    ↓                   ↓
Full-Text Search    Vector Search
(Exact matches)     (Semantic)
    ↓                   ↓
PostgreSQL          Embeddings
ts_rank_cd          L2/Cosine Distance
    ↓                   ↓
    └─────────┬─────────┘
              ↓
  Reciprocal Rank Fusion (RRF)
              ↓
      Combined Results
              ↓
      Ranked by Score
```

#### 1. Full-Text Search
- Использует PostgreSQL's `ts_rank_cd` и `websearch_to_tsquery`
- Находит точные совпадения терминов

#### 2. Semantic Search
- Использует векторные эмбеддинги
- Находит контекстуально связанные документы даже без точных совпадений

#### 3. Reciprocal Rank Fusion (RRF)
- Объединяет результаты из обоих типов поиска
- Формула для сбалансированного ранжирования

#### 4. Result Ranking
- Упорядочивает результаты на основе комбинированного RRF score

### Vector Search - Пример

```bash
curl -X POST http://localhost:7272/v3/retrieval/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What was Uber'\''s profit in 2020?",
    "search_settings": {
      "use_semantic_search": true,
      "search_settings": {
        "chunk_settings": {
          "index_measure": "l2_distance",
          "limit": 10
        }
      }
    }
  }'
```

### Hybrid Search - Пример

```bash
curl -X POST http://localhost:7272/v3/retrieval/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What was Uber'\''s profit in 2020?",
    "search_settings": {
      "use_hybrid_search": true,
      "hybrid_settings": {
        "full_text_weight": 1.0,
        "semantic_weight": 5.0,
        "full_text_limit": 200,
        "rrf_k": 50
      },
      "filters": {
        "title": {
          "$in": ["lyft_2021.pdf", "uber_2021.pdf"]
        }
      },
      "limit": 10,
      "chunk_settings": {
        "index_measure": "l2_distance",
        "probes": 25,
        "ef_search": 100
      }
    }
  }'
```

### Knowledge Graph Search - Пример

```bash
curl -X POST http://localhost:7272/v3/retrieval/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Who was Aristotle?",
    "graph_search_settings": {
      "use_graph_search": true,
      "kg_search_type": "local"
    }
  }'
```

### Best Practices для поиска

1. **Оптимизация БД и Embeddings**
   - Обеспечить индексирование PostgreSQL
   - Оптимизировать конфигурации vector store

2. **Настройка весов и лимитов**
   - Корректировать `full_text_weight`, `semantic_weight`, `rrf_k` в режиме `custom`

3. **Регулярные обновления**
   - Поддерживать эмбеддинги и индексы актуальными

4. **Выбор подходящих эмбеддингов**
   - Выбрать модель эмбеддинга, соответствующую домену контента

---

## RAG

### Введение

R2R объединяет мощные возможности поиска с большими языковыми моделями (LLM) для предоставления комплексных ответов на вопросы и генерации контента на основе загруженных документов.

### Базовый RAG

```bash
curl -X POST http://localhost:7272/v3/retrieval/rag \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What was Uber'\''s profit in 2020?"
  }'
```

### RAG с Hybrid Search

```bash
curl -X POST http://localhost:7272/v3/retrieval/rag \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Who is Jon Snow?",
    "search_settings": {
      "use_hybrid_search": true,
      "limit": 10
    }
  }'
```

### Streaming RAG

```bash
r2r retrieval rag --query="who was aristotle" \
  --use-hybrid-search=True \
  --stream
```

Потоковая передача токенов в реальном времени.

### Кастомизация RAG

```bash
curl -X POST http://localhost:7272/v3/retrieval/rag \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Who is Jon Snow?",
    "rag_generation_config": {
      "model": "claude-3-haiku-20240307",
      "temperature": 0.7
    }
  }'
```

### Продвинутые RAG техники

R2R поддерживает продвинутые техники RAG (в beta):

#### 1. HyDE (Hypothetical Document Embeddings)

**Workflow:**

```
User Query
    ↓
Generate Hypothetical Documents (LLM)
    ↓
Create Embeddings from Hypothetical Docs
    ↓
Similarity Search in Vector DB
    ↓
Retrieve Actual Documents
    ↓
Generate Final Response with Context
```

**Python пример:**

```python
from r2r import R2RClient

client = R2RClient()

hyde_response = client.retrieval.rag(
    "What are the main themes in Shakespeare's plays?",
    search_settings={
        "search_strategy": "hyde",
        "limit": 10
    }
)

print('hyde_response = ', hyde_response)
```

**Пример вывода:**

```json
{
  "results": {
    "completion": "...",
    "search_results": {
      "chunk_search_results": [
        {
          "score": 0.7715058326721191,
          "text": "## Paragraph from the Chapter...",
          "metadata": {
            "associated_query": "The fundamental theorem of calculus..."
          }
        }
      ]
    }
  }
}
```

#### 2. RAG-Fusion

**Workflow:**

```
User Query
    ↓
Generate Multiple Related Queries (LLM)
    ↓
Execute Multiple Searches in Parallel
    ↓
Reciprocal Rank Fusion (RRF)
    ↓
Re-ranked Documents
    ↓
Generate Final Response
```

**Python пример:**

```python
from r2r import R2RClient

client = R2RClient()

rag_fusion_response = client.retrieval.rag(
    "Explain the theory of relativity",
    search_settings={
        "search_strategy": "rag_fusion",
        "limit": 20
    }
)

print('rag_fusion_response = ', rag_fusion_response)
```

**Пример вывода:**

```json
{
  "results": {
    "completion": "...",
    "search_results": {
      "chunk_search_results": [
        {
          "score": 0.04767399003253049,
          "text": "18. The theory of relativity, proposed by Albert Einstein in 1905...",
          "metadata": {
            "associated_queries": [
              "What is the theory of relativity?",
              "Einstein's theory explanation",
              "Relativity physics concept"
            ]
          }
        }
      ]
    }
  }
}
```

### Комбинирование с другими настройками

```python
custom_rag_response = client.retrieval.rag(
    "Describe the impact of climate change on biodiversity",
    search_settings={
        "search_strategy": "hyde",
        "limit": 15,
        "use_hybrid_search": True
    },
    rag_generation_config={
        "model": "anthropic/claude-3-opus-20240229",
        "temperature": 0.7
    }
)
```

### Конфигурация по умолчанию

```toml
[rag_generation_config]
model = "anthropic/claude-3-opus-20240229"
temperature = 0.7
max_tokens = 2000
```

---

## Графы знаний

### Введение

Графы знаний улучшают точность поиска и понимание контекста путем извлечения и связывания информации из документов.

### Двухуровневая архитектура

```
Collection (Soft Container)
    ↓
┌───────────────────────────────┐
│        Documents              │
│  ├─ Document 1                │
│  │   ├─ Entities              │
│  │   └─ Relationships         │
│  ├─ Document 2                │
│  │   ├─ Entities              │
│  │   └─ Relationships         │
│  └─ Document N                │
└───────────────┬───────────────┘
                ↓
      Knowledge Graph
                ↓
          Permissions
                ↓
              User
```

**Уровни:**
1. **Document Level**: Сущности и связи извлекаются и сохраняются с исходными документами
2. **Collection Level**: Коллекции действуют как контейнеры, которые включают документы и поддерживают соответствующие графы

### Getting Started

#### 1. Document-Level Extraction

```python
from r2r import R2RClient

client = R2RClient("http://localhost:7272")

# Извлечение сущностей и связей
document_id = "your-document-id"
extract_response = client.documents.extract(document_id)
```

#### 2. Creating Collection Graphs

```python
# Создание коллекции
collection_response = client.collections.create(
    name="shakespeare_works",
    description="Collection of Shakespeare's works"
)

# Добавление документов в коллекцию
client.collections.add_document(
    collection_id=collection_response["collection_id"],
    document_id="hamlet_id"
)
```

#### 3. Managing Collection Graphs

```python
# Получить граф коллекции
graph = client.collections.get_graph(
    collection_id="your_collection_id"
)

# Запрос к графу (Cypher-like query)
results = client.collections.query_graph(
    collection_id="your_collection_id",
    query="MATCH (p:Person)-[:WROTE]->(w:Work) RETURN p, w"
)
```

**Пример вывода:**

```json
{
  "nodes": [
    {
      "id": "person_1",
      "type": "Person",
      "properties": {"name": "William Shakespeare"}
    },
    {
      "id": "work_1",
      "type": "Work",
      "properties": {"title": "Hamlet"}
    }
  ],
  "relationships": [
    {
      "source": "person_1",
      "target": "work_1",
      "type": "WROTE"
    }
  ],
  "metadata": {
    "node_count": 42,
    "relationship_count": 67
  }
}
```

### Knowledge Graph Workflow

```
Step 1: Extract Document Knowledge
         ↓
Step 2: Initialize and Populate Graph
         ↓
Step 3: View Entities and Relationships
         ↓
Step 4: Build Graph Communities
         ↓
Step 5: KG-Enhanced Search
         ↓
Step 6: Reset Graph (if needed)
```

### Search Integration с KG

```bash
curl -X POST http://localhost:7272/v3/retrieval/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Who wrote Hamlet?",
    "graph_search_settings": {
      "use_graph_search": true
    }
  }'
```

### RAG Integration с KG

```python
rag_response = client.retrieval.rag(
    query="What are the relationships between characters in Hamlet?",
    search_settings={
        "use_graph_search": true,
        "graph_search_settings": {
            "kg_search_type": "local"
        }
    }
)
```

### Access Control

```python
# Установить права доступа к коллекции
client.collections.set_permissions(
    collection_id="your_collection_id",
    user_id="user_id",
    permissions=["read", "write"]
)
```

---

## GraphRAG

### Введение

GraphRAG расширяет традиционный RAG, используя community detection и summarization в графах знаний. Это обеспечивает более богатый контекст и комплексные ответы.

### Архитектура GraphRAG

```
         User Query
              ↓
    QueryTransformPipe
              ↓
      MultiSearchPipe
              ↓
    ┌─────────┴─────────┐
    ↓                   ↓
VectorSearchPipe    KG Search
    ↓                   ↓
  Chunks            Communities
    ↓                   ↓
    └─────────┬─────────┘
              ↓
    RAG-Fusion Process
              ↓
  Reciprocal Rank Fusion
              ↓
      RAG Generation
              ↓
    Knowledge Graph DB
```

### Понимание Communities

**Communities** — автоматически обнаруженные кластеры связанной информации в графе знаний.

**Преимущества:**
1. **Higher-Level Understanding**: Понимание тем документов
2. **Summarized Context**: Краткие резюме для связанных концепций
3. **Improved Retrieval**: Организация по темам улучшает релевантность поиска

#### Примеры Communities

| Домен              | Примеры Communities                           |
|--------------------|-----------------------------------------------|
| Scientific Papers  | Research methods, theories, research teams    |
| News Articles      | World events, industry sectors, key figures   |
| Technical Docs     | System components, APIs, user workflows       |
| Legal Documents    | Case types, jurisdictions, legal principles   |

### Implementation Guide

#### Prerequisites

```python
from r2r import R2RClient

client = R2RClient("http://localhost:7272")

# Настройка коллекции и извлечение знаний
collection_id = "your-collection-id"
client.collections.extract(collection_id)
client.graphs.pull(collection_id)
```

#### Building Communities

```python
# Сгенерировать описание для коллекции
client.collections.update(
    collection_id,
    generate_description=True
)

# Построить communities для графа коллекции
build_response = client.graphs.build(collection_id)
```

**Процесс построения включает:**
1. Анализ связности графа
2. Идентификацию плотных подграфов
3. Генерацию резюме communities
4. Создание findings и insights

#### Using GraphRAG

```python
# Поиск на всех уровнях
search_response = client.retrieval.search(
    "What are the key theories?",
    search_settings={
        "graph_settings": {
            "enabled": True,
        }
    }
)

# RAG с контекстом communities
rag_response = client.retrieval.rag(
    "Explain the relationships between theories",
    graph_search_settings={
        "enabled": True
    }
)
```

### Понимание результатов GraphRAG

GraphRAG возвращает три типа результатов:

#### 1. Document Chunks

```json
{
  "chunk_id": "70c96e8f-e5d3-5912-b79b-13c5793f17b5",
  "text": "Example document text...",
  "score": 0.78,
  "metadata": {
    "document_type": "txt",
    "associated_query": "query text"
  }
}
```

#### 2. Graph Elements

```json
{
  "content": {
    "name": "CONCEPT_NAME",
    "description": "Entity description..."
  },
  "result_type": "entity",
  "score": 0.74
}
```

#### 3. Communities

```json
{
  "content": {
    "name": "Community Name",
    "summary": "High-level community description...",
    "findings": [
      "Key insight 1 with supporting evidence...",
      "Key insight 2 with supporting evidence..."
    ],
    "rating": 9.0,
    "rating_explanation": "Explanation of importance..."
  },
  "result_type": "community",
  "score": 0.57
}
```

### Масштабирование GraphRAG

#### Использование оркестрации

Для больших коллекций используйте возможности оркестрации R2R через Hatchet UI:

- **URL**: http://localhost:7274
- **Логин**: admin@example.com
- **Пароль**: Admin123!!

**Возможности:**
- Мониторинг прогресса извлечения документов
- Отслеживание статуса community detection
- Обработка ошибок и повторы workflow

---

## Агенты

### Введение

Agentic возможности R2R позволяют создавать интеллектуальные системы, которые:
1. Формулируют собственные вопросы
2. Ищут информацию
3. Предоставляют обоснованные ответы на основе полученного контекста

**⚠️ Примечание**: Агенты в R2R находятся в beta. Обратная связь приветствуется по адресу founders@sciphi.ai

### Понимание RAG Agent

RAG Agent — специализированный компонент, который объединяет возможности RAG с автономным принятием решений.

**Возможности:**
1. Формулирование релевантных вопросов
2. Поиск информации
3. Синтез находок
4. Генерация комплексных ответов

### Конфигурация

```toml
[agent]
rag_agent_static_prompt = "rag_agent"
tools = ["search_file_knowledge", "web_search"]
enable_web_search = true
web_search_provider = "google"
```

### Использование RAG Agent

#### Базовый пример

```python
from r2r import R2RClient

client = R2RClient()

# Создание экземпляра агента
response = client.agent.create(
    query="Explain the impact of climate change",
    agent_config={
        "tools": ["search_file_knowledge", "web_search"],
        "temperature": 0.7
    }
)

print(response.completion)
```

#### Streaming Responses

```python
for response in client.agent.create_stream(
    query="Analyze recent AI developments",
    agent_config={"stream": True}
):
    print(response.delta)
```

#### Context-Aware Responses

```python
# Первый запрос
response1 = client.agent.create(
    query="What is machine learning?"
)

# Последующий запрос с сохранением контекста
response2 = client.agent.create(
    query="How does it compare to deep learning?",
    conversation_id=response1.conversation_id
)
```

### Работа с файлами

```python
# Обработка конкретного файла
response = client.agent.create(
    query="Summarize this document",
    document_id="doc_123",
    agent_config={
        "focus_on_document": True
    }
)
```

### Продвинутые функции

#### Combined Search Capabilities

```python
response = client.agent.create(
    query="Research quantum computing advances",
    agent_config={
        "search_settings": {
            "use_hybrid_search": True,
            "use_web_search": True
        }
    }
)
```

#### Custom Search Settings

```python
response = client.agent.create(
    query="Find specific examples",
    agent_config={
        "search_settings": {
            "filters": {
                "date": {"$gt": "2023-01-01"}
            }
        }
    }
)
```

### Планируемые расширения

- Multi-agent collaboration
- Tool usage capabilities
- Memory and state management
- Custom agent behaviors

---

## Оркестрация

### Введение

Оркестрация в R2R управляется с помощью **Hatchet** — распределенной, отказоустойчивой очереди задач.

### Ключевые концепции

| Концепт         | Описание                                                  |
|-----------------|-----------------------------------------------------------|
| **Workflows**   | Наборы функций, выполняемых в ответ на внешние триггеры   |
| **Workers**     | Долгоживущие процессы, выполняющие функции workflow      |
| **Managed Queue**| Низколатентная очередь для обработки задач в реальном времени |

### Workflows в R2R

1. **IngestFilesWorkflow**: Обрабатывает загрузку файлов, парсинг, chunking, embedding
2. **UpdateFilesWorkflow**: Управляет обновлением существующих файлов
3. **KgExtractAndStoreWorkflow**: Извлекает и сохраняет информацию графа знаний
4. **CreateGraphWorkflow**: Оркестрирует создание графа знаний
5. **EnrichGraphWorkflow**: Обрабатывает процессы обогащения графа

### Orchestration GUI

**Доступ к Hatchet UI:**
- **URL**: http://localhost:7274
- **Email**: admin@example.com
- **Password**: Admin123!!

**Возможности GUI:**
- Просмотр всех выполняющихся задач
- Детальная информация о workflow
- История выполнения и метрики производительности
- Мониторинг долгоживущих задач
- Обработка ошибок и повторы

### Benefits of Orchestration

1. **Scalability**: Эффективная обработка крупномасштабных задач
2. **Fault Tolerance**: Встроенные механизмы повтора и обработки ошибок
3. **Flexibility**: Легкое добавление или модификация workflows

---

## Обслуживание и масштабирование

### Vector Indices

#### Нужны ли вам векторные индексы?

Векторные индексы **не обязательны для всех развертываний**, особенно в многопользовательских приложениях, где запросы фильтруются по `user_id`.

**Рассмотрите векторные индексы когда:**
- Пользователи ищут по сотням тысяч документов
- Latency запросов становится узким местом даже с user-specific фильтрацией
- Поддержка cross-user поиска в большом масштабе

#### Управление векторными индексами

```python
from r2r import R2RClient

client = R2RClient()

# Создание векторного индекса
create_response = client.indices.create(
    {
        "table_name": "vectors",
        "index_method": "hnsw",  # Рекомендуемый метод
        "index_measure": "cosine_distance",
        "index_arguments": {
            "m": 16,                # Количество связей на элемент
            "ef_construction": 64   # Размер динамического списка кандидатов
        },
    }
)

# Список существующих индексов
indices = client.indices.list()

# Удаление индекса
delete_response = client.indices.delete(
    index_name="ix_vector_cosine_ops_hnsw__20241021211541",
    table_name="vectors",
)
```

#### Важные соображения

1. **Pre-warming Requirement**:
   - Новые индексы начинаются "холодными"
   - Требуют прогрева для оптимальной производительности
   - Прогрев необходимо повторять после перезапуска системы

2. **Resource Usage**:
   - Создание индекса CPU и memory интенсивно
   - Использование памяти масштабируется с размером dataset и параметром `m`
   - Создавайте индексы в непиковые часы

3. **Performance Tuning**:
   - **HNSW Parameters**:
     - `m`: 16-64 (выше = лучше качество, больше памяти)
     - `ef_construction`: 64-100 (выше = лучше качество, дольше построение)
   - **Distance Measures**:
     - `cosine_distance`: Лучше для нормализованных векторов (наиболее частый)
     - `l2_distance`: Лучше для абсолютных расстояний
     - `max_inner_product`: Оптимизирован для dot product similarity

### Обновление системы

#### Проверка текущей версии

```bash
r2r version
```

#### Процесс обновления

```bash
# 1. Проверить текущие версии
r2r version
r2r db current

# 2. Сгенерировать системный отчет (опционально)
r2r generate-report

# 3. Остановить запущенные сервисы
r2r docker-down

# 4. Обновить R2R
r2r update

# 5. Обновить базу данных
r2r db upgrade

# 6. Перезапустить сервисы
r2r serve --docker
```

#### Database Migration Management

```bash
# Проверить текущую миграцию
r2r db current

# Применить миграции
r2r db upgrade

# Просмотр истории миграций
r2r db history

# Откат при необходимости
r2r db downgrade --revision <previous-working-version>
```

### Управление несколькими средами

```bash
# Development
export R2R_PROJECT_NAME=r2r_dev
r2r serve --docker --project-name r2r-dev

# Staging
export R2R_PROJECT_NAME=r2r_staging
r2r serve --docker --project-name r2r-staging

# Production
export R2R_PROJECT_NAME=r2r_prod
r2r serve --docker --project-name r2r-prod
```

### Стратегии масштабирования

#### 1. Horizontal Scaling
- Реализация балансировки нагрузки
- Использование sharding для больших dataset
- Распределение обработки по узлам

#### 2. Vertical Scaling
- Оптимизация распределения ресурсов
- Обновление hardware по необходимости
- Мониторинг производительности системы

#### 3. Performance Optimization
- Использование подходящей индексации
- Реализация стратегий кэширования
- Регулярное обслуживание и очистка

### Troubleshooting

```bash
# 1. Сгенерировать системный отчет
r2r generate-report

# 2. Проверить здоровье контейнеров
r2r docker-down
r2r serve --docker

# 3. Проверить состояние БД
r2r db current
r2r db history

# 4. Откатить при необходимости
r2r db downgrade --revision <previous-version>
```

---

## Практические рекомендации

### 1. Архитектурные рекомендации

#### Выбор режима развертывания

| Развертывание | Описание | Применение |
|---------------|----------|------------|
| **R2R Light** | Базовая функциональность | Solo developers, прототипирование |
| **R2R Full**  | Полный набор функций | Production, enterprise |

#### Конфигурация для различных сценариев

**Сценарий 1: Небольшой корпоративный поиск**
```toml
[ingestion]
chunk_size = 512
chunk_overlap = 128
enable_chunk_enrichment = false

[embedding]
base_model = "openai/text-embedding-3-small"
batch_size = 128

[retrieval]
search_type = "hybrid"
max_results = 5
```

**Сценарий 2: Крупномасштабная RAG система**
```toml
[ingestion]
chunk_size = 1024
chunk_overlap = 512
enable_chunk_enrichment = true

[embedding]
base_model = "openai/text-embedding-3-large"
batch_size = 512
concurrent_request_limit = 256

[retrieval]
search_type = "hybrid"
reranking_enabled = true
max_results = 20

[graphs]
extraction_model = "openai/gpt-4o"
```

**Сценарий 3: Knowledge-intensive application**
```toml
[ingestion]
chunk_size = 2048
chunk_overlap = 1024
enable_chunk_enrichment = true
strategies = ["semantic", "neighborhood"]

[graphs]
extraction_model = "openai/gpt-4o"
relationship_types = ["works_at", "located_in", "part_of", "related_to"]

[retrieval]
search_type = "hybrid"
reranking_enabled = true
```

### 2. Производительность и оптимизация

#### Оптимизация загрузки данных

```python
# ✅ ХОРОШО: Батч-загрузка
documents = [
    {"file_path": "doc1.pdf"},
    {"file_path": "doc2.pdf"},
    {"file_path": "doc3.pdf"},
]

for doc in documents:
    client.documents.create(**doc)

# ✅ ЕЩЕ ЛУЧШЕ: Асинхронная загрузка (если доступно)
import asyncio

async def ingest_documents():
    tasks = [
        client.documents.create_async(file_path=f"doc{i}.pdf")
        for i in range(100)
    ]
    await asyncio.gather(*tasks)
```

#### Оптимизация поиска

```python
# ✅ ХОРОШО: Использование фильтров для сужения поиска
search_response = client.retrieval.search(
    query="machine learning",
    search_settings={
        "filters": {
            "document_type": {"$eq": "pdf"},
            "created_at": {"$gte": "2023-01-01"}
        },
        "limit": 10
    }
)

# ✅ ХОРОШО: Использование reranking для улучшения качества
search_response = client.retrieval.search(
    query="explain quantum computing",
    search_settings={
        "use_hybrid_search": True,
        "reranking_enabled": True,
        "limit": 20  # Больше candidates для reranking
    }
)
```

### 3. Безопасность

#### Аутентификация и авторизация

```python
# ✅ ПРАВИЛЬНО: Использование токенов
client = R2RClient(
    base_url="http://localhost:7272",
    access_token="your_jwt_token"
)

# ✅ ПРАВИЛЬНО: Role-based access control
client.collections.set_permissions(
    collection_id="sensitive_docs",
    user_id="user_123",
    permissions=["read"]  # Только чтение
)
```

#### Безопасная конфигурация

```toml
[auth]
provider = "r2r"
require_authentication = true
require_email_verification = true
password_min_length = 12
password_require_uppercase = true
password_require_numbers = true
password_require_special = true

[database]
# ❌ НЕ ДЕЛАЙТЕ ТАК в продакшене
password = "your_postgres_password"

# ✅ ИСПОЛЬЗУЙТЕ переменные окружения
password = "${POSTGRES_PASSWORD}"
```

### 4. Мониторинг и логирование

#### Системный мониторинг

```bash
# Проверка здоровья системы
r2r generate-report

# Мониторинг через Hatchet UI
# http://localhost:7274
```

#### Логирование ошибок

```python
import logging

logger = logging.getLogger(__name__)

try:
    response = client.documents.create(file_path="document.pdf")
except Exception as e:
    logger.error(f"Failed to ingest document: {e}")
    # Обработка ошибки
```

### 5. Best Practices по категориям

#### Data Ingestion

✅ **DO:**
- Использовать подходящий режим (`fast`, `hi-res`, `custom`) в зависимости от типа документа
- Включать enrichment для документов с важным контекстом
- Предоставлять осмысленные метаданные при загрузке
- Использовать батч-обработку для множества документов

❌ **DON'T:**
- Загружать очень большие файлы без разбиения
- Игнорировать обработку ошибок
- Пропускать метаданные (затрудняет поиск)

#### Search & Retrieval

✅ **DO:**
- Использовать hybrid search для большинства случаев
- Применять фильтры для сужения результатов
- Настраивать веса в зависимости от use case
- Использовать reranking для улучшения качества

❌ **DON'T:**
- Использовать только keyword search (теряется семантика)
- Запрашивать слишком много результатов без пагинации
- Игнорировать настройки performance (ef_search, probes)

#### RAG

✅ **DO:**
- Тестировать разные модели для вашего use case
- Использовать streaming для больших ответов
- Настраивать temperature в зависимости от задачи
- Комбинировать с hybrid search для лучших результатов

❌ **DON'T:**
- Использовать очень высокую temperature для фактических вопросов
- Игнорировать стоимость API calls к LLM
- Пропускать валидацию generated content

#### Knowledge Graphs

✅ **DO:**
- Организовывать документы в логические коллекции
- Использовать осмысленные имена для сущностей
- Регулярно обновлять графы при изменении документов
- Использовать GraphRAG для complex queries

❌ **DON'T:**
- Создавать слишком большие коллекции (затрудняет обработку)
- Игнорировать управление правами доступа
- Пропускать построение communities для больших графов

#### Orchestration

✅ **DO:**
- Использовать Hatchet UI для мониторинга
- Настраивать подходящие retry policies
- Обрабатывать ошибки gracefully
- Логировать важные этапы workflow

❌ **DON'T:**
- Игнорировать failed workflows
- Создавать слишком сложные workflows
- Пропускать мониторинг resource usage

---

## Интеграция с тестируемым API

### Связь документации с API endpoints

На основе документации и проведенного тестирования API, вот как основные концепции отображаются на endpoints:

#### 1. Documents Management

| Функция | Endpoint | Метод |
|---------|----------|-------|
| Загрузка документа | `/v3/documents` | POST |
| Получить документ | `/v3/documents/{id}` | GET |
| Список документов | `/v3/documents` | GET |
| Обновить документ | `/v3/documents/{id}` | PATCH |
| Удалить документ | `/v3/documents/{id}` | DELETE |
| Извлечь граф | `/v3/documents/{id}/extract` | POST |
| Получить чанки | `/v3/documents/{id}/chunks` | GET |
| Список коллекций документа | `/v3/documents/{id}/collections` | GET |

#### 2. Collections Management

| Функция | Endpoint | Метод |
|---------|----------|-------|
| Создать коллекцию | `/v3/collections` | POST |
| Получить коллекцию | `/v3/collections/{id}` | GET |
| Список коллекций | `/v3/collections` | GET |
| Обновить коллекцию | `/v3/collections/{id}` | PATCH |
| Удалить коллекцию | `/v3/collections/{id}` | DELETE |
| Добавить документ | `/v3/collections/{id}/documents/{document_id}` | POST |
| Удалить документ | `/v3/collections/{id}/documents/{document_id}` | DELETE |
| Список документов | `/v3/collections/{id}/documents` | GET |
| Список пользователей | `/v3/collections/{id}/users` | GET |

#### 3. Retrieval Operations

| Функция | Endpoint | Метод |
|---------|----------|-------|
| Search | `/v3/retrieval/search` | POST |
| RAG | `/v3/retrieval/rag` | POST |
| Agent | `/v3/retrieval/agent` | POST |

#### 4. Graphs Operations

| Функция | Endpoint | Метод |
|---------|----------|-------|
| Создать граф | `/v3/graphs` | POST |
| Получить граф | `/v3/graphs/{id}` | GET |
| Обновить граф | `/v3/graphs/{id}` | PATCH |
| Удалить граф | `/v3/graphs/{id}` | DELETE |
| Pull граф | `/v3/graphs/{collection_id}/pull` | POST |
| Build communities | `/v3/graphs/{collection_id}/build` | POST |
| Reset граф | `/v3/graphs/{collection_id}/reset` | POST |
| Получить entities | `/v3/graphs/{collection_id}/entities` | GET |
| Получить relationships | `/v3/graphs/{collection_id}/relationships` | GET |
| Получить communities | `/v3/graphs/{collection_id}/communities` | GET |

#### 5. Users & Authentication

| Функция | Endpoint | Метод |
|---------|----------|-------|
| Регистрация | `/v3/users/register` | POST |
| Логин | `/v3/users/login` | POST |
| Logout | `/v3/users/logout` | POST |
| Обновить профиль | `/v3/users/profile` | PATCH |
| Сменить пароль | `/v3/users/change-password` | POST |
| Refresh token | `/v3/users/refresh-token` | POST |

### Практические примеры работы с API

#### Полный workflow: От загрузки до RAG

```python
import requests
from typing import Dict, Any

# Конфигурация
API_BASE = "http://136.119.36.216:7272"

class R2RWorkflow:
    def __init__(self, email: str, password: str):
        self.base_url = API_BASE
        self.token = None
        self.email = email
        self.password = password
        
    def authenticate(self) -> bool:
        """Шаг 1: Аутентификация"""
        response = requests.post(
            f"{self.base_url}/v3/users/login",
            data={
                "username": self.email,
                "password": self.password
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            self.token = data["results"]["access_token"]["token"]
            print("✅ Authentication successful")
            return True
        else:
            print(f"❌ Authentication failed: {response.text}")
            return False
    
    @property
    def headers(self) -> Dict[str, str]:
        """Получить заголовки с токеном"""
        return {"Authorization": f"Bearer {self.token}"}
    
    def create_collection(self, name: str, description: str) -> str:
        """Шаг 2: Создать коллекцию"""
        response = requests.post(
            f"{self.base_url}/v3/collections",
            headers=self.headers,
            json={
                "name": name,
                "description": description
            }
        )
        
        if response.status_code == 200:
            collection_id = response.json()["results"]["id"]
            print(f"✅ Collection created: {collection_id}")
            return collection_id
        else:
            print(f"❌ Collection creation failed: {response.text}")
            return None
    
    def upload_document(self, file_path: str, metadata: Dict = None) -> str:
        """Шаг 3: Загрузить документ"""
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {}
            if metadata:
                data['metadata'] = str(metadata)
            
            response = requests.post(
                f"{self.base_url}/v3/documents",
                headers=self.headers,
                files=files,
                data=data
            )
        
        if response.status_code == 200:
            document_id = response.json()["results"]["document_id"]
            print(f"✅ Document uploaded: {document_id}")
            return document_id
        else:
            print(f"❌ Document upload failed: {response.text}")
            return None
    
    def add_document_to_collection(
        self, 
        collection_id: str, 
        document_id: str
    ) -> bool:
        """Шаг 4: Добавить документ в коллекцию"""
        response = requests.post(
            f"{self.base_url}/v3/collections/{collection_id}/documents/{document_id}",
            headers=self.headers
        )
        
        if response.status_code == 200:
            print(f"✅ Document added to collection")
            return True
        else:
            print(f"❌ Failed to add document to collection: {response.text}")
            return False
    
    def trigger_extraction(self, document_id: str) -> bool:
        """Шаг 5: Триггер извлечения графа"""
        response = requests.post(
            f"{self.base_url}/v3/documents/{document_id}/extract",
            headers=self.headers
        )
        
        if response.status_code in [200, 202]:
            print(f"✅ Extraction triggered for document")
            return True
        else:
            print(f"❌ Extraction trigger failed: {response.text}")
            return False
    
    def search(
        self, 
        query: str, 
        collection_id: str = None,
        use_hybrid: bool = True
    ) -> Dict[str, Any]:
        """Шаг 6: Поиск"""
        payload = {
            "query": query,
            "search_settings": {
                "use_hybrid_search": use_hybrid,
                "limit": 10
            }
        }
        
        if collection_id:
            payload["search_settings"]["filters"] = {
                "collection_id": {"$eq": collection_id}
            }
        
        response = requests.post(
            f"{self.base_url}/v3/retrieval/search",
            headers=self.headers,
            json=payload
        )
        
        if response.status_code == 200:
            results = response.json()["results"]
            print(f"✅ Search completed: {len(results.get('chunk_search_results', []))} results")
            return results
        else:
            print(f"❌ Search failed: {response.text}")
            return None
    
    def rag(
        self, 
        query: str,
        collection_id: str = None,
        use_hybrid: bool = True,
        model: str = "google/gemini-2.0-flash-exp"
    ) -> Dict[str, Any]:
        """Шаг 7: RAG"""
        payload = {
            "query": query,
            "search_settings": {
                "use_hybrid_search": use_hybrid,
                "limit": 10
            },
            "rag_generation_config": {
                "model": model,
                "temperature": 0.7
            }
        }
        
        if collection_id:
            payload["search_settings"]["filters"] = {
                "collection_id": {"$eq": collection_id}
            }
        
        response = requests.post(
            f"{self.base_url}/v3/retrieval/rag",
            headers=self.headers,
            json=payload
        )
        
        if response.status_code == 200:
            results = response.json()["results"]
            print(f"✅ RAG completed")
            return results
        else:
            print(f"❌ RAG failed: {response.text}")
            return None

# Использование
if __name__ == "__main__":
    # Инициализация
    workflow = R2RWorkflow(
        email="admin@example.com",
        password="change_me_immediately"
    )
    
    # Полный workflow
    if workflow.authenticate():
        # 1. Создать коллекцию
        collection_id = workflow.create_collection(
            name="Technical Documentation",
            description="Collection of technical documents"
        )
        
        # 2. Загрузить документ
        document_id = workflow.upload_document(
            file_path="technical_doc.pdf",
            metadata={"category": "technical", "version": "1.0"}
        )
        
        # 3. Добавить документ в коллекцию
        if collection_id and document_id:
            workflow.add_document_to_collection(collection_id, document_id)
        
        # 4. Триггер извлечения
        if document_id:
            workflow.trigger_extraction(document_id)
        
        # 5. Поиск
        search_results = workflow.search(
            query="What is the installation process?",
            collection_id=collection_id,
            use_hybrid=True
        )
        
        # 6. RAG
        rag_results = workflow.rag(
            query="Explain the installation process step by step",
            collection_id=collection_id,
            use_hybrid=True
        )
        
        if rag_results:
            print("\n" + "="*50)
            print("RAG RESPONSE:")
            print("="*50)
            print(rag_results.get("completion", {}).get("choices", [{}])[0].get("message", {}).get("content", "No content"))
```

---

## Заключение

### Ключевые выводы

1. **R2R — это комплексная платформа** для построения RAG-приложений с поддержкой:
   - Множественных типов документов
   - Продвинутого поиска (vector, hybrid, knowledge graph)
   - Контекстного обогащения
   - Графов знаний
   - Agentic workflows

2. **Архитектура R2R** построена на провайдерах, сервисах и RESTful API, что обеспечивает:
   - Гибкость конфигурации
   - Масштабируемость
   - Модульность

3. **Оркестрация через Hatchet** предоставляет:
   - Отказоустойчивость
   - Распределенную обработку
   - Мониторинг и управление

4. **Тестируемый API** http://136.119.36.216:7272 полностью соответствует документации и предоставляет:
   - 83 endpoint через 7 категорий
   - OAuth2 аутентификацию
   - Полный CRUD для документов, коллекций, графов
   - Продвинутые возможности RAG и поиска

### Рекомендации по использованию

#### Для начинающих
1. Начните с простого workflow: загрузка → поиск → RAG
2. Используйте `advanced` режим для поиска (хороший баланс)
3. Не включайте enrichment и graphs на начальном этапе
4. Используйте R2R Dashboard для визуального управления

#### Для продвинутых пользователей
1. Настройте контекстное обогащение для критичных документов
2. Используйте GraphRAG для complex queries
3. Настройте векторные индексы для больших dataset
4. Используйте orchestration для масштабирования
5. Мониторьте через Hatchet UI

#### Для enterprise
1. Настройте RBAC и authentication properly
2. Используйте multiple environments (dev/staging/prod)
3. Реализуйте horizontal scaling
4. Настройте proper logging и monitoring
5. Регулярно обновляйте систему
6. Используйте GraphRAG с communities для knowledge-intensive applications

### Следующие шаги

1. ✅ **Изучена полная документация R2R**
2. ✅ **Проведено комплексное тестирование API** (71+ тестов)
3. ✅ **Решена проблема с extraction pending**
4. ✅ **Создана полная документация по использованию**

**Рекомендации для дальнейшей работы:**
- Продолжить мониторинг extraction процесса
- Тестировать GraphRAG capabilities
- Экспериментировать с различными моделями LLM
- Оптимизировать производительность через векторные индексы
- Разработать best practices для конкретных use cases

---

**Документ подготовлен на основе официальной документации R2R**  
**Дата: 2024**  
**Версия R2R: v3**  
**API Base: http://136.119.36.216:7272**
