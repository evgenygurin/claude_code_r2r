# Remove Codegen From Pr

> Remove Codegen from a PR.

This endpoint performs the same action as banning all checks but with more user-friendly naming.
It:
1. Flags the PR to prevent future CI/CD check suite events from being processed
2. Stops all current agents for that PR

## OpenAPI

````yaml api-reference/openapi3.json post /v1/organizations/{org_id}/agent/run/remove-from-pr
paths:
  path: /v1/organizations/{org_id}/agent/run/remove-from-pr
  method: post
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
      query: {}
      header:
        authorization:
          schema:
            - type: any
              required: false
              title: Authorization
      cookie: {}
    body:
      application/json:
        schemaArray:
          - type: object
            properties:
              agent_run_id:
                allOf:
                  - type: integer
                    title: Agent Run Id
              before_card_order_id:
                allOf:
                  - anyOf:
                      - type: string
                      - type: 'null'
                    title: Before Card Order Id
                    description: >-
                      Kanban order key of the card that should come before this
                      agent run in the CANCELLED column
              after_card_order_id:
                allOf:
                  - anyOf:
                      - type: string
                      - type: 'null'
                    title: After Card Order Id
                    description: >-
                      Kanban order key of the card that should come after this
                      agent run in the CANCELLED column
            required: true
            title: StopAgentRunInput
            refIdentifier: '#/components/schemas/StopAgentRunInput'
            requiredProperties:
              - agent_run_id
        examples:
          example:
            value:
              agent_run_id: 123
              before_card_order_id: <string>
              after_card_order_id: <string>
  response:
    '200':
      application/json:
        schemaArray:
          - type: any
        examples:
          example:
            value: <any>
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