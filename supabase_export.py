#!/usr/bin/env python3
"""
Supabase-ready Nelson dataset exporter.

Transforms the existing nelson_textbook_perfect.csv (or the optimized variant)
into the exact normalized schema required for Supabase ingestion.

Output formats:
- CSV: nelson_supabase.csv
- JSONL: nelson_supabase.jsonl

Target schema (per row):
- book_title -> “Nelson Textbook of Pediatrics”
- book_edition
- book_year
- chapter_number
- chapter_title
- section_title (optional)
- block_type -> paragraph | bullet | heading | table | figure_caption
- block_text -> exact text from the book
- page_number (optional, prefers page_start if available, otherwise page_end)
"""

import csv
import json
import sys
from pathlib import Path

SOURCE_PRIORITY = [
    "nelson_textbook_perfect_optimized.csv",
    "nelson_textbook_perfect.csv",
]

CSV_OUTPUT = "nelson_supabase.csv"
JSONL_OUTPUT = "nelson_supabase.jsonl"

TARGET_FIELDS = [
    "book_title",
    "book_edition",
    "book_year",
    "chapter_number",
    "chapter_title",
    "section_title",
    "block_type",
    "block_text",
    "page_number",
]

def find_source_csv() -> Path:
    for name in SOURCE_PRIORITY:
        p = Path(name)
        if p.exists() and p.stat().st_size > 0:
            return p
    raise FileNotFoundError("No source CSV found. Expected one of: "
                            + ", ".join(SOURCE_PRIORITY))

def normalize_row(src: dict) -> dict:
    # Preserve exact medical text
    text = (src.get("text", "") or "").strip()

    # Prefer page_start; if empty, fall back to page_end
    page_start = (src.get("page_start", "") or "").strip()
    page_end = (src.get("page_end", "") or "").strip()
    page_number = page_start if page_start else page_end

    # Map block_type directly, but ensure only allowed values
    allowed_types = {"paragraph", "bullet", "heading", "table", "figure_caption"}
    block_type = (src.get("block_type", "") or "").strip()
    if block_type not in allowed_types:
        # Do not infer; keep as-is if present, else default to paragraph
        block_type = block_type if block_type else "paragraph"

    out = {
        "book_title": (src.get("book_title", "") or "").strip() or "Nelson Textbook of Pediatrics",
        "book_edition": (src.get("book_edition", "") or "").strip(),
        "book_year": (src.get("book_year", "") or "").strip(),
        "chapter_number": (src.get("chapter_number", "") or "").strip(),
        "chapter_title": (src.get("chapter_title", "") or "").strip(),
        "section_title": (src.get("section_title", "") or "").strip(),
        "block_type": block_type,
        "block_text": text,
        "page_number": page_number,
    }
    return out

def validate_row(row: dict, idx: int):
    # Minimal validation per user requirements
    if not row["chapter_number"]:
        raise ValueError(f"Row {idx}: missing chapter_number")
    if not row["block_type"]:
        raise ValueError(f"Row {idx}: missing block_type")
    if not row["block_text"]:
        raise ValueError(f"Row {idx}: empty block_text")

def export():
    src_path = find_source_csv()
    print(f"Reading source: {src_path}")

    # Read source CSV
    with src_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"Rows loaded: {len(rows):,}")

    # Transform
    transformed = []
    for i, r in enumerate(rows, 1):
        out = normalize_row(r)
        validate_row(out, i)
        transformed.append(out)

    print(f"Transformed rows: {len(transformed):,}")

    # Write CSV
    with open(CSV_OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=TARGET_FIELDS, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for row in transformed:
            writer.writerow(row)
    print(f"Wrote CSV: {CSV_OUTPUT}")

    # Write JSONL
    with open(JSONL_OUTPUT, "w", encoding="utf-8") as f:
        for row in transformed:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"Wrote JSONL: {JSONL_OUTPUT}")

    # Summary
    print("Export complete.")
    print(f"- CSV: {CSV_OUTPUT}")
    print(f"- JSONL: {JSONL_OUTPUT}")

if __name__ == "__main__":
    try:
        export()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)