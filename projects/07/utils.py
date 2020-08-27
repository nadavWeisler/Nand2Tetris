ASSEMBLY_SUFFIX = ".asm"

NEW_LINE = "\n"
COMMENT = "//"
END_LINE = "\r"


class Commands:
    Arithmetic = "arithmetics"
    Push = "push"
    Pop = "pop"
    If = "if-goto"
    Label = "label"
    Function = "function"
    Goto = "goto"
    Call = "call"
    Return = "return"


class Arithmetics:
    Add = "add"
    Neg = "neg"
    Sub = "sub"
    Or = "or"
    Not = "not"
    And = "and"
    Gt = "gt"
    Lt = "lt"
    Eq = "eq"
