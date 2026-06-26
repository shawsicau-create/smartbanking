#!/usr/bin/env python3
"""
将 dist/ 整个静态网站打包成单个 HTML 文件
- 内联所有 CSS
- 内联所有 JS
- 多页面以折叠 section 形式合并
"""
import os
import re
import base64
from pathlib import Path

DIST = Path(
    "/Users/xiaoshiishun/微云同步助手(275531137)/qoder工作目录。cnb代码/smartbanking/webversion/dist")
OUTPUT = Path(
    "/Users/xiaoshiishun/微云同步助手(275531137)/qoder工作目录。cnb代码/smartbanking/webversion/bundle.html")

# 1. 读取所有 CSS 文件并合并


def collect_css():
    css = []
    astro_dir = DIST / "_astro"
    if astro_dir.exists():
        for f in astro_dir.glob("*.css"):
            css.append(f"/* {f.name} */\n{f.read_text(encoding='utf-8')}")
    return "\n".join(css)

# 2. 读取所有 JS 文件


def collect_js():
    js = []
    astro_dir = DIST / "_astro"
    if astro_dir.exists():
        for f in astro_dir.glob("*.js"):
            js.append(f"/* {f.name} */\n{f.read_text(encoding='utf-8')}")
    return "\n".join(js)

# 3. 收集所有 HTML 页面


def collect_pages():
    pages = []
    # 找到所有 index.html
    for html_file in sorted(DIST.rglob("index.html")):
        rel = html_file.relative_to(DIST)
        if rel.parts[0] in ("pagefind", "_astro"):
            continue
        path = "/" + str(rel.parent).replace("\\",
                                             "/") if rel.parent != Path(".") else "/"
        title = html_file.stem if html_file.name == "index.html" else html_file.parent.name
        if html_file.parent == DIST:
            title = "首页"
        content = html_file.read_text(encoding="utf-8")
        # 提取 body 内容
        body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL)
        body = body_match.group(1) if body_match else content
        pages.append({
            "path": path,
            "title": title,
            "body": body,
        })
    return pages

# 4. 读取 favicon 并转 base64


def get_favicon():
    favicon = DIST / "favicon.svg"
    if favicon.exists():
        svg = favicon.read_text(encoding="utf-8")
        return f"data:image/svg+xml;base64,{base64.b64encode(svg.encode()).decode()}"
    return ""


def main():
    print("📦 收集 CSS...")
    css = collect_css()
    print(f"   CSS 总大小: {len(css)/1024:.1f} KB")

    print("📜 收集 JS...")
    js = collect_js()
    print(f"   JS 总大小: {len(js)/1024:.1f} KB")

    print("📑 收集页面...")
    pages = collect_pages()
    print(f"   共 {len(pages)} 个页面")

    print("🎨 获取 favicon...")
    favicon = get_favicon()

    # 5. 构建单 HTML
    nav_items = "\n".join([
        f'<li><a href="#page-{i}">{p["title"]}</a></li>'
        for i, p in enumerate(pages)
    ])

    page_sections = "\n".join([
        f'<section id="page-{i}" class="page-section">\n'
        f'  <h2 class="page-title">{p["title"]} <span class="page-path">{p["path"]}</span></h2>\n'
        f'  <div class="page-body">{p["body"]}</div>\n'
        f'</section>'
        for i, p in enumerate(pages)
    ])

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>智慧银行实验教程 - 单页版（EdgeOne MCP 部署演示）</title>
<link rel="icon" href="{favicon}" type="image/svg+xml">
<style>
{css}

/* 单页版特有样式 */
body {{
  margin: 0;
  padding: 0;
  background: var(--sl-color-black, #000);
  color: var(--sl-color-white, #fff);
}}
.bundle-wrapper {{
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem 1rem;
}}
.bundle-header {{
  text-align: center;
  padding: 2rem;
  background: linear-gradient(135deg, #1e3a8a 0%, #7c3aed 100%);
  color: #fff;
  border-radius: 12px;
  margin-bottom: 2rem;
}}
.bundle-header h1 {{
  margin: 0 0 0.5rem;
  font-size: 2.5rem;
}}
.bundle-header p {{
  margin: 0.5rem 0;
  opacity: 0.9;
}}
.bundle-nav {{
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(15, 23, 42, 0.95);
  backdrop-filter: blur(10px);
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}}
.bundle-nav h3 {{
  margin: 0 0 0.5rem;
  color: #93c5fd;
}}
.bundle-nav ul {{
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}}
.bundle-nav li a {{
  display: inline-block;
  padding: 0.4rem 0.8rem;
  background: #1e293b;
  color: #e2e8f0;
  text-decoration: none;
  border-radius: 6px;
  font-size: 0.9rem;
  transition: all 0.2s;
}}
.bundle-nav li a:hover {{
  background: #3b82f6;
  color: #fff;
}}
.page-section {{
  margin: 3rem 0;
  padding: 2rem;
  background: var(--sl-color-gray-6, #1e293b);
  border-radius: 12px;
  border-left: 4px solid #3b82f6;
  scroll-margin-top: 100px;
}}
.page-title {{
  color: #93c5fd;
  margin-top: 0;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #334155;
}}
.page-path {{
  font-size: 0.8rem;
  color: #64748b;
  font-family: monospace;
  margin-left: 0.5rem;
}}
.bundle-footer {{
  text-align: center;
  padding: 2rem;
  color: #64748b;
  font-size: 0.9rem;
}}
@media (max-width: 768px) {{
  .bundle-header h1 {{ font-size: 1.5rem; }}
  .bundle-nav ul {{ flex-direction: column; }}
}}
</style>
</head>
<body>
<div class="bundle-wrapper">
  <header class="bundle-header">
    <h1>📚 智慧银行实验教程</h1>
    <p>单页打包版（EdgeOne MCP 部署演示）</p>
    <p>包含 {len(pages)} 个页面 · 总大小约 {(len(css)+len(js)+sum(len(p['body']) for p in pages))/1024:.0f} KB</p>
  </header>

  <nav class="bundle-nav">
    <h3>🧭 页面导航（点击跳转）</h3>
    <ul>
      {nav_items}
    </ul>
  </nav>

  <main>
    {page_sections}
  </main>

  <footer class="bundle-footer">
    <p>本页面由 EdgeOne makers-mcp-server 部署</p>
    <p>智慧银行实验教程 © 2026 四川农业大学经济学院</p>
  </footer>
</div>
</body>
</html>"""

    OUTPUT.write_text(html, encoding="utf-8")
    size_mb = OUTPUT.stat().st_size / 1024 / 1024
    print(f"\n✅ 打包完成: {OUTPUT}")
    print(f"   大小: {size_mb:.2f} MB ({OUTPUT.stat().st_size/1024:.0f} KB)")


if __name__ == "__main__":
    main()
