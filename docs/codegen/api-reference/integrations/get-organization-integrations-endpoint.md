# Get Organization Integrations Endpoint

> Get all integration statuses for the given organization.

Returns a comprehensive overview of all integrations configured for the organization,
including:
- OAuth-based integrations (Slack, Linear, Notion, Figma, ClickUp, Jira, Sentry, Monday.com)
- GitHub app installations
- API key-based integrations (CircleCI)
- Database connections (PostgreSQL)

Each integration includes its current status (active/inactive), associated token/installation IDs,
and relevant metadata such as app names, organization names, etc.

Rate limit: 60 requests per 30 seconds.

## OpenAPI

````yaml api-reference/openapi3.json get /v1/organizations/{org_id}/integrations
paths:
  path: /v1/organizations/{org_id}/integrations
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
              organization_id:
                allOf:
                  - type: integer
                    title: Organization Id
                    description: ID of the organization
              organization_name:
                allOf:
                  - type: string
                    title: Organization Name
                    description: Name of the organization
              integrations:
                allOf:
                  - items:
                      $ref: '#/components/schemas/IntegrationStatus'
                    type: array
                    title: Integrations
                    description: List of integration statuses
              total_active_integrations:
                allOf:
                  - type: integer
                    title: Total Active Integrations
                    description: Total number of active integrations
            title: OrganizationIntegrationsResponse
            description: Response schema for organization integrations.
            refIdentifier: '#/components/schemas/OrganizationIntegrationsResponse'
            requiredProperties:
              - organization_id
              - organization_name
              - integrations
              - total_active_integrations
        examples:
          example:
            value:
              organization_id: 123
              organization_name: <string>
              integrations:
                - integration_type: <string>
                  active: true
                  token_id: 123
                  installation_id: 123
                  metadata: {}
              total_active_integrations: 123
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
    IntegrationStatus:
      properties:
        integration_type:
          type: string
          title: Integration Type
          description: Type of integration (e.g., 'github', 'slack', 'linear', etc.)
        active:
          type: boolean
          title: Active
          description: Whether the integration is currently active
        token_id:
          anyOf:
            - type: integer
            - type: 'null'
          title: Token Id
          description: ID of the associated token, if any
        installation_id:
          anyOf:
            - type: integer
            - type: 'null'
          title: Installation Id
          description: ID of the app installation, if applicable
        metadata:
          anyOf:
            - additionalProperties: true
              type: object
            - type: 'null'
          title: Metadata
          description: Additional metadata about the integration
      type: object
      required:
        - integration_type
        - active
      title: IntegrationStatus
      description: Status information for a single integration.
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