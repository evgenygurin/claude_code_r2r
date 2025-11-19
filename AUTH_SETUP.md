# R2R Authentication Setup

## Quick Setup with Token

**IMPORTANT**: Don't save the token in files! Pass it directly when installing MCP server.

```bash
# Install MCP server with token directly
claude mcp add --transport stdio r2r \
  --env R2R_AUTH_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBleGFtcGxlLmNvbSIsInRva2VuX3R5cGUiOiJhY2Nlc3MiLCJleHAiOjE3NjcxMTkyMDguMDMyNjc1LCJpYXQiOjE3NjM1MTkyMDguMDMyNzM2LCJuYmYiOjE3NjM1MTkyMDguMDMyNzM2LCJqdGkiOiJhS3lDem9yQnItNkJNeGZzX3pIOHZnPT0iLCJub25jZSI6IlZVdHllcm1FejJodlNWNXhYN094Vmc9PSJ9.nU-WE9XpsalnvmDhk2tIISqRffu-3BLF2D7F5N05OuQ" \
  -- node /path/to/r2r-mcp-server/dist/server.js
```

The token is stored securely by Claude Code and passed to the MCP server.

## Alternative: Login via API

```bash
# Start Claude Code
claude

# In Claude:
> Use r2r_login with email "admin@example.com" and password "change_me_immediately"

# Claude will receive:
# {
#   "status": "success",
#   "message": "Logged in successfully",
#   "token": "eyJhbGci...",
#   "expires_at": "2025-12-30T..."
# }
```

## For Hooks (Optional)

If you want hooks to use authentication, set environment variable in your shell:

```bash
# In your ~/.bashrc or ~/.zshrc (temporary - don't commit!)
export R2R_AUTH_TOKEN="your_token_here"

# Or set it in current session only
R2R_AUTH_TOKEN="token_here" claude
```

## Testing Authentication

```bash
# Test with curl
curl -X GET http://136.119.36.216:7272/v3/documents \
  -H "Authorization: Bearer eyJhbGci..."

# Should return document list if authenticated

# Test via Claude Code
claude
> Use r2r_list_documents to check if authentication works
```

## Token Expiration

Your token expires at: **2025-12-30** (based on `exp: 1767119208`)

When it expires:
1. Use `r2r_login` tool in Claude Code
2. Or generate new token via R2R API
3. Update `R2R_AUTH_TOKEN` environment variable

## Security Best Practices

1. **NEVER commit tokens to git** - Always pass via command line or environment
2. **Use MCP server env vars** - Let Claude Code manage the token securely
3. **Rotate tokens regularly** - Especially when sharing with team
4. **Don't save in .env files** - Use shell environment or MCP config only

## Troubleshooting

**"Unauthorized" errors**:
```bash
# Check token is set
echo $R2R_AUTH_TOKEN

# Try logging in again
claude
> Use r2r_login to get fresh token
```

**Token not working in hooks**:
```bash
# Set token in current shell session
export R2R_AUTH_TOKEN="your_token"

# Verify
echo $R2R_AUTH_TOKEN

# Start Claude Code in same session
claude
```

**"Token expired" errors**:
```bash
# Login again to get new token
claude
> r2r_login with admin@example.com / change_me_immediately
```

## Integration Status

✅ MCP Server - Supports Bearer token
✅ Hooks - Load token from environment
✅ Auto-login - `r2r_login` tool available
✅ Environment - `.env` file support

All components now support authentication!
