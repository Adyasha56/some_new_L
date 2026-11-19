from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

def main():
    user_query = input(">")
    response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=user_query,
        )
    print(f"Bot: {response.text}")

if __name__ == "__main__":
    main()

