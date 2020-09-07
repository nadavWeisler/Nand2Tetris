import re

EMPTY_LINE = ""

END_FILE = ""

INT_RANGE = 32767

KEYWORDS = {
    "class": "CLASS", "method": "METHOD",
    "function": "FUNCTION", "constructor": "CONSTRUCTOR",
    "int": "INT", "boolean": "BOOLEAN", "char": "CHAR",
    "void": "VOID", "var": "VAR", "static": "STATIC",
    "field": "FIELD", "let": "LET", "do": "DO", "if": "IF",
    "else": "ELSE", "while": "WHILE",
    "return": "RETURN", "true": "TRUE", "false": "FALSE",
    "null": "NULL", "this": "THIS"
}

SYMBOLS = ["{", "}", "(", ")", "[", "]",
           ".", ",", ";", "+", "-", "*", "/",
           "&", "|", "<", ">", "=", "~"]

SYMBOLS_STRING = "{}()\[\].,;+\-*/&|<>=~"

TOKEN_REG = r'(\".*\"|(?!\")[' + SYMBOLS_STRING + '])|(?!\")[ \t]'

COMMENT_PATTERN = r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"'

IDENTIFIER_PATTERN = "(\\s*(((_)[\\w])|[a-zA-Z])[\\w_]*\\s*)"

STRING_PATTERN = "\"[^\"]*\""


class JackTokenizer:

    def __init__(self, path):
        self._file = open(path)
        self.current_token = None
        self._in_comment = False
        self._token_buffer = self._get_tokens()

    def _get_tokens(self):
        line = self._file.readline()
        if line:
            line = JackTokenizer.comment_remover(self._handle_comments(line).strip())
            tokens = re.split(TOKEN_REG, line)
            return list(filter(None, tokens))

    def _handle_comments(self, line):
        while self._check_if_to_skip(line):
            line = self._file.readline()
        return line

    @staticmethod
    def comment_remover(text):
        def replace_space(line):
            if line.group(0).startswith('/'):
                return " "
            else:
                return  line.group(0)

        pattern = re.compile(COMMENT_PATTERN, re.DOTALL | re.MULTILINE)
        return re.sub(pattern, replace_space, text)

    def _check_if_to_skip(self, line):
        if line == END_FILE:
            return False
        line = line.strip()
        if line == EMPTY_LINE:
            return True
        if line.startswith("//"):
            return True
        if line.startswith("/**") or line.startswith("/*"):
            self._in_comment = True
        if self._in_comment and line.endswith('*/'):
            self._in_comment = False
            return True
        return self._in_comment

    def get_next_token(self):
        if self._token_buffer:
            return self._token_buffer[0]

    def has_more_tokens(self):
        if self._token_buffer:
            return len(self._token_buffer) > 0

    def advance(self):
        if not self.has_more_tokens():
            self._file.close()
            return
        self.current_token = self._token_buffer.pop(0)
        if not self.has_more_tokens():
            self._token_buffer = self._get_tokens()

    def token_type(self):
        if not self.current_token:
            return "No current token"
        if self._is_keyword():
            return "KEYWORD"
        elif self._is_symbol():
            return "SYMBOL"
        elif self._is_int():
            return "INT_CONST"
        elif self._is_string():
            return "STRING_CONST"
        elif self._is_identifier():
            return "IDENTIFIER"

    def _is_symbol(self):
        return self.current_token in SYMBOLS

    def _is_keyword(self):
        return self.current_token in KEYWORDS

    def _is_int(self):
        token = self.current_token
        return token.isdigit() and int(token) in range(INT_RANGE)

    def _is_string(self):
        return re.match(STRING_PATTERN, self.current_token)

    def _is_identifier(self):
        return re.match(IDENTIFIER_PATTERN, self.current_token)

    def key_word(self):
        if self._is_keyword():
            return self.current_token

    def symbol(self):
        if self._is_symbol():
            return self.current_token

    def identifier(self):
        if self._is_identifier():
            return self.current_token

    def int_val(self):
        if self._is_int():
            return int(self.current_token)

    def string_value(self):
        if self._is_string():
            return self.current_token.replace("\"", "")

    def get_token_string(self):
        current_type = self.token_type()
        if current_type == "KEYWORD":
            return self.key_word()
        if current_type == "SYMBOL":
            return self.symbol()
        if current_type == "IDENTIFIER":
            return self.identifier()
        if current_type == "INT_CONST":
            return self.int_val()
        if current_type == "STRING_CONST":
            return self.string_value()
