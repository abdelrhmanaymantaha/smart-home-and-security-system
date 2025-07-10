import os
import cv2
import torch
import contextlib
import torchvision.transforms as transforms
import torch.nn.functional as F
from facenet_pytorch import InceptionResnetV1
from ultralytics import YOLO
import logging

# ========================== Device Setup ========================== #
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ========================== Model Initialization ========================== #
resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)
yolo = YOLO('best.pt').to(device)
transform = transforms.Compose([transforms.ToTensor()])
INPUT_SHAPE = (160, 160)
YOLO_RESIZE = (320, 240)

@contextlib.contextmanager
def suppress_output():
    with open(os.devnull, 'w') as devnull:
        old_stdout = os.dup(1)
        old_stderr = os.dup(2)
        os.dup2(devnull.fileno(), 1)
        os.dup2(devnull.fileno(), 2)
        try:
            yield
        finally:
            os.dup2(old_stdout, 1)
            os.dup2(old_stderr, 2)

# ========================== Face Detection ========================== #
def detect_faces_yolo(model, img):
    resized = cv2.resize(img, YOLO_RESIZE)
    with suppress_output():
        results = model(resized, verbose=False)
    boxes = results[0].boxes
    if not boxes:
        return []

    # إعادة تحجيم الإحداثيات إلى الصورة الأصلية
    scale_x = img.shape[1] / YOLO_RESIZE[0]
    scale_y = img.shape[0] / YOLO_RESIZE[1]
    return [
        [int(x1 * scale_x), int(y1 * scale_y), int(x2 * scale_x), int(y2 * scale_y)]
        for x1, y1, x2, y2 in boxes.xyxy.cpu().numpy()
    ]

# ========================== Convert Images to .pt ========================== #
def convert_images_to_pt(folder_path, person_name, pt_folder_path):
    os.makedirs(pt_folder_path, exist_ok=True)

    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if not image_files:
        logging.warning(f"No images found in: {folder_path}")
        return False

    existing_pts = set(os.listdir(pt_folder_path))
    new_pts = set()
    processed = 0

    for idx, img_file in enumerate(image_files, start=1):
        pt_filename = f"{person_name}_features_{idx}.pt"
        pt_path = os.path.join(pt_folder_path, pt_filename)
        new_pts.add(pt_filename)

        img_path = os.path.join(folder_path, img_file)
        if os.path.exists(pt_path) and os.path.getmtime(img_path) <= os.path.getmtime(pt_path):
            continue  # Skip if not modified

        image = cv2.imread(img_path)
        if image is None:
            continue

        faces = detect_faces_yolo(yolo, image)
        if not faces:
            continue

        x1, y1, x2, y2 = faces[0]
        face = image[y1:y2, x1:x2]
        face = cv2.resize(face, INPUT_SHAPE)
        face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
        tensor_image = transform(face).unsqueeze(0).to(device)

        with torch.no_grad():
            embedding = resnet(tensor_image)
            embedding = F.normalize(embedding, p=2, dim=1).cpu()

        torch.save(embedding, pt_path)
        processed += 1

    # حذف ملفات .pt التي لم يتم تحديثها
    obsolete_pts = existing_pts - new_pts
    for filename in obsolete_pts:
        try:
            os.remove(os.path.join(pt_folder_path, filename))
        except Exception as e:
            logging.warning(f"Failed to remove obsolete embedding: {filename} | {e}")

    if processed > 0:
        logging.info(f"{person_name}: {processed} embeddings updated.")
    return processed > 0

# ========================== Process All Folders ========================== #
def process_folders(image_dir, embedding_dir):
    for folder_name in os.listdir(image_dir):
        folder_path = os.path.join(image_dir, folder_name)
        pt_folder_path = os.path.join(embedding_dir, f"{folder_name}_pt")

        if not os.path.isdir(folder_path) or folder_name.endswith('_pt'):
            continue

        convert_images_to_pt(folder_path, folder_name, pt_folder_path)

# ========================== Manual Test ========================== #
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    base_path = os.getcwd()
    images_base = os.path.join(base_path, "user_images")
    embeddings_base = os.path.join(base_path, "user_embeddings")
    process_folders(images_base, embeddings_base)
