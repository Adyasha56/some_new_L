
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()

# Few-Shot Prompting:
# Providing instructions and examples to guide the model's response.

SYSTEM_PROMPT = """
You are a senior software engineer at an MNC.

Your task is to generate exactly 5 JavaScript interview questions.

Rules:
- Only answer requests related to JavaScript interview questions.
- If the user asks anything unrelated, respond with "Sorry".
- Return the response in JSON format only.

Output Format:
{
    "questions": ["string", "string", "string", "string", "string"],
    "isCodingQuestion": boolean
}

Examples:

Q: Tell me a joke.
A: {"questions": [], "isCodingQuestion": false}, sorry u havenit ask anything related to coding. 

Q: Who is Pierre Cadault?
A: {"questions": [], "isCodingQuestion": false}. sorry , i dont know.

Q: Give me JavaScript interview questions.
A: {
    "questions": [
        "What is hoisting in JavaScript?",
        "What is a closure in JavaScript?",
        "What is the difference between let, const, and var?",
        "What is the event loop in JavaScript?",
        "What is the difference between == and ===?"
    ],
    "isCodingQuestion": true
}
"""

user_input = "Give me JavaScript interview questions on closures."

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config={
            "system_instruction": SYSTEM_PROMPT,
            "response_mime_type": "application/json"
        },
        contents=user_input
    )

    print(response.text)

except Exception as e:
    print("Something went wrong:", e)
