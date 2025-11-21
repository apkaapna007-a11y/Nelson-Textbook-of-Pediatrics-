#!/usr/bin/env python3
"""
Run the full pipeline to create a comprehensive Supabase-ready CSV dataset
from part1.txt, part2.txt, and part3.txt.

Steps:
1) Parse raw Nelson text parts into nelson_textbook_perfect.csv
   - Emits paragraphs, bullets, tables, figure captions, and headings.
2) Export normalized Supabase schema into nelson_supabase.csv and nelson_supabase.jsonl

Usage:
    python3 run_supabase_pipeline.py
"""

import sys

def main():
    # Step 1: Generate the perfect CSV from local parts
    from create_nelson_perfect_csv import NelsonTextbookParser
    parser = NelsonTextbookParser()
    parser.generate_csv(
        output_file="nelson_textbook_perfect.csv",
        part1_file="part1.txt",
        part2_file="part2.txt",
        part3_file="part3.txt",
    )
    print("Step 1 complete: nelson_textbook_perfect.csv")

    # Step 2: Export to Supabase schema (CSV + JSONL)
    import supabase_export
    supabase_export.export()
    print("Step 2 complete: nelson_supabase.csv, nelson_supabase.jsonl")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Pipeline error: {e}")
        sys.exit(1)