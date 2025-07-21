#!/usr/bin/env python3
"""
Script to parse Nelson Textbook of Pediatrics data and prepare it for database insertion
according to the provided schema.
"""

import re
import json
import uuid
from typing import List, Dict, Tuple, Optional
import hashlib

class NelsonTextbookParser:
    def __init__(self):
        self.chapters = []
        self.current_chapter = None
        self.current_section = None
        
    def extract_keywords(self, text: str) -> List[str]:
        """Extract medical keywords from text using common pediatric terms."""
        # Common pediatric medical terms to look for
        medical_terms = [
            'infection', 'fever', 'pneumonia', 'asthma', 'diabetes', 'seizure',
            'otitis', 'bronchitis', 'gastroenteritis', 'meningitis', 'sepsis',
            'antibiotic', 'amoxicillin', 'acetaminophen', 'ibuprofen', 'steroid',
            'vaccine', 'immunization', 'growth', 'development', 'nutrition',
            'allergy', 'eczema', 'dermatitis', 'anemia', 'leukemia', 'cancer',
            'heart', 'cardiac', 'murmur', 'hypertension', 'kidney', 'renal',
            'liver', 'hepatic', 'respiratory', 'pulmonary', 'neurologic',
            'pediatric', 'infant', 'child', 'adolescent', 'newborn', 'neonate'
        ]
        
        keywords = []
        text_lower = text.lower()
        
        for term in medical_terms:
            if term in text_lower:
                keywords.append(term)
        
        # Extract dosage patterns
        dosage_pattern = r'\d+\s*(?:mg|g|ml|mcg|units?)/kg'
        dosages = re.findall(dosage_pattern, text_lower)
        keywords.extend(dosages)
        
        return list(set(keywords))  # Remove duplicates
    
    def categorize_content(self, chapter_title: str, section_title: str, content: str) -> Tuple[str, str]:
        """Categorize content based on chapter and section titles."""
        title_combined = f"{chapter_title} {section_title}".lower()
        
        # Medical categories mapping
        if any(term in title_combined for term in ['infection', 'infectious', 'bacteria', 'virus', 'antibiotic']):
            category = 'Infectious Diseases'
        elif any(term in title_combined for term in ['respiratory', 'asthma', 'pneumonia', 'lung']):
            category = 'Respiratory'
        elif any(term in title_combined for term in ['cardiac', 'heart', 'cardiovascular']):
            category = 'Cardiovascular'
        elif any(term in title_combined for term in ['gastro', 'digestive', 'liver', 'intestinal']):
            category = 'Gastroenterology'
        elif any(term in title_combined for term in ['neuro', 'seizure', 'brain', 'development']):
            category = 'Neurology'
        elif any(term in title_combined for term in ['kidney', 'renal', 'urologic', 'urology']):
            category = 'Nephrology/Urology'
        elif any(term in title_combined for term in ['endocrine', 'diabetes', 'hormone', 'growth']):
            category = 'Endocrinology'
        elif any(term in title_combined for term in ['hematology', 'blood', 'anemia', 'leukemia']):
            category = 'Hematology/Oncology'
        elif any(term in title_combined for term in ['dermatology', 'skin', 'rash', 'eczema']):
            category = 'Dermatology'
        elif any(term in title_combined for term in ['adolescent', 'puberty']):
            category = 'Adolescent Medicine'
        elif any(term in title_combined for term in ['newborn', 'neonatal', 'infant']):
            category = 'Neonatology'
        else:
            category = 'General Pediatrics'
        
        # Age group determination
        if any(term in title_combined for term in ['newborn', 'neonatal', 'neonate']):
            age_group = 'Newborn (0-28 days)'
        elif any(term in title_combined for term in ['infant']):
            age_group = 'Infant (1-12 months)'
        elif any(term in title_combined for term in ['toddler']):
            age_group = 'Toddler (1-3 years)'
        elif any(term in title_combined for term in ['preschool']):
            age_group = 'Preschool (3-5 years)'
        elif any(term in title_combined for term in ['school', 'child']):
            age_group = 'School Age (5-12 years)'
        elif any(term in title_combined for term in ['adolescent', 'teen']):
            age_group = 'Adolescent (12-18 years)'
        else:
            age_group = 'All Ages'
        
        return category, age_group
    
    def extract_page_number(self, text: str) -> Optional[int]:
        """Extract page number from text if available."""
        # Look for page number patterns
        page_pattern = r'(?:page|p\.)\s*(\d+)'
        match = re.search(page_pattern, text.lower())
        if match:
            return int(match.group(1))
        return None
    
    def parse_file(self, filepath: str) -> List[Dict]:
        """Parse a single Nelson textbook file."""
        records = []
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return records
        
        # Split content into chapters
        chapter_pattern = r'^Chapter\s+(\d+)\s*\n\n(.+?)(?=\n\n|\n[A-Z]|\Z)'
        chapters = re.findall(chapter_pattern, content, re.MULTILINE | re.DOTALL)
        
        for chapter_num, chapter_content in chapters:
            chapter_title = f"Chapter {chapter_num}"
            
            # Split chapter into sections (look for titles in title case)
            section_pattern = r'\n([A-Z][A-Za-z\s,]+)\n([^A-Z\n].+?)(?=\n[A-Z][A-Za-z\s,]+\n|\Z)'
            sections = re.findall(section_pattern, chapter_content, re.DOTALL)
            
            if not sections:
                # If no clear sections, treat entire chapter as one section
                sections = [("General", chapter_content)]
            
            for section_title, section_content in sections:
                # Clean up content
                section_content = re.sub(r'\n+', ' ', section_content.strip())
                section_content = re.sub(r'\s+', ' ', section_content)
                
                # Skip very short sections (likely headers or incomplete)
                if len(section_content) < 100:
                    continue
                
                # Extract keywords
                keywords = self.extract_keywords(section_content)
                
                # Categorize content
                category, age_group = self.categorize_content(chapter_title, section_title, section_content)
                
                # Extract page number (if available)
                page_number = self.extract_page_number(section_content)
                
                # Create record
                record = {
                    'id': str(uuid.uuid4()),
                    'chapter': chapter_title,
                    'section': section_title.strip(),
                    'page_number': page_number,
                    'content': section_content,
                    'keywords': keywords,
                    'medical_category': category,
                    'age_group': age_group
                }
                
                records.append(record)
        
        return records
    
    def parse_all_files(self, file_paths: List[str]) -> List[Dict]:
        """Parse all Nelson textbook files."""
        all_records = []
        
        for filepath in file_paths:
            print(f"Parsing {filepath}...")
            records = self.parse_file(filepath)
            all_records.extend(records)
            print(f"Extracted {len(records)} records from {filepath}")
        
        return all_records
    
    def generate_sql_inserts(self, records: List[Dict], output_file: str):
        """Generate SQL INSERT statements for the records."""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("-- Nelson Textbook of Pediatrics Data Inserts\n")
            f.write("-- Generated automatically from parsed textbook content\n\n")
            
            for record in records:
                # Escape single quotes in text
                chapter = record['chapter'].replace("'", "''")
                section = record['section'].replace("'", "''")
                content = record['content'].replace("'", "''")
                
                # Format keywords array
                keywords_str = "ARRAY[" + ",".join([f"'{kw.replace(chr(39), chr(39)+chr(39))}'" for kw in record['keywords']]) + "]"
                
                sql = f"""INSERT INTO nelson_textbook (id, chapter, section, page_number, content, keywords, medical_category, age_group) VALUES (
    '{record['id']}',
    '{chapter}',
    '{section}',
    {record['page_number'] if record['page_number'] else 'NULL'},
    '{content}',
    {keywords_str},
    '{record['medical_category']}',
    '{record['age_group']}'
);

"""
                f.write(sql)
    
    def generate_json_output(self, records: List[Dict], output_file: str):
        """Generate JSON output for the records."""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(records, f, indent=2, ensure_ascii=False)

def main():
    parser = NelsonTextbookParser()
    
    # File paths
    file_paths = [
        'part1 (1).txt',
        'part2.txt',
        'part3.txt'
    ]
    
    # Parse all files
    print("Starting to parse Nelson Textbook files...")
    records = parser.parse_all_files(file_paths)
    
    print(f"\nTotal records extracted: {len(records)}")
    
    # Generate outputs
    print("Generating SQL insert statements...")
    parser.generate_sql_inserts(records, 'nelson_textbook_inserts.sql')
    
    print("Generating JSON output...")
    parser.generate_json_output(records, 'nelson_textbook_data.json')
    
    # Print sample records
    print("\nSample records:")
    for i, record in enumerate(records[:3]):
        print(f"\nRecord {i+1}:")
        print(f"Chapter: {record['chapter']}")
        print(f"Section: {record['section']}")
        print(f"Category: {record['medical_category']}")
        print(f"Age Group: {record['age_group']}")
        print(f"Keywords: {record['keywords'][:5]}...")  # Show first 5 keywords
        print(f"Content preview: {record['content'][:200]}...")
    
    print(f"\nFiles generated:")
    print(f"- nelson_textbook_inserts.sql (SQL INSERT statements)")
    print(f"- nelson_textbook_data.json (JSON format)")

if __name__ == "__main__":
    main()
