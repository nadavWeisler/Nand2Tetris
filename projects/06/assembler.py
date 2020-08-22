import os
import re
import sys

BIT_SIZE = 16
HACK_SUFFIX = ".hack"
ASM_SUFFIX = ".asm"
NEW_LINE = '\n'
END_LINE = '\r'
TAB = '\t'
JMP_0 = "000"
CMP_0 = "0000000"
COMMENT = "//"
SPACE = " "
AT_SIGN = "@"
OPEN_PARENTHESES = "("
UNTIL_BREAK = ".*?[\n\r \t/]"
C_PREFIX = "111"
EQUALITY = ".*?="

symbols_table = {
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

jmp_values = {
    "JDT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

cmp_values = {
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


def to_pass(line):
    if line.startswith(NEW_LINE) or line.startswith(COMMENT) or line.startswith(END_LINE):
        return True
    return False


def load_symbols(old_file):
    count = 0
    for line in old_file:
        if line.startswith(NEW_LINE) or line.startswith(COMMENT) or \
                line.startswith('\r'):
            pass
        else:
            if line.startswith('('):
                regex_output = re.search("(.*)", line)
                if regex_output:
                    symbols_table[regex_output.group(0)[1:-1]] = count
            else:
                count += 1


def load_variables(old_file):
    count = 16
    old_file.seek(0)
    for line in old_file:
        if line.startswith(NEW_LINE):
            if to_pass(line):
                pass
            if line.startswith(AT_SIGN) or line.startswith((SPACE * 3) + AT_SIGN):
                if line.startswith(AT_SIGN):
                    string = line[1:]
                else:
                    string = line[4:]

                if len(string) > 0 and not string[0].isdigit():
                    regex_output = re.search(".*?[ \n\r/]", string)
                    if regex_output:
                        table_index = regex_output.group(0)[:-1]
                        if table_index not in symbols_table:
                            symbols_table[table_index] = count
                            count += 1


def parse_line_a(line, new_file):
    regex_output = re.search(UNTIL_BREAK, line)
    if regex_output:
        line = regex_output.group(0)
        line = line[:-1]

    if line in symbols_table:
        binary_number = "{0:b}".format(symbols_table[line])
    else:
        binary_number = "{0:b}".format(int(line))

    formatted_binary_number = "0"
    formatted_binary_number *= BIT_SIZE - len(binary_number)
    formatted_binary_number += binary_number
    formatted_binary_number += NEW_LINE
    new_file.write(formatted_binary_number)


def set_binary_code_dest(value, dest):
    dest_string = value[:-1]
    for symbol in dest_string:
        if symbol == 'A':
            dest[0] = '1'
        if symbol == 'D':
            dest[1] = '1'
        if symbol == 'M':
            dest[2] = '1'
    return dest


def set_binary_code_cmp(value):
    if value[0] == '=':
        value = value[1:-1]
    else:
        value = value[:-1]

    if value in cmp_values:
        return cmp_values[value]
    else:
        return CMP_0


def set_binary_code_jmp(value):
    value = value[1:-1]
    if value in jmp_values:
        return jmp_values[str]
    else:
        return JMP_0


def parse_line_c(line, new_file):
    formatted_binary_number = C_PREFIX
    dest = ['0'] * 3
    regex_output = re.search(EQUALITY, line)
    if regex_output:
        dest = set_binary_code_dest(regex_output.group(0), dest)

    cmp = ['0'] * 7
    regex_output = re.search("=.*?[; \n\r/]", line)
    if regex_output:
        cmp = set_binary_code_cmp(regex_output.group(0))
    else:
        regex_output = re.search(".*?[; \n\r/]", line)
        if regex_output:
            cmp = set_binary_code_cmp(regex_output.group(0))

    jmp = JMP_0
    regex_output = re.search(";.*?[ \n\r/]", line)
    if regex_output:
        jmp = set_binary_code_jmp(regex_output.group(0))
    formatted_binary_number = formatted_binary_number + cmp + ''.join(dest) + jmp + '\n'
    new_file.write(formatted_binary_number + '\n')


def create_file(old_file, new_file):
    old_file.seek(0)
    for line in old_file:
        if to_pass(line):
            pass
        else:
            clean_line = line
            if line.startswith(TAB):
                clean_line = line[1:]
            elif line.startswith(SPACE * 3):
                clean_line = line[3:]

            if clean_line.startswith(AT_SIGN):
                parse_line_a(clean_line[1:], new_file)
            elif not clean_line.startswith(OPEN_PARENTHESES):
                parse_line_c(clean_line, new_file)


def run_file(filename):
    with open(filename) as read_file:
        filename = os.path.splitext(filename)[0]
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
