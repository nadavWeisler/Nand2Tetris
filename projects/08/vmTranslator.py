import ntpath
import sys
import os
from glob import glob

from vm_parser import Parser
from writer import CodeWriter
from utils import *


def get_files(input_path):
    if input_path.endswith(VM_SUFFIX):
        return [input_path]
    else:
        return glob(input_path + '/*' + VM_SUFFIX)


def translate_file(code_writer, file_name):
    parse = Parser(file_name)
    while parse.got_more_commands():
        parse.advance()
        write_command(code_writer, parse)


def write_command(code_writer, parse):
    if parse.command_type() == CommandsTypes().Arithmetic:
        code_writer.write_arithmetic(parse.argument_1())
    elif parse.command_type() == CommandsTypes().Push:
        code_writer.write_push(parse.argument_1(),
                               parse.argument_2())
    elif parse.command_type() == CommandsTypes().Pop:
        code_writer.write_pop(parse.argument_1(),
                              parse.argument_2())
    elif parse.command_type() == CommandsTypes().Label:
        code_writer.write_label(parse.argument_1())
    elif parse.command_type() == CommandsTypes().Function:
        code_writer.write_function(parse.argument_1(),
                                   parse.argument_2())
    elif parse.command_type() == CommandsTypes().Call:
        code_writer.write_call(parse.argument_1(),
                               parse.argument_2())
    elif parse.command_type() == CommandsTypes().Return:
        code_writer.write_return()
    elif parse.command_type() == CommandsTypes().Goto:
        code_writer.write_goto(parse.argument_1())
    elif parse.command_type() == CommandsTypes().If:
        code_writer.write_if(parse.argument_1())


def main():
    if os.path.isdir(sys.argv[1]):
        write_file = os.path.join(sys.argv[1], os.path.basename(sys.argv[1]) + ASM_SUFFIX)
    else:
        write_file = sys.argv[1].replace(VM_SUFFIX, ASM_SUFFIX)

    with open(write_file, FilePermissions().WritePlus) as w:
        if os.path.isdir(sys.argv[1]):
            writer = CodeWriter(w, True)
            for root, dirs, files in os.walk(sys.argv[1], topdown=True):
                for f in files:
                    if os.path.splitext(f)[1] == VM_SUFFIX:
                        translate_file(writer, os.path.join(root, f))
        else:
            writer = CodeWriter(w)
            translate_file(writer, sys.argv[1])


if __name__ == '__main__':
    main()
