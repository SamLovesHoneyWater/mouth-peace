from constants.PromptConstants import GPT_PROMPT_PRE, GPT_PROMPT_POST
from modules.OpenAIClientModule import openAIClient as client

def get_gpt_response(prompt):
    response = client.responses.create(
        model="gpt-5-nano",
        input=prompt
    )
    return response.output_text

def react_to_transcription(transcription):
    prompt = f"{GPT_PROMPT_PRE}\n{transcription}\n{GPT_PROMPT_POST}"
    return get_gpt_response(prompt)

if __name__ == "__main__":
    test_prompt = "Hi."
    response = get_gpt_response(test_prompt)
    print(response)
