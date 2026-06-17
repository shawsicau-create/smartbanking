#!/usr/bin/env python3
"""Literature Toolkit CLI - Main entry point."""

import click
import sys
from pathlib import Path
from typing import List

from .parsers import parse_file, LiteratureItem
from .analyzer import LiteratureAnalyzer
from .zhizhen_search import ZhizhenSearcher, print_search_template


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Literature Toolkit - 文献管理工具箱

    支持格式: RIS, EndNote, NoteExpress, BibTeX

    示例:
        lit import references.ris --analyze
        lit search "金融治理" --year 2020-2024
        lit merge file1.ris file2.enw --output merged.ris
    """
    pass


@cli.command()
@click.argument("files", nargs=-1, required=True, type=click.Path(exists=True))
@click.option("--output", "-o", help="输出文件路径")
@click.option("--format", "fmt", default="gb7714", type=click.Choice(["gb7714", "apa"]),
              help="引用格式")
@click.option("--dedupe", is_flag=True, help="去重")
@click.option("--analyze", is_flag=True, help="生成分析报告")
@click.option("--year-from", type=int, help="起始年份")
@click.option("--year-to", type=int, help="截止年份")
def import_files(files, output, fmt, dedupe, analyze, year_from, year_to):
    """导入文献文件并处理。"""
    all_items = []

    for filepath in files:
        click.echo(f"正在解析: {filepath}")
        items = parse_file(filepath)
        click.echo(f"  找到 {len(items)} 条文献")
        all_items.extend(items)

    click.echo(f"\n总计: {len(all_items)} 条文献")

    analyzer = LiteratureAnalyzer(all_items)

    # Filter by year
    if year_from or year_to:
        all_items = analyzer.filter_by_year(year_from, year_to)
        click.echo(f"年份筛选后: {len(all_items)} 条")
        analyzer = LiteratureAnalyzer(all_items)

    # Deduplicate
    if dedupe:
        all_items = analyzer.deduplicate()
        click.echo(f"去重后: {len(all_items)} 条")
        analyzer = LiteratureAnalyzer(all_items)

    # Analyze
    if analyze:
        click.echo("\n" + analyzer.generate_report())

    # Export references
    if output:
        refs = analyzer.export_references(fmt)
        Path(output).write_text(refs, encoding="utf-8")
        click.echo(f"\n已导出到: {output}")


@cli.command()
@click.argument("query")
@click.option("--database", "-d", type=click.Choice(["cnki", "wanfang", "vip", "all"]),
              default="all", help="数据库")
@click.option("--year", "-y", help="年份范围, 如: 2020-2024")
@click.option("--type", "doc_type", default="journal",
              type=click.Choice(["journal", "thesis", "book", "conference"]),
              help="文献类型")
def search(query, database, year, doc_type):
    """在超星发现系统检索文献。"""
    searcher = ZhizhenSearcher()

    year_from = None
    year_to = None
    if year:
        parts = year.split("-")
        year_from = int(parts[0]) if parts[0] else None
        year_to = int(parts[1]) if len(parts) > 1 and parts[1] else None

    url = searcher.build_search_url(
        query=query,
        database=database if database != "all" else None,
        year_from=year_from,
        year_to=year_to,
        doc_type=doc_type
    )

    click.echo(f"""
╔══════════════════════════════════════════════════════════════╗
║                    超星发现系统检索                            ║
╚══════════════════════════════════════════════════════════════╝

检索词: {query}
数据库: {database}
年份: {year or "不限"}
类型: {doc_type}

检索链接:
{url}

请复制链接到浏览器打开，登录后即可查看结果。
导出文献后使用 `lit import` 命令处理。
""")


@cli.command()
@click.argument("files", nargs=-1, required=True, type=click.Path(exists=True))
@click.option("--output", "-o", required=True, help="输出文件")
@click.option("--format", "fmt", default="ris", type=click.Choice(["ris", "bib"]),
              help="输出格式")
def merge(files, output, fmt):
    """合并多个文献文件。"""
    all_items = []

    for filepath in files:
        click.echo(f"导入: {filepath}")
        items = parse_file(filepath)
        all_items.extend(items)

    click.echo(f"总计: {len(all_items)} 条文献")

    # Deduplicate
    analyzer = LiteratureAnalyzer(all_items)
    unique_items = analyzer.deduplicate()
    click.echo(f"去重后: {len(unique_items)} 条 (移除 {len(all_items) - len(unique_items)} 条重复)")

    # Export
    if fmt == "ris":
        content = _export_ris(unique_items)
    else:
        content = _export_bibtex(unique_items)

    Path(output).write_text(content, encoding="utf-8")
    click.echo(f"已保存到: {output}")


@cli.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("--keywords", "-k", help="关键词筛选, 逗号分隔")
@click.option("--journals", "-j", help="期刊筛选, 逗号分隔")
@click.option("--year-from", type=int, help="起始年份")
@click.option("--year-to", type=int, help="截止年份")
def filter_file(file, keywords, journals, year_from, year_to):
    """筛选文献。"""
    items = parse_file(file)
    analyzer = LiteratureAnalyzer(items)

    # Apply filters
    if keywords:
        kw_list = [k.strip() for k in keywords.split(",")]
        items = analyzer.filter_by_keyword(kw_list)
        click.echo(f"关键词筛选后: {len(items)} 条")
        analyzer = LiteratureAnalyzer(items)

    if journals:
        j_list = [j.strip() for j in journals.split(",")]
        items = analyzer.filter_by_journal(j_list)
        click.echo(f"期刊筛选后: {len(items)} 条")
        analyzer = LiteratureAnalyzer(items)

    if year_from or year_to:
        items = analyzer.filter_by_year(year_from, year_to)
        click.echo(f"年份筛选后: {len(items)} 条")

    # Print results
    for i, item in enumerate(items[:20], 1):
        click.echo(f"\n[{i}] {item.title}")
        click.echo(f"    作者: {', '.join(item.authors[:3])}")
        click.echo(f"    期刊: {item.journal} ({item.year})")

    if len(items) > 20:
        click.echo(f"\n... 还有 {len(items) - 20} 条")


@cli.command()
@click.argument("topic")
@click.argument("keywords", nargs=-1)
def template(topic, keywords):
    """生成检索模板。"""
    if not keywords:
        keywords = [topic]
    print_search_template(topic, list(keywords))


@cli.command()
def guide():
    """显示文献导出指南。"""
    searcher = ZhizhenSearcher()
    click.echo(searcher.get_export_instructions())


def _export_ris(items: List[LiteratureItem]) -> str:
    """Export to RIS format."""
    lines = []
    for item in items:
        lines.append("TY  - JOUR")
        if item.title:
            lines.append(f"TI  - {item.title}")
        for author in item.authors:
            lines.append(f"AU  - {author}")
        if item.year:
            lines.append(f"PY  - {item.year}")
        if item.journal:
            lines.append(f"JO  - {item.journal}")
        if item.volume:
            lines.append(f"VL  - {item.volume}")
        if item.issue:
            lines.append(f"IS  - {item.issue}")
        if item.pages:
            lines.append(f"SP  - {item.pages}")
        if item.doi:
            lines.append(f"DO  - {item.doi}")
        if item.abstract:
            lines.append(f"AB  - {item.abstract}")
        for kw in item.keywords:
            lines.append(f"KW  - {kw}")
        if item.url:
            lines.append(f"UR  - {item.url}")
        lines.append("ER  -")
        lines.append("")
    return "\n".join(lines)


def _export_bibtex(items: List[LiteratureItem]) -> str:
    """Export to BibTeX format."""
    lines = []
    for i, item in enumerate(items, 1):
        key = f"ref{i}"
        lines.append(f"@article{{{key},")
        if item.title:
            lines.append(f"  title = {{{item.title}}},")
        if item.authors:
            authors = " and ".join(item.authors)
            lines.append(f"  author = {{{authors}}},")
        if item.journal:
            lines.append(f"  journal = {{{item.journal}}},")
        if item.year:
            lines.append(f"  year = {{{item.year}}},")
        if item.volume:
            lines.append(f"  volume = {{{item.volume}}},")
        if item.issue:
            lines.append(f"  number = {{{item.issue}}},")
        if item.pages:
            lines.append(f"  pages = {{{item.pages}}},")
        if item.doi:
            lines.append(f"  doi = {{{item.doi}}},")
        lines.append("}")
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    cli()
