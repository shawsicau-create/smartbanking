"""Document conversion operations for LibreOffice CLI."""

import json
import os
from pathlib import Path
from typing import Optional

from ..utils.libreoffice_backend import (
    convert_file,
    convert_to_text,
    get_document_info,
    list_supported_formats,
)


def do_convert(
    input_path: str,
    output_format: str,
    output_dir: Optional[str] = None,
    overwrite: bool = True,
    json_output: bool = False,
) -> dict:
    """Convert a single document."""
    result = convert_file(input_path, output_format, output_dir, overwrite)
    if json_output:
        return result
    return result


def do_batch_convert(
    input_dir: str,
    pattern: str,
    output_format: str,
    output_dir: Optional[str] = None,
    json_output: bool = False,
) -> list[dict]:
    """Batch convert files matching a glob pattern."""
    from glob import glob

    files = glob(os.path.join(input_dir, pattern))
    files.sort()

    results = []
    for f in files:
        r = convert_file(f, output_format, output_dir, overwrite=True)
        results.append({
            "input": f,
            **r,
        })

    return results


def do_info(input_path: str, json_output: bool = False) -> dict:
    """Get document info."""
    info = get_document_info(input_path)
    if json_output:
        return info
    return info


def do_list_formats(json_output: bool = False) -> dict:
    """List supported conversion formats."""
    formats = list_supported_formats()
    if json_output:
        return formats
    return formats
