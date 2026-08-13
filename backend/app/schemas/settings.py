from datetime import datetime
from pydantic import BaseModel, EmailStr


# ---------- Profile ----------

class ProfileResponse(BaseModel):
    full_name: str
    email: EmailStr
    role: str | None = None
    time_zone: str | None = None
    two_factor_enabled: bool = False


class ProfileUpdateRequest(BaseModel):
    full_name: str | None = None
    role: str | None = None
    time_zone: str | None = None


# ---------- Organization ----------

class OrganizationResponse(BaseModel):
    name: str
    domain: str
    tenant_id: str
    region: str


class OrganizationUpdateRequest(BaseModel):
    name: str | None = None
    domain: str | None = None
    region: str | None = None


# ---------- Notifications ----------

class NotificationsSettings(BaseModel):
    critical_incidents: bool = True
    weekly_summary: bool = True
    new_ai_findings: bool = True
    product_updates: bool = True


# ---------- Preferences (theme + language) ----------

class PreferencesSettings(BaseModel):
    theme: str = "Deep Navy"
    language: str = "English (US)"


# ---------- API Keys ----------

class ApiKeyCreateRequest(BaseModel):
    name: str


class ApiKeyCreatedResponse(BaseModel):
    name: str
    key: str  # raw key, shown only once
    created_at: datetime


class ApiKeyResponse(BaseModel):
    name: str
    key_preview: str
    created_at: datetime


# ---------- Security ----------

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str


class TwoFactorSetupResponse(BaseModel):
    secret: str
    otpauth_url: str


class TwoFactorVerifyRequest(BaseModel):
    code: str


class TwoFactorToggleResponse(BaseModel):
    two_factor_enabled: bool
