import os
from tkinter import filedialog, Tk

from blessed import Terminal
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import input_dialog
from prompt_toolkit.styles import Style

from config.constants import TOKEN_COLORS_ANSI

style = Style.from_dict(
    {
        "dialog": "bg:#111111",
        "dialog frame.label": "bg:#111111 #f5f5f5",
        "dialog.body": "bg:#1d1f20 #f6bb00",
        "dialog shadow": "bg:#000000",
        "text-area": "bg:#1d1f20",
        "button.focused": "bg:#111111",
    }
)


def prompt_for_code_snippet() -> tuple[str, str, str]:
    """
    Prompts the user to enter a code snippet and specify save location.
    
    Returns:
        tuple: A tuple containing:
            - code_snippet (str): The user-entered code snippet
            - file_name (str): The filename for the output image (without extension)
            - folder_path (str): The directory path where the image will be saved
    """
    os.system("cls")
    code_snippet = prompt(
        "Enter your C# code snippet:\n",
        multiline=True,
    )

    # Get the image save path
    os.system("cls")
    file_name = input_dialog(
        title="Code Snippet Generator",
        text="Enter the file name (without extension):\n",
        style=style,
    ).run()
    folder_path = prompt_for_folder()

    return code_snippet, file_name, folder_path


def prompt_for_title() -> str:
    """
    Prompts the user to enter a title for the code snippet.
    
    Returns:
        str: The user-entered title
    """
    os.system("cls")
    return input_dialog(
        title="Code Snippet Generator",
        text="Enter title:\n",
        style=style,
    ).run()


def prompt_for_file(preset_folder: str | None = None) -> tuple[str, str] | tuple[None, None]:
    """
    Prompts the user to select a file from a file dialog.
    
    Args:
        preset_folder (str, optional): The initial directory to open the file dialog in.
    
    Returns:
        tuple: A tuple containing:
            - file_name (str): The filename of the selected file
            - folder_path (str): The directory path where the file is located
    """
    Tk().withdraw()  # Hide root window
    file_path = filedialog.askopenfilename(
        initialdir=preset_folder,
        filetypes=[
            ("C# Files", "*.cs"),
            ("Text Files", "*.txt"),
            ("Json Files", "*.json"),
        ]
    )

    if file_path:
        folder_path, file_name = os.path.split(file_path)
        return file_name, folder_path

    return None, None


def prompt_for_folder() -> str:
    """
    Prompts the user to select a folder from a directory dialog.
    
    Returns:
        str: The selected directory path
    """
    Tk().withdraw()  # Hide root window
    folder_path = filedialog.askdirectory()

    return folder_path


def print_success(msg: str) -> None:
    """
    Prints a success message in a colored format.
    
    Args:
        msg (str): The message to print
    """
    terminal = Terminal()
    color = TOKEN_COLORS_ANSI.get("comment", TOKEN_COLORS_ANSI["default"])
    print(terminal.color(color)(msg))


def open_folder_in_explorer(folder_path: str) -> None:
    """
    Opens the specified folder in the file explorer.
    
    Args:
        folder_path (str): The path to the folder to open
    """
    os.startfile(folder_path)
