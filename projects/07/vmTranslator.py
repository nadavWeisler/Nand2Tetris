import os
import sys
import ntpath

from .writer import Writer
from .parser import Parser
from .utils import ASSEMBLY_SUFFIX, NEW_LINE


def run_program_on_file(path_src, file_write, bootstrap=False):
    """"create parser and code writer"""
    parser = Parser(path_src)
    code_writer = Writer(parser, file_write, bootstrap)
    code_writer.write_all()


if __name__ == "__main__":
    function_global_counter = 0
    counter_for_lg_gt = 0
    write_file_name = os.path.splitext(ntpath.basename(sys.argv[1]))[0]
    write_file_name += ASSEMBLY_SUFFIX
    with open(write_file_name, 'w') as out_file:
        if os.path.isdir(sys.argv[1]):
            bootstrap = True
            for root, dirs, files in os.walk(sys.argv[1], topdown=True):
                for name in files:
                    file_path = os.path.join(root, name)
                    file_suffix = os.path.splitext(name)[1]
                    if file_suffix == "vm":
                        run_program_on_file(file_path, out_file, bootstrap)
                        bootstrap = False
        else:
            run_program_on_file(sys.argv[1], out_file, bootstrap=True)
