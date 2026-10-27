from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel
from typing import List, Literal

load_dotenv()

client = genai.Client()

# Define schema using Pydantic for guaranteed valid JSON
class CoTStep(BaseModel):
    step: Literal["START", "PLAN", "OUTPUT"]
    content: str

class CoTResponse(BaseModel):
    steps: List[CoTStep]

SYSTEM_PROMPT = """
You are an expert AI assistant resolving user queries through an explicit Chain of Thought.
For every query:
1. Begin with a START step confirming the user input.
2. Break down the reasoning into multiple detailed PLAN steps.
3. Conclude with a final OUTPUT step containing the complete solution/code.
"""

user_input = "write a code in js to add two numbers."

try:
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=user_input,
        config={
            "system_instruction": SYSTEM_PROMPT,
            "response_mime_type": "application/json",
            "response_schema": CoTResponse,
        },
    )

    print(response.text)

except Exception as e:
    print("Something went wrong:", e)