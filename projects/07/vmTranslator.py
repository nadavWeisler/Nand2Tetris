import os
import sys
import ntpath

import vm_parser
import utils
import writer


def run_program(path_src, file_write, boots=False):
    """"
    Create parser and code writer
    """
    current_parser = vm_parser.Parser(path_src)
    code_writer = writer.Writer(current_parser, file_write, boots)
    code_writer.write_all()


if __name__ == "__main__":
    function_global_counter = 0
    counter_for_lg_gt = 0
    write_file_name = os.path.splitext(ntpath.basename(sys.argv[1]))[0]
    write_file_name += utils.ASSEMBLY_SUFFIX
    with open(write_file_name, 'w') as out_file:
        if os.path.isdir(sys.argv[1]):
            bootstrap = True
            for root, dirs, files in os.walk(sys.argv[1], topdown=True):
                for name in files:
                    file_path = os.path.join(root, name)
                    file_suffix = os.path.splitext(name)[1]
                    if file_suffix == utils.VM_SUFFIX:
                        run_program(file_path, out_file, bootstrap)
                        bootstrap = False
        else:
            run_program(sys.argv[1], out_file, boots=True)
