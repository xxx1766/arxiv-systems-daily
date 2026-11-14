import json
import os
import re

candidates_file = "/Users/xqr/.gemini/antigravity/scratch/arxiv-systems-daily/candidates.json"
today_report_file = "/Users/xqr/.gemini/antigravity/scratch/arxiv-systems-daily/today_report.md"

with open(candidates_file, "r", encoding="utf-8") as f:
    papers = json.load(f)

print(f"Total candidates: {len(papers)}")
