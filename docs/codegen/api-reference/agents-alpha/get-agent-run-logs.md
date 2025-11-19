# Get Agent Run Logs

> Retrieve an agent run with its logs using pagination. This endpoint is currently in ALPHA and IS subject to change.

Returns the agent run details along with a paginated list of logs for the specified agent run.
The agent run must belong to the specified organization. Logs are returned in chronological order.
Uses standard pagination parameters (skip and limit) and includes pagination metadata in the response.

Rate limit: 60 requests per 60 seconds.

## OpenAPI

````yaml api-reference/openapi3.json get /v1/alpha/organizations/{org_id}/agent/run/{agent_run_id}/logs
paths:
  path: /v1/alpha/organizations/{org_id}/agent/run/{agent_run_id}/logs
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
        reverse:
          schema:
            - type: boolean
              required: false
              title: Reverse
              default: false
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
              metadata:
                allOf:
                  - anyOf:
                      - additionalProperties: true
                        type: object
                      - type: 'null'
                    title: Metadata
              logs:
                allOf:
                  - items:
                      $ref: '#/components/schemas/AgentRunLogResponse'
                    type: array
                    title: Logs
              total_logs:
                allOf:
                  - anyOf:
                      - type: integer
                      - type: 'null'
                    title: Total Logs
              page:
                allOf:
                  - anyOf:
                      - type: integer
                      - type: 'null'
                    title: Page
              size:
                allOf:
                  - anyOf:
                      - type: integer
                      - type: 'null'
                    title: Size
              pages:
                allOf:
                  - anyOf:
                      - type: integer
                      - type: 'null'
                    title: Pages
            title: AgentRunWithLogsResponse
            description: Represents an agent run in API responses
            refIdentifier: '#/components/schemas/AgentRunWithLogsResponse'
            requiredProperties:
              - id
              - organization_id
              - logs
        examples:
          example:
            value:
              id: 123
              organization_id: 123
              status: <string>
              created_at: <string>
              web_url: <string>
              result: <string>
              metadata: {}
              logs:
                - agent_run_id: 123
                  created_at: <string>
                  tool_name: <string>
                  message_type: <string>
                  thought: <string>
                  observation: {}
                  tool_input: {}
                  tool_output: {}
              total_logs: 123
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
    AgentRunLogResponse:
      properties:
        agent_run_id:
          type: integer
          title: Agent Run Id
        created_at:
          anyOf:
            - type: string
            - type: 'null'
          title: Created At
        tool_name:
          anyOf:
            - type: string
            - type: 'null'
          title: Tool Name
        message_type:
          anyOf:
            - type: string
            - type: 'null'
          title: Message Type
        thought:
          anyOf:
            - type: string
            - type: 'null'
          title: Thought
        observation:
          anyOf:
            - additionalProperties: true
              type: object
            - type: string
            - type: 'null'
          title: Observation
        tool_input:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Tool Input
        tool_output:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Tool Output
      type: object
      required:
        - agent_run_id
      title: AgentRunLogResponse
      description: Represents an agent run log in API responses
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