#!/usr/bin/env python3
"""
Nelson Textbook CSV Dataset Optimizer
Removes duplicates and creates the absolute perfect dataset for RAG pipeline.
"""

import csv
import hashlib
from collections import defaultdict

def optimize_csv_dataset(input_file: str, output_file: str):
    """Remove duplicates and optimize for RAG pipeline."""
    print("=" * 60)
    print("NELSON TEXTBOOK CSV DATASET OPTIMIZER")
    print("=" * 60)
    
    seen_hashes = set()
    unique_records = []
    duplicates_removed = 0
    total_processed = 0
    
    print(f"Reading from: {input_file}")
    print("Detecting and removing duplicates...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            total_processed += 1
            
            # Create hash of the text content for duplicate detection
            text_content = row['text'].strip()
            if not text_content:
                continue  # Skip empty text
                
            # Create a more sophisticated hash including context
            hash_content = f"{row['chapter_number']}|{row['section_title']}|{text_content}"
            content_hash = hashlib.md5(hash_content.encode('utf-8')).hexdigest()
            
            if content_hash not in seen_hashes:
                seen_hashes.add(content_hash)
                unique_records.append(row)
            else:
                duplicates_removed += 1
                
            if total_processed % 5000 == 0:
                print(f"Processed {total_processed:,} records...")
    
    print(f"\n📊 OPTIMIZATION RESULTS")
    print(f"{'='*40}")
    print(f"Total Records Processed: {total_processed:,}")
    print(f"Duplicates Removed: {duplicates_removed:,}")
    print(f"Unique Records Retained: {len(unique_records):,}")
    print(f"Deduplication Rate: {(duplicates_removed/total_processed)*100:.1f}%")
    
    # Write optimized dataset
    print(f"\nWriting optimized dataset to: {output_file}")
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        if unique_records:
            fieldnames = unique_records[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
            writer.writeheader()
            
            for record in unique_records:
                # Additional quality improvements
                cleaned_record = {}
                for key, value in record.items():
                    # Clean up text content
                    if key == 'text':
                        # Remove multiple spaces, clean up formatting
                        cleaned_text = ' '.join(value.split())
                        cleaned_record[key] = cleaned_text
                    else:
                        cleaned_record[key] = value.strip() if value else ''
                
                writer.writerow(cleaned_record)
    
    print(f"✅ Optimized dataset created: {output_file}")
    print(f"✅ {len(unique_records):,} unique, high-quality records")
    print(f"✅ 100% ready for RAG pipeline")
    
    return len(unique_records)


if __name__ == "__main__":
    input_file = "/tmp/apkaapna007-a11y/Nelson-Textbook-of-Pediatrics-/nelson_textbook_perfect.csv"
    output_file = "/tmp/apkaapna007-a11y/Nelson-Textbook-of-Pediatrics-/nelson_textbook_perfect_optimized.csv"
    
    final_count = optimize_csv_dataset(input_file, output_file)
    print(f"\nOptimization complete. Final dataset: {final_count:,} records")