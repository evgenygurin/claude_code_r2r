# LLM Configuration

Codegen offers flexibility in choosing the Large Language Model (LLM) that powers your agent, allowing you to select from various providers and specific models. You can also configure custom API keys and base URLs if you have specific arrangements or need to use self-hosted models.

<Frame>
  <video controls src="https://res.cloudinary.com/dbikr6pew/video/upload/v1757976620/Model_Choice_ogcic1.mp4" className="aspect-[3324/2160]" />
</Frame>

<Card title="Configure Model Settings" icon="microchip" href="https://codegen.com/settings/model">
  Choose your LLM provider, select models, and configure custom API keys for
  your organization.
</Card>

## Accessing LLM Configuration

LLM Configuration settings are applied globally for your entire organization. You can access and modify these settings by navigating to:

<Card title="Configure Model Settings" icon="microchip" href="https://codegen.com/settings/model">
  Choose your LLM provider, select models, and configure custom API keys for
  your organization.
</Card>

This central location ensures that all agents operating under your organization adhere to the selected LLM provider and model, unless specific per-repository or per-agent overrides are explicitly configured (if supported by your plan).

<Frame caption="LLM Configuration UI at codegen.com/settings/model">
  <img src="https://mintcdn.com/codegeninc/TEOdIY76pi_ZHrje/images/llm-configuration.png?fit=max&auto=format&n=TEOdIY76pi_ZHrje&q=85&s=6c090a5eeca24eb8ee7e30bb07cb454a" alt="LLM Configuration UI" data-og-width="1482" width="1482" data-og-height="844" height="844" data-path="images/llm-configuration.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/codegeninc/TEOdIY76pi_ZHrje/images/llm-configuration.png?w=280&fit=max&auto=format&n=TEOdIY76pi_ZHrje&q=85&s=2a926f7a884b2d2cfc65c8836851a91b 280w, https://mintcdn.com/codegeninc/TEOdIY76pi_ZHrje/images/llm-configuration.png?w=560&fit=max&auto=format&n=TEOdIY76pi_ZHrje&q=85&s=c3cd467326c7d16cf2ca3778ee0b3262 560w, https://mintcdn.com/codegeninc/TEOdIY76pi_ZHrje/images/llm-configuration.png?w=840&fit=max&auto=format&n=TEOdIY76pi_ZHrje&q=85&s=5dc37679d7acddfae089134d9eecef3e 840w, https://mintcdn.com/codegeninc/TEOdIY76pi_ZHrje/images/llm-configuration.png?w=1100&fit=max&auto=format&n=TEOdIY76pi_ZHrje&q=85&s=571f1bffa85ec3e78c532a608787b92e 1100w, https://mintcdn.com/codegeninc/TEOdIY76pi_ZHrje/images/llm-configuration.png?w=1650&fit=max&auto=format&n=TEOdIY76pi_ZHrje&q=85&s=1a612078f47433156ce6cb80180664ea 1650w, https://mintcdn.com/codegeninc/TEOdIY76pi_ZHrje/images/llm-configuration.png?w=2500&fit=max&auto=format&n=TEOdIY76pi_ZHrje&q=85&s=8521cb3f241bf2757f7d7002d0796f97 2500w" />
</Frame>

As shown in the UI, you can generally configure the following:

* **LLM Provider:** Select the primary LLM provider you wish to use. Codegen supports major providers such as:
  * Anthropic
  * OpenAI
  * Google (Gemini)
* **LLM Model:** Once a provider is selected, you can choose a specific model from that provider's offerings (e.g., Claude 4 Sonnet, GPT-4, Gemini Pro).

## Enhanced Agent Modes

For improved agent performance, you can enable Claude Code mode which runs agents in Anthropic's specialized coding environment:

<Card title="Claude Code Mode" icon="code" href="/settings/claude-code">
  Configure agents to run in Claude Code harness for enhanced coding
  capabilities and superior development assistance.
</Card>

## Model Recommendation

<Warning>
  While Codegen provides access to a variety of models for experimentation and
  specific use cases, **we highly encourage the use of Anthropic's Claude 4
  Sonnet**. Our internal testing and prompt engineering are heavily optimized
  for Claude 4 Sonnet, and it consistently delivers the best performance,
  reliability, and cost-effectiveness for most software engineering tasks
  undertaken by Codegen agents. Other models are made available primarily for
  users who are curious or have unique, pre-existing workflows.
</Warning>

## Custom API Keys and Base URLs

For advanced users or those with specific enterprise agreements with LLM providers, Codegen allows you to use your own API keys and, in some cases, custom base URLs (e.g., for Azure OpenAI deployments or other proxy/gateway services).

<Card title="Configure API Keys" icon="key" href="https://codegen.com/settings/api-keys">
  Set up custom API keys for OpenAI, Anthropic, Google, and Grok models.
</Card>

We currently support custom API keys for:

* **OpenAI** - GPT-4, GPT-4 Turbo, and other OpenAI models
* **Anthropic** - Claude 4 Sonnet, Claude 4 Opus, and Claude 4 Haiku
* **Google** - Gemini Pro and other Google AI models
* **Grok** - Grok models from xAI

**Benefits of custom API keys:**

* **Custom API Key:** If you provide your own API key, usage will be billed to your account with the respective LLM provider.
* **Custom Base URL:** This allows Codegen to route LLM requests through a different endpoint than the provider's default API.

<Tip>
  Using the default Codegen-managed LLM configuration (especially with Claude 4
  Sonnet) is recommended for most users to ensure optimal performance and to
  benefit from our continuous prompt improvements.
</Tip>

<Note>
  The availability of specific models, providers, and custom configuration
  options may vary based on your Codegen plan and the current platform
  capabilities.
</Note>
