from config.constants import DELIMITERS, TOKEN_TYPES


class TextUtils:
    """
    A utility class for text processing operations.
    """

    @staticmethod
    def is_surrounded_by_span(
            original_string: str, i: int, substring: str,
            token_types: list[str] | None = None
    ) -> bool:
        """
        Check if the substring at position i is surrounded by HTML span tags.

        Args:
            original_string (str): The complete string to check within
            i (int): Starting index of the substring
            substring (str): The substring to check
            token_types (list, optional): List of token types to check for in span class attributes.
                Defaults to TOKEN_TYPES.

        Returns:
            bool: True if the substring is within span tags, False otherwise
        """
        if token_types is None:
            token_types = TOKEN_TYPES

        for token_type in token_types:
            span_open = f'<span class="{token_type}">'
            span_close = "</span>"
            start_index = i - len(span_open)
            end_index = i + len(substring) + len(span_close)

            # Check if the substring is directly surrounded by the span tags
            if (
                    original_string[start_index:i] == span_open and
                    original_string[end_index - len(span_close): end_index] == span_close
            ):
                return True

            # Check if the substring is part of the span (within it)
            if start_index >= 0 and original_string[start_index:i].startswith(span_open):
                return True

        return False

    @staticmethod
    def smart_replace(original_string: str, substring: str, replacement: str,
                      delimiters: list[str] | None = None) -> str:
        """
        Replaces occurrences of a substring with a replacement, but only when the substring
        is properly delimited or within HTML span tags.

        Args:
            original_string (str): The string to perform replacements on
            substring (str): The substring to find and replace
            replacement (str): The string to replace the substring with
            delimiters (list[str], optional): List of delimiter characters. Defaults to DELIMITERS.

        Returns:
            str: The string with smart replacements applied
        """
        if delimiters is None:
            delimiters = DELIMITERS

        result = ""
        length = len(original_string)
        i = 0

        while i < length:
            # Check for the substring
            if original_string[i: i + len(substring)] == substring:
                # Check if the surrounding characters are delimiters
                before = original_string[i - 1] if i > 0 else None
                after = (
                    original_string[i + len(substring)]
                    if (i + len(substring)) < length
                    else None
                )

                if (TextUtils.is_surrounded_by_span(original_string, i, substring) or
                        (before in delimiters and after in delimiters)):
                    # Replace substring if surrounded by span or delimiters
                    result += replacement
                else:
                    # Keep the original substring
                    result += substring

                i += len(substring)
            else:
                # Append current character to result
                result += original_string[i]
                i += 1

        return result
