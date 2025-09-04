from faster_whisper import WhisperModel
from constants.GeneralConstants import WHISPER_MODEL

model = WhisperModel(WHISPER_MODEL, device="cuda", compute_type="float16")

def transcribe_audio(file_path):
    segments, info = model.transcribe(file_path)
    transcription = []

    for segment in segments:
        transcription.append(f"[{segment.start:.2f} → {segment.end:.2f}] {segment.text}")

    return transcription, info

if __name__ == "__main__":
    transcription, info = transcribe_audio("data/Recording.mp3")

    for segment in transcription:
        print(segment)
