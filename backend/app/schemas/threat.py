import re
from pydantic import BaseModel, Field, model_validator
from typing import List, Literal, Optional

IOCType = Literal["Domain", "IP", "URL", "Hash", "Email"]

DOMAIN_RE = re.compile(r"^([a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$")
IPV4_RE = re.compile(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$")
HASH_RE = re.compile(r"^[a-fA-F0-9]{32}$|^[a-fA-F0-9]{40}$|^[a-fA-F0-9]{64}$")
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


class ThreatAnalyzeRequest(BaseModel):
    ioc: str = Field(..., description="The indicator of compromise to look up")
    type: IOCType = Field(..., description="Type of IOC")

    @model_validator(mode="after")
    def validate_ioc_matches_type(self):
        value = self.ioc.strip()

        if self.type == "Domain" and not DOMAIN_RE.match(value):
            raise ValueError("ioc is not a valid domain for type 'Domain'")

        if self.type == "IP":
            match = IPV4_RE.match(value)
            if not match or any(int(octet) > 255 for octet in match.groups()):
                raise ValueError("ioc is not a valid IPv4 address for type 'IP'")

        if self.type == "URL" and not (value.startswith("http://") or value.startswith("https://")):
            raise ValueError("ioc must start with http:// or https:// for type 'URL'")

        if self.type == "Hash" and not HASH_RE.match(value):
            raise ValueError("ioc is not a valid MD5/SHA-1/SHA-256 hash for type 'Hash'")

        if self.type == "Email" and not EMAIL_RE.match(value):
            raise ValueError("ioc is not a valid email address for type 'Email'")

        return self


class ThreatFeedResult(BaseModel):
    name: str
    verdict: str
    malicious: bool = False
    raw: Optional[dict] = None


class ThreatIntelResponse(BaseModel):
    ioc: str
    type: str
    reputation: str
    confidence: int
    malwareFamily: str
    knownCampaign: str
    firstSeen: str
    lastSeen: str
    feeds: List[ThreatFeedResult]
    actions: List[str]