import os

from prompt_toolkit.shortcuts import button_dialog

from cli.benchmark_cli import process_benchmark_table
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
from generators.benchmark_html_generator import BenchmarkHtmlGenerator
from generators.html_generator import HtmlGenerator
from utils.file_handler import FileHandler


def generate_image_logic(code_snippet: str, file_name: str, code_path: str):
    """
    Generates an image from a code snippet or benchmark results.
    
    Args:
        code_snippet (str): The source code to convert to an image
        file_name (str): The file name (without extension)
        code_path (str): The directory path where the code file is stored at
        
    Returns:
        None: The function generates an image file on disk
    """
    if file_name.endswith('.txt'):
        benchmark_table = process_benchmark_table(code_snippet)
        html_code = BenchmarkHtmlGenerator.generate_benchmark_html(benchmark_table)
    else:
        token_classifications = parse_code(code_snippet)
        html_code = HtmlGenerator.generate_code_snippets_image_html(code_snippet, token_classifications)

    image_file_destination = FileHandler.convert_code_to_image_destination(code_path)
    HtmlGenerator.render_code_snippet_image(html_code, image_file_destination, file_name)


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
    file_name, folder_path = prompt_for_file(preset_folder)
    os.system("cls")
    print_success(f"Generating {file_name}.\n\n")

    file_path = f"{folder_path}/{file_name}"
    code_snippet = FileHandler.read_file(file_path)
    if not code_snippet:
        return

    generate_image_logic(code_snippet, file_name, folder_path.replace("/", "\\"))

    os.system("cls")
    print_success(f"Image successfully generated!")
    open_folder_in_explorer(os.path.split(folder_path)[0] + "/Images")


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
