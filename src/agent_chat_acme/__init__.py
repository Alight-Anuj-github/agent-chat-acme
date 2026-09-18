"""Interactive chat script for AgentCore runtime agent."""

import json
import sys
import uuid
from typing import Optional

import boto3
from botocore.exceptions import ClientError

# Configuration
RUNTIME_AGENT_ARN = "arn:aws:bedrock-agentcore:us-east-1:918817395031:runtime/AcmeSupport_AcmeSupport-iybrxT90UT"
REGION = "us-east-1"



def create_client():
    """Create a Bedrock AgentCore client."""
    return boto3.client("bedrock-agentcore", region_name=REGION)


def invoke_agent(client, prompt: str, session_id: str) -> Optional[str]:
    """
    Invoke the AgentCore agent with a prompt and session ID using boto3.

    Args:
        client: Bedrock AgentCore client
        prompt: User's question/prompt
        session_id: Session ID to maintain conversation context

    Returns:
        Response text from the agent or None if error
    """
    try:
        response = client.invoke_agent_runtime(
            agentRuntimeArn=RUNTIME_AGENT_ARN,
            runtimeSessionId=session_id,
            payload=json.dumps({"prompt": prompt}).encode(),
        )
        
        # Read response body
        response_body = response["response"].read()
        response_text = response_body.decode("utf-8")
        
        if not response_text:
            return "No response from agent"
        
        # Try to parse as JSON if possible
        try:
            data = json.loads(response_text)
            if isinstance(data, dict):
                # Check for common response fields
                if "response" in data:
                    return data["response"].strip()
                elif "text" in data:
                    return data["text"].strip()
                else:
                    return json.dumps(data, indent=2).strip()
        except json.JSONDecodeError:
            # Not JSON, return as-is
            pass
        
        return response_text.strip() if response_text.strip() else "No response from agent"
    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "Unknown")
        error_msg = e.response.get("Error", {}).get("Message", str(e))
        return f"Error ({error_code}): {error_msg}"
    except Exception as e:
        return f"Error: {str(e)}"


def main() -> None:
    """Main interactive chat loop."""
    print("=" * 70)
    print("AgentCore Agent Chat")
    print("=" * 70)
    print(f"Agent ARN: {RUNTIME_AGENT_ARN}")

    # Create a new session ID
    session_id = str(uuid.uuid4())
    print(f"Session ID: {session_id}")
    print("\nType 'exit', 'quit', or Ctrl+C to end the session.")
    print("=" * 70)
    print()

    # Create Bedrock AgentCore client
    try:
        client = create_client()
    except Exception as e:
        print(f"Failed to create Bedrock Agent Runtime client: {e}")
        sys.exit(1)

    # Interactive loop
    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit"]:
                print("\nSession ended. Goodbye!")
                break

            # Invoke agent
            output = invoke_agent(client, user_input, session_id)

            if output:
                # Clean up output by removing excessive whitespace
                print(f"\nAgent: {output.strip()}\n")
            else:
                print("\nAgent: No response from agent\n")

        except KeyboardInterrupt:
            print("\n\nSession ended by user. Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            print()
