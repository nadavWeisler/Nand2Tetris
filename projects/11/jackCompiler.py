from compilationEngine import *
from jackTokenizer import *
import sys
import os


def analyze(file_name):
    tokenizer = JackTokenizer(file_name)
    tokenizer.tokenize()
    CompilationEngine(tokenizer).write(file_name.replace(JACK_SUFFIX, VM_SUFFIX))


if __name__ == '__main__':
    for arg in sys.argv[1:]:
        if os.path.isdir(arg):
            for filename in os.listdir(arg):
                filename = os.path.join(arg, filename)
                if filename.endswith(JACK_SUFFIX):
                    analyze(filename)
        elif os.path.isfile(arg):
            analyze(arg)
