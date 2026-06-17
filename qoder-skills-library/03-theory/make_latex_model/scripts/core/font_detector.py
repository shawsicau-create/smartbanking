#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
字体路径自动检测模块
跨平台字体路径检测工具

使用方法:
    from scripts.core.font_detector import FontDetector

    detector = FontDetector()
    font_paths = detector.detect_font("KaiTi")
    print(font_paths)
"""

import platform
import sys
from pathlib import Path
from typing import List, Dict, Optional


class FontDetector:
    """字体检测器 - 跨平台字体路径检测"""

    def __init__(self):
        self.os_type = platform.system()
        self.font_dirs = self._get_system_font_dirs()

    def _get_system_font_dirs(self) -> List[Path]:
        """获取系统字体目录"""
        dirs = []

        if self.os_type == "Darwin":  # macOS
            dirs = [
                Path("/System/Library/Fonts"),
                Path("/Library/Fonts"),
                Path.home() / "Library" / "Fonts",
            ]
        elif self.os_type == "Windows":  # Windows
            dirs = [
                Path("C:/Windows/Fonts"),
                Path.home() / "AppData" / "Local" / "Microsoft" / "Windows" / "Fonts",
            ]
        elif self.os_type == "Linux":  # Linux
            dirs = [
                Path("/usr/share/fonts"),
                Path("/usr/local/share/fonts"),
                Path.home() / ".local" / "share" / "fonts",
                Path.home() / ".fonts",
            ]
        else:
            dirs = []

        # 过滤存在的目录
        return [d for d in dirs if d.exists()]

    def detect_font(self, font_name: str) -> List[Path]:
        """
        检测字体文件路径

        Args:
            font_name: 字体名称（如 "KaiTi", "SimSun", "Times New Roman"）

        Returns:
            字体文件路径列表
        """
        font_files = []

        # 常见字体文件扩展名
        extensions = [".ttf", ".otf", ".ttc", ".dfont"]

        # 在每个字体目录中搜索
        for font_dir in self.font_dirs:
            if not font_dir.exists():
                continue

            # 递归搜索
            for ext in extensions:
                # 精确匹配
                pattern = f"{font_name}*{ext}"
                matches = list(font_dir.glob(pattern))
                font_files.extend(matches)

                # 也搜索子目录
                for subdir in font_dir.iterdir():
                    if subdir.is_dir():
                        matches = list(subdir.glob(pattern))
                        font_files.extend(matches)

        return self._deduplicate_paths(font_files)

    def detect_common_chinese_fonts(self) -> Dict[str, List[Path]]:
        """
        检测常见中文字体

        Returns:
            字体名称到路径的映射
        """
        common_fonts = {
            "KaiTi": [],      # 楷体
            "SimSun": [],     # 宋体
            "SimHei": [],     # 黑体
            "FangSong": [],   # 仿宋
            "Microsoft YaHei": [],  # 微软雅黑
        }

        for font_name in common_fonts.keys():
            common_fonts[font_name] = self.detect_font(font_name)

        return common_fonts

    def detect_common_english_fonts(self) -> Dict[str, List[Path]]:
        """
        检测常见英文字体

        Returns:
            字体名称到路径的映射
        """
        common_fonts = {
            "Times New Roman": [],
            "Arial": [],
            "Calibri": [],
            "Georgia": [],
            "Verdana": [],
        }

        for font_name in common_fonts.keys():
            common_fonts[font_name] = self.detect_font(font_name)

        return common_fonts

    def get_font_path_for_latex(self, font_name: str) -> Optional[str]:
        """
        获取适用于 LaTeX 的字体路径

        Args:
            font_name: 字体名称

        Returns:
            LaTeX 格式的字体路径（使用 / 而非 \）
        """
        font_paths = self.detect_font(font_name)

        if not font_paths:
            return None

        # 返回第一个找到的字体
        font_path = font_paths[0]

        # 转换为 POSIX 格式（使用 /）
        if self.os_type == "Windows":
            # Windows: C:\Windows\Fonts -> C:/Windows/Fonts
            return str(font_path).replace("\\", "/")
        else:
            return str(font_path)

    def _deduplicate_paths(self, paths: List[Path]) -> List[Path]:
        """去重路径列表"""
        seen = set()
        unique = []

        for path in paths:
            path_str = str(path.resolve())
            if path_str not in seen:
                seen.add(path_str)
                unique.append(path)

        return unique

    def print_system_info(self):
        """打印系统信息"""
        print(f"操作系统: {self.os_type}")
        print(f"Python 版本: {sys.version.split()[0]}")
        print(f"\n字体目录 ({len(self.font_dirs)}):")
        for i, d in enumerate(self.font_dirs, 1):
            print(f"  {i}. {d}")


def main():
    """命令行接口"""
    import argparse

    parser = argparse.ArgumentParser(description="字体路径检测工具")
    parser.add_argument("--font", type=str, help="检测特定字体")
    parser.add_argument("--chinese", action="store_true", help="检测常见中文字体")
    parser.add_argument("--english", action="store_true", help="检测常见英文字体")
    parser.add_argument("--info", action="store_true", help="显示系统信息")

    args = parser.parse_args()

    detector = FontDetector()

    if args.info:
        detector.print_system_info()

    if args.font:
        print(f"\n检测字体: {args.font}")
        paths = detector.detect_font(args.font)
        if paths:
            print(f"找到 {len(paths)} 个字体文件:")
            for path in paths:
                print(f"  - {path}")
                latex_path = detector.get_font_path_for_latex(args.font)
                if latex_path:
                    print(f"    LaTeX: {latex_path}")
        else:
            print("未找到该字体")

    if args.chinese:
        print("\n检测常见中文字体:")
        chinese_fonts = detector.detect_common_chinese_fonts()
        for name, paths in chinese_fonts.items():
            if paths:
                print(f"  {name}: {len(paths)} 个文件")
                for path in paths[:1]:  # 只显示第一个
                    print(f"    - {path}")

    if args.english:
        print("\n检测常见英文字体:")
        english_fonts = detector.detect_common_english_fonts()
        for name, paths in english_fonts.items():
            if paths:
                print(f"  {name}: {len(paths)} 个文件")
                for path in paths[:1]:  # 只显示第一个
                    print(f"    - {path}")

    if not any([args.font, args.chinese, args.english, args.info]):
        # 默认行为
        detector.print_system_info()
        print("\n💡 使用 --font <名称> 检测特定字体")
        print("💡 使用 --chinese 检测常见中文字体")
        print("💡 使用 --english 检测常见英文字体")


if __name__ == "__main__":
    main()
