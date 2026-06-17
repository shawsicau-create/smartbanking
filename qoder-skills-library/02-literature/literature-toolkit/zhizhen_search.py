"""Superstar (Zhizhen/超星发现) search integration."""

import json
import re
from typing import List, Dict, Optional
from urllib.parse import quote, urlencode
from dataclasses import dataclass, field


@dataclass
class ZhizhenResult:
    """Single search result from Zhizhen."""
    title: str = ""
    authors: List[str] = field(default_factory=list)
    year: str = ""
    journal: str = ""
    source: str = ""  # CNKI, Wanfang, etc.
    database: str = ""
    url: str = ""
    abstract: str = ""
    keywords: List[str] = field(default_factory=list)
    citation_count: str = ""
    download_count: str = ""


class ZhizhenSearcher:
    """Search Superstar Discovery System (超星发现)."""

    BASE_URL = "http://www.zhizhen.com"
    SEARCH_URL = "http://www.zhizhen.com/s"

    # Database codes
    DATABASES = {
        "cnki": "CNKI",      # 中国知网
        "wanfang": "万方",    # 万方数据
        "vip": "维普",        # 维普
        "scopus": "Scopus",
        "wos": "Web of Science",
        "sd": "ScienceDirect",
        "springer": "Springer",
    }

    def __init__(self, institution: str = "sicau"):
        """Initialize with institution code."""
        self.institution = institution
        self.session_cookies = {}

    def build_search_url(
        self,
        query: str,
        database: str = None,
        year_from: int = None,
        year_to: int = None,
        doc_type: str = "journal",  # journal, thesis, book, etc.
        page: int = 1
    ) -> str:
        """Build search URL for manual browser opening."""
        params = {
            "sw": query,
            "pages": page,
        }

        if database and database in self.DATABASES:
            params["database"] = self.DATABASES[database]

        if year_from:
            params["year_from"] = year_from
        if year_to:
            params["year_to"] = year_to

        if doc_type:
            params["type"] = doc_type

        return f"{self.SEARCH_URL}?{urlencode(params)}"

    def search(
        self,
        query: str,
        database: str = None,
        year_from: int = None,
        year_to: int = None,
        limit: int = 50
    ) -> List[ZhizhenResult]:
        """
        Search Zhizhen (requires institutional access).

        Note: This method requires authentication through your institution.
        It returns instructions for manual search if automated access fails.
        """
        url = self.build_search_url(query, database, year_from, year_to)

        # Since Zhizhen requires institutional login, we provide
        # instructions for manual export instead
        return self._manual_search_instructions(query, url)

    def _manual_search_instructions(self, query: str, url: str) -> List[ZhizhenResult]:
        """Provide instructions for manual search."""
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║           超星发现系统 (Zhizhen) 检索指引                      ║
╚══════════════════════════════════════════════════════════════╝

检索词: {query}
检索URL: {url}

使用步骤:
1. 复制上方URL到浏览器打开
2. 使用学校统一身份认证登录 (账号: 学号/工号)
3. 在结果页面选择需要的文献
4. 点击"导出"按钮，选择格式:
   - RIS格式 (推荐，兼容性最好)
   - EndNote格式
   - NoteExpress格式
   - BibTeX格式
5. 保存导出文件
6. 使用 literature-toolkit CLI 处理:

   lit import 导出文件.ris --dedupe --analyze

提示:
- 超星发现整合了知网、万方、维普等多个数据库
- 一次检索可同时获取多个来源的文献
- 支持高级检索: 标题、作者、关键词、机构等

""")
        return []

    def get_export_instructions(self) -> str:
        """Get instructions for exporting from Zhizhen."""
        return """
超星发现系统文献导出步骤:

1. 访问 http://www.zhizhen.com (校园网内或VPN)
2. 检索所需文献
3. 勾选需要的文献 (可多选)
4. 点击"导出"或"批量导出"
5. 选择导出格式:
   ┌─────────────────────────────────────┐
   │  推荐格式: RIS (EndNote compatible)  │
   │  备选格式: EndNote (.enw)            │
   │  备选格式: NoteExpress (.net)        │
   │  备选格式: BibTeX (.bib)             │
   └─────────────────────────────────────┘
6. 保存文件到本地
7. 使用 CLI 工具处理:

   lit import 文件.ris --output report.md

导出字段建议:
☑ 标题 (Title)
☑ 作者 (Author)
☑ 来源 (Journal/Source)
☑ 年份 (Year)
☑ 卷期页 (Volume/Issue/Pages)
☑ DOI
☑ 摘要 (Abstract)
☑ 关键词 (Keywords)
"""


def generate_search_links(keywords: List[str], institution: str = "sicau") -> Dict[str, str]:
    """Generate search links for multiple keywords."""
    searcher = ZhizhenSearcher(institution)

    links = {}
    for kw in keywords:
        links[kw] = searcher.build_search_url(kw)

    return links


def print_search_template(topic: str, keywords: List[str]):
    """Print a search template for a research topic."""
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║  研究主题: {topic[:40]:<40} ║
╚══════════════════════════════════════════════════════════════╝

检索策略:
""")

    searcher = ZhizhenSearcher()

    for i, kw in enumerate(keywords, 1):
        url = searcher.build_search_url(kw)
        print(f"{i}. 关键词: {kw}")
        print(f"   链接: {url}")
        print()

    print("""
建议操作:
1. 依次点击上述链接进行检索
2. 每个关键词保存前50条结果
3. 使用 lit merge 合并所有导出文件
4. 使用 lit analyze 生成分析报告
""")


