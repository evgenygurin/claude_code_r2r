# Get Users

> Get users for the specified organization.

Returns a paginated list of all users that belong to the specified organization.
Results include user details such as name, email, GitHub username, and avatar.
Use pagination parameters to control the number of results returned.

Rate limit: 60 requests per 30 seconds.

## OpenAPI

````yaml api-reference/openapi3.json get /v1/organizations/{org_id}/users
paths:
  path: /v1/organizations/{org_id}/users
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
      query:
        skip:
          schema:
            - type: integer
              required: false
              title: Skip
              minimum: 0
              default: 0
        limit:
          schema:
            - type: integer
              required: false
              title: Limit
              maximum: 100
              minimum: 1
              default: 100
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
              items:
                allOf:
                  - items:
                      $ref: '#/components/schemas/UserResponse'
                    type: array
                    title: Items
              total:
                allOf:
                  - type: integer
                    title: Total
              page:
                allOf:
                  - type: integer
                    title: Page
              size:
                allOf:
                  - type: integer
                    title: Size
              pages:
                allOf:
                  - type: integer
                    title: Pages
            title: Page[UserResponse]
            refIdentifier: '#/components/schemas/Page_UserResponse_'
            requiredProperties:
              - items
              - total
              - page
              - size
              - pages
        examples:
          example:
            value:
              items:
                - id: 123
                  email: <string>
                  github_user_id: <string>
                  github_username: <string>
                  avatar_url: <string>
                  full_name: <string>
                  role: <string>
                  is_admin: true
              total: 123
              page: 123
              size: 123
              pages: 123
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
    UserResponse:
      properties:
        id:
          type: integer
          title: Id
          description: Unique user ID
        email:
          anyOf:
            - type: string
            - type: 'null'
          title: Email
          description: User's email address
        github_user_id:
          type: string
          title: Github User Id
          description: GitHub user ID
        github_username:
          type: string
          title: Github Username
          description: GitHub username
        avatar_url:
          anyOf:
            - type: string
            - type: 'null'
          title: Avatar Url
          description: URL to user's avatar image
        full_name:
          anyOf:
            - type: string
            - type: 'null'
          title: Full Name
          description: User's full name
        role:
          anyOf:
            - type: string
            - type: 'null'
          title: Role
          description: User's role in the organization (ADMIN, MANAGER, MEMBER)
        is_admin:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Is Admin
          description: Whether the user is an admin (deprecated, use role instead)
      type: object
      required:
        - id
        - github_user_id
        - github_username
      title: UserResponse
      description: Represents a user in API responses
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