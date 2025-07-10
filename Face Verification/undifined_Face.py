import os
import time
import torch
import ssl
import uuid
import cv2
import threading
import logging
import numpy as np
import paho.mqtt.client as mqtt
import torchvision.transforms as transforms
from datetime import datetime
from facenet_pytorch import InceptionResnetV1
from ultralytics import YOLO

from upload_image_to_db import upload_image_to_db
from generate_embeddings import process_folders
from database_utils import load_saved_embeddings, update_database_from_folders
from sync_from_database import sync_database

# ============== Logging Setup ============== #
logging.basicConfig(
    filename="main_system.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ============== Configuration ============== #
BROKER = "2510b2ca3c0d421d82a56d56fa9e2f08.s1.eu.hivemq.cloud"
PORT = 8883
USERNAME = "project"
PASSWORD = "project123P"
KEEP_ALIVE = 60

TOPIC_PUBLISH = "face_recognition/results"
TOPIC_CONTROL = "camera/control"
CLIENT_ID_FACE = f"Face_Client_{uuid.uuid4().hex[:8]}"
CLIENT_ID_CONTROL = f"Control_Client_{uuid.uuid4().hex[:8]}"

BASE_PATH = os.getcwd()
IMAGE_DIR = os.path.join(BASE_PATH, "user_images")
EMBEDDING_DIR = os.path.join(BASE_PATH, "user_embeddings")
INPUT_SHAPE = (160, 160)
THRESHOLD = 0.77
RESIZE_FOR_YOLO = (320, 240)

# ============== Flags ============== #
face_verification_running = False
verification_thread = None

# ============== Load Models Once ============== #
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
logging.info("Loading models and syncing database...")

resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)
yolo = YOLO("best.pt")
yolo.predict(np.zeros((240, 320, 3), dtype=np.uint8), verbose=False)
transform = transforms.Compose([transforms.ToTensor()])

features_mapping = {}
sync_database(IMAGE_DIR)
process_folders(IMAGE_DIR, EMBEDDING_DIR)
update_database_from_folders(EMBEDDING_DIR, features_mapping)
saved_embeddings = load_saved_embeddings(features_mapping)
logging.info("System is ready.")

# ============== Face Detection ============== #
def detect_faces(model, frame):
    small = cv2.resize(frame, RESIZE_FOR_YOLO)
    results = model.predict(small, stream=False, verbose=False)
    boxes = results[0].boxes
    if boxes is None:
        return []
    scale_x = frame.shape[1] / RESIZE_FOR_YOLO[0]
    scale_y = frame.shape[0] / RESIZE_FOR_YOLO[1]
    return [
        [int(x1 * scale_x), int(y1 * scale_y), int(x2 * scale_x), int(y2 * scale_y)]
        for x1, y1, x2, y2 in boxes.xyxy.cpu().numpy()
    ]

def compare_embeddings_batch(live_batch, saved_embeddings, threshold=THRESHOLD):
    identities = []
    for live_embed in live_batch:
        identity, min_dist = "Unknown", float("inf")
        for name, emb_list in saved_embeddings.items():
            for emb in emb_list:
                dist = torch.dist(live_embed, emb.to(live_embed.device)).item()
                if dist < min_dist:
                    identity = name
                    min_dist = dist
        if min_dist > threshold:
            identity = "Unknown"
        identities.append((identity, min_dist))
    return identities

# ============== Face Verification Thread ============== #
def face_verification_loop():
    global face_verification_running
    cap = cv2.VideoCapture(0)
    last_unknown_time = None
    unknown_saved = False
    capture_delay = 2

    while face_verification_running and cap.isOpened():
        ret, frame = cap.read()
        if not ret or not face_verification_running:
            break

        coords = detect_faces(yolo, frame)
        face_tensors = []
        face_boxes = []

        for x1, y1, x2, y2 in coords:
            face = frame[y1:y2, x1:x2]
            face = cv2.resize(face, INPUT_SHAPE)
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            tensor = transform(face).unsqueeze(0).to(device)
            face_tensors.append(tensor)
            face_boxes.append((x1, y1, x2, y2))

        if face_tensors:
            batch = torch.cat(face_tensors)
            with torch.no_grad():
                embeddings = resnet(batch)
            identities = compare_embeddings_batch(embeddings, saved_embeddings)

            for (identity, dist), (x1, y1, x2, y2) in zip(identities, face_boxes):
                color = (0, 255, 0) if identity != "Unknown" else (0, 0, 255)
                label = f"{identity} ({dist:.2f})"
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

                if identity == "Unknown":
                    current_time = time.time()
                    if last_unknown_time is None:
                        last_unknown_time = current_time
                        unknown_saved = False
                    elif not unknown_saved and (current_time - last_unknown_time >= capture_delay):
                        _, img_encoded = cv2.imencode('.jpg', frame)
                        upload_image_to_db(img_encoded.tobytes(), datetime.now())
                        unknown_saved = True
                else:
                    mqtt_face.publish(TOPIC_PUBLISH, "ON")

        cv2.imshow("Face Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            face_verification_running = False
            break

    cap.release()
    cv2.destroyAllWindows()

# ============== MQTT Callbacks ============== #
def on_connect_control(client, userdata, flags, rc):
    client.subscribe(TOPIC_CONTROL)

def on_message_control(client, userdata, msg):
    global face_verification_running, verification_thread
    command = msg.payload.decode().lower()
    print(f"[MQTT] Received command: {command.upper()}")
    logging.info(f"MQTT command received: {command}")

    if command == "on" and not face_verification_running:
        face_verification_running = True
        verification_thread = threading.Thread(target=face_verification_loop)
        verification_thread.start()
    elif command == "off":
        face_verification_running = False
        if verification_thread is not None and verification_thread.is_alive():
            verification_thread.join()
        logging.info("Face recognition stopped via MQTT.")

# ============== MQTT Setup ============== #
mqtt_face = mqtt.Client(client_id=CLIENT_ID_FACE)
mqtt_face.username_pw_set(USERNAME, PASSWORD)
mqtt_face.tls_set(tls_version=ssl.PROTOCOL_TLSv1_2)
mqtt_face.connect(BROKER, PORT, KEEP_ALIVE)
mqtt_face.loop_start()

mqtt_control = mqtt.Client(client_id=CLIENT_ID_CONTROL)
mqtt_control.username_pw_set(USERNAME, PASSWORD)
mqtt_control.tls_set(tls_version=ssl.PROTOCOL_TLSv1_2)
mqtt_control.on_connect = on_connect_control
mqtt_control.on_message = on_message_control
mqtt_control.connect(BROKER, PORT, KEEP_ALIVE)
mqtt_control.loop_forever()