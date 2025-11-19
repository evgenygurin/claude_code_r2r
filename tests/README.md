# R2R API Tests

Automated tests for R2R API authentication and retrieval endpoints.

## Structure

- `test_api_login.py` - Main test client for API testing

## Running Tests

### 1. Install dependencies

```bash
pip install -r requirements-test.txt
```

### 2. Start SSH tunnel (if not already running)

```bash
# In another terminal:
gcloud compute ssh r2r-production --zone=us-central1-a -- -L 7272:localhost:7272

# Or use the tunnel manager script:
./scripts/r2r-tunnel.sh start
```

### 3. Run tests

```bash
# Auto-detect best available connection
python3 test_api_login.py

# Or explicitly use tunnel
python3 test_api_login.py --url=http://localhost:7272

# Or use remote (if direct access available)
python3 test_api_login.py --use-remote
```

## Test Cases

1. **Health Check** - Verify API is responding
2. **User Login** - Test authentication with default credentials
3. **Get User Info** - Retrieve authenticated user information
4. **List Collections** - List all document collections
5. **Search Documents** - Test document search functionality

## Expected Output

```
R2R API Testing Tool
============================================================
Testing against: http://localhost:7272

Running R2R API tests against http://localhost:7272...

Running: Health Check... ✅
Running: Login... ✅
Running: Get User Info... ✅
Running: List Collections... ✅
Running: Search... ✅

============================================================
TEST RESULTS
============================================================
✅ PASS | Health Check                   | 0.15s
✅ PASS | User Login                     | 0.42s
✅ PASS | Get User Info                  | 0.08s
✅ PASS | List Collections               | 0.12s
✅ PASS | Search Documents               | 0.25s
============================================================
Summary: 5/5 tests passed
============================================================
```

## Troubleshooting

### Connection Refused (localhost:7272)
- SSH tunnel is not running
- Start the tunnel: `./scripts/r2r-tunnel.sh start`

### Connection Timeout (remote IP)
- Remote API not accessible from current network
- Use SSH tunnel instead: `gcloud compute ssh r2r-production ...`

### Authentication Failed
- Check credentials in test_api_login.py
- Default: admin@example.com / change_me_immediately

### No Collections Found
- Database may be empty
- Upload some documents first via the R2R UI or API

## API Credentials

Default test credentials:
- **Username:** admin@example.com
- **Password:** change_me_immediately

⚠️ **Note:** Change these in production!

## CI/CD Integration

Example GitHub Actions workflow:

```yaml
- name: Start R2R tunnel
  run: |
    gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
    gcloud compute ssh r2r-production --zone=us-central1-a -- -L 7272:localhost:7272 &
    sleep 3

- name: Install test dependencies
  run: pip install -r requirements-test.txt

- name: Run API tests
  run: python3 tests/test_api_login.py
```

## Development

To add new tests:

1. Add new test method to `R2RAPITester` class
2. Call test in `run_all_tests()` method
3. Update test results to include timing

Example:

```python
def test_custom_endpoint(self) -> bool:
    """Test custom endpoint"""
    if not self.access_token:
        self.add_result(TestResult(
            name="Custom Test",
            passed=False,
            message="No access token",
            duration=0
        ))
        return False

    start = time.time()
    try:
        # Your test code here
        duration = time.time() - start
        self.add_result(TestResult(...))
        return success
    except Exception as e:
        duration = time.time() - start
        self.add_result(TestResult(...))
        return False
```

## References

- R2R API Docs: http://localhost:7272/docs
- OpenAPI Schema: http://localhost:7272/openapi.json
- Testing Guide: ../API_TESTING.md
