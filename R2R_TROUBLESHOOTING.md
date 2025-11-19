# R2R Connection Troubleshooting

## Current Issue: R2R API Not Accessible

**Symptoms**:
- ❌ `http://136.119.36.216:7272` returns 403 Forbidden
- ❌ `http://localhost:7272` connection refused
- ❌ Port 7272 not listening on local machine
- ❌ No R2R processes running

**Impact**: Cannot test integration until R2R service is accessible

---

## Diagnosis Steps

### 1. Check if R2R is Running

```bash
# Check if port 7272 is listening
netstat -tulpn | grep 7272
# or
ss -tulpn | grep 7272

# Check for R2R processes
ps aux | grep r2r

# Check docker containers
docker ps | grep r2r
```

### 2. Test R2R Endpoints

```bash
# Try health endpoint
curl http://localhost:7272/health
curl http://127.0.0.1:7272/health
curl http://136.119.36.216:7272/health

# Try login
curl -X POST http://localhost:7272/v2/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"change_me_immediately"}'
```

### 3. Check Network Connectivity

```bash
# Ping the remote server
ping 136.119.36.216

# Check if port is reachable
nc -zv 136.119.36.216 7272
# or
telnet 136.119.36.216 7272
```

---

## Possible Solutions

### Solution 1: Start R2R Locally

If R2R should run on this machine:

```bash
# Using Docker
docker run -d -p 7272:7272 \
  -e R2R_SECRET_KEY="3276b4262bcfa6a267a7989b4feb0b169b806afa8494aa7d4ab2e435272c433a" \
  r2r:latest

# Using Python
r2r serve --host 0.0.0.0 --port 7272

# Using docker-compose (if available)
docker-compose up -d r2r
```

### Solution 2: Configure Proxy/Firewall

The Envoy proxy is blocking requests:

**Check Envoy Configuration**:
```bash
# Find envoy config
find /etc -name "envoy.yaml" 2>/dev/null
cat /etc/envoy/envoy.yaml

# Check if there's an allow list
grep -r "136.119.36.216" /etc/envoy/
```

**Possible fixes**:
- Add route to R2R backend in Envoy config
- Add IP whitelist for R2R service
- Disable authentication for local development

### Solution 3: Use SSH Tunnel

If R2R is on a remote server:

```bash
# Create SSH tunnel
ssh -L 7272:localhost:7272 user@136.119.36.216

# Then use localhost
curl http://localhost:7272/health
```

### Solution 4: Update R2R URL in Code

If R2R is accessible at a different URL:

```bash
# Set environment variable
export R2R_BASE_URL="http://your-actual-r2r-url:7272"

# Or update in code
# r2r-mcp-server/src/server.ts line 4:
# const R2R_BASE_URL = process.env.R2R_BASE_URL || 'http://localhost:7272';
```

---

## Environment-Specific Issues

### Issue: 403 Forbidden from Envoy

**Cause**: Proxy authorization required or IP blocked

**Debug**:
```bash
# Check proxy settings
echo $HTTP_PROXY
echo $HTTPS_PROXY
echo $NO_PROXY

# View full request/response
curl -v http://136.119.36.216:7272/health
```

**Fix**:
- Configure Envoy to allow this IP
- Add proper proxy credentials
- Use direct connection bypassing proxy

### Issue: Connection Refused

**Cause**: R2R not running or wrong port

**Fix**:
```bash
# Check R2R logs
docker logs r2r
# or
journalctl -u r2r -n 50

# Verify R2R config
cat ~/.r2r/config.yaml
cat /etc/r2r/config.yaml
```

### Issue: Port Not Listening

**Cause**: R2R service not started

**Fix**:
```bash
# Start R2R service
systemctl start r2r
# or
docker start r2r
# or
r2r serve
```

---

## Quick Test After R2R Starts

Once R2R is accessible, run these quick tests:

```bash
# 1. Health check
curl http://localhost:7272/health

# 2. Login
curl -X POST http://localhost:7272/v2/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"change_me_immediately"}'

# 3. List documents (with token from step 2)
curl -X GET http://localhost:7272/v3/documents \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 4. Test MCP server
cd r2r-mcp-server
node dist/server.js
```

---

## Expected R2R Responses

### Healthy R2R Service:

```bash
$ curl http://localhost:7272/health
{"status":"ok"}

$ curl -X POST http://localhost:7272/v2/login -H "Content-Type: application/json" -d '{"email":"admin@example.com","password":"change_me_immediately"}'
{
  "results": {
    "access_token": {
      "token": "eyJhbGci...",
      "token_type": "access"
    }
  }
}

$ curl -X GET http://localhost:7272/v3/documents -H "Authorization: Bearer TOKEN"
{
  "results": [...]
}
```

### Current Broken State:

```bash
$ curl http://136.119.36.216:7272/health
Access denied

$ curl http://localhost:7272/health
curl: (7) Failed to connect to localhost port 7272: Connection refused
```

---

## Next Steps After R2R is Running

1. ✅ Verify health endpoint responds
2. ✅ Test login and get JWT token
3. ✅ Update MCP server test with real token
4. ✅ Test document ingestion
5. ✅ Test search functionality
6. ✅ Test RAG queries
7. ✅ Run full integration tests
8. ✅ Commit and push tested code

---

## Contact/Resources

**R2R Documentation**: https://r2r-docs.sciphi.ai/
**R2R GitHub**: https://github.com/SciPhi-AI/R2R

**Current Configuration**:
- Expected URL: `http://136.119.36.216:7272` or `http://localhost:7272`
- Auth Email: `admin@example.com`
- Auth Password: `change_me_immediately`
- Secret Key: `3276b4262bcfa6a267a7989b4feb0b169b806afa8494aa7d4ab2e435272c433a`
