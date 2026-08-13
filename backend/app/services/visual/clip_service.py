import torch
import clip
from PIL import Image

# -----------------------------
# Load model once
# -----------------------------

device = "cuda" if torch.cuda.is_available() else "cpu"

model, preprocess = clip.load(
    "ViT-B/32",
    device=device
)


def clip_similarity(
    uploaded_image: str,
    reference_image: str
):
    """
    Compute semantic similarity between two images
    using CLIP embeddings.
    """

    image1 = preprocess(
        Image.open(uploaded_image)
    ).unsqueeze(0).to(device)

    image2 = preprocess(
        Image.open(reference_image)
    ).unsqueeze(0).to(device)

    with torch.no_grad():

        embedding1 = model.encode_image(image1)

        embedding2 = model.encode_image(image2)

    embedding1 /= embedding1.norm(
        dim=-1,
        keepdim=True
    )

    embedding2 /= embedding2.norm(
        dim=-1,
        keepdim=True
    )

    similarity = (
        embedding1 @ embedding2.T
    ).item()

    return round(float(similarity), 3)