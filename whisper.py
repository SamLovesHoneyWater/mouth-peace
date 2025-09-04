from faster_whisper import WhisperModel

model = WhisperModel("large-v3", device="cuda", compute_type="float16")

def transcribe_audio(file_path):
    segments, info = model.transcribe(file_path)
    return segments, info

if __name__ == "__main__":
    segments, info = transcribe_audio("data/Recording.mp3")

    for segment in segments:
        print(f"[{segment.start:.2f} → {segment.end:.2f}] {segment.text}")
