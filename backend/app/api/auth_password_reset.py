import secrets
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException, status

from app.database import users_col, password_resets_col
from app.core.security import hash_password
from app.schemas.password_reset import ForgotPasswordRequest, ResetPasswordRequest

router = APIRouter(prefix="/auth", tags=["auth"])

RESET_TOKEN_TTL_MINUTES = 30

# Where your frontend's reset-password page lives.
# Change this if your dev server runs on a different port.
FRONTEND_RESET_URL = "http://localhost:8080/reset-password"


@router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(payload: ForgotPasswordRequest):
    user = await users_col.find_one({"email": payload.email})

    # Always return the same generic message whether or not the email
    # exists — this avoids leaking which emails are registered.
    generic_response = {
        "message": "If that email is registered, a reset link has been generated."
    }

    if not user:
        return generic_response

    token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=RESET_TOKEN_TTL_MINUTES)

    await password_resets_col.insert_one({
        "user_id": str(user["_id"]),
        "token": token,
        "expires_at": expires_at,
    })

    reset_link = f"{FRONTEND_RESET_URL}?token={token}"

    # ---- DEV MODE ----
    # No email service is configured yet, so we print the link here.
    # Copy it from this terminal and paste it into your browser.
    # Replace this block with a real email send once SMTP is set up.
    print("\n" + "=" * 60)
    print(f"PASSWORD RESET LINK for {payload.email}:")
    print(reset_link)
    print(f"(expires in {RESET_TOKEN_TTL_MINUTES} minutes)")
    print("=" * 60 + "\n")

    return generic_response


@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(payload: ResetPasswordRequest):
    record = await password_resets_col.find_one({"token": payload.token})

    if not record:
        raise HTTPException(status_code=400, detail="Invalid or expired reset link")

    expires_at = record["expires_at"]
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at < datetime.now(timezone.utc):
        await password_resets_col.delete_one({"_id": record["_id"]})
        raise HTTPException(status_code=400, detail="Invalid or expired reset link")

    try:
        new_hash = hash_password(payload.new_password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    from bson import ObjectId

    await users_col.update_one(
        {"_id": ObjectId(record["user_id"])},
        {"$set": {"password_hash": new_hash}},
    )

    # Token is single-use — remove it once consumed
    await password_resets_col.delete_one({"_id": record["_id"]})

    return {"message": "Password has been reset. You can now log in."}
