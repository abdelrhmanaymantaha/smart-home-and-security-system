# Smart Home and Security System

A comprehensive smart home automation and security system that integrates face recognition, voice control, and web-based monitoring. This project provides a complete solution for modern smart home management with multiple interfaces and security features.

## 🏗️ System Architecture

The system consists of three main modules that work together to provide a complete smart home experience:

```
Smart Home and Security System/
├── Face Verification/           # AI-powered face recognition security
├── voice-assistant-module/      # Voice control and command processing
├── Website-smarthome/          # Web interface for monitoring and control
└── [Embedded Systems/]         # Hardware integration (planned)
└── [Hardware/]                 # IoT devices and sensors (planned)
```

## 🚀 Features

### 🔐 Security & Access Control
- **Real-time Face Recognition**: AI-powered face detection and recognition using YOLO and FaceNet
- **Unknown Face Detection**: Automatic capture and storage of unrecognized faces
- **MQTT-based Control**: Remote activation/deactivation of security features
- **Database Integration**: PostgreSQL storage for user data and security logs

### 🎤 Voice Assistant
- **Wake Word Detection**: "Hey Whisper" activation using Porcupine
- **Natural Language Processing**: Intent recognition and command extraction
- **Multi-device Control**: Voice commands for lights, fans, temperature, and more
- **Voice Feedback**: Text-to-speech responses for user confirmation

### 🌐 Web Interface
- **Real-time Monitoring**: Live sensor data display (temperature, humidity, gas, soil)
- **Device Control**: Web-based control panel for all smart devices
- **User Management**: JWT-based authentication and user registration
- **Image Gallery**: Personal image storage and management
- **Security Alerts**: Warning system for unknown face detections

### 📊 Monitoring & Analytics
- **Sensor Integration**: Temperature, humidity, gas, and soil moisture sensors
- **Performance Logging**: CPU and memory usage tracking
- **Real-time Updates**: MQTT-based live data streaming
- **Historical Data**: Database storage for trend analysis

## 🛠️ Technology Stack

### Face Recognition Module
- **AI Models**: YOLO (face detection), FaceNet (face recognition)
- **Framework**: PyTorch, OpenCV
- **Communication**: MQTT with TLS encryption
- **Database**: PostgreSQL with SQLAlchemy
- **Languages**: Python 3.8+

### Voice Assistant Module
- **Speech Recognition**: OpenAI Whisper
- **Wake Word**: Porcupine
- **NLP**: Custom intent recognition with scikit-learn
- **Text-to-Speech**: pyttsx3
- **Audio Processing**: PyAudio
- **Communication**: MQTT

### Web Interface
- **Backend**: Flask with ASGI support
- **Authentication**: JWT tokens
- **Database**: PostgreSQL
- **Real-time**: MQTT integration
- **Frontend**: HTML5, CSS3, JavaScript
- **Deployment**: Uvicorn/ASGI ready

## 📦 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- PostgreSQL database
- MQTT broker (HiveMQ Cloud recommended)
- Microphone and camera for voice/face features

### 1. Clone the Repository
```bash
git clone <repository-url>
cd smart-home-and-security-system
```

### 2. Database Setup
```bash
# Install PostgreSQL and create database
createdb smart_home_db

# Set up environment variables
cp .env.example .env
# Edit .env with your database and MQTT credentials
```

### 3. Face Recognition Module
```bash
cd Face\ Verification/
python -m venv ai_env
ai_env\Scripts\activate  # Windows
source ai_env/bin/activate  # Linux/Mac
pip install -r requirements.txt

# Initial setup
python sync_from_database.py
python generate_embeddings.py
```

### 4. Voice Assistant Module
```bash
cd voice-assistant-module/
pip install -r requirements.txt

# Download required models
# The system will automatically download Whisper model on first run
```

### 5. Web Interface
```bash
cd Website-smarthome/
pip install -r requirements.txt

# Set up environment variables in config.py
# Run the application
python app.py
```

## 🚀 Usage

### Starting the System

1. **Start the Web Interface**:
   ```bash
   cd Website-smarthome/
   python app.py
   # Access at http://localhost:5000
   ```

2. **Start Face Recognition**:
   ```bash
   cd Face\ Verification/
   python undifined_Face.py
   # System will listen for MQTT commands
   ```

3. **Start Voice Assistant**:
   ```bash
   cd voice-assistant-module/
   python main.py
   # Say "Hey Whisper" to activate
   ```

### Voice Commands Examples
- "Turn on the living room lights"
- "Set the kitchen temperature to 25 degrees"
- "Turn off the bedroom fan"
- "Set fan speed to 3 in the living room"

### Web Interface Features
- **Login/Register**: Create user accounts
- **Monitor**: View real-time sensor data
- **Control**: Manage devices through web interface
- **Gallery**: Upload and manage personal images
- **Warning**: View security alerts

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
# Database
DATABASE_URI=postgresql://username:password@localhost/smart_home_db
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret

# MQTT Configuration
MQTT_BROKER=your-mqtt-broker.com
MQTT_PORT=8883
MQTT_USER=your-mqtt-username
MQTT_PASSWORD=your-mqtt-password

# Face Recognition
FACE_RECOGNITION_THRESHOLD=0.77
CAMERA_INDEX=0

# Voice Assistant
PORCUPINE_ACCESS_KEY=your-porcupine-key
```

### MQTT Topics
- `camera/control` - Face recognition on/off
- `face_recognition/results` - Face detection results
- `home/{room}/{sensor}` - Sensor data
- `home/{room}/{device}` - Device control
- `voice/command` - Voice command processing

## 📊 Database Schema

### Users Table
- User authentication and management
- JWT token storage
- User preferences

### NewUsers Table
- Face recognition user data
- Image storage and embeddings
- User metadata

### SecurityDB Table
- Unknown face captures
- Security event logs
- Timestamp and location data

### SensorData Table
- Real-time sensor readings
- Historical data storage
- Performance metrics

## 🔒 Security Features

- **TLS Encryption**: All MQTT communications are encrypted
- **JWT Authentication**: Secure web interface access
- **Face Recognition**: Biometric access control
- **Unknown Face Detection**: Security monitoring
- **Database Security**: Encrypted credentials and data

## 📈 Performance & Monitoring

### Logging
- Face recognition logs: `face_recognition.log`
- Performance metrics: `performance_log.csv`
- System logs: `main_system.log`

### Metrics Tracked
- CPU and memory usage
- Face recognition accuracy
- Response times
- Error rates

## 🔮 Future Enhancements

### Planned Features
- **Mobile App**: iOS/Android companion app
- **Cloud Integration**: AWS/Azure deployment
- **Advanced Analytics**: Machine learning insights
- **Multi-language Support**: Internationalization
- **API Documentation**: RESTful API endpoints

### Embedded Systems Integration
- **ESP32/ESP8266**: IoT device control
- **Arduino**: Sensor integration
- **Raspberry Pi**: Local processing hub
- **Custom PCBs**: Specialized hardware

### Hardware Integration
- **Smart Sensors**: Temperature, humidity, motion
- **Actuators**: Relays, motors, servos
- **Displays**: LCD screens, LED indicators
- **Cameras**: IP cameras, USB cameras
- **Audio**: Microphones, speakers

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Development Team

- **Face Recognition Module** - AI and Computer Vision
- **Voice Assistant Module** - NLP and Speech Processing
- **Web Interface** - Full-stack Development
- **Embeded System** -- hardware and ESP32 to emulate home devices

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation in each module
- Review the logs for debugging information

## 📚 Documentation

- [Face Recognition Documentation](Face%20Verification/README.txt)
- [Voice Assistant Documentation](voice-assistant-module/readme.md)
- [Web Interface Documentation](Website-smarthome/README.md)

---

**Built with ❤️ for smart home automation and security** 
