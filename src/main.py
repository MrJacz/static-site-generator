import os
import shutil
import sys

from copystatic import copy_files_recursive
from generator import generate_pages_recursive

# Directory configuration - using docs/ as output for GitHub Pages compatibility
dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"
default_basepath = "/"


def main():
    # Allow custom base path for deployment (e.g., "/my-site/" for subdirectory hosting)
    basepath = default_basepath
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    # Clean slate: remove existing output directory
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    # Copy static assets (CSS, images, etc.) before generating HTML
    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    # Convert all markdown files to HTML using the template
    print("Generating content...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public, basepath)


main()
