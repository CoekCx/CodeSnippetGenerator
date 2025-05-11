import os
import sys

from dotenv import load_dotenv


class Settings:
    """
    A class that holds configuration settings for the code snippet generator.
    """

    def __init__(self):
        # Load the .env file from the project root
        dotenv_path = os.path.join(os.getcwd(), '.env')
        load_dotenv(dotenv_path)

        # Required environment variables - app will stop if any are missing
        required_vars = [
            "BLOG_POSTS_PATH",
            "OUTPUT_PATH",
            "LINKEDIN_POSTS_PATH",
            "LINKEDIN_BLOG_POSTS_PATH"
        ]

        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)

        if missing_vars:
            print(f"ERROR: Missing required environment variables: {', '.join(missing_vars)}")
            print("Please check your .env file and ensure all required variables are set.")
            sys.exit(1)

        self.blog_posts_path = os.getenv("BLOG_POSTS_PATH")
        self.output_path = os.getenv("OUTPUT_PATH")
        self.server_port = int(os.getenv("SERVER_PORT", "55003"))
        self.linkedin_posts_path = os.getenv("LINKEDIN_POSTS_PATH")
        self.linkedin_blog_posts_path = os.getenv("LINKEDIN_BLOG_POSTS_PATH")

    @classmethod
    def load(cls) -> "Settings":
        """
        Loads the settings from the environment variables.
        
        Returns:
            Settings: The loaded settings
        """
        return cls()
