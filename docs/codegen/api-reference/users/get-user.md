# Get User

> Get details for a specific user in an organization.

Returns detailed information about a user within the specified organization.
The requesting user must be a member of the organization to access this endpoint.

Rate limit: 60 requests per 30 seconds.

## OpenAPI

````yaml api-reference/openapi3.json get /v1/organizations/{org_id}/users/{user_id}
paths:
  path: /v1/organizations/{org_id}/users/{user_id}
  method: get
  servers:
    - url: https://api.codegen.com
      description: Codegen API
  request:
    security: []
    parameters:
      path:
        org_id:
          schema:
            - type: integer
              required: true
              title: Org Id
        user_id:
          schema:
            - type: integer
              required: true
              title: User Id
      query: {}
      header:
        authorization:
          schema:
            - type: any
              required: false
              title: Authorization
      cookie: {}
    body: {}
  response:
    '200':
      application/json:
        schemaArray:
          - type: object
            properties:
              id:
                allOf:
                  - type: integer
                    title: Id
                    description: Unique user ID
              email:
                allOf:
                  - anyOf:
                      - type: string
                      - type: 'null'
                    title: Email
                    description: User's email address
              github_user_id:
                allOf:
                  - type: string
                    title: Github User Id
                    description: GitHub user ID
              github_username:
                allOf:
                  - type: string
                    title: Github Username
                    description: GitHub username
              avatar_url:
                allOf:
                  - anyOf:
                      - type: string
                      - type: 'null'
                    title: Avatar Url
                    description: URL to user's avatar image
              full_name:
                allOf:
                  - anyOf:
                      - type: string
                      - type: 'null'
                    title: Full Name
                    description: User's full name
              role:
                allOf:
                  - anyOf:
                      - type: string
                      - type: 'null'
                    title: Role
                    description: User's role in the organization (ADMIN, MANAGER, MEMBER)
              is_admin:
                allOf:
                  - anyOf:
                      - type: boolean
                      - type: 'null'
                    title: Is Admin
                    description: >-
                      Whether the user is an admin (deprecated, use role
                      instead)
            title: UserResponse
            description: Represents a user in API responses
            refIdentifier: '#/components/schemas/UserResponse'
            requiredProperties:
              - id
              - github_user_id
              - github_username
        examples:
          example:
            value:
              id: 123
              email: <string>
              github_user_id: <string>
              github_username: <string>
              avatar_url: <string>
              full_name: <string>
              role: <string>
              is_admin: true
        description: Successful Response
    '403':
      application/json:
        schemaArray:
          - type: object
            properties:
              message:
                allOf:
                  - type: string
                    title: Message
                    default: You do not have access to this organization.
              status_code:
                allOf:
                  - type: integer
                    title: Status Code
                    default: 403
            title: PermissionsErrorResponse
            refIdentifier: '#/components/schemas/PermissionsErrorResponse'
        examples:
          example:
            value:
              message: You do not have access to this organization.
              status_code: 403
        description: Forbidden
    '404':
      application/json:
        schemaArray:
          - type: object
            properties:
              message:
                allOf:
                  - type: string
                    title: Message
                    default: User not found.
              status_code:
                allOf:
                  - type: integer
                    title: Status Code
                    default: 404
            title: UserNotFoundErrorResponse
            refIdentifier: '#/components/schemas/UserNotFoundErrorResponse'
        examples:
          example:
            value:
              message: User not found.
              status_code: 404
        description: Not Found
    '422':
      application/json:
        schemaArray:
          - type: object
            properties:
              detail:
                allOf:
                  - items:
                      $ref: '#/components/schemas/ValidationError'
                    type: array
                    title: Detail
            title: HTTPValidationError
            refIdentifier: '#/components/schemas/HTTPValidationError'
        examples:
          example:
            value:
              detail:
                - loc:
                    - <string>
                  msg: <string>
                  type: <string>
        description: Validation Error
    '429':
      application/json:
        schemaArray:
          - type: object
            properties:
              message:
                allOf:
                  - type: string
                    title: Message
                    default: Rate limit exceeded. Please try again later.
              status_code:
                allOf:
                  - type: integer
                    title: Status Code
                    default: 429
            title: APIRateLimitErrorResponse
            refIdentifier: '#/components/schemas/APIRateLimitErrorResponse'
        examples:
          example:
            value:
              message: Rate limit exceeded. Please try again later.
              status_code: 429
        description: Too Many Requests
  deprecated: false
  type: path
components:
  schemas:
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          title: Location
        msg:
          type: string
          title: Message
        type:
          type: string
          title: Error Type
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError

````