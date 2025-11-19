## Collections

### Introduction

A **collection** in R2R is a logical grouping of users and documents that allows for efficient access control and organization. Collections enable you to manage permissions and access to documents at a group level, rather than individually.

R2R provides robust document collection management, allowing developers to implement efficient access control and organization of users and documents.

**Note**: Collection permissioning in R2R is under development and may continue evolving in future releases.

### Basic Usage

#### Collection CRUD Operations

**Creating a Collection:**

```python
from r2r import R2RClient

client = R2RClient("http://localhost:7272")  # Replace with your R2R deployment URL

# Create a new collection
collection_result = client.collections.create("Marketing Team", "Collection for marketing department")
print(f"Collection creation result: {collection_result}")
# {'results': {'collection_id': '123e4567-e89b-12d3-a456-426614174000', 'name': 'Marketing Team', 'description': 'Collection for marketing department', ...}}
```

**Retrieving Collection Details:**

```python
collection_id = '123e4567-e89b-12d3-a456-426614174000'  # Use the actual collection_id

collection_details = client.collections.retrieve(collection_id)
print(f"Collection details: {collection_details}")
# {'results': {'collection_id': '123e4567-e89b-12d3-a456-426614174000', 'name': 'Marketing Team', 'description': 'Collection for marketing department', ...}}
```

**Updating a Collection:**

```python
update_result = client.collections.update(
    collection_id,
    name="Updated Marketing Team",
    description="New description for marketing team"
)
print(f"Collection update result: {update_result}")
# {'results': {'collection_id': '123e4567-e89b-12d3-a456-426614174000', 'name': 'Updated Marketing Team', 'description': 'New description for marketing team', ...}}
```

**Deleting a Collection:**

```python
client.collections.delete(collection_id)
```

### User Management in Collections

#### Adding a User to a Collection

```python
user_id = '456e789f-g01h-34i5-j678-901234567890'  # Valid user ID
collection_id = '123e4567-e89b-12d3-a456-426614174000'  # Valid collection ID

add_user_result = client.collections.add_user(user_id, collection_id)
print(f"Add user to collection result: {add_user_result}")
# {'results': {'message': 'User successfully added to the collection'}}
```

#### Removing a User from a Collection

```python
remove_user_result = client.collections.remove_user(user_id, collection_id)
print(f"Remove user from collection result: {remove_user_result}")
# {'results': None}
```

#### Listing Users in a Collection

```python
users_in_collection = client.collections.list_users(collection_id)
print(f"Users in collection: {users_in_collection}")
# {'results': [{'user_id': '456e789f-g01h-34i5-j678-901234567890', 'email': 'user@example.com', 'name': 'John Doe', ...}, ...]}
```

#### Getting Collections for a User

```python
user_collections = client.user.list_collections(user_id)
print(f"User's collections: {user_collections}")
# {'results': [{'collection_id': '123e4567-e89b-12d3-a456-426614174000', 'name': 'Updated Marketing Team', ...}, ...]}
```

### Document Management in Collections

#### Assigning a Document to a Collection

```python
document_id = '789g012j-k34l-56m7-n890-123456789012'  # Valid document ID

assign_doc_result = client.collections.add_document(collection_id, document_id)
print(f"Assign document to collection result: {assign_doc_result}")
# {'results': {'message': 'Document successfully assigned to the collection'}}
```

#### Removing a Document from a Collection

```python
remove_doc_result = client.collections.remove_document(collection_id, document_id)
print(f"Remove document from collection result: {remove_doc_result}")
# {'results': {'message': 'Document successfully removed from the collection'}}
```

#### Listing Documents in a Collection

```python
docs_in_collection = client.collections.list_documents(collection_id)
print(f"Documents in collection: {docs_in_collection}")
# {'results': [{'document_id': '789g012j-k34l-56m7-n890-123456789012', 'title': 'Marketing Strategy 2024', ...}, ...]}
```

#### Getting Collections for a Document

```python
document_collections = client.documents.list_collections(document_id)
print(f"Document's collections: {document_collections}")
# {'results': [{'collection_id': '123e4567-e89b-12d3-a456-426614174000', 'name': 'Updated Marketing Team', ...}, ...]}
```

### Advanced Collection Management

#### Generating Synthetic Descriptions

Generate a description for a collection using an LLM.

```python
update_result = client.collections.update(
    collection_id,
    generate_description=True
)
print(f"Collection update result: {update_result}")
# {'results': {'collection_id': '123e4567-e89b-12d3-a456-426614174000', 'name': 'Updated Marketing Team', 'description': 'A rich description...', ...}}
```

#### Collection Overview

Get an overview of collections, including user and document counts.

```python
collections_list = client.collections.list()
print(f"Collections overview: {collections_list}")
# {'results': [{'collection_id': '123e4567-e89b-12d3-a456-426614174000', 'name': 'Updated Marketing Team', 'description': 'New description...', 'user_count': 5, 'document_count': 10, ...}, ...]}
```

### Pagination and Filtering

Many collection-related methods support pagination and filtering.

**Examples:**

```python
# List collections with pagination
paginated_collections = client.collections.list(offset=10, limit=20)

# Get users in a collection with pagination
paginated_users = client.collections.list_users(collection_id, offset=5, limit=10)

# Get documents in a collection with pagination
paginated_docs = client.collections.list_documents(collection_id, offset=0, limit=50)

# Get specific collections by IDs
specific_collections = client.collections.list(collection_ids=['id1', 'id2', 'id3'])
```

### Security Considerations

When implementing collection permissions, consider the following security best practices:

1. **Least Privilege Principle**: Assign minimum necessary permissions to users and collections.
2. **Regular Audits**: Periodically review collection memberships and document assignments.
3. **Access Control**: Ensure only authorized users (e.g., admins) can perform collection management operations.
4. **Logging and Monitoring**: Implement comprehensive logging for all collection-related actions.

### Customizing Collection Permissions

While R2R’s current collection system follows a flat hierarchy, you can build more complex permission structures:

1. **Custom Roles**: Implement application-level roles within collections (e.g., collection admin, editor, viewer).
2. **Hierarchical Collections**: Create a hierarchy by establishing parent-child relationships between collections in your application logic.
3. **Permission Inheritance**: Implement rules for permission inheritance based on collection memberships.

### Troubleshooting

**Common Issues and Solutions:**

1. **Unable to Create/Modify Collections**:
   - Ensure the user has superuser privileges.

2. **User Not Seeing Collection Content**:
   - Verify that the user is correctly added to the collection.
   - Ensure documents are properly assigned.

3. **Performance Issues with Large Collections**:
   - Use pagination when retrieving users or documents.
   - Consider splitting large collections.

### Conclusion

R2R’s collection permissioning system provides a foundation for implementing sophisticated access control in your applications. As the feature set evolves, more advanced capabilities will become available. Regularly update your practices based on the latest R2R documentation.

### Next Steps

- Explore [GraphRAG](https://r2r-docs.sciphi.ai/cookbooks/graphrag) for advanced features.
- Learn about [hybrid search](https://r2r-docs.sciphi.ai/cookbooks/hybrid-search) integration.
- Discover more about [observability](https://r2r-docs.sciphi.ai/cookbooks/observability).
- Set up [orchestration](https://r2r-docs.sciphi.ai/cookbooks/orchestration) for large-scale processing.

---