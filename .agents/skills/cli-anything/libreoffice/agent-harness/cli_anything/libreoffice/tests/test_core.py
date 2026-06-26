"""Unit tests for cli-anything-libreoffice core modules."""

import pytest

from cli_anything.libreoffice.utils.libreoffice_backend import (
    find_libreoffice,
    get_document_info,
    list_supported_formats,
)


class TestBackend:
    def test_find_libreoffice_returns_path(self):
        path = find_libreoffice()
        assert path is not None
        assert isinstance(path, str)
        assert len(path) > 0

    def test_list_formats_has_writer(self):
        fmts = list_supported_formats()
        assert "writer" in fmts
        assert "pdf" in fmts["writer"]
        assert "docx" in fmts["writer"]

    def test_list_formats_has_calc(self):
        fmts = list_supported_formats()
        assert "calc" in fmts
        assert "csv" in fmts["calc"]

    def test_get_info_for_docx(self):
        info = get_document_info("/tmp/fake.docx")
        assert info["extension"] == ".docx"
        assert info["type"] == "writer"

    def test_get_info_for_unknown(self):
        info = get_document_info("/tmp/fake.xyz")
        assert info["type"] == "unknown"
