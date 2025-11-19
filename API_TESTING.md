# R2R API Testing Guide

## Prerequisites

### 1. SSH Tunnel Setup

Откройте SSH туннель в отдельном терминале:

```bash
gcloud compute ssh r2r-production --zone=us-central1-a -- -L 7272:localhost:7272
```

Или используйте управляющий скрипт:

```bash
./scripts/r2r-tunnel.sh start
```

### 2. Environment

```bash
# Убедитесь что доступны:
- curl
- jq (для парсинга JSON)
- lsof (для проверки портов)
```

## API Testing

### Health Check

```bash
curl -s http://localhost:7272/v3/health | jq .
```

### User Login

```bash
# 1. Получить access token
TOKEN=$(curl -s -X POST http://localhost:7272/v3/users/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@example.com&password=change_me_immediately" \
  | jq -r '.results.access_token.token')

echo "Access Token: $TOKEN"
```

### Authenticated Requests

После получения токена, используйте его для запросов:

```bash
# Get current user info
curl -s http://localhost:7272/v3/users/me \
  -H "Authorization: Bearer $TOKEN" | jq .

# List collections
curl -s http://localhost:7272/v3/collections \
  -H "Authorization: Bearer $TOKEN" | jq '.results[] | {name, document_count}'

# Search documents
curl -s -X POST http://localhost:7272/v3/retrieval/search \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"your search query","limit":5}' | jq '.results.chunk_search_results'
```

## Using the Tunnel Manager Script

```bash
# Start tunnel
./scripts/r2r-tunnel.sh start

# Check status
./scripts/r2r-tunnel.sh status

# Run full test suite
./scripts/r2r-tunnel.sh test

# Stop tunnel
./scripts/r2r-tunnel.sh stop

# Restart tunnel
./scripts/r2r-tunnel.sh restart
```

## API Endpoints

### Authentication
- `POST /v3/users/login` - Login with credentials
- `POST /v3/users/refresh` - Refresh access token

### User Management
- `GET /v3/users/me` - Get current user info
- `GET /v3/users/{user_id}` - Get user by ID
- `PUT /v3/users/{user_id}` - Update user

### Collections
- `GET /v3/collections` - List all collections
- `POST /v3/collections` - Create collection
- `GET /v3/collections/{collection_id}` - Get collection details

### Documents
- `GET /v3/documents` - List documents
- `POST /v3/documents` - Upload document
- `DELETE /v3/documents/{document_id}` - Delete document

### Search & Retrieval
- `POST /v3/retrieval/search` - Search in documents
- `POST /v3/retrieval/rag` - RAG (Retrieval-Augmented Generation)

## Common Issues

### SSH Tunnel Not Connecting
```bash
# Check if tunnel is running
lsof -i :7272

# If stuck, restart
./scripts/r2r-tunnel.sh restart
```

### Token Expiration
If you get 401 Unauthorized, get a new token:
```bash
TOKEN=$(curl -s -X POST http://localhost:7272/v3/users/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@example.com&password=change_me_immediately" \
  | jq -r '.results.access_token.token')
```

### CORS or Content-Type Errors
Always include proper headers:
```bash
curl -X POST http://localhost:7272/v3/users/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "..."
```

## Testing with cURL

### Login Test Script

```bash
#!/bin/bash

API_URL="http://localhost:7272"
USERNAME="admin@example.com"
PASSWORD="change_me_immediately"

echo "Testing R2R API..."
echo "==================="
echo ""

# Health check
echo "1. Health Check..."
curl -s $API_URL/v3/health | jq .
echo ""

# Login
echo "2. Login..."
LOGIN_RESPONSE=$(curl -s -X POST $API_URL/v3/users/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=$USERNAME&password=$PASSWORD")

ACCESS_TOKEN=$(echo "$LOGIN_RESPONSE" | jq -r '.results.access_token.token')

if [ "$ACCESS_TOKEN" != "null" ] && [ -n "$ACCESS_TOKEN" ]; then
  echo "✅ Login successful"
  echo ""

  # Get user info
  echo "3. User Info..."
  curl -s $API_URL/v3/users/me \
    -H "Authorization: Bearer $ACCESS_TOKEN" | jq .
else
  echo "❌ Login failed"
  echo "$LOGIN_RESPONSE" | jq .
fi
```

## Testing with Python

See the accompanying Python test client for more advanced testing scenarios.

## CI/CD Integration

The `r2r-tunnel.sh` script can be used in CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Start R2R tunnel
  run: |
    ./scripts/r2r-tunnel.sh start

- name: Run API tests
  run: |
    python tests/api_tests.py

- name: Stop R2R tunnel
  run: ./scripts/r2r-tunnel.sh stop
  if: always()
```

## References

- R2R API Documentation: http://localhost:7272/docs
- OpenAPI Schema: http://localhost:7272/openapi.json
