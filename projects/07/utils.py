NEW_LINE = "\n"

C_ARITHMETIC = 0
C_PUSH = 1
C_POP = 2
C_LABEL = 3
C_GOTO = 4
C_IF = 5
C_FUNCTION = 6
C_RETURN = 7
C_CALL = 8
C_ERROR = 9

R_SP = 0
R_LCL = 1
R_ARG = 2
R_PTR = 3
R_TEMP = 5

R_THIS = 3
R_THAT = 4

R_FRAME = 13
R_RET = 14
R_COPY = 15

R_R0 = 0
R_R1 = 1
R_R2 = 2
R_R3 = 3
R_R4 = 4
R_R5 = 5
R_R6 = 6
R_R7 = 7
R_R8 = 8
R_R9 = 9
R_R10 = 10
R_R11 = 11
R_R12 = 12
R_R13 = 13
R_R14 = 14
R_R15 = 15

S_LCL = 'local'
S_ARG = 'argument'
S_THIS = 'this'
S_THAT = 'that'
S_PTR = 'pointer'
S_TEMP = 'temp'
S_CONST = 'constant'
S_STATIC = 'static'
S_REG = 'reg'

COMMANDS = {
    'label': C_LABEL,
    'goto': C_GOTO,
    'if-goto': C_IF,
    'push': C_PUSH,
    'pop': C_POP,
    'call': C_CALL,
    'return': C_RETURN,
    'function': C_FUNCTION,
    'add': C_ARITHMETIC,
    'sub': C_ARITHMETIC,
    'neg': C_ARITHMETIC,
    'eq': C_ARITHMETIC,
    'gt': C_ARITHMETIC,
    'lt': C_ARITHMETIC,
    'and': C_ARITHMETIC,
    'or': C_ARITHMETIC,
    'not': C_ARITHMETIC
}

NULLARY_COMMANDS = ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not', 'return']
UNARY_COMMANDS = ['label', 'goto', 'if-goto']
BINARY_COMMANDS = ['push', 'pop', 'function', 'call']
