from .utils import Arithmetics, Commands, COMMENT, NEW_LINE, END_LINE


class Parser:
    def __init__(self, file_name):
        self.file = open(file_name, 'r')
        self.current_line = ""
        self.end_of_file = False
        self._argument1 = ""
        self._argument2 = ""
        self._command = ""
        self.read_line()

    def get_argument1(self):
        return self._argument1

    def get_argument2(self):
        return self._argument2

    def get_command(self):
        return self._command

    def _to_pass(self):
        """
        If we need to pass
        """
        return self.current_line.startswith(COMMENT) or \
               self.current_line.startswith(END_LINE) or \
               self.current_line.startswith(NEW_LINE)

    def read_line(self):
        """
        Read line
        """
        self.current_line = self.file.readline()
        if self.current_line == "":
            self.end_of_file = True
            self.file.close()
        elif self._to_pass():
            self.read_line()
        else:
            self._set_command()
            args = self.current_line.split(' ')
            if self._command == Commands.Arithmetic:
                self._argument1 = args[0]
            else:
                if len(args) > 1:
                    self._argument1 = args[1]
                if len(args) > 2:
                    self._argument2 = args[2]

    def _set_command(self):
        """
        Set command name
        """
        if self.current_line.startswith(Commands.Push):
            self._command = Commands.Push
        elif self.current_line.startswith(Commands.If):
            self._command = Commands.If
        elif self.current_line.startswith(Commands.Pop):
            self._command = Commands.Pop
        elif self.current_line.startswith(Commands.Label):
            self._command = Commands.Label
        elif self.current_line.startswith(Commands.Call):
            self._command = Commands.Call
        elif self.current_line.startswith(Commands.Return):
            self._command = Commands.Return
        elif self.current_line.startswith(Commands.Goto):
            self._command = Commands.Goto
        elif self.current_line.startswith(Commands.Function):
            self._command = Commands.Function
        else:
            if self.current_line.startswith(Arithmetics.Lt) or \
                    self.current_line.startswith(Arithmetics.Gt) or \
                    self.current_line.startswith(Arithmetics.Not) or \
                    self.current_line.startswith(Arithmetics.Or) or \
                    self.current_line.startswith(Arithmetics.Add) or \
                    self.current_line.startswith(Arithmetics.Neg) or \
                    self.current_line.startswith(Arithmetics.Sub) or \
                    self.current_line.startswith(Arithmetics.Eq) or \
                    self.current_line.startswith(Arithmetics.And):
                self._command = Commands.Arithmetic
