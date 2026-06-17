#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键式优化脚本
自动化完成 LaTeX 模板优化的完整流程

使用方法:
    # 基本用法
    python scripts/optimize.py --project NSFC_Young

    # 交互模式
    python scripts/optimize.py --project NSFC_Young --interactive

    # 生成报告
    python scripts/optimize.py --project NSFC_Young --report optimization_report.html
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
REPO_ROOT = SKILL_DIR.parent.parent
PROJECTS_ROOT = (REPO_ROOT / "projects").resolve()

sys.path.insert(0, str(SKILL_DIR))

from scripts.core.workspace_manager import WorkspaceManager


class Optimizer:
    """LaTeX 模板优化器"""

    def __init__(self, project_path: Path, interactive: bool = False):
        self.project_path = project_path.resolve()
        self.interactive = interactive
        self.steps = []
        self.results = {}
        self.ws_manager = WorkspaceManager(SKILL_DIR)
        self.workspace = self.ws_manager.get_project_workspace(self.project_path)

    def confirm(self, message: str) -> bool:
        """交互式确认"""
        if not self.interactive:
            return True

        while True:
            response = input(f"{message} [Y/n] ").strip().lower()
            if response in ["", "y", "yes"]:
                return True
            elif response in ["n", "no"]:
                return False
            else:
                print("请输入 Y 或 N")

    def run_step(self, step_name: str, func, *args, **kwargs) -> Any:
        """运行一个优化步骤"""
        print(f"\n{'='*60}")
        print(f"步骤 {len(self.steps) + 1}: {step_name}")
        print(f"{'='*60}")

        self.steps.append(step_name)

        try:
            result = func(*args, **kwargs)
            self.results[step_name] = {"status": "success", "result": result}
            return result
        except Exception as e:
            self.results[step_name] = {"status": "error", "error": str(e)}
            print(f"❌ 步骤失败: {e}")
            return None

    def analyze_word_pdf(self) -> Optional[Dict[str, Any]]:
        """步骤 1: 分析 Word PDF 基准"""
        print("正在分析 Word PDF 基准...")

        # 查找 Word PDF 基准
        baseline_dir = self.workspace / "baselines"
        word_pdf = None

        if baseline_dir.exists():
            pdf_files = list(baseline_dir.glob("word*.pdf")) or list(baseline_dir.glob("*.pdf"))
            if pdf_files:
                word_pdf = next((p for p in pdf_files if p.name.lower() == "word.pdf"), pdf_files[0])

        if not word_pdf:
            print("⚠️  未找到 Word PDF 基准")
            print("💡 请将 Word 导出的 PDF 放入 projects/{project}/.make_latex_model/baselines/word.pdf")
            return None

        # 运行 analyze_pdf.py
        script_path = Path(__file__).parent / "analyze_pdf.py"

        if not script_path.exists():
            print(f"⚠️  分析脚本不存在: {script_path}")
            return None

        result = subprocess.run(
            ["python3", str(script_path), str(word_pdf)],
            capture_output=True,
            text=True
        )

        print(result.stdout)

        # 查找生成的 JSON 文件
        json_file = word_pdf.with_name(word_pdf.stem + "_analysis.json")
        if json_file.exists():
            with open(json_file, "r", encoding="utf-8") as f:
                return json.load(f)

        return None

    def extract_headings(self) -> Optional[Dict[str, Any]]:
        """步骤 2: 提取标题文字"""
        print("正在提取标题文字...")

        # 查找 Word 模板
        template_dir = self.project_path / "template"
        word_template = None

        if template_dir.exists():
            docx_files = list(template_dir.glob("*.docx"))
            if docx_files:
                word_template = docx_files[0]

        if not word_template:
            print("⚠️  未找到 Word 模板 (.docx)")
            return None

        # 运行 compare_headings.py
        script_path = Path(__file__).parent / "compare_headings.py"
        main_tex = self.project_path / "main.tex"

        if not script_path.exists() or not main_tex.exists():
            return None

        result = subprocess.run(
            ["python3", str(script_path), str(word_template), str(main_tex)],
            capture_output=True,
            text=True
        )

        print(result.stdout)

        # 解析输出
        return {"matched": 0, "differences": 0, "only_in_one": 0}

    def compare_styles(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """步骤 3: 对比样式参数"""
        print("正在对比样式参数...")

        # 运行 sync_config.py
        script_path = Path(__file__).parent / "sync_config.py"
        config_file = self.project_path / "extraTex" / "@config.tex"

        # 查找分析 JSON
        baseline_dir = self.workspace / "baselines"
        json_file = None

        if baseline_dir.exists():
            json_files = list(baseline_dir.glob("*_analysis.json"))
            if json_files:
                json_file = json_files[0]

        if not script_path.exists() or not config_file.exists() or not json_file:
            return []

        result = subprocess.run(
            ["python3", str(script_path), str(config_file), "--analysis", str(json_file)],
            capture_output=True,
            text=True
        )

        print(result.stdout)
        return []

    def generate_suggestions(self, analysis: Dict[str, Any],
                            style_diffs: List[Dict]) -> List[str]:
        """步骤 4: 生成修改建议"""
        print("正在生成修改建议...")

        suggestions = []

        # 基于 PDF 分析生成建议
        if analysis:
            page_layout = analysis.get("page_layout", {})
            margins = page_layout.get("margins", {})

            if margins:
                suggestions.append(
                    f"调整页面边距: 左 {margins.get('left', 0):.2f}cm, "
                    f"右 {margins.get('right', 0):.2f}cm"
                )

        return suggestions

    def apply_modifications(self, suggestions: List[str]) -> bool:
        """步骤 5: 应用修改（可选）"""
        if not suggestions:
            print("✅ 没有需要修改的内容")
            return True

        print("\n修改建议:")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"  {i}. {suggestion}")

        if not self.confirm("\n是否应用这些修改？"):
            print("⏭️  跳过修改步骤")
            return True

        print("💡 请手动应用这些修改到 @config.tex")
        return True

    def compile_latex(self) -> bool:
        """步骤 6: 编译 LaTeX 项目"""
        print("正在编译 LaTeX 项目...")

        main_tex = self.project_path / "main.tex"
        if not main_tex.exists():
            print("❌ 主文件不存在")
            return False

        # 执行 xelatex 编译
        result = subprocess.run(
            ["xelatex", "-interaction=nonstopmode", "main.tex"],
            cwd=self.project_path,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("✅ 编译成功")
            return True
        else:
            print("❌ 编译失败")
            print(result.stderr[-500:])  # 只显示最后 500 字符
            return False

    def run_validators(self) -> bool:
        """步骤 7: 运行验证器"""
        print("正在运行验证器...")

        script_path = Path(__file__).parent / "run_validators.py"

        if not script_path.exists():
            print("⚠️  验证器脚本不存在")
            return False

        result = subprocess.run(
            ["python3", str(script_path), "--project", str(self.project_path)],
            capture_output=False
        )

        return result.returncode == 0

    def generate_report(self, output_path: Optional[Path] = None) -> str:
        """步骤 8: 生成优化报告"""
        print("正在生成优化报告...")

        # 生成 Markdown 报告
        lines = []
        lines.append("# LaTeX 模板优化报告")
        lines.append(f"\n生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"\n项目路径: {self.project_path}")

        lines.append("\n## 执行步骤")
        for i, step in enumerate(self.steps, 1):
            result = self.results.get(step, {})
            status = result.get("status", "unknown")
            icon = "✅" if status == "success" else "❌"
            lines.append(f"\n{icon} **步骤 {i}: {step}**")

        lines.append("\n## 总结")
        lines.append(f"- 总步骤数: {len(self.steps)}")
        lines.append(f"- 成功: {sum(1 for r in self.results.values() if r.get('status') == 'success')}")
        lines.append(f"- 失败: {sum(1 for r in self.results.values() if r.get('status') == 'error')}")

        report = "\n".join(lines)

        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)

            if output_path.suffix == ".html":
                # 转换为 HTML
                html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>优化报告</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #667eea; }}
    </style>
</head>
<body>
{report.replace('#', '').replace('**', '<strong>').replace('**', '</strong>')}
</body>
</html>"""
                output_path.write_text(html, encoding="utf-8")
            else:
                output_path.write_text(report, encoding="utf-8")

            print(f"✅ 报告已保存: {output_path}")

        return report


def main():
    parser = argparse.ArgumentParser(description="一键式 LaTeX 模板优化")
    parser.add_argument("--project", type=Path, required=True, help="项目路径或名称")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互模式")
    parser.add_argument("--report", type=Path, help="生成报告文件")

    args = parser.parse_args()

    raw = str(args.project).strip()
    p = args.project
    if p.exists():
        project_path = p
    else:
        if p.is_absolute() or any(sep in raw for sep in ("/", "\\")):
            candidate = p if p.is_absolute() else (REPO_ROOT / p)
        else:
            candidate = REPO_ROOT / "projects" / raw
        project_path = candidate

    project_path = project_path.resolve()
    if not project_path.exists():
        print(f"❌ 错误: 项目路径不存在: {project_path}")
        raise SystemExit(1)

    try:
        project_path.relative_to(PROJECTS_ROOT)
    except Exception:
        print(f"❌ 错误: 项目必须位于 {PROJECTS_ROOT} 下: {project_path}")
        raise SystemExit(1)

    # 创建优化器
    optimizer = Optimizer(project_path, args.interactive)

    print(f"\n{'='*60}")
    print("  LaTeX 模板一键优化")
    print(f"{'='*60}")
    print(f"\n项目: {project_path}")
    print(f"模式: {'交互式' if args.interactive else '自动'}")

    # 执行优化流程
    analysis = optimizer.run_step("分析 Word PDF 基准", optimizer.analyze_word_pdf)

    headings = optimizer.run_step("提取标题文字", optimizer.extract_headings)

    style_diffs = optimizer.run_step("对比样式参数", optimizer.compare_styles, analysis or {})

    suggestions = optimizer.run_step("生成修改建议",
                                    optimizer.generate_suggestions,
                                    analysis or {},
                                    style_diffs or [])

    optimizer.run_step("应用修改", optimizer.apply_modifications, suggestions or [])

    if optimizer.confirm("是否编译 LaTeX 项目？"):
        optimizer.run_step("编译 LaTeX", optimizer.compile_latex)

    optimizer.run_step("运行验证器", optimizer.run_validators)

    # 生成报告
    optimizer.generate_report(args.report)

    print(f"\n{'='*60}")
    print("  优化完成")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
