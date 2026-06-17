# cli-anything-libreoffice

CLI harness for LibreOffice. Converts documents, extracts text, and performs batch operations via the real `soffice` backend.

## Installation

### Prerequisites

LibreOffice must be installed:

```bash
# macOS
brew install --cask libreoffice

# Debian/Ubuntu
apt install libreoffice

# Fedora
dnf install libreoffice
```

### Install the CLI

```bash
cd /path/to/agent-harness
pip install -e .
```

Verify:

```bash
cli-anything-libreoffice --help
```

## Usage

### Interactive REPL (default)

```bash
cli-anything-libreoffice
```

### Convert a document

```bash
cli-anything-libreoffice convert report.docx pdf
cli-anything-libreoffice convert data.xlsx csv --outdir ./exports
```

### Extract text

```bash
cli-anything-libreoffice text document.docx
```

### Document info

```bash
cli-anything-libreoffice info spreadsheet.xlsx --json
```

### Batch conversion

```bash
cli-anything-libreoffice batch ./docs "*.docx" pdf --outdir ./pdfs
```

### List supported formats

```bash
cli-anything-libreoffice formats
```

### Merge PDFs

```bash
cli-anything-libreoffice merge a.pdf b.pdf c.pdf -o merged.pdf
```

## JSON Output

Every command supports `--json` for machine parsing:

```bash
cli-anything-libreoffice convert file.docx pdf --json
```

## REPL Commands

| Command | Description |
|---------|-------------|
| `convert <file> <format>` | Convert a document |
| `text <file>` | Extract text content |
| `info <file>` | Show document info |
| `batch <dir> <pattern> <format>` | Batch convert |
| `formats` | List supported formats |
| `merge <files> -o <out>` | Merge PDFs |
| `version` | Show LibreOffice version |
| `help` | Show help |
| `quit` | Exit REPL |
