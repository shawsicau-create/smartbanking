# Test Plan — cli-anything-libreoffice

## Test Inventory

- `test_core.py`: 4 unit tests planned
- `test_full_e2e.py`: 5 E2E tests planned

## Unit Test Plan

### test_backend.py

| Function | What to test | Edge cases | Count |
|----------|-------------|------------|-------|
| `find_libreoffice()` | Returns path when installed | Raises RuntimeError when missing | 2 |
| `list_supported_formats()` | Returns dict with writer/calc/impress/draw | — | 1 |
| `get_document_info()` | Returns correct type by extension | Unknown extension -> "unknown" | 2 |

## E2E Test Plan

### Real backend tests

| Test | Workflow | Verification |
|------|----------|-------------|
| `test_txt_to_pdf` | Create txt -> convert to pdf | File exists, size > 0, magic bytes `%PDF-` |
| `test_txt_to_docx` | Create txt -> convert to docx | File exists, valid ZIP (OOXML) |
| `test_text_extraction` | Create docx -> extract text | Text content matches input |
| `test_batch_convert` | Create 2 txt files -> batch to pdf | Both succeed |
| `test_cli_subprocess` | Invoke installed CLI for convert | Returncode 0, output file exists |

## Workflow Scenarios

1. **Document pipeline**: txt -> docx -> pdf roundtrip
2. **Batch report generation**: Multiple spreadsheets -> PDF export
3. **Text mining prep**: Mixed documents -> unified text extraction
