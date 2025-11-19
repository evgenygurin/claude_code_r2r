## User Management

R2R provides robust user authentication and management capabilities, ensuring secure and efficient access control over documents and features.

### Introduction

R2R's authentication system supports secure user registration, login, session management, and access control. This guide covers basic usage, advanced features, security considerations, and troubleshooting.

For detailed configuration, refer to the [Authentication Configuration Documentation](https://r2r-docs.sciphi.ai/documentation/configuration/auth) and the [User API Reference](https://r2r-docs.sciphi.ai/api-and-sdks/users/users).

**Default Behavior**: When `require_authentication` is set to `false` (default in `r2r.toml`), unauthenticated requests use default admin credentials. Use caution in production environments.

### Basic Usage

#### User Registration and Login

**Python Example:**

```python
from r2r import R2RClient

client = R2RClient("http://localhost:7272")  # Replace with your R2R deployment URL

# Register a new user
user_result = client.users.create("user1@test.com", "password123")
print(user_result)
# {'results': {'email': 'user1@test.com', 'id': 'bf417057-f104-4e75-8579-c74d26fcbed3', ...}}

# Login immediately (assuming email verification is disabled)
login_result = client.users.login("user1@test.com", "password123")
print(login_result)
# {'results': {'access_token': {...}, 'refresh_token': {...}}}
```

#### Email Verification (Optional)

If email verification is enabled:

```python
# Verify email
verify_result = client.users.verify_email("verification_code_here")
print(verify_result)
# {"results": {"message": "Email verified successfully"}}
```

#### Token Refresh

Refresh an expired access token:

```python
refresh_result = client.users.refresh_access_token("YOUR_REFRESH_TOKEN")
print(refresh_result)
# {'access_token': {...}, 'refresh_token': {...}}
```

#### User-Specific Search

Authenticated searches are filtered based on the user's permissions.

**Curl Example:**

```bash
curl -X POST http://localhost:7272/v3/retrieval/search \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Who was Aristotle"
  }'
```

**Sample Output:**

```json
{
  "results": {
    "chunk_search_results": [],
    "kg_search_results": []
  }
}
```

> *Search results are empty for a new user.*

#### User Logout

Invalidate the current access token.

**Curl Example:**

```bash
curl -X POST http://localhost:7272/v3/users/logout \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Sample Output:**

```json
{
  "results": {"message": "Logged out successfully"}
}
```

### Advanced Authentication Features

#### Password Management

Users can change their passwords and request password resets.

**Python Example:**

```python
# Change password
change_password_result = client.users.change_password("password123", "new_password")
print(change_password_result)
# {"results": {"message": "Password changed successfully"}}

# Request password reset
reset_request_result = client.users.request_password_reset("user@example.com")
print(reset_request_result)
# {"results": {"message": "If the email exists, a reset link has been sent"}}

# Confirm password reset
reset_confirm_result = client.users.confirm_password_reset("reset_token_here", "new_password")
print(reset_confirm_result)
# {"results": {"message": "Password reset successfully"}}
```

#### User Profile Management

Users can view and update their profiles.

**Python Example:**

```python
# Update user profile (requires login)
update_result = client.users.update_user(name="John Doe", bio="R2R enthusiast")
print(update_result)
# {'results': {'email': 'user1@test.com', 'id': '76eea168-9f98-4672-af3b-2c26ec92d7f8', ...}}
```

#### Account Deletion

Users can delete their accounts.

**Python Example:**

```python
# Delete account (requires password confirmation)
user_id = register_response["results"]["id"]  # Use the actual user ID
delete_result = client.delete_user(user_id, "password123")
print(delete_result)
# {'results': {'message': 'User account deleted successfully'}}
```

#### Logout

To end a user session:

```python
# Logout
logout_result = client.users.logout()
print(f"Logout Result:\n{logout_result}")
# {'results': {'message': 'Logged out successfully'}}
```

### Superuser Capabilities and Default Admin Creation

#### Superuser Capabilities

Superusers have elevated privileges, enabling them to:

1. **User Management**: View, modify, and delete user accounts.
2. **System-wide Document Access**: Access and manage all documents.
3. **Analytics and Observability**: Access system-wide analytics and logs.
4. **Configuration Management**: Modify system configurations and settings.

#### Default Admin Creation

R2R automatically creates a default admin user during initialization via the `R2RAuthProvider` class.

**Configuration:**

```toml
[auth]
provider = "r2r"
access_token_lifetime_in_minutes = 60
refresh_token_lifetime_in_days = 7
require_authentication = true
require_email_verification = false
default_admin_email = "admin@example.com"
default_admin_password = "change_me_immediately"
```

- **`require_authentication`**: Set to `false` for development/testing; `true` for production.
- **`require_email_verification`**: Set to `false` by default; consider enabling for production.

#### Accessing Superuser Features

Authenticate as the default admin or another superuser to access superuser features.

**Python Example:**

```python
from r2r import R2RClient

client = R2RClient("http://localhost:7272")

# Login as admin
login_result = client.users.login("admin@example.com", "change_me_immediately")

# Access superuser features
users_overview = client.users.list()
print(users_overview)

# Access system-wide logs
logs = client.logs()
print(logs)

# Perform analytics
analytics_result = client.analytics(
    {"all_latencies": "search_latency"},
    {"search_latencies": ["basic_statistics", "search_latency"]}
)
print(analytics_result)
```

### Security Considerations for Superusers

When using superuser capabilities:

1. **Limit Superuser Access**: Only grant to trusted individuals.
2. **Use Strong Passwords**: Ensure superuser accounts use strong, unique passwords.
3. **Enable Authentication and Verification**: Set `require_authentication` and `require_email_verification` to `true` in production.
4. **Audit Superuser Actions**: Regularly review logs of superuser activities.
5. **Rotate Credentials**: Periodically update superuser credentials, including the default admin password.

### Security Considerations

When implementing user authentication, consider the following security best practices:

1. **Use HTTPS**: Always use HTTPS in production to encrypt data in transit.
2. **Implement Rate Limiting**: Protect against brute-force attacks by limiting login attempts.
3. **Use Secure Password Hashing**: R2R uses bcrypt for password hashing by default.
4. **Implement Multi-Factor Authentication (MFA)**: Add MFA for an extra layer of security.
5. **Regular Security Audits**: Conduct regular security audits of your authentication system.

### Customizing Authentication

R2R’s authentication system is flexible and can be customized to fit your specific needs:

1. **Custom User Fields**: Extend the User model to include additional fields.
2. **OAuth Integration**: Integrate with third-party OAuth providers for social login.
3. **Custom Password Policies**: Implement custom password strength requirements.
4. **User Roles and Permissions**: Implement a role-based access control system.

### Troubleshooting

**Common Issues and Solutions:**

1. **Login Fails After Registration**:
   - Ensure email verification is completed if enabled.

2. **Token Refresh Fails**:
   - Check if the refresh token has expired; the user may need to log in again.

3. **Unable to Change Password**:
   - Verify that the current password is correct.

### Conclusion

R2R provides a comprehensive set of user authentication and management features, allowing developers to implement secure and user-friendly applications. By leveraging these capabilities, you can implement robust user authentication, document management, and access control in your R2R-based projects.

For more advanced use cases or custom implementations, refer to the R2R documentation or reach out to the community for support.

---