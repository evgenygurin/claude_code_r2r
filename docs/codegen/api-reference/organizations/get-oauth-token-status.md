# Get Oauth Token Status

> Get list of providers that have active OAuth tokens for the current user and organization.

Returns a list of provider names that are connected.

## OpenAPI

````yaml api-reference/openapi3.json get /v1/oauth/tokens/status
paths:
  path: /v1/oauth/tokens/status
  method: get
  servers:
    - url: https://api.codegen.com
      description: Codegen API
  request:
    security: []
    parameters:
      path: {}
      query:
        org_id:
          schema:
            - type: integer
              required: true
              title: Org Id
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
          - type: any
        examples:
          example:
            value: <any>
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