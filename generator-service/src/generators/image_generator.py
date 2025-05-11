"""
DEPRECATED: This file is no longer in use and will be removed in a future version.
"""

import os
import shutil
import time
import warnings

from PIL import Image
from html2image import Html2Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from config.prompts import print_success
from rendering.html_simulator import get_code_content_size
from utils.file_handler import FileHandler

warnings.warn(
    "The module 'image_generator' is deprecated and will be removed in a future version.",
    DeprecationWarning,
    stacklevel=2
)


def generate_image_with_html2image(
        html_code: str,
        img_name: str = "generated_image.png",
        img_path: str = "Generated Images",
) -> None:
    """
    Generates an image from HTML code and saves it to the specified path.
    
    Args:
        html_code (str): The HTML content to render as an image
        img_name (str, optional): The name for the generated image file. 
            Defaults to "generated_image.png".
        img_path (str, optional): The directory path where the image will be saved. 
            Defaults to "Generated Images".
            
    Raises:
        Exception: If there is an error during image generation
    """
    # Create a temporary directory for Html2Image
    temp_output_dir = os.path.abspath("temp_output")
    if not os.path.exists(temp_output_dir):
        os.makedirs(temp_output_dir)

    try:
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"

        hti = Html2Image(output_path=temp_output_dir, browser_executable=chrome_path)
        hti.size = get_code_content_size()

        if img_name.endswith(".cs"):
            img_name = img_name[:-3] + ".png"
        elif img_name.endswith(".txt"):
            img_name = img_name[:-4] + ".png"
        else:
            img_name += ".png"

        # Try to generate the image without suppressing output to see any errors
        hti.screenshot(html_str=html_code, save_as=img_name)

        # Check if the image was created
        source_path = os.path.join(temp_output_dir, img_name)
        if not os.path.exists(source_path):
            print(f"Failed to generate image. Expected at: {source_path}")
            print(f"HTML content length: {len(html_code)}")
            print(f"Size settings: {hti.size}")
            input()
            return

        dest_path = FileHandler.move_image(img_name, img_path)
        shutil.rmtree(temp_output_dir)

        os.system("cls")
        print_success(f"Image saved to {dest_path}")

    except Exception as e:
        print(f"Error generating image: {str(e)}")
        if os.path.exists(temp_output_dir):
            shutil.rmtree(temp_output_dir)
        raise


def generate_image_with_selenium(html_path: str, output_path: str) -> bool:
    """
    Generates an image from an HTML file using Selenium WebDriver.
    
    Args:
        html_path (str): Path to the HTML file to render
        output_path (str): Path where the generated image will be saved
        
    Returns:
        bool: True if the image was successfully generated, False otherwise
        
    Raises:
        Exception: The function catches all exceptions internally and returns False,
                  but prints the error message to the console
    """
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chrome_options)

    try:
        abs_path = os.path.abspath(html_path)
        file_url = f"file:///{abs_path}"

        # Load the HTML file
        driver.get(file_url)

        # Wait for the page to load
        time.sleep(10)

        total_height = driver.execute_script("return document.body.scrollHeight")
        total_width = driver.execute_script("return document.body.scrollWidth")

        # Set window size to capture everything
        driver.set_window_size(total_width, total_height)

        driver.save_screenshot('temp_screenshot.png')

        # Process the image using PIL
        screenshot = Image.open('temp_screenshot.png')
        screenshot.save(output_path)

        # Clean up
        os.remove('temp_screenshot.png')
        driver.quit()

        return True

    except Exception as e:
        print(f"Error converting HTML to image: {str(e)}")
        driver.quit()
        return False
