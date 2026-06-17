---
name: cli-anything-libreoffice
description: CLI harness for LibreOffice — document conversion, text extraction, and
  batch operations via the real soffice backend.
workflow_stage: communication
compatibility:
- claude-code
- cursor
- codex
author: Qoder Skills Library
version: 1.0.0
tags:
- cli
- anything
- libreoffice
---


# cli-anything-libreoffice

Use when you need to convert documents between formats (docx/pdf/csv/etc.), extract text from Office documents, merge PDFs, or perform batch document operations.

## Commands

- `cli-anything-libreoffice convert <file> <format>` — Convert a document
- `cli-anything-libreoffice text <file>` — Extract plain text
- `cli-anything-libreoffice info <file>` — Show document metadata
- `cli-anything-libreoffice batch <dir> <pattern> <format>` — Batch convert
- `cli-anything-libreoffice formats` — List supported formats
- `cli-anything-libreoffice merge <files> -o <output>` — Merge PDFs

All commands support `--json` for machine-readable output.
