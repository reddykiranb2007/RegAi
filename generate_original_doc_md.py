import os
import urllib.parse

root_dir = "ORIGINAL_DOC"
base_path = os.path.abspath(root_dir)

def build_tree(path):
    tree = {}
    try:
        entries = os.listdir(path)
    except Exception:
        return tree
    
    dirs = []
    files = []
    for entry in entries:
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            dirs.append((entry, full_path))
        else:
            files.append(entry)
            
    for d, p in sorted(dirs):
        tree[d] = build_tree(p)
    for f in sorted(files):
        tree[f] = None
    return tree

tree = build_tree(base_path)

def generate_markdown(tree, current_path, indent=0):
    md = ""
    prefix = "    " * indent
    for k, v in sorted(tree.items(), key=lambda t: (t[1] is None, t[0])):
        if v is None:
            # File
            url_path = urllib.parse.quote(current_path.replace("\\", "/"))
            md += f"{prefix}- [{k}](./ORIGINAL_DOC/{url_path}/{urllib.parse.quote(k)})\n"
        else:
            # Folder
            md += f"{prefix}- **{k}**\n"
            child_path = os.path.join(current_path, k) if current_path else k
            md += generate_markdown(v, child_path, indent + 1)
    return md

md_content = "# ORIGINAL_DOC Folder Structure\n\nThis document provides a hierarchical view of the folders and files within the `ORIGINAL_DOC` directory.\n\n- **ORIGINAL_DOC**\n"
md_content += generate_markdown(tree, "", 1)

with open("ORIGINAL_DOC_Structure.md", "w", encoding="utf-8") as f:
    f.write(md_content)

print("Markdown generated successfully.")
