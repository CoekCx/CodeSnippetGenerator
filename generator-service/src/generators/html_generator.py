import os

import pyperclip
from blessed import Terminal

from api.renderer_service import RendererService
from config.constants import TOKEN_COLORS_ANSI
from config.prompts import print_success
from config.settings import Settings
from config.syntax_presets import SyntaxPresets
from core.token_combiners import combine_string_tokens, combine_comment_tokens
from core.tokenizer import tokenize


class HtmlGenerator:
    @staticmethod
    def __print_token(token: str, token_classifications: dict[str, str]) -> None:
        """
        Prints a token to the console with syntax highlighting based on its classification.

        Args:
            token (str): The code token to print
            token_classifications (dict[str, str]): A dictionary mapping tokens to their
                classification types (e.g., 'keyword', 'class-name', 'method')
        """
        terminal = Terminal()
        color = TOKEN_COLORS_ANSI.get(
            token_classifications.get(token, ""), TOKEN_COLORS_ANSI["default"]
        )
        print(terminal.color(color)(token), end="")

    @staticmethod
    def generate_code_snippet_html(
            code_snippet: str,
            token_classifications: dict[str, str],
            show_code_snippet: bool = False,
    ) -> str:
        """
        Generates HTML markup for a code snippet with syntax highlighting.
        
        Args:
            code_snippet (str): The source code to convert to HTML
            token_classifications (dict[str, str]): A dictionary mapping tokens to their
                classification types (e.g., 'keyword', 'class-name', 'method')
            show_code_snippet (bool, optional): Whether to print the code snippet to
                the console with syntax highlighting. Defaults to False.
                
        Returns:
            str: HTML markup of the code snippet with syntax highlighting spans
        """
        tokens = token_classifications.keys()
        code_tokens = tokenize(code_snippet)
        code_tokens = combine_string_tokens(code_tokens)
        code_tokens = combine_comment_tokens(code_tokens)
        code_snippet_html = ""

        starting_index = 0
        ending_index = None
        if code_tokens[0] == "\n":
            starting_index = 1
        if code_tokens[-1] == "\n":
            ending_index = -1

        for token in code_tokens[starting_index:ending_index]:
            if token not in tokens:
                if token == "<":
                    code_snippet_html += "&lt;"
                elif token == ">":
                    code_snippet_html += "&gt;"
                else:
                    code_snippet_html += token
            else:
                code_snippet_html += (
                    f'<span class="{token_classifications[token]}">{token}</span>'
                )
            if show_code_snippet:
                HtmlGenerator.__print_token(token, token_classifications)

        if show_code_snippet:
            print("\n\n")
        return code_snippet_html

    @staticmethod
    def generate_code_snippets_image_html(
            code_snippet: str, token_classifications: dict[str, str]
    ) -> str:
        """
        Generates HTML for a code snippet that will be rendered as an image.
        
        Args:
            code_snippet (str): The source code to convert to HTML
            token_classifications (dict[str, str]): A dictionary mapping tokens to their
                classification types (e.g., 'keyword', 'class-name', 'method')
                
        Returns:
            str: Complete HTML document with the syntax-highlighted code snippet
                 embedded in a template suitable for rendering as an image
        """
        code_snippet_html = HtmlGenerator.generate_code_snippet_html(
            code_snippet, token_classifications, True
        )

        current_dir = os.getcwd()
        template_path = os.path.join(current_dir, "resources/snippet_template.html").replace("\\", "/")
        font_path = os.path.join(current_dir, "resources/fonts/Hack-Regular.ttf").replace("\\", "/")

        with open(template_path, "r", encoding="utf-8") as file:
            html_code = file.read()

        html_code = (html_code
                     .replace("{{FONT_PATH}}", font_path)
                     .replace("{{CODE_SNIPPET}}", code_snippet_html)
                     .replace("{{CSS_CODE}}", SyntaxPresets.generate_css(Settings.load().syntax_preset)))

        return html_code

    @staticmethod
    def render_code_snippet_image(
            html_code: str,
            dest_path: str = "snippets",
            filename: str = "code_snippet.png"
    ) -> dict:
        """
        Renders a code snippet as an image using the external renderer service.
        
        Args:
            html_code (str): The html code to render as an image
            dest_path (str, optional): The destination folder path. Defaults to "snippets".
            filename (str, optional): The filename for the image. Defaults to "code_snippet.png".
                
        Returns:
            dict: Response from the renderer service with image path information
        """
        if not filename.lower().endswith('.png'):
            filename = os.path.splitext(filename)[0] + '.png'

        renderer = RendererService()
        result = renderer.convert_html_to_image(html_code, dest_path, filename)

        print_success(f"\n\nImage successfully generated at: {result.get('path')}")
        return result

    @staticmethod
    def generate_blog_html(
            code_snippet: str, token_classifications: dict[str, str], title="csharp"
    ) -> None:
        """
        Generates HTML for a code snippet suitable for blog posts and copies it to clipboard.
        
        Args:
            code_snippet (str): The source code to convert to HTML
            token_classifications (dict[str, str]): A dictionary mapping tokens to their
                classification types (e.g., 'keyword', 'class-name', 'method')
            title (str, optional): The title to display in the code header.
                Defaults to "csharp".
                
        Returns:
            None: The HTML is copied to the clipboard
        """
        code_snippet_html = HtmlGenerator.generate_code_snippet_html(
            code_snippet, token_classifications, True
        )
        html_code = f"""
        <div class="code-container">
            <div class="code-header">
                <span class="code-header-title">{title}</span>
            </div>
            <pre><code>{code_snippet_html}</code></pre>
        </div>
        """
        pyperclip.copy(html_code)
        print_success("\n\nSuccessfully copied html code to clipboard!")

    @staticmethod
    def generate_blog_html_file_content(
            code_snippet: str, token_classifications: dict[str, str], title="csharp"
    ) -> str:
        """
        Generates HTML content for a code snippet suitable for blog app.
        
        Args:
            code_snippet (str): The source code to convert to HTML
            token_classifications (dict[str, str]): A dictionary mapping tokens to their
                classification types (e.g., 'keyword', 'class-name', 'method')
            title (str, optional): The title to display in the code header.
                Defaults to "csharp".
                
        Returns:
            str: The generated HTML code as a string
        """
        code_snippet_html = HtmlGenerator.generate_code_snippet_html(
            code_snippet, token_classifications, True
        )
        html_code = f"""<div class="code-container">
    <div class="code-header">
    <span class="code-header-title">{title}</span>
    </div>
    <pre><code>{code_snippet_html}</code></pre>
    </div>"""
        print_success("\n\nSuccessfully copied html code to clipboard!")
        return html_code
