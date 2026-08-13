import cv2
import imagehash
from PIL import Image
from skimage.metrics import structural_similarity as ssim

from app.services.visual.clip_service import clip_similarity
from app.services.visual.color_service import calculate_color_similarity
from app.services.visual.layout_service import calculate_layout_similarity


def compare_brand(uploaded_image, reference_image):
    """
    Compare uploaded screenshot with the
    official reference screenshot.
    """

    img1 = cv2.imread(uploaded_image)
    img2 = cv2.imread(reference_image)

    if img1 is None or img2 is None:

        return {

            "visualSimilarity": 0,

            "ssim": 0,

            "clipSimilarity": 0,

            "colorSimilarity": 0,

            "layoutSimilarity": 0,

            "perceptualHash": 64

        }

    # -----------------------------
    # Resize
    # -----------------------------

    img1 = cv2.resize(img1, (1200, 800))
    img2 = cv2.resize(img2, (1200, 800))

    # -----------------------------
    # SSIM
    # -----------------------------

    gray1 = cv2.cvtColor(
        img1,
        cv2.COLOR_BGR2GRAY
    )

    gray2 = cv2.cvtColor(
        img2,
        cv2.COLOR_BGR2GRAY
    )

    ssim_score = ssim(
        gray1,
        gray2
    )

    # -----------------------------
    # Perceptual Hash
    # -----------------------------

    hash1 = imagehash.phash(
        Image.open(uploaded_image)
    )

    hash2 = imagehash.phash(
        Image.open(reference_image)
    )

    phash = hash1 - hash2

    # -----------------------------
    # CLIP
    # -----------------------------

    clip_score = clip_similarity(
        uploaded_image,
        reference_image
    )

    # -----------------------------
    # Color
    # -----------------------------

    color_score = calculate_color_similarity(
        uploaded_image,
        reference_image
    )

    # -----------------------------
    # Layout
    # -----------------------------

    layout_score = calculate_layout_similarity(
        uploaded_image,
        reference_image
    )

    # -----------------------------
    # Overall
    # -----------------------------

    visual_similarity = round(

        (

            ssim_score * 0.25 +

            clip_score * 0.40 +

            color_score * 0.15 +

            layout_score * 0.20

        ),

        3

    )

    return {

        "visualSimilarity": visual_similarity,

        "ssim": round(float(ssim_score), 3),

        "clipSimilarity": round(clip_score, 3),

        "colorSimilarity": round(color_score, 3),

        "layoutSimilarity": round(layout_score, 3),

        "perceptualHash": phash

    }