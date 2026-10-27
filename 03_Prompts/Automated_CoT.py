import json
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel
from typing import Literal

load_dotenv()

client = genai.Client()

# Schema for a single step
class CoTStep(BaseModel):
    step: Literal["START", "PLAN", "OUTPUT"]
    content: str

SYSTEM_PROMPT = """
You are an expert AI assistant that thinks strictly step-by-step using a Chain of Thought process.
You execute exactly ONE step per response.

Rules:
1. Always begin with a "START" step acknowledging and framing the user's request.
2. Next, generate one or more "PLAN" steps. Each "PLAN" step must focus on a single reasoning or analytical sub-step.
3. Once all planning/reasoning is sufficient, emit the final "OUTPUT" step containing the complete solution or answer.
4. Output strictly adheres to the JSON schema with fields 'step' and 'content'.
"""

def run_automated_cot(user_query: str):
    print(f"\n--- Starting Chain of Thought for: '{user_query}' ---\n")
    
    # Initialize chat session to maintain step history
    chat = client.chats.create(
        model="gemini-3.5-flash",
        config={
            "system_instruction": SYSTEM_PROMPT,
            "response_mime_type": "application/json",
            "response_schema": CoTStep,
        }
    )

    prompt = f"User Request: {user_query}\nPlease begin the Chain of Thought with the START step."
    step_count = 1

    while True:
        response = chat.send_message(prompt)
        raw_text = response.text.strip()
        
        try:
            parsed = json.loads(raw_text)
            current_step = parsed.get("step")
            content = parsed.get("content")
        except json.JSONDecodeError:
            print("Error parsing model response as JSON:", raw_text)
            break

        print(f"Step {step_count} [{current_step}]: {content}")

        if current_step == "OUTPUT":
            print("\nProcess complete.")
            break

        # Prompt the model to proceed to the next step
        prompt = "Continue with the next PLAN step, or emit the final OUTPUT step if planning is complete."
        step_count += 1

if __name__ == "__main__":
    query = input("Enter your prompt: ").strip()
    if query:
        try:
            run_automated_cot(query)
        except Exception as e:
            print("Something went wrong:", e)
    else:
        print("Input cannot be empty.")