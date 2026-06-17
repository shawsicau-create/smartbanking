"""Literature format parsers - RIS, EndNote, NoteExpress, BibTeX."""

import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from pathlib import Path


@dataclass
class LiteratureItem:
    """Single literature item."""
    title: str = ""
    authors: List[str] = field(default_factory=list)
    year: str = ""
    journal: str = ""
    volume: str = ""
    issue: str = ""
    pages: str = ""
    doi: str = ""
    abstract: str = ""
    keywords: List[str] = field(default_factory=list)
    source: str = ""  # CNKI, Wanfang, etc.
    url: str = ""
    raw_type: str = ""  # Journal Article, etc.

    def to_gb7714(self) -> str:
        """Convert to GB/T 7714-2015 format."""
        authors_str = ", ".join(self.authors[:3])
        if len(self.authors) > 3:
            authors_str += ", 等"

        parts = [authors_str]
        if self.title:
            parts.append(f"{self.title}[J]")
        if self.journal:
            parts.append(self.journal)
        if self.year:
            parts.append(self.year)
        if self.volume:
            vol_str = self.volume
            if self.issue:
                vol_str += f"({self.issue})"
            parts.append(vol_str)
        if self.pages:
            parts.append(f"{self.pages}.")

        return ", ".join(parts)

    def to_apa(self) -> str:
        """Convert to APA format."""
        authors_str = "", "".join(self.authors) if len(self.authors) <= 2 else ", ".join(self.authors[:-1]) + ", & " + self.authors[-1]
        return f"{authors_str} ({self.year}). {self.title}. {self.journal}, {self.volume}({self.issue}), {self.pages}."


class RISParser:
    """Parse RIS format files."""

    TAG_MAP = {
        "TI": "title",
        "T1": "title",
        "AU": "authors",
        "A1": "authors",
        "PY": "year",
        "Y1": "year",
        "JO": "journal",
        "JA": "journal",
        "JF": "journal",
        "T2": "journal",
        "VL": "volume",
        "IS": "issue",
        "SP": "start_page",
        "EP": "end_page",
        "DO": "doi",
        "AB": "abstract",
        "N2": "abstract",
        "KW": "keywords",
        "UR": "url",
        "L2": "url",
        "TY": "raw_type",
        "DB": "source",
    }

    def parse(self, content: str) -> List[LiteratureItem]:
        """Parse RIS content."""
        items = []
        records = content.split("ER  -")

        for record in records:
            record = record.strip()
            if not record:
                continue

            item = LiteratureItem()
            current_tag = None
            current_value = []

            for line in record.split("\n"):
                line = line.strip()
                if not line or line.startswith("<?"):
                    continue

                # Match tag pattern "XX  - value"
                match = re.match(r'^([A-Z][A-Z0-9])\s+-\s+(.*)$', line)
                if match:
                    # Save previous tag
                    if current_tag and current_value:
                        self._set_field(item, current_tag, "\n".join(current_value))

                    current_tag = match.group(1)
                    current_value = [match.group(2)]
                elif current_tag:
                    # Continuation line
                    current_value.append(line)

            # Save last tag
            if current_tag and current_value:
                self._set_field(item, current_tag, "\n".join(current_value))

            if item.title or item.authors:
                items.append(item)

        return items

    def _set_field(self, item: LiteratureItem, tag: str, value: str):
        """Set field based on tag."""
        field_name = self.TAG_MAP.get(tag)
        if not field_name:
            return

        if field_name == "authors":
            item.authors.append(value)
        elif field_name == "keywords":
            item.keywords.extend([k.strip() for k in value.split(";") if k.strip()])
        elif field_name == "start_page":
            item.pages = value
        elif field_name == "end_page" and item.pages:
            item.pages += f"-{value}"
        elif hasattr(item, field_name):
            setattr(item, field_name, value)


class EndNoteParser:
    """Parse EndNote export format."""

    def parse(self, content: str) -> List[LiteratureItem]:
        """Parse EndNote text export."""
        items = []
        # EndNote uses similar format to RIS
        ris_parser = RISParser()
        return ris_parser.parse(content)


class NoteExpressParser:
    """Parse NoteExpress format."""

    def parse(self, content: str) -> List[LiteratureItem]:
        """Parse NoteExpress export."""
        items = []
        # NoteExpress can export as RIS or custom format
        # Try RIS first
        ris_parser = RISParser()
        items = ris_parser.parse(content)

        if items:
            return items

        # Try custom format
        return self._parse_custom(content)

    def _parse_custom(self, content: str) -> List[LiteratureItem]:
        """Parse NoteExpress custom format."""
        items = []
        # NoteExpress custom format uses {Title}, {Author} etc.
        pattern = r'\{Title\}([^\{]*)'

        # Simple line-based parsing
        current = LiteratureItem()
        for line in content.split("\n"):
            line = line.strip()
            if not line:
                if current.title:
                    items.append(current)
                    current = LiteratureItem()
                continue

            if line.startswith("标题:") or line.startswith("Title:"):
                current.title = line.split(":", 1)[1].strip()
            elif line.startswith("作者:") or line.startswith("Author:"):
                authors = line.split(":", 1)[1].strip()
                current.authors = [a.strip() for a in authors.split(";") if a.strip()]
            elif line.startswith("年份:") or line.startswith("Year:"):
                current.year = line.split(":", 1)[1].strip()
            elif line.startswith("期刊:") or line.startswith("Journal:"):
                current.journal = line.split(":", 1)[1].strip()

        if current.title:
            items.append(current)

        return items


class BibTeXParser:
    """Parse BibTeX format."""

    def parse(self, content: str) -> List[LiteratureItem]:
        """Parse BibTeX content."""
        items = []

        # Find all entries
        entries = re.findall(r'@\w+\{([^,]+),([^@]+)\}', content, re.DOTALL)

        for entry_id, entry_content in entries:
            item = LiteratureItem()

            # Parse fields
            fields = re.findall(r'(\w+)\s*=\s*\{([^}]+)\}', entry_content)
            for field_name, value in fields:
                field_lower = field_name.lower()
                if field_lower == "title":
                    item.title = value
                elif field_lower == "author":
                    item.authors = [a.strip() for a in value.split(" and ")]
                elif field_lower == "year":
                    item.year = value
                elif field_lower == "journal":
                    item.journal = value
                elif field_lower == "volume":
                    item.volume = value
                elif field_lower == "number":
                    item.issue = value
                elif field_lower == "pages":
                    item.pages = value
                elif field_lower == "doi":
                    item.doi = value
                elif field_lower == "abstract":
                    item.abstract = value
                elif field_lower == "keywords":
                    item.keywords = [k.strip() for k in value.split(",")]
                elif field_lower == "url":
                    item.url = value

            if item.title:
                items.append(item)

        return items


def parse_file(filepath: str) -> List[LiteratureItem]:
    """Auto-detect format and parse file."""
    path = Path(filepath)
    content = path.read_text(encoding="utf-8", errors="ignore")

    # Detect format by extension and content
    ext = path.suffix.lower()

    if ext == ".ris" or "TY  -" in content[:1000]:
        parser = RISParser()
    elif ext == ".bib" or "@article{" in content[:1000]:
        parser = BibTeXParser()
    elif ext == ".enw" or "%0 " in content[:1000]:
        parser = EndNoteParser()
    else:
        # Try RIS first, then BibTeX
        try:
            parser = RISParser()
            items = parser.parse(content)
            if items:
                return items
        except:
            pass
        parser = BibTeXParser()

    return parser.parse(content)
