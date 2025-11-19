## Users

### Overview

A **User** in R2R represents an authenticated entity that can interact with the system. Users are the foundation of R2R’s access control system, enabling granular permissions management, activity tracking, and content organization through collections.

### Core Features of Users

1. **Authentication & Authorization**
    - Secure login and token-based authentication.
    - Role-based access control (regular users vs. superusers).

2. **Collection Membership Management**
    - Manage access to documents and graphs through collections.
    - Add or remove users from collections to control access.

3. **Activity Tracking & Analytics**
    - Monitor user activities and interactions within the system.

4. **Metadata Customization**
    - Store additional user information such as name, bio, and profile picture.

5. **Superuser Capabilities**
    - Manage system-wide settings, users, and prompts.

### Available Endpoints

| Method | Endpoint                                      | Description                                         |
| :---- | :-------------------------------------------- | :-------------------------------------------------- |
| GET    | `/users`                                      | List users with pagination (superusers only)       |
| GET    | `/users/{user_id}`                            | Get detailed user information                      |
| GET    | `/users/{user_id}/collections`                | List user’s collections                             |
| POST   | `/users/{user_id}/collections/{collection_id}`| Add user to collection                              |
| DELETE | `/users/{user_id}/collections/{collection_id}`| Remove user from collection                         |
| POST   | `/users/{user_id}`                            | Update user information                             |
| POST   | `/users/register`                             | Register a new user                                 |
| POST   | `/users/verify-email`                         | Verify user's email address                         |
| POST   | `/users/login`                                | Authenticate user and get tokens                    |
| POST   | `/users/logout`                               | Log out current user                                |
| POST   | `/users/refresh-token`                        | Refresh access token using a refresh token          |
| POST   | `/users/change-password`                      | Change the authenticated user’s password            |
| POST   | `/users/request-password-reset`               | Request a password reset for a user                  |
| POST   | `/users/reset-password`                       | Reset a user’s password using a reset token          |
| GET    | `/users/me`                                   | Get detailed information about the currently authenticated user |
| GET    | `/users/{id}`                                 | Get detailed information about a specific user       |
| POST   | `/users/{id}`                                 | Update user information                              |
| DELETE | `/users/{id}`                                 | Delete a specific user                               |
| GET    | `/users/{id}/collections`                     | List all collections associated with a specific user |
| POST   | `/users/{id}/collections/{collection_id}`     | Add a user to a collection                          |
| DELETE | `/users/{id}/collections/{collection_id}`     | Remove a user from a collection                     |

### Endpoint Details

#### 1. Register a New User

```http
POST /v3/users/register
```

**Description:**
Registers a new user with the provided email and password. Upon registration, the user is inactive until their email is verified.

**Request Body:**

A JSON object containing the user's email and password.

**Example Request Body:**

```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Successful Response:**

```json
{
  "results": {
    "id": "user-id",
    "email": "user@example.com",
    "is_active": true,
    "is_superuser": false,
    "created_at": "2024-01-15T09:30:00Z",
    "updated_at": "2024-01-15T09:30:00Z",
    "is_verified": false,
    "collection_ids": ["collection_id1"],
    "graph_ids": ["graph_id1"],
    "document_ids": ["document_id1"],
    "hashed_password": "hashed_password",
    "verification_code_expiry": "2024-01-16T09:30:00Z",
    "name": "John Doe",
    "bio": "A software developer.",
    "profile_picture": "https://example.com/profile.jpg",
    "total_size_in_bytes": 204800,
    "num_files": 10
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**: Invalid input or email already exists.

**Example cURL:**

```bash
curl -X POST "https://api.example.com/v3/users/register" \
     -H "Content-Type: application/json" \
     -d '{
           "email": "user@example.com",
           "password": "SecurePassword123!"
         }'
```

---

#### 2. Verify User's Email Address

```http
POST /v3/users/verify-email
```

**Description:**
Verifies a user’s email address using a verification code sent during registration.

**Request Body:**

A JSON object containing the user's email and verification code.

**Example Request Body:**

```json
{
  "email": "user@example.com",
  "verification_code": "123456"
}
```

**Successful Response:**

```json
{
  "results": {
    "message": "Email verified successfully."
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**: Invalid verification code or email.

**Example cURL:**

```bash
curl -X POST "https://api.example.com/v3/users/verify-email" \
     -H "Content-Type: application/json" \
     -d '{
           "email": "user@example.com",
           "verification_code": "123456"
         }'
```

---

#### 3. Authenticate User and Get Tokens

```http
POST /v3/users/login
```

**Description:**
Authenticates a user and provides access and refresh tokens upon successful login.

**Request Body:**

A JSON object containing the user's email and password.

**Example Request Body:**

```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Successful Response:**

```json
{
  "results": {
    "access_token": {
      "token": "access_token_string",
      "token_type": "Bearer"
    },
    "refresh_token": {
      "token": "refresh_token_string",
      "token_type": "Bearer"
    }
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**: Invalid credentials or account inactive.

**Example cURL:**

```bash
curl -X POST "https://api.example.com/v3/users/login" \
     -H "Content-Type: application/json" \
     -d '{
           "email": "user@example.com",
           "password": "SecurePassword123!"
         }'
```

---

#### 4. Log Out Current User

```http
POST /v3/users/logout
```

**Description:**
Logs out the current user, invalidating their access token.

**Request Body:**

No parameters required.

**Successful Response:**

```json
{
  "results": {
    "message": "Logged out successfully."
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**: Invalid token or already logged out.

**Example cURL:**

```bash
curl -X POST "https://api.example.com/v3/users/logout" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---

#### 5. Refresh Access Token

```http
POST /v3/users/refresh-token
```

**Description:**
Refreshes the access token using a valid refresh token, providing new access and refresh tokens.

**Request Body:**

A JSON object containing the refresh token.

**Example Request Body:**

```json
{
  "refresh_token": "refresh_token_string"
}
```

**Successful Response:**

```json
{
  "results": {
    "access_token": {
      "token": "new_access_token_string",
      "token_type": "Bearer"
    },
    "refresh_token": {
      "token": "new_refresh_token_string",
      "token_type": "Bearer"
    }
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**: Invalid or expired refresh token.

**Example cURL:**

```bash
curl -X POST "https://api.example.com/v3/users/refresh-token" \
     -H "Content-Type: application/json" \
     -d '{
           "refresh_token": "refresh_token_string"
         }'
```

---

#### 6. Change User Password

```http
POST /v3/users/change-password
```

**Description:**
Changes the authenticated user’s password.

**Request Body:**

A JSON object containing the current and new passwords.

**Example Request Body:**

```json
{
  "current_password": "OldPassword123!",
  "new_password": "NewSecurePassword456!"
}
```

**Successful Response:**

```json
{
  "results": {
    "message": "Password changed successfully."
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**: Invalid current password or new password does not meet criteria.

**Example cURL:**

```bash
curl -X POST "https://api.example.com/v3/users/change-password" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "current_password": "OldPassword123!",
           "new_password": "NewSecurePassword456!"
         }'
```

---

#### 7. Request Password Reset

```http
POST /v3/users/request-password-reset
```

**Description:**
Requests a password reset for a user by sending a reset link to their email.

**Request Body:**

A JSON object containing the user's email.

**Example Request Body:**

```json
{
  "email": "user@example.com"
}
```

**Successful Response:**

```json
{
  "results": {
    "message": "Password reset link sent to email."
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**: Email does not exist or already requested.

**Example cURL:**

```bash
curl -X POST "https://api.example.com/v3/users/request-password-reset" \
     -H "Content-Type: application/json" \
     -d '{
           "email": "user@example.com"
         }'
```

---

#### 8. Reset Password with Token

```http
POST /v3/users/reset-password
```

**Description:**
Resets a user’s password using a valid reset token.

**Request Body:**

A JSON object containing the reset token and the new password.

**Example Request Body:**

```json
{
  "reset_token": "reset_token_string",
  "new_password": "NewSecurePassword456!"
}
```

**Successful Response:**

```json
{
  "results": {
    "message": "Password reset successfully."
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**: Invalid or expired reset token.

**Example cURL:**

```bash
curl -X POST "https://api.example.com/v3/users/reset-password" \
     -H "Content-Type: application/json" \
     -d '{
           "reset_token": "reset_token_string",
           "new_password": "NewSecurePassword456!"
         }'
```

---

#### 9. List All Users (Superusers Only)

```http
GET /v3/users
```

**Description:**
Lists all users in the system with pagination and filtering options. Accessible only by superusers.

**Query Parameters:**

| Parameter | Type      | Required | Description                           |
| :-------- | :-------- | :------ | :------------------------------------ |
| `ids`     | `string` | No      | A comma-separated list of user IDs to retrieve. |
| `offset`  | `integer`| No      | Number of users to skip. Defaults to `0`. |
| `limit`   | `integer`| No      | Number of users to return (`1–100`). Defaults to `100`. |

**Successful Response:**

```json
{
  "results": [
    {
      "id": "user_id",
      "email": "user@example.com",
      "is_active": true,
      "is_superuser": false,
      "created_at": "2024-01-15T09:30:00Z",
      "updated_at": "2024-01-15T09:30:00Z",
      "is_verified": true,
      "collection_ids": ["collection_id1"],
      "graph_ids": ["graph_id1"],
      "document_ids": ["document_id1"],
      "hashed_password": "hashed_password",
      "verification_code_expiry": "2024-01-16T09:30:00Z",
      "name": "John Doe",
      "bio": "A software developer.",
      "profile_picture": "https://example.com/profile.jpg",
      "total_size_in_bytes": 204800,
      "num_files": 10
    }
  ],
  "total_entries": 1
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X GET "https://api.example.com/v3/users?limit=10" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---

#### 10. Get Authenticated User Details

```http
GET /v3/users/me
```

**Description:**
Retrieves detailed information about the currently authenticated user.

**Successful Response:**

```json
{
  "results": {
    "id": "id",
    "email": "email@example.com",
    "is_active": true,
    "is_superuser": true,
    "created_at": "2024-01-15T09:30:00Z",
    "updated_at": "2024-01-15T09:30:00Z",
    "is_verified": true,
    "collection_ids": ["collection_id1"],
    "graph_ids": ["graph_id1"],
    "document_ids": ["document_id1"],
    "hashed_password": "hashed_password",
    "verification_code_expiry": "2024-01-16T09:30:00Z",
    "name": "John Doe",
    "bio": "A software developer.",
    "profile_picture": "https://example.com/profile.jpg",
    "total_size_in_bytes": 204800,
    "num_files": 10
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X GET "https://api.example.com/v3/users/me" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---

#### 11. Get User Details

```http
GET /v3/users/:id
```

**Description:**
Retrieves detailed information about a specific user. Users can only access their own information unless they are superusers.

**Path Parameters:**

| Parameter | Type   | Required | Description                |
| :-------- | :----- | :------ | :------------------------- |
| `id`      | `string` | Yes      | The User ID to retrieve.   |

**Successful Response:**

```json
{
  "results": {
    "id": "user_id",
    "email": "user@example.com",
    "is_active": true,
    "is_superuser": false,
    "created_at": "2024-01-15T09:30:00Z",
    "updated_at": "2024-01-15T09:30:00Z",
    "is_verified": true,
    "collection_ids": ["collection_id1"],
    "graph_ids": ["graph_id1"],
    "document_ids": ["document_id1"],
    "hashed_password": "hashed_password",
    "verification_code_expiry": "2024-01-16T09:30:00Z",
    "name": "John Doe",
    "bio": "A software developer.",
    "profile_picture": "https://example.com/profile.jpg",
    "total_size_in_bytes": 204800,
    "num_files": 10
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X GET "https://api.example.com/v3/users/user_id" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---

#### 12. Update User Information

```http
POST /v3/users/:id
```

**Description:**
Updates user information. Users can only update their own information unless they are superusers. Superuser status can only be modified by existing superusers.

**Path Parameters:**

| Parameter | Type   | Required | Description                         |
| :-------- | :----- | :------ | :---------------------------------- |
| `id`      | `string` | Yes      | The User ID to update.              |

**Request Body:**

A JSON object containing the updated user details.

**Example Request Body:**

```json
{
  "email": "new_email@example.com",
  "name": "Jane Doe",
  "bio": "An experienced software engineer.",
  "profile_picture": "https://example.com/new_profile.jpg"
}
```

**Successful Response:**

```json
{
  "results": {
    "id": "user_id",
    "email": "new_email@example.com",
    "is_active": true,
    "is_superuser": false,
    "created_at": "2024-01-15T09:30:00Z",
    "updated_at": "2024-02-20T10:45:00Z",
    "is_verified": true,
    "collection_ids": ["collection_id1"],
    "graph_ids": ["graph_id1"],
    "document_ids": ["document_id1"],
    "hashed_password": "hashed_password",
    "verification_code_expiry": "2024-01-16T09:30:00Z",
    "name": "Jane Doe",
    "bio": "An experienced software engineer.",
    "profile_picture": "https://example.com/new_profile.jpg",
    "total_size_in_bytes": 204800,
    "num_files": 10
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X POST "https://api.example.com/v3/users/user_id" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "email": "new_email@example.com",
           "name": "Jane Doe",
           "bio": "An experienced software engineer.",
           "profile_picture": "https://example.com/new_profile.jpg"
         }'
```

---

#### 13. Delete User

```http
DELETE /v3/users/:id
```

**Description:**
Deletes a specific user account. Users can only delete their own account unless they are superusers.

**Path Parameters:**

| Parameter | Type   | Required | Description                        |
| :-------- | :----- | :------ | :--------------------------------- |
| `id`      | `string` | Yes      | The User ID to delete.             |

**Request Body:**

A JSON object containing optional parameters to confirm deletion.

**Example Request Body:**

```json
{
  "password": "SecurePassword123!",
  "delete_vector_data": true
}
```

**Successful Response:**

```json
{
  "results": {
    "success": true
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X DELETE "https://api.example.com/v3/users/user_id" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "password": "SecurePassword123!",
           "delete_vector_data": true
         }'
```

---

#### 14. List User's Collections

```http
GET /v3/users/:id/collections
```

**Description:**
Retrieves all collections associated with a specific user. Users can only access their own collections unless they are superusers.

**Path Parameters:**

| Parameter | Type   | Required | Description                        |
| :-------- | :----- | :------ | :--------------------------------- |
| `id`      | `string` | Yes      | The User ID to retrieve collections for. |

**Query Parameters:**

| Parameter | Type      | Required | Description                           |
| :-------- | :-------- | :------ | :------------------------------------ |
| `offset`  | `integer` | No      | Number of collections to skip. Defaults to `0`. |
| `limit`   | `integer` | No      | Number of collections to return (`1–100`). Defaults to `100`. |

**Successful Response:**

```json
{
  "results": [
    {
      "id": "collection_id",
      "name": "Collection Name",
      "graph_cluster_status": "status",
      "graph_sync_status": "status",
      "created_at": "2024-01-15T09:30:00Z",
      "updated_at": "2024-01-15T09:30:00Z",
      "user_count": 10,
      "document_count": 50,
      "owner_id": "owner_id",
      "description": "A sample collection."
    }
  ],
  "total_entries": 1
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X GET "https://api.example.com/v3/users/user_id/collections?limit=10" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---

#### 15. Add User to Collection

```http
POST /v3/users/:id/collections/:collection_id
```

**Description:**
Adds a user to a specific collection, granting them access to its documents and graphs. The authenticated user must have admin permissions for the collection to add new users.

**Path Parameters:**

| Parameter      | Type   | Required | Description                                |
| :------------- | :----- | :------ | :----------------------------------------- |
| `id`           | `string` | Yes      | The User ID to add to the collection.      |
| `collection_id`| `string` | Yes      | The Collection ID to add the user to.       |

**Successful Response:**

```json
{
  "results": {
    "success": true
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X POST "https://api.example.com/v3/users/user_id/collections/collection_id" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---

#### 16. Remove User from Collection

```http
DELETE /v3/users/:id/collections/:collection_id
```

**Description:**
Removes a user from a specific collection, revoking their access to its documents and graphs. The authenticated user must have admin permissions for the collection to remove users.

**Path Parameters:**

| Parameter      | Type   | Required | Description                                |
| :------------- | :----- | :------ | :----------------------------------------- |
| `id`           | `string` | Yes      | The User ID to remove from the collection. |
| `collection_id`| `string` | Yes      | The Collection ID to remove the user from.  |

**Successful Response:**

```json
{
  "results": {
    "success": true
  }
}
```

**Error Response:**

- **422 Unprocessable Entity**

**Example cURL:**

```bash
curl -X DELETE "https://api.example.com/v3/users/user_id/collections/collection_id" \
     -H "Authorization: Bearer YOUR_API_KEY"
```

---