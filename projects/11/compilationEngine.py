from Symbol import *
from SymbolTable import *
from vmWriter import *
from utils import *


class CompilationEngine:
    def __init__(self, tokenizer):
        self._writer = VmWriter()
        self._current_class = None
        self._current_function = None
        self._current_function_type = None
        self._subroutine_table = None
        self._class_table = []
        self._tokenizer = tokenizer
        self._result = []
        self.counters = {
            'static': 0, 'field': 0,
            'argument': 0, 'local': 0
        }
        self.labels_counters = {
            "if": 0,
            "while": 0
        }
        self.compile_class()

    def write(self, file_name):
        self._writer.write(file_name)

    def reset_label(self):
        for label_counter in self.labels_counters:
            self.labels_counters[label_counter] = 0

    def terminal(self, var_type, token):
        self._result.append("<" + var_type + "> " + token + " </" + var_type + ">" + NEW_LINE)

    def get_next(self):
        if self._tokenizer.got_more_tokens():
            var_type, token = self._tokenizer.get_token()
            return var_type, token
        else:
            return

    def get_current(self):
        return self._tokenizer.get_token()

    def compile_class(self):
        var_type, token = self.get_next()
        self.terminal(var_type, token)
        var_type, token = self.get_next()
        self._current_class = token
        self.terminal(var_type, token)
        var_type, token = self.get_next()
        self.terminal(var_type, token)
        var_type, token = self.get_next()
        while self.is_class_var_dec(token):
            self.compile_class_var_dec()
            var_type, token = self.get_next()
        while self.is_subroutine_dec(token):
            self.reset_label()
            self.compile_subroutine_dec()
            var_type, token = self.get_next()
            if token == '}':
                break
        self.terminal(var_type, token)

    @staticmethod
    def is_class_var_dec(token):
        return token == "field" or token == "static"

    @staticmethod
    def is_subroutine_dec(token):
        return token == "method" or token == "function" or token == "constructor"

    def compile_class_var_dec(self):
        var_type, token = self.get_current()
        var_kind = token
        self.terminal(var_type, token)
        var_type, token = self.get_next()
        var_type = token
        self.terminal(var_type, token)
        var_type, token = self.get_next()
        var_name = token
        self.terminal(var_type, token)
        self._class_table.append(Symbol(var_name, var_type, var_kind, self.counters[var_kind]))
        self.counters[var_kind] += 1
        var_type, token = self.get_next()
        while token == ",":
            self.terminal(var_type, token)
            var_type, token = self.get_next()
            self.terminal(var_type, token)
            var_name = token
            self._class_table.append(Symbol(var_name, var_type, var_kind, self.counters[var_kind]))
            self.counters[var_kind] += 1
            var_type, token = self.get_next()
        self.terminal(var_type, token)

    def compile_subroutine_dec(self):
        var_type, token = self.get_current()
        self._subroutine_table = SymbolTable(self._class_table)
        self._current_function_type = token
        self.terminal(var_type, token)
        var_type, token = self.get_next()
        if self._current_function_type == "method":
            self._subroutine_table.add_symbol(Symbol("this", self._current_class, "argument", 0))
            self._subroutine_table.get_counters()["argument"] += 1
        self.terminal(var_type, token)
        var_type, token = self.get_next()
        self._current_function = token
        self.terminal(var_type, token)
        var_type, token = self.get_next()
        self.terminal(var_type, token)
        self.get_next()
        self.compile_parameter_lst()
        var_type, token = self.get_current()
        self.terminal(var_type, token)
        self.compile_subroutine_body()

    def compile_parameter(self):
        var_type, token = self.get_current()
        argument_type = token
        self.terminal(var_type, token)
        var_type, token = self.get_next()
        argument_name = token
        self._subroutine_table.add_symbol(Symbol(argument_name, argument_type, "argument",
                                                 self._subroutine_table.get_counters()["argument"]))
        self._subroutine_table.get_counters()["argument"] += 1
        self.terminal(var_type, token)

    def compile_parameter_lst(self):
        var_type, token = self.get_current()
        if token == ")":
            return
        self.compile_parameter()
        var_type, token = self.get_next()
        while token == ",":
            self.terminal(var_type, token)
            self.get_next()
            self.compile_parameter()
            var_type, token = self.get_next()

    def compile_subroutine_body(self):
        var_type, token = self.get_next()
        self.terminal(var_type, token)
        var_type, token = self.get_next()
        while token == "var":
            self.compile_var_dec()
            var_type, token = self.get_next()
        self._writer.write_function(self._current_class + '.' + self._current_function,
                                    self._subroutine_table.get_counters()["local"])
        if self._current_function_type == "constructor":
            self._writer.write_push("constant", self.counters["field"])
            self._writer.write_memory()
            self._writer.write_pop("pointer", 0)
        elif self._current_function_type == "method":
            self._writer.write_push("argument", 0)
            self._writer.write_pop("pointer", 0)
        self.compile_statement(var_type, token)
        var_type, token = self.get_current()
        self.terminal(var_type, token)

    def compile_var_dec(self):
        var_type, token = self.get_current()
        self.terminal(var_type, token)
        var_type, token = self.get_next()
        var_type = token
        self.terminal(var_type, token)
        var_type, token = self.get_next()
        var_name = token
        self._subroutine_table.add_symbol(Symbol(var_name, var_type, "local",
                                                 self._subroutine_table.get_counters()["local"]))
        self._subroutine_table.get_counters()["local"] += 1
        self.terminal(var_type, token)
        var_type, token = self.get_next()
        while token == ",":
            self.terminal(var_type, token)
            var_type, token = self.get_next()
            var_name = token
            self._subroutine_table.add_symbol(Symbol(var_name, var_type, "local",
                                                     self._subroutine_table.get_counters()["local"]))
            self._subroutine_table.get_counters()["local"] += 1
            self.terminal(var_type, token)
            var_type, token = self.get_next()
        self.terminal(var_type, token)

    def compile_statement(self, var_type, token):
        while token in ["do", "let", "if", "while", "return"]:
            if token == "do":
                self.compile_do(var_type, token)
            elif token == "let":
                self.compile_let(var_type, token)
            elif token == "if":
                self.compile_if(var_type, token)
                var_type, token = self.get_current()
                continue
            elif token == "while":
                self.compile_while(var_type, token)
            elif token == "return":
                self.compile_return(var_type, token)
            var_type, token = self.get_next()

    def compile_do(self, var_type, token):
        self.terminal(var_type, token)
        self.compileSubroutineCall()
        var_type, token = self.get_next()
        self.terminal(var_type, token)

    def compile_let(self, var_type, token):
        self.terminal(var_type, token)
        var_type, token = self.get_next()
        symbol = self._subroutine_table.get_symbol(token)
        self.terminal(var_type, token)
        var_type, token = self.get_next()
        if token == "[":
            self.terminal(var_type, token)
            self.get_next()
            self.compile_expression()
            self._writer.write_push(symbol.get_kind(), symbol.get_number())
            self._writer.write_arithmetic("add")
            var_type, token = self.get_current()
            self.terminal(var_type, token)
            var_type, token = self.get_next()
            self.terminal(var_type, token)
            self.get_next()
            self.compile_expression()
            self._writer.write_pop("temp", 0)
            self._writer.write_pop("pointer", 1)
            self._writer.write_push("temp", 0)
            self._writer.write_pop("that", 0)
        else:
            self.terminal(var_type, token)
            self.get_next()
            self.compile_expression()
            self._writer.write_pop(symbol.get_kind(), symbol.get_number())
        var_type, token = self.get_current()
        self.terminal(var_type, token)

    def compile_while(self, var_type, token):
        start_while = "WHILE_EXP" + str(self.labels_counters["while"])
        end_while = "WHILE_END" + str(self.labels_counters["while"])
        self.labels_counters["while"] += 1
        self.terminal(var_type, token)
        var_type, token = self.get_next()
        self.terminal(var_type, token)
        self.get_next()
        self._writer.write_label(start_while)
        self.compile_expression()
        self._writer.write_arithmetic("not")
        self._writer.write_if(end_while)
        var_type, token = self.get_current()
        self.terminal(var_type, token)
        var_type, token = self.get_next()
        self.terminal(var_type, token)
        var_type, token = self.get_next()
        self.compile_statement(var_type, token)
        self._writer.write_goto(start_while)
        self._writer.write_label(end_while)
        var_type, token = self.get_current()
        self.terminal(var_type, token)

    def compile_return(self, var_type, token):
        self.terminal(var_type, token)
        var_type, token = self.get_next()
        if self.is_expression(var_type, token):
            self.compile_expression()
            var_type, token = self.get_current()
        else:
            self._writer.write_push("constant", 0)
        self._writer.write_return()
        self.terminal(var_type, token)

    def compile_if(self, var_type, token):
        self.terminal(var_type, token)
        var_type, token = self.get_next()
        self.terminal(var_type, token)
        self.get_next()
        self.compile_expression()
        num = self.labels_counters["if"]
        true_label = "IF_TRUE" + str(num)
        false_label = "IF_FALSE" + str(num)
        self.labels_counters["if"] += 1
        self._writer.write_if(true_label)
        self._writer.write_goto(false_label)
        self._writer.write_label(true_label)
        var_type, token = self.get_current()
        self.terminal(var_type, token)
        var_type, token = self.get_next()
        self.terminal(var_type, token)
        var_type, token = self.get_next()
        self.compile_statement(var_type, token)
        var_type, token = self.get_current()
        self.terminal(var_type, token)
        var_type, token = self.get_next()
        if token == "else":
            else_label = "IF_END" + str(num)
            self._writer.write_goto(else_label)
            self._writer.write_label(false_label)
            self.terminal(var_type, token)
            var_type, token = self.get_next()
            self.terminal(var_type, token)
            var_type, token = self.get_next()
            self.compile_statement(var_type, token)
            self._writer.write_label(else_label)
            var_type, token = self.get_current()
            self.terminal(var_type, token)
            self.get_next()
        else:
            self._writer.write_label(false_label)

    def compile_expression(self):
        self.compile_term()
        var_type, token = self.get_current()
        while token in OPERATORS:
            operation = token
            self.terminal(var_type, token)
            self.get_next()
            self.compile_term()
            self._writer.write_arithmetic(OPERATORS[operation])
            var_type, token = self.get_current()

    @staticmethod
    def is_expression(var_type, token):
        return var_type == "integerConstant" or \
               var_type == "stringConstant" or \
               var_type == "identifier" or \
               token in UNARY_OPERATORS or \
               token in CONSTANTS_KEYWORDS or \
               token == '('

    def compile_term(self):
        var_type, token = self.get_current()
        if var_type == "integerConstant":
            self._writer.write_push("constant", token)
            self.get_next()
            return
        elif var_type == "stringConstant":
            self._writer.write_push("constant", len(token))
            self._writer.write_call("String.new", 1)
            for letter in token:
                self._writer.write_push("constant", ord(letter))
                self._writer.write_call("String.appendChar", 2)
            self.get_next()
            return
        elif token in CONSTANTS_KEYWORDS:
            self.terminal(var_type, token)
            self._writer.write_keywordConstants(token)
            self.get_next()
            return
        elif var_type == "identifier":
            self.terminal(var_type, token)
            name = token
            symbol = self._subroutine_table.get_symbol(name)
            var_type, token = self.get_next()
            if token == "[":
                self.terminal(var_type, token)
                self.get_next()
                self.compile_expression()
                self._writer.write_push(symbol.get_kind(), symbol.get_number())
                self._writer.write_arithmetic("add")
                self._writer.write_pop("pointer", 1)
                self._writer.write_push("that", 0)
                var_type, token = self.get_current()
                self.terminal(var_type, token)
                self.get_next()
                return
            elif token == "(":
                self._writer.write_push("pointer", 0)
                name = self._current_class + '.' + name
                counter = 1
                self.terminal(var_type, token)
                counter += self.compileExpressionList()
                var_type, token = self.get_current()
                self.terminal(var_type, token)
                self._writer.write_call(name, counter)
                self.get_next()
                return
            elif token == ".":
                counter = 0
                self.terminal(var_type, token)
                if symbol:
                    self._writer.write_push(symbol.get_kind(), symbol.get_number())
                    counter = 1
                    name = symbol.get_type()
                name += token
                var_type, token = self.get_next()
                name += token
                self.terminal(var_type, token)
                var_type, token = self.get_next()
                self.terminal(var_type, token)
                counter += self.compileExpressionList()
                var_type, token = self.get_current()
                self.terminal(var_type, token)
                self._writer.write_call(name, counter)
                self.get_next()
                return
            self._writer.write_push(symbol.get_kind(), symbol.get_number())
            return
        elif token in UNARY_OPERATORS:
            self.terminal(var_type, token)
            self.get_next()
            self.compile_term()
            if token == "-":
                self._writer.write_arithmetic("neg")
            else:
                self._writer.write_arithmetic("not")
            return
        elif token == "(":
            self.terminal(var_type, token)
            self.get_next()
            self.compile_expression()
            var_type, token = self.get_current()
            self.terminal(var_type, token)
            self.get_next()
            return

    def compileSubroutineCall(self):
        counter = 0
        var_type, token = self.get_next()
        self.terminal(var_type, token)
        symbol = self._subroutine_table.get_symbol(token)
        name = token
        var_type, token = self.get_next()
        if token == ".":
            self.terminal(var_type, token)
            var_type, token = self.get_next()
            if symbol:
                counter = 1
                self._writer.write_push(symbol.get_kind(), symbol.get_number())
                name = symbol.get_type() + '.' + token
            else:
                name += "." + token
            self.terminal(var_type, token)
            var_type, token = self.get_next()
        else:
            self._writer.write_push("pointer", 0)
            name = self._current_class + "." + name
            counter = 1
        self.terminal(var_type, token)
        counter += self.compileExpressionList()
        self._writer.write_call(name, counter)
        self._writer.write_pop("temp", 0)
        var_type, token = self.get_current()
        self.terminal(var_type, token)

    def compileExpressionList(self):
        counter = 0
        var_type, token = self.get_next()
        if self.is_expression(var_type, token):
            counter += 1
            self.compile_expression()
        var_type, token = self.get_current()
        while token == ",":
            self.terminal(var_type, token)
            self.get_next()
            counter += 1
            self.compile_expression()
            var_type, token = self.get_current()
        return counter
