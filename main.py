import os
import logging
import threading
from pathlib import Path
import pyperclip
import keyboard

from constants.GeneralConstants import BUFFER_SECONDS, HOTKEY, TEMP_AUDIO_DIR, LOG_DIR
from modules.AudioBufferModule import AudioBuffer
from modules.SpeechModule import transcribe_audio
from modules.GPTModule import react_to_transcription
from modules.PlaySoundModule import play_sound

# -----------------------------
# Setup directories
# -----------------------------
Path(TEMP_AUDIO_DIR).mkdir(exist_ok=True)
Path(LOG_DIR).mkdir(exist_ok=True)

# Setup logging
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "assistant.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"  # <-- important!
)

# -----------------------------
# Main functionality
# -----------------------------
def on_hotkey_pressed(audio_buffer: AudioBuffer):
    try:
        logging.info("Hotkey pressed, capturing audio...")
        # Save snapshot to temp file
        temp_file_path = audio_buffer.snapshot_to_wav()

        logging.info(f"Audio snapshot saved: {temp_file_path}")

        # Transcribe
        transcription, metadata = transcribe_audio(temp_file_path)
        logging.info(f"Transcription: {transcription}")

        # Generate GPT response
        response = react_to_transcription(transcription)
        logging.info(f"GPT Response: {response}")

        # Put response in clipboard
        pyperclip.copy(response)
        logging.debug("Response copied to clipboard.")

        # Play notification sound
        play_sound("ding")
        logging.debug("Played notification sound.")

        # Clean up temp audio
        os.remove(temp_file_path)
        logging.info(f"Deleted temp audio file: {temp_file_path}")

    except Exception as e:
        logging.exception(f"Error in hotkey handler: {e}")

def main():
    # Start audio buffer
    audio_buffer = AudioBuffer(buffer_seconds=BUFFER_SECONDS)
    audio_buffer.start()

    # Register global hotkey
    keyboard.add_hotkey(HOTKEY, lambda: threading.Thread(target=on_hotkey_pressed, args=(audio_buffer,), daemon=True).start())
    logging.info(f"Hotkey registered: {HOTKEY}")

    # Play welcome sound
    play_sound("ding")

    print(f"Voice assistant running. Press {HOTKEY} to capture last {BUFFER_SECONDS} seconds of audio...")
    print("Press Ctrl+C to quit.")

    try:
        keyboard.wait()  # keep program alive
    except KeyboardInterrupt:
        audio_buffer.stop()
        print("Exiting...")

if __name__ == "__main__":
    main()
