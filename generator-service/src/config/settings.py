import os
import sys

from dotenv import load_dotenv

from config.syntax_presets import SyntaxPresets


class Settings:
    """
    A class that holds configuration settings for the code snippet generator.
    Implements the Singleton pattern to ensure only one instance exists.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
            
        self._initialized = True
        dotenv_path = os.path.join(os.getcwd(), '.env')
        if not os.path.exists(dotenv_path):
            parent_dotenv_path = os.path.join(os.path.dirname(os.getcwd()), '.env')
            if os.path.exists(parent_dotenv_path):
                dotenv_path = parent_dotenv_path

        load_dotenv(dotenv_path)

        required_vars = [
            "LINKEDIN_POSTS_PATH",
            "BLOG_POSTS_PATH",
            "OUTPUT_PATH",
            "SERVER_PORT",
            "RENDERER_SERVICE_URL",
            "BLOG_MODE",
            "SYNTAX_PRESET"
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
        self.renderer_service_url = os.getenv("RENDERER_SERVICE_URL", 'http://localhost:3000')
        self.blog_mode = os.getenv("BLOG_MODE", "False").lower() == "true"
        syntax_preset_value = os.getenv("SYNTAX_PRESET")
        self.syntax_preset = SyntaxPresets[syntax_preset_value]

        # In Docker, use the container service name for renderer
        if os.environ.get('DOCKER_ENV') == 'true':
            self.renderer_service_url = 'http://renderer-service:3000'

    @classmethod
    def reset(cls) -> None:
        """
        Deletes the singleton instance. The next call to load() will create a fresh instance.
        """
        cls._instance = None

    @classmethod
    def load(cls) -> "Settings":
        """
        Loads the settings from the environment variables.
        Returns the same instance on subsequent calls.
        
        Returns:
            Settings: The singleton settings instance
        """
        return cls()
