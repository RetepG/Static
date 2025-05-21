from textnode import TextNode, TextType
import os
import shutil
from block_mardown import generate_page
from copy_static_to_public import copy_static_to_public

dir_path_public = "./public"
dir_path_content = "./content"

def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    #look for content make public
    copy_static_to_public("content", "public")

    generate_page(
        from_path="content/index.md",
        template_path="template.html",
        dest_path="public/index.html"
    )
    print("Site generation complete!")

if __name__ == "__main__":
    main()