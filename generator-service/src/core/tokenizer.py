from config.constants import DELIMITERS


def tokenize(code: str, delimiters: list[str] | None = None) -> list[str]:
    """
    Tokenizes a code string by splitting it at specified delimiters.
    
    Args:
        code (str): The source code string to tokenize.
        delimiters (list, optional): A list of delimiter characters to use for tokenization.
            If None, uses the default DELIMITERS from config.
    
    Returns:
        list[str]: A list of tokens extracted from the code.
    """
    if delimiters is None:
        delimiters = DELIMITERS
    tokens = []
    current_token = ""
    length = len(code)

    for i in range(length):
        char = code[i]

        # Check if the current character is a delimiter
        if char in delimiters:
            # If there's a current token, add it to the tokens list
            if current_token:
                tokens.append(current_token)
                current_token = ""
            # Add the delimiter itself as a token
            tokens.append(char)
        else:
            # Build the current token
            current_token += char

    # Add any remaining token
    if current_token:
        tokens.append(current_token)

    return tokens
