def combine_string_tokens(code_tokens):
    """Combine tokens that are part of a string delimited by double quotes or starting with $."""
    combined_tokens = []
    in_string = False
    is_interpolated_string = False
    current_string = ""

    for i, token in enumerate(code_tokens):
        # Check if the token starts with a double quote or starts with $ and a double quote
        if token.startswith('"') or (
            token.startswith("$")
            and len(code_tokens) > i + 1
            and code_tokens[i + 1] == '"'
        ):
            if in_string:
                current_string += token
                if is_interpolated_string:
                    is_interpolated_string = False
                    continue
                combined_tokens.append(current_string)
                current_string = ""
                in_string = False
            else:
                in_string = True
                if token.startswith("$"):
                    is_interpolated_string = True
                current_string += token
        elif token.endswith('"'):
            if in_string:
                current_string += token
                combined_tokens.append(current_string)
                current_string = ""
                in_string = False
            else:
                combined_tokens.append(token)
        elif in_string:
            current_string += token
        else:
            combined_tokens.append(token)

    return combined_tokens


def combine_comment_tokens(code_tokens):
    """Combine tokens that are part of a comment starting with // and continuing until the next newline token."""
    combined_tokens = []
    in_comment = False
    current_comment = ""

    for token in code_tokens:
        if token == "/" and not in_comment:
            # Start of a comment
            in_comment = True
            current_comment += token
        elif token == "/" and in_comment:
            # Second part of the comment start
            current_comment += token
        elif token == "\n":
            if in_comment:
                # End of the comment
                current_comment += token
                combined_tokens.append(current_comment)
                current_comment = ""
                in_comment = False
            else:
                combined_tokens.append(token)
        elif in_comment:
            current_comment += token
        else:
            if in_comment:
                # If we are ending the comment, add the current comment
                combined_tokens.append(current_comment)
                current_comment = ""
                in_comment = False
            combined_tokens.append(token)

    # Append any remaining comment if the list ended without a newline
    if in_comment:
        combined_tokens.append(current_comment)

    return combined_tokens
