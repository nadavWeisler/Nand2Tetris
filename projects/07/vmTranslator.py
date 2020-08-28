import sys
import os
from glob import glob
from vm_parser import Parser
from writer import CodeWriter
from utils import *


def _get_code(parser, code_writer):
    cmd = parser.command_type()
    if cmd == C_ARITHMETIC:
        code_writer.write_arithmetic(parser.argument_1())
    elif cmd == C_PUSH or cmd == C_POP:
        code_writer.write_push_pop(cmd, parser.argument_1(), parser.argument_2())
    elif cmd == C_LABEL:
        code_writer.write_label(parser.argument_1())
    elif cmd == C_GOTO:
        code_writer.write_goto(parser.argument_1())
    elif cmd == C_IF:
        code_writer.write_if(parser.argument_1())
    elif cmd == C_FUNCTION:
        code_writer.write_function(parser.argument_1(), parser.argument_2())
    elif cmd == C_RETURN:
        code_writer.write_return()
    elif cmd == C_CALL:
        code_writer.write_call(parser.argument_1(), parser.argument_2())


def _translate(infile, code_writer):
    parser = Parser(infile)
    code_writer.set_file_name(os.path.basename(infile))
    while parser.has_more_commands():
        parser.advance()
        _get_code(parser, code_writer)


def translate_all(read_file, out_file):
    if read_file:
        code_writer = CodeWriter(out_file)
        code_writer.write_init()
        _translate(read_file, code_writer)


def get_files(file_or_dir):
    if file_or_dir.endswith('.vm'):
        return [file_or_dir]
    else:
        return glob(file_or_dir + '/*.vm')


def main():
    if len(sys.argv) != 2:
        print("Usage: Bad amount of params")
    else:
        read_file = get_files(sys.argv[1])
        for file_path in read_file:
            with open(os.path.splitext(file_path)[0] + ".asm", 'w+') as w:
                translate_all(file_path, w)


if __name__ == '__main__':
    main()
