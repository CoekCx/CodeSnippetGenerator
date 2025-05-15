from enum import Enum

from config.constants import TOKEN_CLASS_NAME, TOKEN_INTERFACE, TOKEN_METHOD, TOKEN_PROPERTY, TOKEN_VARIABLE, \
    TOKEN_KEYWORD, TOKEN_NUMBER, TOKEN_COMMENT, TOKEN_STRING, TOKEN_BLANK, BACKGROUND_COLOR


class SyntaxPresets(Enum):
    """
    Enumeration of syntax highlighting presets for code snippets.
    
    This class provides different color schemes for syntax highlighting
    and methods to generate the appropriate CSS for each preset.
    
    Attributes:
        RIDER: JetBrains Rider IDE color scheme
        VISUAL_STUDIO: Visual Studio IDE color scheme
    """
    RIDER = "RIDER"
    VISUAL_STUDIO = "VISUAL_STUDIO"

    @classmethod
    def get_color_scheme(cls, preset_name):
        """
        Returns the color scheme for the given preset name.
        
        Args:
            preset_name: The name of the preset to get the color scheme for
            
        Returns:
            dict: A dictionary mapping token types to their colors
        """
        preset_map = {
            cls.RIDER: rider_preset_colors,
            cls.VISUAL_STUDIO: visual_studio_preset_colors
        }

        return preset_map.get(preset_name, default_preset_colors)

    @classmethod
    def generate_css(cls, preset_name):
        """
        Generates CSS for syntax highlighting based on the given preset.
        
        Args:
            preset_name: The name of the preset to generate CSS for
            
        Returns:
            str: CSS code for syntax highlighting
        """
        colors = cls.get_color_scheme(preset_name)

        css = """
        .code-container {
            background-color: #%s;
            padding: 12px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            width: fit-content;
            margin: 0 auto;
        }

        .code-header {
            background-color: #%s;
            padding: 0.5rem 1rem 0.5rem 9px;
            display: flex;
            align-items: center;
        }

        pre {
            letter-spacing: 0.25px;
            font-family: 'Hack', monospace;
            padding: 5px;
            background-color: #%s;
            color: white;
            overflow: auto;
            margin: 0;
        }
        
        /* Syntax Highlighting */
        .class-name {
            color: #%s;
        }
        
        .interface {
            color: #%s;
        }

        .method {
            color: #%s;
        }
        
        .property {
            color: #%s;
        }

        .variable {
            color: #%s;
        }

        .keyword {
            color: #%s;
        }

        .number {
            color: #%s;
        }

        .comment {
            color: #%s;
        }

        .string {
            color: #%s;
        }
        """ % (
            colors.get(BACKGROUND_COLOR, ""),
            colors.get(BACKGROUND_COLOR, ""),
            colors.get(BACKGROUND_COLOR, ""),
            colors.get(TOKEN_CLASS_NAME, ""),
            colors.get(TOKEN_INTERFACE, ""),
            colors.get(TOKEN_METHOD, ""),
            colors.get(TOKEN_PROPERTY, ""),
            colors.get(TOKEN_VARIABLE, ""),
            colors.get(TOKEN_KEYWORD, ""),
            colors.get(TOKEN_NUMBER, ""),
            colors.get(TOKEN_COMMENT, ""),
            colors.get(TOKEN_STRING, "")
        )

        return css


rider_preset_colors = {
    TOKEN_CLASS_NAME: "c19fff",
    TOKEN_INTERFACE: "c19fff",
    TOKEN_METHOD: "39cc9b",
    TOKEN_PROPERTY: "66c3cc",
    TOKEN_VARIABLE: "ffffff",
    TOKEN_KEYWORD: "6c95eb",
    TOKEN_COMMENT: "85c46c",
    TOKEN_STRING: "c9a26d",
    TOKEN_NUMBER: "ed94c0",
    TOKEN_BLANK: "bdbdbd",
    BACKGROUND_COLOR: "262626",
}

visual_studio_preset_colors = {
    TOKEN_CLASS_NAME: "4ec9b0",
    TOKEN_INTERFACE: "b8d7a3",
    TOKEN_METHOD: "dcdcaa",
    TOKEN_PROPERTY: "dcdcdc",
    TOKEN_VARIABLE: "9cdcfe",
    TOKEN_KEYWORD: "569cd6",
    TOKEN_COMMENT: "57a64a",
    TOKEN_STRING: "d69d85",
    TOKEN_NUMBER: "b5cea8",
    TOKEN_BLANK: "dcdcdc",
    BACKGROUND_COLOR: "1e1e1e",
}

default_preset_colors = {
    TOKEN_CLASS_NAME: "",
    TOKEN_INTERFACE: "",
    TOKEN_METHOD: "",
    TOKEN_PROPERTY: "",
    TOKEN_VARIABLE: "",
    TOKEN_KEYWORD: "",
    TOKEN_COMMENT: "",
    TOKEN_STRING: "",
    TOKEN_NUMBER: "",
    TOKEN_BLANK: "",
    BACKGROUND_COLOR: "",
}
