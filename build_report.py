#!/usr/bin/env python3
import json
import os

candidates_file = "/Users/xqr/.gemini/antigravity/scratch/arxiv-systems-daily/candidates.json"
today_report_file = "/Users/xqr/.gemini/antigravity/scratch/arxiv-systems-daily/today_report.md"

with open(candidates_file, "r", encoding="utf-8") as f:
    papers = json.load(f)

paper_map = {p["id"]: p for p in papers}

# The 12 top papers
top_12_ids = [
    "2611.16180", "2611.14904", "2611.15951", "2611.16661", "2611.16219",
    "2611.15130", "2611.16248", "2611.16467", "2611.14848", "2611.15126",
    "2611.17294", "2611.17206"
]

other_ids = [p["id"] for p in papers if p["id"] not in top_12_ids]

print(f"Top 12: {len(top_12_ids)}, Others: {len(other_ids)}, Total: {len(papers)}")
