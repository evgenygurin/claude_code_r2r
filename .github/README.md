# GitHub Workflows and Codegen Integration

This directory contains GitHub Actions workflows and Codegen configuration for the R2R + Claude Code integration project.

## 📁 Directory Structure

```
.github/
├── workflows/                  # GitHub Actions workflows
│   ├── ci.yml                 # Main CI/CD pipeline
│   ├── codegen-pr-review.yml  # Automatic PR reviews by Codegen
│   ├── codegen-checks-autofixer.yml  # Auto-fix failing CI checks
│   ├── codegen-agent-trigger.yml     # Trigger agents via comments/labels
│   └── codegen-circleci-integration.yml  # CircleCI monitoring
├── ISSUE_TEMPLATE/            # Issue templates
│   ├── codegen-feature-request.yml  # Feature requests for Codegen
│   └── codegen-bug-fix.yml          # Bug reports for Codegen
├── PULL_REQUEST_TEMPLATE.md   # PR template with Codegen commands
├── CODEOWNERS                 # Code ownership and auto-reviewers
├── codegen-config.json        # Codegen repository configuration
└── markdown-link-check.json   # Markdown link validation config
```

## 🤖 Codegen Workflows

### 1. PR Review (`codegen-pr-review.yml`)

**Trigger:** On pull request opened/updated  
**Purpose:** Automatic code review by Codegen AI agent

**Features:**
- AI-powered code analysis
- Security vulnerability detection
- Performance optimization suggestions
- Code quality recommendations

**Usage:**
```yaml
# Automatically runs on all PRs
# Results appear as PR comments and reviews
```

### 2. Checks Auto-fixer (`codegen-checks-autofixer.yml`)

**Trigger:** When CI checks fail  
**Purpose:** Automatically fix failing tests and linting errors

**Features:**
- Detects Codegen-created PRs
- Analyzes failure logs
- Pushes fix commits automatically
- Retries up to 3 times

**Usage:**
```yaml
# Automatic - no configuration needed
# Only runs on Codegen PRs
# Configure retry limit in codegen-config.json
```

### 3. Agent Trigger (`codegen-agent-trigger.yml`)

**Trigger:** GitHub comments with `@codegen` or `codegen` label  
**Purpose:** Manually trigger Codegen agents from issues/PRs

**Usage:**

**Via Comment:**
```
@codegen implement authentication middleware with JWT
```

**Via Label:**
1. Add `codegen` label to issue/PR
2. Agent automatically starts working

**Environment Variables Required:**
- `CODEGEN_API_KEY` - Your Codegen API key
- `CODEGEN_ORG_ID` - Your organization ID

### 4. CircleCI Integration (`codegen-circleci-integration.yml`)

**Trigger:** CircleCI webhook or manual dispatch  
**Purpose:** Monitor CircleCI builds and auto-fix failures

**Features:**
- Fetches CircleCI logs
- Analyzes build failures
- Triggers Codegen agent to fix issues
- Posts status updates to PRs

**Setup:**
1. Add `CIRCLECI_TOKEN` secret to repository
2. Configure webhook in CircleCI:
   ```bash
   curl -X POST \
     "https://api.github.com/repos/evgenygurin/claude_code_r2r/dispatches" \
     -H "Authorization: token $GITHUB_TOKEN" \
     -d '{"event_type": "circleci-failure", "client_payload": {...}}'
   ```

## 🚀 CI/CD Pipeline (`ci.yml`)

### Test Matrix

Tests run on Python 3.10, 3.11, and 3.12:

**Stages:**
1. **Linting** - `ruff check .`
2. **Type Checking** - `mypy .`
3. **Unit Tests** - `pytest tests/`
4. **Coverage** - Minimum 80% required
5. **Integration Tests** - With mock R2R server
6. **Security Scan** - Trivy + Bandit
7. **Documentation Check** - Docstrings + markdown links

### Quality Gates

All checks must pass:
- ✅ Linting (ruff)
- ✅ Type checking (mypy)
- ✅ Tests (pytest)
- ✅ Coverage ≥ 80%
- ✅ Security scan (no critical issues)
- ✅ Documentation complete

### Failure Notifications

If CI fails on a Codegen PR:
- Automatic comment posted
- Codegen agent notified via `@codegen`
- Check suite auto-fixer triggered

## 📋 Issue Templates

### Feature Request (`codegen-feature-request.yml`)

**Use for:**
- New features
- Enhancements
- API additions

**Auto-assigns:** `@codegen-agent`

**Fields:**
- Feature description
- Acceptance criteria
- Priority level
- Technical notes
- Files to modify
- Agent behavior preferences

### Bug Fix (`codegen-bug-fix.yml`)

**Use for:**
- Bug reports
- Error fixes
- Performance issues

**Auto-assigns:** `@codegen-agent`

**Fields:**
- Bug description
- Expected behavior
- Reproduction steps
- Error logs
- Environment details
- Severity level
- Suspected files

## 🔧 Configuration Files

### `codegen-config.json`

**Repository-level Codegen configuration:**

```json
{
  "agent_behavior": {
    "propose_plan": true,
    "require_explicit_mentions": false,
    "auto_fix_checks": true,
    "max_check_retries": 3
  },
  "testing": {
    "coverage_threshold": 80
  },
  "integrations": {
    "github": { "enabled": true },
    "circleci": { "enabled": true },
    "mcp_servers": { "enabled": true }
  }
}
```

**Key Settings:**
- `propose_plan`: Agent shows implementation plan before coding
- `auto_fix_checks`: Auto-fix failing CI checks
- `max_check_retries`: Retry limit for failed checks (default: 3)

### Environment Variables

**Required Secrets:**

Add these to GitHub repository secrets:

```bash
# Codegen API Access
CODEGEN_API_KEY=<your-api-key>
CODEGEN_ORG_ID=<your-org-id>

# R2R Service Account
R2R_SERVICE_EMAIL=claude-code-service@example.com
R2R_SERVICE_PASSWORD=<secure-password>

# CircleCI Integration (optional)
CIRCLECI_TOKEN=<circleci-token>

# GitHub Token (automatically provided)
GITHUB_TOKEN=<auto-generated>
```

**How to Add Secrets:**
1. Go to repository Settings
2. Navigate to Secrets and Variables → Actions
3. Click "New repository secret"
4. Add each secret with exact name

## 📖 Usage Examples

### Trigger Codegen via Comment

```
@codegen implement error handling for authentication

Requirements:
- Catch all authentication errors
- Return proper HTTP status codes
- Log errors with context
- Include unit tests
```

### Trigger Codegen via Label

1. Create issue: "Add database connection pooling"
2. Add label: `codegen`
3. Agent automatically starts working

### Manual Workflow Dispatch

```bash
# Trigger CircleCI integration manually
curl -X POST \
  "https://api.github.com/repos/evgenygurin/claude_code_r2r/actions/workflows/codegen-circleci-integration.yml/dispatches" \
  -H "Authorization: token $GITHUB_TOKEN" \
  -d '{
    "ref": "master",
    "inputs": {
      "circleci_build_url": "https://circleci.com/gh/evgenygurin/claude_code_r2r/123",
      "pr_number": "42"
    }
  }'
```

### Check Agent Status

```bash
# View agent runs
curl -H "Authorization: Bearer $CODEGEN_API_KEY" \
  "https://api.codegen.com/v1/organizations/$CODEGEN_ORG_ID/agent/run"

# Get specific agent
curl -H "Authorization: Bearer $CODEGEN_API_KEY" \
  "https://api.codegen.com/v1/organizations/$CODEGEN_ORG_ID/agent/run/$AGENT_RUN_ID"
```

## 🎯 Best Practices

### When Creating Issues

1. **Be specific** - Clear requirements = better results
2. **Include context** - Link to related code/docs
3. **Add acceptance criteria** - Define "done"
4. **Specify files** - Help agent focus
5. **Choose agent behavior** - Propose plan? Include tests?

### When Reviewing Codegen PRs

1. **Check the plan** - Did agent understand requirements?
2. **Review implementation** - Does code match plan?
3. **Verify tests** - Are tests comprehensive?
4. **Check docs** - Is documentation updated?
5. **Use Codegen commands** - `@codegen add tests`, `@codegen fix checks`

### When CI Checks Fail

1. **Wait for auto-fix** - Agent will attempt fix automatically
2. **Check retry count** - Max 3 attempts by default
3. **Review logs** - If auto-fix fails, check what went wrong
4. **Manual trigger** - Comment `@codegen fix checks` to retry
5. **Escalate** - If still failing, human intervention needed

## 🔗 Related Documentation

- **[CLAUDE.md](../CLAUDE.md)** - Primary project instructions
- **[AGENTS.md](../AGENTS.md)** - Agent-specific rules and guidelines
- **[Codegen Docs](https://codegen.com/docs)** - Official Codegen documentation
- **[API Reference](https://api.codegen.com/docs)** - Codegen API documentation

## 🆘 Troubleshooting

### Agent Not Triggering

**Check:**
1. `@codegen` spelled correctly
2. Issue/PR has correct label
3. Repository has Codegen app installed
4. Secrets configured correctly

### CI Checks Always Failing

**Check:**
1. Coverage threshold (80% required)
2. Linting errors (run `ruff check .` locally)
3. Type errors (run `mypy .` locally)
4. Test failures (run `pytest tests/` locally)

### CircleCI Integration Not Working

**Check:**
1. `CIRCLECI_TOKEN` secret added
2. Webhook configured in CircleCI
3. Build URL format correct
4. PR number valid

## 📞 Support

**Issues:** Create issue with `question` label  
**Slack:** Join [Codegen community](https://community.codegen.com)  
**Email:** support@codegen.com

---

**Last Updated:** 2025-01-19  
**Maintained By:** @evgenygurin
