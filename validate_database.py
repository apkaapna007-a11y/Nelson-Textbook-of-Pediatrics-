#!/usr/bin/env python3
"""
Validation script to test the Nelson Pediatric Database setup.
This script can be used to verify that the database is properly configured
and contains the expected data.
"""

import json
import sys
from typing import Dict, List

def validate_json_files():
    """Validate the generated JSON files."""
    print("🔍 Validating JSON files...")
    
    try:
        # Validate Nelson textbook data
        with open('nelson_textbook_data.json', 'r', encoding='utf-8') as f:
            nelson_data = json.load(f)
        
        print(f"✅ Nelson textbook data: {len(nelson_data)} records loaded")
        
        # Check required fields
        required_fields = ['id', 'chapter', 'section', 'content', 'keywords', 'medical_category', 'age_group']
        sample_record = nelson_data[0]
        
        for field in required_fields:
            if field not in sample_record:
                print(f"❌ Missing required field: {field}")
                return False
        
        print("✅ All required fields present in Nelson data")
        
        # Validate pediatric resources data
        with open('pediatric_resources_data.json', 'r', encoding='utf-8') as f:
            resources_data = json.load(f)
        
        print(f"✅ Pediatric resources data: {len(resources_data)} records loaded")
        
        # Check required fields for resources
        resource_fields = ['id', 'title', 'content', 'resource_type', 'category', 'age_range', 'source']
        sample_resource = resources_data[0]
        
        for field in resource_fields:
            if field not in sample_resource:
                print(f"❌ Missing required field in resources: {field}")
                return False
        
        print("✅ All required fields present in resources data")
        
        return True
        
    except Exception as e:
        print(f"❌ Error validating JSON files: {e}")
        return False

def validate_sql_files():
    """Validate the generated SQL files."""
    print("\n🔍 Validating SQL files...")
    
    try:
        # Check Nelson textbook inserts
        with open('nelson_textbook_inserts.sql', 'r', encoding='utf-8') as f:
            nelson_sql = f.read()
        
        insert_count = nelson_sql.count('INSERT INTO nelson_textbook')
        print(f"✅ Nelson textbook SQL: {insert_count} INSERT statements")
        
        # Check pediatric resources inserts
        with open('pediatric_resources_inserts.sql', 'r', encoding='utf-8') as f:
            resources_sql = f.read()
        
        resource_insert_count = resources_sql.count('INSERT INTO pediatric_medical_resources')
        print(f"✅ Pediatric resources SQL: {resource_insert_count} INSERT statements")
        
        # Check setup script
        with open('setup_nelson_database.sql', 'r', encoding='utf-8') as f:
            setup_sql = f.read()
        
        # Verify key components in setup script
        required_components = [
            'CREATE EXTENSION IF NOT EXISTS vector',
            'CREATE TABLE IF NOT EXISTS nelson_textbook',
            'CREATE TABLE IF NOT EXISTS pediatric_medical_resources',
            'CREATE TABLE IF NOT EXISTS chat_sessions',
            'CREATE TABLE IF NOT EXISTS chat_messages',
            'CREATE OR REPLACE FUNCTION match_documents'
        ]
        
        for component in required_components:
            if component not in setup_sql:
                print(f"❌ Missing component in setup script: {component}")
                return False
        
        print("✅ Setup script contains all required components")
        
        return True
        
    except Exception as e:
        print(f"❌ Error validating SQL files: {e}")
        return False

def analyze_data_distribution():
    """Analyze the distribution of data across categories and age groups."""
    print("\n📊 Analyzing data distribution...")
    
    try:
        with open('nelson_textbook_data.json', 'r', encoding='utf-8') as f:
            nelson_data = json.load(f)
        
        # Analyze categories
        categories = {}
        age_groups = {}
        chapters = set()
        
        for record in nelson_data:
            category = record.get('medical_category', 'Unknown')
            age_group = record.get('age_group', 'Unknown')
            chapter = record.get('chapter', 'Unknown')
            
            categories[category] = categories.get(category, 0) + 1
            age_groups[age_group] = age_groups.get(age_group, 0) + 1
            chapters.add(chapter)
        
        print(f"📈 Data distribution:")
        print(f"   - Total records: {len(nelson_data)}")
        print(f"   - Unique categories: {len(categories)}")
        print(f"   - Unique age groups: {len(age_groups)}")
        print(f"   - Unique chapters: {len(chapters)}")
        
        print(f"\n🏥 Top 5 medical categories:")
        sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)
        for category, count in sorted_categories[:5]:
            print(f"   - {category}: {count} records")
        
        print(f"\n👶 Age group distribution:")
        sorted_age_groups = sorted(age_groups.items(), key=lambda x: x[1], reverse=True)
        for age_group, count in sorted_age_groups:
            print(f"   - {age_group}: {count} records")
        
        return True
        
    except Exception as e:
        print(f"❌ Error analyzing data distribution: {e}")
        return False

def validate_content_quality():
    """Validate the quality of parsed content."""
    print("\n🔍 Validating content quality...")
    
    try:
        with open('nelson_textbook_data.json', 'r', encoding='utf-8') as f:
            nelson_data = json.load(f)
        
        # Check for empty or very short content
        short_content_count = 0
        empty_content_count = 0
        total_content_length = 0
        
        for record in nelson_data:
            content = record.get('content', '')
            if not content:
                empty_content_count += 1
            elif len(content) < 50:
                short_content_count += 1
            
            total_content_length += len(content)
        
        avg_content_length = total_content_length / len(nelson_data) if nelson_data else 0
        
        print(f"📝 Content quality metrics:")
        print(f"   - Average content length: {avg_content_length:.0f} characters")
        print(f"   - Empty content records: {empty_content_count}")
        print(f"   - Very short content records (<50 chars): {short_content_count}")
        
        # Check keyword extraction
        total_keywords = 0
        records_with_keywords = 0
        
        for record in nelson_data:
            keywords = record.get('keywords', [])
            if keywords:
                records_with_keywords += 1
                total_keywords += len(keywords)
        
        avg_keywords = total_keywords / records_with_keywords if records_with_keywords else 0
        
        print(f"🏷️  Keyword extraction metrics:")
        print(f"   - Records with keywords: {records_with_keywords}/{len(nelson_data)}")
        print(f"   - Average keywords per record: {avg_keywords:.1f}")
        
        # Quality assessment
        quality_score = 100
        if empty_content_count > 0:
            quality_score -= 20
            print("⚠️  Warning: Found records with empty content")
        
        if short_content_count > len(nelson_data) * 0.1:  # More than 10% short content
            quality_score -= 15
            print("⚠️  Warning: High number of very short content records")
        
        if records_with_keywords < len(nelson_data) * 0.5:  # Less than 50% have keywords
            quality_score -= 10
            print("⚠️  Warning: Low keyword extraction rate")
        
        print(f"\n🎯 Overall quality score: {quality_score}/100")
        
        return quality_score >= 70
        
    except Exception as e:
        print(f"❌ Error validating content quality: {e}")
        return False

def generate_sample_queries():
    """Generate sample SQL queries for testing."""
    print("\n📝 Generating sample queries...")
    
    sample_queries = """
-- Sample SQL queries for testing the Nelson Pediatric Database

-- 1. Get all infectious disease content
SELECT chapter, section, content 
FROM nelson_textbook 
WHERE medical_category = 'Infectious Diseases' 
LIMIT 5;

-- 2. Search for fever-related content
SELECT chapter, section, content 
FROM nelson_textbook 
WHERE 'fever' = ANY(keywords) 
LIMIT 5;

-- 3. Get content appropriate for infants
SELECT chapter, section, content 
FROM nelson_textbook 
WHERE age_group IN ('Infant (1-12 months)', 'All Ages') 
LIMIT 5;

-- 4. Get emergency protocols
SELECT title, content, age_range 
FROM pediatric_medical_resources 
WHERE resource_type = 'protocol' 
  AND category = 'Emergency Medicine';

-- 5. Get medication dosing information
SELECT title, content, age_range, weight_range 
FROM pediatric_medical_resources 
WHERE resource_type = 'dosage' 
ORDER BY category;

-- 6. Search content by multiple keywords
SELECT * FROM search_by_keywords(
  ARRAY['antibiotic', 'infection', 'pediatric'], 
  10
);

-- 7. Get respiratory content for school-age children
SELECT * FROM get_age_appropriate_content(
  'School Age (5-12 years)', 
  'Respiratory', 
  5
);

-- 8. Database statistics
SELECT * FROM database_statistics;

-- 9. Count records by category
SELECT medical_category, COUNT(*) as record_count
FROM nelson_textbook 
GROUP BY medical_category 
ORDER BY record_count DESC;

-- 10. Find content with most keywords
SELECT chapter, section, array_length(keywords, 1) as keyword_count
FROM nelson_textbook 
WHERE keywords IS NOT NULL
ORDER BY keyword_count DESC 
LIMIT 10;
"""
    
    with open('sample_queries.sql', 'w', encoding='utf-8') as f:
        f.write(sample_queries)
    
    print("✅ Sample queries saved to sample_queries.sql")

def main():
    """Run all validation checks."""
    print("🚀 Starting Nelson Pediatric Database validation...\n")
    
    all_passed = True
    
    # Run validation checks
    if not validate_json_files():
        all_passed = False
    
    if not validate_sql_files():
        all_passed = False
    
    if not analyze_data_distribution():
        all_passed = False
    
    if not validate_content_quality():
        all_passed = False
    
    # Generate sample queries
    generate_sample_queries()
    
    # Final result
    print("\n" + "="*60)
    if all_passed:
        print("🎉 All validation checks passed!")
        print("✅ The Nelson Pediatric Database dataset is ready for use.")
        print("\n📋 Next steps:")
        print("   1. Set up PostgreSQL with pgvector extension")
        print("   2. Run setup_nelson_database.sql")
        print("   3. Load data using the generated SQL insert files")
        print("   4. Test with sample_queries.sql")
        print("   5. Generate embeddings for vector search functionality")
    else:
        print("❌ Some validation checks failed.")
        print("⚠️  Please review the issues above before using the dataset.")
        sys.exit(1)

if __name__ == "__main__":
    main()

