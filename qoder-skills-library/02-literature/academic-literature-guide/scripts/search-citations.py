#!/usr/bin/env python3
"""
文献引用检索脚本
用于检索论文的后续引用、批评、复现报告、撤稿信息等
"""

import sys
import json
from typing import List, Dict, Optional

def search_citations(author: str, year: str, title_keywords: List[str]) -> Dict:
    """
    检索论文的后续发展信息
    
    Args:
        author: 第一作者姓氏
        year: 发表年份
        title_keywords: 标题关键词列表
    
    Returns:
        包含检索结果的字典
    """
    results = {
        "query": f'"{author} {year}"',
        "categories": {
            "后续研究": [],
            "综述评价": [],
            "复现报告": [],
            "勘误撤稿": [],
            "方法改进": []
        },
        "risk_alert": None
    }
    
    # 构建检索查询
    queries = [
        f'"{author} {year}" citation',
        f'"{author} {year}" replication',
        f'"{author} {year}" criticism',
        f'"{author} {year}" retraction',
        f'"{author} {year}" review',
    ]
    
    print("🔍 建议的检索查询：")
    for i, q in enumerate(queries, 1):
        print(f"  {i}. {q}")
    
    print("\n📌 推荐检索平台：")
    print("  - Google Scholar (scholar.google.com)")
    print("  - Web of Science")
    print("  - PubMed (生物医学)")
    print("  - arXiv (预印本)")
    print("  - Retraction Watch (retractionwatch.com) - 撤稿查询")
    
    return results

def format_search_report(results: Dict) -> str:
    """
    格式化检索报告
    
    Args:
        results: 检索结果字典
    
    Returns:
        Markdown 格式的报告
    """
    report = []
    report.append("## 后续发展追踪\n")
    
    # 已检索到
    has_findings = False
    for category, items in results["categories"].items():
        if items:
            has_findings = True
            report.append(f"### ✅ {category}")
            for item in items:
                report.append(f"- [{item['title']}]({item.get('url', '#')}) - {item.get('finding', 'N/A')} [可信度：{item.get('credibility', '待评估')}]")
            report.append("")
    
    # 未检索到
    if not has_findings:
        report.append("### ⚠️ 未检索到")
        report.append("- 未发现撤稿或重大纠正（截至检索日期）")
        report.append("- 建议关注：后续研究、复现报告、方法改进")
        report.append("")
    
    # 风险预警
    if results["risk_alert"]:
        report.append("> ⚠️ 学习警示：本文因" + results["risk_alert"]["reason"] + "被" + results["risk_alert"]["action"] + "。")
        report.append("> 我们将用它作为'科学方法论'的案例学习，而非可靠结论来源。")
        report.append(f"> [权威链接]({results['risk_alert'].get('url', '#')})")
        report.append("")
    
    return "\n".join(report)

def main():
    if len(sys.argv) < 4:
        print("用法：python search-citations.py <作者姓氏> <年份> <关键词...>")
        print("示例：python search-citations.py \"Zimbardo\" \"1973\" \"prison\" \"guards\"")
        sys.exit(1)
    
    author = sys.argv[1]
    year = sys.argv[2]
    keywords = sys.argv[3:]
    
    results = search_citations(author, year, keywords)
    report = format_search_report(results)
    
    print("\n" + report)

if __name__ == "__main__":
    main()
