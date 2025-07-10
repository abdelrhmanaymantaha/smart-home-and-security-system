import requests
import sys
import os

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
try:
    from config_secrets import HUGGING_FACE_API_TOKEN
except ImportError:
    HUGGING_FACE_API_TOKEN = os.getenv('HUGGING_FACE_API_TOKEN', '')

# Hugging Face API endpoint and headers
API_URL = "https://api-inference.huggingface.co/models/openai/whisper-medium.en"
headers = {"Authorization": f"Bearer {HUGGING_FACE_API_TOKEN}"}

def query(filename):
    """
    Send an audio file to the Hugging Face API for transcription.
    
    Args:
        filename (str): Path to the audio file.
    
    Returns:
        str: The transcribed text from the audio file.
    
    Raises:
        Exception: If an error occurs during the process.
    """
    try:
        # Open the file in binary mode
        with open(filename, "rb") as f:
            data = f.read()
        
        # Send the request to the Hugging Face API
        response = requests.post(API_URL, headers=headers, data=data)
        
        # Check if the request was successful
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        
        # Parse the JSON response
        data_query = response.json()
        
        # Check if the response contains the "text" key
        if "text" in data_query:
            return str(data_query["text"])
        else:
            raise KeyError("The API response does not contain the 'text' key.")
    
    except FileNotFoundError:
        return "Error: The specified file does not exist."
    except requests.exceptions.HTTPError as e:
        return f"HTTP Error: {e}"
    except requests.exceptions.RequestException as e:
        return f"Request Error: {e}"
    except KeyError as e:
        return f"Key Error: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"