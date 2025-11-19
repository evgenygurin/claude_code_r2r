#!/bin/bash
# PostToolUse Hook: Auto-index newly created/edited files in background
# Fire-and-forget: returns immediately, indexing happens asynchronously

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name')
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path')

# Only process Write/Edit tools
if [[ "$TOOL_NAME" != "Write" && "$TOOL_NAME" != "Edit" ]]; then
  exit 0
fi

# Only index documentation/code files (not binaries)
if [[ ! "$FILE_PATH" =~ \.(md|txt|py|ts|js|jsx|tsx|json|yaml|yml|toml|sh|bash)$ ]]; then
  exit 0
fi

# Check if file exists and is readable
if [ ! -f "$FILE_PATH" ] || [ ! -r "$FILE_PATH" ]; then
  exit 0
fi

# Get absolute path
ABSOLUTE_PATH=$(realpath "$FILE_PATH" 2>/dev/null || echo "$FILE_PATH")

# Load auth token from environment (if available)
AUTH_TOKEN="${R2R_AUTH_TOKEN}"

# Background ingestion (fire and forget - no blocking!)
(
  if [ -n "$AUTH_TOKEN" ]; then
    curl -s -X POST http://136.119.36.216:7272/v3/documents \
      -H "Authorization: Bearer $AUTH_TOKEN" \
      -F "file=@$ABSOLUTE_PATH" \
      -F "ingestion_mode=fast" \
      -F "metadata={\"source\":\"claude_code_auto\",\"file\":\"$FILE_PATH\",\"tool\":\"$TOOL_NAME\"}" \
      > /tmp/r2r_ingest_$$.log 2>&1 &
  else
    curl -s -X POST http://136.119.36.216:7272/v3/documents \
      -F "file=@$ABSOLUTE_PATH" \
      -F "ingestion_mode=fast" \
      -F "metadata={\"source\":\"claude_code_auto\",\"file\":\"$FILE_PATH\",\"tool\":\"$TOOL_NAME\"}" \
      > /tmp/r2r_ingest_$$.log 2>&1 &
  fi
) &

# Return immediately with success message
cat << EOF
{
  "suppressOutput": true,
  "systemMessage": "🔄 Background indexing started for: $(basename $FILE_PATH)"
}
EOF

exit 0
