from .parser import Commands
from os import path
from .utils import Arithmetics, NEW_LINE

RET = "15"
FRAME = "14"
SP = '0'

ARITHMETICS = {
    "add", "neg", "sub",
    "or", "not", "and",
    "gt", "lt", "eq"
}

# translate symbols into their meanings
SYMBOLS_TABLE = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "temp": 5,
    "stack": 256,
}

# transition keyword into right address
TRANSITION_TO_ADDRESS = {
    "local": 1,
    "argument": 2,
    "this": 3,
    "that": 4,
}


def create_function_return(function_name):
    """static function to create the name of asm function"""
    tmp = function_name + '$ret.' + str(Writer.function_global_counter)
    Writer.function_global_counter += 1
    return tmp


class Writer:
    # static variables
    function_global_counter = 0
    counter_for_lg_gt = 0

    def __init__(self, parser, output_file, bootstrap=False):
        """constructor, create the file"""
        self.out_file = output_file
        self.parser = parser
        self.file_name = path.basename(self.parser.file.name)
        self.file_name = self.file_name.split('.')[0]
        self.current_function = ""  # to know which function I'm currently in
        if bootstrap:
            self._write_line_to_file("@256")
            self._write_line_to_file("D=A")
            self._write_line_to_file("@0")
            self._write_line_to_file("M=D")
            self._create_call("BOOTSTRAP_RETURN_ADDRESS", "Sys.init", '0')

    def write_all(self):
        while not self.parser.end_of_file:
            if self.parser.get_command() == Commands.Arithmetic:
                self._write_arithmetic()
            elif self.parser.get_command() == Commands.Push or \
                    self.parser.get_command() == Commands.Pop:
                self._write_push_pop(self.parser.get_command(),
                                     self.parser.get_argument1(),
                                     self.parser.get_argument2())
            elif self.parser.get_command() == Commands.Label:
                self._write_label()
            elif self.parser.get_command() == Commands.Goto:
                self._write_goto()
            elif self.parser.get_command() == Commands.If:
                self._write_if()
            elif self.parser.get_command() == Commands.Function:
                self._write_function()
            elif self.parser.get_command() == Commands.Call:
                self._write_line_to_file("// CALL")
                self._create_call(self.current_function, self.parser.get_arg1(
                ), self.parser.get_arg2())
            elif self.parser.get_command() == Commands.Return:
                self._write_return()
            self.parser.read_line()

    def _write_return(self):
        """write return asm code"""
        self._write_line_to_file("//  FRAME=LCL")
        # FRAME=LCL
        self._write_line_to_file('@' + str(SYMBOLS_TABLE["LCL"]))
        self._write_line_to_file("D=M")
        self._write_line_to_file('@' + FRAME)
        self._write_line_to_file("M=D")
        # RET=*(FRAME-5)
        self._write_line_to_file("//  RET=*(FRAME-5))")
        self._write_line_to_file("@5")
        self._write_line_to_file("A=D-A")
        self._write_line_to_file("D=M")
        self._write_line_to_file('@' + RET)
        self._write_line_to_file("M=D")
        self._write_line_to_file("//  *ARG=pop()")
        # *ARG=pop()
        self._decrease_SP_and_read_into_d()
        self._write_line_to_file('@' + str(SYMBOLS_TABLE["ARG"]))
        self._write_line_to_file("A=M")
        self._write_line_to_file("M=D")
        self._write_line_to_file("//  SP=ARG+1")
        # SP=ARG+1
        self._write_line_to_file('@' + str(SYMBOLS_TABLE["ARG"]))
        self._write_line_to_file("D=M")
        self._write_line_to_file('@' + str(SYMBOLS_TABLE["SP"]))
        self._write_line_to_file("M=D+1")
        self._write_line_to_file("//  THAT=*(FRAME-1)")
        # THAT=*(FRAME-1)
        self._decrease_frame_by_one_and_load_into_d()
        self._write_line_to_file('@' + str(SYMBOLS_TABLE["THAT"]))
        self._write_line_to_file("M=D")
        self._write_line_to_file("//  THIS=*(FRAME-2)")
        # THIS=*(FRAME-2)
        self._decrease_frame_by_one_and_load_into_d()
        self._write_line_to_file('@' + str(SYMBOLS_TABLE["THIS"]))
        self._write_line_to_file("M=D")
        self._write_line_to_file("//  ARG=*(FRAME-3)")
        # ARG=*(FRAME-3)
        self._decrease_frame_by_one_and_load_into_d()
        self._write_line_to_file('@' + str(SYMBOLS_TABLE["ARG"]))
        self._write_line_to_file("M=D")
        self._write_line_to_file("//  LCL=*(FRAME-4)")
        # LCL=*(FRAME-4)
        self._decrease_frame_by_one_and_load_into_d()
        self._write_line_to_file('@' + str(SYMBOLS_TABLE["LCL"]))
        self._write_line_to_file("M=D")
        self._write_line_to_file("//  GOTO RET")
        # GOTO RET
        self._write_line_to_file('@' + RET)
        self._write_line_to_file("A=M")
        self._write_line_to_file("0;JMP")

    def _write_function(self):
        """write function asm code"""
        self._write_line_to_file("// FUNCTION")
        self.current_function = self.parser.get_arg1()
        self._write_line_to_file('(' + self.current_function + ')')
        for x in range(int(self.parser.get_arg2())):
            self._write_line_to_file("@0")
            self._write_line_to_file("D=A")
            self._load_from_d()
            self._increment_stack_pointer()

    def _write_if(self):
        """write IF-GOTO asm code"""
        self._write_line_to_file("// IF")
        self._decrease_SP_and_read_into_d()
        label = self._create_label()
        self._write_line_to_file('@' + label)
        self._write_line_to_file("D;JNE")

    def _write_goto(self):
        """write GOTO asm code"""
        self._write_line_to_file("// GOTO")
        label = self._create_label()
        self._write_line_to_file('@' + label)
        self._write_line_to_file("0;JMP")

    def _create_call(self, curr_function, function_to_jump, args_num):
        """write CALL asm code"""
        ret_label = create_function_return(curr_function)
        self._write_line_to_file("//  push ret address")
        self._value_into_stack(ret_label)
        self._write_line_to_file("//  push LCL")
        self._write_line_to_file('@' + str(SYMBOLS_TABLE["LCL"]))
        self._add_to_stack()
        self._write_line_to_file("//  push ARG")
        self._write_line_to_file('@' + str(SYMBOLS_TABLE["ARG"]))
        self._add_to_stack()
        self._write_line_to_file("//  push THIS")
        self._write_line_to_file('@' + str(SYMBOLS_TABLE["THIS"]))
        self._add_to_stack()
        self._write_line_to_file("//  push THAT")
        self._write_line_to_file('@' + str(SYMBOLS_TABLE["THAT"]))
        self._add_to_stack()
        self._write_line_to_file("//  ARG = SP  -5 -nARGS")
        self._write_line_to_file('@' + str(SYMBOLS_TABLE["SP"]))
        self._write_line_to_file("D=M")
        self._write_line_to_file("@5")
        self._write_line_to_file("D=D-A")
        self._write_line_to_file("@" + args_num)
        self._write_line_to_file("D=D-A")
        self._write_line_to_file('@' + str(SYMBOLS_TABLE["ARG"]))
        self._write_line_to_file("M=D")
        self._write_line_to_file("//  LCL = SP")
        self._write_line_to_file('@' + str(SYMBOLS_TABLE["SP"]))
        self._write_line_to_file("D=M")
        self._write_line_to_file('@' + str(SYMBOLS_TABLE["LCL"]))
        self._write_line_to_file("M=D")
        self._write_line_to_file('@' + function_to_jump)
        self._write_line_to_file("0;JMP")
        self._write_line_to_file('(' + ret_label + ')')

    def _decrease_frame_by_one_and_load_into_d(self):
        """decrease frame by one and load its value into D"""
        self._write_line_to_file('@' + FRAME)
        self._write_line_to_file("M=M-1")
        self._write_line_to_file("A=M")
        self._write_line_to_file("D=M")

    def _write_label(self):
        """write LABEL asm code"""
        temp_str = self._create_label()
        self._write_line_to_file('(' + temp_str + ')')

    def _create_label(self):
        """create label according to naming conventions"""
        return self.current_function + '$' + self.parser.get_arg1()

    def _write_arithmetic(self):
        """Writer for any arithmetic function"""
        if self.parser.get_arg1() == Arithmetics.Add:
            self._write_add()
        if self.parser.get_arg1() == Arithmetics.Sub:
            self._write_sub()
        if self.parser.get_arg1() == Arithmetics.Neg:
            self._write_neg()
        if self.parser.get_arg1() == Arithmetics.Not:
            self._write_not()
        if self.parser.get_arg1() == Arithmetics.And:
            self._write_and()
        if self.parser.get_arg1() == Arithmetics.Eq:
            self._write_eq()
        if self.parser.get_arg1() == Arithmetics.Or:
            self._write_or()
        if self.parser.get_arg1() == Arithmetics.Gt:
            self._write_line_to_file("// gt")
            self._gt()
        if self.parser.get_arg1() == Arithmetics.Lt:
            self._write_line_to_file("// lt")
            self._lt()

    def _write_sub(self):
        """write sub arithmetic"""
        self._write_line_to_file("// sub")
        self._decrease_SP_and_read_into_d()
        self._decrease_stack_pointer_and_read_into_a()
        self._write_line_to_file("D=M-D")
        self._read_from_d_into_stack()

    def _write_add(self):
        """write add arithmetic"""
        self._write_line_to_file("// add")
        self._decrease_SP_and_read_into_d()
        self._decrease_stack_pointer_and_read_into_a()
        self._write_line_to_file("D=D+M")
        self._read_from_d_into_stack()

    def _write_neg(self):
        """write neg arithmetic"""
        self._write_line_to_file("// neg")
        self._decrease_SP_and_read_into_d()
        self._write_line_to_file("D=-D")
        self._read_from_d_into_stack()

    def _write_not(self):
        """write not arithmetic"""
        self._write_line_to_file("// not")
        self._decrease_SP_and_read_into_d()
        self._write_line_to_file("D=!D")
        self._read_from_d_into_stack()

    def _write_and(self):
        """write and arithmetic"""
        self._write_line_to_file("// and")
        self._decrease_SP_and_read_into_d()
        self._decrease_stack_pointer_and_read_into_a()
        self._write_line_to_file("D=D&M")
        self._read_from_d_into_stack()

    def _write_eq(self):
        """write eq arithmetic"""
        self._write_line_to_file("// eq")
        self._decrease_SP_and_read_into_d()
        self._decrease_stack_pointer_and_read_into_a()
        self._write_line_to_file("A=M")
        self._write_line_to_file("D=D-A")
        self._print_with_counter_for_lg_gt("@TRUE")
        self._write_line_to_file("D;JEQ")
        self._method_name()

    def _write_or(self):
        """write or arithmetic"""
        self._write_line_to_file("// or")
        self._decrease_SP_and_read_into_d()
        self._decrease_stack_pointer_and_read_into_a()
        self._write_line_to_file("D=D|M")
        self._read_from_d_into_stack()

    def _gt(self):
        """for gt function (greater than)"""
        self._decrease_SP_and_read_into_d()
        self._print_with_counter_for_lg_gt("@YBIGGERTHANZERO")
        self._write_line_to_file("D;JGE")
        # y bigger than zero
        self._write_line_to_file("@R13")
        # y loaded into R13
        self._write_line_to_file("M=D")
        self._decrease_SP_and_read_into_d()
        # if x>=0 than it must be true
        self._print_with_counter_for_lg_gt("@TRUE")
        self._write_line_to_file("D;JGE")
        self._write_line_to_file("@R13")
        # d = x - y
        self._write_line_to_file("D=D-M")
        self._print_with_counter_for_lg_gt("@TRUE")
        self._write_line_to_file("D;JGT")
        # second part x >= 0
        self._print_label_with_counter_for_lg_gt("YBIGGERTHANZERO")
        self._write_line_to_file("@R13")
        # y loaded into R13
        self._write_line_to_file("M=D")
        self._decrease_SP_and_read_into_d()
        # if x<=0 than it must be false
        self._print_with_counter_for_lg_gt("@FALSE")
        self._write_line_to_file("D;JLE")
        # if y>0 and x<=0 than it must be false
        self._write_line_to_file("@R13")
        # d = x - y
        self._write_line_to_file("D=D-M")
        self._print_with_counter_for_lg_gt("@TRUE")
        self._write_line_to_file("D;JGT")
        # false
        self._print_label_with_counter_for_lg_gt("FALSE")
        self._method_name()

    def _lt(self):
        """for lt function (less than)"""
        self._decrease_SP_and_read_into_d()
        self._print_with_counter_for_lg_gt("@YBIGGERTHANZERO")
        self._write_line_to_file("D;JGE")
        # y bigger than zero
        self._write_line_to_file("@R13")
        # y loaded into R13
        self._write_line_to_file("M=D")
        self._decrease_SP_and_read_into_d()
        # if x>=0 than it must be false
        self._print_with_counter_for_lg_gt("@FALSE")
        self._write_line_to_file("D;JGE")
        self._write_line_to_file("@R13")
        # d = x - y
        self._write_line_to_file("D=D-M")
        self._print_with_counter_for_lg_gt("@FALSE")
        self._write_line_to_file("D;JGE")
        # second part x >= 0
        self._print_label_with_counter_for_lg_gt("YBIGGERTHANZERO")
        self._write_line_to_file("@R13")
        # y loaded into R13
        self._write_line_to_file("M=D")
        self._decrease_SP_and_read_into_d()
        # if x<=0 than it must be false
        self._print_with_counter_for_lg_gt("@TRUE")
        self._write_line_to_file("D;JLE")
        # if y>0 and x<=0 than it must be false
        self._write_line_to_file("@R13")
        # d = x - y
        self._write_line_to_file("D=D-M")
        self._print_with_counter_for_lg_gt("@TRUE")
        self._write_line_to_file("D;JLT")

        self._print_label_with_counter_for_lg_gt("FALSE")
        self._method_name()

    def _method_name(self):
        self._write_line_to_file("@0")
        self._write_line_to_file("D=A")
        self._print_with_counter_for_lg_gt("@END")
        self._write_line_to_file("0;JMP")
        # if true
        self._print_label_with_counter_for_lg_gt("TRUE")
        self._write_line_to_file("D=-1")
        self._print_label_with_counter_for_lg_gt("END")
        self._load_from_d()
        self._increment_stack_pointer()
        Writer.counter_for_lg_gt += 1

    def _print_with_counter_for_lg_gt(self, string):
        """print with counter (so label from diffrent parts in the program
        wont have the smae label)"""
        self._write_line_to_file(string + str(Writer.counter_for_lg_gt))

    def _print_label_with_counter_for_lg_gt(self, label):
        """print with counter (so label from different parts in the program
        wont have the same label)"""
        self._write_line_to_file(
            "(" + label + str(Writer.counter_for_lg_gt) + ")")

    def _decrease_stack_pointer_and_read_into_a(self):
        """read into a vraialbe (and SP--)"""
        self._decrement_stack_pointer()
        self._write_line_to_file("@0")
        self._write_line_to_file("A=M")

    def _read_from_d_into_stack(self):
        """read into d vraialbe (and SP--)"""
        self._write_line_to_file("@0")
        self._write_line_to_file("A=M")
        self._write_line_to_file("M=D")
        self._increment_stack_pointer()

    def _write_push_pop(self, command, arg1, arg2):
        """write the code for any push or pop commands"""
        if command == command.C_PUSH:
            self._write_line_to_file("// push")
            self._write_push(arg1, arg2)
        if command == command.C_POP:
            self._write_line_to_file("// pop")
            if arg1 == "temp":
                place_in_stack = str(5 + int(arg2))
                self._decrease_SP_and_read_into_d()
                self._write_line_to_file("@" + place_in_stack)
                self._write_line_to_file("M=D")
            elif arg1 in TRANSITION_TO_ADDRESS:
                self._write_line_to_file("@" + str(TRANSITION_TO_ADDRESS[
                                                       arg1]))
                self._write_line_to_file("D=M")
                self._write_line_to_file("@" + arg2)
                self._write_line_to_file("D=A+D")
                self._write_line_to_file("@" + str(TRANSITION_TO_ADDRESS[
                                                       arg1]))
                self._write_line_to_file("M=D")
                self._decrease_SP_and_read_into_d()
                self._write_line_to_file("@" + str(TRANSITION_TO_ADDRESS[
                                                       arg1]))
                self._write_line_to_file("A=M")
                self._write_line_to_file("M=D")
                self._write_line_to_file("@" + str(TRANSITION_TO_ADDRESS[
                                                       arg1]))
                self._write_line_to_file("D=M")
                self._write_line_to_file("@" + arg2)
                self._write_line_to_file("D=D-A")
                self._write_line_to_file("@" + str(TRANSITION_TO_ADDRESS[
                                                       arg1]))
                self._write_line_to_file("M=D")

            elif arg1 == "static":
                str_stack_var_name = str(self.file_name) + '.' + str(arg2)
                self._decrease_SP_and_read_into_d()
                self._write_line_to_file("@" + str_stack_var_name)
                self._write_line_to_file("M=D")
            elif arg1 == "pointer":
                if arg2 == SP:
                    this_or_that = SYMBOLS_TABLE["THIS"]
                else:
                    this_or_that = SYMBOLS_TABLE["THAT"]
                self._decrease_SP_and_read_into_d()
                self._write_line_to_file("@" + str(this_or_that))
                self._write_line_to_file("M=D")

    def _decrease_SP_and_read_into_d(self):
        """decrease SP and read its content into d"""
        self._decrease_stack_pointer_and_read_into_a()
        self._write_line_to_file("D=M")

    def _write_push(self, arg1, arg2):
        """method resposible for creating push"""
        if arg1 == "temp":
            place_in_stack = str(5 + int(arg2))
            self._write_line_to_file("@" + place_in_stack)
            self._add_to_stack()
        elif arg1 in TRANSITION_TO_ADDRESS:
            self._write_line_to_file("@" + str(TRANSITION_TO_ADDRESS[arg1]))
            self._write_line_to_file("D=M")
            self._write_line_to_file("@" + arg2)
            self._write_line_to_file("A=D+A")
            self._add_to_stack()
        elif arg1 == "constant":
            self._value_into_stack(arg2)
        elif arg1 == "static":
            str_stack_var_name = str(self.file_name) + '.' + str(arg2)
            self._write_line_to_file("@" + str_stack_var_name)
            self._write_line_to_file("D=M")
            self._load_from_d()
            self._increment_stack_pointer()
        elif arg1 == "pointer":
            if arg2 == SP:
                this_or_that = SYMBOLS_TABLE["THIS"]
            else:
                this_or_that = SYMBOLS_TABLE["THAT"]
            self._write_line_to_file("@" + str(this_or_that))
            self._write_line_to_file("D=M")
            self._load_from_d()
            self._increment_stack_pointer()

    def _value_into_stack(self, value):
        """add value into stack"""
        self._write_line_to_file("@" + str(value))
        self._write_line_to_file("D=A")
        self._load_from_d()
        self._increment_stack_pointer()

    def _add_to_stack(self):
        """add to stack from D value"""
        self._write_line_to_file("D=M")
        self._load_from_d()
        self._increment_stack_pointer()

    def _load_from_d(self):
        """load value from D"""
        self._write_line_to_file("@0")
        self._write_line_to_file("A=M")
        self._write_line_to_file("M=D")

    def _increment_stack_pointer(self):
        """increment stack pointer by 1, SP++"""
        self._increment_var(SP)

    def _increment_var(self, var):
        """increment var by 1, var++"""
        self._write_line_to_file("@" + var)
        self._write_line_to_file("M=M+1")

    def _decrement_var(self, var):
        """decrement var by 1, var--"""
        self._write_line_to_file("@" + var)
        self._write_line_to_file("M=M-1")

    def _decrement_stack_pointer(self):
        """decrement stack pointer by 1, SP--"""
        self._decrement_var(SP)

    def _write_line_to_file(self, string_to_write):
        """write the string into file and add new line"""
        self.out_file.write(string_to_write + NEW_LINE)
