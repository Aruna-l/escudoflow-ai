import io
import os
import tempfile
import zipfile

try:
    from oletools.olevba import VBA_Parser
    OLETOOLS_AVAILABLE = True
except ImportError:
    OLETOOLS_AVAILABLE = False


def has_macro_container(filename: str, data: bytes) -> bool:
    """
    Cheap structural check: does this OOXML file contain a VBA project
    (vbaProject.bin) inside its zip package at all. Works even without
    oletools installed, so it's used as the primary "macros_detected" flag.
    """
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            return any("vbaProject.bin" in n for n in zf.namelist())
    except Exception:
        # Legacy binary formats (.doc/.xls/.ppt) are OLE, not zip — treat
        # any OLE compound file as "has a macro container" so downstream
        # oletools/fallback extraction still runs on it.
        return data[:8] == b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"


def extract_vba_code(filename: str, data: bytes) -> str:
    """
    Extract concatenated VBA macro source code from an Office file.
    Returns an empty string if no macros are found or the file can't
    be parsed.

    Always combines the oletools result (when available) with the raw
    ASCII-string fallback, rather than trusting oletools' "no macros
    found" as final. oletools can correctly report "not a valid VBA
    project" for malformed/synthetic vbaProject.bin streams while that
    same stream still contains readable plaintext indicators (AutoOpen,
    Shell, powershell, URLs, etc.) worth flagging. Real-world malware
    droppers are also sometimes deliberately malformed to evade parsers
    like oletools, so skipping the fallback whenever oletools "succeeds"
    (even with an empty result) would create a bypass.
    """
    oletools_result = _extract_vba_with_oletools(filename, data) if OLETOOLS_AVAILABLE else ""
    fallback_result = _extract_vba_fallback(data)

    if oletools_result and fallback_result:
        return oletools_result + "\n" + fallback_result
    return oletools_result or fallback_result


def _extract_vba_with_oletools(filename: str, data: bytes) -> str:
    suffix = os.path.splitext(filename)[1] or ".bin"
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(data)
            tmp_path = tmp.name

        vba_parser = VBA_Parser(tmp_path)
        if not vba_parser.detect_vba_macros():
            return ""

        chunks = []
        for (_, _, _, vba_code) in vba_parser.extract_macros():
            if vba_code:
                chunks.append(vba_code)
        return "\n".join(chunks)
    except Exception:
        return ""
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)


def _extract_vba_fallback(data: bytes) -> str:
    """
    Lightweight fallback when oletools isn't installed: pull the raw
    'vbaProject.bin' entry out of an OOXML zip and decode any readable
    ASCII strings from it. Far less precise than oletools (it can't
    decompress the compressed VBA source streams), but it still lets us
    catch plaintext strings like "AutoOpen", "Shell", "powershell", URLs,
    etc. that malware authors leave un-obfuscated.
    """
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            names = [n for n in zf.namelist() if "vbaProject.bin" in n]
            if not names:
                return ""
            raw = zf.read(names[0])
            printable = bytes(b if 32 <= b < 127 else 32 for b in raw)
            return printable.decode("ascii", errors="ignore")
    except Exception:
        return ""
