
import json
import os
import subprocess
from typing import Literal, Optional

import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field


load_dotenv()

client = genai.Client()


def run_command(cmd: str) -> str:
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = result.stdout.strip()
        error = result.stderr.strip()
        if output and error:
            return f"{output}\n{error}"
        return output or error or f"Command exited with code {result.returncode}"
    except subprocess.TimeoutExpired:
        return "Command timed out after 30 seconds"
    except Exception as exc:
        return f"Could not run command: {exc}"


def get_weather(city: str) -> str:
    try:
        response = requests.get(
            f"https://wttr.in/{city.lower()}?format=%C+%t",
            timeout=10,
        )
        if response.status_code == 200:
            return f"The weather in {city} is {response.text}"
        return "Something went wrong"
    except requests.RequestException as exc:
        return f"Could not get weather: {exc}"


available_tools = {
    "get_weather": get_weather,
    "run_command": run_command,
}


SYSTEM_PROMPT = """
You're an expert AI assistant that resolves user queries by selecting one step at a time.
The user-visible steps are START, PLAN, and OUTPUT. You may call a tool with a TOOL step.
After a tool call, wait for the OBSERVE value from the tool.

Rules:
- Return strictly valid JSON matching the requested schema.
- Only run one step at a time.
- Do not expose private chain-of-thought. PLAN messages may contain concise, non-sensitive
  summaries of actions and decisions, not detailed hidden reasoning.
- For every tool call, set tool and input.

Available Tools:
- get_weather(city: str): Gets weather information for a city.
- run_command(cmd: str): Runs a command on the user's system and returns its output.
"""


class MyOutputFormat(BaseModel):
    step: Literal["START", "PLAN", "OUTPUT", "TOOL", "OBSERVE"]
    content: Optional[str] = Field(
        None,
        description="A concise summary or user-facing response.",
    )
    tool: Optional[str] = Field(None, description="The tool name to call.")
    input: Optional[str] = Field(None, description="The tool input.")
    output: Optional[str] = Field(None, description="The tool output.")


def parse_step(response) -> MyOutputFormat:
    if response.parsed is not None:
        return response.parsed
    return MyOutputFormat.model_validate_json(response.text)


def main() -> None:
    model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    chat = client.chats.create(
        model=model,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
            response_schema=MyOutputFormat,
        ),
    )

    print("\n\n")
    while True:
        user_query = input("👉🏻 ")
        if user_query.lower() in {"exit", "quit"}:
            break

        next_message = user_query
        while True:
            response = chat.send_message(next_message)
            parsed_result = parse_step(response)

            if parsed_result.step == "START":
                print("🔥", parsed_result.content)
                next_message = json.dumps({"step": "CONTINUE"})
                continue

            if parsed_result.step == "TOOL":
                tool_name = parsed_result.tool
                tool_input = parsed_result.input or ""
                print(f"🛠️: {tool_name} ({tool_input})")

                if tool_name not in available_tools:
                    tool_response = f"Unknown tool: {tool_name}"
                else:
                    tool_response = available_tools[tool_name](tool_input)

                print(f"🛠️ : {tool_name} ({tool_input}) = {tool_response}")
                next_message = json.dumps(
                    {
                        "step": "OBSERVE",
                        "tool": tool_name,
                        "input": tool_input,
                        "output": str(tool_response),
                    }
                )
                continue

            if parsed_result.step == "PLAN":
                print("🧠", parsed_result.content)
                next_message = json.dumps({"step": "CONTINUE"})
                continue

            if parsed_result.step == "OUTPUT":
                print("🤖", parsed_result.content)
                break

    print("\n\n")


if __name__ == "__main__":
    main()
