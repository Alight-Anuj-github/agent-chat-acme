"""Interactive chat script for AgentCore runtime agent."""

import json
import os
import subprocess
import sys
import uuid
from pathlib import Path
from typing import Optional

# Configuration
RUNTIME_AGENT_ARN = "arn:aws:bedrock-agentcore:us-east-1:918817395031:runtime/AcmeSupport_AcmeSupport-iybrxT90UT"

# Determine project root (parent of agent-chat)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent


def invoke_agent(prompt: str, session_id: str) -> Optional[str]:
    """
    Invoke the agent with a prompt and session ID using agentcore CLI.

    Args:
        prompt: User's question/prompt
        session_id: Session ID to maintain conversation context

    Returns:
        Response text from the agent or None if error
    """
    try:
        result = subprocess.run(
            [
                "agentcore",
                "invoke",
                "--prompt",
                prompt,
                "--session-id",
                session_id,
            ],
            capture_output=True,
            text=True,
            check=False,
            cwd=str(PROJECT_ROOT),
            stdin=subprocess.DEVNULL,
        )
        if result.returncode != 0:
            error_msg = result.stderr.strip() if result.stderr else "Unknown error"
            return f"Error: {error_msg}"
        
        output = result.stdout.strip() if result.stdout else "No response from agent"
        
        # Try to parse JSON response and extract the "response" field
        try:
            data = json.loads(output)
            if isinstance(data, dict) and "response" in data:
                return data["response"]
        except json.JSONDecodeError:
            pass
        
        return output
    except FileNotFoundError:
        return "Error: 'agentcore' CLI not found. Please ensure agentcore CLI is installed and in your PATH."
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
            output = invoke_agent(user_input, session_id)

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
