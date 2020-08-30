NEW_LINE = "\n"


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


class CodeWriter:
    def __init__(self, file):
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

    def write_arithmetic(self, command):
        self.label_count += 1
        loop = "LOOP" + str(self.label_count)
        end = "END" + str(self.label_count)
        if command == "eq":
            ln = get_eg_command_line(end, loop)
        elif command == "lt":
            ln = get_lt_command_line(end, loop)
        elif command == "gt":
            ln = get_gt_command_line(end, loop)
        else:
            ln = self.arithmetic[command]
        self.out_file.write(ln + NEW_LINE)

    def write_push_pop(self, command, segment, index):
        ln = ""
        if command == "C_PUSH":
            ln = self.get_push_command_line(index, ln, segment)
        elif command == "C_POP":
            ln = self.get_pop_command_line(index, ln, segment)
        self.out_file.write(ln + NEW_LINE)

    def get_pop_command_line(self, index, ln, segment):
        if segment == "local":
            ln = "@" + index + NEW_LINE + \
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
        if segment == "argument":
            ln = "@" + index + "" + NEW_LINE + \
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
        if segment == "this":
            ln = "@" + index + NEW_LINE + \
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
        if segment == "that":
            ln = "@" + index + NEW_LINE + \
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
        if segment == "pointer":
            ln = "@" + index + NEW_LINE + \
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
        if segment == "temp":
            ln = "@" + index + NEW_LINE + \
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
        if segment == "static":
            ln = "@SP" + NEW_LINE + \
                 "M=M-1" + NEW_LINE + \
                 "A=M" + NEW_LINE + \
                 "D=M" + NEW_LINE + \
                 "@" + self.out_file.name + "." + index + NEW_LINE + \
                 "M=D"
        return ln

    def get_push_command_line(self, index, ln, segment):
        if segment == "local":
            ln = "@" + index + NEW_LINE + \
                 "D=A" + NEW_LINE + \
                 "@LCL" + NEW_LINE + \
                 "A=M+D" + NEW_LINE + \
                 "D=M" + NEW_LINE + \
                 "@SP" + NEW_LINE + \
                 "A=M" + NEW_LINE + \
                 "M=D" + NEW_LINE + \
                 "@SP" + NEW_LINE + \
                 "M=M+1"
        if segment == "constant":
            ln = "@" + index + NEW_LINE + \
                 "D=A" + NEW_LINE + \
                 "@SP" + NEW_LINE + \
                 "A=M" + NEW_LINE + \
                 "M=D" + NEW_LINE + \
                 "@SP" + NEW_LINE + \
                 "M=M+1"
        if segment == "argument":
            ln = "@" + index + NEW_LINE + \
                 "D=A" + NEW_LINE + \
                 "@ARG" + NEW_LINE + \
                 "A=M+D" + NEW_LINE + \
                 "D=M" + NEW_LINE + \
                 "@SP" + NEW_LINE + \
                 "A=M" + NEW_LINE + \
                 "M=D" + NEW_LINE + \
                 "@SP" + NEW_LINE + \
                 "M=M+1"
        if segment == "this":
            ln = "@" + index + NEW_LINE + \
                 "D=A" + NEW_LINE + \
                 "@THIS" + NEW_LINE + \
                 "A=M+D" + NEW_LINE + \
                 "D=M" + NEW_LINE + \
                 "@SP" + NEW_LINE + \
                 "A=M" + NEW_LINE + \
                 "M=D" + NEW_LINE + \
                 "@SP" + NEW_LINE + \
                 "M=M+1"
        if segment == "that":
            ln = "@" + index + NEW_LINE + \
                 "D=A" + NEW_LINE + \
                 "@THAT" + NEW_LINE + \
                 "A=M+D" + NEW_LINE + \
                 "D=M" + NEW_LINE + \
                 "@SP" + NEW_LINE + \
                 "A=M" + NEW_LINE + \
                 "M=D" + NEW_LINE + \
                 "@SP" + NEW_LINE + \
                 "M=M+1"
        if segment == "pointer":
            ln = "@" + index + NEW_LINE + \
                 "D=A" + NEW_LINE + \
                 "@THIS" + NEW_LINE \
                 + "A=A+D" + NEW_LINE + \
                 "D=M" + NEW_LINE + \
                 "@SP" + NEW_LINE + \
                 "A=M" + NEW_LINE + \
                 "M=D" + NEW_LINE + \
                 "@SP" + NEW_LINE + \
                 "M=M+1"
        if segment == "temp":
            ln = "@" + index + NEW_LINE + \
                 "D=A" + NEW_LINE + \
                 "@5" + NEW_LINE + \
                 "A=A+D" + NEW_LINE + \
                 "D=M" + NEW_LINE + \
                 "@SP" + NEW_LINE + \
                 "A=M" + NEW_LINE + \
                 "M=D" + NEW_LINE + \
                 "@SP" + NEW_LINE + \
                 "M=M+1"
        if segment == "static":
            ln = "@" + self.out_file.name + "." + index + NEW_LINE + \
                 "D=M" + NEW_LINE + \
                 "@SP" + NEW_LINE + \
                 "A=M" + NEW_LINE + \
                 "M=D" + NEW_LINE + \
                 "@SP" + NEW_LINE + \
                 "M=M+1"
        return ln
