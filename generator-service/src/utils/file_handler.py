import os
import re
import shutil
from pathlib import Path
from typing import Optional

from config.prompts import print_success
from config.settings import Settings


class FileHandler:
    """
    A utility class for handling file operations.
    """

    @staticmethod
    def get_latest_post_folder() -> Optional[str]:
        """
        Get the latest LinkedIn post folder from the given base path.
        
        Returns:
            Optional[str]: Path to the Code directory in the latest post folder,
                          or None if no post folders are found
        """
        base_path = Settings.load().linkedin_posts_path
        folders = [f for f in os.listdir(base_path) if f.startswith("Post ")]
        if not folders:
            return None

        post_numbers = [(int(re.search(r"Post (\d+)", f).group(1)), f) for f in folders]
        latest_folder = max(post_numbers, key=lambda x: x[0])[1]
        return os.path.join(base_path, latest_folder, "Code")

    @staticmethod
    def get_latest_blog_folder(base_path: Path | None = None) -> str | None:
        """
        Get the latest blog folder from the given base path.

        Args:
            base_path (Path): The base path to search for blog folders

        Returns:
            Optional[Path]: The latest blog folder or None if no folders are found
        """
        if base_path is None:
            base_path = Settings.load().blog_posts_path

        folders = [f for f in os.listdir(base_path) if f.startswith("Blog Post ")]
        if not folders:
            return None

        blog_numbers = []
        for f in folders:
            match = re.search(r"Blog Post (\d+)", f)
            if match:
                blog_numbers.append((int(match.group(1)), f))

        if not blog_numbers:
            return None

        latest_folder = max(blog_numbers, key=lambda x: x[0])[1]
        return os.path.join(base_path, latest_folder, "Code")

    @staticmethod
    def save_file(contents: str, file_name: str, folder_path: str, file_extension: str | None = "") -> str:
        """
        Saves a code snippet to a file in the specified folder.

        Args:
            contents (str): The file contents
            file_name (str): The name of the file to save the code to
            folder_path (str): The path to the folder where the file will be saved
            file_extension (str | None): The extension of the file to save the code to

        Returns:
            str: The file path of the saved file
        """
        os.system("cls")
        print_success(f"Generating {file_name}.\n\n")

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        if not file_extension and not file_name.endswith(file_extension):
            file_name += f".{file_extension}"

        file_path = f"{folder_path}/{file_name}"
        with open(file_path, "w") as file:
            file.write(contents)

        print_success(f"File saved to {file_path}")
        return file_path

    @staticmethod
    def read_file(file_path: str) -> str | None:
        """
        Args:
            file_path (str): The path to the file

        Returns:
            str: The contents of the file
            None: If the file does not exist
        """
        if not os.path.exists(file_path):
            print(f"File does not exist: {file_path}")
            input()
            return None

        with open(file_path, "r") as file:
            return file.read()

    @staticmethod
    def move_image(img_name: str, img_path: str = "") -> str:
        """
        Moves an image file to a specified destination folder.

        Args:
            img_name (str): The name of the image file to move
            img_path (str, optional): The path to the image file. 
                Defaults to an empty string.
                
        Returns:
            str: The path to the moved image file
        """
        post_folder = os.path.split(img_path)[0]
        dest_folder = f"{post_folder}/Images"
        dest_path = f"{dest_folder}/{img_name}"

        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)

        shutil.move(img_name, dest_path)

        return dest_path
