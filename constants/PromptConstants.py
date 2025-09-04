# Prompt-related constants

GPT_PROMPT_PRE = """
    The user is playing a tactical game.
    He needs to communicate with his teammates, but he doesn't have time to type.
    You are given a transcription of what he said recently.
    Your task is to generate a message that he can quickly copy-paste to his teammates in the game chat.
    Key points to include:
    - What the user is doing (if mentioned), e.g., "I'm pushing mid with infantry", "Sending airstrike against armor", "Sending recon drone"
    - What the user needs from teammates and where (if mentioned), e.g., "Need help with Bravo", "Need anti-air on me", "Need artillery on ping"
    - Any enemy positions or movements mentioned, e.g., "Enemy armor moving to Charlie", "Sniper in forest on ping"
    - The meaning of any pings the user made, e.g., "Pinged backline enemy AA", "Need artillery on ping"
    - Strategic suggestions or observations, e.g., "We should take Alpha", "Let's defend Bravo", "Watch out for enemy flanking from Delta"
    - Keep the message concise and to the point, suitable for quick glance by teammates in a fast-paced game.
    - Concisely: What you as an assistant suggest the user's teammates should do based on the user's current situation and needs.
    Ignore:
    - Off-topic comments
    - Hesitations or corrections
    - Cut-off conversations (especially at the start or end) that you cannot fully understand

    Here's the transcription (including timestamps, larger number means more recent):
    -------- START Transcription --------
    """

GPT_PROMPT_POST = """
    -------- END Transcription --------
    Based on the above transcription, generate a message that the user can copy-paste to his teammates in the game chat.
    If the transcript is in English, just respond in English plain text.
    If the transcript is in another language, respond in that language AND add English translation with prefix like this:
    [ZH-CN] <response in Chinese>
    [EN] <response in English>
    Apart from that, ensure minimal formatting so the message can be sent as-is in the game chat.
    """