#!/bin/bash
# UserPromptSubmit Hook: Enrich user prompts with relevant context from R2R
# Adds semantic search results to user queries when relevant

INPUT=$(cat)
USER_PROMPT=$(echo "$INPUT" | jq -r '.prompt')

# Skip if prompt is too short or looks like a command
if [ ${#USER_PROMPT} -lt 10 ] || [[ "$USER_PROMPT" =~ ^/ ]]; then
  exit 0
fi

# Load auth token from environment (if available)
AUTH_TOKEN="${R2R_AUTH_TOKEN}"

# Quick semantic search for relevant docs (with timeout)
if [ -n "$AUTH_TOKEN" ]; then
  RESULTS=$(timeout 2s curl -s -X POST http://136.119.36.216:7272/v3/retrieval/search \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $AUTH_TOKEN" \
    -d "{
      \"query\": \"$USER_PROMPT\",
      \"search_settings\": {
        \"search_mode\": \"advanced\",
        \"limit\": 3
      }
    }" 2>/dev/null)
else
  RESULTS=$(timeout 2s curl -s -X POST http://136.119.36.216:7272/v3/retrieval/search \
    -H "Content-Type: application/json" \
    -d "{
      \"query\": \"$USER_PROMPT\",
      \"search_settings\": {
        \"search_mode\": \"advanced\",
        \"limit\": 3
      }
    }" 2>/dev/null)
fi

# Check if we got meaningful results
if [ -n "$RESULTS" ] && [ "$RESULTS" != "null" ]; then
  # Extract relevant snippets with high scores (> 0.5)
  CONTEXT=$(echo "$RESULTS" | jq -r '
    .results.chunk_search_results[]? |
    select(.score > 0.5) |
    "- **\(.metadata.title // "Document")** (relevance: \(.score | tostring | .[0:4])):\n  \(.text | .[0:150])...\n"
  ' | head -5)

  # Only add context if we found relevant matches
  if [ -n "$CONTEXT" ]; then
    cat << EOF
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "\n---\n📚 **Relevant Context from R2R Knowledge Base:**\n\n$CONTEXT\n*For more details, use r2r_search or r2r_rag tools.*\n---\n"
  }
}
EOF
  fi
fi

exit 0
