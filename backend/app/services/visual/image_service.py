import os
import uuid
import cv2
from fastapi import UploadFile
from PIL import Image

# -------------------------
# Configuration
# -------------------------

UPLOAD_FOLDER = "uploads/visual"

ALLOWED_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp"
}

MAX_WIDTH = 1920
MAX_HEIGHT = 1080


# -------------------------
# Save Uploaded Image
# -------------------------

async def save_uploaded_image(file: UploadFile):

    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            "Only PNG, JPG, JPEG and WEBP images are supported."
        )

    os.makedirs(
        UPLOAD_FOLDER,
        exist_ok=True
    )

    filename = f"{uuid.uuid4()}{extension}"

    file_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    with open(file_path, "wb") as image:
        image.write(await file.read())

    preprocess_image(file_path)

    return file_path


# -------------------------
# Image Preprocessing
# -------------------------

def preprocess_image(image_path):

    image = Image.open(image_path)

    # Convert RGBA → RGB
    if image.mode != "RGB":
        image = image.convert("RGB")

    # Resize very large screenshots
    width, height = image.size

    if width > MAX_WIDTH or height > MAX_HEIGHT:

        image.thumbnail(
            (MAX_WIDTH, MAX_HEIGHT)
        )

    image.save(image_path)

    return image_path


# -------------------------
# OpenCV Image
# -------------------------

def load_cv_image(image_path):

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Unable to read uploaded image.")

    return image