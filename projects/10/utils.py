from enum import Enum

XML_SUFFIX = ".xml"

JACK_SUFFIX = '.jack'

VM_SUFFIX = ".vm"

NEW_LINE = "\n"

LINE_COMMENT = "//"

UNARY = ['-', '~']

RETURN_STATEMENT = "returnStatement"

CLASS_VAR_DEC = "classVarDec"

ILLEGAL_STATEMENT_ERROR = "illegal statement"

EXPRESSION_LIST = "expressionList"

TERM = "term"

EXPRESSION = "expression"

IF_TAG = "ifStatement"

LET_TAG = "letStatement"

VAR_TAG = "varDec"

SUBROUTINE_BODY = "subroutineBody"

PARAMETER_LIST = "parameterList"

SUBROUTINE_TAG = "subroutineDec"

IS_ENDING = True

DO_STATEMENT_TAG = "doStatement"

STATEMENTS_TAG = "statements"

CLASS_TAG = "class"

COMPILE_CLASS_ERROR = "invalid input in compile class"

COMPILE_TERM_ERROR = "invalid input in compile term"

CLASS_VAR_KEYWORDS = [
    'static', 'field'
]

KEYWORDS_TYPES = [
    'int', 'char',
    'boolean'
]

SUB_ROUTINE = [
    'constructor', 'function',
    'method'
]

CONST_KEYWORD = [
    'true', 'false',
    'null', 'this'
]

STATEMENTS = [
    'let', 'if',
    'while', 'do',
    'return'
]

TOKEN_TYPE_STRINGS = {
    "KEYWORD": "keyword",
    "SYMBOL": "symbol",
    "IDENTIFIER": "identifier",
    "INT_CONST": "integerConstant",
    "STRING_CONST": "stringConstant"
}

class Types(Enum):
    STATIC = "static"
    FIELD = "this"
    ARG = "argument"
    VAR = 3
    CONST = "constant"
    LOCAL = "local"
    THIS = "this"
    THAT = "that"
    POINTER = "pointer"
    TEMP = "temp"
    NONE = 10


OPERATORS = {
    '+': "add", '-': "sub", '*': "call Math.multiply 2",
    '/': "call Math.divide 2", '&': "and",
    '|': "or",
    '<': "lt", '>': "gt", '=': "eq"
}

SYMBOLS = {
    '{', '}', '(', ')',
    '[', ']', '.', ',',
    '+', '-', ';', '*',
    '/', '&', '|', '<',
    '>', '=', '~'
}

KEYWORDS = {
    "class", "constructor", "function",
    "method", "field", "static", "var",
    "int", "char", "boolean", "void",
    "true", "false", "null", "this", "let",
    "do", "if", "else", "while", "return"
}

SYMBOLS_STRING = "{}\(\)\[\]\.,\+\-;\*/&\|<>=~ "

EMPTY_LINE = ""

END_FILE = ""

INT_RANGE = 32767

TOKEN_REG = r'(\".*\"|(?!\")[' + SYMBOLS_STRING + '])|(?!\")[ \t]'

COMMENT_PATTERN = r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"'

IDENTIFIER_PATTERN = "(\\s*(((_)[\\w])|[a-zA-Z])[\\w_]*\\s*)"

STRING_PATTERN = "\"[^\"]*\""
