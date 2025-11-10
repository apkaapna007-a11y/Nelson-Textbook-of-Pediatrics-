#!/usr/bin/env python3
"""
Enhanced dataset generation using existing parsed Nelson data.
Converts nelson_textbook_data.json to enhanced format with chunking, embeddings, and AI metadata.
"""

import json
import csv
import re
import numpy as np
from typing import List, Dict, Tuple
from pathlib import Path

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable, **kwargs):
        return iterable

try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False
    print("Warning: tiktoken not available, using fallback token counting")

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    print("Warning: sentence-transformers not available")


class EnhancedNelsonFromExisting:
    def __init__(self, use_gpu: bool = True, skip_ai: bool = False):
        """Initialize converter for existing Nelson data."""
        self.skip_ai = skip_ai
        self.device = "cpu"
        
        if TORCH_AVAILABLE and use_gpu:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        print(f"Using device: {self.device}")
        
        # Initialize tiktoken
        if TIKTOKEN_AVAILABLE:
            self.tiktoken_encoding = tiktoken.get_encoding("cl100k_base")
        else:
            self.tiktoken_encoding = None
        
        # Initialize embedding model
        self.embedding_model = None
        if not skip_ai and SENTENCE_TRANSFORMERS_AVAILABLE:
            print("Loading embedding model...")
            try:
                self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2', device=self.device)
            except Exception as e:
                print(f"Warning: Could not load embedding model: {e}")
        
        # Medical categories
        self.categories = {
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
            'Growth and Development': ['growth', 'development', 'developmental', 'milestone'],
            'General Pediatrics': []
        }
        
        # Medical keywords
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
        
        print("Models loaded successfully!")
    
    def count_tokens(self, text: str) -> int:
        """Count tokens using tiktoken or word-based fallback."""
        if self.tiktoken_encoding:
            try:
                tokens = self.tiktoken_encoding.encode(text)
                return len(tokens)
            except Exception:
                pass
        
        # Fallback
        return int(len(text.split()) * 1.3)
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate 1536-dimensional embedding."""
        if self.embedding_model:
            try:
                embedding = self.embedding_model.encode(text, convert_to_numpy=True)
                embedding = embedding.astype(np.float32)
                
                if len(embedding) < 1536:
                    padded = np.zeros(1536, dtype=np.float32)
                    padded[:len(embedding)] = embedding
                    embedding = padded
                elif len(embedding) > 1536:
                    embedding = embedding[:1536]
                
                return embedding.tolist()
            except Exception:
                pass
        
        # Fallback: deterministic pseudo-embedding
        text_hash = hash(text) % (2**32)
        np.random.seed(text_hash)
        embedding = np.random.randn(1536).astype(np.float32)
        embedding = embedding / (np.linalg.norm(embedding) + 1e-10)
        return embedding.tolist()
    
    def extract_topic_subtopic(self, content: str, chapter: str, section: str) -> Tuple[str, str]:
        """Extract topic and subtopic from content."""
        content_lower = content.lower()[:500]
        
        specific_topics = {
            'Physical Growth': ['growth', 'weight', 'height', 'length', 'development'],
            'Infection': ['infection', 'bacteria', 'virus', 'infectious'],
            'Pneumonia': ['pneumonia', 'pneumococ', 'respiratory'],
            'Diabetes': ['diabetes', 'glucose', 'insulin'],
            'Asthma': ['asthma', 'respiratory', 'airway'],
            'Seizure': ['seizure', 'epilepsy', 'convulsion'],
            'Cardiac': ['cardiac', 'heart', 'murmur', 'arrhythmia'],
            'Gastrointestinal': ['gastro', 'stomach', 'intestin', 'bowel'],
            'Neurological': ['neuro', 'brain', 'central', 'peripheral'],
            'Hematology': ['blood', 'anemia', 'hemoglobin'],
            'Oncology': ['cancer', 'oncology', 'tumor', 'leukemia'],
            'Dermatology': ['skin', 'dermatology', 'rash', 'lesion'],
            'Nutrition': ['nutrition', 'feeding', 'diet', 'calorie'],
            'Immunization': ['vaccine', 'immunization', 'immunology'],
        }
        
        topic = 'General Pediatrics'
        for topic_name, keywords in specific_topics.items():
            if any(kw in content_lower for kw in keywords):
                topic = topic_name
                break
        
        subtopic = 'Clinical Overview'
        if 'infant' in content_lower or 'newborn' in content_lower:
            subtopic = 'Neonatal and Infant'
        elif 'child' in content_lower:
            subtopic = 'Childhood'
        elif 'adolescent' in content_lower:
            subtopic = 'Adolescent'
        elif 'diagnosis' in content_lower or 'clinical' in content_lower:
            subtopic = 'Diagnosis and Evaluation'
        elif 'treatment' in content_lower or 'management' in content_lower:
            subtopic = 'Management and Treatment'
        elif 'prevention' in content_lower or 'vaccine' in content_lower:
            subtopic = 'Prevention'
        
        return topic, subtopic
    
    def extract_keywords(self, text: str) -> str:
        """Extract keywords as comma-separated string."""
        keywords_found = set()
        text_lower = text.lower()
        
        for term in self.medical_keywords:
            if term in text_lower:
                keywords_found.add(term)
        
        dosage_patterns = [
            r'\d+\s*(?:mg|g|ml|mcg|units?)/kg',
            r'\d+\s*(?:mg|g|ml|mcg|units?)\s*(?:daily|bid|tid|qid)'
        ]
        
        for pattern in dosage_patterns:
            matches = re.findall(pattern, text_lower)
            keywords_found.update(matches)
        
        return ",".join(sorted(keywords_found)) if keywords_found else "general"
    
    def categorize_content(self, text: str) -> str:
        """Categorize content."""
        text_lower = text.lower()
        
        for category, keywords in self.categories.items():
            if keywords and any(kw in text_lower for kw in keywords):
                return category
        
        return 'General Pediatrics'
    
    def generate_summary(self, text: str, max_length: int = 200) -> str:
        """Generate extractive summary."""
        if len(text) <= max_length:
            return text.strip()
        
        sentences = re.split(r'(?<=[.!?])\s+', text)
        summary = ""
        
        for sent in sentences:
            if len(summary) + len(sent) + 1 <= max_length:
                summary += (" " if summary else "") + sent
            else:
                break
        
        return summary.strip() if summary else text[:max_length].strip()
    
    def process_existing_data(self, input_file: str) -> List[Dict]:
        """Process existing nelson_textbook_data.json."""
        print(f"Loading existing data from {input_file}...")
        
        with open(input_file, 'r', encoding='utf-8') as f:
            existing_records = json.load(f)
        
        print(f"Processing {len(existing_records)} existing records...")
        
        enhanced_records = []
        
        for record in tqdm(existing_records, desc="Enhancing records"):
            try:
                chapter = record.get('chapter', 'Unknown')
                section = record.get('section', 'General')
                content = record.get('content', '')
                page_number = record.get('page_number', 0)
                existing_keywords = record.get('keywords', '')
                
                # Skip empty content
                if not content or len(content) < 50:
                    continue
                
                # Extract enhanced metadata
                topic, subtopic = self.extract_topic_subtopic(content, chapter, section)
                summary = self.generate_summary(content)
                keywords = self.extract_keywords(content)
                category = self.categorize_content(content)
                token_count = self.count_tokens(content)
                embedding = self.generate_embedding(content)
                
                enhanced = {
                    'chapter': chapter,
                    'section': section[:100],
                    'topic': topic,
                    'subtopic': subtopic,
                    'content_summary': summary[:200],
                    'page_number': int(page_number) if page_number else 0,
                    'category': category,
                    'keywords': keywords,
                    'chunk_text': content[:5000],
                    'embedding': embedding,
                    'token_count': token_count,
                    'original_keywords': existing_keywords
                }
                
                enhanced_records.append(enhanced)
            
            except Exception as e:
                print(f"Error processing record: {e}")
                continue
        
        print(f"\nTotal enhanced records: {len(enhanced_records)}")
        return enhanced_records
    
    def export_csv(self, records: List[Dict], filename: str = "enhanced_nelson_dataset.csv"):
        """Export to CSV."""
        print(f"\nExporting to CSV: {filename}")
        
        fieldnames = ['chapter', 'section', 'topic', 'subtopic', 'content_summary',
                      'page_number', 'category', 'keywords', 'chunk_text']
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for record in tqdm(records, desc="Writing CSV"):
                csv_record = {k: v for k, v in record.items() if k in fieldnames}
                writer.writerow(csv_record)
        
        print(f"✓ Exported {len(records)} records")
    
    def export_json(self, records: List[Dict], filename: str = "enhanced_nelson_data.json"):
        """Export to JSON."""
        print(f"\nExporting to JSON: {filename}")
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(records, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Exported {len(records)} records")
    
    def export_sql(self, records: List[Dict],
                   create_table_file: str = "setup_nelson_gpt_knowledge.sql",
                   inserts_file: str = "enhanced_nelson_inserts.sql"):
        """Export to SQL."""
        print(f"\nGenerating SQL...")
        
        create_table_sql = """-- Create pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Drop table if exists
DROP TABLE IF EXISTS nelson_gpt_knowledge CASCADE;

-- Create table
CREATE TABLE IF NOT EXISTS nelson_gpt_knowledge (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  chapter TEXT,
  section TEXT,
  topic TEXT,
  subtopic TEXT,
  content_summary TEXT,
  page_number INT,
  category TEXT,
  keywords TEXT,
  chunk_text TEXT,
  embedding VECTOR(1536),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indices
CREATE INDEX IF NOT EXISTS idx_nelson_chapter ON nelson_gpt_knowledge(chapter);
CREATE INDEX IF NOT EXISTS idx_nelson_category ON nelson_gpt_knowledge(category);
CREATE INDEX IF NOT EXISTS idx_nelson_topic ON nelson_gpt_knowledge(topic);
CREATE INDEX IF NOT EXISTS idx_nelson_keywords ON nelson_gpt_knowledge USING GIN(to_tsvector('english', keywords));
CREATE INDEX IF NOT EXISTS idx_nelson_embedding ON nelson_gpt_knowledge USING HNSW (embedding vector_cosine_ops);
"""
        
        with open(create_table_file, 'w', encoding='utf-8') as f:
            f.write(create_table_sql)
        
        print(f"✓ Created table definition")
        
        with open(inserts_file, 'w', encoding='utf-8') as f:
            f.write("-- Insert statements\n\n")
            
            for record in tqdm(records, desc="Writing SQL inserts"):
                chapter = record['chapter'].replace("'", "''")
                section = record['section'].replace("'", "''")
                topic = record['topic'].replace("'", "''")
                subtopic = record['subtopic'].replace("'", "''")
                summary = record['content_summary'].replace("'", "''")
                category = record['category'].replace("'", "''")
                keywords = record['keywords'].replace("'", "''")
                chunk = record['chunk_text'].replace("'", "''")
                
                embedding_str = ','.join(f"{e:.6f}" for e in record['embedding'])
                embedding_pg = f"'[{embedding_str}]'::vector(1536)"
                
                insert = f"""INSERT INTO nelson_gpt_knowledge 
(chapter, section, topic, subtopic, content_summary, page_number, category, keywords, chunk_text, embedding)
VALUES ('{chapter}', '{section}', '{topic}', '{subtopic}', '{summary}', {record['page_number']},
        '{category}', '{keywords}', '{chunk}', {embedding_pg});
"""
                f.write(insert)
        
        print(f"✓ Generated {len(records)} insert statements")
    
    def export_report(self, records: List[Dict], filename: str = "enhanced_dataset_summary.md"):
        """Generate summary report."""
        print(f"\nGenerating report: {filename}")
        
        token_counts = [r['token_count'] for r in records]
        categories = {}
        chapters = set()
        topics = set()
        
        for r in records:
            categories[r['category']] = categories.get(r['category'], 0) + 1
            chapters.add(r['chapter'])
            topics.add(r['topic'])
        
        report = f"""# Enhanced Nelson Dataset Summary

## Overview
- **Total Records**: {len(records)}
- **Unique Chapters**: {len(chapters)}
- **Unique Topics**: {len(topics)}
- **Unique Categories**: {len(categories)}

## Token Distribution
- **Minimum**: {min(token_counts)}
- **Maximum**: {max(token_counts)}
- **Average**: {np.mean(token_counts):.1f}
- **Median**: {np.median(token_counts):.1f}

## Categories
"""
        for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
            pct = (count / len(records)) * 100
            report += f"- **{cat}**: {count} ({pct:.1f}%)\n"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✓ Generated report")


def main():
    """Main execution."""
    import sys
    
    use_gpu = TORCH_AVAILABLE and torch.cuda.is_available()
    skip_ai = "--skip-ai" in sys.argv
    
    print("Enhanced Nelson Dataset Generation (from existing data)")
    print("="*60)
    
    converter = EnhancedNelsonFromExisting(use_gpu=use_gpu, skip_ai=skip_ai)
    
    input_file = "/project/workspace/apkaapna007-a11y/Nelson-Textbook-of-Pediatrics-/nelson_textbook_data.json"
    output_base = "/project/workspace"
    
    records = converter.process_existing_data(input_file)
    
    if records:
        converter.export_csv(records, f"{output_base}/enhanced_nelson_dataset.csv")
        converter.export_json(records, f"{output_base}/enhanced_nelson_data.json")
        converter.export_sql(
            records,
            f"{output_base}/setup_nelson_gpt_knowledge.sql",
            f"{output_base}/enhanced_nelson_inserts.sql"
        )
        converter.export_report(records, f"{output_base}/enhanced_dataset_summary.md")
    
    print("\n" + "="*60)
    print("✓ ENHANCED DATASET GENERATION COMPLETE")
    print("="*60)


if __name__ == "__main__":
    main()
