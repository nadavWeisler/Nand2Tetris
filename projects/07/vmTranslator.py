from vm_parser import Parser
from writer import CodeWriter
from glob import glob
import sys
import os


def get_files(input_path):
    if input_path.endswith('.vm'):
        return [input_path]
    else:
        return glob(input_path + '/*.vm')


def translate_file(code_writer, file_name):
    parse = Parser(file_name)
    while parse.got_more_commands():
        parse.advance()
        if parse.command_type() == "C_ARITHMETIC":
            code_writer.write_arithmetic(parse.argument_1())
        elif parse.command_type() == "C_PUSH" or parse.command_type() == "C_POP":
            code_writer.write_push_pop(parse.command_type(), parse.argument_1(), parse.argument_2())


def main():
    if len(sys.argv) != 2:
        print("Usage: Bad amount of parameters")
    else:
        read_file = get_files(sys.argv[1])
        for file_path in read_file:
            with open(os.path.splitext(file_path)[0] + ".asm", 'w+') as w:
                translate_file(CodeWriter(w), file_path)


if __name__ == '__main__':
    main()
