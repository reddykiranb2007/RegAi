import os

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

def generate_html(tree, current_path, indent=0):
    html = ""
    for k, v in sorted(tree.items(), key=lambda t: (t[1] is None, t[0])):
        if v is None:
            html += f'<li>📄 {k}</li>\n'
        else:
            html += f'<li class="folder">📁 <strong>{k}</strong><ul>\n'
            child_path = os.path.join(current_path, k) if current_path else k
            html += generate_html(v, child_path, indent + 1)
            html += '</ul></li>\n'
    return html

html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>ORIGINAL_DOC Folder Structure</title>
    <style>
        body { font-family: Arial, sans-serif; font-size: 14px; line-height: 1.5; color: #333; margin: 40px; }
        h1 { color: #2c3e50; border-bottom: 2px solid #eee; padding-bottom: 10px; }
        ul { list-style-type: none; padding-left: 20px; }
        .folder { margin-top: 5px; margin-bottom: 5px; }
    </style>
</head>
<body>
    <h1>ORIGINAL_DOC Folder Structure</h1>
    <ul>
        <li class="folder">📁 <strong>ORIGINAL_DOC</strong>
            <ul>
"""
html_content += generate_html(tree, "")
html_content += """
            </ul>
        </li>
    </ul>
</body>
</html>
"""

with open("ORIGINAL_DOC_Structure_print.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("HTML generated.")
