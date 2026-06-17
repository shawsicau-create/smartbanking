#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
样式配置双向同步工具
解析 LaTeX 配置文件并与 JSON 分析结果对比

使用方法:
    # 对比配置
    python scripts/sync_config.py projects/NSFC_Young/extraTex/@config.tex --analysis word_baseline_analysis.json

    # 自动应用修改
    python scripts/sync_config.py @config.tex --analysis word_baseline_analysis.json --apply

    # 预览模式
    python scripts/sync_config.py @config.tex --analysis word_baseline_analysis.json --dry-run
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, Any, List, Tuple
from datetime import datetime


class LatexConfigParser:
    """LaTeX 配置解析器"""

    def __init__(self, config_file: Path):
        self.config_file = config_file
        self.content = config_file.read_text(encoding="utf-8") if config_file.exists() else ""
        self.config = {}

    def parse(self) -> Dict[str, Any]:
        """解析配置文件"""
        self.config = {
            "colors": self._parse_colors(),
            "font_sizes": self._parse_font_sizes(),
            "page_margins": self._parse_page_margins(),
            "line_spacing": self._parse_line_spacing(),
            "title_formats": self._parse_title_formats(),
        }
        return self.config

    def _parse_colors(self) -> Dict[str, Dict[str, Any]]:
        """解析颜色定义"""
        colors = {}

        # 匹配 \definecolor{name}{model}{value}
        pattern = r"\\definecolor\{(\w+)\}\s*\{(\w+)\}\s*\{([^}]+)\}"
        matches = re.findall(pattern, self.content)

        for name, model, value in matches:
            if model == "RGB":
                # 解析 RGB 值: 0,112,192
                rgb_values = [int(x.strip()) for x in value.split(",")]
                colors[name] = {
                    "model": model,
                    "value": value,
                    "rgb": rgb_values
                }
            else:
                colors[name] = {"model": model, "value": value}

        return colors

    def _parse_font_sizes(self) -> Dict[str, Dict[str, Any]]:
        """解析字号定义"""
        font_sizes = {}

        # 匹配 \newcommand{\name}{\fontsize{size}{leading}\selectfont}
        pattern = r"\\newcommand\{\\(\w+)\}\s*\{\s*\\fontsize\{([0-9.]+)\s*pt?\}\{([0-9.]+)\s*pt?\}"
        matches = re.findall(pattern, self.content)

        for name, size, leading in matches:
            font_sizes[name] = {
                "size": float(size),
                "leading": float(leading)
            }

        return font_sizes

    def _parse_page_margins(self) -> Dict[str, float]:
        """解析页面边距"""
        margins = {}

        # 匹配 \geometry{left=Xcm, right=Ycm, ...}
        pattern = r"\\geometry\s*\{[^}]*left=([0-9.]+)cm[^}]*right=([0-9.]+)cm[^}]*top=([0-9.]+)cm[^}]*bottom=([0-9.]+)cm"
        match = re.search(pattern, self.content)

        if match:
            margins = {
                "left": float(match.group(1)),
                "right": float(match.group(2)),
                "top": float(match.group(3)),
                "bottom": float(match.group(4))
            }

        return margins

    def _parse_line_spacing(self) -> float:
        """解析行距设置"""
        # 匹配 \renewcommand{\baselinestretch}{value}
        pattern = r"\\renewcommand\{\\baselinestretch\}\s*\{([0-9.]+)\}"
        match = re.search(pattern, self.content)

        if match:
            return float(match.group(1))

        # 备选: \linespread{value}
        pattern = r"\\linespread\s*\{([0-9.]+)\}"
        match = re.search(pattern, self.content)

        if match:
            return float(match.group(1))

        return None

    def _parse_title_formats(self) -> Dict[str, Dict[str, Any]]:
        """解析标题格式"""
        formats = {}

        # 匹配 \titleformat{\section}... \hspace*{2em}（仅抽取缩进值）
        pattern = r"\\titleformat\{\\(\w+)\}.*?\\hspace\*\{([0-9.]+)\s*em\}"
        for m in re.finditer(pattern, self.content, flags=re.DOTALL):
            name = m.group(1)
            indent = m.group(2)
            try:
                formats[name] = {"indent": float(indent)}
            except Exception:
                continue

        return formats


def compare_configs(latex_config: Dict[str, Any], json_analysis: Dict[str, Any],
                   tolerance: Dict[str, float] = None) -> List[Dict[str, Any]]:
    """
    对比 LaTeX 配置与 JSON 分析结果

    Args:
        latex_config: LaTeX 解析的配置
        json_analysis: PDF 分析的 JSON 结果
        tolerance: 容差设置

    Returns:
        差异列表
    """
    if tolerance is None:
        tolerance = {
            "color_diff": 2,
            "font_size_diff": 0.5,
            "margin_diff": 0.5,
            "line_spacing_diff": 0.1,
        }

    differences = []

    # 对比颜色
    if "MsBlue" in latex_config.get("colors", {}):
        latex_rgb = latex_config["colors"]["MsBlue"]["rgb"]
        # 从 JSON 分析中提取颜色（假设在 font_usage 中）
        json_colors = json_analysis.get("font_usage", [])
        expected_rgb = [0, 112, 192]  # 默认值

        for font in json_colors:
            if "color" in font and len(font["color"]) > 0:
                # 找到第一个非黑色颜色
                color = font["color"][0]
                if color != [0, 0, 0]:
                    expected_rgb = color
                    break

        color_diff = max(abs(latex_rgb[i] - expected_rgb[i]) for i in range(3))

        if color_diff > tolerance["color_diff"]:
            differences.append({
                "type": "color",
                "name": "MsBlue",
                "latex_value": latex_rgb,
                "expected_value": expected_rgb,
                "diff": color_diff,
                "severity": "error" if color_diff > 5 else "warning"
            })

    # 对比页面边距
    latex_margins = latex_config.get("page_margins", {})
    json_page = json_analysis.get("page_layout", {})

    if latex_margins and json_page:
        margin_names = ["left", "right", "top", "bottom"]
        for name in margin_names:
            latex_value = latex_margins.get(name)
            json_value = json_page.get("margins", {}).get(name)

            if latex_value and json_value:
                diff = abs(latex_value - json_value)
                if diff > tolerance["margin_diff"]:
                    differences.append({
                        "type": "margin",
                        "name": name,
                        "latex_value": latex_value,
                        "expected_value": json_value,
                        "diff": diff,
                        "severity": "error" if diff > 1.0 else "warning"
                    })

    # 对比行距
    latex_line_spacing = latex_config.get("line_spacing")
    json_line_spacing = json_analysis.get("line_spacing", {}).get("average")

    if latex_line_spacing and json_line_spacing:
        # 将 pt 转换为倍数（假设 12pt 字号）
        expected_ratio = json_line_spacing / 12.0
        diff = abs(latex_line_spacing - expected_ratio)

        if diff > tolerance["line_spacing_diff"]:
            differences.append({
                "type": "line_spacing",
                "name": "baselinestretch",
                "latex_value": latex_line_spacing,
                "expected_value": expected_ratio,
                "diff": diff,
                "severity": "error" if diff > 0.2 else "warning"
            })

    return differences


def generate_modification_suggestions(differences: List[Dict[str, Any]],
                                     config_file: Path) -> List[str]:
    """生成修改建议"""
    suggestions = []

    for diff in differences:
        if diff["type"] == "color":
            r, g, b = diff["expected_value"]
            suggestions.append(
                f"修改颜色 {diff['name']}: \\definecolor{{{diff['name']}}}{{RGB}}{{{{{r},{g},{b}}}}}"
            )

        elif diff["type"] == "margin":
            suggestions.append(
                f"修改边距 {diff['name']}: {diff['name']}={diff['expected_value']:.2f}cm"
            )

        elif diff["type"] == "line_spacing":
            suggestions.append(
                f"修改行距: \\renewcommand{{\\baselinestretch}}{{{diff['expected_value']:.2f}}}"
            )

    return suggestions


def apply_modifications(config_file: Path, differences: List[Dict[str, Any]],
                       dry_run: bool = False) -> bool:
    """应用修改"""
    if not differences:
        print("✅ 没有需要修改的配置")
        return True

    content = config_file.read_text(encoding="utf-8")
    original_content = content

    for diff in differences:
        if diff["type"] == "color":
            # 修改颜色定义
            color_name = re.escape(str(diff["name"]))
            pattern = rf"\\definecolor\{{{color_name}\}}\s*\{{RGB\}}\s*\{{[^}}]+\}}"
            replacement = f"\\definecolor{{{diff['name']}}}{{RGB}}{{{','.join(map(str, diff['expected_value']))}}}"
            content = re.sub(pattern, lambda _: replacement, content)

        elif diff["type"] == "line_spacing":
            # 修改行距
            pattern = r"\\renewcommand\{\\baselinestretch\}\s*\{[0-9.]+\}"
            replacement = f"\\renewcommand{{\\baselinestretch}}{{{diff['expected_value']:.2f}}}"
            content = re.sub(pattern, lambda _: replacement, content)

    if dry_run:
        print("🔍 预览模式 - 不会实际修改文件")
        print("\n将进行以下修改:")
        print("=" * 60)
        print(content)
        print("=" * 60)
    else:
        if content != original_content:
            config_file.write_text(content, encoding="utf-8")
            print(f"✅ 已修改配置文件: {config_file}")

            # 备份原文件
            backup_file = config_file.with_suffix(".tex.bak")
            backup_file.write_text(original_content, encoding="utf-8")
            print(f"📦 已备份原文件: {backup_file}")
        else:
            print("✅ 配置文件无需修改")

    return True


def main():
    parser = argparse.ArgumentParser(description="LaTeX 配置同步工具")
    parser.add_argument("config_file", type=Path, help="LaTeX 配置文件路径")
    parser.add_argument("--analysis", type=Path, required=True, help="PDF 分析 JSON 文件")
    parser.add_argument("--apply", action="store_true", help="自动应用修改")
    parser.add_argument("--dry-run", action="store_true", help="预览模式")

    args = parser.parse_args()

    # 检查文件
    if not args.config_file.exists():
        print(f"错误: 配置文件不存在: {args.config_file}")
        sys.exit(1)

    if not args.analysis.exists():
        print(f"错误: 分析文件不存在: {args.analysis}")
        sys.exit(1)

    print(f"📖 正在解析 LaTeX 配置: {args.config_file}")
    parser = LatexConfigParser(args.config_file)
    latex_config = parser.parse()

    print(f"📖 正在读取 PDF 分析结果: {args.analysis}")
    with open(args.analysis, "r", encoding="utf-8") as f:
        json_analysis = json.load(f)

    print("\n🔍 正在对比配置...")
    differences = compare_configs(latex_config, json_analysis)

    if not differences:
        print("✅ 配置完全一致！")
        return

    print(f"\n发现 {len(differences)} 处差异:")
    print("=" * 60)

    for diff in differences:
        severity_icon = "❌" if diff["severity"] == "error" else "⚠️"
        print(f"\n{severity_icon} {diff['type']} - {diff['name']}")
        print(f"   当前值: {diff['latex_value']}")
        print(f"   期望值: {diff['expected_value']}")
        print(f"   差异: {diff['diff']}")

    # 生成修改建议
    suggestions = generate_modification_suggestions(differences, args.config_file)

    if suggestions:
        print(f"\n💡 修改建议:")
        print("=" * 60)
        for i, suggestion in enumerate(suggestions, 1):
            print(f"{i}. {suggestion}")

    # 应用修改
    if args.apply or args.dry_run:
        apply_modifications(args.config_file, differences, args.dry_run)
    else:
        print("\n💡 使用 --apply 查看修改效果")
        print("💡 使用 --dry-run 预览修改（不实际修改文件）")


if __name__ == "__main__":
    main()
