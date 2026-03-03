import os
import urllib.parse

root_dir = "03_MASTER PROCEDURES"
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

html_template = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>MASTER PROCEDURES - Help System</title>
<style>
    body { font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; display: flex; height: 100vh; overflow: hidden; background-color: #f5f5f5; }
    #sidebar { width: 350px; background: #ffffff; border-right: 1px solid #ccc; display: flex; flex-direction: column; }
    #sidebar-header { background: #005a9e; color: white; padding: 15px; font-size: 16px; font-weight: bold; display: flex; align-items: center; }
    #sidebar-header::before { content: "📚"; margin-right: 8px; font-size: 20px; }
    #tree-container { flex: 1; overflow-y: auto; padding: 10px; font-size: 14px; }
    #content-pane { flex: 1; display: flex; flex-direction: column; background: #fff; }
    #content-header { background: #f0f0f0; padding: 12px 20px; border-bottom: 1px solid #ccc; font-weight: bold; color: #333; font-size: 18px; }
    #iframe-container { flex: 1; display: flex; flex-direction: column; }
    iframe { width: 100%; flex: 1; border: none; }
    
    ul.tree { list-style-type: none; padding-left: 17px; margin: 0; }
    ul.tree.root { padding-left: 0; }
    ul.tree li { margin: 2px 0; position: relative; }
    .node { cursor: pointer; user-select: none; display: flex; align-items: flex-start; padding: 4px 6px; border-radius: 3px; line-height: 1.4; }
    .node:hover { background-color: #e5f3ff; }
    .node.active { background-color: #cce8ff; border: 1px solid #99d1ff; padding: 3px 5px; }
    .icon { display: inline-block; width: 16px; height: 16px; margin-right: 6px; text-align: center; font-size: 14px; flex-shrink: 0; }
    .folder-icon { color: #dcb67a; }
    .file-icon { color: #555; }
    .caret { cursor: pointer; display: inline-block; width: 16px; height: 16px; font-size: 10px; color: #555; text-align: center; line-height: 16px; flex-shrink: 0; }
    .caret::before { content: "▶"; }
    .caret-down::before { content: "▼"; }
    .nocaret { display: inline-block; width: 16px; flex-shrink: 0; }
    .nested { display: none; }
    .active-nested { display: block; }
    .node-text { word-break: break-word; }
    
    /* Welcome screen */
    #welcome { padding: 40px; text-align: center; color: #666; margin: auto; max-width: 600px; }
    #welcome h2 { color: #005a9e; font-size: 28px; margin-bottom: 20px; }
    #welcome p { font-size: 16px; margin-bottom: 15px; }
    .help-icon { font-size: 64px; color: #005a9e; margin-bottom: 20px; }
</style>
</head>
<body>

<div id="sidebar">
    <div id="sidebar-header">Contents</div>
    <div id="tree-container">
        {tree_html}
    </div>
</div>

<div id="content-pane">
    <div id="content-header">Welcome</div>
    <div id="iframe-container">
        <div id="welcome">
            <div class="help-icon">📖</div>
            <h2>MASTER PROCEDURES Help System</h2>
            <p>Select a document from the table of contents on the left pane to view it.</p>
            <p>Note: Supported files (like PDFs or text files) will be previewed directly in this window. For Word or Excel files, clicking the link may prompt your browser to download and open them in their native applications.</p>
        </div>
        <iframe id="viewer" src="about:blank" style="display:none;"></iframe>
    </div>
</div>

<script>
    var toggler = document.getElementsByClassName("caret");
    for (var i = 0; i < toggler.length; i++) {
        toggler[i].addEventListener("click", function(e) {
            e.stopPropagation();
            this.parentElement.parentElement.querySelector(".nested").classList.toggle("active-nested");
            this.classList.toggle("caret-down");
        });
    }

    var nodes = document.getElementsByClassName("node");
    for (var i = 0; i < nodes.length; i++) {
        nodes[i].addEventListener("click", function(e) {
            var isFolder = this.hasAttribute('data-folder');
            
            // Highlight node selection
            for(var j=0; j<nodes.length; j++) nodes[j].classList.remove("active");
            this.classList.add("active");
            
            if(isFolder) {
                // Clicking a folder toggles it
                var caret = this.querySelector('.caret');
                if(caret && e.target !== caret) {
                    caret.click();
                }
            } else {
                // Clicking a file opens it
                var path = this.getAttribute('data-path');
                var name = this.getAttribute('data-name');
                document.getElementById('content-header').innerText = name;
                document.getElementById('welcome').style.display = 'none';
                var iframe = document.getElementById('viewer');
                iframe.style.display = 'block';
                iframe.src = path;
            }
        });
    }
</script>

</body>
</html>
"""

def generate_html_node(name, content, current_path):
    if content is None:
        # File
        url_path = urllib.parse.quote(current_path.replace("\\", "/"))
        return f'<li><div class="node" data-path="{url_path}" data-name="{name}"><span class="nocaret"></span><span class="icon file-icon">📄</span><span class="node-text">{name}</span></div></li>'
    else:
        # Folder
        html = f'<li><div class="node" data-folder="true"><span class="caret"></span><span class="icon folder-icon">📁</span><span class="node-text">{name}</span></div>'
        html += '<ul class="nested">'
        for k, v in content.items():
            child_path = os.path.join(current_path, k)
            html += generate_html_node(k, v, child_path)
        html += '</ul></li>'
        return html

tree_html = '<ul class="tree root">'
for k, v in tree.items():
    tree_html += generate_html_node(k, v, os.path.join("03_MASTER PROCEDURES", k))
tree_html += '</ul>'

final_html = html_template.replace("{tree_html}", tree_html)

with open("03_MASTER_PROCEDURES_Help.html", "w", encoding="utf-8") as f:
    f.write(final_html)

print("HTML Help file generated successfully.")
