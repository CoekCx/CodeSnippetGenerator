import os

from config.constants import menu_text
from config.prompts import (
    prompt_for_folder,
    print_success,
    open_folder_in_explorer,
    prompt_for_file,
    prompt_for_code_snippet,
    prompt_for_title,
)
from config.prompts import style
from core.code_classifier import parse_code
from generators.html_generator import HtmlGenerator
from prompt_toolkit.shortcuts import button_dialog
from utils.file_handler import FileHandler


# current_working_directory = os.getcwd()
# new_working_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(f"Current working directory: {current_working_directory}")
# print(f"New working directory:     {new_working_directory}")
# input()
# os.chdir(new_working_directory)
# try:
#     from ..config.constants import menu_text
# except Exception as e:
#     print(e)
#     input("Press enter to exit.")


def generate_html_file(file_name: str, folder_path: str) -> None:
    """
    Generates an HTML file from a code file with syntax highlighting.
    
    Args:
        file_name (str): The name of the code file to process
        folder_path (str): The directory path where the file is located
        
    Returns:
        None: The function writes the HTML file to disk
    """
    if not file_name or not folder_path:
        print("File name or folder path is not valid.")
        input()
        return

    os.system("cls")
    print_success(f"Generating {file_name}.\n\n")

    file_path = f"{folder_path}/{file_name}"
    html_file_path = os.path.splitext(file_path)[0] + ".html"

    code_snippet = FileHandler.read_file(file_path)
    if not code_snippet:
        return

    title = "csharp" if file_name.endswith(".cs") else "json"
    token_classifications = parse_code(code_snippet)
    html_code = HtmlGenerator.generate_blog_html_file_content(code_snippet, token_classifications, title)

    with open(html_file_path, "w") as html_file:
        html_file.write(html_code)


def generate_html_from_manual_input() -> None:
    """
    Generates an HTML file from manually entered code snippet.
    """
    code_snippet, file_name, folder_path = prompt_for_code_snippet()
    title = prompt_for_title()

    token_classifications = parse_code(code_snippet)
    html_code = HtmlGenerator.generate_blog_html_file_content(code_snippet, token_classifications, title)

    FileHandler.save_file(file_name, folder_path, html_code)
    open_folder_in_explorer(folder_path)


def generate_html_from_file(preset_folder: str | None = None) -> None:
    """
    Prompts user to select a code file, generates an HTML version with syntax highlighting,
    and opens the target folder after completion.
    
    This function displays the result in the console for verification before opening
    the folder where the HTML file was created.
    
    Args:
        preset_folder (str | None, optional): The initial directory to open 
            the file dialog in. If None, uses the default directory.
            
    Returns:
        None: Generates an HTML file and opens the containing folder
    """
    file_name, folder_path = prompt_for_file(preset_folder)

    generate_html_file(file_name, folder_path)
    input()

    os.system("cls")
    print_success(f"Html file successfully generated!")
    open_folder_in_explorer(folder_path)


def generate_htmls_from_folder(preset_folder: str | None = None) -> None:
    """
    Batch converts all supported code files in a folder to HTML with syntax highlighting.
    
    Processes all .cs and .json files in the selected folder, generating corresponding
    HTML files in the same location. Displays completion status for each file and
    opens the folder upon completion.
    
    Args:
        preset_folder (str | None, optional): The initial directory to use.
            If None, prompts user to select a folder.
            
    Returns:
        None: Generates HTML files and opens the containing folder
    """
    folder_path = preset_folder or prompt_for_folder()

    if folder_path:
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".cs") or file_name.endswith(".json"):
                generate_html_file(file_name, folder_path)
                input()

        os.system("cls")
        print_success(f"Html files successfully generated!")
        open_folder_in_explorer(folder_path)


def main():
    choice_map = {
        "blog_file": lambda: generate_html_from_file(FileHandler.get_latest_blog_folder()),
        "blog_folder": lambda: generate_htmls_from_folder(FileHandler.get_latest_blog_folder()),
        "custom_snippet": generate_html_from_manual_input,
        "custom_file": lambda: generate_html_from_file(),
        "custom_folder": lambda: generate_htmls_from_folder(),
        "exit": exit,
    }

    while True:
        choice = button_dialog(
            title="HTML Generator",
            text=menu_text,
            buttons=[
                ("Blog File\n", "blog_file"),
                ("Blog Folder\n", "blog_folder"),
                ("Snippet\n", "custom_snippet"),
                ("File\n", "custom_file"),
                ("Folder\n", "custom_folder"),
                ("Exit", "exit"),
            ],
            style=style,
        ).run()

        if choice in choice_map:
            if choice == "exit":
                return

            os.system("cls")
            choice_map[choice]()
        else:
            os.system("cls")
            print("Invalid option. Try again.")


if __name__ == "__main__":
    # Change working directory to the src folder (parent directory)

    try:
        main()
    except Exception as e:
        print(e)
        input("Press enter to exit.")
