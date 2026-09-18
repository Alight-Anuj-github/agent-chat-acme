# AgentCore Agent Chat for Acme Support

Interactive CLI chat for conversing with your Amazon Bedrock AgentCore runtime agent for Acme Support. Maintain multi-turn conversations with full session context persistence.

## Features

- **Interactive multi-turn conversations** - Ask questions and maintain context across turns
- **Persistent session** - Automatically creates a session ID on startup and reuses it throughout the conversation
- **Simple CLI interface** - Clean command-line interface with clear prompts and formatted output
- **Error handling** - Graceful error handling with detailed error messages
- **Direct AWS SDK integration** - Uses boto3 for direct Bedrock AgentCore API access
- **Lightweight & fast** - Single Python file, minimal dependencies

## Prerequisites

- Python 3.10+
- AWS credentials configured (via AWS SSO or environment variables)
- Bedrock AgentCore runtime deployed and accessible

## Installation

Clone the repository and install dependencies using UV:

```bash
git clone https://github.com/Alight-Anuj-github/agent-chat-acme.git
cd agent-chat-acme
uv sync
```

**Requirements:**
- Python 3.10+
- UV package manager
- AWS credentials with Bedrock AgentCore access

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

1. **Session Creation** - Creates a unique UUID session ID when started
2. **Context Persistence** - Maintains the same session ID throughout the conversation for full context
3. **API Integration** - Uses boto3 `bedrock-agentcore` client's `invoke_agent_runtime()` method
4. **Message Sending** - Sends the agent runtime ARN, session ID, and prompt payload as JSON
5. **Response Processing** - Reads and decodes the response stream from the agent
6. **User Loop** - Continues the conversation loop until user exits
7. **Session Cleanup** - Displays exit message when conversation ends

### Bedrock AgentCore API Details

The script uses the following boto3 Bedrock AgentCore API:

```python
response = client.invoke_agent_runtime(
    agentRuntimeArn="arn:aws:bedrock-agentcore:region:account:runtime/AgentName",
    runtimeSessionId="unique-session-id",
    payload=json.dumps({"prompt": "user question"}).encode()
)

response_text = response["response"].read().decode("utf-8")
```

- **Client**: `bedrock-agentcore` boto3 client (not `bedrock-agent-runtime`)
- **Method**: `invoke_agent_runtime()` 
- **Parameters**: Agent ARN, session ID, and JSON-encoded payload
- **Response**: Byte stream accessible via `response["response"].read()`
- **Session Context**: Same `runtimeSessionId` maintains conversation context across invocations

## Troubleshooting

### Authentication Issues

- **"Failed to create Bedrock AgentCore client"**: Check AWS credentials with `aws sts get-caller-identity`
- **"Access Denied" / "UnauthorizedOperation"**: Verify IAM permissions for `bedrock-agentcore:InvokeAgentRuntime` action
- **"NoCredentialsError"**: Run `aws sso login --profile alight-qc-data-solutions` to refresh SSO credentials

### Agent Issues

- **"Error invoking agent"**: Verify the agent ARN is correct using `agentcore status`
- **"ValidationException"**: Check that:
  - The ARN format is correct: `arn:aws:bedrock-agentcore:region:account:runtime/AgentName`
  - The deployed runtime exists and is active
  - The region matches your agent deployment

### Runtime Issues

- **Empty responses**: Confirm that:
  - Your AgentCore runtime is deployed: `agentcore status`
  - The session ID is valid (automatically handled)
  - The agent has properly configured skills and knowledge bases
- **Slow responses**: Check CloudWatch logs and agent configuration for bottlenecks
- **"Connection timeout"**: Verify network connectivity and AWS region configuration

## Development

### Project Structure

```
agent-chat-acme/
├── src/agent_chat_acme/
│   └── __init__.py        # Main CLI implementation
├── pyproject.toml         # Project configuration and dependencies
├── README.md              # This file
└── .gitignore             # Git ignore rules
```

### Dependencies

- `boto3` >= 1.26.0 - AWS SDK for Python
- `botocore` >= 1.29.0 - Low-level AWS API client

### Running Locally

```bash
# Install dependencies
uv sync

# Run the CLI
uv run agent-chat-acme

# Or after installation
agent-chat-acme
```

### Modifying Agent ARN

To connect to a different Bedrock AgentCore runtime, update the ARN in `src/agent_chat_acme/__init__.py`:

```python
RUNTIME_AGENT_ARN = "arn:aws:bedrock-agentcore:region:account-id:runtime/AgentName"
```

### Contributing

Contributions are welcome! For bug reports or feature requests, please open an issue or submit a pull request.

## Resources

- [AWS Bedrock AgentCore Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-concepts.html)
- [boto3 Bedrock Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore.html)
- [AgentCore CLI Documentation](https://github.com/aws/agentcore)
- [UV Package Manager](https://docs.astral.sh/uv/)

## License

This project is provided as-is for Acme Support internal use.

---

**Last Updated**: September 2026  
**Repository**: https://github.com/Alight-Anuj-github/agent-chat-acme