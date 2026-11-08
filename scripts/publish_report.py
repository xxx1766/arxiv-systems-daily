#!/usr/bin/env python3
"""
Publish daily report to GitHub repository:
- Saves report into docs/<YYYY-MM-DD>.md
- Updates README.md latest report & archive table with bullet list highlights
- Git commits and pushes to origin main
"""

import sys
import os
import re
import subprocess
from datetime import datetime

REPO_DIR = "/Users/xqr/.gemini/antigravity/scratch/arxiv-systems-daily"

def parse_report_highlights(report_content):
    """
    Extracts paper count and list of must-read highlights from the report.
    """
    if "arXiv 无新增论文" in report_content:
        return "0", []

    count_match = re.search(r'入选深读[*：:\s]*(\d+)\s*篇', report_content)
    paper_count = count_match.group(1) if count_match else "多"

    must_reads = []
    must_read_match = re.search(r'今日必读[^\n]*\n(.*?)(?=\n---|###|\Z)', report_content, re.DOTALL)
    if must_read_match:
        raw_items = re.findall(r'^\s*\d+\.\s*(.*?)$', must_read_match.group(1), re.MULTILINE)
        for it in raw_items:
            m = re.search(r'\*\*(.*?)\*\*[：:]\s*(.*)', it)
            if m:
                full_title, summary = m.group(1).strip(), m.group(2).strip()
                short_title = full_title.split(':')[0].strip() if ':' in full_title else full_title
                must_reads.append({"title": short_title, "summary": summary})
            else:
                clean_text = re.sub(r'^\d+\.\s*', '', it).strip()
                must_reads.append({"title": "精选论文", "summary": clean_text})

    return paper_count, must_reads

def main():
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: publish_report.py <YYYY-MM-DD> <report_content_file>\n")
        sys.exit(1)

    date_str = sys.argv[1]
    report_file = sys.argv[2]

    if not os.path.exists(report_file):
        sys.stderr.write(f"Report file {report_file} does not exist.\n")
        sys.exit(1)

    with open(report_file, "r", encoding="utf-8") as f:
        report_content = f.read()

    docs_dir = os.path.join(REPO_DIR, "docs")
    os.makedirs(docs_dir, exist_ok=True)
    doc_path = os.path.join(docs_dir, f"{date_str}.md")

    with open(doc_path, "w", encoding="utf-8") as f:
        f.write(report_content)

    paper_count, must_reads = parse_report_highlights(report_content)

    # Format table summary with unordered bullet points (<br>• <b>Title</b>: summary)
    if must_reads:
        table_summary = "<br>".join([f"• <b>{item['title']}</b>: {item['summary']}" for item in must_reads])
        latest_summary = "\n" + "\n".join([f"  - **{item['title']}**: {item['summary']}" for item in must_reads])
    elif "arXiv 无新增论文" in report_content:
        table_summary = "周末 / 节假日 arXiv 无新增论文"
        latest_summary = " 周末 / 节假日 arXiv 无新增论文"
    else:
        table_summary = "系统方向前沿文献深度解读"
        latest_summary = " 系统方向前沿文献深度解读"

    readme_path = os.path.join(REPO_DIR, "README.md")
    
    # Read existing history rows from README if present
    existing_rows = []
    old_readme = ""
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            old_readme = f.read()
            rows = re.findall(r'(\| \*\*\d{4}-\d{2}-\d{2}\*\* \|.*?\n)', old_readme)
            seen_dates = {date_str}
            for r in rows:
                d_match = re.search(r'\*\*(\d{4}-\d{2}-\d{2})\*\*', r)
                if d_match and d_match.group(1) not in seen_dates:
                    seen_dates.add(d_match.group(1))
                    existing_rows.append(r)

    # Generate current row
    new_row = f"| **{date_str}** | {paper_count} 篇 | {table_summary} | [查看全文](docs/{date_str}.md) |\n"

    all_rows = [new_row] + existing_rows
    def extract_date(row):
        m = re.search(r'\*\*(\d{4}-\d{2}-\d{2})\*\*', row)
        return m.group(1) if m else "1970-01-01"
    all_rows.sort(key=extract_date, reverse=True)

    max_existing_date = max([extract_date(r) for r in existing_rows], default="1970-01-01")
    latest_block_match = re.search(r'(## 📌 最新日报\s*\n.*?\n)(?=## 📅 历史归档)', old_readme, re.DOTALL)
    if date_str >= max_existing_date or not latest_block_match:
        latest_section = f"""## 📌 最新日报
- **[{date_str} 日报](docs/{date_str}.md)**（入选 {paper_count} 篇）：{latest_summary}
"""
    else:
        latest_section = latest_block_match.group(1).rstrip() + "\n"

    readme_content = f"""# arXiv Systems Daily Digest 🚀

每日自动追踪并深度解读系统方向与 AI Infra 领域的最新 arXiv 论文。

读者定位为从事「容器架构与运行时、Kubernetes 编排、AI 基础设施（分布式训练/推理/GPU集群）」的工程师与研究者。

{latest_section}
## 📅 历史归档
| 日期 | 入选篇数 | 重点内容提要 | 报告链接 |
| :--- | :---: | :--- | :--- |
{''.join(all_rows)}---
*由 Google Antigravity 定时自动化流水线每日早晨自动分析并生成推送。*
"""

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)

    # Git operations
    subprocess.run(["git", "-C", REPO_DIR, "add", "."], check=True)
    subprocess.run(["git", "-C", REPO_DIR, "commit", "-m", f"docs: update README with bullet highlights for {date_str}"], check=False)
    subprocess.run(["git", "-C", REPO_DIR, "push", "origin", "main"], check=True)
    print(f"Successfully published and pushed {date_str} to GitHub repository {REPO_DIR}!")

if __name__ == "__main__":
    main()
