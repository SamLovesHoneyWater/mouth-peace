from constants.GeneralConstants import WHISPER_MODEL
from constants.GeneralConstants import DEFAULT_WHISPER_MODE

class BaseSpeechModule:
    def transcribe_audio(self, file_path):
        raise NotImplementedError("Subclasses should implement this method")

class APISpeechModule(BaseSpeechModule):
    def __init__(self):
        from modules.OpenAIClientModule import openAIClient as client
        self.client = client

    def transcribe_audio(self, file_path):
        audio_file = open(file_path, "rb")
        transcription = self.client.audio.transcriptions.create(
            model="gpt-4o-transcribe", 
            file=audio_file
        )
        return transcription.text

class LocalSpeechModule(BaseSpeechModule):
    def __init__(self):
        from faster_whisper import WhisperModel
        self.model = WhisperModel(WHISPER_MODEL, device="cuda", compute_type="float16")

    def transcribe_audio(self, file_path):
        segments, info_ = self.model.transcribe(file_path)
        transcription = []

        for segment in segments:
            transcription.append(f"[{segment.start:.2f} → {segment.end:.2f}] {segment.text}")

        return transcription

def get_speech_module():
    if DEFAULT_WHISPER_MODE == "API":
        return APISpeechModule()
    elif DEFAULT_WHISPER_MODE == "local":
        return LocalSpeechModule()
    else:
        raise ValueError(f"Unknown DEFAULT_WHISPER_MODE: {DEFAULT_WHISPER_MODE}")

if __name__ == "__main__":
    speech_module = get_speech_module()
    transcription = speech_module.transcribe_audio("data/Recording.mp3")

    print("Transcription:")
    print(transcription)
