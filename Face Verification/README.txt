# Smart Home Face Recognition System

A secure and intelligent face recognition system built for Smart Home environments. It utilizes real-time camera input, YOLO for face detection, FaceNet for recognition, and MQTT for smart control. All detected data is stored and updated through a PostgreSQL database.

---

## 📁 Project Structure

```
project_root/
├── ai_env/                       # Virtual environment
├── undifined_Face.py             # Controls recognition via MQTT (on/off) and Main face recognition application
├── generate_embeddings.py        # Converts face images to .pt embeddings
├── database_utils.py             # Loads and maps .pt embeddings
├── sync_from_database.py         # Syncs face images from PostgreSQL DB
├── upload_image_to_db.py         # Uploads unknown faces to database
├── performance_log.csv           # Logs system performance (CPU, RAM)
├── face_recognition.log          # Main logging file
└── last_id.txt                   # Tracks last synced user ID

```

---

## ✅ Requirements

Make sure you have Python 3.8+ and `virtualenv` installed.

### Setup Virtual Environment:

```bash
python -m venv ai_env
ai_env\Scripts\activate        # On Windows
pip install -r requirements.txt
```

### Required Libraries:

* torch
* facenet-pytorch
* ultralytics
* opencv-python
* torchvision
* paho-mqtt
* sqlalchemy
* psycopg2-binary

---

## 🚀 Project Flow & Execution

### 1. 🔁 `sync_from_database.py`

* Fetches user images from the PostgreSQL `new_users` table.
* Creates a local folder per user (if not exists).
* Deletes folders for users removed from DB.

**Run once before using the system:**

```bash
python sync_from_database.py
```

---

### 2. 🧠 `generate_embeddings.py`

* Detects faces in each user folder using YOLO.
* Extracts and normalizes 512D embeddings using FaceNet.
* Stores them as `.pt` files inside folders named `username_pt/`.

**You can also run this after syncing or updating users:**

```bash
python generate_embeddings.py
```

---

### 3. 🧩 `database_utils.py`

* Used internally by `main.py` and `mqtt_control_listener.py`.
* Loads and maps `.pt` embeddings to user names.

> 📌 No need to run it manually.

---

### 4. 🎮 `mqtt_control_listener.py`

* Subscribes to MQTT topic `camera/control`
* Accepts:

  * `on` → Starts face recognition in background
  * `off` → Terminates face recognition
* Automatically sends `ON` to `face_recognition/results` when a known face is detected
* Automatically uploads an image of an `Unknown` face if seen for more than 2s

**Run this to start listening for control signals:**

```bash
python mqtt_control_listener.py
```

---

### 5. 📸 `main.py`

* Can be run manually instead of MQTT trigger.
* Performs live face recognition from webcam.
* Publishes `ON` / `OFF` status via MQTT.
* Logs CPU & memory usage into `performance_log.csv`

**Example Run:**

```bash
python main.py
```

> ✔ Will auto-sync images + regenerate embeddings before starting.

---

## 🗄️ `upload_image_to_db.py`

* Contains function `upload_image_to_db(image_data, timestamp)`
* Used inside other scripts to insert unknown face images into the `security_db` table.

**Manual Testing:**

```python
from upload_image_to_db import upload_image_to_db
from datetime import datetime

with open("unknown_test.jpg", "rb") as f:
    upload_image_to_db(f.read(), datetime.now())
```

---

## 📡 MQTT Topics

* `camera/control` → receives `on` / `off`
* `face_recognition/results` → sends `ON` when face is known, `OFF` otherwise

---

## 📊 Logging & Monitoring

* Logs saved in `face_recognition.log`
* Performance metrics (CPU, RAM) saved to `performance_log.csv`

---

## 🔐 Security Notes

* Uses TLS (`ssl.PROTOCOL_TLSv1_2`) for secure MQTT.
* Database credentials stored directly in the code (can be moved to `.env` in production).

---

## 📌 Future Enhancements

* Firebase or Pushbullet integration for real-time mobile/web alerts
* Face registration GUI for new users
* Admin panel to review unknown detections
* Tracking multiple faces simultaneously with more robust comparison logic
* Scheduled database cleanup for old unknown entries

---

## 👨‍💻 Developed by

Mohamed Ebrahim - 2025

> "Built to recognize, secure, and automate."
