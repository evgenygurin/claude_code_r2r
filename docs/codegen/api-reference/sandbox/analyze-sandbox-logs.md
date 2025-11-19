# Analyze Sandbox Logs

> Analyze sandbox setup logs using an AI agent.

This endpoint creates an AI agent that will analyze the setup logs from a sandbox,
identify any errors, provide insights about what went wrong, and suggest potential
solutions. The analysis runs asynchronously and results can be retrieved using the
returned agent run ID.

Rate limit: 5 requests per minute.

## OpenAPI

````yaml api-reference/openapi3.json post /v1/organizations/{org_id}/sandbox/{sandbox_id}/analyze-logs
paths:
  path: /v1/organizations/{org_id}/sandbox/{sandbox_id}/analyze-logs
  method: post
  servers:
    - url: https://api.codegen.com
      description: Codegen API
  request:
    security: []
    parameters:
      path:
        sandbox_id:
          schema:
            - type: integer
              required: true
              title: Sandbox Id
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
              agent_run_id:
                allOf:
                  - type: integer
                    title: Agent Run Id
                    description: The ID of the agent run analyzing the logs
              status:
                allOf:
                  - type: string
                    title: Status
                    description: The status of the agent run
              message:
                allOf:
                  - type: string
                    title: Message
                    description: Information about the analysis process
            title: AnalyzeLogsResponse
            refIdentifier: '#/components/schemas/AnalyzeLogsResponse'
            requiredProperties:
              - agent_run_id
              - status
              - message
        examples:
          example:
            value:
              agent_run_id: 123
              status: <string>
              message: <string>
        description: Successful Response
    '400':
      _mintlify/placeholder:
        schemaArray:
          - type: any
            description: No logs available for analysis
        examples: {}
        description: No logs available for analysis
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
      _mintlify/placeholder:
        schemaArray:
          - type: any
            description: Sandbox not found
        examples: {}
        description: Sandbox not found
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