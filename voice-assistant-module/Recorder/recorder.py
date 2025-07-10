import pyaudio
import numpy as np
import wave
import warnings
import threading

# Suppress FP16 warning
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

# Parameters
FORMAT = pyaudio.paInt16  # Audio format (16-bit)
CHANNELS = 1              # Mono audio
RATE = 44100              # Sampling rate (44.1 kHz)
CHUNK = 1024              # Buffer size
SILENCE_THRESHOLD = 500   # Threshold to detect silence
SILENCE_DURATION = 2      # Duration of silence to stop recording (in seconds)



def play_wav(filename):
    
    """
    Play a WAV file using PyAudio.
    """
    audio = pyaudio.PyAudio()
    chunk = 1024  # Buffer size
    with wave.open(filename, 'rb') as wf:
        stream = audio.open(format=audio.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)

        data = wf.readframes(chunk)
        while data:
            stream.write(data)
            data = wf.readframes(chunk)

        stream.stop_stream()
        stream.close()



def record_audio_silence(output_file="output.wav"):
    
    """
    Records audio until silence is detected and saves it to a WAV file.
    
    Args:
        output_file (str): Path to save the recorded audio file.
    """
    # Initialize PyAudio once
    audio = pyaudio.PyAudio()
    
    # Open audio stream
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("Recording... Speak now!")
    
    # Play beep sound in a separate thread
    threading.Thread(target=play_wav, args=("beepbeep.wav",)).start()

    frames = []
    silence_counter = 0
    recording = True
    silence_limit = int(SILENCE_DURATION * (RATE / CHUNK))  # Precompute silence limit

    while recording:
        # Read audio data from the stream
        data = stream.read(CHUNK)
        frames.append(data)

        # Convert audio data to numpy array
        audio_data = np.frombuffer(data, dtype=np.int16)

        # Check if the audio level is below the silence threshold
        if np.abs(audio_data).mean() < SILENCE_THRESHOLD:
            silence_counter += 1
        else:
            silence_counter = 0

        # Stop recording if silence duration is reached
        if silence_counter > silence_limit:
            recording = False

    # Stop and close the stream
    stream.stop_stream()
    stream.close()

    # Save the recorded audio as a WAV file
    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print(f"Audio saved as {output_file}")
    play_wav("beepbeep.wav")

def record_audio_duration(duration, output_file="output.wav"):
    """
    Records audio for a specified duration and saves it to a WAV file.
    
    Args:
        duration (float): Duration of the recording in seconds.
        output_file (str): Path to save the recorded audio file.
    """
    # Open audio stream
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print(f"Recording for {duration} seconds...")

    frames = []
    total_frames = int(RATE / CHUNK * duration)

    for _ in range(total_frames):
        # Read audio data from the stream
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording stopped.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()

    # Save the recorded audio as a WAV file
    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print(f"Audio saved as {output_file}")

if __name__ == "__main__":
    record_audio_silence(output_file="output.wav")
    # record_audio_duration(duration=5, output_file="output.wav")