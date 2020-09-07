from utils import *


class VmWriter:
    def __init__(self, output_file):
        self.output_file = output_file

    def write_push(self, kind, param_id):
        self.write_line("push " + kind.value + " " + str(param_id))

    def write_pop(self, kind, param_id):
        self.write_line("pop " + kind.value + " " + str(param_id))

    def write_arithmetic(self, operator):
        self.write_line(OPERATORS[operator])

    def write_plain_arithmetic(self, operator):
        self.write_line(operator)

    def write_label(self, symbol):
        self.write_line("label " + symbol)

    def write_goto(self, symbol):
        self.write_line("goto " + symbol)

    def write_if(self, symbol):
        self.write_line("if-goto " + symbol)

    def write_call(self, string_name, n_args):
        self.write_line("call " + string_name + " " + str(n_args))

    def write_function(self, name, n_locals):
        self.write_line("function " + name + " " + str(n_locals))

    def write_return(self):
        self.write_line("return")

    def write_line(self, line):
        self.output_file.write(line + NEW_LINE)
