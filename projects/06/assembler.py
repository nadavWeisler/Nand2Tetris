import os
import sys

BIT_SIZE = 16
HACK_SUFFIX = ".hack"
ASM_SUFFIX = ".asm"
NEW_LINE = '\n'
TAB_SPACE = '\r'
JMP_0 = "000"
CMP_0 = "0000000"
COMMENT = "//"
SYMBOLS = {
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
    "R7": 7,
    "R8": 8,
    "R9": 9,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15,
    "KDB": 24576,
    "SCREEN": 16384,
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4
}

JMP = {
    "JDT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

CMP = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "M": "1110000",
    "!D": "0001101",
    "!A": "0110001",
    "!M": "1110001",
    "-D": "0001111",
    "-A": "0110011",
    "-M": "1110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "M+1": "1110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "M-1": "1110010",
    "D+A": "0000010",
    "D+M": "1000010",
    "D-A": "0010011",
    "D-M": "1010011",
    "A-D": "0000111",
    "M-D": "1000111",
    "D&A": "0000000",
    "D&M": "1000000",
    "D|A": "0010101",
    "D|M": "1010101"
}


def if_pass(line):
    if(line.startswith(NEW_LINE) or line.startswith(COMMENT) or line.startswith(TAB_SPACE)):
        return True
    return False


def add_symboles(old_file, new_file):
    count = 0
    for line in old_file:
        if if_pass(line):
            pass
        else:
            pass
    pass


def add_varriables(old_file, new_file):
    pass


def create_file():
    pass


def run_file(file_path):
    with open(file_path) as read_file:
        filename = os.path.splitext(file_path)[0]
        with open(filename + HACK_SUFFIX, 'w') as write_file:
            pass


if __name__ == "__main__":
    if os.path.isdir(sys.argv[1]):
        for root, dirs, files in os.walk(sys.argv[1], topdown=True):
            for name in files:
                file_path = os.path.join(root, name)
                file_extension = os.path.splitext(file_path)[1]
                if file_extension == ASM_SUFFIX:
                    run_file(file_path)
    else:
        run_file(sys.argv[1])
