import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Command_extraction.command_extract import extract_command_data
from Recorder import recorder
from Speaker import speaker
from SpeechToText import model
from command_execute.mqtt import mqtt_send
from sql_modes import mode_database
from TextPreProcessing import text_processing

MQTT_USERNAME = "abdo"
MQTT_PASSWORD = "234"

def command_execute(command:dict) -> str | None:
    if command['intent'] == 'turn_on':
        mqtt_command =  'ON'
        if command['device'] == 'camera' or command['device'] == 'face id camera':
            response_msg = f"Turning on The Face ID Camera"
            topic = "home/security/camera"
        
        elif command['device'] == 'lights' or 'lamp' or 'light' :
            topic = f'home/{command['location']}/lamp'
            

        else:
            topic = f"home/{command['location']}/{command['device']}"

        response_msg = f"Turning on {command['device']} at {command['location']}"

    elif command['intent'] == 'turn_off':
        mqtt_command = 'OFF'
        if command['device'] == 'lights' or 'lamp' or 'light':
            topic = f'home/{command['location']}/lamp'
            response_msg = f"Turning off lights at {command['location']}"
        else:
            topic = f"home/{command['location']}/{command['device']}"
            response_msg = f"Turning off {command['device']} at {command['location']}"

    elif command['intent'] == 'set_temperature': 

        mqtt_command = f'{command['value']}'
        topic = f"home/{command['location']}/temperature"
        response_msg = f"Setting temperature of {command['device']} at {command['location']} to {command['value']}"
        
    elif command['intent'] == 'set_fan_speed':

        mqtt_command =f'{command['value']}'
        topic = f"home/{command['location']}/fan"
        response_msg = f"Setting fan speed at {command['location']} to {command['value']}"

    elif command['intent'] == 'open_door':

        mqtt_command =  'on'
        topic = f"home/security/door"
        response_msg = "Opening the door"

    elif command['intent'] == 'close_door':
        
        mqtt_command =  'off'
        topic = f"home/security/door"
        response_msg = "Closing the door"

    elif command['intent'] == 'execute_mode':
        mqtt_command = None
        mode_name = command['mode']
        
        print(f"Mode name: {mode_name}")
        db = mode_database.ModeDatabase()
        response_msg = f"Activating mode {mode_name}"
        mode = db.get_mode_by_name(mode_name)
        for cmd in mode['commands']:
            command_execute(cmd)

    elif command['intent'] == 'add_mode':
        mqtt_command = None
        speaker.text_to_sound('What is the mode name?')
        recorder.record_audio_silence('mode_name.wav')
        mode_name = model.SpeechToTextPipeline().transcribe('mode_name.wav')
        mode_name = text_processing.text_preprocessor(mode_name)
        print(f"Mode name: {mode_name}")
        db = mode_database.ModeDatabase()
        db.create_mode(mode_name)
        response_msg = f"Mode {mode_name} created successfully"

    else:
        mqtt_command = None
        print("Invalid command!")
        response_msg = None
    
    if mqtt_command:
        mqtt_send(mqtt_command,topic=topic)

    return response_msg



if __name__ == "__main__":

    
    from TextPreProcessing import text_processing


    test_phrases = [
        'activate study mode',
        'turn on the light in the living room',
        'turn off the light in the living room',
        'set the temperature in the living room to 25',
        'open the door',
        'turn on the camera',
        
     ]
    

    for text in test_phrases:
        print(f"Input: {text}")
        text = text_processing.text_preprocessor(text)
        command = extract_command_data(text)
        print(f"Command: {command}")
        response = command_execute(command)
        print(response)

        print('-' * 50)


#     from mqtt import mqtt_send
#     command_list = [
#         {
#         'intent': 'turn_on',
#         'device': 'light',
#         'location': 'living room',
#         'temperature': None
#     },
#     {
#         'intent': 'turn_on',
#         'device': 'light',
#         'location': None,
#         'value': None
#     },
#     {
#         'intent': 'turn_off',
#         'device': 'light',
#         'location': None,
#         'value': None
#     }
#     ]
#     previous_command = {
#         'device': 'light',
#         'location': None,
#         'value': None
#     }
#     for command in command_list:
#         response = command_execute(command,previous_command=previous_command)  # Expected output: Turning on light at living room
#         print(response)
#         previous_command = command




