import json
import re
import math
import sys
import os

try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
except ImportError:
    print("Error: sentence-transformers or numpy not installed.")
    print("Please install via: pip install sentence-transformers numpy")
    sys.exit(1)

def normalize_text(text):
    if not text:
        return ""
    # Lowercase, strip
    text = text.lower().strip()
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove common punctuation if needed, but keeping for semantic meaning is usually fine.
    # User asked for "strict normalization".
    return text

def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Strip JS assignment
    # match "const extractedDeviceDatabase = { ... };"
    match = re.search(r'const\s+extractedDeviceDatabase\s*=\s*(\{.*\});', content, re.DOTALL)
    if not match:
        print("Could not extract JSON object from file.")
        sys.exit(1)
        
    json_str = match.group(1)
    try:
        data = json.loads(json_str)
        return data
    except json.JSONDecodeError as e:
        print(f"JSON Parsing failed: {e}")
        # Fallback: maybe trailing commas? standard json doesn't like them.
        # But looking at file view, it seems standard.
        sys.exit(1)

def main():
    input_file = r'd:\RegAi\device_data.js'
    output_file = r'd:\RegAi\device_data_embedded.js'
    
    print(f"Loading data from {input_file}...")
    data_map = load_data(input_file)
    print(f"Loaded {len(data_map)} items.")
    
    print("Loading model all-MiniLM-L6-v2...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    output_list = []
    
    print("Generating embeddings...")
    count = 0
    skipped = 0
    
    # Convert Object to Array and Embed
    # keys are usually normalized names, values are objects
    for key, item in data_map.items():
        name = item.get('originalName', '')
        use = item.get('use', '')
        
        # Prepare text
        norm_name = normalize_text(name)
        norm_use = normalize_text(use)
        
        text_to_embed = f"{norm_name} {norm_use}"
        
        if not text_to_embed.strip():
            print(f"Skipping empty item: {key}")
            skipped += 1
            continue
            
        # Embed
        embedding = model.encode(text_to_embed)
        
        # Check NaN
        if np.isnan(embedding).any():
            print(f"Warning: NaN found in embedding for {name}. Skipping.")
            skipped += 1
            continue
            
        # Convert to list for JSON serialization
        # Rounding to reduce file size (optional but good practice)
        # keeping precision for now, but maybe 5-6 decimals is enough.
        # JSON float precision usually handles it.
        embed_list = embedding.tolist()
        
        # Construct new item
        new_item = item.copy()
        new_item['embedding'] = embed_list
        # Id could be useful if not present, but originalName is unique-ish.
        
        output_list.append(new_item)
        count += 1
        
        if count % 100 == 0:
            print(f"Processed {count} items...")

    print(f"Finished. Total: {count}, Skipped: {skipped}")
    
    print(f"Saving to {output_file}...")
    
    # Write as JS const
    with open(output_file, 'w', encoding='utf-8') as f:
        json_content = json.dumps(output_list, indent=None) # Compact
        f.write(f"const extractedDeviceDatabase = {json_content};")
        
    print("Done.")

if __name__ == "__main__":
    main()
