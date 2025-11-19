# R2R API Login Testing - Complete Guide

This guide covers testing the R2R API login endpoint and related functionality.

## Quick Start

### Option 1: Using Bash Script (Recommended - No Python Required)

```bash
# Start your SSH tunnel first (in another terminal):
gcloud compute ssh r2r-production --zone=us-central1-a -- -L 7272:localhost:7272

# Then run the test script:
./scripts/test-api.sh

# Or specify a custom URL:
./scripts/test-api.sh http://your-api-host:7272
```

### Option 2: Using Python Test Client

```bash
# Install dependencies
pip install -r requirements-test.txt

# Run tests
python3 tests/test_api_login.py

# Or with custom URL
python3 tests/test_api_login.py --url=http://your-api-host:7272
```

### Option 3: Using Tunnel Manager Script

```bash
# Start tunnel and test
./scripts/r2r-tunnel.sh start
./scripts/r2r-tunnel.sh test

# Stop tunnel
./scripts/r2r-tunnel.sh stop
```

## Setup

### Prerequisites

- `curl` (for API requests)
- `jq` (for JSON parsing)
- `lsof` (for checking ports)
- Google Cloud SDK (`gcloud`) - for opening SSH tunnels

### Install on macOS

```bash
brew install curl jq lsof
brew install --cask google-cloud-sdk
```

### Install on Linux (Ubuntu/Debian)

```bash
sudo apt-get install curl jq lsof
# For gcloud, see: https://cloud.google.com/sdk/docs/install
```

## SSH Tunnel Setup

### Method 1: Direct gcloud SSH Tunnel

Open tunnel in one terminal and keep it open:

```bash
gcloud compute ssh r2r-production --zone=us-central1-a -- -L 7272:localhost:7272
```

This command:
- Connects to the r2r-production instance
- Forwards local port 7272 to remote localhost:7272
- Keeps the tunnel open (blocking)

Leave this terminal open while running tests.

### Method 2: Background SSH Tunnel

Run tunnel in background:

```bash
gcloud compute ssh r2r-production --zone=us-central1-a -- -L 7272:localhost:7272 -N -f
```

Check if running:

```bash
lsof -i :7272
```

Kill tunnel later:

```bash
kill $(lsof -ti :7272)
```

### Method 3: Using Tunnel Manager Script

```bash
./scripts/r2r-tunnel.sh start    # Start tunnel
./scripts/r2r-tunnel.sh status   # Check status
./scripts/r2r-tunnel.sh stop     # Stop tunnel
./scripts/r2r-tunnel.sh test     # Run full test suite
```

## API Login Credentials

Default test credentials:
- **Username:** admin@example.com
- **Password:** change_me_immediately

⚠️ Change these credentials in production!

## Manual Testing with cURL

### 1. Health Check

```bash
curl -s http://localhost:7272/v3/health | jq .
```

**Expected response:**
```json
{
  "results": {
    "status": "ok"
  }
}
```

### 2. Login Request

```bash
curl -X POST http://localhost:7272/v3/users/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@example.com&password=change_me_immediately" | jq .
```

**Expected response:**
```json
{
  "results": {
    "access_token": {
      "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "token_type": "access"
    },
    "refresh_token": {
      "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "token_type": "refresh"
    }
  }
}
```

### 3. Using Access Token

Save the token for later use:

```bash
TOKEN=$(curl -s -X POST http://localhost:7272/v3/users/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@example.com&password=change_me_immediately" \
  | jq -r '.results.access_token.token')

echo "Token: $TOKEN"
```

### 4. Get Current User

```bash
curl -s http://localhost:7272/v3/users/me \
  -H "Authorization: Bearer $TOKEN" | jq .
```

### 5. List Collections

```bash
curl -s http://localhost:7272/v3/collections \
  -H "Authorization: Bearer $TOKEN" | jq '.results[] | {name, document_count}'
```

### 6. Search Documents

```bash
curl -s -X POST http://localhost:7272/v3/retrieval/search \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"your search query","limit":5}' | jq '.results.chunk_search_results'
```

## Test Scripts

### Bash Test Script

Located at: `scripts/test-api.sh`

Features:
- No Python required
- Color-coded output
- Tests all main endpoints
- Easy to understand

```bash
./scripts/test-api.sh                              # Uses localhost:7272
./scripts/test-api.sh http://custom-host:7272     # Custom host
```

### Python Test Client

Located at: `tests/test_api_login.py`

Features:
- Comprehensive error reporting
- Timing information
- Auto-detection of tunnel vs remote
- Detailed test results

```bash
python3 tests/test_api_login.py                   # Auto-detect
python3 tests/test_api_login.py --use-remote      # Force remote
python3 tests/test_api_login.py --url=http://...  # Custom URL
```

### Tunnel Manager

Located at: `scripts/r2r-tunnel.sh`

Features:
- Start/stop SSH tunnel
- Check tunnel status
- Run full test suite
- Display API health

```bash
./scripts/r2r-tunnel.sh start           # Start tunnel
./scripts/r2r-tunnel.sh status          # Check status
./scripts/r2r-tunnel.sh test            # Run tests
./scripts/r2r-tunnel.sh restart         # Restart tunnel
./scripts/r2r-tunnel.sh stop            # Stop tunnel
```

## Troubleshooting

### "Connection refused" on localhost:7272

**Problem:** SSH tunnel is not running or not properly established

**Solution:**
```bash
# Check if tunnel is running
lsof -i :7272

# If not, start it
gcloud compute ssh r2r-production --zone=us-central1-a -- -L 7272:localhost:7272 &

# Or use the tunnel manager
./scripts/r2r-tunnel.sh start
```

### "Connection timeout" on remote IP

**Problem:** Network doesn't allow direct access to remote IP

**Solution:** Use SSH tunnel instead (see above)

### "Authentication failed"

**Problem:** Wrong credentials or server has different defaults

**Solution:**
1. Check credentials in the scripts
2. Verify with administrator
3. Update credentials if needed

### "jq: command not found"

**Problem:** jq is not installed

**Solution:**
```bash
# macOS
brew install jq

# Ubuntu/Debian
sudo apt-get install jq

# Or download from: https://stedolan.github.io/jq/
```

### "No collections found"

**Problem:** Database is empty

**Solution:** Upload documents via R2R UI or API first

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Test R2R API

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Authenticate with Google Cloud
        uses: google-github-actions/auth@v1
        with:
          credentials_json: ${{ secrets.GCP_SA_KEY }}

      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v1

      - name: Start SSH tunnel
        run: |
          gcloud compute ssh r2r-production \
            --zone=us-central1-a \
            -- -L 7272:localhost:7272 -N -f
          sleep 3

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          pip install -r requirements-test.txt

      - name: Run tests
        run: python3 tests/test_api_login.py

      - name: Stop tunnel
        if: always()
        run: kill $(lsof -ti :7272) || true
```

### Local Development

```bash
# In terminal 1: Start tunnel
gcloud compute ssh r2r-production --zone=us-central1-a -- -L 7272:localhost:7272

# In terminal 2: Run tests
./scripts/test-api.sh

# Or watch tests for changes
while inotifywait -e modify tests/; do
    python3 tests/test_api_login.py
done
```

## API Documentation

### Available Endpoints

- `GET /v3/health` - Health check
- `POST /v3/users/login` - User login
- `GET /v3/users/me` - Get current user
- `GET /v3/collections` - List collections
- `POST /v3/retrieval/search` - Search documents

### Interactive Documentation

Once tunnel is open, visit:
- **Swagger UI:** http://localhost:7272/docs
- **ReDoc:** http://localhost:7272/redoc
- **OpenAPI Schema:** http://localhost:7272/openapi.json

### Authentication

All authenticated endpoints require the `Authorization` header:

```
Authorization: Bearer {ACCESS_TOKEN}
```

## Testing Strategy

### Unit Tests
- Test individual API endpoints
- Verify response formats
- Check error handling

### Integration Tests
- Test end-to-end workflows
- Verify data consistency
- Test multiple requests in sequence

### Performance Tests
- Measure response times
- Test under load
- Monitor resource usage

## Resources

- R2R Documentation: https://r2r.docs
- Google Cloud SSH: https://cloud.google.com/compute/docs/instances/connecting-advanced#gcloud-ssh
- curl Manual: https://curl.se/docs/manual.html
- jq Manual: https://stedolan.github.io/jq/manual/

## Support

For issues:
1. Check the troubleshooting section above
2. Review R2R API documentation
3. Check Google Cloud documentation
4. Open an issue on GitHub

## Files Overview

```
.
├── API_LOGIN_TESTING_GUIDE.md      # This file
├── API_TESTING.md                  # Detailed testing guide
├── requirements-test.txt           # Python test dependencies
├── scripts/
│   ├── r2r-tunnel.sh              # SSH tunnel manager
│   └── test-api.sh                # Quick bash test script
└── tests/
    ├── README.md                   # Test directory guide
    └── test_api_login.py           # Python test client
```

---

Last updated: 2024-11-19
