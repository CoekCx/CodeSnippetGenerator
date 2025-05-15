import os

from dotenv import load_dotenv, set_key
from prompt_toolkit.shortcuts import button_dialog

from config.prompts import style, print_success
from config.syntax_presets import SyntaxPresets


def update_env_file(preset_name: str) -> None:
    """
    Updates the SYNTAX_PRESET value in the .env file.
    
    Args:
        preset_name (str): The name of the syntax preset to set
    """
    dotenv_path = os.path.join(os.getcwd(), '.env')
    if not os.path.exists(dotenv_path):
        parent_dotenv_path = os.path.join(os.path.dirname(os.getcwd()), '.env')
        if os.path.exists(parent_dotenv_path):
            dotenv_path = parent_dotenv_path

    load_dotenv(dotenv_path)
    set_key(dotenv_path, "SYNTAX_PRESET", preset_name)


def main():
    """
    Displays a dialog for selecting the syntax highlighting preset and updates the settings.
    The selected preset will be used for all code snippet generation.
    """
    preset_buttons = [
                         (f"{preset.name}\n", preset.name) for preset in SyntaxPresets
                     ] + [("Exit", "exit")]

    choice = button_dialog(
        title="Syntax Preset Configuration",
        text="Select the syntax highlighting preset to use:",
        buttons=preset_buttons,
        style=style,
    ).run()

    os.system("cls")

    if choice == "exit":
        return

    update_env_file(choice)
    print_success(f"Syntax preset set to {choice}!")


if __name__ == "__main__":
    main()
