# AgentCore Agent Chat for Acme Support

Interactive chat for conversing with your AgentCore runtime agent for Acme Support.

## Features

- **Interactive multi-turn conversations** - Ask questions and maintain context across turns
- **Persistent session** - Automatically creates a session ID on startup and reuses it throughout the conversation
- **Simple CLI interface** - Clean command-line interface with clear prompts
- **Error handling** - Graceful error handling and user feedback
- **Uses boto3** - Leverages AWS SDK for Python to directly invoke AgentCore runtime

## Prerequisites

- Python 3.10+
- AWS credentials configured (via AWS SSO or environment variables)
- Bedrock AgentCore runtime deployed and accessible

## Installation

Install dependencies using UV:

```bash
uv sync
```

## AWS Authentication

Before running the chat, you must authorize your AWS credentials using AWS SSO with the **alight-qc-data-solutions** account:

```bash
aws sso login --profile alight-qc-data-solutions
```

Make sure you have an appropriate role assigned in the alight-qc-data-solutions account that has permissions to invoke AgentCore agents (e.g., `bedrock-agentcore:InvokeAgentRuntime` action).

Once authenticated, boto3 will automatically use your SSO credentials to invoke the agent.

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

To use with a different Bedrock AgentCore runtime, update the ARN in `src/agent_chat_acme/__init__.py`:

```python
RUNTIME_AGENT_ARN = "arn:aws:bedrock-agentcore:region:account-id:runtime/AgentName"
```

You can find your runtime ARN by running:
```bash
agentcore status
```

## How It Works

1. Creates a new session ID (UUID) when started
2. Maintains this session ID throughout the conversation
3. Uses boto3 `bedrock-agentcore` client's `invoke_agent_runtime()` method
4. Sends the agent runtime ARN, session ID, and prompt payload
5. Reads and processes the response stream from the agent
6. Displays agent responses in real-time
7. Continues until user types "exit" or "quit"

This approach uses boto3's Bedrock AgentCore API which provides direct access to deployed AgentCore runtimes.

## Troubleshooting

- **"Failed to create Bedrock AgentCore client"**: Check that AWS credentials are configured and accessible via `aws sts get-caller-identity`
- **"Error invoking agent"**: Verify the agent ARN is correct by running `agentcore status`
- **"Access Denied"**: Make sure you have IAM permissions for `bedrock-agentcore:InvokeAgentRuntime` action
- **"ValidationException"**: Check that the ARN format is correct and points to a valid deployed runtime
- **Empty responses**: Check that your AgentCore runtime is deployed (`agentcore status`) and the session ID is valid

