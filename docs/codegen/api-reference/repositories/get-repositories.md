# Get Repositories

> Get repositories for the specified organization.

Returns a paginated list of all repositories that belong to the specified organization.
Results include repository details such as name, ID, description, visibility, and setup status.
Use pagination parameters to control the number of results returned.

Rate limit: 60 requests per 30 seconds.

## OpenAPI

````yaml api-reference/openapi3.json get /v1/organizations/{org_id}/repos
paths:
  path: /v1/organizations/{org_id}/repos
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
                      $ref: '#/components/schemas/RepoResponse'
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
            title: Page[RepoResponse]
            refIdentifier: '#/components/schemas/Page_RepoResponse_'
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
                  name: <string>
                  full_name: <string>
                  description: <string>
                  github_id: <string>
                  organization_id: 123
                  visibility: <string>
                  archived: true
                  setup_status: <string>
                  language: <string>
              total: 123
              page: 123
              size: 123
              pages: 123
        description: Successful Response
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
    RepoResponse:
      properties:
        id:
          type: integer
          title: Id
        name:
          type: string
          title: Name
        full_name:
          type: string
          title: Full Name
        description:
          anyOf:
            - type: string
            - type: 'null'
          title: Description
        github_id:
          type: string
          title: Github Id
        organization_id:
          type: integer
          title: Organization Id
        visibility:
          anyOf:
            - type: string
            - type: 'null'
          title: Visibility
        archived:
          anyOf:
            - type: boolean
            - type: 'null'
          title: Archived
        setup_status:
          type: string
          title: Setup Status
        language:
          anyOf:
            - type: string
            - type: 'null'
          title: Language
      type: object
      required:
        - id
        - name
        - full_name
        - description
        - github_id
        - organization_id
        - visibility
        - archived
        - setup_status
        - language
      title: RepoResponse
      description: Represents a repository in API responses
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