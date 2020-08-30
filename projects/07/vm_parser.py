COMMENT = "//"


class Parser:
    def __init__(self, file_name):
        self.file_name = open(file_name, "r")
        self.current_command = ""
        self.current_position = -1
        self.commands = []
        self.arithmetic = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]

        for line in self.file_name.readlines():
            command = line.split(COMMENT)
            if command[0].strip() != "":
                self.commands.append(command[0].strip())

    def got_more_commands(self):
        if self.current_position < len(self.commands) - 1:
            return True
        else:
            return False

    def advance(self):
        if self.got_more_commands():
            self.current_command = self.commands[self.current_position + 1]
            self.current_position += True

    def command_type(self):
        name = self.current_command.split(" ")[0]
        if name in self.arithmetic:
            return "C_ARITHMETIC"
        elif name == "push":
            return "C_PUSH"
        elif name == "pop":
            return "C_POP"
        elif name == "label":
            return "C_LABEL"
        elif name == "function":
            return "C_FUNCTION"
        elif name == "call":
            return "C_CALL"
        elif name == "return":
            return "C_RETURN"
        elif name == "goto":
            return "C_GOTO"
        elif name == "if-goto":
            return "C_IF"

    def argument_1(self):
        if self.current_command == "return":
            pass
        elif self.command_type() == "C_ARITHMETIC":
            return self.current_command
        else:
            return self.current_command.split(" ")[1]

    def argument_2(self):
        c_type = self.command_type()
        if c_type == "C_PUSH" or \
                c_type == "C_POP" or \
                c_type == "C_FUNCTION" or \
                c_type == "C_CALL":
            return self.current_command.split(" ")[2]

    def command_exist(self):
        return self.current_command.split(" ")[0]
