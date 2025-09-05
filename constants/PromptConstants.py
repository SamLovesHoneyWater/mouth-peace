# Prompt-related constants

GPT_PROMPT_PRE = """
    The user is playing a tactical game on modern warfare between US and Russia.
    He needs to communicate with his teammates, but he doesn't have time to type.
    You are given a transcription of what he said recently.
    Your task is to generate a message that he can quickly copy-paste to his teammates in the game chat.
    Key points to include (if mentioned):
    - What the user is doing, e.g., "I'm pushing mid with infantry"
    - What the user needs from teammates and where, e.g., "Need anti-air on me"
    - Any enemy intel mentioned, e.g., "Enemy armor moving to Charlie", "Sniper in forest on ping"
    - The meaning of any pings the user made, e.g., "Pinged backline enemy AA, shoot artillery at it"
    - Strategic suggestions or observations, e.g., "We should take Alpha", "Watch out for enemy flanking from Delta"
    Ignore:
    - Off-topic comments
    - Hesitations or corrections
    - Cut-off conversations (especially at the start or end) that you cannot fully understand

    Here's the transcription (sometimes it includes timestamps, larger number means more recent):
    -------- START Transcription --------
    """

#GPT_PROMPT_PRE = "-------- START Transcription --------"

GPT_PROMPT_POST = """
    -------- END Transcription --------
    Based on the above transcription, generate a message that the user can copy-paste to his teammates in the game chat.
    If the transcript is in English, just respond in English plain text.
    If the transcript is in another language, respond in English translation
    Ensure minimal formatting so the message can be sent as-is in the game chat.
    Do not hallucinate any details. If the player is swearing, do not act polite. Instead, match the tone of the player.
    It is better to keep it faithful.
    """