VM_SUFFIX = ".vm"
ASM_SUFFIX = ".asm"
COMMENT = "//"

NEW_LINE = "\n"
EMPTY_STRING = ""

ERROR_BAD_AMOUNT_OF_PARAMS = "Usage: Bad amount of parameters"


class CommandsTypes:
    def __init__(self):
        self.Arithmetic = "C_ARITHMETIC"
        self.Push = "C_PUSH"
        self.Pop = "C_POP"
        self.Function = "C_FUNCTION"
        self.Label = "C_LABEL"
        self.Goto = "C_GOTO"
        self.If = "C_IF"
        self.Call = "C_CALL"
        self.Return = "C_RETURN"


class SegmentsTypes():
    def __init__(self):
        self.Local = "local"
        self.Temp = "temp"
        self.Constant = "constant"
        self.Argument = "argument"
        self.This = "this"
        self.That = "That"
        self.Pointer = "pointer"
        self.Static = "static"


class FilePermissions:
    def __init__(self):
        self.Read = "r"
        self.WritePlus = "w+"
        self.Addition = "a"
