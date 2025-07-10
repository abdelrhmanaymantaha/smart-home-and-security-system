# Smart Home Voice Assistant

This project implements a voice assistant to control home devices in a smart home setup. The assistant listens to user commands, processes the speech, extracts relevant details such as device name, location, action, and value (like temperature or fan speed), and sends this information to an MQTT server for device control.

## Project Structure

The project is organized into the following blocks:

### 1. **Recorder**
- The Recorder listens for user voice commands via a microphone.
- It captures audio input continuously until the user stops speaking, then sends the recorded audio for processing.
- Supports recording until silence is detected or for a specified duration.

### 2. **Speech to Text AI Model**
- Converts the recorded audio into text using the Whisper speech-to-text model from OpenAI.
- The transcription process uses a custom `speech_to_text()` function that leverages the Whisper model to convert speech into text from an audio file.

### 3. **Command Extractor**
- Processes the transcribed text and extracts the device name, location, action, and value.
- Sub-blocks:
  - **Intent Extractor**: Identifies the user's intent (e.g., "turn on", "set temperature").
  - **Device Extractor**: Identifies the target device (e.g., light, fan, thermostat).
  - **Location Extractor**: Identifies the location of the device (e.g., living room, kitchen).
  - **Value Extractor**: Extracts the value of temperature or fan speed

### 4. **Command Executer**
- Sends the extracted data (device, location, action, value) to the MQTT server to control the smart home devices.
- Uses the `paho-mqtt` library to publish messages to an MQTT broker.

### 5. **Voice Feedback**
- Provides voice feedback to the user about the status of their commands.
- Uses the `pyttsx3` library to convert text responses into speech.

## Requirements

- Python 3.8+
- Libraries:
    - `pandas`
    - `paho-mqtt`
    - `pyaudio`
    - `pyttsx3`
    - `torch`
    - `openai-whisper`
    - `scikit-learn`
    - `joblib`
    - `requests`

Install the dependencies by running:

```bash
pip install -r requirements.txt
