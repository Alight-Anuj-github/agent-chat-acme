# AgentCore Agent Chat for Acme Support

Interactive chat for conversing with your AgentCore runtime agent for Acme Support.

## Features

- **Interactive multi-turn conversations** - Ask questions and maintain context across turns
- **Persistent session** - Automatically creates a session ID on startup and reuses it throughout the conversation
- **Simple CLI interface** - Clean command-line interface with clear prompts
- **Error handling** - Graceful error handling and user feedback
- **Zero external dependencies** - Uses only Python standard library + agentcore CLI

## Prerequisites

- Python 3.10+
- `agentcore` CLI installed and in your PATH
- AWS credentials configured (inherited by agentcore CLI)

## Installation

Install dependencies using UV:

```bash
uv sync
```

## AWS Authentication

Before running the chat, you must authorize your command line with AWS SSO using the **alight-qc-data-solutions** account:

```bash
aws sso login --profile alight-qc-data-solutions
```

Make sure you have an appropriate role assigned in the alight-qc-data-solutions account that has permissions to invoke AgentCore agents (e.g., `bedrock:InvokeAgent` action).

Once authenticated, the agentcore CLI will use your SSO credentials automatically to invoke the agent.

## Usage

### Run the chat:

```bash
uv run agent-chat-acme
```

Or using the command directly (after installation):

```bash
agent-chat-acme
```

### Interactive Session

Once started, you'll see:
- Agent ARN
- Session ID (automatically generated UUID)

Then enter your questions one by one:

```
========================================================================
AgentCore Agent Chat
========================================================================
Agent ARN: arn:aws:bedrock-agentcore:us-east-1:918817395031:runtime/AcmeSupport_AcmeSupport-iybrxT90UT
Session ID: 550e8400-e29b-41d4-a716-446655440000

Type 'exit', 'quit', or Ctrl+C to end the session.
========================================================================

You: What's the status of order ORD-1001?
Agent: <response from agent>

You: What about order ORD-1002?
Agent: <response from agent>

You: exit

Session ended. Goodbye!
```

**Commands:**
- Type any question and press Enter to send it to the agent
- Type `exit` or `quit` to end the session
- Press `Ctrl+C` to terminate immediately

## Configuration

To use with a different agent ARN, edit the constant in `src/agent_chat/__init__.py`:

```python
RUNTIME_AGENT_ARN = "arn:aws:bedrock-agentcore:region:account-id:runtime/AgentName"
```

## How It Works

1. Creates a new session ID (UUID) when started
2. Maintains this session ID throughout the conversation
3. Calls the `agentcore invoke` CLI command with each user input and the session ID
4. Displays agent responses in real-time
5. Continues until user types "exit" or "quit"

This approach leverages the agentcore CLI which you've already tested and verified works with your AWS setup.

## Troubleshooting

- **"Error: 'agentcore' CLI not found"**: Make sure the agentcore CLI is installed and in your PATH
- **"Error invoking agent"**: Check that the agentcore CLI command works directly: `agentcore invoke --prompt "test" --session-id 123`
- **Empty responses**: Check that your AWS credentials are configured and you have permissions to invoke the agent

