from utils import COMMENT, FilePermissions, CommandsTypes, EMPTY_STRING


class Parser:
    def __init__(self, file_name):
        self.file_name = open(file_name, FilePermissions().Read)
        self.current_command = EMPTY_STRING
        self.current_position = -1
        self.commands = []
        self.COMMANDS_DIC = {
            "add": CommandsTypes().Arithmetic,
            "sub": CommandsTypes().Arithmetic,
            "neg": CommandsTypes().Arithmetic,
            "eq": CommandsTypes().Arithmetic,
            "gt": CommandsTypes().Arithmetic,
            "lt": CommandsTypes().Arithmetic,
            "and": CommandsTypes().Arithmetic,
            "or": CommandsTypes().Arithmetic,
            "not": CommandsTypes().Arithmetic,
            "push": CommandsTypes().Push,
            "pop": CommandsTypes().Pop,
            "label": CommandsTypes().Label,
            "call": CommandsTypes().Call,
            "function": CommandsTypes().Function,
            "goto": CommandsTypes().Goto,
            "if-goto": CommandsTypes().If,
            "return": CommandsTypes().Return
        }

        for line in self.file_name.readlines():
            command = line.split(COMMENT)
            if command[0].strip() != EMPTY_STRING:
                self.commands.append(command[0].strip())

    def got_more_commands(self):
        return self.current_position < (len(self.commands) - 1)

    def advance(self):
        if self.got_more_commands():
            self.current_command = self.commands[self.current_position + 1]
            self.current_position += True

    def command_type(self):
        name = self.current_command.split(" ")[0]
        if name in self.COMMANDS_DIC.keys():
            return self.COMMANDS_DIC[name]

    def argument_1(self):
        if self.current_command == "return":
            pass
        elif self.command_type() == CommandsTypes().Arithmetic:
            return self.current_command
        else:
            return self.current_command.split(" ")[1]

    def argument_2(self):
        c_type = self.command_type()
        if c_type == CommandsTypes().Push or \
                c_type == CommandsTypes().Pop or \
                c_type == CommandsTypes().Function or \
                c_type == CommandsTypes().Call:
            return self.current_command.split(" ")[2]

    def command_exist(self):
        return self.current_command.split(" ")[0]
