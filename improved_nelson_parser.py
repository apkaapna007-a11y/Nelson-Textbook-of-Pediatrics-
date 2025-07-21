#!/usr/bin/env python3
"""
Improved script to parse Nelson Textbook of Pediatrics data and prepare it for database insertion.
"""

import re
import json
import uuid
from typing import List, Dict, Tuple, Optional

class ImprovedNelsonParser:
    def __init__(self):
        self.medical_keywords = [
            'infection', 'fever', 'pneumonia', 'asthma', 'diabetes', 'seizure',
            'otitis', 'bronchitis', 'gastroenteritis', 'meningitis', 'sepsis',
            'antibiotic', 'amoxicillin', 'acetaminophen', 'ibuprofen', 'steroid',
            'vaccine', 'immunization', 'growth', 'development', 'nutrition',
            'allergy', 'eczema', 'dermatitis', 'anemia', 'leukemia', 'cancer',
            'heart', 'cardiac', 'murmur', 'hypertension', 'kidney', 'renal',
            'liver', 'hepatic', 'respiratory', 'pulmonary', 'neurologic',
            'pediatric', 'infant', 'child', 'adolescent', 'newborn', 'neonate',
            'treatment', 'diagnosis', 'symptoms', 'syndrome', 'disease',
            'therapy', 'medication', 'dosage', 'clinical', 'pathology'
        ]
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract medical keywords from text."""
        keywords = []
        text_lower = text.lower()
        
        for term in self.medical_keywords:
            if term in text_lower:
                keywords.append(term)
        
        # Extract dosage patterns
        dosage_patterns = [
            r'\d+\s*(?:mg|g|ml|mcg|units?)/kg',
            r'\d+\s*(?:mg|g|ml|mcg|units?)\s*(?:per|/)\s*(?:kg|day)',
            r'\d+\s*(?:mg|g|ml|mcg|units?)\s*(?:daily|bid|tid|qid)'
        ]
        
        for pattern in dosage_patterns:
            matches = re.findall(pattern, text_lower)
            keywords.extend(matches)
        
        return list(set(keywords))
    
    def categorize_content(self, title: str, content: str) -> Tuple[str, str]:
        """Categorize content based on title and content."""
        combined_text = f"{title} {content}".lower()
        
        # Medical categories with more specific patterns
        categories = {
            'Infectious Diseases': ['infection', 'infectious', 'bacteria', 'virus', 'antibiotic', 'sepsis', 'meningitis', 'pneumonia'],
            'Respiratory': ['respiratory', 'asthma', 'lung', 'bronch', 'pulmonary', 'breathing'],
            'Cardiovascular': ['cardiac', 'heart', 'cardiovascular', 'murmur', 'hypertension', 'circulation'],
            'Gastroenterology': ['gastro', 'digestive', 'liver', 'intestinal', 'stomach', 'bowel', 'hepatic'],
            'Neurology': ['neuro', 'seizure', 'brain', 'nervous', 'epilepsy', 'cerebral'],
            'Nephrology/Urology': ['kidney', 'renal', 'urologic', 'urology', 'urinary', 'bladder'],
            'Endocrinology': ['endocrine', 'diabetes', 'hormone', 'thyroid', 'adrenal', 'insulin'],
            'Hematology/Oncology': ['hematology', 'blood', 'anemia', 'leukemia', 'cancer', 'oncology', 'lymphoma'],
            'Dermatology': ['dermatology', 'skin', 'rash', 'eczema', 'dermatitis', 'lesion'],
            'Adolescent Medicine': ['adolescent', 'puberty', 'teenager', 'teen'],
            'Neonatology': ['newborn', 'neonatal', 'neonate', 'birth'],
            'Growth and Development': ['growth', 'development', 'developmental', 'milestone']
        }
        
        for category, terms in categories.items():
            if any(term in combined_text for term in terms):
                return category, self.determine_age_group(combined_text)
        
        return 'General Pediatrics', self.determine_age_group(combined_text)
    
    def determine_age_group(self, text: str) -> str:
        """Determine age group from text content."""
        age_patterns = {
            'Newborn (0-28 days)': ['newborn', 'neonatal', 'neonate', 'birth'],
            'Infant (1-12 months)': ['infant', 'infancy'],
            'Toddler (1-3 years)': ['toddler'],
            'Preschool (3-5 years)': ['preschool'],
            'School Age (5-12 years)': ['school age', 'school-age', 'child'],
            'Adolescent (12-18 years)': ['adolescent', 'teen', 'puberty']
        }
        
        for age_group, terms in age_patterns.items():
            if any(term in text for term in terms):
                return age_group
        
        return 'All Ages'
    
    def split_into_chunks(self, text: str, max_length: int = 2000) -> List[str]:
        """Split long text into manageable chunks."""
        if len(text) <= max_length:
            return [text]
        
        chunks = []
        sentences = re.split(r'(?<=[.!?])\s+', text)
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk + sentence) <= max_length:
                current_chunk += sentence + " "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + " "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def parse_file_content(self, filepath: str) -> List[Dict]:
        """Parse file content into structured records."""
        records = []
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return records
        
        # Find chapter boundaries more flexibly
        lines = content.split('\n')
        current_chapter = None
        current_section = None
        current_content = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Check for chapter headers
            chapter_match = re.match(r'^Chapter\s+(\d+)', line)
            if chapter_match:
                # Save previous content if exists
                if current_chapter and current_content:
                    content_text = ' '.join(current_content).strip()
                    if len(content_text) > 50:  # Only save substantial content
                        chunks = self.split_into_chunks(content_text)
                        for j, chunk in enumerate(chunks):
                            record = self.create_record(
                                current_chapter,
                                current_section or "General",
                                chunk,
                                j + 1 if len(chunks) > 1 else None
                            )
                            records.append(record)
                
                current_chapter = line
                current_section = None
                current_content = []
                continue
            
            # Check for section headers (capitalized lines that aren't too long)
            if (line and line[0].isupper() and len(line) < 100 and 
                not line.endswith('.') and not line.startswith('Chapter')):
                # Save previous section content
                if current_chapter and current_content:
                    content_text = ' '.join(current_content).strip()
                    if len(content_text) > 50:
                        chunks = self.split_into_chunks(content_text)
                        for j, chunk in enumerate(chunks):
                            record = self.create_record(
                                current_chapter,
                                current_section or "General",
                                chunk,
                                j + 1 if len(chunks) > 1 else None
                            )
                            records.append(record)
                
                current_section = line
                current_content = []
                continue
            
            # Add content lines
            if line and current_chapter:
                current_content.append(line)
        
        # Handle final content
        if current_chapter and current_content:
            content_text = ' '.join(current_content).strip()
            if len(content_text) > 50:
                chunks = self.split_into_chunks(content_text)
                for j, chunk in enumerate(chunks):
                    record = self.create_record(
                        current_chapter,
                        current_section or "General",
                        chunk,
                        j + 1 if len(chunks) > 1 else None
                    )
                    records.append(record)
        
        return records
    
    def create_record(self, chapter: str, section: str, content: str, chunk_num: Optional[int] = None) -> Dict:
        """Create a database record from parsed content."""
        # Clean content
        content = re.sub(r'\s+', ' ', content.strip())
        
        # Add chunk number to section if needed
        if chunk_num:
            section = f"{section} (Part {chunk_num})"
        
        # Extract keywords
        keywords = self.extract_keywords(content)
        
        # Categorize content
        category, age_group = self.categorize_content(f"{chapter} {section}", content)
        
        # Extract page number if mentioned
        page_match = re.search(r'(?:page|p\.)\s*(\d+)', content.lower())
        page_number = int(page_match.group(1)) if page_match else None
        
        return {
            'id': str(uuid.uuid4()),
            'chapter': chapter,
            'section': section,
            'page_number': page_number,
            'content': content,
            'keywords': keywords,
            'medical_category': category,
            'age_group': age_group
        }
    
    def parse_all_files(self, file_paths: List[str]) -> List[Dict]:
        """Parse all files and return combined records."""
        all_records = []
        
        for filepath in file_paths:
            print(f"Parsing {filepath}...")
            records = self.parse_file_content(filepath)
            all_records.extend(records)
            print(f"Extracted {len(records)} records from {filepath}")
        
        return all_records
    
    def generate_sql_inserts(self, records: List[Dict], output_file: str):
        """Generate SQL INSERT statements."""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("-- Nelson Textbook of Pediatrics Data Inserts\n")
            f.write("-- Generated automatically from parsed textbook content\n\n")
            
            for record in records:
                # Escape single quotes
                chapter = record['chapter'].replace("'", "''")
                section = record['section'].replace("'", "''")
                content = record['content'].replace("'", "''")
                
                # Format keywords array
                if record['keywords']:
                    keywords_list = [f"'{kw.replace(chr(39), chr(39)+chr(39))}'" for kw in record['keywords']]
                    keywords_str = "ARRAY[" + ",".join(keywords_list) + "]"
                else:
                    keywords_str = "ARRAY[]::TEXT[]"
                
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
        """Generate JSON output."""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(records, f, indent=2, ensure_ascii=False)
    
    def generate_summary_report(self, records: List[Dict], output_file: str):
        """Generate a summary report of the parsed data."""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Nelson Textbook Parsing Summary Report\n\n")
            f.write(f"Total records extracted: {len(records)}\n\n")
            
            # Category distribution
            categories = {}
            age_groups = {}
            chapters = set()
            
            for record in records:
                categories[record['medical_category']] = categories.get(record['medical_category'], 0) + 1
                age_groups[record['age_group']] = age_groups.get(record['age_group'], 0) + 1
                chapters.add(record['chapter'])
            
            f.write(f"## Categories Distribution\n")
            for category, count in sorted(categories.items()):
                f.write(f"- {category}: {count} records\n")
            
            f.write(f"\n## Age Groups Distribution\n")
            for age_group, count in sorted(age_groups.items()):
                f.write(f"- {age_group}: {count} records\n")
            
            f.write(f"\n## Chapters Found\n")
            f.write(f"Total unique chapters: {len(chapters)}\n")
            for chapter in sorted(chapters):
                f.write(f"- {chapter}\n")

def main():
    parser = ImprovedNelsonParser()
    
    file_paths = [
        'part1 (1).txt',
        'part2.txt',
        'part3.txt'
    ]
    
    print("Starting improved parsing of Nelson Textbook files...")
    records = parser.parse_all_files(file_paths)
    
    print(f"\nTotal records extracted: {len(records)}")
    
    # Generate outputs
    print("Generating SQL insert statements...")
    parser.generate_sql_inserts(records, 'nelson_textbook_inserts.sql')
    
    print("Generating JSON output...")
    parser.generate_json_output(records, 'nelson_textbook_data.json')
    
    print("Generating summary report...")
    parser.generate_summary_report(records, 'parsing_summary.md')
    
    # Print sample records
    print("\nSample records:")
    for i, record in enumerate(records[:3]):
        print(f"\nRecord {i+1}:")
        print(f"Chapter: {record['chapter']}")
        print(f"Section: {record['section']}")
        print(f"Category: {record['medical_category']}")
        print(f"Age Group: {record['age_group']}")
        print(f"Keywords: {record['keywords'][:5]}")
        print(f"Content preview: {record['content'][:200]}...")
    
    print(f"\nFiles generated:")
    print(f"- nelson_textbook_inserts.sql ({len(records)} INSERT statements)")
    print(f"- nelson_textbook_data.json (JSON format)")
    print(f"- parsing_summary.md (Summary report)")

if __name__ == "__main__":
    main()

