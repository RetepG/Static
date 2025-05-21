from textnode import TextNode, TextType
import os
import shutil
from block_mardown import generate_page

def main():
    textnode = TextNode("This is some anchor text", TextType.LINKS, "https://www.boot.dev")
    print(textnode)
    copy_static_to_public()

    generate_page(
        from_path="content/index.md",
        template_path="template.html",
        dest_path="public/index.html"
    )
    print("Site generation complete!")

def copy_static_to_public(src='static', dst='public'):
    """
    Recursively copies contents from the source directory to the destination directory.
    If the destination directory exists, it is deleted before copying.
    """
    #Delete the destination directory if it exists
    if os.path.exists(dst):
        shutil.rmtree(dst)
        print(f"Deleted existing directory: {dst}")

    #Start the recursive copying process
    def recursive_copy(source_path, destination_path):
        # Create the destination directory if it doesn't exist
        os.makedirs(destination_path, exist_ok=True)
        print(f"Created directory: {destination_path}")

        # Iterate over all items in the source directory
        for item in os.listdir(source_path):
            src_item = os.path.join(source_path, item)
            dst_item = os.path.join(destination_path, item)

            if os.path.isdir(src_item):
                # If the item is a directory, recurse into it
                recursive_copy(src_item, dst_item)
            else:
                # If the item is a file, copy it
                shutil.copy2(src_item, dst_item)
                print(f"Copied file: {src_item} to {dst_item}")

    # Initiate the recursive copying from the source to the destination
    recursive_copy(src, dst)

if __name__ == "__main__":
    main()