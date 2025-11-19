# Generate Slack Connect Token Endpoint

> Generate a temporary token for Slack account connection.

This token:
- Expires in 10 minutes
- Can only be used once
- Must be sent to the Codegen bot in a DM with format: "Connect my account: {token}"

## OpenAPI

````yaml api-reference/openapi3.json post /v1/slack-connect/generate-token
paths:
  path: /v1/slack-connect/generate-token
  method: post
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
    body:
      application/json:
        schemaArray:
          - type: object
            properties:
              org_id:
                allOf:
                  - type: integer
                    title: Org Id
            required: true
            title: GenerateTokenRequest
            refIdentifier: '#/components/schemas/GenerateTokenRequest'
            requiredProperties:
              - org_id
        examples:
          example:
            value:
              org_id: 123
  response:
    '200':
      application/json:
        schemaArray:
          - type: object
            properties:
              token:
                allOf:
                  - type: string
                    title: Token
              message:
                allOf:
                  - type: string
                    title: Message
              expires_in_minutes:
                allOf:
                  - type: integer
                    title: Expires In Minutes
            title: GenerateTokenResponse
            refIdentifier: '#/components/schemas/GenerateTokenResponse'
            requiredProperties:
              - token
              - message
              - expires_in_minutes
        examples:
          example:
            value:
              token: <string>
              message: <string>
              expires_in_minutes: 123
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