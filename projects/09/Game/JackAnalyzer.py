import sys
import os
import ntpath
from Tokenizer import Tokenizer
from CompilationEngine import CompilationEngine


def run_program_on_file(string_path):
    """run the script on single file"""
    out_file = write_file(string_path)
    tokenizer = Tokenizer(string_path)
    compilation_engine = CompilationEngine(tokenizer, out_file)
    compilation_engine.compile_class()


def write_file(path):
    """"create write file and return it"""
    str_temp = os.path.splitext(path)[0] + ".xml"
    return open(str_temp, 'w')


# """the script should be given path as argument"""
if __name__ == "__main__":
    if os.path.isdir(sys.argv[1]):
        for root, dirs, files in os.walk(sys.argv[1], topdown=True):
            for name in files:
                string_path = os.path.join(root, name)
                string_splited = name.split('.')
                if len(string_splited) == 2:
                    if string_splited[1] == "jack":
                        run_program_on_file(string_path)
    else:
        run_program_on_file(sys.argv[1])
