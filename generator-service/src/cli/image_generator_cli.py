"""
DEPRECATED: This file is no longer in use and will be removed in a future version.
"""

import os
import threading
import warnings
from http.server import SimpleHTTPRequestHandler, HTTPServer

from config.constants import menu_text
from config.prompts import (
    prompt_for_code_snippet,
    prompt_for_file,
    prompt_for_folder,
    print_success,
    open_folder_in_explorer,
    style,
)
from core.code_classifier import parse_code
from generators.html_generator import HtmlGenerator
from generators.image_generator import generate_image_with_selenium
from prompt_toolkit.shortcuts import button_dialog
from utils.file_handler import FileHandler

warnings.warn(
    "The module 'image_generator' is deprecated and will be removed in a future version.",
    DeprecationWarning,
    stacklevel=2
)


# Function to run the HTTP server
def run_server():
    """
    Starts a simple HTTP server, on port 55003, that serves files from the current
    directory. The server runs indefinitely until manually terminated.
    
    Returns:
        None: The function blocks while the server is running
    """
    port = 55003
    handler = SimpleHTTPRequestHandler
    with HTTPServer(("", port), handler) as httpd:
        print(f"Server started at port {port}")
        httpd.serve_forever()


def generate_image_logic(code_snippet: str, img_name: str, img_path: str):
    """
    Generates an image from a code snippet.
    
    Args:
        code_snippet (str): The source code to convert to an image
        img_name (str): The filename for the output image (without extension)
        img_path (str): The directory path where the image will be saved
        
    Returns:
        None: The function generates an image file on disk
    """
    token_classifications = parse_code(code_snippet)
    html_code = HtmlGenerator.generate_code_snippets_image_html(code_snippet, token_classifications)

    temp_html_path = FileHandler.save_file(html_code, "temp", "resources", "html")
    generate_image_with_selenium(temp_html_path, f"{img_path}/{img_name}")
    os.remove(temp_html_path)


def generate_image_from_manual_input():
    """
    Generates an image from a manually entered code snippet. It also saves
    the original code snippet as a .cs file in the same location.
    
    Returns:
        None: The function generates files on disk and opens the folder
    """
    code_snippet, img_name, post_folder_path = prompt_for_code_snippet()

    generate_image_logic(code_snippet, img_name, f"{post_folder_path}/Codes")
    FileHandler.save_file(code_snippet, img_name, f"{post_folder_path}/Codes", "cs")
    open_folder_in_explorer(post_folder_path)


def generate_image_from_file(preset_folder=None):
    """
    Prompts user to select a code file and generates an image from it.
    
    Args:
        preset_folder (str | None, optional): The initial directory to open 
            the file dialog in. If None, uses the default directory.
            
    Returns:
        None: Generates an image file and opens the containing folder
    """
    file_name, file_path = prompt_for_file(preset_folder)
    os.system("cls")
    print_success(f"Generating {file_name}.\n\n")

    file_path = f"{file_path}/{file_name}"
    code_snippet = FileHandler.read_file(file_path)
    if not code_snippet:
        return

    generate_image_logic(code_snippet, file_name, file_path)

    os.system("cls")
    print_success(f"Image successfully generated!")
    open_folder_in_explorer(os.path.split(file_path)[0] + "/Images")


def generate_images_from_folder(preset_folder=None):
    """
    Batch converts all supported code files in a folder to images with syntax highlighting.
    
    Args:
        preset_folder (str | None, optional): The initial directory to use.
            If None, prompts user to select a folder.
            
    Returns:
        None: Generates image files and opens the containing folder
    """
    folder_path = preset_folder or prompt_for_folder()

    if folder_path:
        for file_name in os.listdir(folder_path):
            if (
                    file_name.endswith(".cs") or
                    file_name.endswith(".txt") or
                    file_name.endswith(".json")
            ):
                os.system("cls")
                print_success(f"Generating {file_name}.\n\n")

                file_path = f"{folder_path}/{file_name}"
                code_snippet = FileHandler.read_file(file_path)
                if not code_snippet:
                    continue

                generate_image_logic(code_snippet, file_name, folder_path)

        os.system("cls")
        print_success(f"Images successfully generated!")
        open_folder_in_explorer(os.path.split(folder_path)[0] + "/Images")


def main():
    # Start the HTTP server in a separate thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    while True:
        choice = button_dialog(
            title="Image Generator",
            text=menu_text,
            buttons=[
                ("Post File\n", "latest_post_file"),
                ("Post Folder\n", "latest_post_folder"),
                ("Blog File\n", "latest_blog_file"),
                ("Blog Folder\n", "latest_blog_folder"),
                ("Custom Snippet\n", "custom_snippet"),
                ("Custom File\n", "custom_file"),
                ("Custom Folder\n", "custom_folder"),
                ("Exit", "exit"),
            ],
            style=style,
        ).run()

        os.system("cls")

        if choice == "exit":
            return
        elif choice == "latest_post_file":
            generate_image_from_file(FileHandler.get_latest_post_folder())
        elif choice == "latest_post_folder":
            generate_images_from_folder(FileHandler.get_latest_post_folder())
        elif choice == "latest_blog_file":
            generate_image_from_file(FileHandler.get_latest_blog_folder())
        elif choice == "latest_blog_folder":
            generate_images_from_folder(FileHandler.get_latest_blog_folder())
        elif choice == "custom_snippet":
            generate_image_from_manual_input()
        elif choice == "custom_file":
            generate_image_from_file()
        elif choice == "custom_folder":
            generate_images_from_folder()
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
