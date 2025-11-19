# Get Mcp Providers

> Get all MCP providers from oauth_providers table.

Returns only providers with is_mcp=True.

## OpenAPI

````yaml api-reference/openapi3.json get /v1/mcp-providers
paths:
  path: /v1/mcp-providers
  method: get
  servers:
    - url: https://api.codegen.com
      description: Codegen API
  request:
    security: []
    parameters:
      path: {}
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
          - type: array
            items:
              allOf:
                - $ref: '#/components/schemas/OAuthProviderResponse'
            title: Response Get Mcp Providers V1 Mcp Providers Get
        examples:
          example:
            value:
              - id: 123
                name: <string>
                issuer: <string>
                authorization_endpoint: <string>
                token_endpoint: <string>
                default_scopes:
                  - <string>
                is_mcp: true
                meta: {}
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
  deprecated: false
  type: path
components:
  schemas:
    OAuthProviderResponse:
      properties:
        id:
          type: integer
          title: Id
        name:
          type: string
          title: Name
        issuer:
          type: string
          title: Issuer
        authorization_endpoint:
          type: string
          title: Authorization Endpoint
        token_endpoint:
          type: string
          title: Token Endpoint
        default_scopes:
          anyOf:
            - items:
                type: string
              type: array
            - type: 'null'
          title: Default Scopes
        is_mcp:
          type: boolean
          title: Is Mcp
        meta:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Meta
      type: object
      required:
        - id
        - name
        - issuer
        - authorization_endpoint
        - token_endpoint
        - default_scopes
        - is_mcp
      title: OAuthProviderResponse
      description: Response model for OAuth provider data.
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