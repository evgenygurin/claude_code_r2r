# Update Check Suite Settings

> Update check suite settings for a repository.

## OpenAPI

````yaml api-reference/openapi3.json put /v1/organizations/{org_id}/repos/check-suite-settings
paths:
  path: /v1/organizations/{org_id}/repos/check-suite-settings
  method: put
  servers:
    - url: https://api.codegen.com
      description: Codegen API
  request:
    security: []
    parameters:
      path: {}
      query:
        repo_id:
          schema:
            - type: integer
              required: true
              title: Repo Id
              description: Repository ID
      header: {}
      cookie: {}
    body:
      application/json:
        schemaArray:
          - type: object
            properties:
              check_retry_count:
                allOf:
                  - anyOf:
                      - type: integer
                        maximum: 10
                        minimum: 0
                      - type: 'null'
                    title: Check Retry Count
                    description: Global retry count for failed checks
              ignored_checks:
                allOf:
                  - anyOf:
                      - items:
                          type: string
                        type: array
                      - type: 'null'
                    title: Ignored Checks
                    description: List of check names to ignore
              check_retry_counts:
                allOf:
                  - anyOf:
                      - additionalProperties:
                          type: integer
                        type: object
                      - type: 'null'
                    title: Check Retry Counts
                    description: Per-check retry counts
              custom_prompts:
                allOf:
                  - anyOf:
                      - additionalProperties:
                          type: string
                        type: object
                      - type: 'null'
                    title: Custom Prompts
                    description: Custom prompts per check
              high_priority_apps:
                allOf:
                  - anyOf:
                      - items:
                          type: string
                        type: array
                      - type: 'null'
                    title: High Priority Apps
                    description: Apps that trigger immediate processing on failure
            required: true
            title: CheckSuiteSettingsRequest
            description: Request model for updating check suite settings.
            refIdentifier: '#/components/schemas/CheckSuiteSettingsRequest'
        examples:
          example:
            value:
              check_retry_count: 5
              ignored_checks:
                - <string>
              check_retry_counts: {}
              custom_prompts: {}
              high_priority_apps:
                - <string>
  response:
    '200':
      application/json:
        schemaArray:
          - type: object
            properties: {}
            title: >-
              Response Update Check Suite Settings V1 Organizations  Org Id 
              Repos Check Suite Settings Put
        examples:
          example:
            value: {}
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