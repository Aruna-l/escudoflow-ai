import io
import re
import zipfile
from typing import List, Tuple

from app.core.constants import EXECUTABLE_EXTENSIONS
from app.schemas.attachment import ThreatItem

AUTOEXEC_PATTERNS = [
    r"\bautoopen\b", r"\bautoexec\b", r"\bautoclose\b",
    r"\bdocument_open\b", r"\bworkbook_open\b",
]

SHELL_PATTERNS = [
    r"\bshell\s*\(", r"wscript\.shell",
    r"createobject\s*\(\s*[\"']wscript\.shell[\"']",
]

POWERSHELL_PATTERNS = [
    r"powershell(\.exe)?", r"\biex\s*\(", r"invoke-expression",
]

DOWNLOAD_PATTERNS = [
    r"urldownloadtofile", r"net\.webclient", r"downloadstring",
    r"downloadfile", r"invoke-webrequest", r"bitsadmin",
    r"\bcurl\b", r"\bwget\b",
]

# A run of base64-alphabet chars long enough that it's very unlikely to be
# coincidental (e.g. a real word or a short constant).
BASE64_BLOB_PATTERN = re.compile(r"(?:[A-Za-z0-9+/]{4}){15,}={0,2}")

URL_PATTERN = re.compile(r"https?://[^\s\"'<>]+")


def _any_match(patterns: List[str], text: str) -> bool:
    return any(re.search(p, text, re.IGNORECASE) for p in patterns)


def analyze_vba_code(vba_code: str) -> Tuple[List[ThreatItem], int]:
    """
    Scan extracted VBA/script source for known malicious patterns and
    build the Threat Summary list shown in the UI.

    Returns (threat_items, embedded_scripts_count).
    """
    items: List[ThreatItem] = []
    script_hits = 0

    if not vba_code:
        return items, script_hits

    has_autoexec = _any_match(AUTOEXEC_PATTERNS, vba_code)
    has_shell = _any_match(SHELL_PATTERNS, vba_code)
    has_powershell = _any_match(POWERSHELL_PATTERNS, vba_code)

    if has_autoexec and has_powershell:
        items.append(ThreatItem(name="Auto-executing macro invokes PowerShell", severity="critical"))
        script_hits += 1
    elif has_autoexec and has_shell:
        items.append(ThreatItem(name="Auto-executing macro launches a shell command", severity="critical"))
        script_hits += 1
    elif has_autoexec:
        items.append(ThreatItem(name="Macro auto-executes on document open", severity="high"))
        script_hits += 1
    elif has_powershell:
        items.append(ThreatItem(name="Script shells out to PowerShell", severity="high"))
        script_hits += 1

    if BASE64_BLOB_PATTERN.search(vba_code):
        items.append(ThreatItem(name="Base64-encoded payload downloader", severity="high"))
        script_hits += 1

    urls = sorted(set(m.group(0) for m in URL_PATTERN.finditer(vba_code)))
    for url in urls:
        items.append(ThreatItem(
            name=f"Fetches remote binary from {_short_domain(url)}",
            severity="high",
        ))
        script_hits += 1

    if _any_match(DOWNLOAD_PATTERNS, vba_code) and not urls and not has_powershell:
        items.append(ThreatItem(name="Contains a remote download routine", severity="suspicious"))
        script_hits += 1

    return items, script_hits


def _short_domain(url: str) -> str:
    match = re.match(r"https?://([^/]+)", url)
    return f"a newly-registered domain ({match.group(1)})" if match else "an external URL"


def count_suspicious_executables(filename: str, data: bytes, extension: str) -> int:
    """
    Count executables either embedded inside an archive/office container,
    or the uploaded file itself if it's directly an executable type.
    """
    if extension in EXECUTABLE_EXTENSIONS:
        return 1

    count = 0
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            for name in zf.namelist():
                ext = "." + name.rsplit(".", 1)[-1].lower() if "." in name else ""
                if ext in EXECUTABLE_EXTENSIONS:
                    count += 1
    except zipfile.BadZipFile:
        pass

    return count
