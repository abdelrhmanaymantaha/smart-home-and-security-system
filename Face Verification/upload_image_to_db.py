from sqlalchemy import create_engine, Table, Column, MetaData, Integer, LargeBinary, DateTime
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import logging

# =================== Logging Setup =================== #
logging.basicConfig(
    filename="face_recognition.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# =================== Database Setup =================== #
DATABASE_URL = "postgresql://postgres:GxaExhHWMCwhpRIHyqLeJYLEvDuvjdQO@trolley.proxy.rlwy.net:55305/railway"
engine = create_engine(DATABASE_URL, future=True)  # ✅ future mode improves performance slightly
metadata = MetaData()

# =================== Table Definition =================== #
image_table = Table(
    "ai_security_images", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("image_data", LargeBinary),
    Column("timestamp", DateTime)
)

# Prepare session factory once
SessionFactory = sessionmaker(bind=engine, expire_on_commit=False)  # ✅ improves commit performance

# =================== Upload Function =================== #
def upload_image_to_db(image_data: bytes, timestamp: datetime):
    """
    Upload a single image (in bytes) with a timestamp to the PostgreSQL database.
    """
    session = SessionFactory()
    try:
        session.execute(
            image_table.insert().values(image_data=image_data, timestamp=timestamp)
        )
        session.commit()
        logging.debug("Image uploaded to database.")  # ✅ use debug instead of info inside loop
    except Exception as e:
        logging.error(f"[ERROR] Failed to upload image to DB: {e}")
    finally:
        session.close()

# =================== Manual Test =================== #
if __name__ == "__main__":
    try:
        with open("unknown_20250410_104335.jpg", "rb") as f:
            img_data = f.read()
            upload_image_to_db(img_data, datetime.now())
        print("✅ Test upload completed.")
    except FileNotFoundError:
        logging.warning("Test image not found. Manual test skipped.")
