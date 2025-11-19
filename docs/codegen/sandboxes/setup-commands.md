# Setup Commands

Codegen lets you configure custom setup commands that run once when initializing a repository's sandbox environment. The resulting file system snapshot serves as the starting point for all future agent runs, ensuring consistency.

<Tip>
  The most common use cases for setup commands is installing dependencies, e.g.
  `npm install`
</Tip>

## Base Image

Codegen sandboxes are built on a custom Docker image that provides a comprehensive development environment. For detailed information about the base image, including the complete Dockerfile and available tools, see the [Base Image](/sandboxes/base-image) documentation.

## Accessing Setup Commands

To configure setup commands for a repository:

1. Navigate to [codegen.com/repos](https://codegen.com/repos).
2. Click on the desired repository from the list.
3. You will be taken to the repository's settings page. The setup commands can be found at a URL similar to `https://www.codegen.com/repos/{arepo_name}/setup-commands`

<Frame caption="Set setup commands at codegen.com/repos">
  <img src="https://mintcdn.com/codegeninc/TEOdIY76pi_ZHrje/images/setup-commands-ui.png?fit=max&auto=format&n=TEOdIY76pi_ZHrje&q=85&s=62463761493cbd7ec2585c602ab9c4df" alt="Setup Commands UI" data-og-width="3058" width="3058" data-og-height="1912" height="1912" data-path="images/setup-commands-ui.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/codegeninc/TEOdIY76pi_ZHrje/images/setup-commands-ui.png?w=280&fit=max&auto=format&n=TEOdIY76pi_ZHrje&q=85&s=bf6a89ad8ca5073009d3a6e25761e096 280w, https://mintcdn.com/codegeninc/TEOdIY76pi_ZHrje/images/setup-commands-ui.png?w=560&fit=max&auto=format&n=TEOdIY76pi_ZHrje&q=85&s=d59b8b2d56ba0f7d2a86b1b925f9cfc4 560w, https://mintcdn.com/codegeninc/TEOdIY76pi_ZHrje/images/setup-commands-ui.png?w=840&fit=max&auto=format&n=TEOdIY76pi_ZHrje&q=85&s=c06715abb12ef19745775a67e9eb71d0 840w, https://mintcdn.com/codegeninc/TEOdIY76pi_ZHrje/images/setup-commands-ui.png?w=1100&fit=max&auto=format&n=TEOdIY76pi_ZHrje&q=85&s=876d4f3dd1721a2251f7096f3d3af7bb 1100w, https://mintcdn.com/codegeninc/TEOdIY76pi_ZHrje/images/setup-commands-ui.png?w=1650&fit=max&auto=format&n=TEOdIY76pi_ZHrje&q=85&s=5a46c0451b0d6a63509e0af9f6f642c7 1650w, https://mintcdn.com/codegeninc/TEOdIY76pi_ZHrje/images/setup-commands-ui.png?w=2500&fit=max&auto=format&n=TEOdIY76pi_ZHrje&q=85&s=554f0675fc1ae0c97e0ac1633cf1738c 2500w" />
</Frame>

## How it Works

Enter your desired setup commands in the provided text area, with one command per line. These commands will be executed in sequence within the sandbox environment.

For example, you might want to:

* Switch to a specific Node.js version.
* Install project dependencies.
* Run any necessary build steps or pre-compilation tasks.

After the commands are executed successfully, Codegen takes a snapshot of the sandbox's file system. This snapshot then serves as the base environment for future agent interactions with this repository, meaning your setup commands don't need to be re-run every time, saving time and ensuring consistency.

## Common Examples

Here are a few common use cases for setup commands:

```bash
# Switch to Node.js version 20
nvm use 20

# Install npm dependencies
npm install
```

```bash
# Setup with specific Python version for compatibility
pyenv install 3.12.0
pyenv local 3.12.0
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

```bash
# Or a combination of commands
nvm use 18
npm ci
npm run build
```

### Working with Different Python Versions

The sandbox comes with Python 3.13 by default, but some packages may not yet be compatible with this version. Here are strategies for handling different Python versions:

#### Using pyenv for Multiple Python Versions

If you need to work with a different Python version, you can install and use `pyenv`:

```bash
# Install pyenv
curl https://pyenv.run | bash

# Add pyenv to PATH (for current session)
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

# Install Python 3.12 (or your desired version)
pyenv install 3.12.0

# Set Python 3.12 as the local version for your project
pyenv local 3.12.0

# Create a virtual environment with Python 3.12
python -m venv venv
source venv/bin/activate

# Install your dependencies
pip install -r requirements.txt
```

#### Using uv with Specific Python Versions

The `uv` package manager (already installed) can also manage Python versions:

```bash
# Install Python 3.12 and create a virtual environment
uv venv --python=3.12

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt --refresh --upgrade
```

#### Virtual Environment Best Practices

When working with packages that require older Python versions:

```bash
# Create a virtual environment with a specific Python version
python3.12 -m venv venv_312
source venv_312/bin/activate

# Verify the Python version
python --version

# Install packages that require Python 3.12
pip install argis==2.4.0  # Example package that needs older Python

# Deactivate when done
deactivate
```

<Warning>
  Remember to activate your virtual environment in your setup commands if you need specific Python versions for your project dependencies.
</Warning>

<Note>
  Ensure your setup commands are non-interactive and can run to completion
  without user input.
</Note>

<Tip>
  The environment variables listed in the "Env Variables" section are available
  during the execution of these setup commands.
</Tip>
