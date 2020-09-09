VM_SUFFIX = ".vm"

JACK_SUFFIX = '.jack'

NEW_LINE = "\n"

OPERATORS = {
    '+': 'add', '-': 'sub',
    '*': "call Math.multiply 2",
    '/': "call Math.divide 2",
    '&amp;': 'and', '|': 'or',
    '&lt;': 'lt', '&gt;': 'gt',
    '=': 'eq', '&quot;': None
}

UNARY_OPERATORS = {
    '-', '~'
}

CONSTANTS_KEYWORDS = {
    'true', 'false',
    'null', 'this'
}


class TokenTypes:
    Static = "static"
    Field = "field"
    Method = "method"
    Function = "function"
    Constructor = "constructor"


KEYWORDS = [
    'class', 'constructor', 'function', 'method', 'field', 'static',
    'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null',
    'this', 'let', 'do', 'if', 'else', 'while', 'return'
]

SYMBOLS = [
    '{', '}', '(', ')', '[', ']', '.', ',', ';',
    '+', '-', '*', '/', '&', '|', '<', '>', '=', '~'
]

TOKEN_KEYWORDS = {
    'keyword', 'symbol', 'identifier', 'integerConstant', 'stringConstant'
}

MAX_INT = 32767


class VmCommands:
    Push = "push"
    Pop = "pop"
    Label = "label"
    Goto = "goto"
    If = "if-goto"
    Call = "call"
    Function = "function"
    Return = "return"
    MemoryCall = "call Memory.alloc 1"


class Kinds:
    Constants = "constant"
    Pointer = "pointer"
    Static = "static"
    Field = "this"
    Argument = "argument"
    Variable = 3
    Local = "local"
    This = "this"
    That = "that"
    Temp = "temp"
    Nothing = 10
