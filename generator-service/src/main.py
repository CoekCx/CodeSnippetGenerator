import os

from prompt_toolkit.shortcuts import button_dialog

from cli import blog_generator_cli, image_generator_cli
from config.constants import menu_text
from config.prompts import style


def main():
    choice_map = {
        "Blog Generator": blog_generator_cli.main,
        "Image Generator": image_generator_cli.main,
        "Exit": exit,
    }

    while True:
        choice = button_dialog(
            title="Code Snippet Generator",
            text=menu_text,
            buttons=[
                ("Blog\n", "Blog Generator"),
                ("Image\n", "Image Generator"),
                ("Exit", "Exit"),
            ],
            style=style,
        ).run()

        if choice in choice_map:
            os.system("cls")
            choice_map[choice]()
        else:
            os.system("cls")
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
