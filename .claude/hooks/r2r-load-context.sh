#!/bin/bash
# SessionStart Hook: Load relevant R2R documents at session start
# This enriches the initial context with relevant indexed documents

INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id')
PROJECT_DIR=$(echo "$INPUT" | jq -r '.cwd')
PROJECT_NAME=$(basename "$PROJECT_DIR")

# Quick search for project-related docs
SEARCH_RESULTS=$(curl -s -X POST http://136.119.36.216:7272/v3/retrieval/search \
  -H "Content-Type: application/json" \
  -d "{
    \"query\": \"project overview $PROJECT_NAME documentation\",
    \"search_settings\": {
      \"search_mode\": \"advanced\",
      \"limit\": 5
    }
  }" 2>/dev/null)

# Check if we got results
if [ -n "$SEARCH_RESULTS" ] && [ "$SEARCH_RESULTS" != "null" ]; then
  # Format results for Claude
  FORMATTED_RESULTS=$(echo "$SEARCH_RESULTS" | jq -r '
    .results.chunk_search_results[]? |
    "📄 \(.metadata.title // "Unknown Document"):\n   \(.text | .[0:200])...\n   (Score: \(.score | tostring))\n"
  ' | head -10)

  if [ -n "$FORMATTED_RESULTS" ]; then
    # Return context as additional context for SessionStart
    cat << EOF
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "📚 **Relevant Documentation from R2R Knowledge Base:**\n\n$FORMATTED_RESULTS\n\n*Use r2r_search or r2r_rag tools for more detailed information.*"
  }
}
EOF
  fi
fi

exit 0
