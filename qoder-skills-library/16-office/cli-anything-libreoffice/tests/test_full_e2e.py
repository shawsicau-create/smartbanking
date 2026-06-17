"""E2E tests invoking the real LibreOffice backend."""

import os
import shutil
import subprocess
import sys

import pytest

from cli_anything.libreoffice.utils.libreoffice_backend import (
    convert_file,
    convert_to_text,
    find_libreoffice,
)


def _resolve_cli(name):
    """Resolve installed CLI command; falls back to python -m for dev."""
    force = os.environ.get("CLI_ANYTHING_FORCE_INSTALLED", "").strip() == "1"
    path = shutil.which(name)
    if path:
        print(f"[_resolve_cli] Using installed command: {path}")
        return [path]
    if force:
        raise RuntimeError(f"{name} not found in PATH. Install with: pip install -e .")
    module = name.replace("cli-anything-", "cli_anything.") + "." + name.split("-")[-1] + "_cli"
    print(f"[_resolve_cli] Falling back to: {sys.executable} -m {module}")
    return [sys.executable, "-m", module]


class TestTrueBackend:
    """Tests that invoke the real soffice binary."""

    def test_txt_to_pdf(self, tmp_path):
        src = tmp_path / "test.txt"
        src.write_text("Hello LibreOffice\nSecond line\n")
        result = convert_file(str(src), "pdf", str(tmp_path))
        assert result["success"], result.get("stderr", "")
        out = result["output"]
        assert os.path.exists(out)
        assert os.path.getsize(out) > 100
        with open(out, "rb") as f:
            assert f.read(5) == b"%PDF-"
        print(f"\n  PDF: {out} ({os.path.getsize(out):,} bytes)")

    def test_txt_to_docx(self, tmp_path):
        src = tmp_path / "test.txt"
        src.write_text("Hello World")
        result = convert_file(str(src), "docx", str(tmp_path))
        assert result["success"], result.get("stderr", "")
        out = result["output"]
        assert os.path.exists(out)
        assert os.path.getsize(out) > 100
        # DOCX is a ZIP file
        with open(out, "rb") as f:
            assert f.read(2) == b"PK"
        print(f"\n  DOCX: {out} ({os.path.getsize(out):,} bytes)")

    def test_text_extraction(self, tmp_path):
        # Create a docx first
        src = tmp_path / "test.txt"
        src.write_text("Extractable content")
        conv = convert_file(str(src), "docx", str(tmp_path))
        assert conv["success"]
        docx_path = conv["output"]
        # Now extract text from it
        result = convert_to_text(docx_path)
        assert result["success"], result.get("stderr", "")
        assert "Extractable" in result["text"]
        print(f"\n  Text: {result['text'][:80]}...")

    def test_batch_convert(self, tmp_path):
        for i in range(2):
            (tmp_path / f"file{i}.txt").write_text(f"File {i} content")
        from cli_anything.libreoffice.core.convert import do_batch_convert
        results = do_batch_convert(str(tmp_path), "*.txt", "pdf", str(tmp_path), json_output=True)
        assert len(results) == 2
        assert all(r["success"] for r in results)
        print(f"\n  Batch: {len(results)} files converted")


class TestCLISubprocess:
    """Tests that invoke the installed CLI command."""

    CLI_BASE = _resolve_cli("cli-anything-libreoffice")

    def _run(self, args, check=True):
        return subprocess.run(
            self.CLI_BASE + args,
            capture_output=True, text=True,
            check=check,
        )

    def test_help(self):
        result = self._run(["--help"])
        assert result.returncode == 0
        assert "convert" in result.stdout

    def test_version(self):
        result = self._run(["version"])
        assert result.returncode == 0
        assert "LibreOffice" in result.stdout

    def test_formats_json(self):
        result = self._run(["formats", "--json"])
        assert result.returncode == 0
        import json
        data = json.loads(result.stdout)
        assert "writer" in data

    def test_convert_txt_to_pdf(self, tmp_path):
        src = tmp_path / "cli_test.txt"
        src.write_text("CLI test content")
        outdir = str(tmp_path)
        result = self._run(["convert", str(src), "pdf", "--outdir", outdir, "--json"])
        assert result.returncode == 0, result.stderr
        import json
        data = json.loads(result.stdout)
        assert data["success"]
        assert os.path.exists(data["output"])
        print(f"\n  CLI PDF: {data['output']} ({os.path.getsize(data['output']):,} bytes)")
