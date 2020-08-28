from utils import *
from lexer import *


class Parser(object):
    """
    Parser class
    """

    def __init__(self, file):
        self.lexer = Lexer(file)
        self._init_command()

    def _init_command(self):
        self._command_type = C_ERROR
        self._argument_1 = ''
        self._argument_2 = 0

    def has_more_commands(self):
        return self.lexer.has_more()

    def advance(self):
        self._init_command()
        self.lexer.next()
        token, val = self.lexer.current_token

        if token != ID:
            pass
        if val in NULLARY_COMMANDS:
            self._nullary_command(val)
        elif val in UNARY_COMMANDS:
            self._unary_command(val)
        elif val in BINARY_COMMANDS:
            self._binary_command(val)

    def command_type(self):
        return self._command_type

    def argument_1(self):
        return self._argument_1

    def argument_2(self):
        return self._argument_2

    def _set_command_type(self, command_id):
        self._command_type = COMMANDS[command_id]

    def _nullary_command(self, command_id):
        self._set_command_type(command_id)
        if COMMANDS[command_id] == C_ARITHMETIC:
            self._argument_1 = command_id

    def _unary_command(self, command_id):
        self._nullary_command(command_id)
        self.token, val = self.lexer.next_token()
        self._argument_1 = val

    def _binary_command(self, command_id):
        self._unary_command(command_id)
        self.token, val = self.lexer.next_token()
        self._argument_2 = int(val)
