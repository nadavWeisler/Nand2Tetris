import os
from compilationEngine import *
from utils import *

INVALID_INPUT_ERROR = "Invalid input file"
ARGUMENT_COUNT = 2
ARGUMENT_ERROR = "Invalid argument count"


class JackAnalyzer:
    def __init__(self, file_path):
        self._read_path = file_path
        self._write_path = file_path
        self._inputs = self._get_paths()

    def create_output_file(self):
        for file in self._inputs:
            output_file_name = str(os.path.basename(file).split('.')[0]) + XML_SUFFIX
            compilation = CompilationEngine(file, self._write_path + "/" + output_file_name)
            compilation.compile_class()

    def _get_paths(self):
        result = []
        if os.path.isdir(self._read_path):
            if self._read_path.endswith("/"):
                self._read_path = self._read_path[0:-1]

            files = os.listdir(self._read_path)
            lst = []
            for file in files:
                if file.endswith(JACK_SUFFIX):
                    lst.append(file)
            for file in lst:
                result.append(self._read_path + '/' + file)

        elif os.path.isfile(self._read_path):
            self._write_path = os.path.dirname(self._read_path)
            result.append(self._read_path)

        else:
            print(INVALID_INPUT_ERROR)
            sys.exit()
        return result


if __name__ == '__main__':
    if len(sys.argv) != ARGUMENT_COUNT:
        print(ARGUMENT_ERROR)
        sys.exit()
    current_input = sys.argv[1]
    analyzer = JackAnalyzer(current_input)
    analyzer.create_output_file()
