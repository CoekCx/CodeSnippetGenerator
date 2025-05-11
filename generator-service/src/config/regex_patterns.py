"""
This module contains regex patterns used for extracting and identifying
various elements from C# code in the code snippet generator.
These patterns are used for syntax highlighting and code analysis.
"""

# Pattern to extract using directives and namespace declarations
IMPORTS_AND_NAMESPACES_PATTERN = r"(?:using|namespace)\s+([a-zA-Z0-9_.]+);"

# Pattern to extract class names (not following a dot, and not followed by parentheses)
CLASS_NAMES_PATTERN = r"(?<![.])\b[A-Z][a-zA-Z]*\b(?!\()"

# Pattern to extract method names
METHODS_PATTERN = r"\w+\(.*?"

# Pattern to extract generic method names
GENERIC_METHODS_PATTERN = r".?\b(\w+)<[^>]*>+\("

# Pattern to extract constructors
CONSTRUCTORS_PATTERN = r"\bnew (\w+)"

# Pattern to extract object initializers
OBJECT_INITIALIZERS_PATTERN = r"new\s+\w+\s*\{[^{}]*\}"

# Pattern to extract properties from object initializers
OBJECT_INITIALIZER_PROPERTIES_PATTERN = r"\b(\w+)\b(?=\s*[:=])"

# Pattern to extract properties from member access
MEMBER_ACCESS_PROPERTIES_PATTERN = r"\.\b[A-Z][a-zA-Z0-9]*\b(?!\()"

# Pattern to extract records
RECORDS_PATTERN = r"record \b[A-Z][a-zA-Z]*\b\((?:\w+\s+\w+\,?\s*)+\)"

# Pattern to extract properties from records
RECORD_PROPERTIES_PATTERN = r"\b\w+\s+(\w+)"

# Pattern to extract numbers
NUMBERS_PATTERN = r"\d+"

# Pattern to extract string literals
STRINGS_PATTERN = r'(\$"[^"]*?"|"[^"]*?")'

# Pattern to extract comments
COMMENTS_PATTERN = r"//.*?(?=\n|$)"

# Pattern to extract class properties - handles generic types and various modifiers
CLASS_PROPERTY_PATTERN = r"public\s+(?:[A-Za-z0-9_<>?,\s]+\s+)(\w+)\s*\{\s*get;\s*set;\s*\}"

# Pattern to extract auto-implemented properties with only get
AUTO_PROPERTY_GET_PATTERN = r"(?i)\b\w+\s+[A-Z]\w*\s*\{\s*get;"

# Pattern to extract region names
REGION_NAME_PATTERN = r"#region\s+(.+)$"

# Pattern to extract interpolated string expressions
INTERPOLATED_STRING_EXPRESSIONS_PATTERN = r'\{[^}]*\}'
