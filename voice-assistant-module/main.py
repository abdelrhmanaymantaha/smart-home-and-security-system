
from Command_extraction import command_extract
import pvporcupine

from Recorder import recorder
from Speaker.speaker import text_to_sound
from SpeechToText import model
from command_execute import command_executor
from TextPreProcessing import text_processing
import sys
import os

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
try:
    from config_secrets import PORCUPINE_ACCESS_KEY
except ImportError:
    PORCUPINE_ACCESS_KEY = os.getenv('PORCUPINE_ACCESS_KEY', '')

# Initialize the speech-to-text pipeline once
pipline = model.SpeechToTextPipeline()
import pyaudio
import struct
WAKE_WORD_PATH = r"models\whisper_en_windows_v3_0_0.ppn"
ACCESS_KEY = PORCUPINE_ACCESS_KEY

def wait_for_wake_word():
    porcupine = pvporcupine.create(keyword_paths=[WAKE_WORD_PATH],
                                   access_key= ACCESS_KEY)
    pa = pyaudio.PyAudio()
    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )
    print("Listening for wake word...")
    try:
        while True:
            pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            result = porcupine.process(pcm)
            if result >= 0:
                print("Wake word detected!")
                break
    finally:
        audio_stream.close()
        pa.terminate()
        porcupine.delete()

def main():     
    SPEECH_FILE = "output.wav"
    while True:
        try:
            wait_for_wake_word()
            text_to_sound('How can I help you?')
            recorder.record_audio_silence(output_file=SPEECH_FILE)
            text = pipline.transcribe(SPEECH_FILE)
            print(f"User said: {text}")

            print(f"Input: {text}")

            text = text_processing.text_preprocessor(text)
            print(f"Processed text: {text}")
            command = command_extract.extract_command_data(text)
            print(f'user command: {command}')
            response = command_executor.command_execute(command)
            if  response:
                print(f"Response: {response}")
                print()

                if 'stop' in text:
                    break
            else:
                print("Invalid command!")
                text_to_sound("Sorry, I didn't understand that command. Please try again.")
                
        except Exception as e:
            print(f"An error occurred: {e}")
        
if __name__ == "__main__":
    main()
