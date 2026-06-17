"""LibreOffice backend — wraps the real `soffice` CLI."""

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Optional


def find_libreoffice() -> str:
    """Find the LibreOffice/soffice executable.

    Raises RuntimeError with install instructions if not found.
    """
    for name in ("soffice", "libreoffice"):
        path = shutil.which(name)
        if path:
            return path
    raise RuntimeError(
        "LibreOffice is not installed. Install it with:\n"
        "  brew install --cask libreoffice   # macOS\n"
        "  apt install libreoffice            # Debian/Ubuntu\n"
        "  dnf install libreoffice            # Fedora"
    )


def get_version() -> str:
    """Return LibreOffice version string."""
    exe = find_libreoffice()
    result = subprocess.run(
        [exe, "--version"],
        capture_output=True, text=True, check=False
    )
    return result.stdout.strip()


def list_supported_formats() -> dict[str, list[str]]:
    """Return a mapping of document type -> supported output formats.

    These are the most common filters LibreOffice supports via --convert-to.
    """
    return {
        "writer": [
            "pdf", "docx", "doc", "odt", "rtf", "txt", "html", "epub"
        ],
        "calc": [
            "pdf", "xlsx", "xls", "ods", "csv", "html"
        ],
        "impress": [
            "pdf", "pptx", "ppt", "odp", "html", "swf"
        ],
        "draw": [
            "pdf", "svg", "png", "jpg", "bmp", "gif", "tiff"
        ],
    }


def convert_file(
    input_path: str,
    output_format: str,
    output_dir: Optional[str] = None,
    overwrite: bool = True,
    infilter: Optional[str] = None,
) -> dict:
    """Convert a single file using LibreOffice headless mode.

    Args:
        input_path: Path to the source document.
        output_format: Target format extension (e.g. 'pdf', 'csv').
        output_dir: Directory for the output. Defaults to same as input.
        overwrite: Whether to overwrite existing output.
        infilter: Optional input filter string.

    Returns:
        Dict with keys: success, output, stdout, stderr, returncode
    """
    exe = find_libreoffice()
    src = Path(input_path).resolve()
    if not src.exists():
        return {
            "success": False,
            "output": None,
            "stdout": "",
            "stderr": f"File not found: {input_path}",
            "returncode": 1,
        }

    out_dir = Path(output_dir).resolve() if output_dir else src.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        exe,
        "--headless",
        "--nologo",
        "--nodefault",
        "--convert-to", output_format,
        "--outdir", str(out_dir),
    ]
    if infilter:
        cmd.extend(["--infilter", infilter])
    cmd.append(str(src))

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=False,
    )

    # LibreOffice writes conversion messages to stdout, not stderr
    # Output filename is usually input basename + new extension
    base = src.stem
    out_file = out_dir / f"{base}.{output_format}"

    # Some formats have different extensions (e.g. jpg -> jpeg)
    if not out_file.exists():
        for ext in (output_format, output_format.replace("jpg", "jpeg")):
            candidate = out_dir / f"{base}.{ext}"
            if candidate.exists():
                out_file = candidate
                break

    success = result.returncode == 0 and out_file.exists()
    return {
        "success": success,
        "output": str(out_file) if success else None,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode,
    }


def convert_to_text(input_path: str) -> dict:
    """Convert a document to plain text using --cat (when available) or txt export.

    Returns dict with success, text, output path.
    """
    # First try headless convert to txt
    result = convert_file(input_path, "txt")
    if result["success"]:
        txt_path = Path(result["output"])
        text = txt_path.read_text(encoding="utf-8", errors="ignore")
        return {
            "success": True,
            "text": text,
            "output": str(txt_path),
        }
    return {
        "success": False,
        "text": None,
        "output": None,
        "stderr": result.get("stderr", ""),
    }


def merge_pdfs(input_paths: list[str], output_path: str) -> dict:
    """Merge multiple PDFs into one using LibreOffice Impress.

    LibreOffice itself doesn't have a native PDF merge CLI, so this
    uses a Python-based fallback if available, otherwise returns an error.
    """
    try:
        import pypdf
        merger = pypdf.PdfMerger()
        for p in input_paths:
            merger.append(p)
        merger.write(output_path)
        merger.close()
        return {
            "success": True,
            "output": output_path,
        }
    except ImportError:
        return {
            "success": False,
            "output": None,
            "stderr": "PDF merge requires 'pypdf'. Install: pip install pypdf",
        }


def get_document_info(input_path: str) -> dict:
    """Get basic information about a document.

    Uses file extension heuristics and libmagic if available.
    """
    path = Path(input_path)
    info = {
        "path": str(path.resolve()),
        "exists": path.exists(),
        "size": path.stat().st_size if path.exists() else 0,
        "extension": path.suffix.lower(),
        "type": "unknown",
    }

    ext_map = {
        ".docx": "writer",
        ".doc": "writer",
        ".odt": "writer",
        ".rtf": "writer",
        ".txt": "writer",
        ".pdf": "pdf",
        ".xlsx": "calc",
        ".xls": "calc",
        ".ods": "calc",
        ".csv": "calc",
        ".pptx": "impress",
        ".ppt": "impress",
        ".odp": "impress",
        ".svg": "draw",
        ".png": "draw",
        ".jpg": "draw",
        ".jpeg": "draw",
    }
    info["type"] = ext_map.get(info["extension"], "unknown")

    # Try python-magic for MIME type
    try:
        import magic
        mime = magic.from_file(str(path.resolve()), mime=True)
        info["mime_type"] = mime
    except Exception:
        info["mime_type"] = None

    return info
