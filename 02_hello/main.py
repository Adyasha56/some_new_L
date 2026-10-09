from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()

try:
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents="Hey there! I am Adyasha."
    )

    print("Response:", response.text)

except Exception as e:
    print("Something went wrong:", e)