---
name: r2r-document-manager
description: Manage R2R document lifecycle - ingest, list, check status, delete. Use when user wants to add documents to knowledge base, check indexing status, list indexed documents, or remove documents. Handles async ingestion operations.
allowed-tools: mcp__r2r__ingest, mcp__r2r__list_documents, mcp__r2r__delete_document
---

# R2R Document Manager Skill

## When to Use This Skill

Activate when:
- User wants to add documents to R2R knowledge base
- Checking ingestion status of documents
- Listing all indexed documents
- Removing documents from index
- Managing document lifecycle
- User mentions: "index", "ingest", "add to R2R", "list docs", "delete document"

## Core Capabilities

1. **Document Ingestion** (async) - Add files to knowledge base
2. **Status Checking** - Monitor ingestion progress
3. **Document Listing** - View all indexed content
4. **Document Deletion** - Remove from knowledge base

## Ingestion Modes

| Mode | Speed | Quality | Use Case |
|------|-------|---------|----------|
| `fast` | ⚡ Fastest | Good | Quick indexing, large volumes |
| `hi-res` | 🐌 Slower | Best | PDFs, complex docs, images |
| `custom` | 🔧 Variable | Configurable | Full control over parsing |

## How to Use

### 1. Ingest Documents (Async)

**Simple Ingestion:**
```json
{
  "file_path": "/absolute/path/to/document.pdf",
  "mode": "fast"
}
```

**With Metadata:**
```json
{
  "file_path": "/path/to/api_docs.md",
  "mode": "hi-res",
  "metadata": {
    "category": "api",
    "version": "v2.0",
    "author": "Engineering Team"
  }
}
```

**Important**: Ingestion is ASYNC
- Returns immediately with `document_id`
- Actual processing happens in background
- Use `r2r_list_documents` to check status

### 2. Check Document Status

```json
{
  "limit": 100,
  "offset": 0
}
```

**Status Values:**
- `pending` - Queued for processing
- `processing` - Currently being indexed
- `success` - ✅ Ready for search/RAG
- `failed` - ❌ Error occurred

### 3. Delete Documents

```json
{
  "document_id": "9fbe403b-c11c-5aae-8ade-ef22980c3ad1"
}
```

**Cascading Deletion:**
- Removes document metadata
- Deletes all chunks
- Removes vector embeddings
- Cleans up knowledge graph entries

## Workflows

### Bulk Ingestion
```
User: "Index all documentation in the docs/ folder"

Workflow:
1. Use Glob to find files: docs/**/*.md
2. For each file:
   - mcp__r2r__ingest({file_path, mode: "fast"})
   - Collect document_ids
3. Wait 10-30 seconds (async processing)
4. mcp__r2r__list_documents to verify status
5. Report: X/Y documents successfully indexed
```

### Selective Ingestion
```
User: "Add the new API documentation with high quality indexing"

Workflow:
1. Identify specific files
2. mcp__r2r__ingest({
     file_path: "api_v2_docs.pdf",
     mode: "hi-res",
     metadata: {
       "type": "api_documentation",
       "version": "2.0"
     }
   })
3. Return document_id for user reference
4. Inform user about async processing
```

### Document Cleanup
```
User: "Remove outdated v1 API documentation"

Workflow:
1. mcp__r2r__list_documents({limit: 200})
2. Filter by metadata: version: "1.0"
3. For each doc:
   - mcp__r2r__delete_document({document_id})
4. Confirm deletion count
```

### Status Monitoring
```
User: "Check if my documents finished indexing"

Workflow:
1. mcp__r2r__list_documents()
2. Filter by status != "success"
3. Report:
   - Pending: X
   - Processing: Y
   - Failed: Z (with details)
   - Success: N
```

## Best Practices

### 1. Choose Right Ingestion Mode

**Fast Mode** - Use for:
- Plain text files (.txt, .md)
- Simple documents
- Large volumes (100+ files)
- Quick prototyping

**Hi-Res Mode** - Use for:
- PDFs with complex layouts
- Documents with images/tables
- Scanned documents (OCR)
- When quality > speed

**Custom Mode** - Use for:
- Special chunking requirements
- Custom parsers
- Fine-tuned control
- Integration with existing pipeline

### 2. Handle Async Operations

```typescript
// Wrong: Immediate search after ingest
ingest(file)
search(query) // ❌ Document not ready yet!

// Right: Check status first
ingest(file) → document_id
wait(5-10 seconds)
list_documents() → check status
if (status === "success") {
  search(query) // ✅ Ready!
}
```

### 3. Use Metadata Effectively

**Good Metadata:**
```json
{
  "category": "api_docs",
  "version": "2.1.0",
  "author": "platform_team",
  "tags": ["authentication", "REST"],
  "last_updated": "2025-01-19"
}
```

**Use metadata for:**
- Filtering searches
- Document organization
- Version control
- Source tracking

### 4. Monitor Failed Ingestions

```
1. list_documents()
2. Filter: status === "failed"
3. Check error messages
4. Common fixes:
   - File not found → verify path
   - Unsupported format → convert file
   - Too large → split file
   - Corrupted → re-export file
```

## Supported File Types

| Category | Extensions | Recommended Mode |
|----------|-----------|------------------|
| Text | .txt, .md, .rst | fast |
| Code | .py, .js, .ts, .java | fast |
| Documents | .pdf, .docx | hi-res |
| Data | .json, .yaml, .csv | fast |
| Presentations | .pptx | hi-res |

## Limitations

1. **File Size**: Very large files (>100MB) may timeout
   - Solution: Split into smaller chunks
2. **Processing Time**: Hi-res mode can take minutes
   - Solution: Use fast mode for quick testing
3. **Concurrent Ingestions**: System has queue limits
   - Solution: Batch ingestions with delays
4. **Binary Files**: Images/videos not directly supported
   - Solution: Extract text first, then ingest

## Output Formatting

### Ingestion Response
```markdown
## Document Ingested ✅

**Document ID**: `9fbe403b-c11c-5aae-8ade-ef22980c3ad1`
**File**: `api_documentation.pdf`
**Mode**: `hi-res`
**Status**: Processing in background

Use `r2r_list_documents` to check ingestion status.
Indexing typically completes in 10-30 seconds for fast mode,
2-5 minutes for hi-res mode.
```

### List Documents Response
```markdown
## Indexed Documents (50 total)

### Ready (✅ 45)
- **API Reference v2.0** (`pdf`) - *Last updated: 2025-01-15*
- **User Guide** (`md`) - *Last updated: 2025-01-10*
...

### Processing (⏳ 3)
- **Technical Spec** (`pdf`) - *Started: 2 min ago*
...

### Failed (❌ 2)
- **Old Doc** (`docx`) - *Error: Unsupported format*
...
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| "File not found" | Wrong path | Use absolute paths |
| "Processing forever" | Large file | Check R2R logs |
| "Failed" status | Format issue | Try different mode |
| "Duplicate" error | File already indexed | Delete first, then re-ingest |

## Integration Patterns

### With SessionStart Hook
```bash
# Auto-load recent docs at startup
.claude/hooks/session-start.sh:
  list_documents()
  show recent (last 7 days)
```

### With PostToolUse Hook
```bash
# Auto-index on Write
.claude/hooks/post-write.sh:
  if file.ext in [.md, .txt, .py]:
    r2r_ingest(file, mode="fast")
```

### With RAG Skill
```
1. User asks question
2. Document Manager: Check if relevant docs indexed
3. RAG Skill: Query indexed docs
4. If gaps found: Suggest ingesting missing docs
```

## See Also

- `r2r-rag` skill for querying indexed documents
- `r2r-knowledge-graph` skill for entity exploration
- PostToolUse hooks for auto-indexing
