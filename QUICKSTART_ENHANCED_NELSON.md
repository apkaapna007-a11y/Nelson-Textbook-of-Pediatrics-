# Quick Start Guide - Enhanced Nelson Textbook Dataset

## ⚡ 5-Minute Setup

### 1. View the Data

**Spreadsheet (CSV)**
```bash
# Open in Excel, Google Sheets, or LibreOffice
open enhanced_nelson_dataset.csv

# Or view in terminal
head -5 enhanced_nelson_dataset.csv
```

**JSON (Python)**
```python
import json
data = json.load(open('enhanced_nelson_data.json'))
print(f"Records: {len(data)}")
print(f"Sample: {data[0]['chapter']} - {data[0]['topic']}")
```

### 2. Database Setup (PostgreSQL)

```bash
# 1. Install PostgreSQL (if needed)
# Mac: brew install postgresql
# Ubuntu: sudo apt-get install postgresql postgresql-contrib
# Windows: Download from postgresql.org

# 2. Enable pgvector extension
sudo -u postgres psql
CREATE EXTENSION vector;
\q

# 3. Create database
createdb nelson_medical

# 4. Load table definition
psql -d nelson_medical -f setup_nelson_gpt_knowledge.sql

# 5. Load data (this may take a few minutes)
psql -d nelson_medical -f enhanced_nelson_inserts.sql

# 6. Verify
psql -d nelson_medical -c "SELECT COUNT(*) FROM nelson_gpt_knowledge;"
```

### 3. Query the Data

**SQL - All Records**
```sql
SELECT chapter, topic, subtopic, content_summary
FROM nelson_gpt_knowledge
LIMIT 5;
```

**SQL - By Category**
```sql
SELECT chapter, topic, content_summary
FROM nelson_gpt_knowledge
WHERE category = 'Infectious Diseases'
LIMIT 10;
```

**SQL - Vector Search**
```sql
-- Find similar content using embeddings
SELECT chapter, topic, content_summary,
       embedding <-> '[0.1, -0.2, ..., 0.5]'::vector(1536) AS distance
FROM nelson_gpt_knowledge
ORDER BY distance ASC
LIMIT 5;
```

## 📚 What You Get

| Format | Size | Best For |
|--------|------|----------|
| CSV | 25 MB | Spreadsheets, Excel, Analytics |
| JSON | 1.5 GB | APIs, Python, JavaScript |
| SQL | 509 MB | PostgreSQL Database |

## 🎯 Common Use Cases

### Use Case 1: Medical Search Engine

```python
# Find articles about specific disease
import json
data = json.load(open('enhanced_nelson_data.json'))
results = [r for r in data if 'pneumonia' in r['keywords']]
print(f"Found {len(results)} articles about pneumonia")
```

### Use Case 2: Topic Analysis

```python
# Count records by medical category
from collections import Counter
categories = Counter(r['category'] for r in data)
print(categories.most_common(5))
```

### Use Case 3: Semantic Search

```sql
-- Find similar content by embedding distance
WITH query_record AS (
  SELECT embedding FROM nelson_gpt_knowledge 
  WHERE topic = 'Diabetes' LIMIT 1
)
SELECT chapter, topic, 
       embedding <-> (SELECT embedding FROM query_record) AS distance
FROM nelson_gpt_knowledge
WHERE category NOT LIKE 'Diabetes'
ORDER BY distance
LIMIT 10;
```

### Use Case 4: Export by Category

```bash
# Extract only Infectious Diseases
grep "Infectious Diseases" enhanced_nelson_dataset.csv > infectious_diseases.csv
```

## 🔍 Data Structure

### CSV Columns
```
chapter              - Chapter number (e.g., "Chapter 150")
section              - Section title
topic                - Main medical topic
subtopic             - Specific aspect/age group
content_summary      - Max 200 char summary
page_number          - Original page number
category             - Medical specialty (13 categories)
keywords             - Comma-separated medical terms
chunk_text           - Full content text
```

### JSON Record
```json
{
  "chapter": "Chapter 150",
  "topic": "General Pediatrics",
  "subtopic": "Clinical Overview",
  "category": "General Pediatrics",
  "keywords": "general,pediatric",
  "content_summary": "Text summary...",
  "embedding": [0.124, -0.432, ..., 0.891],  // 1536 floats
  "token_count": 145
}
```

## 📊 Dataset Stats

```
Total Records:        34,306
Unique Chapters:      600+
Embedding Dims:       1536
Categories:           13
Topics:               14+
File Sizes:
  - CSV:              25 MB
  - JSON:             1.5 GB
  - SQL:              509 MB
  - Total:            2.2 GB
```

## 🚀 Performance Tips

### For Large Datasets
```sql
-- Use indices for faster queries
CREATE INDEX idx_quick_search ON nelson_gpt_knowledge(category, topic);

-- Use LIMIT to paginate results
SELECT * FROM nelson_gpt_knowledge LIMIT 100 OFFSET 0;
```

### For Embeddings
```sql
-- Vector search is fastest with proper index
SELECT * FROM nelson_gpt_knowledge 
ORDER BY embedding <-> query_vector
LIMIT 10;
```

### For CSV Analysis
```bash
# Count records: 34,306
wc -l enhanced_nelson_dataset.csv

# Get unique categories
cut -d',' -f7 enhanced_nelson_dataset.csv | sort -u
```

## 🐛 Troubleshooting

### Issue: "psql: command not found"
```bash
# Install PostgreSQL
brew install postgresql    # Mac
apt-get install postgresql # Ubuntu
```

### Issue: "could not translate host name"
```bash
# Use localhost explicitly
psql -h localhost -d nelson_medical
```

### Issue: Permission denied for large SQL file
```bash
# Try line-by-line loading
head -1000 enhanced_nelson_inserts.sql | psql -d nelson_medical
```

### Issue: Out of memory with JSON
```bash
# Stream process instead of loading all at once
import json
with open('enhanced_nelson_data.json') as f:
    for line in f:
        record = json.loads(line)
        # Process one record at a time
```

## 📖 Full Documentation

For detailed information, see:
- **ENHANCED_DATASET_README.md** - Complete technical guide
- **ENHANCED_NELSON_COMPLETION_SUMMARY.md** - Project report
- **INDEX_ENHANCED_NELSON.md** - File reference

## ✅ Validation

```bash
# Verify data integrity
python3 validate_enhanced_dataset.py

# Check file sizes
ls -lh enhanced*

# Count records
wc -l enhanced_nelson_dataset.csv
```

## 🔄 Re-generate Dataset

```bash
# Regenerate from existing data (faster, ~2 minutes)
python3 create_enhanced_nelson_from_existing.py

# Regenerate from raw text files (slower, more control)
python3 create_enhanced_nelson_dataset.py
```

## 💡 Example Queries

### Find all growth and development content
```sql
SELECT chapter, topic, content_summary
FROM nelson_gpt_knowledge
WHERE category = 'Growth and Development'
AND topic LIKE '%Growth%';
```

### Search for dosage information
```sql
SELECT chapter, topic, keywords
FROM nelson_gpt_knowledge
WHERE keywords LIKE '%mg/kg%' OR keywords LIKE '%daily%';
```

### Get neonatal content
```sql
SELECT chapter, topic, content_summary
FROM nelson_gpt_knowledge
WHERE subtopic = 'Neonatal and Infant'
LIMIT 20;
```

### Vector similarity (medical clustering)
```sql
-- Find related topics using embeddings
SELECT DISTINCT a.topic, b.topic,
       a.embedding <-> b.embedding AS similarity
FROM nelson_gpt_knowledge a, nelson_gpt_knowledge b
WHERE a.category = b.category
AND a.embedding <-> b.embedding < 0.5
LIMIT 50;
```

---

## 🎓 Next Steps

1. **Explore Data**
   - Open CSV in spreadsheet for quick overview
   - Run validation to verify integrity

2. **Setup Database** (optional)
   - Install PostgreSQL with pgvector
   - Load SQL files for powerful queries

3. **Build Applications**
   - Use JSON for APIs
   - Use SQL for web apps
   - Use embeddings for ML models

4. **Integrate Systems**
   - Connect to medical apps
   - Build search engines
   - Create decision support tools

---

## ❓ Quick Help

| Need | Command |
|------|---------|
| View CSV | `head enhanced_nelson_dataset.csv` |
| Count JSON | `python3 -c "import json; print(len(json.load(open('enhanced_nelson_data.json'))))"` |
| Database check | `psql -d nelson_medical -c "SELECT COUNT(*) FROM nelson_gpt_knowledge;"` |
| Validate | `python3 validate_enhanced_dataset.py` |

---

**Generated**: November 10, 2025  
**Status**: ✅ Ready to Use
