# Website-smarthome

A smart home web application built with Flask, SQLAlchemy, JWT authentication, and MQTT integration. This project allows users to monitor and control smart home devices, upload images, and manage user authentication.

## Features
- User registration and login with JWT authentication
- Real-time sensor data via MQTT
- Image upload and gallery per user
- Device control interface
- Responsive web UI (HTML/CSS/JS)

## Project Structure
- `app.py` - Main Flask application
- `asgi_app.py` - ASGI adapter for running with Uvicorn
- `config.py` - Configuration settings
- `init.py` - App and database initialization
- `uploads/` - User-uploaded images
- `static/` - Static files (CSS, JS, images)
- `templates/` - HTML templates
- `instance/` - Database file

## Setup
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the app (development):**
   ```bash
   python app.py
   ```
3. **Run with Uvicorn (production/ASGI):**
   ```bash
   uvicorn asgi_app:asgi_app --host 0.0.0.0 --port 8000
   ```

## Configuration
- Edit `config.py` for environment variables and secrets.
- Use environment variables for sensitive data in production.

## Deployment (Railway example)
- **Build command:**
  ```bash
  pip install -r requirements.txt
  ```
- **Start command:**
  ```bash
  uvicorn asgi_app:asgi_app --host 0.0.0.0 --port 8000
  ```

## Security Notes
- Never commit secrets or credentials to version control.
- Validate and sanitize all uploads.
- Restrict CORS origins in production.

## License
MIT
