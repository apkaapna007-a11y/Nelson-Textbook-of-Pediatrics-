#!/usr/bin/env python3
"""
Script to create a comprehensive dataset.csv from Nelson Textbook text files
following the database schema for nelson_textbook table.
"""

import csv
import re
import uuid
from datetime import datetime
import os

def extract_chapter_info(text_chunk):
    """Extract chapter and section information from text."""
    chapter_match = re.search(r'Chapter\s+(\d+)', text_chunk, re.IGNORECASE)
    chapter_num = chapter_match.group(1) if chapter_match else "Unknown"
    
    # Look for section titles (usually after chapter)
    lines = text_chunk.split('\n')
    section = "General"
    for i, line in enumerate(lines):
        if 'Chapter' in line and i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            if next_line and len(next_line) > 3:
                section = next_line
                break
    
    return f"Chapter {chapter_num}", section

def extract_medical_keywords(content):
    """Extract medical keywords from content."""
    # Common medical terms to look for
    medical_terms = [
        'diagnosis', 'treatment', 'symptoms', 'therapy', 'medication', 'disease',
        'syndrome', 'disorder', 'infection', 'inflammation', 'development',
        'growth', 'pediatric', 'adolescent', 'neonatal', 'infant', 'child',
        'dosage', 'mg/kg', 'antibiotic', 'vaccine', 'immunization'
    ]
    
    found_keywords = []
    content_lower = content.lower()
    
    for term in medical_terms:
        if term in content_lower:
            found_keywords.append(term)
    
    # Add specific medical terms found in the content
    medical_patterns = [
        r'\b\w+itis\b',  # conditions ending in -itis
        r'\b\w+osis\b',  # conditions ending in -osis  
        r'\b\w+emia\b',  # conditions ending in -emia
        r'\d+\s*mg/kg\b', # dosages
        r'\b[A-Z][a-z]+\s+syndrome\b'  # syndromes
    ]
    
    for pattern in medical_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        found_keywords.extend([match.lower() for match in matches])
    
    return list(set(found_keywords))  # Remove duplicates

def categorize_content(content, chapter):
    """Categorize content based on keywords and chapter."""
    content_lower = content.lower()
    
    if any(term in content_lower for term in ['adolescent', 'teenager', 'puberty']):
        return 'Adolescent Medicine'
    elif any(term in content_lower for term in ['development', 'growth', 'milestone']):
        return 'Growth and Development'
    elif any(term in content_lower for term in ['kidney', 'renal', 'urinary', 'urology']):
        return 'Urology'
    elif any(term in content_lower for term in ['infection', 'antibiotic', 'bacteria', 'virus']):
        return 'Infectious Diseases'
    elif any(term in content_lower for term in ['heart', 'cardiac', 'cardiovascular']):
        return 'Cardiology'
    elif any(term in content_lower for term in ['respiratory', 'lung', 'asthma', 'pneumonia']):
        return 'Pulmonology'
    elif any(term in content_lower for term in ['neurologic', 'brain', 'seizure', 'neurology']):
        return 'Neurology'
    else:
        return 'General Pediatrics'

def determine_age_group(content):
    """Determine age group based on content."""
    content_lower = content.lower()
    
    if any(term in content_lower for term in ['adolescent', 'teenager', 'puberty']):
        return 'Adolescent'
    elif any(term in content_lower for term in ['neonate', 'newborn', 'birth']):
        return 'Neonatal'
    elif any(term in content_lower for term in ['infant', 'baby', 'months old']):
        return 'Infant'
    else:
        return 'Pediatric'

def process_text_file(filename):
    """Process a text file and extract structured data."""
    try:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return []
    
    # Split content into chunks (by chapters or sections)
    chunks = []
    
    # Split by "Chapter" occurrences
    chapter_splits = re.split(r'\n\s*Chapter\s+\d+', content, flags=re.IGNORECASE)
    
    for i, chunk in enumerate(chapter_splits):
        if len(chunk.strip()) < 100:  # Skip very short chunks
            continue
            
        # Clean up the chunk
        chunk = chunk.strip()
        if not chunk:
            continue
            
        # Extract meaningful paragraphs (at least 200 characters)
        paragraphs = [p.strip() for p in chunk.split('\n\n') if len(p.strip()) > 200]
        
        for paragraph in paragraphs[:3]:  # Take first 3 substantial paragraphs per chapter
            if len(paragraph) > 200:
                chunks.append(paragraph)
    
    return chunks

def create_dataset():
    """Create the main dataset CSV file."""
    text_files = ['part1 (1).txt', 'part2.txt', 'part3.txt']
    
    dataset = []
    current_time = datetime.now().isoformat() + 'Z'
    
    entry_id = 1
    
    for filename in text_files:
        if not os.path.exists(filename):
            print(f"Warning: {filename} not found")
            continue
            
        print(f"Processing {filename}...")
        chunks = process_text_file(filename)
        
        for chunk in chunks:
            chapter, section = extract_chapter_info(chunk)
            keywords = extract_medical_keywords(chunk)
            category = categorize_content(chunk, chapter)
            age_group = determine_age_group(chunk)
            
            # Estimate page number (rough approximation)
            page_number = entry_id * 50 + 100
            
            entry = {
                'id': entry_id,
                'chapter': chapter,
                'section': section,
                'page_number': page_number,
                'content': chunk.replace('"', '""'),  # Escape quotes for CSV
                'keywords': '|'.join(keywords) if keywords else 'general pediatrics',
                'medical_category': category,
                'age_group': age_group,
                'created_at': current_time,
                'updated_at': current_time
            }
            
            dataset.append(entry)
            entry_id += 1
            
            # Process more entries from each file
            if len(dataset) >= 200:
                break
        
        if len(dataset) >= 600:
            break
    
    # Write to CSV
    fieldnames = ['id', 'chapter', 'section', 'page_number', 'content', 'keywords', 
                  'medical_category', 'age_group', 'created_at', 'updated_at']
    
    with open('dataset.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dataset)
    
    print(f"Created dataset.csv with {len(dataset)} entries")
    return len(dataset)

if __name__ == "__main__":
    create_dataset()
