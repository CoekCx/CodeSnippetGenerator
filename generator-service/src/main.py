import os

from prompt_toolkit.shortcuts import button_dialog

from cli import blog_generator_cli, image_generator_cli
from config.constants import menu_text
from config.prompts import style


def run_blog_generator():
    # subprocess.run(["python", "cli/blog_generator_cli.py"])
    blog_generator_cli.main()


def run_image_generator():
    # subprocess.run(["python", "cli/image_generator_cli.py"])
    image_generator_cli.main()


def main():
    choice_map = {
        "Blog Generator": run_blog_generator,
        "Image Generator": run_image_generator,
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
