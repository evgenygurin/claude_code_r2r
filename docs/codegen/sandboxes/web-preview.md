# Web Preview

Codegen's Web Preview feature lets you start a development server in your sandbox and view your running application directly in the Codegen interface.

## How it Works

Define your web server startup commands just like [Setup Commands](./setup-commands). Instead of taking a snapshot, Codegen keeps the server running as a long-lived process.

A "View Web Preview" button appears on the agent trace page once the server starts. Click it to open your running application in a new tab through Codegen's secure proxy.

<Frame caption="Access the Web Preview from the agent trace page">
  <img src="https://mintcdn.com/codegeninc/TEOdIY76pi_ZHrje/images/sandbox-buttons.png?fit=max&auto=format&n=TEOdIY76pi_ZHrje&q=85&s=6a920bcf4ab1a8d3b92896dfb6625405" alt="Web Preview button on Trace Page" data-og-width="746" width="746" data-og-height="130" height="130" data-path="images/sandbox-buttons.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/codegeninc/TEOdIY76pi_ZHrje/images/sandbox-buttons.png?w=280&fit=max&auto=format&n=TEOdIY76pi_ZHrje&q=85&s=18a415c146b6c155aa8d569739360b9e 280w, https://mintcdn.com/codegeninc/TEOdIY76pi_ZHrje/images/sandbox-buttons.png?w=560&fit=max&auto=format&n=TEOdIY76pi_ZHrje&q=85&s=db7f068e76cf7cca73dc0a4555ecaab6 560w, https://mintcdn.com/codegeninc/TEOdIY76pi_ZHrje/images/sandbox-buttons.png?w=840&fit=max&auto=format&n=TEOdIY76pi_ZHrje&q=85&s=a12101d7ad1fbdc47f36a820ca7a9b3b 840w, https://mintcdn.com/codegeninc/TEOdIY76pi_ZHrje/images/sandbox-buttons.png?w=1100&fit=max&auto=format&n=TEOdIY76pi_ZHrje&q=85&s=975ee37b915f58cb08dfcf2be316f3d4 1100w, https://mintcdn.com/codegeninc/TEOdIY76pi_ZHrje/images/sandbox-buttons.png?w=1650&fit=max&auto=format&n=TEOdIY76pi_ZHrje&q=85&s=2ae5aa65c03957092aac837d58b738d1 1650w, https://mintcdn.com/codegeninc/TEOdIY76pi_ZHrje/images/sandbox-buttons.png?w=2500&fit=max&auto=format&n=TEOdIY76pi_ZHrje&q=85&s=23dab1af527e0d682a0e17f0be0912bf 2500w" />
</Frame>

## Configuration

You configure Web Preview commands in a manner similar to Setup Commands, likely within the same repository settings area (e.g., `https://codegen.com/{your_org}/{repo_name}/settings/web-preview`).

You'll provide the command(s) necessary to start your development server. Ensure that your server is configured to listen on an appropriate host (often `127.0.0.1`) and a predictable port that Codegen can then expose.

<Warning>
  The web server started for Web Preview **MUST** listen on port 3000. Codegen
  is specifically configured to look for and expose applications running on this
  port within the sandbox.
</Warning>

## Common Examples

The primary use case is starting a development web server:

```bash
# For a Node.js/npm project
npm run dev
```

```bash
# For a Python/Django project
python manage.py runserver 127.0.0.1:3000
```

```bash
# For a Ruby on Rails project
bundle exec rails server -b 127.0.0.1 -p 3000
```

<Tip>
  The Web Preview server runs within the same sandbox environment as your other
  agent tasks, meaning it has access to the same file system (including any
  changes made by the agent) and the [Environment
  Variables](./environment-variables).
</Tip>

<Tip>
  The `CG_PREVIEW_URL` environment variable is automatically set and contains
  the URL where your web preview will be accessible. Use this in your
  application code when you need to reference the preview URL programmatically
  (e.g., for CORS configuration, webhooks, or generating absolute URLs).
</Tip>

<Note>
  The web preview is intended for development and debugging purposes. The server
  is typically only accessible while the agent run is active or for a short
  period afterward, and it's not designed for public hosting.
</Note>
