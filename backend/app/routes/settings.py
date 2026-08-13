from datetime import datetime, timezone

import pyotp
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from app.database import (
    users_col,
    organizations_col,
    notifications_col,
    preferences_col,
    api_keys_col,
)
from app.core.auth import get_current_user
from app.core.security import hash_password, verify_password
from app.schemas.settings import (
    ProfileResponse,
    ProfileUpdateRequest,
    OrganizationResponse,
    OrganizationUpdateRequest,
    NotificationsSettings,
    PreferencesSettings,
    ApiKeyCreateRequest,
    ApiKeyCreatedResponse,
    ApiKeyResponse,
    ChangePasswordRequest,
    TwoFactorSetupResponse,
    TwoFactorVerifyRequest,
    TwoFactorToggleResponse,
)

router = APIRouter(prefix="/settings", tags=["settings"])


async def _get_user_doc(current: dict = Depends(get_current_user)) -> dict:
    """core.auth.get_current_user only decodes the token (email, name).
    Settings routes need the full Mongo document, so we fetch it here."""
    user = await users_col.find_one({"email": current["email"]})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ---------------- Profile ----------------

@router.get("/profile", response_model=ProfileResponse)
async def get_profile(user: dict = Depends(_get_user_doc)):
    return ProfileResponse(
        full_name=user["full_name"],
        email=user["email"],
        role=user.get("role"),
        time_zone=user.get("time_zone"),
        two_factor_enabled=user.get("two_factor_enabled", False),
    )


@router.put("/profile", response_model=ProfileResponse)
async def update_profile(payload: ProfileUpdateRequest, user: dict = Depends(_get_user_doc)):
    updates = {k: v for k, v in payload.model_dump().items() if v is not None}
    if updates:
        await users_col.update_one({"_id": user["_id"]}, {"$set": updates})
        user.update(updates)

    return ProfileResponse(
        full_name=user["full_name"],
        email=user["email"],
        role=user.get("role"),
        time_zone=user.get("time_zone"),
        two_factor_enabled=user.get("two_factor_enabled", False),
    )


# ---------------- Organization ----------------

@router.get("/organization", response_model=OrganizationResponse)
async def get_organization(user: dict = Depends(_get_user_doc)):
    org = await organizations_col.find_one({"owner_id": str(user["_id"])})
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return OrganizationResponse(
        name=org.get("name", ""),
        domain=org.get("domain", ""),
        tenant_id=org.get("tenant_id", ""),
        region=org.get("region", ""),
    )


@router.put("/organization", response_model=OrganizationResponse)
async def update_organization(payload: OrganizationUpdateRequest, user: dict = Depends(_get_user_doc)):
    user_id = str(user["_id"])
    org = await organizations_col.find_one({"owner_id": user_id})
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    updates = {k: v for k, v in payload.model_dump().items() if v is not None}
    if updates:
        await organizations_col.update_one({"owner_id": user_id}, {"$set": updates})
        org.update(updates)

    return OrganizationResponse(
        name=org.get("name", ""),
        domain=org.get("domain", ""),
        tenant_id=org.get("tenant_id", ""),
        region=org.get("region", ""),
    )


# ---------------- Notifications ----------------

@router.get("/notifications", response_model=NotificationsSettings)
async def get_notifications(user: dict = Depends(_get_user_doc)):
    user_id = str(user["_id"])
    doc = await notifications_col.find_one({"user_id": user_id})
    if not doc:
        doc = NotificationsSettings().model_dump()
        doc["user_id"] = user_id
        await notifications_col.insert_one(doc)
    return NotificationsSettings(**doc)


@router.put("/notifications", response_model=NotificationsSettings)
async def update_notifications(payload: NotificationsSettings, user: dict = Depends(_get_user_doc)):
    await notifications_col.update_one(
        {"user_id": str(user["_id"])}, {"$set": payload.model_dump()}, upsert=True
    )
    return payload


# ---------------- Theme + Language ----------------

@router.get("/preferences", response_model=PreferencesSettings)
async def get_preferences(user: dict = Depends(_get_user_doc)):
    user_id = str(user["_id"])
    doc = await preferences_col.find_one({"user_id": user_id})
    if not doc:
        doc = PreferencesSettings().model_dump()
        doc["user_id"] = user_id
        await preferences_col.insert_one(doc)
    return PreferencesSettings(**doc)


@router.put("/preferences", response_model=PreferencesSettings)
async def update_preferences(payload: PreferencesSettings, user: dict = Depends(_get_user_doc)):
    await preferences_col.update_one(
        {"user_id": str(user["_id"])}, {"$set": payload.model_dump()}, upsert=True
    )
    return payload


# ---------------- API Keys ----------------

def _preview(raw_key: str) -> str:
    if len(raw_key) <= 12:
        return raw_key
    return f"{raw_key[:8]}\u2026{raw_key[-4:]}"


@router.get("/api-keys", response_model=list[ApiKeyResponse])
async def list_api_keys(user: dict = Depends(_get_user_doc)):
    cursor = api_keys_col.find({"user_id": str(user["_id"])}).sort("created_at", -1)
    keys = await cursor.to_list(length=100)
    return [ApiKeyResponse(name=k["name"], key_preview=k["key_preview"], created_at=k["created_at"]) for k in keys]


@router.post("/api-keys", response_model=ApiKeyCreatedResponse, status_code=status.HTTP_201_CREATED)
async def create_api_key(payload: ApiKeyCreateRequest, user: dict = Depends(_get_user_doc)):
    import secrets
    raw_key = f"af_{secrets.token_urlsafe(32)}"
    now = datetime.now(timezone.utc)
    await api_keys_col.insert_one({
        "user_id": str(user["_id"]),
        "name": payload.name,
        "key_hash": hash_password(raw_key),
        "key_preview": _preview(raw_key),
        "created_at": now,
    })
    # raw_key is returned ONCE — the frontend must show/copy it immediately
    return ApiKeyCreatedResponse(name=payload.name, key=raw_key, created_at=now)


@router.delete("/api-keys/{key_id}", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_api_key(key_id: str, user: dict = Depends(_get_user_doc)):
    try:
        oid = ObjectId(key_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid key id")

    result = await api_keys_col.delete_one({"_id": oid, "user_id": str(user["_id"])})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="API key not found")


# ---------------- Security ----------------

@router.put("/security/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(payload: ChangePasswordRequest, user: dict = Depends(_get_user_doc)):
    if not verify_password(payload.current_password, user["password_hash"]):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    try:
        new_hash = hash_password(payload.new_password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    await users_col.update_one({"_id": user["_id"]}, {"$set": {"password_hash": new_hash}})


@router.post("/security/2fa/setup", response_model=TwoFactorSetupResponse)
async def setup_two_factor(user: dict = Depends(_get_user_doc)):
    secret = pyotp.random_base32()
    await users_col.update_one({"_id": user["_id"]}, {"$set": {"two_factor_secret": secret}})
    otpauth_url = pyotp.totp.TOTP(secret).provisioning_uri(name=user["email"], issuer_name="EscudoFlow AI")
    return TwoFactorSetupResponse(secret=secret, otpauth_url=otpauth_url)


@router.post("/security/2fa/verify", response_model=TwoFactorToggleResponse)
async def verify_two_factor(payload: TwoFactorVerifyRequest, user: dict = Depends(_get_user_doc)):
    secret = user.get("two_factor_secret")
    if not secret:
        raise HTTPException(status_code=400, detail="No 2FA setup in progress")
    if not pyotp.TOTP(secret).verify(payload.code):
        raise HTTPException(status_code=400, detail="Invalid authentication code")
    await users_col.update_one({"_id": user["_id"]}, {"$set": {"two_factor_enabled": True}})
    return TwoFactorToggleResponse(two_factor_enabled=True)


@router.post("/security/2fa/disable", response_model=TwoFactorToggleResponse)
async def disable_two_factor(user: dict = Depends(_get_user_doc)):
    await users_col.update_one(
        {"_id": user["_id"]}, {"$set": {"two_factor_enabled": False, "two_factor_secret": None}}
    )
    return TwoFactorToggleResponse(two_factor_enabled=False)
