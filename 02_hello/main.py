from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()

try:
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        config={
            "system_instruction": (
                "You are a senior engineer in an MNC."
            )
        },
        contents="Give me 5 interview questions on JavaScript."
    )

    print("Response:", response.text)

except Exception as e:
    print("Something went wrong:", e)