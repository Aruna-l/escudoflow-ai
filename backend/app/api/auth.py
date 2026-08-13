from datetime import datetime, timezone

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from app.database import (
    users_col,
    organizations_col,
    notifications_col,
    preferences_col,
)
from app.core.security import hash_password, verify_password, create_access_token
from app.core.auth import get_current_user
from app.schemas.auth import SignupRequest, LoginRequest
from app.schemas.settings import ProfileResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(payload: SignupRequest):
    existing = await users_col.find_one({"email": payload.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    try:
        password_hash = hash_password(payload.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    now = datetime.now(timezone.utc)
    user_doc = {
        "full_name": payload.full_name,
        "email": payload.email,
        "password_hash": password_hash,
        "role": None,
        "time_zone": "UTC",
        "two_factor_enabled": False,
        "two_factor_secret": None,
        "created_at": now,
    }
    result = await users_col.insert_one(user_doc)
    user_id = str(result.inserted_id)

    # Seed related settings documents so GET endpoints never 404 for a fresh user
    await organizations_col.insert_one({
        "owner_id": user_id,
        "name": payload.organization,
        "domain": "",
        "tenant_id": f"af_ten_{ObjectId()}"[:20],
        "region": "US-East-1",
    })
    await notifications_col.insert_one({
        "user_id": user_id,
        "critical_incidents": True,
        "weekly_summary": True,
        "new_ai_findings": True,
        "product_updates": True,
    })
    await preferences_col.insert_one({
        "user_id": user_id,
        "theme": "Deep Navy",
        "language": "English (US)",
    })

    token = create_access_token({"sub": payload.email, "name": payload.full_name})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login")
async def login(payload: LoginRequest):
    user = await users_col.find_one({"email": payload.email})
    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": user["email"], "name": user["full_name"]})
    return {
        "access_token": token,
        "token_type": "bearer",
        "email": user["email"],
        "name": user["full_name"],
    }

@router.get("/me", response_model=ProfileResponse)
async def me(current: dict = Depends(get_current_user)):
    user = await users_col.find_one({"email": current["email"]})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return ProfileResponse(
        full_name=user["full_name"],
        email=user["email"],
        role=user.get("role"),
        time_zone=user.get("time_zone"),
        two_factor_enabled=user.get("two_factor_enabled", False),
    )