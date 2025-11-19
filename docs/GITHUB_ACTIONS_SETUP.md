# GitHub Actions Setup Guide

This guide explains how to configure GitHub Actions workflows for Codegen integration.

## Required Secrets

Configure the following secrets in your repository settings (`Settings` → `Secrets and variables` → `Actions`):

### 1. **CODEGEN_API_KEY** (Required)

Your Codegen API key for authentication.

**How to obtain:**
1. Go to [codegen.com/settings/api-keys](https://codegen.com/settings/api-keys)
2. Click "Generate New API Key"
3. Copy the key (it will only be shown once!)
4. Add it to GitHub Secrets as `CODEGEN_API_KEY`

**Scope:** Required for all Codegen workflows

---

### 2. **CODEGEN_ORG_ID** (Required)

Your Codegen organization ID.

**How to obtain:**
1. Go to [codegen.com/settings](https://codegen.com/settings)
2. Your organization ID is shown in the URL: `codegen.com/org/{ORG_ID}/settings`
3. Or find it in the API response when creating an agent run
4. Add it to GitHub Secrets as `CODEGEN_ORG_ID`

**Type:** Integer (e.g., `12345`)

**Scope:** Required for all Codegen workflows

---

### 3. **CIRCLECI_TOKEN** (Optional)

CircleCI API token for CircleCI integration workflows.

**How to obtain:**
1. Go to CircleCI: [app.circleci.com/settings/user/tokens](https://app.circleci.com/settings/user/tokens)
2. Click "Create New Token"
3. Give it a name (e.g., "GitHub Actions Integration")
4. Copy the token
5. Add it to GitHub Secrets as `CIRCLECI_TOKEN`

**Scope:** Only required if using `codegen-circleci-integration.yml`

---

## Workflow Configuration

### Available Workflows

| Workflow | Purpose | Trigger | Secrets Required |
|----------|---------|---------|------------------|
| `ci.yml` | Run tests, linting, security scans | Push, PR | `GITHUB_TOKEN` (auto) |
| `codegen-agent-trigger.yml` | Trigger Codegen agent from comments | Issue/PR comment with `@codegen` | `CODEGEN_API_KEY`, `CODEGEN_ORG_ID` |
| `codegen-checks-autofixer.yml` | Auto-fix failing CI checks | Check suite failure | `CODEGEN_API_KEY`, `CODEGEN_ORG_ID` |
| `codegen-pr-review.yml` | Automated PR code review | PR opened/updated | `CODEGEN_API_KEY`, `CODEGEN_ORG_ID` |
| `codegen-circleci-integration.yml` | Monitor CircleCI failures | Manual dispatch or webhook | `CODEGEN_API_KEY`, `CODEGEN_ORG_ID`, `CIRCLECI_TOKEN` |
| `codegen-sync.yml` | Health checks and analytics | Daily cron | `CODEGEN_API_KEY`, `CODEGEN_ORG_ID` |

---

## Step-by-Step Setup

### 1. Add Secrets to GitHub

```bash
# Navigate to your repository
# Go to: Settings → Secrets and variables → Actions → New repository secret

# Add each secret:
CODEGEN_API_KEY=sk_live_xxxxxxxxxxxxx
CODEGEN_ORG_ID=12345
CIRCLECI_TOKEN=xxxxxxxxxxxxxxx  # Optional
```

### 2. Enable Workflows

All workflows are already in `.github/workflows/`. They will activate automatically when:

- **ci.yml**: Automatically runs on push/PR
- **codegen-agent-trigger.yml**: Triggers when you comment `@codegen` on issues/PRs
- **codegen-checks-autofixer.yml**: Automatically runs when checks fail on Codegen PRs
- **codegen-pr-review.yml**: Automatically runs when PRs are opened
- **codegen-circleci-integration.yml**: Manual dispatch or CircleCI webhook
- **codegen-sync.yml**: Runs daily at 2 AM UTC

### 3. Verify Setup

#### Test Agent Trigger

1. Create an issue or PR
2. Comment: `@codegen please help with this`
3. Check:
   - ✅ Workflow runs in `Actions` tab
   - ✅ Codegen responds with Agent Run ID
   - ✅ Agent appears at [codegen.com/agents](https://codegen.com/agents)

#### Test Auto-fixer

1. Create a PR with Codegen
2. Let a CI check fail
3. Check:
   - ✅ Auto-fixer workflow triggers
   - ✅ Codegen comments on the PR
   - ✅ Fix commits are pushed automatically

---

## Troubleshooting

### Error: "Codegen API call failed with status 403"

**Cause:** Invalid or missing API key

**Solution:**
1. Verify `CODEGEN_API_KEY` is set correctly in GitHub Secrets
2. Check that the API key hasn't expired at [codegen.com/settings/api-keys](https://codegen.com/settings/api-keys)
3. Regenerate the key if needed

---

### Error: "Failed to trigger Codegen fix: No repos found"

**Cause:** Repository not connected to Codegen organization

**Solution:**
1. Go to [github.com/apps/codegen-sh](https://github.com/apps/codegen-sh)
2. Click "Configure"
3. Add your repository to Codegen's access list
4. Verify `CODEGEN_ORG_ID` matches your organization

---

### Error: "Rate limit exceeded"

**Cause:** Too many API calls (limit: 10 requests/minute)

**Solution:**
- Wait 1 minute and retry
- Reduce frequency of workflow triggers
- Contact Codegen support to increase rate limit

---

### Workflow doesn't trigger

**Cause:** Permissions or triggers misconfigured

**Solution:**
1. Check repository settings:
   - `Settings` → `Actions` → `General`
   - Enable "Allow all actions and reusable workflows"
   - Enable "Read and write permissions" for GITHUB_TOKEN

2. Verify workflow trigger:
   - For comment triggers: Ensure you use exact format `@codegen`
   - For check failures: Ensure PR is created by Codegen

---

## Best Practices

### Security

1. **Never commit secrets to git**
   - Always use GitHub Secrets
   - Add `.env` to `.gitignore`

2. **Rotate API keys regularly**
   - Regenerate keys every 90 days
   - Update GitHub Secrets when rotating

3. **Use least privilege**
   - Only enable workflows you need
   - Limit repository access in Codegen app settings

### Performance

1. **Avoid rate limits**
   - Don't spam `@codegen` mentions
   - Use manual dispatch for testing instead of triggers

2. **Monitor usage**
   - Check `codegen-sync.yml` analytics daily
   - Review token usage at [codegen.com/analytics](https://codegen.com/analytics)

3. **Optimize prompts**
   - Be specific in agent requests
   - Include relevant context and files

---

## Additional Resources

- **Codegen Documentation**: [docs.codegen.com](https://docs.codegen.com)
- **API Reference**: [docs.codegen.com/api-reference](https://docs.codegen.com/api-reference)
- **GitHub Integration Guide**: [docs.codegen.com/integrations/github](https://docs.codegen.com/integrations/github)
- **Support**: [codegen.com/support](https://codegen.com/support)

---

## Example: Triggering Agent from Comment

```markdown
@codegen please implement the following:

- Add authentication middleware
- Create JWT token generation
- Add protected route decorator

Files to modify:
- src/middleware/auth.py
- src/utils/jwt.py
- src/routes/protected.py
```

Codegen will:
1. Create an agent run
2. Analyze the requirements
3. Create a new branch
4. Implement the changes
5. Open a PR with the solution
6. Respond to PR comments and fix failing tests automatically

---

**Last Updated:** 2025-11-19
