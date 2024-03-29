import sys
from jackTokenizer import *
from utils import *


class CompilationEngine:
    def __init__(self, in_file, out_file):
        self.tokenizer = JackTokenizer(in_file)
        self.out_file = open(out_file, 'w')
        self._indent_count = 0

    def compile_class(self):
        self._write_outer_tag(CLASS_TAG)
        self.tokenizer.advance()
        if self.tokenizer.key_word() != CLASS_TAG:
            print(COMPILE_CLASS_ERROR)
            sys.exit()
        self._write_token(self.tokenizer.token_type())
        self._is_write_name()
        self._is_write_symbol("{")
        while self._is_var_dec():
            self.compile_class_var_dec()
        while self._is_subroutine_dec():
            self.compile_subroutine_dec()
        self._is_write_symbol("}")
        self._write_outer_tag(CLASS_TAG, IS_ENDING)

    def compile_class_var_dec(self):
        self.compile_variable(CLASS_VAR_DEC)

    def compile_subroutine_dec(self):
        self._write_outer_tag(SUBROUTINE_TAG)
        self._write_token(self.tokenizer.token_type())
        if self.tokenizer.key_word() == 'void':
            self._write_token(self.tokenizer.token_type())
        else:
            self._is_write_type()
        self._is_write_name()
        self._is_write_symbol("(")
        self.compile_parameter_list()
        self._is_write_symbol(")")
        self.compile_subroutine_body()
        self._write_outer_tag(SUBROUTINE_TAG, IS_ENDING)

    def compile_parameter_list(self):
        self._write_outer_tag(PARAMETER_LIST)
        if self.tokenizer.symbol() != ')':
            self._is_write_type()
            self._is_write_name()
            while self._is_comma():
                self._is_write_symbol(",")
                self._is_write_type()
                self._is_write_name()
        self._write_outer_tag(PARAMETER_LIST, IS_ENDING)

    def compile_subroutine_body(self):
        self._write_outer_tag(SUBROUTINE_BODY)
        self._is_write_symbol("{")
        while self.tokenizer.key_word() == 'var':
            self.compile_var_dec()
        self.compile_statements()
        self._is_write_symbol("}")
        self._write_outer_tag(SUBROUTINE_BODY, IS_ENDING)

    def compile_var_dec(self):
        self.compile_variable(VAR_TAG)

    def compile_variable(self, tag):
        self._write_outer_tag(tag)
        self._write_token(self.tokenizer.token_type())
        self._is_write_type()
        self._is_write_name()
        while self._is_comma():
            self._is_write_symbol(",")
            self._is_write_name()
        self._is_write_symbol(";")
        self._write_outer_tag(VAR_TAG, IS_ENDING)

    def compile_statements(self):
        self._write_outer_tag(STATEMENTS_TAG)
        while self._is_statement():
            if self.tokenizer.key_word() == 'let':
                self.compile_let()
            elif self.tokenizer.key_word() == 'if':
                self.compile_if()
            elif self.tokenizer.key_word() == 'while':
                self.compile_while()
            elif self.tokenizer.key_word() == 'do':
                self.compile_do()
            elif self.tokenizer.key_word() == 'return':
                self.compile_return()
        self._write_outer_tag(STATEMENTS_TAG, IS_ENDING)

    def compile_do(self):
        self._write_outer_tag(DO_STATEMENT_TAG)
        self._write_token(self.tokenizer.token_type())
        self.compile_subroutine_call()
        self._is_write_symbol(";")
        self._write_outer_tag(DO_STATEMENT_TAG, IS_ENDING)

    def compile_let(self):
        self._write_outer_tag(LET_TAG)
        self._write_token(self.tokenizer.token_type())
        self._is_write_name()
        if self.tokenizer.symbol() == '[':
            self._is_write_symbol("[")
            self.compile_expression()
            self._is_write_symbol("]")
        self._is_write_symbol("=")
        self.compile_expression()
        self._is_write_symbol(";")
        self._write_outer_tag(LET_TAG, IS_ENDING)

    def compile_if(self):
        self._write_outer_tag(IF_TAG)
        self._write_token(self.tokenizer.token_type())
        self._is_write_symbol("(")
        self.compile_expression()
        self._is_write_symbol(")")
        self._is_write_symbol("{")
        self.compile_statements()
        self._is_write_symbol("}")
        if self.tokenizer.key_word() == 'else':
            self._write_token(self.tokenizer.token_type())
            self._is_write_symbol("{")
            self.compile_statements()
            self._is_write_symbol("}")
        self._write_outer_tag(IF_TAG, IS_ENDING)

    def compile_while(self):
        self._write_outer_tag("whileStatement")
        self._write_token(self.tokenizer.token_type())
        self._is_write_symbol("(")
        self.compile_expression()
        self._is_write_symbol(")")
        self._is_write_symbol("{")
        self.compile_statements()
        self._is_write_symbol("}")
        self._write_outer_tag("whileStatement", IS_ENDING)

    def compile_return(self):
        self._write_outer_tag(RETURN_STATEMENT)
        self._write_token(self.tokenizer.token_type())
        if not self.tokenizer.symbol() == ';':
            self.compile_expression()
        self._is_write_symbol(";")
        self._write_outer_tag(RETURN_STATEMENT, IS_ENDING)

    def compile_subroutine_call(self):
        self._is_write_name()
        if self.tokenizer.symbol() == ".":
            self._is_write_symbol(".")
            self._is_write_name()
        self._is_write_symbol("(")
        self.compile_expression_list()
        self._is_write_symbol(")")

    def compile_expression(self):
        self._write_outer_tag(EXPRESSION)
        self.compile_term()
        while self.tokenizer.symbol() in OPERATORS:
            self._write_operation()
            self.compile_term()
        self._write_outer_tag(EXPRESSION, IS_ENDING)

    def compile_term(self):
        self._write_outer_tag(TERM)
        current_type = self.tokenizer.token_type()
        if self.tokenizer.token_type() in ["INT_CONST", "STRING_CONST"]:
            self._write_token(current_type)
        elif self.tokenizer.key_word() in CONST_KEYWORD:
            self._write_token(current_type)
        elif self.tokenizer.symbol() == '(':
            self._write_token(current_type)
            self.compile_expression()
            self._is_write_symbol(")")
        elif self.tokenizer.symbol() in UNARY:
            self._write_operation()
            self.compile_term()
        elif self.tokenizer.identifier():
            self._compile_term_identifier()
        else:
            print(COMPILE_TERM_ERROR)
            sys.exit()
        self._write_outer_tag(TERM, IS_ENDING)

    def _compile_term_identifier(self):
        if self.tokenizer.get_next_token() == '[':
            self._is_write_name()
            self._is_write_symbol("[")
            self.compile_expression()
            self._is_write_symbol("]")
        elif self.tokenizer.get_next_token() in [".", "("]:
            self.compile_subroutine_call()
        else:
            self._is_write_name()

    def compile_expression_list(self):
        self._write_outer_tag(EXPRESSION_LIST)
        if self.tokenizer.symbol() != ')':
            self.compile_expression()
            while self._is_comma():
                self._write_token(self.tokenizer.token_type())
                self.compile_expression()
        self._write_outer_tag(EXPRESSION_LIST, IS_ENDING)

    def _is_var_dec(self):
        return self.tokenizer.key_word() in CLASS_VAR_KEYWORDS

    def _is_subroutine_dec(self):
        return self.tokenizer.key_word() in SUB_ROUTINE

    def _is_comma(self):
        return self.tokenizer.symbol() == ','

    def _is_statement(self):
        return self.tokenizer.key_word() in STATEMENTS

    def _is_write_type(self):
        if self.tokenizer.key_word() in KEYWORDS_TYPES:
            self._write_token(self.tokenizer.token_type())
        else:
            self._is_write_name()

    def _is_write_symbol(self, expected_symbol):
        if self.tokenizer.symbol() != expected_symbol:
            print(ILLEGAL_STATEMENT_ERROR)
            sys.exit()
        self._write_token(self.tokenizer.token_type())

    def _is_write_name(self):
        if self.tokenizer.identifier():
            self._write_token("IDENTIFIER")
        else:
            print(ILLEGAL_STATEMENT_ERROR)
            sys.exit()

    def _write_outer_tag(self, tag_str, end=False):
        if end:
            self._indent_count -= 1
            self.out_file.write("\t" * self._indent_count)
            self.out_file.write("</" + tag_str + ">" + NEW_LINE)
        else:
            self.out_file.write("\t" * self._indent_count)
            self.out_file.write("<" + tag_str + ">" + NEW_LINE)
            self._indent_count += 1

    def _write_operation(self):
        self.out_file.write("\t" * self._indent_count)
        self.out_file.write("<symbol> ")
        if self.tokenizer.symbol() == '<':
            self.out_file.write("&lt;")
        elif self.tokenizer.symbol() == '>':
            self.out_file.write("&gt;")
        elif self.tokenizer.symbol() == '&':
            self.out_file.write("&amp;")
        elif self.tokenizer.symbol() == '\"':
            self.out_file.write("&quot;")
        else:
            self.out_file.write(self.tokenizer.symbol())
        self.out_file.write(" </symbol>" + NEW_LINE)
        self.tokenizer.advance()

    def _write_token(self, cur_type):
        self.out_file.write("\t" * self._indent_count)
        self.out_file.write("<" + TOKEN_TYPE_STRINGS[cur_type] + "> ")
        self.out_file.write(str(self.tokenizer.get_token_string()))
        self.out_file.write(" </" + TOKEN_TYPE_STRINGS[cur_type] + ">" + NEW_LINE)
        self.tokenizer.advance()
