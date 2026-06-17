"""Main CLI entry point for cli-anything-libreoffice."""

import json
import os
import sys
from pathlib import Path

import click

from .core.convert import do_batch_convert, do_convert, do_info, do_list_formats
from .utils.libreoffice_backend import (
    convert_to_text,
    find_libreoffice,
    get_version,
    merge_pdfs,
)
from .utils.repl_skin import ReplSkin


# ── Shared options ─────────────────────────────────────────────────────

def _json_option(f):
    return click.option(
        "--json", "json_output", is_flag=True,
        help="Output in JSON format for machine parsing."
    )(f)


def _print_json(data: dict):
    click.echo(json.dumps(data, ensure_ascii=False, indent=2))


# ── REPL command ───────────────────────────────────────────────────────

@click.command(name="repl")
def repl_cmd():
    """Start interactive REPL session."""
    skin = ReplSkin("libreoffice", version="0.1.0")
    skin.print_banner()

    commands = {
        "convert <file> <format>": "Convert a document to another format",
        "text <file>": "Extract text content from a document",
        "info <file>": "Show document information",
        "formats": "List supported conversion formats",
        "version": "Show LibreOffice version",
        "merge <file1> <file2> ... -o <out>": "Merge PDFs",
        "batch <dir> <pattern> <format>": "Batch convert files",
        "help": "Show this help",
        "quit": "Exit REPL",
    }

    pt_session = skin.create_prompt_session()

    while True:
        try:
            line = skin.get_input(pt_session)
        except (EOFError, KeyboardInterrupt):
            break

        if not line:
            continue

        parts = line.strip().split()
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd in ("quit", "exit", "q"):
            break

        if cmd == "help":
            skin.help(commands)
            continue

        if cmd == "version":
            try:
                ver = get_version()
                skin.info(ver)
            except RuntimeError as e:
                skin.error(str(e))
            continue

        if cmd == "formats":
            fmts = do_list_formats(json_output=True)
            skin.section("Supported Formats")
            for doc_type, exts in fmts.items():
                skin.status(doc_type.title(), ", ".join(exts))
            continue

        if cmd == "convert" and len(args) >= 2:
            src, fmt = args[0], args[1]
            skin.info(f"Converting {src} -> {fmt} ...")
            result = do_convert(src, fmt, json_output=True)
            if result["success"]:
                skin.success(f"Output: {result['output']}")
            else:
                skin.error(result.get("stderr", "Conversion failed"))
            continue

        if cmd == "text" and len(args) >= 1:
            src = args[0]
            result = convert_to_text(src)
            if result["success"]:
                click.echo(result["text"])
            else:
                skin.error(result.get("stderr", "Text extraction failed"))
            continue

        if cmd == "info" and len(args) >= 1:
            info = do_info(args[0], json_output=True)
            skin.status_block(info, title="Document Info")
            continue

        if cmd == "batch" and len(args) >= 3:
            d, pat, fmt = args[0], args[1], args[2]
            skin.info(f"Batch converting {pat} in {d} -> {fmt} ...")
            results = do_batch_convert(d, pat, fmt, json_output=True)
            ok = sum(1 for r in results if r["success"])
            skin.success(f"{ok}/{len(results)} files converted")
            for r in results:
                if not r["success"]:
                    skin.error(f"  Failed: {r['input']}")
            continue

        if cmd == "merge" and len(args) >= 3:
            # merge file1 file2 ... -o output
            if "-o" not in args:
                skin.error("Usage: merge <file1> <file2> ... -o <output>")
                continue
            o_idx = args.index("-o")
            inputs = args[:o_idx]
            output = args[o_idx + 1] if o_idx + 1 < len(args) else None
            if not output:
                skin.error("Missing output path")
                continue
            result = merge_pdfs(inputs, output)
            if result["success"]:
                skin.success(f"Merged: {result['output']}")
            else:
                skin.error(result.get("stderr", "Merge failed"))
            continue

        skin.warning(f"Unknown command: {cmd}. Type 'help' for commands.")

    skin.print_goodbye()


# ── Main CLI group ─────────────────────────────────────────────────────

@click.group(invoke_without_command=True)
@click.pass_context
@click.version_option(version="0.1.0", prog_name="cli-anything-libreoffice")
def cli(ctx):
    """CLI harness for LibreOffice — document conversion, text extraction,
    and batch operations via the real soffice backend.
    """
    if ctx.invoked_subcommand is None:
        ctx.invoke(repl_cmd)


# ── Subcommands ────────────────────────────────────────────────────────

@cli.command(name="convert")
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("output_format")
@click.option("-o", "--outdir", type=click.Path(), help="Output directory")
@click.option("--overwrite/--no-overwrite", default=True)
@_json_option
def convert(input_path, output_format, outdir, overwrite, json_output):
    """Convert a document to another format."""
    result = do_convert(input_path, output_format, outdir, overwrite, json_output)
    if json_output:
        _print_json(result)
        return
    if result["success"]:
        click.echo(f"✓ Converted: {result['output']}")
    else:
        click.echo(f"✗ Failed: {result.get('stderr', 'Unknown error')}", err=True)
        sys.exit(1)


@cli.command(name="text")
@click.argument("input_path", type=click.Path(exists=True))
@_json_option
def text(input_path, json_output):
    """Extract plain text from a document."""
    result = convert_to_text(input_path)
    if json_output:
        _print_json(result)
        return
    if result["success"]:
        click.echo(result["text"])
    else:
        click.echo(f"✗ Failed: {result.get('stderr', 'Unknown error')}", err=True)
        sys.exit(1)


@cli.command(name="info")
@click.argument("input_path", type=click.Path(exists=True))
@_json_option
def info(input_path, json_output):
    """Show document information."""
    result = do_info(input_path, json_output)
    if json_output:
        _print_json(result)
        return
    click.echo(f"Path:     {result['path']}")
    click.echo(f"Size:     {result['size']:,} bytes")
    click.echo(f"Type:     {result['type']}")
    click.echo(f"MIME:     {result.get('mime_type') or 'unknown'}")


@cli.command(name="formats")
@_json_option
def formats(json_output):
    """List supported conversion formats."""
    result = do_list_formats(json_output)
    if json_output:
        _print_json(result)
        return
    for doc_type, exts in result.items():
        click.echo(f"{doc_type.title():10} {', '.join(exts)}")


@cli.command(name="batch")
@click.argument("input_dir", type=click.Path(exists=True, file_okay=False))
@click.argument("pattern")
@click.argument("output_format")
@click.option("-o", "--outdir", type=click.Path(), help="Output directory")
@_json_option
def batch(input_dir, pattern, output_format, outdir, json_output):
    """Batch convert files matching a pattern."""
    results = do_batch_convert(input_dir, pattern, output_format, outdir, json_output)
    if json_output:
        _print_json({"results": results})
        return
    ok = sum(1 for r in results if r["success"])
    click.echo(f"✓ {ok}/{len(results)} files converted")
    for r in results:
        if r["success"]:
            click.echo(f"  ✓ {r['input']} -> {r['output']}")
        else:
            click.echo(f"  ✗ {r['input']}: {r.get('stderr', 'failed')}")


@cli.command(name="merge")
@click.argument("input_paths", nargs=-1, required=True)
@click.option("-o", "--output", required=True, type=click.Path(), help="Output PDF path")
def merge(input_paths, output):
    """Merge multiple PDFs into one."""
    result = merge_pdfs(list(input_paths), output)
    if result["success"]:
        click.echo(f"✓ Merged: {result['output']}")
    else:
        click.echo(f"✗ Failed: {result.get('stderr', 'Unknown error')}", err=True)
        sys.exit(1)


@cli.command(name="version")
def version_cmd():
    """Show LibreOffice version."""
    try:
        click.echo(get_version())
    except RuntimeError as e:
        click.echo(f"✗ {e}", err=True)
        sys.exit(1)


# ── Entry point ────────────────────────────────────────────────────────

if __name__ == "__main__":
    cli()
