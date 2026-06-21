---
name: cli-anything
description: Build stateful CLI interfaces for GUI apps via cli-anything methodology.
workflow_stage: communication
compatibility:
  - claude-code
  - cursor
  - codex
author: Qoder Skills Library
version: 1.0.0
tags:
  - cli
  - gui
  - automation
  - harness
argument-hint: "[software-path-or-repo] [command options]"
allowed-tools: Bash(*), Read, Write, Edit, Glob, Grep
---

# CLI-Anything Skill for Qoder

Build complete, stateful CLI harnesses for any GUI application using the cli-anything methodology. This skill transforms GUI applications into agent-usable CLIs with REPL mode, JSON output, undo/redo, and comprehensive test coverage.

## CRITICAL: Read HARNESS.md First

**Before doing anything else, you MUST read the HARNESS.md documentation** (located in the skill's assets directory). It defines the complete methodology, architecture standards, and implementation patterns. Every phase below follows HARNESS.md. Do not improvise — follow the harness specification.

## Workflow: MUST EXECUTE ALL STEPS

### Step 0: Pre-flight Check

1. **Verify prerequisites:**
   - Python 3.10+
   - `click` - CLI framework
   - `pytest` - Testing framework
   - `prompt_toolkit` - For REPL interface

2. **Install dependencies if needed:**
```bash
pip install click pytest prompt_toolkit
```

### Step 1: Understand the Target Software

Parse the input: **$ARGUMENTS**

1. **Accept software source:**
   - Local path to software source code (e.g., `/home/user/gimp`, `./blender`)
   - GitHub repository URL (e.g., `https://github.com/GNOME/gimp`)
   
2. **Software names alone are NOT accepted** (e.g., "gimp" alone is invalid)
   - User must provide actual source code path or repository URL
   - This allows the agent to analyze the codebase

3. **If GitHub URL provided:**
   - Clone the repository to a local working directory first
   - Work on the local copy

### Step 2: Phase 0 - Source Acquisition

```bash
# If GitHub URL provided
git clone <repository-url> <local-directory>

# Verify the local path exists and contains source code
ls -la <software-path>

# Derive software name from directory name
# e.g., /home/user/gimp -> gimp
```

### Step 3: Phase 1 - Codebase Analysis

Analyze the target software:

1. **Identify the backend engine:**
   - Most GUI apps separate presentation from logic
   - Find the core library/framework (e.g., MLT for Shotcut, ImageMagick for GIMP)

2. **Map GUI actions to API calls:**
   - Every button click, drag, and menu item corresponds to a function call
   - Catalog these mappings

3. **Identify the data model:**
   - What file formats does it use?
   - How is project state represented? (XML, JSON, binary, database?)

4. **Find existing CLI tools:**
   - Many backends ship their own CLI (`melt`, `ffmpeg`, `convert`)
   - These are building blocks

5. **Catalog the command/undo system:**
   - If the app has undo/redo, it likely uses a command pattern
   - These commands are your CLI operations

### Step 4: Phase 2 - CLI Architecture Design

Design the CLI structure:

1. **Choose the interaction model:**
   - **Stateful REPL** for interactive sessions (agents that maintain context)
   - **Subcommand CLI** for one-shot operations (scripting, pipelines)
   - **Both** (recommended) — a CLI that works in both modes

2. **Define command groups** matching the app's logical domains:
   - Project management (new, open, save, close)
   - Core operations (the app's primary purpose)
   - Import/Export (file I/O, format conversion)
   - Configuration (settings, preferences, profiles)
   - Session/State management (undo, redo, history, status)

3. **Design the state model:**
   - What must persist between commands? (open project, cursor position, selection)
   - Where is state stored? (in-memory for REPL, file-based for CLI)
   - How does state serialize? (JSON session files)

4. **Plan the output format:**
   - Human-readable (tables, colors) for interactive use
   - Machine-readable (JSON) for agent consumption
   - Both, controlled by `--json` flag

5. **Create software-specific SOP document** (e.g., GIMP.md)

### Step 5: Phase 3 - Implementation

Create the directory structure and implement:

```
<software-name>/
└── agent-harness/
    ├── <SOFTWARE>.md          # Software-specific SOP
    ├── setup.py               # PyPI package config
    └── cli_anything/          # Namespace package
        └── <software>/        # Sub-package
            ├── README.md          # Installation and usage guide
            ├── <software>_cli.py  # Main CLI entry point
            ├── core/              # Core modules
            │   ├── project.py
            │   ├── session.py
            │   ├── export.py
            │   └── ...
            ├── utils/             # Utilities
            │   ├── repl_skin.py   # Copied from skill assets
            │   └── <software>_backend.py
            └── tests/
                ├── TEST.md
                ├── test_core.py
                └── test_full_e2e.py
```

**Implementation steps:**

1. **Start with the data layer** — XML/JSON manipulation of project files

2. **Add probe/info commands** — Let agents inspect before they modify

3. **Add mutation commands** — One command per logical operation

4. **Add the backend integration** — Create `utils/<software>_backend.py`:
   ```python
   # Example backend module
   import shutil
   import subprocess
   
   def find_software_executable():
       """Find the software executable"""
       exe = shutil.which("<software-executable>")
       if not exe:
           raise RuntimeError(
               f"<Software> not found. Install it first:\n"
               f"  sudo apt install <package-name>\n"
               f"  # or\n"
               f"  pip install <package-name>"
           )
       return exe
   
   def invoke_backend(operation, *args, **kwargs):
       """Invoke the real software's CLI"""
       exe = find_software_executable()
       result = subprocess.run(
           [exe, *args],
           capture_output=True,
           text=True,
           check=False
       )
       return {
           "success": result.returncode == 0,
           "stdout": result.stdout,
           "stderr": result.stderr,
           "returncode": result.returncode
       }
   ```

5. **Add rendering/export** — The export pipeline calls the backend module

6. **Add session management** — State persistence, undo/redo

7. **Add the REPL with unified skin:**
   - Copy `repl_skin.py` from skill assets to `utils/repl_skin.py`
   - Import and use `ReplSkin` for the REPL interface
   - Make REPL the default behavior when no subcommand is given

### Step 6: Phase 4 - Test Planning

Create `TEST.md` with comprehensive test plan:

1. Plan unit tests for all core modules
2. Plan E2E tests with real files
3. Design realistic workflow scenarios
4. Include output verification (pixel analysis, format validation, etc.)

### Step 7: Phase 5 - Test Implementation

Write tests:

1. **Unit tests** (`test_core.py`):
   - Synthetic data, no external dependencies
   - Test each core module independently

2. **E2E tests** (`test_full_e2e.py`):
   - Real files, full pipeline
   - Workflow tests simulating real-world usage
   - Add `TestCLISubprocess` class with `_resolve_cli("cli-anything-<software>")`
   - Test the installed command via subprocess (no hardcoded paths or CWD)

3. **Run tests and document results:**
```bash
pytest -v --tb=no
# Append full test results to TEST.md
```

### Step 8: Phase 6 - PyPI Packaging and Installation

Create `setup.py`:

```python
from setuptools import setup, find_namespace_packages

setup(
    name="cli-anything-<software>",
    version="0.1.0",
    packages=find_namespace_packages(include=["cli_anything.*"]),
    namespace_packages=["cli_anything"],  # PEP 420
    install_requires=[
        "click>=8.0",
        "prompt_toolkit>=3.0",
    ],
    entry_points={
        "console_scripts": [
            f"cli-anything-<software>=cli_anything.<software>.<software>_cli:cli",
        ],
    },
)
```

**Package structure:**
- Package name: `cli-anything-<software>`
- Namespace: `cli_anything.<software>`
- `cli_anything/` has NO `__init__.py` (PEP 420 namespace package)
- `<software>/` sub-package HAS `__init__.py`

**Install and verify:**
```bash
# Test local installation
pip install -e .

# Verify CLI is available in PATH
which cli-anything-<software>
cli-anything-<software> --help
```

## Commands Reference

### Primary Command

**Usage:** `/cli-anything <software-path-or-repo> [options]`

Builds a complete CLI harness for the specified GUI application.

**Options:**
- `--refine` - Refine an existing CLI to expand coverage
- `--test` - Run tests for an existing CLI harness
- `--list` - List all available CLI-Anything tools

### List Command

**Usage:** `/cli-anything --list [--path <directory>] [--depth <n>] [--json]`

List all available CLI-Anything tools (installed and generated).

**Options:**
- `--path <directory>` - Directory to search for generated CLIs (default: current directory)
- `--depth <n>` - Maximum recursion depth for scanning (default: unlimited)
- `--json` - Output in JSON format for machine parsing

## Output Format

The skill generates a complete, production-ready CLI harness with:

1. **Full CLI implementation** with Click-based subcommands
2. **REPL interface** with prompt_toolkit styling
3. **Backend integration** that invokes the real software
4. **Comprehensive test suite** (unit + E2E)
5. **Documentation** (README, SOP, TEST.md)
6. **PyPI package** ready for distribution

## Examples

### Build CLI for GIMP

```bash
/cli-anything /home/user/gimp
```

This will:
1. Analyze GIMP's codebase and backend (ImageMagick, GEGL)
2. Design CLI commands for image editing operations
3. Implement core modules (project, session, export)
4. Create tests for all functionality
5. Package as `cli-anything-gimp`

### Build CLI from GitHub Repo

```bash
/cli-anything https://github.com/blender/blender
```

This will:
1. Clone the Blender repository
2. Analyze Blender's architecture
3. Build a complete CLI for Blender operations
4. Package as `cli-anything-blender`

### Refine Existing CLI

```bash
/cli-anything /home/user/gimp --refine "particle systems and effects"
```

Analyzes gaps and adds new commands for the specified functionality area.

### Run Tests

```bash
/cli-anything /home/user/gimp --test
```

Runs all tests and updates TEST.md with results.

## Math Formulas in Documentation

When documenting CLI commands that involve mathematical operations, use LaTeX notation:
- Subscripts: `$x_i$`, `$\\alpha_{ij}$`
- Superscripts: `$x^2$`, `$e^{i\\pi}$`
- Fractions: `$\\frac{a}{b}$`
- Greek letters: `$\\alpha$`, `$\\beta$`, `$\\gamma$`
- Matrices: `$\\begin{bmatrix} a & b \\\\ c & d \\end{bmatrix}$`

## Related Documentation

- **HARNESS.md** - Complete methodology and architecture (in skill assets)
- **QUICKSTART.md** - Quick start guide (in skill assets)
- **PUBLISHING.md** - Publishing to PyPI (in skill assets)
