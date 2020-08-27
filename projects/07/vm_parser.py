import utils


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
        return self.current_line.startswith(utils.COMMENT) or \
               self.current_line.startswith(utils.END_LINE) or \
               self.current_line.startswith(utils.NEW_LINE)

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
            if self._command == utils.Commands.Arithmetic:
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
        if self.current_line.startswith(utils.Commands.Push):
            self._command = utils.Commands.Push
        elif self.current_line.startswith(utils.Commands.If):
            self._command = utils.Commands.If
        elif self.current_line.startswith(utils.Commands.Pop):
            self._command = utils.Commands.Pop
        elif self.current_line.startswith(utils.Commands.Label):
            self._command = utils.Commands.Label
        elif self.current_line.startswith(utils.Commands.Call):
            self._command = utils.Commands.Call
        elif self.current_line.startswith(utils.Commands.Return):
            self._command = utils.Commands.Return
        elif self.current_line.startswith(utils.Commands.Goto):
            self._command = utils.Commands.Goto
        elif self.current_line.startswith(utils.Commands.Function):
            self._command = utils.Commands.Function
        else:
            if self.current_line.startswith(utils.Arithmetics.Lt) or \
                    self.current_line.startswith(utils.Arithmetics.Gt) or \
                    self.current_line.startswith(utils.Arithmetics.Not) or \
                    self.current_line.startswith(utils.Arithmetics.Or) or \
                    self.current_line.startswith(utils.Arithmetics.Add) or \
                    self.current_line.startswith(utils.Arithmetics.Neg) or \
                    self.current_line.startswith(utils.Arithmetics.Sub) or \
                    self.current_line.startswith(utils.Arithmetics.Eq) or \
                    self.current_line.startswith(utils.Arithmetics.And):
                self._command = utils.Commands.Arithmetic
