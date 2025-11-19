# Get Organizations

> Get organizations for the authenticated user.

Returns a paginated list of all organizations that the authenticated user is a member of.
Results include basic organization details such as name, ID, and membership information.
Use pagination parameters to control the number of results returned.

Rate limit: 60 requests per 30 seconds.

## OpenAPI

````yaml api-reference/openapi3.json get /v1/organizations
paths:
  path: /v1/organizations
  method: get
  servers:
    - url: https://api.codegen.com
      description: Codegen API
  request:
    security: []
    parameters:
      path: {}
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
                      $ref: '#/components/schemas/OrganizationResponse'
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
            title: Page[OrganizationResponse]
            refIdentifier: '#/components/schemas/Page_OrganizationResponse_'
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
                  settings:
                    enable_pr_creation: true
                    enable_rules_detection: true
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
    OrganizationResponse:
      properties:
        id:
          type: integer
          title: Id
        name:
          type: string
          title: Name
        settings:
          $ref: '#/components/schemas/OrganizationSettings'
      type: object
      required:
        - id
        - name
        - settings
      title: OrganizationResponse
      description: Represents an organization in API responses
    OrganizationSettings:
      properties:
        enable_pr_creation:
          type: boolean
          title: Enable Pr Creation
          default: true
        enable_rules_detection:
          type: boolean
          title: Enable Rules Detection
          default: true
      type: object
      title: OrganizationSettings
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