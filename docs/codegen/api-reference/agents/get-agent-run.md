# Get Agent Run

> Retrieve the status and result of an agent run.

Returns the current status, progress, and any available results for the specified agent run.
The agent run must belong to the specified organization. If the agent run is still in progress,
this endpoint can be polled to check for completion.

Rate limit: 60 requests per 30 seconds.

## OpenAPI

````yaml api-reference/openapi3.json get /v1/organizations/{org_id}/agent/run/{agent_run_id}
paths:
  path: /v1/organizations/{org_id}/agent/run/{agent_run_id}
  method: get
  servers:
    - url: https://api.codegen.com
      description: Codegen API
  request:
    security: []
    parameters:
      path:
        agent_run_id:
          schema:
            - type: integer
              required: true
              title: Agent Run Id
        org_id:
          schema:
            - type: integer
              required: true
              title: Org Id
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
              organization_id:
                allOf:
                  - type: integer
                    title: Organization Id
              status:
                allOf:
                  - anyOf:
                      - type: string
                      - type: 'null'
                    title: Status
              created_at:
                allOf:
                  - anyOf:
                      - type: string
                      - type: 'null'
                    title: Created At
              web_url:
                allOf:
                  - anyOf:
                      - type: string
                      - type: 'null'
                    title: Web Url
              result:
                allOf:
                  - anyOf:
                      - type: string
                      - type: 'null'
                    title: Result
              summary:
                allOf:
                  - anyOf:
                      - type: string
                      - type: 'null'
                    title: Summary
              source_type:
                allOf:
                  - anyOf:
                      - $ref: '#/components/schemas/ApiAgentRunSourceType'
                      - type: 'null'
              github_pull_requests:
                allOf:
                  - anyOf:
                      - items:
                          $ref: '#/components/schemas/GithubPullRequestResponse'
                        type: array
                      - type: 'null'
                    title: Github Pull Requests
              metadata:
                allOf:
                  - anyOf:
                      - additionalProperties: true
                        type: object
                      - type: 'null'
                    title: Metadata
            title: AgentRunResponse
            description: Represents an agent run in API responses
            refIdentifier: '#/components/schemas/AgentRunResponse'
            requiredProperties:
              - id
              - organization_id
        examples:
          example:
            value:
              id: 123
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
                    default: Agent run not found.
              status_code:
                allOf:
                  - type: integer
                    title: Status Code
                    default: 404
            title: AgentRunNotFoundErrorResponse
            refIdentifier: '#/components/schemas/AgentRunNotFoundErrorResponse'
        examples:
          example:
            value:
              message: Agent run not found.
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