# Get Check Suite Settings

> Get check suite settings for a repository.

## OpenAPI

````yaml api-reference/openapi3.json get /v1/organizations/{org_id}/repos/check-suite-settings
paths:
  path: /v1/organizations/{org_id}/repos/check-suite-settings
  method: get
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
    body: {}
  response:
    '200':
      application/json:
        schemaArray:
          - type: object
            properties:
              check_retry_count:
                allOf:
                  - type: integer
                    title: Check Retry Count
              ignored_checks:
                allOf:
                  - items:
                      type: string
                    type: array
                    title: Ignored Checks
              check_retry_counts:
                allOf:
                  - additionalProperties:
                      type: integer
                    type: object
                    title: Check Retry Counts
              custom_prompts:
                allOf:
                  - additionalProperties:
                      type: string
                    type: object
                    title: Custom Prompts
              high_priority_apps:
                allOf:
                  - items:
                      type: string
                    type: array
                    title: High Priority Apps
              available_check_suite_names:
                allOf:
                  - items:
                      type: string
                    type: array
                    title: Available Check Suite Names
            title: CheckSuiteSettingsResponse
            description: Response model for check suite settings.
            refIdentifier: '#/components/schemas/CheckSuiteSettingsResponse'
            requiredProperties:
              - check_retry_count
              - ignored_checks
              - check_retry_counts
              - custom_prompts
              - high_priority_apps
              - available_check_suite_names
        examples:
          example:
            value:
              check_retry_count: 123
              ignored_checks:
                - <string>
              check_retry_counts: {}
              custom_prompts: {}
              high_priority_apps:
                - <string>
              available_check_suite_names:
                - <string>
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