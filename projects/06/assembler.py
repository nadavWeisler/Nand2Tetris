import os
import sys

HACK_SUFFIX = ".hack"
ASM_SUFFIX = ".asm"
NEW_LINE = "\n"
COMMENT = "//"
AT_SIGN = "@"
OPEN_PARENTHESES = "("
EQUAL_SIGN = "="
SEMICOLON = ";"
EMPTY_STRING = ""

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

DST = {
    "": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111",
}

JMP = {
    "": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

CMP = {
    "": "0000000",
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

variables = {}
labels = {}
variables_count = 16


def get_symbol(symbol):
    """
    Get symbol value
    """
    global variables_count
    if symbol in labels:
        return labels[symbol]
    if symbol in SYMBOLS:
        return SYMBOLS[symbol]
    else:
        if symbol not in variables:
            variables[symbol] = variables_count
            variables_count += 1
        return variables[symbol]


def clean_file(file):
    """
    Get file lines
    """
    lines = []
    for line in file:
        clean_line = line.split(COMMENT)[0].strip()
        if clean_line.startswith(OPEN_PARENTHESES):
            label_name = clean_line[1:-1]
            labels[label_name] = len(lines)
        elif clean_line:
            lines.append(clean_line)
    return lines


def translate_line(line):
    """
    Translate ASM line
    """
    if line.startswith(AT_SIGN):
        return get_instruction_a(line)
    else:
        return get_instruction_c(line)


def write_to_file(new_file_path, lines):
    """
    Write translate file to file
    """
    with open(new_file_path, 'w') as write_file:
        for line in lines:
            write_file.write(translate_line(line) + NEW_LINE)


def get_instruction_a(line):
    """
    Get instruction a translated line
    """
    target = line[1:]
    try:
        address = int(target)
    except ValueError:
        address = get_symbol(target)

    return "0{:0>15b}".format(address)


def get_instruction_c(line):
    """
    Get instruction c translated line
    """
    if EQUAL_SIGN in line:
        dest, rest = line.split(EQUAL_SIGN)
    else:
        dest, rest = ("", line)

    if SEMICOLON in rest:
        comp, jump = rest.split(";")
    else:
        comp, jump = (rest, "")

    return "111" + CMP[comp] + DST[dest] + JMP[jump]


def translate_file(in_file_name, out_file_name):
    """
    Translate file
    """
    with open(in_file_name) as read_file:
        write_to_file(out_file_name, clean_file(read_file))


if __name__ == "__main__":
    if os.path.isdir(sys.argv[1]):
        for root, dirs, files in os.walk(sys.argv[1], topdown=True):
            for name in files:
                file_path = os.path.join(root, name)
                filename, file_extension = os.path.splitext(file_path)
                if file_extension == ASM_SUFFIX:
                    translate_file(file_path, filename + HACK_SUFFIX)
    else:
        filename = os.path.splitext(sys.argv[1])[0]
        translate_file(sys.argv[1], filename + HACK_SUFFIX)
