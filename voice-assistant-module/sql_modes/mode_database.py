import json  # Import the json module

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from Command_extraction import command_extract
from TextPreProcessing import text_processing
from SpeechToText import model
from Speaker import speaker
from Recorder import recorder


Base = declarative_base()

class Mode(Base):
    __tablename__ = 'modes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    commands = relationship('Command', back_populates='mode', cascade='all, delete-orphan')

class Command(Base):
    __tablename__ = 'commands'
    id = Column(Integer, primary_key=True, autoincrement=True)
    mode_id = Column(Integer, ForeignKey('modes.id'))
    command = Column(String, nullable=False)
    mode = relationship('Mode', back_populates='commands')

class ModeDatabase:
    def __init__(self, db_name='sqlite:///modes.db'):
        self.engine = create_engine(db_name)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_mode(self, mode_name, commands):
        session = self.Session()
        if session.query(Mode).filter_by(name=mode_name).first():
            session.close()
            raise ValueError(f"Mode with name '{mode_name}' already exists.")
        
        # Convert each command dictionary to a JSON string
        mode = Mode(name=mode_name, commands=[Command(command=json.dumps(cmd)) for cmd in commands])
        session.add(mode)
        session.commit()
        session.close()

    def get_mode_by_name(self, mode_name):
        session = self.Session()
        mode = session.query(Mode).filter_by(name=mode_name).first()
        if mode:
            # Convert each command JSON string back to a dictionary
            mode_data = {
                'id': mode.id,
                'name': mode.name,
                'commands': [json.loads(cmd.command) for cmd in mode.commands]
            }
            session.close()
            return mode_data
        else:
            session.close()
            raise ValueError(f"Mode with name '{mode_name}' does not exist.")

    def update_mode_by_name(self, mode_name, commands):
        session = self.Session()
        mode = session.query(Mode).filter_by(name=mode_name).first()
        if not mode:
            session.close()
            raise ValueError(f"Mode with name '{mode_name}' does not exist.")
        
        # Convert each command dictionary to a JSON string
        mode.commands = [Command(command=json.dumps(cmd)) for cmd in commands]
        session.commit()
        session.close()

    def get_user_commands(self):
        pipline = model.SpeechToTextPipeline()
        commands_list = []
        while True:
            speaker.text_to_sound('Please say your command')
            recorder.record_audio_silence('command.wav')
            text = pipline.transcribe('command.wav')
            preprocessed_text = text_processing.text_preprocessor(text)
            print(f"User said: {preprocessed_text}")
            
            if preprocessed_text == 'stop':                                                                                                                          
                print(commands_list)
                return commands_list
            
            command = command_extract.extract_command_data(preprocessed_text)
            print(f"User command: {command}")
            if command['intent'] == 'unsupported':
                speaker.text_to_sound("Sorry, I didn't understand that command. Please try again.")
                continue
            else:
                commands_list.append(command)

    def create_mode(self, mode_name):

        print(f"enter the commands of {mode_name}")
        command_list = self.get_user_commands()
        self.add_mode(mode_name=mode_name, commands=command_list)
        print('your mode created successfully')
    
    def get_all_modes(self):
        session = self.Session()
        modes = session.query(Mode).all()
        mode_names = [mode.name for mode in modes]  # Extract mode names
        session.close()
        return mode_names



    def close(self):
        self.engine.dispose()

# Example usage
if __name__ == '__main__':
    db = ModeDatabase()

    print(db.get_all_modes())
    db.close()
