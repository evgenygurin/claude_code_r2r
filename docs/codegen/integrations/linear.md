# Linear Integration

Linear is designed to orchestrate teams of humans and agents working together. It's the most efficient way to track progress and scale teams of agents to tackle large, complex tasks. Codegen can take a first pass at virtually any issue, breaking down work and making meaningful progress before human review. We recommend letting Codegen handle the initial exploration and implementation of most tasks.

<img src="https://mintcdn.com/codegeninc/TEOdIY76pi_ZHrje/images/linear.png?fit=max&auto=format&n=TEOdIY76pi_ZHrje&q=85&s=e3fd8f2979967068f89e392659015b65" className="rounded-lg" data-og-width="2676" width="2676" data-og-height="1658" height="1658" data-path="images/linear.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/codegeninc/TEOdIY76pi_ZHrje/images/linear.png?w=280&fit=max&auto=format&n=TEOdIY76pi_ZHrje&q=85&s=84587f3b89dbe51c08bc77c4fdf31051 280w, https://mintcdn.com/codegeninc/TEOdIY76pi_ZHrje/images/linear.png?w=560&fit=max&auto=format&n=TEOdIY76pi_ZHrje&q=85&s=475134d7f224c07d139583b9b7a4df50 560w, https://mintcdn.com/codegeninc/TEOdIY76pi_ZHrje/images/linear.png?w=840&fit=max&auto=format&n=TEOdIY76pi_ZHrje&q=85&s=26167b040f786b245ab177aaf4313690 840w, https://mintcdn.com/codegeninc/TEOdIY76pi_ZHrje/images/linear.png?w=1100&fit=max&auto=format&n=TEOdIY76pi_ZHrje&q=85&s=165ffc374977ba12f03b955c4fa425aa 1100w, https://mintcdn.com/codegeninc/TEOdIY76pi_ZHrje/images/linear.png?w=1650&fit=max&auto=format&n=TEOdIY76pi_ZHrje&q=85&s=d7ca01f1f252baa78654df9ee08a0f76 1650w, https://mintcdn.com/codegeninc/TEOdIY76pi_ZHrje/images/linear.png?w=2500&fit=max&auto=format&n=TEOdIY76pi_ZHrje&q=85&s=2a2127ca00104ba5890f83eb7b68b36b 2500w" />

## Installation

Connect your Linear workspace to Codegen to enable agent interactions.

<Card title="Connect Linear Workspace" icon="moon" href="https://linear.app/integrations/codegen">
  Authorize Codegen to access your Linear workspace via the API settings.
</Card>

<Note>
  API access allows agents to interact with issues and projects according to
  your permissions in Linear.
</Note>

## Capabilities

The Linear integration provides comprehensive project management capabilities:

* **Create and update issues automatically** - Generate new tasks and update existing ones based on development needs
* **Track development progress** - Monitor and report on the status of ongoing work
* **Link code changes to tickets** - Connect GitHub pull requests and commits directly to Linear issues
* **Sync status updates** - Keep issue statuses current as work progresses through different stages
* **Multi Agent Systems:** Create sub-issues and assign child agents to break down complex tasks into manageable pieces. [Learn more](#multi-agent-systems).

## Permissions

The Codegen Linear integration requires the following permissions:

* **Create issues for your workspace** - Generate new tasks and tickets as needed
* **Create issue comments and discussions** - Provide updates, ask questions, and facilitate collaboration
* **Read access to your workspace data** - Access existing issues, projects, and team information
* **Write access to update issues and projects** - Modify issue status, assignees, and project details
* **Assign issues and projects to teams** - Route work to appropriate team members
* **Mention app in issues and documents** - Enable notifications and cross-references
* **Receive realtime updates about workspace changes** - Stay synchronized with workspace activity

## How Agents Use Linear

Agents use the Linear integration to streamline project management:

* **Track Work:** Automatically update the status of issues they are working on.
* **Link Code:** Connect implemented changes (GitHub PRs) directly to the relevant Linear issue.
* **Provide Updates:** Post comments on issues with progress reports, results, or questions.
* **Create Tasks:** Generate new issues for follow-up work, bugs discovered, or sub-tasks.

## Multi Agent Systems

### Overview

Once you've enabled linear self-assign in the settings [page](https://www.codegen.com/integrations/linear), a codegen agent, that has been assigned to a linear issue (or has been tagged in one), can spawn child agents
by creating sub-issues and assigning itself to those sub-issues. For each sub-issue that codegen assigns to itself a child agent will be spawned and tasked with completing the sub-issue. Once the child agents are
finished with their tasks they will notify their parent by sending it a message. The parent will then incorporate the child's work into its own as appropriate.

### Best Practices

#### Triggering the Child Agents

If you'd like to have codegen break up a linear issue into smaller issues and assign them to child agents you should instruct it to do so in the
description of the original linear issue.

#### Shared Context

Before creating sub-issues and assigning them to child agents the parent agent will produce scaffolding in the form of a git branch and include details
of this branch in the description of the sub-issues. The child agents will then work off of this scaffolding branch. If you have specific scaffolding requirements
or context you'd like the child agents to share, please include them in the description of the parent issue.

#### Availability

This feature is only available on the Team Plan.
