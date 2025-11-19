# Generate Setup Commands

> Generate setup commands for a repository.

Creates and initiates a setup command generation agent for the specified repository.
The agent will analyze the repository structure and generate appropriate setup commands.

Rate limit: 5 requests per minute.

## OpenAPI

````yaml api-reference/openapi3.json post /v1/organizations/{org_id}/setup-commands/generate
paths:
  path: /v1/organizations/{org_id}/setup-commands/generate
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
              repo_id:
                allOf:
                  - type: integer
                    title: Repo Id
              prompt:
                allOf:
                  - anyOf:
                      - type: string
                      - type: 'null'
                    title: Prompt
              trigger_source:
                allOf:
                  - type: string
                    title: Trigger Source
                    default: setup-commands
            required: true
            title: GenerateSetupCommandsInput
            description: Input for generating setup commands.
            refIdentifier: '#/components/schemas/GenerateSetupCommandsInput'
            requiredProperties:
              - repo_id
        examples:
          example:
            value:
              repo_id: 123
              prompt: <string>
              trigger_source: setup-commands
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
              status:
                allOf:
                  - type: string
                    title: Status
              url:
                allOf:
                  - type: string
                    title: Url
            title: SetupCommandsResponse
            description: Response for setup commands generation.
            refIdentifier: '#/components/schemas/SetupCommandsResponse'
            requiredProperties:
              - agent_run_id
              - status
              - url
        examples:
          example:
            value:
              agent_run_id: 123
              status: <string>
              url: <string>
        description: Successful Response
    '400':
      _mintlify/placeholder:
        schemaArray:
          - type: any
            description: Invalid input
        examples: {}
        description: Invalid input
    '404':
      _mintlify/placeholder:
        schemaArray:
          - type: any
            description: Repository not found
        examples: {}
        description: Repository not found
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
    '500':
      _mintlify/placeholder:
        schemaArray:
          - type: any
            description: Internal server error
        examples: {}
        description: Internal server error
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