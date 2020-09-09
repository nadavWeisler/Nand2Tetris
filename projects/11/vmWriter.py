from utils import *


class VmWriter:
    def __init__(self):
        self._result = []

    def write(self, file_name):
        result = open(file_name, 'w')
        for line in self._result:
            result.write(line)
        result.close()

    def write_push(self, segment, index):
        self._result.append(VmCommands.Push + " " + segment + " " + str(index) + NEW_LINE)

    def write_pop(self, segment, index):
        self._result.append(VmCommands.Pop + " " + segment + " " + str(index) + NEW_LINE)

    def write_arithmetic(self, command):
        self._result.append(command + NEW_LINE)

    def write_label(self, label):
        self._result.append(VmCommands.Label + " " + label + NEW_LINE)

    def write_goto(self, label):
        self._result.append(VmCommands.Goto + " " + label + NEW_LINE)

    def write_if(self, label):
        self._result.append(VmCommands.If + " " + label + NEW_LINE)

    def write_call(self, name, argument_count):
        self._result.append(VmCommands.Call + " " + name + " " + str(argument_count) + NEW_LINE)

    def write_function(self, name, locals_count):
        self._result.append(VmCommands.Function + " " + name + " " + str(locals_count) + NEW_LINE)

    def write_return(self):
        self._result.append(VmCommands.Return + NEW_LINE)

    def write_memory(self):
        self._result.append(VmCommands.MemoryCall + NEW_LINE)

    def write_true(self):
        self.write_push(Kinds.Constants, 0)
        self.write_arithmetic("not")

    def write_this(self):
        self.write_push(Kinds.Pointer, 0)

    def write_false_or_null(self):
        self.write_push(Kinds.Constants, 0)

    def write_keywordConstants(self, keyword):
        if keyword == "true":
            self.write_true()
            return
        elif keyword == Kinds.This:
            self.write_this()
        else:
            self.write_false_or_null()
