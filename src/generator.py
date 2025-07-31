import os
from pathlib import Path
from md_blocks import markdown_to_html_node

# Recursively process all markdown files in a directory tree
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            # Convert .md files to .html
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, basepath)
        else:
            # Recursively process subdirectories
            generate_pages_recursive(from_path, template_path, dest_path, basepath)


# Convert a single markdown file to HTML using the template
def generate_page(from_path, template_path, dest_path, basepath):
    print(f" * {from_path} {template_path} -> {dest_path}")
    # Read markdown source
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    # Read HTML template
    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    # Convert markdown to HTML
    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    # Extract title and perform template substitutions
    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    # Fix relative URLs for deployment to subdirectories
    template = template.replace('href="/', 'href="' + basepath)
    template = template.replace('src="/', 'src="' + basepath)

    # Create output directory if needed and write HTML file
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)


# Extract the first H1 heading to use as the page title
def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]  # Remove the "# " prefix
    raise ValueError("no title found")
