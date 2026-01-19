import sys
import re
import json
import csv
import os

def load_all_text():
    files = ['part1.txt', 'part2.txt', 'part3.txt']
    text = ""
    for fn in files:
        if os.path.exists(fn):
            with open(fn, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                text += content
                if content and not content.endswith('\n'):
                    text += '\n'
        else:
            fn_cap = fn.capitalize()
            if os.path.exists(fn_cap):
                with open(fn_cap, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    text += content
                    if content and not content.endswith('\n'):
                        text += '\n'
    return text

def parse_headings(text):
    lines = text.splitlines(keepends=True)
    toc = []
    offset = 0

    re_part = re.compile(r'^PART\s+([IVXLC]+)$', re.I)
    re_chapter = re.compile(r'^Chapter\s+(\d+)$', re.I)
    re_numbered = re.compile(r'^(\d+\.\d+(?:\.\d+)*)\s+(.*)$')
    re_all_caps = re.compile(r'^[A-Z][A-Z\s\d\-\.\:\,]{10,}$')

    candidates = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        line_offset = offset
        offset += len(line)

        # Level 1: PART
        if re_part.match(stripped):
            title = stripped
            j = i + 1
            while j < len(lines) and not lines[j].strip(): j += 1
            if j < len(lines) and len(lines[j].strip()) < 100 and \
               not re_part.match(lines[j].strip()) and not re_chapter.match(lines[j].strip()):
                title += " " + lines[j].strip()
            candidates.append({'level': 1, 'title': title, 'start_offset': line_offset})

        # Level 2: Chapter
        elif re_chapter.match(stripped):
            title = stripped
            j = i + 1
            while j < len(lines) and not lines[j].strip(): j += 1
            if j < len(lines) and len(lines[j].strip()) < 100 and \
               not re_chapter.match(lines[j].strip()) and not re_numbered.match(lines[j].strip()):
                title += ": " + lines[j].strip()
            candidates.append({'level': 2, 'title': title, 'start_offset': line_offset})

        # Level 3: Numbered
        elif re_numbered.match(stripped):
            candidates.append({'level': 3, 'title': stripped, 'start_offset': line_offset})

        # Level 4: ALL CAPS
        elif re_all_caps.match(stripped):
            if "Chapter" not in stripped and "PART" not in stripped and "Downloaded for" not in stripped:
                candidates.append({'level': 4, 'title': stripped, 'start_offset': line_offset})

        # Level 5: Title Case + blank line
        elif stripped and i > 0 and not lines[i-1].strip() and i < len(lines)-1 and not lines[i+1].strip():
            if re.match(r'^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*$', stripped):
                if 3 < len(stripped) < 60:
                    candidates.append({'level': 5, 'title': stripped, 'start_offset': line_offset})

        i += 1

    tree = []
    stack = []
    for cand in candidates:
        node = {
            'id': f"TOC_{len(tree):06d}",
            'level': cand['level'],
            'title': cand['title'],
            'start_offset': cand['start_offset'],
            'end_offset': -1,
            'parent_id': None
        }
        while stack and stack[-1]['level'] >= cand['level']:
            stack.pop()
        if stack:
            node['parent_id'] = stack[-1]['id']
        tree.append(node)
        stack.append(node)

    for i in range(len(tree)):
        if i < len(tree) - 1:
            tree[i]['end_offset'] = tree[i+1]['start_offset']
        else:
            tree[i]['end_offset'] = len(text)

    return tree

def extract_entities(text):
    entities = {
        'diseases': [], 'drugs': [], 'organisms': [], 'labs': [],
        'procedures': [], 'vaccines': [], 'abbreviations': []
    }
    patterns = {
        'diseases': r'\b[\w\s-]+(?:syndrome|disease|agenesis|dysgenesis|aplasia|hypoplasia|dysplasia|disorder|anomaly|anomalies|malformation|atrophy|infection|inflammation|cancer|tumor|carcinoma|sarcoma|lymphoma|leukemia|deficiency|insufficiency|failure|colic|depression|amblyopia|strabismus)\b',
        'drugs': r'\b(?:alcohol|mercury|nicotine|aspirin|ibuprofen|acetaminophen|penicillin|amoxicillin|insulin|progestins|thiopurine)\b',
        'organisms': r'\b(?:virus|bacteria|fungus|parasite|streptococcus|staphylococcus|e\. coli|hiv|hcv|hbv)\b',
        'labs': r'\b(?:IQ|DNA|RNA|PCR|CT|MRI|ultrasound|ultrasonography|scintigraphy|glucose|creatinine|hemoglobin|white blood cell|platelet|electrolytes|pH|pO2|pCO2|methylation|acetylation)\b',
        'procedures': r'\b(?:surgery|resection|biopsy|incision|drainage|transplant|intubation|catheterization|vaccination|immunization|therapy|treatment|management|counseling|patching)\b',
        'vaccines': r'\b(?:vaccine|vaccination|immunization|dtap|mmr|ipv|hepb|hib|pcv|rv)\b',
    }
    for cat, pat in patterns.items():
        matches = re.findall(pat, text, re.I)
        entities[cat] = sorted(list(set(m.strip() for m in matches)))
    abbr_matches = re.findall(r'\b([A-Z]{2,})\b(?:\s*\(([^)]+)\))?', text)
    for abbr, expansion in abbr_matches:
        if expansion and len(expansion) > 3:
            entities['abbreviations'].append(f"{abbr} ({expansion})")
        else:
            entities['abbreviations'].append(abbr)
    entities['abbreviations'] = sorted(list(set(entities['abbreviations'])))
    return entities

def extract_keywords(text, entities):
    words = re.findall(r'\b[a-zA-Z]{5,}\b', text.lower())
    stopwords = {'their', 'there', 'these', 'those', 'which', 'where', 'while', 'after', 'before', 'would', 'could', 'should'}
    words = [w for w in words if w not in stopwords]
    freq = {}
    for w in words: freq[w] = freq.get(w, 0) + 1
    sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    top_words = [w for w, f in sorted_words[:15]]
    entity_terms = []
    for cat in ['diseases', 'drugs', 'organisms']:
        entity_terms.extend([e.lower() for e in entities[cat]])
    keywords = sorted(list(set(top_words + entity_terms)))
    return keywords[:25]

def create_chunk(section_counter, section, chunk_text, start_off, end_off, chapter_title, chapter_id, subsection_path):
    entities = extract_entities(chunk_text)
    keywords = extract_keywords(chunk_text, entities)
    return {
        'chunk_id': "",
        'chapter_title': chapter_title,
        'chapter_id': chapter_id,
        'section_title': section['title'],
        'section_id': section['id'],
        'subsection_path': subsection_path,
        'start_offset': start_off,
        'end_offset': end_off,
        'chunk_index_in_section': section_counter,
        'token_estimate': len(chunk_text.split()),
        'text': chunk_text,
        'keywords': "|".join(keywords),
        'entities_json': json.dumps(entities)
    }

def chunk_sections(text, toc):
    leaf_ids = set(node['id'] for node in toc)
    for node in toc:
        if node['parent_id'] in leaf_ids:
            leaf_ids.remove(node['parent_id'])
    leaf_sections = sorted([node for node in toc if node['id'] in leaf_ids], key=lambda x: x['start_offset'])

    chunks = []
    buffered_text = ""
    buffered_start_off = -1

    for i, section in enumerate(leaf_sections):
        section_text = text[section['start_offset']:section['end_offset']]
        if not section_text.strip(): continue

        # Determine if we should buffer this section
        num_words = len(section_text.split())
        next_section = leaf_sections[i+1] if i+1 < len(leaf_sections) else None
        if num_words < 250 and next_section and next_section['parent_id'] == section['parent_id']:
            if buffered_text:
                buffered_text += section_text
            else:
                buffered_text = section_text
                buffered_start_off = section['start_offset']
            continue

        if buffered_text:
            section_text = buffered_text + section_text
            curr_start_off = buffered_start_off
            buffered_text = ""
        else:
            curr_start_off = section['start_offset']

        path = []
        curr = section
        while curr:
            path.append(curr['title'])
            curr = next((n for n in toc if n['id'] == curr['parent_id']), None)
        subsection_path = " > ".join(reversed(path))

        chapter_title, chapter_id = "", ""
        curr = section
        while curr:
            if curr['level'] == 2:
                chapter_title, chapter_id = curr['title'], curr['id']
                break
            curr = next((n for n in toc if n['id'] == curr['parent_id']), None)

        # Split into atomic blocks
        blocks = []
        raw_lines = section_text.splitlines(keepends=True)
        curr_block = ""
        for line in raw_lines:
            curr_block += line
            if not line.strip(): # Blank line marks end of block
                blocks.append(curr_block)
                curr_block = ""
        if curr_block:
            blocks.append(curr_block)

        curr_chunk_text, curr_chunk_words = "", 0
        chunk_idx = 0
        j = 0
        while j < len(blocks):
            block = blocks[j]
            block_words = len(block.split())

            # If block itself is huge (e.g. a big table), we might have to split it anyway
            # but the requirement says "Never split inside: bullet lists... tables"
            # so we'll keep it together unless it's insane.

            if curr_chunk_words + block_words > 1200 and curr_chunk_words >= 800:
                # Finalize current chunk
                chunk = create_chunk(chunk_idx, section, curr_chunk_text, curr_start_off, curr_start_off + len(curr_chunk_text), chapter_title, chapter_id, subsection_path)
                chunks.append(chunk)
                chunk_idx += 1

                # Overlap: backtrack some blocks if possible
                overlap_text, overlap_words = "", 0
                k = j - 1
                while k >= 0 and overlap_words < 150:
                    overlap_text = blocks[k] + overlap_text
                    overlap_words += len(blocks[k].split())
                    k -= 1

                curr_start_off = (curr_start_off + len(curr_chunk_text)) - len(overlap_text)
                curr_chunk_text, curr_chunk_words = overlap_text, overlap_words

            curr_chunk_text += block
            curr_chunk_words += block_words
            j += 1

        if curr_chunk_text.strip():
            # If this is the last chunk and it's tiny, maybe merge it?
            # But the requirement is about tiny SECTIONS.
            chunks.append(create_chunk(chunk_idx, section, curr_chunk_text, curr_start_off, curr_start_off + len(curr_chunk_text), chapter_title, chapter_id, subsection_path))

    for i, chunk in enumerate(chunks):
        chunk['chunk_id'] = f"NELSON_{i+1:06d}"
    return chunks

def main():
    text = load_all_text()
    if not text: return
    toc = parse_headings(text)
    chunks = chunk_sections(text, toc)

    with open('nelson_chunks.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'chunk_id', 'chapter_title', 'chapter_id', 'section_title', 'section_id',
            'subsection_path', 'start_offset', 'end_offset', 'chunk_index_in_section',
            'token_estimate', 'text', 'keywords', 'entities_json'
        ])
        writer.writeheader()
        writer.writerows(chunks)

    with open('nelson_toc.json', 'w', encoding='utf-8') as f:
        json.dump(toc, f, indent=2)

    chapter_counts = {}
    for c in chunks: chapter_counts[c['chapter_title']] = chapter_counts.get(c['chapter_title'], 0) + 1
    token_estimates = [c['token_estimate'] for c in chunks]
    manifest = {
        'total_chars': len(text),
        'total_chunks': len(chunks),
        'avg_token_estimate': sum(token_estimates)/len(chunks) if chunks else 0,
        'min_chunk_size': min(token_estimates) if chunks else 0,
        'max_chunk_size': max(token_estimates) if chunks else 0,
        'counts_per_chapter': chapter_counts,
        'warnings': [f"Chunk {c['chunk_id']} oversized: {c['token_estimate']}" for c in chunks if c['token_estimate'] > 1600]
    }
    with open('nelson_manifest.json', 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)

if __name__ == "__main__":
    main()
