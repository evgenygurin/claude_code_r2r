# List Agent Runs

> List agent runs for an organization with optional user filtering.

Returns a paginated list of agent runs for the specified organization.
Optionally filter by user_id to get only agent runs initiated by a specific user.
Results are ordered by creation date (newest first).

Rate limit: 60 requests per 30 seconds.

## OpenAPI

````yaml api-reference/openapi3.json get /v1/organizations/{org_id}/agent/runs
paths:
  path: /v1/organizations/{org_id}/agent/runs
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
        user_id:
          schema:
            - type: integer
              required: false
              title: User Id
              description: Filter by user ID who initiated the agent runs
            - type: 'null'
              required: false
              title: User Id
              description: Filter by user ID who initiated the agent runs
        source_type:
          schema:
            - type: enum<string>
              enum:
                - LOCAL
                - SLACK
                - GITHUB
                - GITHUB_CHECK_SUITE
                - GITHUB_PR_REVIEW
                - LINEAR
                - API
                - CHAT
                - JIRA
                - CLICKUP
                - MONDAY
                - SETUP_COMMANDS
              required: false
              title: ApiAgentRunSourceType
              description: Filter by source type of the agent runs
              refIdentifier: '#/components/schemas/ApiAgentRunSourceType'
            - type: 'null'
              required: false
              title: Source Type
              description: Filter by source type of the agent runs
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
                      $ref: '#/components/schemas/AgentRunResponse'
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
            title: Page[AgentRunResponse]
            refIdentifier: '#/components/schemas/Page_AgentRunResponse_'
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
                  organization_id: 123
                  status: <string>
                  created_at: <string>
                  web_url: <string>
                  result: <string>
                  summary: <string>
                  source_type: LOCAL
                  github_pull_requests:
                    - id: 123
                      title: <string>
                      url: <string>
                      created_at: <string>
                      head_branch_name: <string>
                  metadata: {}
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
    AgentRunResponse:
      properties:
        id:
          type: integer
          title: Id
        organization_id:
          type: integer
          title: Organization Id
        status:
          anyOf:
            - type: string
            - type: 'null'
          title: Status
        created_at:
          anyOf:
            - type: string
            - type: 'null'
          title: Created At
        web_url:
          anyOf:
            - type: string
            - type: 'null'
          title: Web Url
        result:
          anyOf:
            - type: string
            - type: 'null'
          title: Result
        summary:
          anyOf:
            - type: string
            - type: 'null'
          title: Summary
        source_type:
          anyOf:
            - $ref: '#/components/schemas/ApiAgentRunSourceType'
            - type: 'null'
        github_pull_requests:
          anyOf:
            - items:
                $ref: '#/components/schemas/GithubPullRequestResponse'
              type: array
            - type: 'null'
          title: Github Pull Requests
        metadata:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Metadata
      type: object
      required:
        - id
        - organization_id
      title: AgentRunResponse
      description: Represents an agent run in API responses
    ApiAgentRunSourceType:
      type: string
      enum:
        - LOCAL
        - SLACK
        - GITHUB
        - GITHUB_CHECK_SUITE
        - GITHUB_PR_REVIEW
        - LINEAR
        - API
        - CHAT
        - JIRA
        - CLICKUP
        - MONDAY
        - SETUP_COMMANDS
      title: ApiAgentRunSourceType
    GithubPullRequestResponse:
      properties:
        id:
          type: integer
          title: Id
        title:
          anyOf:
            - type: string
            - type: 'null'
          title: Title
        url:
          anyOf:
            - type: string
            - type: 'null'
          title: Url
        created_at:
          type: string
          title: Created At
        head_branch_name:
          anyOf:
            - type: string
            - type: 'null'
          title: Head Branch Name
      type: object
      required:
        - id
        - created_at
      title: GithubPullRequestResponse
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