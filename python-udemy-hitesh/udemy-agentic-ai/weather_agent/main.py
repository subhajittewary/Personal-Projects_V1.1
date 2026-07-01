from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    api_key="AIzaSyDyqAmIXtVadt4cTLTEL_A-ta8CiS6IwHg",
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

def main():
    user_query = input("> ")
    response = client.chat.completions.create(
        model = "gemini-2.5-flash",
        messages = [
            {"role":"user", "content": user_query}
        ]
    )

    print(f"🤖: {response.choices[0].message.content}")


if __name__ == "__main__":
    main()
