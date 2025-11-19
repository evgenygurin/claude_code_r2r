# Get Cli Rules

> Get organization and user rules for CLI applications.

This endpoint is designed for CLI applications that need to fetch both organization-specific
rules and user-specific custom prompts that are used in prompts. This includes:

- Organization rules: Same as MCP organization_rules prompt and agent prompt builders
- User custom prompt: Same as MCP user_custom_prompt and agent prompt builders

Returns the rules and prompts that should be followed by AI agents.

Rate limit: 30 requests per minute.

## OpenAPI

````yaml api-reference/openapi3.json get /v1/organizations/{org_id}/cli/rules
paths:
  path: /v1/organizations/{org_id}/cli/rules
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
              organization_rules:
                allOf:
                  - anyOf:
                      - type: string
                      - type: 'null'
                    title: Organization Rules
              user_custom_prompt:
                allOf:
                  - anyOf:
                      - type: string
                      - type: 'null'
                    title: User Custom Prompt
            title: CLIRulesResponse
            description: >-
              Response model for CLI rules containing organization and user
              rules.
            refIdentifier: '#/components/schemas/CLIRulesResponse'
            requiredProperties:
              - organization_rules
              - user_custom_prompt
        examples:
          example:
            value:
              organization_rules: <string>
              user_custom_prompt: <string>
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