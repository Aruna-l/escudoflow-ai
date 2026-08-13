# ---------------------------------------------------------------------------
# Attachment Intelligence constants
# Merge this block into your existing app/core/constants.py
# (keep whatever else already lives in that file — this is additive).
# ---------------------------------------------------------------------------

# Base risk contribution by file extension (0-100). Used as the starting
# point before macro / script / executable findings are added on top.
SUSPICIOUS_EXTENSIONS = {
    ".exe": 100,
    ".dll": 100,
    ".bat": 60,
    ".cmd": 60,
    ".scr": 95,
    ".js": 55,
    ".vbs": 60,
    ".ps1": 60,
    ".jar": 55,
    # Archives carry moderate baseline risk on their own — they're only
    # dangerous because of what's inside them. Real risk comes from the
    # suspicious-executable count found during content inspection, not
    # from merely being a zip/rar/7z.
    ".zip": 25,
    ".rar": 25,
    ".7z": 25,
    ".iso": 35,
    ".docm": 55,
    ".xlsm": 55,
    ".pptm": 55,
    ".doc": 35,
    ".xls": 35,
    ".ppt": 35,
    ".pdf": 20,
    ".docx": 15,
    ".xlsx": 15,
    ".pptx": 15,
    ".txt": 5,
}

# Office formats that are known to support a VBA macro project.
MACRO_ENABLED_EXTENSIONS = {".docm", ".xlsm", ".pptm", ".doc", ".xls", ".ppt"}

# Every office format we attempt macro analysis on (macro-enabled + modern
# OOXML formats, since a .docx can still be checked for a smuggled
# vbaProject.bin even though it's not supposed to have one).
OFFICE_EXTENSIONS = MACRO_ENABLED_EXTENSIONS | {".docx", ".xlsx", ".pptx"}

ARCHIVE_EXTENSIONS = {".zip", ".rar", ".7z"}

# Script files whose own text content should be scanned directly for
# malicious patterns (as opposed to Office files, where we extract VBA
# macro source first). These are treated as plain text.
RAW_SCRIPT_EXTENSIONS = {".js", ".vbs", ".ps1", ".bat", ".cmd"}

EXECUTABLE_EXTENSIONS = {
    ".exe", ".dll", ".scr", ".bat", ".cmd", ".ps1", ".vbs", ".js", ".jar",
}

# Extensions accepted by the /attachment/analyze upload endpoint.
SUPPORTED_UPLOAD_EXTENSIONS = {
    ".pdf", ".docx", ".docm", ".doc",
    ".xlsx", ".xlsm", ".xls",
    ".pptx", ".pptm", ".ppt",
    ".zip", ".rar", ".7z", ".iso",
    ".exe", ".dll", ".js", ".vbs", ".ps1", ".bat", ".cmd", ".scr", ".jar",
}

MAX_UPLOAD_SIZE_MB = 32

# How much each threat-summary finding adds to the aggregate risk score.
# Keys match RiskBadge's `level` prop in cyber-ui.tsx exactly (lowercase).
SEVERITY_WEIGHTS = {"critical": 25, "high": 15, "suspicious": 8, "low": 3, "safe": 0}

# Ordered high -> low; first threshold the score clears wins.
# Mirrors scoreToLevel() in cyber-ui.tsx exactly (85 / 65 / 40 / 20) so the
# label returned by the API always matches the color RiskMeter renders on
# the frontend (RiskMeter computes its own color from the score, it does
# not read this label — but everything else that reads riskLabel, e.g.
# the recommendation text, has to agree with what the ring is showing).
RISK_THRESHOLDS = [(85, "critical"), (65, "high"), (40, "suspicious"), (20, "low"), (0, "safe")]

# Human-readable "TYPE" field shown in the File Metadata panel.
FILE_TYPE_LABELS = {
    ".docx": "DOCX",
    ".docm": "DOCX (macro-enabled)",
    ".doc": "DOC (legacy, macro-enabled)",
    ".xlsx": "XLSX",
    ".xlsm": "XLSX (macro-enabled)",
    ".xls": "XLS (legacy, macro-enabled)",
    ".pptx": "PPTX",
    ".pptm": "PPTX (macro-enabled)",
    ".ppt": "PPT (legacy, macro-enabled)",
    ".pdf": "PDF",
    ".zip": "ZIP archive",
    ".rar": "RAR archive",
    ".7z": "7Z archive",
    ".iso": "Disk image",
    ".exe": "Windows Executable",
    ".dll": "Dynamic Link Library",
    ".js": "JavaScript",
    ".vbs": "VBScript",
    ".ps1": "PowerShell Script",
    ".bat": "Batch Script",
    ".cmd": "Command Script",
    ".scr": "Screensaver Executable",
    ".jar": "Java Archive",
}

IOC_TYPES = ["Domain", "IP", "URL", "Hash", "Email"]
THREAT_FEED_NAMES = ["VirusTotal", "AbuseIPDB", "PhishTank", "AlienVault OTX"]
