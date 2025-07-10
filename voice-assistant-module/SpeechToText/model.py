import torch
import whisper
import contextlib

@contextlib.contextmanager
def patch_torch_load():
    """Temporarily patch torch.load to use weights_only=True if not already set."""
    original_load = torch.load
    def patched_load(*args, **kwargs):
        if 'weights_only' not in kwargs:
            kwargs['weights_only'] = True
        return original_load(*args, **kwargs)
    torch.load = patched_load
    try:
        yield
    finally:
        torch.load = original_load

class SpeechToTextPipeline:
    def __init__(self, model_name="tiny.en"):
        """Initialize the Whisper model as a pipeline."""
        with patch_torch_load():
            self.model = whisper.load_model(model_name)
    
    def transcribe(self, audio_path) -> str:
        """Transcribe an audio file and return text."""
        result = self.model.transcribe(audio_path)
        text = result.get("text", "")
        return str(text) if text is not None else ""

# Example usage
if __name__ == "__main__":
    pipeline = SpeechToTextPipeline()  # Load the model once
    audio_file = "output.wav"
    
    transcribed_text = pipeline.transcribe(audio_file)
    print("Transcribed Text:", transcribed_text)
