import os
import shutil
import logging
import hashlib
from sqlalchemy import create_engine, Table, MetaData, select

# ======================= CONFIG ======================= #
DATABASE_URL = "postgresql://postgres:GxaExhHWMCwhpRIHyqLeJYLEvDuvjdQO@trolley.proxy.rlwy.net:55305/railway"
TABLE_NAME = "new_users"
ID_TRACK_FILE = "last_id.txt"

# ======================= Logging ======================= #
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="sync_database.log"
)

# ======================= Helpers ======================= #
def hash_bytes(data):
    return hashlib.md5(data).hexdigest()

def file_changed(file_path, new_data):
    """Check if file exists and contents differ from new_data."""
    if not os.path.exists(file_path):
        return True
    with open(file_path, "rb") as f:
        existing_data = f.read()
    return hash_bytes(existing_data) != hash_bytes(new_data)

# ======================= Sync Function ======================= #
def sync_database(image_dir):
    """
    Synchronize PostgreSQL image data with local folders:
    - Download new/updated users.
    - Remove folders of deleted users.
    - Avoid redundant writes using hashing.
    """
    engine = create_engine(DATABASE_URL, future=True)

    with engine.connect() as conn:
        metadata = MetaData()
        metadata.reflect(bind=engine)
        data_table = metadata.tables.get(TABLE_NAME)

        if data_table is None:
            logging.error(f"❌ Table '{TABLE_NAME}' not found in database.")
            return

        # Track last synced ID
        track_file_path = os.path.join(image_dir, ID_TRACK_FILE)
        last_id = 0
        if os.path.exists(track_file_path):
            with open(track_file_path, "r") as f:
                try:
                    last_id = int(f.read().strip())
                except ValueError:
                    logging.warning("Invalid last_id.txt format, resetting to 0.")
                    last_id = 0

        # Fetch current users from DB
        all_users_result = conn.execute(select(data_table)).fetchall()
        user_names = {row.username for row in all_users_result}
        max_id = last_id

        # Remove old folders
        excluded = {"__pycache__", "ai_env", "user_embeddings", "best.pt", "user_embeddings_pt"}
        for folder in os.listdir(image_dir):
            full_path = os.path.join(image_dir, folder)
            if not os.path.isdir(full_path):
                continue
            folder_base = folder.replace("_pt", "")
            if folder_base in excluded or folder_base in user_names:
                continue
            try:
                shutil.rmtree(full_path)
                logging.info(f"🗑 Deleted folder for removed user: {folder}")
            except Exception as e:
                logging.error(f"❌ Failed to delete folder '{folder}': {e}")

        # Update/add users
        for row in all_users_result:
            username = row.username
            user_id = row.id
            user_folder = os.path.join(image_dir, username)

            if user_id > last_id or not os.path.exists(user_folder):
                os.makedirs(user_folder, exist_ok=True)

            # Save images only if changed
            try:
                paths = {
                    "image1.jpg": row.image1,
                    "image2.jpg": row.image2,
                    "image3.jpg": row.image3
                }
                for fname, data in paths.items():
                    fpath = os.path.join(user_folder, fname)
                    if file_changed(fpath, data):
                        with open(fpath, "wb") as f:
                            f.write(data)

                logging.info(f"✅ Synced images for user: {username}")
            except Exception as e:
                logging.error(f"❌ Failed to sync user '{username}': {e}")

            max_id = max(max_id, user_id)

        # Update last ID tracker
        with open(track_file_path, "w") as f:
            f.write(str(max_id))

        logging.info("✅ Sync complete.")
