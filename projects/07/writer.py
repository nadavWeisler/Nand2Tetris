from os import path
import utils

RET = "15"
FRAME = "14"
SP = '0'

ARITHMETICS = {
    "add", "neg", "sub",
    "or", "not", "and",
    "gt", "lt", "eq"
}

# Symbols to meanings
SYMBOLS_TABLE = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "temp": 5,
    "stack": 256,
}

# Keyword to address
TRANSITION_TO_ADDRESS = {
    "local": 1,
    "argument": 2,
    "this": 3,
    "that": 4,
}


def create_function_return(function_name):
    """
    create the name of asm function
    """
    Writer.function_global_counter += 1
    return function_name + '$ret.' + str(Writer.function_global_counter)


class Writer:
    function_global_counter = 0
    lg_gt_counter = 0

    def __init__(self, parser, output_file, bootstrap=False):
        """
        constructor
        """
        self.out_file = output_file
        self.parser = parser
        self.file_name = path.splitext(self.parser.file.name)[0]
        self.current_function = ""
        if bootstrap:
            self._write_line_to_file("@256")
            self._write_line_to_file("D=A")
            self._write_line_to_file("@0")
            self._write_line_to_file("M=D")
            self._create_call("BOOTSTRAP_RETURN_ADDRESS", "Sys.init", '0')

    def write_all(self):
        while not self.parser.end_of_file:
            if self.parser.get_command() == utils.Commands.Arithmetic:
                self._write_arithmetic()
            elif self.parser.get_command() == utils.Commands.Push or \
                    self.parser.get_command() == utils.Commands.Pop:
                self._write_push_pop(self.parser.get_command(),
                                     self.parser.get_argument1(),
                                     self.parser.get_argument2())
            elif self.parser.get_command() == utils.Commands.Label:
                self._write_label()
            elif self.parser.get_command() == utils.Commands.Goto:
                self._write_goto()
            elif self.parser.get_command() == utils.Commands.If:
                self._write_if()
            elif self.parser.get_command() == utils.Commands.Function:
                self._write_function()
            elif self.parser.get_command() == utils.Commands.Call:
                self._write_line_to_file("// CALL")
                self._create_call(self.current_function,
                                  self.parser.get_argument1(),
                                  self.parser.get_argument2())
            elif self.parser.get_command() == utils.Commands.Return:
                self._write_return()
            self.parser.read_line()

    def _write_return(self):
        """write return asm code"""
        self._write_line_to_file("// FRAME=LCL")

        # FRAME=LCL
        self._write_line_to_file('@' + str(SYMBOLS_TABLE["LCL"]))
        self._write_line_to_file("D=M")
        self._write_line_to_file('@' + FRAME)
        self._write_line_to_file("M=D")

        # RET=*(FRAME-5)
        self._write_line_to_file("// RET=*(FRAME-5))")
        self._write_line_to_file("@5")
        self._write_line_to_file("A=D-A")
        self._write_line_to_file("D=M")
        self._write_line_to_file('@' + RET)
        self._write_line_to_file("M=D")

        # *ARG=pop()
        self._write_line_to_file("// *ARG=pop()")
        self._decrease_SP_and_read_to_d()
        self._write_line_to_file('@' + str(SYMBOLS_TABLE["ARG"]))
        self._write_line_to_file("A=M")
        self._write_line_to_file("M=D")

        # SP=ARG+1
        self._write_line_to_file("// SP=ARG+1")
        self._write_line_to_file('@' + str(SYMBOLS_TABLE["ARG"]))
        self._write_line_to_file("D=M")
        self._write_line_to_file('@' + str(SYMBOLS_TABLE["SP"]))
        self._write_line_to_file("M=D+1")

        # THAT=*(FRAME-1)
        self._write_line_to_file("// THAT=*(FRAME-1)")
        self._decrease_frame_by_one_and_load_into_d()
        self._write_line_to_file('@' + str(SYMBOLS_TABLE["THAT"]))
        self._write_line_to_file("M=D")

        # THIS=*(FRAME-2)
        self._write_line_to_file("// THIS=*(FRAME-2)")
        self._decrease_frame_by_one_and_load_into_d()
        self._write_line_to_file('@' + str(SYMBOLS_TABLE["THIS"]))
        self._write_line_to_file("M=D")

        # ARG=*(FRAME-3)
        self._write_line_to_file("// ARG=*(FRAME-3)")
        self._decrease_frame_by_one_and_load_into_d()
        self._write_line_to_file('@' + str(SYMBOLS_TABLE["ARG"]))
        self._write_line_to_file("M=D")

        # LCL=*(FRAME-4)
        self._write_line_to_file("// LCL=*(FRAME-4)")
        self._decrease_frame_by_one_and_load_into_d()
        self._write_line_to_file('@' + str(SYMBOLS_TABLE["LCL"]))
        self._write_line_to_file("M=D")

        # GOTO RET
        self._write_line_to_file("// GOTO RET")
        self._write_line_to_file('@' + RET)
        self._write_line_to_file("A=M")
        self._write_line_to_file("0;JMP")

    def _write_function(self):
        """
        write asm code - function
        """
        self._write_line_to_file("// FUNCTION")
        self.current_function = self.parser.get_argument1()
        self._write_line_to_file('(' + self.current_function + ')')
        for x in range(int(self.parser.get_argument2())):
            self._write_line_to_file("@0")
            self._write_line_to_file("D=A")
            self._load_value_from_d()
            self._stack_pointer_inc()

    def _write_if(self):
        """
        write asm code - IF-GOTO
        """
        self._write_line_to_file("// IF")
        self._decrease_SP_and_read_to_d()
        label = self._create_label()
        self._write_line_to_file('@' + label)
        self._write_line_to_file("D;JNE")

    def _write_goto(self):
        """
        write asm code - GOTO
        """
        self._write_line_to_file("// GOTO")
        self._write_line_to_file('@' + self._create_label())
        self._write_line_to_file("0;JMP")

    def _create_call(self, curr_function, function_to_jump, args_num):
        """
        write asm code - CALL
        """
        ret_label = create_function_return(curr_function)
        self._write_line_to_file("// Push ret address")
        self._add_value_to_stack(ret_label)
        self._write_line_to_file("// Push LCL")
        self._write_line_to_file('@' + str(SYMBOLS_TABLE["LCL"]))
        self._stack_adding()
        self._write_line_to_file("// Push ARG")
        self._write_line_to_file('@' + str(SYMBOLS_TABLE["ARG"]))
        self._stack_adding()
        self._write_line_to_file("// Push THIS")
        self._write_line_to_file('@' + str(SYMBOLS_TABLE["THIS"]))
        self._stack_adding()
        self._write_line_to_file("// Push THAT")
        self._write_line_to_file('@' + str(SYMBOLS_TABLE["THAT"]))
        self._stack_adding()
        self._write_line_to_file("// ARG = SP  -5 -nARGS")
        self._write_line_to_file('@' + str(SYMBOLS_TABLE["SP"]))
        self._write_line_to_file("D=M")
        self._write_line_to_file("@5")
        self._write_line_to_file("D=D-A")
        self._write_line_to_file("@" + args_num)
        self._write_line_to_file("D=D-A")
        self._write_line_to_file('@' + str(SYMBOLS_TABLE["ARG"]))
        self._write_line_to_file("M=D")
        self._write_line_to_file("// LCL = SP")
        self._write_line_to_file('@' + str(SYMBOLS_TABLE["SP"]))
        self._write_line_to_file("D=M")
        self._write_line_to_file('@' + str(SYMBOLS_TABLE["LCL"]))
        self._write_line_to_file("M=D")
        self._write_line_to_file('@' + function_to_jump)
        self._write_line_to_file("0;JMP")
        self._write_line_to_file('(' + ret_label + ')')

    def _decrease_frame_by_one_and_load_into_d(self):
        """
        decrease frame by one and load its value into D
        """
        self._write_line_to_file('@' + FRAME)
        self._write_line_to_file("M=M-1")
        self._write_line_to_file("A=M")
        self._write_line_to_file("D=M")

    def _write_label(self):
        """
        write asm code - label
        """
        temp_str = self._create_label()
        self._write_line_to_file('(' + temp_str + ')')

    def _create_label(self):
        """
        create label according to naming conventions
        """
        return self.current_function + '$' + self.parser.get_arg1()

    def _write_arithmetic(self):
        """
        Writer for arithmetic function
        """
        if self.parser.get_argument1() == utils.Arithmetics.Add:
            self._write_add()
        if self.parser.get_argument1() == utils.Arithmetics.Sub:
            self._write_sub()
        if self.parser.get_argument1() == utils.Arithmetics.Neg:
            self._write_neg()
        if self.parser.get_argument1() == utils.Arithmetics.Not:
            self._write_not()
        if self.parser.get_argument1() == utils.Arithmetics.And:
            self._write_and()
        if self.parser.get_argument1() == utils.Arithmetics.Eq:
            self._write_eq()
        if self.parser.get_argument1() == utils.Arithmetics.Or:
            self._write_or()
        if self.parser.get_argument1() == utils.Arithmetics.Gt:
            self._write_gt()
        if self.parser.get_argument1() == utils.Arithmetics.Lt:
            self._write_lt()

    def _write_sub(self):
        """
        write sub arithmetic
        """
        self._write_line_to_file("// sub")
        self._decrease_SP_and_read_to_d()
        self._decrease_stack_pointer_and_read_into_a()
        self._write_line_to_file("D=M-D")
        self._read_from_d_into_stack()

    def _write_add(self):
        """
        write add arithmetic
        """
        self._write_line_to_file("// add")
        self._decrease_SP_and_read_to_d()
        self._decrease_stack_pointer_and_read_into_a()
        self._write_line_to_file("D=D+M")
        self._read_from_d_into_stack()

    def _write_neg(self):
        """
        write neg arithmetic
        """
        self._write_line_to_file("// neg")
        self._decrease_SP_and_read_to_d()
        self._write_line_to_file("D=-D")
        self._read_from_d_into_stack()

    def _write_not(self):
        """
        write not arithmetic
        """
        self._write_line_to_file("// not")
        self._decrease_SP_and_read_to_d()
        self._write_line_to_file("D=!D")
        self._read_from_d_into_stack()

    def _write_and(self):
        """
        write and arithmetic
        """
        self._write_line_to_file("// and")
        self._decrease_SP_and_read_to_d()
        self._decrease_stack_pointer_and_read_into_a()
        self._write_line_to_file("D=D&M")
        self._read_from_d_into_stack()

    def _write_eq(self):
        """
        write eq arithmetic
        """
        self._write_line_to_file("// eq")
        self._decrease_SP_and_read_to_d()
        self._decrease_stack_pointer_and_read_into_a()
        self._write_line_to_file("A=M")
        self._write_line_to_file("D=D-A")
        self._write_line_to_file("@TRUE" + str(Writer.lg_gt_counter))
        self._write_line_to_file("D;JEQ")
        self._end_g_l_gate()

    def _write_or(self):
        """
        write or arithmetic
        """
        self._write_line_to_file("// or")
        self._decrease_SP_and_read_to_d()
        self._decrease_stack_pointer_and_read_into_a()
        self._write_line_to_file("D=D|M")
        self._read_from_d_into_stack()

    def _write_gt(self):
        """
        for gt function (greater than)
        """
        self._write_line_to_file("// gt")
        self._decrease_SP_and_read_to_d()
        self._write_line_to_file("@YBIGGERTHANZERO" + str(Writer.lg_gt_counter))
        self._write_line_to_file("D;JGE")
        # y bigger than zero
        self._write_line_to_file("@R13")
        # y loaded into R13
        self._write_line_to_file("M=D")
        self._decrease_SP_and_read_to_d()
        # if x>=0 than it must be true
        self._write_line_to_file("@TRUE" + str(Writer.lg_gt_counter))

        self._write_line_to_file("D;JGE")
        self._write_line_to_file("@R13")
        # d = x - y
        self._write_line_to_file("D=D-M")
        self._write_line_to_file("@TRUE" + str(Writer.lg_gt_counter))
        self._write_line_to_file("D;JGT")
        # second part x >= 0
        self._print_label_with_lg_gt_counter("YBIGGERTHANZERO")
        self._write_line_to_file("@R13")
        # y loaded into R13
        self._write_line_to_file("M=D")
        self._decrease_SP_and_read_to_d()
        # if x<=0 than it must be false
        self._write_line_to_file("@FALSE" + str(Writer.lg_gt_counter))
        self._write_line_to_file("D;JLE")
        # if y>0 and x<=0 than it must be false
        self._write_line_to_file("@R13")
        # d = x - y
        self._write_line_to_file("D=D-M")
        self._write_line_to_file("@TRUE" + str(Writer.lg_gt_counter))
        self._write_line_to_file("D;JGT")
        # false
        self._print_label_with_lg_gt_counter("FALSE")
        self._end_g_l_gate()

    def _write_lt(self):
        """
        for lt function (less than)
        """
        self._write_line_to_file("// lt")
        self._decrease_SP_and_read_to_d()
        self._write_line_to_file("@YBIGGERTHANZERO" + str(Writer.lg_gt_counter))
        self._write_line_to_file("D;JGE")
        self._write_line_to_file("@R13")
        self._write_line_to_file("M=D")
        self._decrease_SP_and_read_to_d()
        self._write_line_to_file("@FALSE" + str(Writer.lg_gt_counter))
        self._write_line_to_file("D;JGE")
        self._write_line_to_file("@R13")
        self._write_line_to_file("D=D-M")
        self._write_line_to_file("@FALSE" + str(Writer.lg_gt_counter))
        self._write_line_to_file("D;JGE")
        self._print_label_with_lg_gt_counter("YBIGGERTHANZERO")
        self._write_line_to_file("@R13")
        self._write_line_to_file("M=D")
        self._decrease_SP_and_read_to_d()
        self._write_line_to_file("@TRUE" + str(Writer.lg_gt_counter))
        self._write_line_to_file("D;JLE")
        self._write_line_to_file("@R13")
        self._write_line_to_file("D=D-M")
        self._write_line_to_file("@TRUE" + str(Writer.lg_gt_counter))
        self._write_line_to_file("D;JLT")
        self._print_label_with_lg_gt_counter("FALSE")
        self._end_g_l_gate()

    def _end_g_l_gate(self):
        self._write_line_to_file("@0")
        self._write_line_to_file("D=A")
        self._write_line_to_file("@END" + str(Writer.lg_gt_counter))
        self._write_line_to_file("0;JMP")
        self._print_label_with_lg_gt_counter("TRUE")
        self._write_line_to_file("D=-1")
        self._print_label_with_lg_gt_counter("END")
        self._load_value_from_d()
        self._stack_pointer_inc()
        Writer.lg_gt_counter += 1

    def _print_label_with_lg_gt_counter(self, label):
        """
        print with counter
        """
        self._write_line_to_file("(" + label + str(Writer.lg_gt_counter) + ")")

    def _decrease_stack_pointer_and_read_into_a(self):
        """
        Read into A variable
        """
        self._write_line_to_file("@" + SP)
        self._write_line_to_file("M=M-1")
        self._write_line_to_file("@0")
        self._write_line_to_file("A=M")

    def _read_from_d_into_stack(self):
        """
        Read to D variable
        """
        self._write_line_to_file("@0")
        self._write_line_to_file("A=M")
        self._write_line_to_file("M=D")
        self._stack_pointer_inc()

    def _write_push_pop(self, command, arg1, arg2):
        """
        Write push or pop commands
        """
        if command == utils.Commands.Push:
            self._write_line_to_file("// Push")
            self._write_push(arg1, arg2)
        if command == utils.Commands.Pop:
            self._write_line_to_file("// Pop")
            if arg1 == "temp":
                place_in_stack = str(5 + int(arg2))
                self._decrease_SP_and_read_to_d()
                self._write_line_to_file("@" + place_in_stack)
                self._write_line_to_file("M=D")
            elif arg1 in TRANSITION_TO_ADDRESS:
                self._write_line_to_file("@" + str(TRANSITION_TO_ADDRESS[arg1]))
                self._write_line_to_file("D=M")
                self._write_line_to_file("@" + arg2)
                self._write_line_to_file("D=A+D")
                self._write_line_to_file("@" + str(TRANSITION_TO_ADDRESS[arg1]))
                self._write_line_to_file("M=D")
                self._decrease_SP_and_read_to_d()
                self._write_line_to_file("@" + str(TRANSITION_TO_ADDRESS[arg1]))
                self._write_line_to_file("A=M")
                self._write_line_to_file("M=D")
                self._write_line_to_file("@" + str(TRANSITION_TO_ADDRESS[arg1]))
                self._write_line_to_file("D=M")
                self._write_line_to_file("@" + arg2)
                self._write_line_to_file("D=D-A")
                self._write_line_to_file("@" + str(TRANSITION_TO_ADDRESS[arg1]))
                self._write_line_to_file("M=D")
            elif arg1 == "static":
                str_stack_var_name = str(self.file_name) + '.' + str(arg2)
                self._decrease_SP_and_read_to_d()
                self._write_line_to_file("@" + str_stack_var_name)
                self._write_line_to_file("M=D")
            elif arg1 == "pointer":
                if arg2 == SP:
                    this_or_that = SYMBOLS_TABLE["THIS"]
                else:
                    this_or_that = SYMBOLS_TABLE["THAT"]
                self._decrease_SP_and_read_to_d()
                self._write_line_to_file("@" + str(this_or_that))
                self._write_line_to_file("M=D")

    def _decrease_SP_and_read_to_d(self):
        """
        Decrease SP and read its content to D
        """
        self._decrease_stack_pointer_and_read_into_a()
        self._write_line_to_file("D=M")

    def _write_push(self, arg1, arg2):
        """
        Push creation
        """
        if arg1 == "temp":
            place_in_stack = str(5 + int(arg2))
            self._write_line_to_file("@" + place_in_stack)
            self._stack_adding()
        elif arg1 in TRANSITION_TO_ADDRESS:
            self._write_line_to_file("@" + str(TRANSITION_TO_ADDRESS[arg1]))
            self._write_line_to_file("D=M")
            self._write_line_to_file("@" + arg2)
            self._write_line_to_file("A=D+A")
            self._stack_adding()
        elif arg1 == "constant":
            self._add_value_to_stack(arg2)
        elif arg1 == "static":
            str_stack_var_name = str(self.file_name) + '.' + str(arg2)
            self._write_line_to_file("@" + str_stack_var_name)
            self._write_line_to_file("D=M")
            self._load_value_from_d()
            self._stack_pointer_inc()
        elif arg1 == "pointer":
            if arg2 == SP:
                this_or_that = SYMBOLS_TABLE["THIS"]
            else:
                this_or_that = SYMBOLS_TABLE["THAT"]
            self._write_line_to_file("@" + str(this_or_that))
            self._write_line_to_file("D=M")
            self._load_value_from_d()
            self._stack_pointer_inc()

    def _add_value_to_stack(self, value):
        """
        add value to stack
        """
        self._write_line_to_file("@" + str(value))
        self._write_line_to_file("D=A")
        self._load_value_from_d()
        self._stack_pointer_inc()

    def _stack_adding(self):
        """
        add to stack from D
        """
        self._write_line_to_file("D=M")
        self._load_value_from_d()
        self._stack_pointer_inc()

    def _load_value_from_d(self):
        """
        load value from D
        """
        self._write_line_to_file("@0")
        self._write_line_to_file("A=M")
        self._write_line_to_file("M=D")

    def _stack_pointer_inc(self):
        """
        increment stack pointer(SP) by 1
        """
        self._write_line_to_file("@" + SP)
        self._write_line_to_file("M=M+1")

    def _write_line_to_file(self, string_to_write):
        """
        write line to file
        """
        self.out_file.write(string_to_write + utils.NEW_LINE)
