import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=openai_api_key)

def get_gpt_response(prompt):
    response = client.responses.create(
        model="gpt-5-nano",
        input=prompt
    )
    return response.output_text

if __name__ == "__main__":
    test_prompt = "Hi."
    response = get_gpt_response(test_prompt)
    print(response)
