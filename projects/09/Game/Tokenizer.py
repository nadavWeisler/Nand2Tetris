from enum import Enum
import re


class TokenType(Enum):
    """Enum to identify keywords type"""
    KEYWORD = 0
    SYMBOL = 1
    IDENTIFIER = 2
    INT_CONST = 3
    STRING_CONST = 4


# symbols set
symbols = {
    '{', '}', '(', ')', '[', ']', '.', ',', '+', '-', ';', '*', '/', '&', '|',
    '<', '>', '=', '~'
}

# keywords set
keywords = {
    "class", "constructor", "function", "method", "field", "static", "var",
    "int", "char", "boolean", "void", "true", "false", "null", "this", "let",
    "do", "if", "else", "while", "return"
}

symbols_string = "{}\(\)\[\]\.,\+\-;\*/&\|<>=~ "


class Tokenizer:
    """generate token from file path"""

    def __init__(self, path):
        """gets path for jack file and creates a tokenizer object"""
        self.has_ended = False
        self.file = open(path, 'r')
        self.current_token_type = ''

    def advance(self):
        """generator for next token"""
        pattern = re.compile("[^\"]*")
        symbols_pattern = re.compile(
            "[" + symbols_string + "]|[^" + symbols_string + "]*")
        for line in self.file:
            line = re.sub(' +', ' ', line)
            line = line.replace('\t', '')
            line = line.split("//")
            line = line[0].split("/**")
            line = line[0].split("/*")
            if line[0].startswith(" *"):
                line[0] = ''
            if len(line) >= 1 and line[0] != '' and line[0] != '\n' and line[
                0] != "":
                line = line[0].strip('\n')
                flag = False
                for letters in re.findall(pattern, line):
                    letters = letters.replace('\t', '')  # remove tabs
                    if letters != '':  # ignore empty matches
                        if flag:
                            self.current_token_type = TokenType.STRING_CONST
                            yield letters
                            flag = False
                        else:
                            flag = True
                            for token in re.findall(symbols_pattern, letters):
                                token = token.replace('\t', '')  # remove tabs
                                if token != ' ' and token != '':  # ignore empty matches
                                    if token in symbols:
                                        self.current_token_type = TokenType.SYMBOL
                                    elif token in keywords:
                                        self.current_token_type = TokenType.KEYWORD
                                    elif token[0].isdigit():
                                        self.current_token_type = TokenType.INT_CONST
                                    else:
                                        self.current_token_type = TokenType.IDENTIFIER
                                    yield token

    def token_type(self):
        return self.current_token_type
