from utils import NEW_LINE, SegmentsTypes


def get_gt_command_line(end, loop):
    ln = "@SP" + NEW_LINE + \
         "M=M-1" + NEW_LINE + \
         "A=M" + NEW_LINE + \
         "D=M" + NEW_LINE + \
         "A=A-1" + NEW_LINE + \
         "M=M-D" + NEW_LINE + \
         "D=M" + NEW_LINE + \
         "@" + loop + NEW_LINE
    ln += "D;JLE" + NEW_LINE + \
          "@SP" + NEW_LINE + \
          "M=M-1" + NEW_LINE + \
          "A=M" + NEW_LINE + \
          "M=-1" + NEW_LINE + \
          "@" + end + "" + NEW_LINE + \
          "0;JMP" + NEW_LINE + \
          "(" + loop + ")" + NEW_LINE + \
          "@SP" + NEW_LINE + \
          "M=M-1" + NEW_LINE + \
          "A=M" + NEW_LINE + \
          "M=0" + NEW_LINE + \
          "(" + end + ")" + NEW_LINE + \
          "@SP" + NEW_LINE + \
          "M=M+1"
    return ln


def get_lt_command_line(end, loop):
    ln = "@SP" + NEW_LINE + \
         "M=M-1" + NEW_LINE + \
         "A=M" + NEW_LINE + \
         "D=M" + NEW_LINE + \
         "A=A-1" + NEW_LINE + \
         "M=M-D" + NEW_LINE + \
         "D=M" + NEW_LINE + \
         "@" + loop + NEW_LINE
    ln += "D;JGE" + NEW_LINE + \
          "@SP" + NEW_LINE + \
          "M=M-1" + NEW_LINE + \
          "A=M" + NEW_LINE + \
          "M=-1" + NEW_LINE + \
          "@" + end + NEW_LINE + \
          "0;JMP" + NEW_LINE + \
          "(" + loop + ")" + NEW_LINE + \
          "@SP" + NEW_LINE + \
          "M=M-1" + NEW_LINE + \
          "A=M" + NEW_LINE + \
          "M=0" + NEW_LINE + \
          "(" + end + ")" + NEW_LINE + \
          "@SP" + NEW_LINE + \
          "M=M+1"
    return ln


def get_eg_command_line(end, loop):
    ln = "@SP" + NEW_LINE + \
         "M=M-1" + NEW_LINE + \
         "A=M" + NEW_LINE + \
         "D=M" + NEW_LINE + \
         "A=A-1" + NEW_LINE + \
         "M=M-D" + NEW_LINE + \
         "D=M" + NEW_LINE + \
         "@" + loop + NEW_LINE
    ln += "D;JNE" + NEW_LINE + \
          "@SP" + NEW_LINE + \
          "M=M-1" + NEW_LINE + \
          "A=M" + NEW_LINE + \
          "M=-1" + NEW_LINE + \
          "@" + end + NEW_LINE + \
          "0;JMP" + NEW_LINE + \
          "(" + loop + ")" + NEW_LINE + \
          "@SP" + NEW_LINE + \
          "M=M-1" + NEW_LINE + \
          "A=M" + NEW_LINE + \
          "M=0" + NEW_LINE + \
          "(" + end + ")" + NEW_LINE + \
          "@SP" + NEW_LINE + \
          "M=M+1"
    return ln


def get_push_local_line(index):
    return "@" + index + NEW_LINE + \
           "D=A" + NEW_LINE + \
           "@LCL" + NEW_LINE + \
           "A=M+D" + NEW_LINE + \
           "D=M" + NEW_LINE + \
           "@SP" + NEW_LINE + \
           "A=M" + NEW_LINE + \
           "M=D" + NEW_LINE + \
           "@SP" + NEW_LINE + \
           "M=M+1"


def get_push_constant_line(index):
    return "@" + index + NEW_LINE + \
           "D=A" + NEW_LINE + \
           "@SP" + NEW_LINE + \
           "A=M" + NEW_LINE + \
           "M=D" + NEW_LINE + \
           "@SP" + NEW_LINE + \
           "M=M+1"


def get_push_argument_line(index):
    return "@" + index + NEW_LINE + \
           "D=A" + NEW_LINE + \
           "@ARG" + NEW_LINE + \
           "A=M+D" + NEW_LINE + \
           "D=M" + NEW_LINE + \
           "@SP" + NEW_LINE + \
           "A=M" + NEW_LINE + \
           "M=D" + NEW_LINE + \
           "@SP" + NEW_LINE + \
           "M=M+1"


def get_push_this_line(index):
    return "@" + index + NEW_LINE + \
           "D=A" + NEW_LINE + \
           "@THIS" + NEW_LINE + \
           "A=M+D" + NEW_LINE + \
           "D=M" + NEW_LINE + \
           "@SP" + NEW_LINE + \
           "A=M" + NEW_LINE + \
           "M=D" + NEW_LINE + \
           "@SP" + NEW_LINE + \
           "M=M+1"


def get_push_that_line(index):
    return "@" + index + NEW_LINE + \
           "D=A" + NEW_LINE + \
           "@THAT" + NEW_LINE + \
           "A=M+D" + NEW_LINE + \
           "D=M" + NEW_LINE + \
           "@SP" + NEW_LINE + \
           "A=M" + NEW_LINE + \
           "M=D" + NEW_LINE + \
           "@SP" + NEW_LINE + \
           "M=M+1"


def get_push_pointer_line(index):
    return "@" + index + NEW_LINE + \
           "D=A" + NEW_LINE + \
           "@THIS" + NEW_LINE \
           + "A=A+D" + NEW_LINE + \
           "D=M" + NEW_LINE + \
           "@SP" + NEW_LINE + \
           "A=M" + NEW_LINE + \
           "M=D" + NEW_LINE + \
           "@SP" + NEW_LINE + \
           "M=M+1"


def get_push_temp_line(index):
    return "@" + index + NEW_LINE + \
           "D=A" + NEW_LINE + \
           "@5" + NEW_LINE + \
           "A=A+D" + NEW_LINE + \
           "D=M" + NEW_LINE + \
           "@SP" + NEW_LINE + \
           "A=M" + NEW_LINE + \
           "M=D" + NEW_LINE + \
           "@SP" + NEW_LINE + \
           "M=M+1"


def get_pop_temp_line(index):
    return "@" + index + NEW_LINE + \
           "D=A" + NEW_LINE \
           + "@5" + NEW_LINE + \
           "D=D+A" + NEW_LINE + \
           "@13" + NEW_LINE + \
           "M=D" + NEW_LINE + \
           "@SP" + NEW_LINE + \
           "M=M-1" + NEW_LINE + \
           "A=M" + NEW_LINE + \
           "D=M" + NEW_LINE + \
           "@13" + NEW_LINE + \
           "A=M" + NEW_LINE + \
           "M=D"


def get_pop_pointer_line(index):
    return "@" + index + NEW_LINE + \
           "D=A" + NEW_LINE + \
           "@THIS" + NEW_LINE + \
           "D=D+A" + NEW_LINE + \
           "@13" + NEW_LINE + \
           "M=D" + NEW_LINE + \
           "@SP" + NEW_LINE + \
           "M=M-1" + NEW_LINE + \
           "A=M" + NEW_LINE + \
           "D=M" + NEW_LINE + \
           "@13" + NEW_LINE + \
           "A=M" + NEW_LINE + \
           "M=D"


def get_pop_that_line(index):
    return "@" + index + NEW_LINE + \
           "D=A" + NEW_LINE + \
           "@THAT" + NEW_LINE + \
           "D=D+M" + NEW_LINE + \
           "@13" + NEW_LINE + \
           "M=D" + NEW_LINE + \
           "@SP" + NEW_LINE + \
           "M=M-1" + NEW_LINE + \
           "A=M" + NEW_LINE + \
           "D=M" + NEW_LINE + \
           "@13" + NEW_LINE + \
           "A=M" + NEW_LINE + \
           "M=D"


def get_pop_this_line(index):
    return "@" + index + NEW_LINE + \
           "D=A" + NEW_LINE + \
           "@THIS" + NEW_LINE + \
           "D=D+M" + NEW_LINE + \
           "@13" + NEW_LINE + \
           "M=D" + NEW_LINE + \
           "@SP" + NEW_LINE + \
           "M=M-1" + NEW_LINE + \
           "A=M" + NEW_LINE + \
           "D=M" + NEW_LINE + \
           "@13" + NEW_LINE + \
           "A=M" + NEW_LINE + \
           "M=D"


def get_pop_argument_line(index):
    return "@" + index + "" + NEW_LINE + \
           "D=A" + NEW_LINE + \
           "@ARG" + NEW_LINE + \
           "D=D+M" + NEW_LINE + \
           "@13" + NEW_LINE + \
           "M=D" + NEW_LINE + \
           "@SP" + NEW_LINE + \
           "M=M-1" + NEW_LINE + \
           "A=M" + NEW_LINE + \
           "D=M" + NEW_LINE + \
           "@13" + NEW_LINE + \
           "A=M" + NEW_LINE + \
           "M=D"


def get_pop_local_line(index):
    return "@" + index + NEW_LINE + \
           "D=A" + NEW_LINE + \
           "@LCL" + NEW_LINE + \
           "D=D+M" + NEW_LINE + \
           "@13" + NEW_LINE + \
           "M=D" + NEW_LINE + \
           "@SP" + NEW_LINE + \
           "M=M-1" + NEW_LINE + \
           "A=M" + NEW_LINE + \
           "D=M" + NEW_LINE + \
           "@13" + NEW_LINE + \
           "A=M" + NEW_LINE + \
           "M=D"


class CodeWriter:
    def __init__(self, file, init_file=False):
        self.arithmetic = {
            "add": "@SP" + NEW_LINE +
                   "M=M-1" + NEW_LINE +
                   "A=M" + NEW_LINE +
                   "D=M" + NEW_LINE +
                   "A=A-1" + NEW_LINE +
                   "M=M+D" + NEW_LINE,
            "sub": "@SP" + NEW_LINE +
                   "M=M-1" + NEW_LINE +
                   "A=M" + NEW_LINE +
                   "D=M" + NEW_LINE +
                   "A=A-1" + NEW_LINE +
                   "M=M-D" + NEW_LINE,
            "neg": "@SP" + NEW_LINE +
                   "A=M-1" + NEW_LINE +
                   "M=-M" + NEW_LINE,
            "and": "@SP" + NEW_LINE +
                   "M=M-1" + NEW_LINE +
                   "A=M" + NEW_LINE +
                   "D=M" + NEW_LINE +
                   "A=A-1" + NEW_LINE +
                   "M=M&D" + NEW_LINE,
            "or": "@SP" + NEW_LINE +
                  "M=M-1" + NEW_LINE +
                  "A=M" + NEW_LINE +
                  "D=M" + NEW_LINE +
                  "A=A-1" + NEW_LINE +
                  "M=M|D" + NEW_LINE,
            "not": "@SP" + NEW_LINE +
                   "A=M-1" + NEW_LINE +
                   "M=!M" + NEW_LINE
        }
        self.label_count = 0
        self.out_file = file
        if init_file:
            self._write_init_file()

    def _write_init_file(self):
        new_line = "@256" + NEW_LINE + \
                   "D=A" + NEW_LINE + \
                   "@SP" + NEW_LINE + \
                   "M=D" + NEW_LINE + \
                   "@300" + NEW_LINE + \
                   "D=A" + NEW_LINE + \
                   "@LCL" + NEW_LINE + \
                   "M=D" + NEW_LINE + \
                   "@400" + NEW_LINE + \
                   "D=A" + NEW_LINE + \
                   "@ARG" + NEW_LINE + \
                   "M=D" + NEW_LINE + \
                   "@3000" + NEW_LINE + \
                   "D=A" + NEW_LINE + \
                   "@THIS" + NEW_LINE + \
                   "M=D" + NEW_LINE + \
                   "@4000" + NEW_LINE + \
                   "D=A" + NEW_LINE + \
                   "@THAT" + NEW_LINE + \
                   "M=D"
        self._write_line(new_line)
        self.write_call("Sys.init", '0')

    def write_arithmetic(self, command):
        self.label_count += 1
        loop = "LOOP" + str(self.label_count)
        end = "END" + str(self.label_count)
        if command == "eq":
            new_line = get_eg_command_line(end, loop)
        elif command == "lt":
            new_line = get_lt_command_line(end, loop)
        elif command == "gt":
            new_line = get_gt_command_line(end, loop)
        else:
            new_line = self.arithmetic[command]
        self._write_line(new_line + NEW_LINE)

    def write_push(self, segment, index):
        self._write_line(self.get_push_command_line(index, segment))

    def write_pop(self, segment, index):
        self._write_line(self.get_pop_command_line(index, segment))

    def write_label(self, label):
        self._write_line("(" + label + ")")

    def write_return(self):
        new_line = '@LCL' + NEW_LINE + \
                   'D=M' + NEW_LINE + \
                   '@FRAME' + NEW_LINE + \
                   'M=D' + NEW_LINE + \
                   '@FRAME' + NEW_LINE + \
                   'D=M' + NEW_LINE + \
                   '@5' + NEW_LINE + \
                   'D=D-A' + NEW_LINE + \
                   'A=D' + NEW_LINE + \
                   'D=M' + NEW_LINE + \
                   '@RET' + NEW_LINE + \
                   'M=D' + NEW_LINE + \
                   '@SP' + NEW_LINE + \
                   'D=M' + NEW_LINE + \
                   'D=D-1' + NEW_LINE + \
                   'A=D' + NEW_LINE + \
                   'D=M' + NEW_LINE + \
                   '@ARG' + NEW_LINE + \
                   'A=M' + NEW_LINE + \
                   'M=D' + NEW_LINE + \
                   '@ARG' + NEW_LINE + \
                   'D=M' + NEW_LINE + \
                   'D=D+1' + NEW_LINE + \
                   '@SP' + NEW_LINE + \
                   'M=D' + NEW_LINE + \
                   '@FRAME' + NEW_LINE + \
                   'D=M' + NEW_LINE + \
                   'D=D-1' + NEW_LINE + \
                   'A=D' + NEW_LINE + \
                   'D=M' + NEW_LINE + \
                   '@THAT' + NEW_LINE + \
                   'M=D' + NEW_LINE + \
                   '@FRAME' + NEW_LINE + \
                   'D=M' + NEW_LINE + \
                   '@2' + NEW_LINE + \
                   'D=D-A' + NEW_LINE + \
                   'A=D' + NEW_LINE + \
                   'D=M' + NEW_LINE + \
                   '@THIS' + NEW_LINE + \
                   'M=D' + NEW_LINE + \
                   '@FRAME' + NEW_LINE + \
                   'D=M' + NEW_LINE + \
                   '@3' + NEW_LINE + \
                   'D=D-A' + NEW_LINE + \
                   'A=D' + NEW_LINE + \
                   'D=M' + NEW_LINE + \
                   '@ARG' + NEW_LINE + \
                   'M=D' + NEW_LINE + \
                   '@FRAME' + NEW_LINE + \
                   'D=M' + NEW_LINE + \
                   '@4' + NEW_LINE + \
                   'D=D-A' + NEW_LINE + \
                   'A=D' + NEW_LINE + \
                   'D=M' + NEW_LINE + \
                   '@LCL' + NEW_LINE + \
                   'M=D' + NEW_LINE + \
                   '@RET' + NEW_LINE + \
                   'A=M' + NEW_LINE + \
                   '0;JMP'
        self._write_line(new_line)

    def write_goto(self, label):
        new_line = "@" + label + NEW_LINE + \
                   "0;JMP"
        self._write_line(new_line)

    def write_if(self, label):
        new_line = "@SP" + NEW_LINE + \
                   "M=M-1" + NEW_LINE + \
                   "A=M" + NEW_LINE + \
                   "D=M" + NEW_LINE + \
                   "A=A-1" + NEW_LINE + \
                   "@" + label + NEW_LINE + \
                   "D;JNE"
        self._write_line(new_line)

    def write_call(self, function_name, args):
        self.label_count += 1
        return_line = "RETURN" + str(self.label_count)
        new_line = get_push_constant_line(return_line) + NEW_LINE + \
                   "@LCL" + NEW_LINE + \
                   "D=M" + NEW_LINE + \
                   "@SP" + NEW_LINE + \
                   "A=M" + NEW_LINE + \
                   "M=D" + NEW_LINE + \
                   "@SP" + NEW_LINE + \
                   "M=M+1" + NEW_LINE + \
                   "@ARG" + NEW_LINE + \
                   "D=M" + NEW_LINE + \
                   "@SP" + NEW_LINE + \
                   "A=M" + NEW_LINE + \
                   "M=D" + NEW_LINE + \
                   "@SP" + NEW_LINE + \
                   "M=M+1" + NEW_LINE + \
                   "@THIS" + NEW_LINE + \
                   "D=M" + NEW_LINE + \
                   "@SP" + NEW_LINE + \
                   "A=M" + NEW_LINE + \
                   "M=D" + NEW_LINE + \
                   "@SP" + NEW_LINE + \
                   "M=M+1" + NEW_LINE + \
                   "@THAT" + NEW_LINE + \
                   "D=M" + NEW_LINE + \
                   "@SP" + NEW_LINE + \
                   "A=M" + NEW_LINE + \
                   "M=D" + NEW_LINE + \
                   "@SP" + NEW_LINE + \
                   "M=M+1" + NEW_LINE + \
                   "@SP" + NEW_LINE + \
                   "D=M" + NEW_LINE + \
                   "@" + args + NEW_LINE + \
                   "D=D-A" + NEW_LINE + \
                   "@5" + NEW_LINE + \
                   "D=D-A" + NEW_LINE + \
                   "@ARG" + NEW_LINE + \
                   "M=D" + NEW_LINE + \
                   "@SP" + NEW_LINE + \
                   "D=M" + NEW_LINE + \
                   "@LCL" + NEW_LINE + \
                   "M=D" + NEW_LINE + \
                   "@" + function_name + NEW_LINE + \
                   "0;JMP" + NEW_LINE + \
                   "(" + return_line + ")"
        self._write_line(new_line)

    def get_pop_command_line(self, index, segment):
        new_line = ""
        if segment == SegmentsTypes().Local:
            new_line = get_pop_local_line(index)
        if segment == SegmentsTypes().Argument:
            new_line = get_pop_argument_line(index)
        if segment == SegmentsTypes().This:
            new_line = get_pop_this_line(index)
        if segment == SegmentsTypes().That:
            new_line = get_pop_that_line(index)
        if segment == SegmentsTypes().Pointer:
            new_line = get_pop_pointer_line(index)
        if segment == SegmentsTypes().Temp:
            new_line = get_pop_temp_line(index)
        if segment == SegmentsTypes().Static:
            new_line = self.get_pop_static_line(index)
        return new_line

    def get_pop_static_line(self, index):
        return "@SP" + NEW_LINE + \
               "M=M-1" + NEW_LINE + \
               "A=M" + NEW_LINE + \
               "D=M" + NEW_LINE + \
               "@" + self.out_file.name + "." + index + NEW_LINE + \
               "M=D"

    def get_push_command_line(self, index, segment):
        new_line = ""
        if segment == SegmentsTypes().Local:
            new_line = get_push_local_line(index)
        elif segment == SegmentsTypes().Constant:
            new_line = get_push_constant_line(index)
        elif segment == SegmentsTypes().Argument:
            new_line = get_push_argument_line(index)
        elif segment == SegmentsTypes().This:
            new_line = get_push_this_line(index)
        elif segment == SegmentsTypes().That:
            new_line = get_push_that_line(index)
        elif segment == SegmentsTypes().Pointer:
            new_line = get_push_pointer_line(index)
        elif segment == SegmentsTypes().Temp:
            new_line = get_push_temp_line(index)
        elif segment == SegmentsTypes().Static:
            new_line = self.get_push_static_line(index)
        return new_line

    def get_push_static_line(self, index):
        return "@" + self.out_file.name + "." + index + NEW_LINE + \
               "D=M" + NEW_LINE + \
               "@SP" + NEW_LINE + \
               "A=M" + NEW_LINE + \
               "M=D" + NEW_LINE + \
               "@SP" + NEW_LINE + \
               "M=M+1"

    def write_function(self, function_name, var_count):
        self.label_count += 1
        new_line = '(' + function_name + ')' + NEW_LINE + \
                   '@' + var_count + NEW_LINE + \
                   'D=A' + NEW_LINE + \
                   '@i' + NEW_LINE + \
                   'M=D' + NEW_LINE + \
                   'D=M' + NEW_LINE + \
                   '@' + function_name + '.' + var_count + NEW_LINE + \
                   'D;JEQ' + NEW_LINE + \
                   '(' + function_name + '..' + var_count + ')' + NEW_LINE + \
                   '@SP' + NEW_LINE + \
                   'A=M' + NEW_LINE + \
                   'M=0' + NEW_LINE + \
                   '@SP' + NEW_LINE + \
                   'D=M' + NEW_LINE + \
                   'D=D+1' + NEW_LINE + \
                   'M=D' + NEW_LINE + \
                   '@i' + NEW_LINE + \
                   'D=M' + NEW_LINE + \
                   'D=D-1' + NEW_LINE + \
                   'M=D' + NEW_LINE + \
                   '@' + function_name + '..' + var_count + NEW_LINE + \
                   'D;JNE' + NEW_LINE + \
                   '(' + function_name + '.' + var_count + ')'
        self._write_line(new_line)

    def _write_line(self, line):
        self.out_file.write(line + NEW_LINE)
