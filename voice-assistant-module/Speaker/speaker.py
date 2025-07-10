import pyttsx3


# Initialize the TTS engine
engine = pyttsx3.init()

# Set properties (optional)
engine.setProperty('rate', 180)  # Speed of speech
engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)

def text_to_sound(word:str):
    # Convert text to speech and wait for completion
    engine.say(word)
    engine.runAndWait()






if __name__ == "__main__":
    text_to_sound("Hello, how are you today?")

    