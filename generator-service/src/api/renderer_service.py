import os

import requests

from config.settings import Settings


class RendererService:
    """
    Service class for communicating with the Node.js renderer service
    that handles HTML to image conversion.
    """

    def __init__(self):
        """Initialize the renderer service with configuration from environment variables."""
        self.settings = Settings.load()
        self.renderer_url = self.settings.renderer_service_url

    def _get_relative_path(self, full_path):
        """
        Converts a full Windows path to a path relative to the Docker container's /output mount.
        
        Args:
            full_path (str): The full Windows path
            
        Returns:
            str: The path relative to the Docker container's /output directory
        """
        # For LinkedIn posts (images)
        if full_path.startswith(self.settings.linkedin_posts_path):
            return os.path.relpath(full_path, "D:/Coek/Work/Social Media Nikola")

        # For Blog posts (HTML/images)
        if full_path.startswith(self.settings.blog_posts_path):
            return os.path.relpath(full_path, "D:/Coek/Work/Social Media Nikola")

        # Default case - return the path as is
        return full_path

    def convert_html_to_image(self, html_content: str, dest_path: str, filename: str) -> dict:
        """
        Sends HTML content to the renderer service to be converted to an image.
        
        Args:
            html_content (str): The HTML content to convert
            dest_path (str): The destination path (can be a full Windows path)
            filename (str): The filename for the generated image (must end with .png, .jpg, or .jpeg)
            
        Returns:
            dict: Response from the renderer service containing status and path information
            
        Raises:
            Exception: If the renderer service returns an error or is unavailable
        """
        # Convert full Windows path to relative path for Docker container
        relative_dest_path = self._get_relative_path(dest_path)

        try:
            response = requests.post(
                f"{self.renderer_url}/convert",
                json={
                    "html": html_content,
                    "destPath": relative_dest_path,
                    "filename": filename
                },
                timeout=30
            )

            if response.status_code == 200:
                # Convert the relative path back to full Windows path for local use
                result = response.json()
                result['path'] = os.path.join("D:/Coek/Work/Social Media Nikola", relative_dest_path, filename)
                return result
            else:
                error_data = response.json()
                raise Exception(f"Renderer service error: {error_data.get('error', 'Unknown error')}")

        except requests.RequestException as e:
            raise Exception(f"Failed to communicate with renderer service: {str(e)}")
