import os
from utils import *


def _get_register(register_num):
    return 'R' + str(register_num)


def _get_memory_segment(segment):
    asm_label = {
        S_LCL: 'LCL',
        S_ARG: 'ARG',
        S_THIS: 'THIS',
        S_THAT: 'THAT'
    }
    return asm_label[segment]


def _register_base(segment):
    reg_base = {
        'reg': R_R0,
        'pointer': R_PTR,
        'temp': R_TEMP
    }
    return reg_base[segment]


def _register_num(segment, index):
    return _register_base(segment) + index


def _is_const_segment(segment):
    return segment == S_CONST


def _is_static_segment(segment):
    return segment == S_STATIC


def _is_register_segment(segment):
    return segment in [S_REG, S_PTR, S_TEMP]


def _is_memory_segment(segment):
    return segment in [S_LCL, S_ARG, S_THIS, S_THAT]


def _a_command(write_file, address):
    write_file.write('@' + address + NEW_LINE)


def _c_command(write_file, destination, comp, jump=None):
    if destination is not None:
        write_file.write(destination + '=')
    write_file.write(comp)
    if jump is not None:
        write_file.write(';' + jump)
    write_file.write(NEW_LINE)


def _l_command(write_file, label):
    write_file.write('(' + label + ')' + NEW_LINE)


def _register_to_destination(write_file, destination, reg):
    _a_command(write_file, _get_register(reg))
    _c_command(write_file, destination, 'M')


def _compare_to_register(write_file, reg, comp):
    _a_command(write_file, _get_register(reg))
    _c_command(write_file, 'M', comp)


def _in_folder(write_file, destination='A'):
    _c_command(write_file, destination, 'M')


def _register_to_register(write_file, destination, src):
    _register_to_destination(write_file, 'D', src)
    _compare_to_register(write_file, destination, 'D')


def _load_segment_index(write_file, seg, index, in_folder):
    comp = 'D+A'
    if index < 0:
        index = -index
        comp = 'A-D'
    _a_command(write_file, str(index))
    _c_command(write_file, 'D', 'A')
    _a_command(write_file, seg)
    if in_folder:
        _in_folder(write_file)
    _c_command(write_file, 'AD', comp)


def _load_segment_without_index(write_file, segment, in_folder):
    _a_command(write_file, segment)
    if in_folder:
        _in_folder(write_file, destination='AD')


def _load_segment(write_file, segment, index, in_folder=True):
    if index == 0:
        _load_segment_without_index(write_file, segment, in_folder)
    else:
        _load_segment_index(write_file, segment, index, in_folder)


def _load_sp_offset(write_file, offset):
    _load_segment(write_file, _get_register(R_SP), offset)


def _load_sp(write_file):
    _a_command(write_file, 'SP')
    _c_command(write_file, 'A', 'M')


def _dec_sp(write_file):
    _a_command(write_file, 'SP')
    _c_command(write_file, 'M', 'M-1')


def _inc_sp(write_file):
    _a_command(write_file, 'SP')
    _c_command(write_file, 'M', 'M+1')


def _prev_frame_to_register(write_file, register):
    _register_to_destination(write_file, 'D', R_FRAME)
    _c_command(write_file, 'D', 'D-1')
    _compare_to_register(write_file, R_FRAME, 'D')
    _c_command(write_file, 'A', 'D')
    _c_command(write_file, 'D', 'M')
    _compare_to_register(write_file, register, 'D')


def write_label(write_file, label):
    _l_command(write_file, label)


def write_goto(write_file, label):
    _a_command(write_file, label)
    _c_command(write_file, None, '0', 'JMP')


def _comp_to_stack(write_file, comp):
    _load_sp(write_file)
    _c_command(write_file, 'M', comp)


def _mem_to_stack(write_file, segment, index, in_folder=True):
    _load_segment(write_file, segment, index, in_folder)
    _c_command(write_file, 'D', 'M')
    _comp_to_stack(write_file, 'D')


def _reg_to_stack(write_file, segment, index):
    _register_to_destination(write_file, 'D', _register_num(segment, index))
    _comp_to_stack(write_file, 'D')


def _stack_to_destination(write_file, destination):
    _load_sp(write_file)
    _c_command(write_file, destination, 'M')


def _pop_to_destination(write_file, destination):
    _dec_sp(write_file)
    _stack_to_destination(write_file, destination)


def _unary_command(write_file, comp):
    _dec_sp(write_file)
    _stack_to_destination(write_file, 'D')
    _c_command(write_file, 'D', comp)
    _comp_to_stack(write_file, 'D')
    _inc_sp(write_file)


def _binary_command(write_file, comp):
    _dec_sp(write_file)
    _stack_to_destination(write_file, 'D')
    _dec_sp(write_file)
    _stack_to_destination(write_file, 'A')
    _c_command(write_file, 'D', comp)
    _comp_to_stack(write_file, 'D')
    _inc_sp(write_file)


def _val_to_stack(write_file, val):
    _a_command(write_file, val)
    _c_command(write_file, 'D', 'A')
    _comp_to_stack(write_file, 'D')


def _stack_to_register(write_file, segment, index):
    _stack_to_destination(write_file, 'D')
    _compare_to_register(write_file, _register_num(segment, index), 'D')


def _stack_to_memory(write_file, segment, index, in_folder=True):
    _load_segment(write_file, segment, index, in_folder)
    _compare_to_register(write_file, R_COPY, 'D')
    _stack_to_destination(write_file, 'D')
    _register_to_destination(write_file, 'A', R_COPY)
    _c_command(write_file, 'M', 'D')


def write_if(write_file, label):
    _pop_to_destination(write_file, 'D')
    _a_command(write_file, label)
    _c_command(write_file, None, 'D', 'JNE')


class CodeWriter(object):
    """
    Code writer class
    """

    def __init__(self, write_file):
        self.write_file = write_file
        self._vm_file = ''
        self._label_count = 0

    def set_file_name(self, filename):
        self._vm_file, extension = os.path.splitext(filename)

    def write_init(self):
        _a_command(self.write_file, '256')
        _c_command(self.write_file, 'D', 'A')
        _compare_to_register(self.write_file, R_SP, 'D')
        self.write_call('Sys.init', 0)

    def write_arithmetic(self, command):
        if command == 'add':
            _binary_command(self.write_file, 'D+A')
        elif command == 'sub':
            _binary_command(self.write_file, 'A-D')
        elif command == 'neg':
            _unary_command(self.write_file, '-D')
        elif command == 'eq':
            self._compare_command(self.write_file, 'JEQ')
        elif command == 'gt':
            self._compare_command(self.write_file, 'JGT')
        elif command == 'lt':
            self._compare_command(self.write_file, 'JLT')
        elif command == 'and':
            _binary_command(self.write_file, 'D&A')
        elif command == 'or':
            _binary_command(self.write_file, 'D|A')
        elif command == 'not':
            _unary_command(self.write_file, '!D')

    def write_push_pop(self, command, segment, index):
        if command == C_PUSH:
            self._push_command(self.write_file, segment, index)
        elif command == C_POP:
            self._pop_command(self.write_file, segment, index)

    def write_call(self, function_name, num_args):
        return_address = self._new_label()
        self._push_command(self.write_file, S_CONST, return_address)
        self._push_command(self.write_file, S_REG, R_LCL)
        self._push_command(self.write_file, S_REG, R_ARG)
        self._push_command(self.write_file, S_REG, R_THIS)
        self._push_command(self.write_file, S_REG, R_THAT)
        _load_sp_offset(self.write_file, -num_args - 5)
        _compare_to_register(self.write_file, R_ARG, 'D')
        _register_to_register(self.write_file, R_LCL, R_SP)
        _a_command(self.write_file, function_name)
        _c_command(self.write_file, None, '0', 'JMP')
        _l_command(self.write_file, return_address)

    def write_return(self):
        _register_to_register(self.write_file, R_FRAME, R_LCL)
        _a_command(self.write_file, '5')
        _c_command(self.write_file, 'A', 'D-A')
        _c_command(self.write_file, 'D', 'M')
        _compare_to_register(self.write_file, R_RET, 'D')
        self._pop_command(self.write_file, S_ARG, 0)
        _register_to_destination(self.write_file, 'D', R_ARG)
        _compare_to_register(self.write_file, R_SP, 'D+1')
        _prev_frame_to_register(self.write_file, R_THAT)
        _prev_frame_to_register(self.write_file, R_THIS)
        _prev_frame_to_register(self.write_file, R_ARG)
        _prev_frame_to_register(self.write_file, R_LCL)
        _register_to_destination(self.write_file, 'A', R_RET)
        _c_command(self.write_file, None, '0', 'JMP')

    def write_function(self, function_name, num_locals):
        _l_command(self.write_file, function_name)
        for i in range(num_locals):
            self._push_command(self.write_file, S_CONST, 0)

    def _push_command(self, write_file, segment, index):
        if _is_const_segment(segment):
            _val_to_stack(write_file, str(index))
        elif _is_memory_segment(segment):
            _mem_to_stack(write_file, _get_memory_segment(segment), index)
        elif _is_register_segment(segment):
            _reg_to_stack(write_file, segment, index)
        elif _is_static_segment(segment):
            self._static_to_stack(write_file, segment)
        _inc_sp(write_file)

    def _pop_command(self, write_file, segment, index):
        _dec_sp(write_file)
        if _is_memory_segment(segment):
            _stack_to_memory(write_file, _get_memory_segment(segment), index)
        elif _is_register_segment(segment):
            _stack_to_register(write_file, segment, index)
        elif _is_static_segment(segment):
            self._stack_to_static(write_file, index)

    def _compare_command(self, write_file, jump):
        _dec_sp(write_file)
        _stack_to_destination(write_file, 'D')
        _dec_sp(write_file)
        _stack_to_destination(write_file, 'A')
        _c_command(write_file, 'D', 'A-D')
        label_eq = self._jump(write_file, 'D', jump)
        _comp_to_stack(write_file, '0')
        label_ne = self._jump(write_file, '0', 'JMP')
        _l_command(write_file, label_eq)
        _comp_to_stack(write_file, '-1')
        _l_command(write_file, label_ne)
        _inc_sp(write_file)

    def _static_to_stack(self, write_file, index):
        _a_command(write_file, self._get_static_name(index))
        _c_command(write_file, 'D', 'M')
        _comp_to_stack(write_file, 'D')

    def _stack_to_static(self, write_file, index):
        _stack_to_destination(write_file, 'D')
        _a_command(write_file, self._get_static_name(index))
        _c_command(write_file, 'M', 'D')

    def _get_static_name(self, index):
        return self._vm_file + '.' + str(index)

    def _jump(self, write_file, comp, jump):
        label = self._new_label()
        _a_command(write_file, label)
        _c_command(write_file, None, comp, jump)
        return label

    def _new_label(self):
        self._label_count += 1
        return 'LABEL' + str(self._label_count)
