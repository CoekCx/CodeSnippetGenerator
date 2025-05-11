DELIMITERS = [
    " ",  # Space
    "\n",  # New line
    "\t",  # Tab
    ".",  # Member access
    "(",  # Opening parenthesis
    ")",  # Closing parenthesis
    "{",  # Opening brace
    "}",  # Closing brace
    "[",  # Opening bracket
    "]",  # Closing bracket
    "<",  # Opening angle bracket
    ">",  # Closing angle bracket
    "=",  # Assignment
    "==",  # Equality
    "!=",  # Inequality
    ">",  # Greater than
    "<",  # Less than
    ">=",  # Greater than or equal
    "<=",  # Less than or equal
    "+",  # Addition
    "-",  # Subtraction
    "*",  # Multiplication
    "/",  # Division
    "%",  # Modulus
    "&&",  # Logical AND
    "||",  # Logical OR
    "!",  # Logical NOT
    ";",  # Statement terminator
    ":",  # Colon
    "?",  # Ternary conditional
    ",",  # Comma
    "@",  # Verbatim identifier
    "#",  # Preprocessor directive
    '"',  # String literal
    "'",  # Character literal
]

# Token classification constants
TOKEN_CLASS_NAME = "class-name"
TOKEN_METHOD = "method"
TOKEN_VARIABLE = "variable"
TOKEN_KEYWORD = "keyword"
TOKEN_NUMBER = "number"
TOKEN_COMMENT = "comment"
TOKEN_STRING = "string"
TOKEN_BLANK = ""

# RGB color values for syntax highlighting in code snippets
TOKEN_COLORS_RGB = {
    TOKEN_CLASS_NAME: (193, 145, 255),
    TOKEN_METHOD: (57, 204, 155),
    TOKEN_VARIABLE: (102, 195, 204),
    TOKEN_KEYWORD: (104, 148, 234),
    TOKEN_NUMBER: (237, 148, 192),
    TOKEN_COMMENT: (133, 196, 108),
    TOKEN_STRING: (200, 161, 98),
    TOKEN_BLANK: (189, 189, 189),
}

TOKEN_COLORS_ANSI = {
    "class-name": 141,
    "method": 79,
    "variable": 110,
    "keyword": 104,
    "number": 218,
    "comment": 108,
    "string": 143,
    "default": 231,
}

TOKEN_TYPES = [
    "class-name",
    "method",
    "variable",
    "keyword",
    "comment",
    "number",
    "default",
]

C_SHARP_KEYWORDS = {
    "abstract",
    "as",
    "base",
    "bool",
    "break",
    "byte",
    "case",
    "catch",
    "char",
    "checked",
    "class",
    "const",
    "continue",
    "decimal",
    "default",
    "delegate",
    "do",
    "double",
    "else",
    "enum",
    "event",
    "explicit",
    "extern",
    "false",
    "finally",
    "fixed",
    "float",
    "for",
    "foreach",
    "goto",
    "if",
    "implicit",
    "in",
    "int",
    "interface",
    "internal",
    "is",
    "lock",
    "long",
    "native",
    "new",
    "null",
    "object",
    "operator",
    "or",
    "out",
    "override",
    "params",
    "private",
    "protected",
    "public",
    "readonly",
    "ref",
    "remove",
    "return",
    "sbyte",
    "sealed",
    "short",
    "sizeof",
    "stackalloc",
    "static",
    "string",
    "struct",
    "switch",
    "this",
    "throw",
    "true",
    "try",
    "typeof",
    "uint",
    "ulong",
    "unchecked",
    "unsafe",
    "ushort",
    "using",
    "virtual",
    "void",
    "volatile",
    "while",
    "with",
    "not",
    "await",
    "sync",
    "async",
    "var",
    "record",
    "get",
    "set",
    "namespace",
    "nameof",
    "file",
    "#region",
    "#endregion",
    "yield",
    "and",
    "union",
    "init",
    "where",
    "required",
    "partial",
}

menu_text = """
    
                                                                                                                                                                     
                                                                                                                                                                     
                                                                                                                                                                     
                                                                                    ███████████████                                                                          
                                                                                █████             █████                                                                      
                                                                              ███                    ████                                                                    
                                                                            ███                         ███                                                                  
                                                                          ███    █       █████            ███                                                                
                                                                         ███  ██████    ███████            ███                                                               
                                                                        ███              █████              ███                                                              
                                                                       ███   ███                  █ █████    ███                                                             
                                                                       ██     ██                              ██                                                             
                                                                      ██████  ██                        █████████                                                            
                                                                      ██      ██  ███████████████ █ ██         ██                                                            
                                                                      ██    █████ ███████ █████████████████    ██                                                            
                                                                      ██    █ ███ ██ █████                █    ██                                                            
                                                                      ████  █ ███ ███ █ ██ ███ █ █ █  █ █ █  ████                                                            
                                                                       ██   █ ███ ███████  █ ███ ████████ █   ██                                                             
                                                                       ████ █ ████       ███████ ████████ █ ████                                                             
                                                                        ███ █ ███                 ███████ █ ███                                                              
                                                                               ███                   ███                                                                     
                                                                          ███████████████████████████████████                                                                
                                                                            ███                         ███                                                                  
                                                                              ████                   ████                                                                    
                                                                                ███████████████████████                                                                      
                                                                                    ███████████████                                                                          
                                                                                                                                                                             
                                                                                                                                                                             
                                                                        █    ██  ███  █   █ █  ██   █  █  █ █ ██                                                             
                                                                        ███  ██  █ █  ███ █ █ █  █  █   ██  █ █                                                              
                                                                                                                                                                     

"""
