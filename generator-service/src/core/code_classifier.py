import re

from config.constants import *
from config.regex_patterns import *


def get_tokens(code: str) -> set[str]:
    """
    Extracts tokens from a code string by replacing delimiters with spaces
    and splitting the resulting string.

    Args:
        code (str): The source code string to tokenize

    Returns:
        set[str]: A set of unique tokens extracted from the code
    """
    for delimiter in DELIMITERS:
        code = code.replace(delimiter, " ")

    tokens = set(code.split())
    return tokens


# noinspection DuplicatedCode
def parse_code(code: str) -> dict[str, str]:
    """
    Parses C# code and classifies tokens for syntax highlighting.

    Identifies C# language elements like keywords, classes, methods, and properties
    using regex patterns to match different code constructs.

    Args:
        code (str): The C# code to parse

    Returns:
        dict[str, str]: Mapping of tokens to classification types (keyword,
        class-name, method, variable, number, string, comment)
    """
    tokens = set(get_tokens(code))

    keywords = [kw for kw in C_SHARP_KEYWORDS if kw in tokens]

    imports_and_namespaces = set(re.findall(IMPORTS_AND_NAMESPACES_PATTERN, code))

    domains = set()
    for domain in imports_and_namespaces:
        if "." in domain:
            split_domains = domain.split(".")
            for d in split_domains:
                domains.add(d)
        else:
            domains.add(domain)

    classes = set(re.findall(CLASS_NAMES_PATTERN, code))

    methods = set(re.findall(METHODS_PATTERN, code))
    methods = set([method.split("(")[0] for method in methods])

    generic_methods = set(re.findall(GENERIC_METHODS_PATTERN, code))

    constructors = set(re.findall(CONSTRUCTORS_PATTERN, code))

    object_initializers = set(re.findall(OBJECT_INITIALIZERS_PATTERN, code))
    properties_set = set()
    for initializer in object_initializers:
        # Find all matches for properties using the regex and add them to the set
        properties = re.findall(OBJECT_INITIALIZER_PROPERTIES_PATTERN, initializer)
        properties_set.update(properties)
    variable_properties = [
        prop[1:] for prop in set(re.findall(MEMBER_ACCESS_PROPERTIES_PATTERN, code))
    ]
    # class_properties = set(re.findall(CLASS_PROPERTY_PATTERN, code))  # TODO: Fix this
    class_properties = set(re.findall(AUTO_PROPERTY_GET_PATTERN, code))
    class_properties = [prop.split(" ")[1] for prop in class_properties]

    records = set(re.findall(RECORDS_PATTERN, code))
    record_properties_set = set()
    record_names_set = set()
    for record in records:
        # Find all property names using the regex
        record_name = record.split("(")[0].split()[1]
        record_names_set.add(record_name)

        properties = re.findall(RECORD_PROPERTIES_PATTERN, record.split("(")[1][0:-1])
        record_properties_set.update(properties)

    numbers = set(re.findall(NUMBERS_PATTERN, code))

    strings = set(re.findall(STRINGS_PATTERN, code))

    interpolated_strings = set(re.findall(INTERPOLATED_STRING_EXPRESSIONS_PATTERN, code))  # TODO: Fix this

    comments = set(re.findall(COMMENTS_PATTERN, code))

    region_names = set(re.findall(REGION_NAME_PATTERN, code))  # TODO: Fix this

    token_classifications = {}

    # Classes (highest priority)
    for cls in classes:
        token_classifications[cls] = TOKEN_CLASS_NAME

    # Methods
    for method in methods:
        token_classifications[method] = TOKEN_METHOD

    # Object initializer properties
    for prop in properties_set:
        token_classifications[prop] = TOKEN_VARIABLE

    # Variable properties
    for prop in variable_properties:
        token_classifications[prop] = TOKEN_VARIABLE

    # Class properties
    for prop in class_properties:
        token_classifications[prop] = TOKEN_VARIABLE

    # Domains (from imports and namespaces)
    for domain in domains:
        token_classifications[domain] = TOKEN_CLASS_NAME

    # Generic methods
    for method in generic_methods:
        token_classifications[method] = TOKEN_METHOD

    # Constructors
    for con in constructors:
        token_classifications[con] = TOKEN_CLASS_NAME

    # Record properties
    for prop in record_properties_set:
        token_classifications[prop] = TOKEN_BLANK

    # Record names
    for rec in record_names_set:
        token_classifications[rec] = TOKEN_CLASS_NAME

    # Numbers
    for num in numbers:
        token_classifications[num] = TOKEN_NUMBER

    # Strings
    for string in strings:
        token_classifications[f"{string}"] = TOKEN_STRING

    # Comments
    for comment in comments:
        token_classifications[f"{comment}\n"] = TOKEN_COMMENT

    # Region names
    for region in region_names:
        token_classifications[region] = TOKEN_COMMENT

    # Keywords
    for keyword in keywords:
        token_classifications[keyword] = TOKEN_KEYWORD

    # Interpolated strings
    for interpolated_string in interpolated_strings:
        token_classifications[interpolated_string] = TOKEN_BLANK

    return token_classifications
