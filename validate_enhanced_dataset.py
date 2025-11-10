#!/usr/bin/env python3
"""
Validation script for enhanced Nelson dataset.
Checks integrity and quality of generated files.
"""

import json
import csv
import re
from pathlib import Path
from typing import Dict, List

class DatasetValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.stats = {}
    
    def validate_csv(self, filepath: str) -> bool:
        """Validate CSV file structure and data."""
        print(f"\n[CSV] Validating {filepath}...")
        
        if not Path(filepath).exists():
            self.errors.append(f"CSV file not found: {filepath}")
            return False
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                records = list(reader)
            
            if not records:
                self.errors.append("CSV file is empty")
                return False
            
            # Check headers
            required_headers = ['chapter', 'section', 'topic', 'subtopic', 'content_summary', 
                              'page_number', 'category', 'keywords', 'chunk_text']
            reader = csv.DictReader(open(filepath))
            if reader.fieldnames != required_headers:
                self.warnings.append(f"CSV headers mismatch. Expected: {required_headers}, Got: {reader.fieldnames}")
            
            # Validate records
            categories = set()
            topics = set()
            page_numbers = []
            summary_lengths = []
            empty_fields = 0
            
            for i, record in enumerate(records):
                # Check required fields
                for field in required_headers:
                    if field not in record or not record[field].strip():
                        empty_fields += 1
                
                # Collect stats
                categories.add(record.get('category', 'Unknown'))
                topics.add(record.get('topic', 'Unknown'))
                
                try:
                    page_numbers.append(int(record.get('page_number', 0)))
                except ValueError:
                    self.warnings.append(f"Row {i}: Invalid page_number: {record.get('page_number')}")
                
                summary = record.get('content_summary', '')
                if len(summary) > 200:
                    self.warnings.append(f"Row {i}: Summary exceeds 200 chars ({len(summary)})")
                summary_lengths.append(len(summary))
                
                # Check chunk length
                chunk = record.get('chunk_text', '')
                if len(chunk) < 100:
                    self.warnings.append(f"Row {i}: Chunk text very short ({len(chunk)} chars)")
            
            # Store statistics
            self.stats['csv_records'] = len(records)
            self.stats['unique_categories'] = len(categories)
            self.stats['unique_topics'] = len(topics)
            self.stats['empty_fields_count'] = empty_fields
            self.stats['avg_summary_length'] = sum(summary_lengths) / len(summary_lengths) if summary_lengths else 0
            self.stats['page_range'] = (min(page_numbers) if page_numbers else 0, max(page_numbers) if page_numbers else 0)
            
            print(f"  ✓ CSV validation passed: {len(records)} records")
            print(f"    - Categories: {len(categories)}")
            print(f"    - Topics: {len(topics)}")
            print(f"    - Avg summary length: {self.stats['avg_summary_length']:.1f} chars")
            
            return True
        
        except Exception as e:
            self.errors.append(f"CSV validation error: {e}")
            return False
    
    def validate_json(self, filepath: str) -> bool:
        """Validate JSON file structure and embeddings."""
        print(f"\n[JSON] Validating {filepath}...")
        
        if not Path(filepath).exists():
            self.errors.append(f"JSON file not found: {filepath}")
            return False
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not data:
                self.errors.append("JSON file is empty")
                return False
            
            # Validate each record
            embedding_dims = set()
            chunk_tokens = []
            
            for i, record in enumerate(data):
                # Check required fields
                required_fields = ['chapter', 'section', 'topic', 'subtopic', 'content_summary',
                                 'page_number', 'category', 'keywords', 'chunk_text', 'embedding', 'token_count']
                
                for field in required_fields:
                    if field not in record:
                        self.warnings.append(f"Record {i}: Missing field '{field}'")
                
                # Check embedding
                embedding = record.get('embedding', [])
                if not isinstance(embedding, list):
                    self.errors.append(f"Record {i}: Embedding is not a list")
                else:
                    embedding_dims.add(len(embedding))
                    if len(embedding) != 1536:
                        self.errors.append(f"Record {i}: Embedding dimension {len(embedding)} != 1536")
                
                # Check token count
                token_count = record.get('token_count', 0)
                if token_count < 100:
                    self.warnings.append(f"Record {i}: Token count very low ({token_count})")
                chunk_tokens.append(token_count)
            
            # Store statistics
            self.stats['json_records'] = len(data)
            self.stats['embedding_dimensions'] = list(embedding_dims)
            self.stats['token_range'] = (min(chunk_tokens) if chunk_tokens else 0,
                                        max(chunk_tokens) if chunk_tokens else 0)
            self.stats['avg_tokens'] = sum(chunk_tokens) / len(chunk_tokens) if chunk_tokens else 0
            
            print(f"  ✓ JSON validation passed: {len(data)} records")
            print(f"    - Embedding dimensions: {self.stats['embedding_dimensions']}")
            print(f"    - Token range: {self.stats['token_range']}")
            print(f"    - Average tokens: {self.stats['avg_tokens']:.1f}")
            
            return True
        
        except json.JSONDecodeError as e:
            self.errors.append(f"JSON parsing error: {e}")
            return False
        except Exception as e:
            self.errors.append(f"JSON validation error: {e}")
            return False
    
    def validate_sql(self, filepath: str) -> bool:
        """Validate SQL file structure."""
        print(f"\n[SQL] Validating {filepath}...")
        
        if not Path(filepath).exists():
            self.errors.append(f"SQL file not found: {filepath}")
            return False
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Count INSERT statements
            insert_count = len(re.findall(r'INSERT INTO', content, re.IGNORECASE))
            
            # Check for pgvector extension
            if 'CREATE EXTENSION' in content and 'vector' in content:
                print("  ✓ pgvector extension declaration found")
            
            # Check for table creation
            if 'CREATE TABLE' in content:
                print("  ✓ Table creation statement found")
            
            # Check for indices
            index_count = len(re.findall(r'CREATE INDEX', content, re.IGNORECASE))
            print(f"  ✓ {index_count} indices defined")
            
            print(f"  ✓ {insert_count} INSERT statements")
            self.stats['sql_inserts'] = insert_count
            
            return True
        
        except Exception as e:
            self.errors.append(f"SQL validation error: {e}")
            return False
    
    def validate_markdown(self, filepath: str) -> bool:
        """Validate Markdown summary file."""
        print(f"\n[Markdown] Validating {filepath}...")
        
        if not Path(filepath).exists():
            self.errors.append(f"Markdown file not found: {filepath}")
            return False
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not content:
                self.errors.append("Markdown file is empty")
                return False
            
            # Check sections
            sections = ['Overview', 'Token Distribution', 'Category Breakdown', 'Sample Records']
            found_sections = sum(1 for section in sections if section in content)
            
            print(f"  ✓ Found {found_sections}/{len(sections)} expected sections")
            
            return True
        
        except Exception as e:
            self.errors.append(f"Markdown validation error: {e}")
            return False
    
    def print_report(self):
        """Print validation report."""
        print("\n" + "="*60)
        print("ENHANCED DATASET VALIDATION REPORT")
        print("="*60)
        
        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error}")
        else:
            print("\n✓ NO ERRORS FOUND")
        
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings[:10]:  # Show first 10
                print(f"  - {warning}")
            if len(self.warnings) > 10:
                print(f"  ... and {len(self.warnings) - 10} more")
        
        print("\n📊 STATISTICS:")
        for key, value in self.stats.items():
            print(f"  - {key}: {value}")
        
        if not self.errors:
            print("\n✅ VALIDATION PASSED")
        else:
            print(f"\n❌ VALIDATION FAILED ({len(self.errors)} errors)")
        
        print("="*60 + "\n")
        
        return len(self.errors) == 0


def main():
    """Run validation on all enhanced dataset files."""
    validator = DatasetValidator()
    
    base_path = "/project/workspace"
    files = {
        'csv': f"{base_path}/enhanced_nelson_dataset.csv",
        'json': f"{base_path}/enhanced_nelson_data.json",
        'sql': f"{base_path}/enhanced_nelson_inserts.sql",
        'markdown': f"{base_path}/enhanced_dataset_summary.md"
    }
    
    # Validate all files
    results = {}
    for file_type, filepath in files.items():
        if file_type == 'csv':
            results[file_type] = validator.validate_csv(filepath)
        elif file_type == 'json':
            results[file_type] = validator.validate_json(filepath)
        elif file_type == 'sql':
            results[file_type] = validator.validate_sql(filepath)
        elif file_type == 'markdown':
            results[file_type] = validator.validate_markdown(filepath)
    
    # Print report
    passed = validator.print_report()
    
    return 0 if passed else 1


if __name__ == "__main__":
    exit(main())
