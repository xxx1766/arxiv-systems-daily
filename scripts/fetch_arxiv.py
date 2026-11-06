#!/usr/bin/env python3
"""
Fetch and parse arXiv new submissions and cross-lists for cs.DC, cs.OS, cs.PF,
plus keyword fallback from cs/new.

Optimizations:
- Supports direct file output argument (no shell redirection `>` needed).
- Defaults to scratch workspace: /Users/xqr/.gemini/antigravity/scratch/arxiv-systems-daily/candidates.json
- Includes staleness/duplicate detection against previous candidate snapshot.
- Robust timeout and retry handling.
"""

import sys
import os
import re
import json
import time
import urllib.request
import urllib.error
from datetime import datetime

DEFAULT_OUTPUT_PATH = "/Users/xqr/.gemini/antigravity/scratch/arxiv-systems-daily/candidates.json"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

KEYWORDS = [
    "kubernetes", "container", "serverless", "scheduling", "cluster",
    "gpu", "accelerator", "llm serving", "inference system", "kv cache",
    "distributed training", "collective communication", "rdma", "checkpoint",
    "ebpf", "sandbox", "mlsys", "ai infrastructure"
]

def fetch_url(url, timeout=15, retries=3):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(1.0)
                continue
            sys.stderr.write(f"Error fetching {url}: {e}\n")
            return ""

def parse_listing(html):
    """
    Parses an arXiv /list/<cat>/new page.
    Only takes 'New submissions' and 'Cross submissions'.
    Ignores 'Replacement submissions'.
    Returns list of dicts: {id, title, authors, subjects, is_cross, abstract}
    """
    papers = []
    sections = re.split(r'<h3>(New submissions|Cross submissions|Replacement submissions)[^<]*</h3>', html)
    for i in range(1, len(sections), 2):
        sec_name = sections[i]
        sec_html = sections[i+1]
        if "Replacement" in sec_name:
            continue
        is_cross = ("Cross" in sec_name)
        
        dt_dd_pairs = re.findall(r'<dt>(.*?)</dt>\s*<dd>(.*?)</dd>', sec_html, re.DOTALL)
        for dt, dd in dt_dd_pairs:
            id_match = re.search(r'href\s*=\s*"/abs/([^"]+)"', dt)
            if not id_match:
                continue
            arxiv_id = id_match.group(1).strip()
            
            title_match = re.search(r'<div class=[\'"]list-title mathjax[\'"]>\s*<span class=[\'"]descriptor[\'"]>Title:</span>\s*(.*?)\s*</div>', dd, re.DOTALL)
            title = ""
            if title_match:
                title = re.sub(r'\s+', ' ', title_match.group(1)).strip()
                title = title.replace("\n", " ").strip()
            
            authors_match = re.search(r'<div class=[\'"]list-authors[\'"]>(.*?)</div>', dd, re.DOTALL)
            authors = []
            if authors_match:
                author_names = re.findall(r'<a[^>]*>([^<]+)</a>', authors_match.group(1))
                authors = [a.strip() for a in author_names if a.strip()]
            
            subj_match = re.search(r'<div class=[\'"]list-subjects[\'"]>\s*<span class=[\'"]descriptor[\'"]>Subjects:</span>\s*(.*?)\s*</div>', dd, re.DOTALL)
            subjects = ""
            if subj_match:
                subjects = re.sub(r'<[^>]+>', '', subj_match.group(1)).strip()
                subjects = re.sub(r'\s+', ' ', subjects)
            
            papers.append({
                "id": arxiv_id,
                "title": title,
                "authors": authors,
                "subjects": subjects,
                "is_cross": is_cross,
                "section": sec_name
            })
            
    return papers

def fetch_abstract_and_affiliations(arxiv_id):
    """
    Fetches abstract page https://arxiv.org/abs/{id} and HTML page if needed.
    """
    abs_url = f"https://arxiv.org/abs/{arxiv_id}"
    html = fetch_url(abs_url, timeout=10, retries=3)
    
    abstract = ""
    abs_match = re.search(r'<blockquote class=[\'"]abstract mathjax[\'"]>\s*<span class=[\'"]descriptor[\'"]>Abstract:</span>\s*(.*?)\s*</blockquote>', html, re.DOTALL)
    if abs_match:
        abstract = re.sub(r'\s+', ' ', abs_match.group(1)).strip()
    
    affiliations = []
    html_url = f"https://arxiv.org/html/{arxiv_id}"
    full_html = fetch_url(html_url, timeout=3, retries=1)
    if full_html:
        affil_matches = re.findall(r'<span class=[\'"]ltx_institution[\'"]>([^<]+)</span>', full_html)
        if not affil_matches:
            affil_matches = re.findall(r'<div class=[\'"]ltx_institution[\'"]>([^<]+)</div>', full_html)
        if not affil_matches:
            affil_matches = re.findall(r'<span class=[\'"]ltx_affil[\'"]>([^<]+)</span>', full_html)
        if affil_matches:
            seen_affil = set()
            for af in affil_matches:
                clean_af = af.strip()
                if clean_af and clean_af not in seen_affil:
                    seen_affil.add(clean_af)
                    affiliations.append(clean_af)
                    
    time.sleep(0.2)
    return abstract, affiliations

def main():
    output_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_OUTPUT_PATH

    categories = ["cs.DC", "cs.OS", "cs.PF"]
    candidates = {} # arxiv_id -> paper_dict
    
    # Step 1: Collect from primary categories
    for cat in categories:
        url = f"https://arxiv.org/list/{cat}/new"
        html = fetch_url(url)
        papers = parse_listing(html)
        sys.stderr.write(f"Fetched {len(papers)} papers from {cat}\n")
        for p in papers:
            p_id = p["id"]
            if p_id not in candidates:
                p["source_categories"] = [cat]
                candidates[p_id] = p
            else:
                if cat not in candidates[p_id]["source_categories"]:
                    candidates[p_id]["source_categories"].append(cat)
                    
    # Step 1.2: Keyword fallback in cs/new
    cs_url = "https://arxiv.org/list/cs/new"
    cs_html = fetch_url(cs_url)
    cs_papers = parse_listing(cs_html)
    sys.stderr.write(f"Fetched {len(cs_papers)} total papers from cs/new for fallback\n")
    
    fallback_count = 0
    for p in cs_papers:
        p_id = p["id"]
        if p_id in candidates:
            continue
        
        title_lower = p["title"].lower()
        if any(kw in title_lower for kw in KEYWORDS):
            p["source_categories"] = ["keyword_fallback"]
            candidates[p_id] = p
            fallback_count += 1
            
    sys.stderr.write(f"Added {fallback_count} papers from keyword fallback\n")
    sys.stderr.write(f"Total unique candidates: {len(candidates)}\n")
    
    # Step 2: Check for duplicate / staleness against previous run
    new_ids = set(candidates.keys())
    if os.path.exists(output_path):
        try:
            with open(output_path, "r", encoding="utf-8") as prev_f:
                old_data = json.load(prev_f)
                if isinstance(old_data, list):
                    old_ids = {item.get("id") for item in old_data if "id" in item}
                    if old_ids and new_ids == old_ids:
                        sys.stderr.write("\n⚠️ WARNING: New candidate IDs are 100% IDENTICAL to previous candidates.json snapshot!\n")
                        sys.stderr.write("arXiv may not have refreshed today's listing yet, or today is a non-publishing weekend day.\n\n")
        except Exception as e:
            sys.stderr.write(f"Note: Could not compare with existing file: {e}\n")

    # Step 3: Fetch abstracts for all candidates
    candidate_list = list(candidates.values())
    for idx, p in enumerate(candidate_list):
        sys.stderr.write(f"Fetching abstract [{idx+1}/{len(candidate_list)}]: {p['id']}...\n")
        abstract, affils = fetch_abstract_and_affiliations(p["id"])
        p["abstract"] = abstract
        p["affiliations"] = affils
        
    # Step 4: Write directly to output_path
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(candidate_list, f, ensure_ascii=False, indent=2)
    
    sys.stderr.write(f"✅ Successfully wrote {len(candidate_list)} candidates directly to {output_path}\n")

if __name__ == "__main__":
    main()
