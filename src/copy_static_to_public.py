import os
from block_mardown import generate_page

def copy_static_to_public(content_dir, output_dir):
    """
    Recursively processes all markdown files in content_dir and its subdirectories.
    Generates HTML pages for each markdown file.
    """
    for root, _, files in os.walk(content_dir):
        for file in files:
            if file.endswith(".md"):
                # Get the full path of the markdown file
                md_path = os.path.join(root, file)
                
                # Calculate the relative path from content_dir
                rel_path = os.path.relpath(root, content_dir)
                
                # Calculate the destination path
                if rel_path == ".":  # This is for files directly in the content directory
                    dest_dir = output_dir
                else:
                    dest_dir = os.path.join(output_dir, rel_path)
                
                # Create destination directory if it doesn't exist
                os.makedirs(dest_dir, exist_ok=True)
                
                # Generate the HTML page
                dest_path = os.path.join(dest_dir, file.replace(".md", ".html"))
                generate_page(
                    from_path=md_path,
                    template_path="template.html",
                    dest_path=dest_path
                )
                print(f"Generated HTML: {dest_path}")