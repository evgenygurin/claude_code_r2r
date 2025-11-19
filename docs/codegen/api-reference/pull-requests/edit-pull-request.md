# Edit Pull Request

> Edit pull request properties (RESTful endpoint).

Update the state of a pull request (open, closed, draft, ready_for_review).
This endpoint requires both repo_id and pr_id for RESTful compliance.
The requesting user must have write permissions to the repository.

Rate limit: 30 requests per minute.

## OpenAPI

````yaml api-reference/openapi3.json patch /v1/organizations/{org_id}/repos/{repo_id}/prs/{pr_id}
paths:
  path: /v1/organizations/{org_id}/repos/{repo_id}/prs/{pr_id}
  method: patch
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
        repo_id:
          schema:
            - type: integer
              required: true
              title: Repo Id
        pr_id:
          schema:
            - type: integer
              required: true
              title: Pr Id
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
              state:
                allOf:
                  - type: string
                    enum:
                      - open
                      - closed
                      - draft
                      - ready_for_review
                    title: State
            required: true
            title: EditPRInput
            description: Input for editing PR properties.
            refIdentifier: '#/components/schemas/EditPRInput'
            requiredProperties:
              - state
        examples:
          example:
            value:
              state: open
  response:
    '200':
      application/json:
        schemaArray:
          - type: object
            properties:
              success:
                allOf:
                  - type: boolean
                    title: Success
              url:
                allOf:
                  - anyOf:
                      - type: string
                      - type: 'null'
                    title: Url
              number:
                allOf:
                  - anyOf:
                      - type: integer
                      - type: 'null'
                    title: Number
              title:
                allOf:
                  - anyOf:
                      - type: string
                      - type: 'null'
                    title: Title
              state:
                allOf:
                  - anyOf:
                      - type: string
                      - type: 'null'
                    title: State
              error:
                allOf:
                  - anyOf:
                      - type: string
                      - type: 'null'
                    title: Error
            title: EditPRResponse
            description: Response from editing PR properties.
            refIdentifier: '#/components/schemas/EditPRResponse'
            requiredProperties:
              - success
        examples:
          example:
            value:
              success: true
              url: <string>
              number: 123
              title: <string>
              state: <string>
              error: <string>
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