"""Literature analysis and deduplication."""

from typing import List, Dict, Set, Tuple
from collections import defaultdict
import re
from difflib import SequenceMatcher

from .parsers import LiteratureItem


class LiteratureAnalyzer:
    """Analyze literature collection."""

    def __init__(self, items: List[LiteratureItem]):
        self.items = items

    def deduplicate(self, threshold: float = 0.85) -> List[LiteratureItem]:
        """Remove duplicate items based on title similarity."""
        unique_items = []
        seen_titles = []

        for item in self.items:
            is_duplicate = False
            normalized_title = self._normalize_title(item.title)

            for seen_title, seen_item in seen_titles:
                similarity = SequenceMatcher(None, normalized_title, seen_title).ratio()
                if similarity >= threshold:
                    is_duplicate = True
                    break

            if not is_duplicate:
                seen_titles.append((normalized_title, item))
                unique_items.append(item)

        return unique_items

    def _normalize_title(self, title: str) -> str:
        """Normalize title for comparison."""
        # Remove punctuation, lowercase
        title = re.sub(r'[^\w\s]', '', title.lower())
        # Remove extra whitespace
        title = ' '.join(title.split())
        return title

    def analyze_sources(self) -> Dict[str, int]:
        """Count items by source database."""
        sources = defaultdict(int)
        for item in self.items:
            source = item.source or "Unknown"
            sources[source] += 1
        return dict(sources)

    def analyze_years(self) -> Dict[str, int]:
        """Count items by year."""
        years = defaultdict(int)
        for item in self.items:
            if item.year:
                years[item.year] += 1
        return dict(sorted(years.items()))

    def analyze_journals(self, top_n: int = 20) -> List[Tuple[str, int]]:
        """Get top journals."""
        journals = defaultdict(int)
        for item in self.items:
            if item.journal:
                journals[item.journal] += 1
        return sorted(journals.items(), key=lambda x: x[1], reverse=True)[:top_n]

    def analyze_keywords(self, top_n: int = 30) -> List[Tuple[str, int]]:
        """Get top keywords."""
        keywords = defaultdict(int)
        for item in self.items:
            for kw in item.keywords:
                # Normalize keyword
                kw = kw.strip().lower()
                if kw and len(kw) > 1:
                    keywords[kw] += 1
        return sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:top_n]

    def analyze_authors(self, top_n: int = 20) -> List[Tuple[str, int]]:
        """Get top authors."""
        authors = defaultdict(int)
        for item in self.items:
            for author in item.authors:
                author = author.strip()
                if author:
                    authors[author] += 1
        return sorted(authors.items(), key=lambda x: x[1], reverse=True)[:top_n]

    def generate_report(self) -> str:
        """Generate analysis report."""
        lines = ["=" * 60, "文献分析报告", "=" * 60, ""]

        lines.append(f"总文献数: {len(self.items)}")

        # Deduplicate
        unique = self.deduplicate()
        if len(unique) < len(self.items):
            lines.append(f"去重后: {len(unique)} (移除 {len(self.items) - len(unique)} 篇重复)")
        lines.append("")

        # Sources
        lines.append("-" * 40)
        lines.append("数据库来源分布:")
        for source, count in self.analyze_sources().items():
            lines.append(f"  {source}: {count}")
        lines.append("")

        # Years
        lines.append("-" * 40)
        lines.append("年份分布:")
        for year, count in self.analyze_years().items():
            lines.append(f"  {year}: {count}")
        lines.append("")

        # Top journals
        lines.append("-" * 40)
        lines.append("主要期刊 (Top 10):")
        for journal, count in self.analyze_journals(10):
            lines.append(f"  {journal}: {count}")
        lines.append("")

        # Top keywords
        lines.append("-" * 40)
        lines.append("高频关键词 (Top 15):")
        for kw, count in self.analyze_keywords(15):
            lines.append(f"  {kw}: {count}")
        lines.append("")

        # Top authors
        lines.append("-" * 40)
        lines.append("高产作者 (Top 10):")
        for author, count in self.analyze_authors(10):
            lines.append(f"  {author}: {count}")
        lines.append("")

        lines.append("=" * 60)
        return "\n".join(lines)

    def export_references(self, style: str = "gb7714") -> str:
        """Export references in specified format."""
        lines = []

        for i, item in enumerate(self.items, 1):
            if style == "gb7714":
                ref = item.to_gb7714()
            elif style == "apa":
                ref = item.to_apa()
            else:
                ref = item.to_gb7714()

            lines.append(f"[{i}] {ref}")

        return "\n".join(lines)

    def filter_by_year(self, start_year: int = None, end_year: int = None) -> List[LiteratureItem]:
        """Filter items by year range."""
        filtered = []
        for item in self.items:
            if not item.year:
                continue
            try:
                year = int(item.year)
                if start_year and year < start_year:
                    continue
                if end_year and year > end_year:
                    continue
                filtered.append(item)
            except ValueError:
                continue
        return filtered

    def filter_by_keyword(self, keywords: List[str]) -> List[LiteratureItem]:
        """Filter items by keywords."""
        filtered = []
        keywords_lower = [k.lower() for k in keywords]

        for item in self.items:
            text = f"{item.title} {' '.join(item.keywords)} {item.abstract}".lower()
            if any(kw in text for kw in keywords_lower):
                filtered.append(item)

        return filtered

    def filter_by_journal(self, journals: List[str]) -> List[LiteratureItem]:
        """Filter items by journal names."""
        filtered = []
        journals_lower = [j.lower() for j in journals]

        for item in self.items:
            if item.journal and any(j in item.journal.lower() for j in journals_lower):
                filtered.append(item)

        return filtered
