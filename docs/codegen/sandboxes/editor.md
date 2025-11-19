# Remote Editor (VSCode)

Codegen provides access to a remote VSCode editor instance that is directly connected to your active sandbox environment. This powerful feature allows for real-time interaction with the agent's workspace, offering capabilities for live debugging, manual intervention, and detailed progress monitoring.

## Accessing the Editor

When an agent is active and utilizing a sandbox, a link or button to access the Remote Editor will typically be available on the agent's trace page or within the Codegen UI.

<Frame caption="Access the Remote Editor from the Codegen UI (example)">
  <img src="https://mintcdn.com/codegeninc/TEOdIY76pi_ZHrje/images/sandbox-buttons.png?fit=max&auto=format&n=TEOdIY76pi_ZHrje&q=85&s=6a920bcf4ab1a8d3b92896dfb6625405" alt="Remote VSCode Editor" data-og-width="746" width="746" data-og-height="130" height="130" data-path="images/sandbox-buttons.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/codegeninc/TEOdIY76pi_ZHrje/images/sandbox-buttons.png?w=280&fit=max&auto=format&n=TEOdIY76pi_ZHrje&q=85&s=18a415c146b6c155aa8d569739360b9e 280w, https://mintcdn.com/codegeninc/TEOdIY76pi_ZHrje/images/sandbox-buttons.png?w=560&fit=max&auto=format&n=TEOdIY76pi_ZHrje&q=85&s=db7f068e76cf7cca73dc0a4555ecaab6 560w, https://mintcdn.com/codegeninc/TEOdIY76pi_ZHrje/images/sandbox-buttons.png?w=840&fit=max&auto=format&n=TEOdIY76pi_ZHrje&q=85&s=a12101d7ad1fbdc47f36a820ca7a9b3b 840w, https://mintcdn.com/codegeninc/TEOdIY76pi_ZHrje/images/sandbox-buttons.png?w=1100&fit=max&auto=format&n=TEOdIY76pi_ZHrje&q=85&s=975ee37b915f58cb08dfcf2be316f3d4 1100w, https://mintcdn.com/codegeninc/TEOdIY76pi_ZHrje/images/sandbox-buttons.png?w=1650&fit=max&auto=format&n=TEOdIY76pi_ZHrje&q=85&s=2ae5aa65c03957092aac837d58b738d1 1650w, https://mintcdn.com/codegeninc/TEOdIY76pi_ZHrje/images/sandbox-buttons.png?w=2500&fit=max&auto=format&n=TEOdIY76pi_ZHrje&q=85&s=23dab1af527e0d682a0e17f0be0912bf 2500w" />
</Frame>

Access to the editor is password-protected. A unique password will be dynamically generated at runtime for each session and provided to you, ensuring secure access to the sandbox environment.

## Capabilities

The Remote Editor offers several key benefits:

* **Run Arbitrary Commands:** Open a terminal directly within VSCode to execute any shell commands in the sandbox. This is useful for:
  * Manually running tests.
  * Inspecting file contents.
  * Trying out different commands or scripts.
  * Installing additional temporary tools or dependencies.
* **View Agent's Progress:** See the files the agent is creating or modifying in real-time. This provides a transparent view into the agent's operations and can help in understanding its decision-making process.
* **Live Debugging:** If the agent is running a service or script, you can use VSCode's debugging tools (if applicable to the language/runtime) to step through code, inspect variables, and diagnose issues.
* **Manual Edits:** While generally agents manage the codebase, you can make manual edits to files directly if needed for quick fixes or experiments. Be mindful that agent actions might overwrite manual changes if not coordinated.

## How it Works

The remote editor essentially provides a fully functional VSCode interface tunneled into the agent's sandbox. This means you are working directly within the same environment as the agent, with access to the same file system, installed tools, and [Environment Variables](./environment-variables).

<Tip>
  The Remote Editor is an excellent tool for gaining deeper insights into an
  agent's operations and for situations where you need to interact more directly
  with the sandbox environment than through standard agent commands.
</Tip>

<Note>
  Like other sandbox features, the editor session is tied to the lifecycle of
  the sandbox. Changes made might be ephemeral if the sandbox is reset or a new
  snapshot is used for subsequent runs, unless those changes are committed back
  through the agent or other means.
</Note>

{" "}
