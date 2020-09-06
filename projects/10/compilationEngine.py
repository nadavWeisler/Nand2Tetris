import sys

from jackTokenizer import *

RETURN_STATEMENT = "returnStatement"

CLASS_VAR_DEC = "classVarDec"

ILLEGAL_STATEMENT_ERROR = "illegal statement"

EXPRESSION_LIST = "expressionList"

TERM = "term"

EXPRESSION = "expression"

IF_TAG = "ifStatement"

LET_TAG = "letStatement"

VAR_TAG = "varDec"

SUBROUTINE_BODY = "subroutineBody"

PARAMETER_LIST = "parameterList"

SUBROUTINE_TAG = "subroutineDec"

IS_ENDING = True

DO_STATEMENT_TAG = "doStatement"

STATEMENTS_TAG = "statements"

CLASS_TAG = "class"

COMPILE_CLASS_ERROR = "invalid input in compile class"

COMPILE_TERM_ERROR = "invalid input in compile term"

CLASS_VAR_KEYWORDS = ['static', 'field']

TYPE_KEYWORDS = ['int', 'char', 'boolean']

SUBROUTINE = ['constructor', 'function', 'method']

UNARY_OPS = ['-', '~']

KEYWORD_CONST = ['true', 'false', 'null', 'this']

STATEMENTS = ['let', 'if', 'while', 'do', 'return']

TOKEN_TYPE_STR = {"KEYWORD": "keyword", "SYMBOL": "symbol",
                  "IDENTIFIER": "identifier", "INT_CONST": "integerConstant",
                  "STRING_CONST": "stringConstant"}
OPERATIONS = ['+', '-', '=', '>',
              '<', "*", "/", "&", "|"]


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
        self._check_write_name()
        self._check_write_symbol("{")
        while self._check_if_var_dec():
            self.compile_class_var_dec()
        while self._check_subroutine_dec():
            self.compile_subroutine_dec()
        self._check_write_symbol("}")
        self._write_outer_tag(CLASS_TAG, IS_ENDING)

    def compile_class_var_dec(self):
        self.compile_variable(CLASS_VAR_DEC)

    def compile_subroutine_dec(self):
        self._write_outer_tag(SUBROUTINE_TAG)
        self._write_token(self.tokenizer.token_type())
        if self.tokenizer.key_word() == 'void':
            self._write_token(self.tokenizer.token_type())
        else:
            self._check_write_type()
        self._check_write_name()
        self._check_write_symbol("(")
        self.compile_parameter_list()
        self._check_write_symbol(")")
        self.compile_subroutine_body()
        self._write_outer_tag(SUBROUTINE_TAG, IS_ENDING)

    def compile_parameter_list(self):
        self._write_outer_tag(PARAMETER_LIST)
        if self.tokenizer.symbol() != ')':
            self._check_write_type()
            self._check_write_name()
            while self._check_if_comma():
                self._check_write_symbol(",")
                self._check_write_type()
                self._check_write_name()
        self._write_outer_tag(PARAMETER_LIST, IS_ENDING)

    def compile_subroutine_body(self):
        self._write_outer_tag(SUBROUTINE_BODY)
        self._check_write_symbol("{")
        while self.tokenizer.key_word() == 'var':
            self.compile_var_dec()
        self.compile_statements()
        self._check_write_symbol("}")
        self._write_outer_tag(SUBROUTINE_BODY, IS_ENDING)

    def compile_var_dec(self):
        self.compile_variable(VAR_TAG)

    def compile_variable(self, tag):
        self._write_outer_tag(tag)
        self._write_token(self.tokenizer.token_type())
        self._check_write_type()
        self._check_write_name()
        while self._check_if_comma():
            self._check_write_symbol(",")
            self._check_write_name()
        self._check_write_symbol(";")
        self._write_outer_tag(VAR_TAG, IS_ENDING)

    def compile_statements(self):
        self._write_outer_tag(STATEMENTS_TAG)
        while self._check_if_statement():
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
        self._check_write_symbol(";")
        self._write_outer_tag(DO_STATEMENT_TAG, IS_ENDING)

    def compile_let(self):
        self._write_outer_tag(LET_TAG)
        self._write_token(self.tokenizer.token_type())
        self._check_write_name()
        if self.tokenizer.symbol() == '[':  # if there is an array
            self._check_write_symbol("[")
            self.compile_expression()
            self._check_write_symbol("]")
        self._check_write_symbol("=")
        self.compile_expression()
        self._check_write_symbol(";")
        self._write_outer_tag(LET_TAG, IS_ENDING)

    def compile_if(self):
        self._write_outer_tag(IF_TAG)
        self._write_token(self.tokenizer.token_type())
        self._check_write_symbol("(")
        self.compile_expression()
        self._check_write_symbol(")")
        self._check_write_symbol("{")
        self.compile_statements()
        self._check_write_symbol("}")
        if self.tokenizer.key_word() == 'else':
            self._write_token(self.tokenizer.token_type())
            self._check_write_symbol("{")
            self.compile_statements()
            self._check_write_symbol("}")
        self._write_outer_tag(IF_TAG, IS_ENDING)

    def compile_while(self):
        self._write_outer_tag("whileStatement")
        self._write_token(self.tokenizer.token_type())
        self._check_write_symbol("(")
        self.compile_expression()
        self._check_write_symbol(")")
        self._check_write_symbol("{")
        self.compile_statements()
        self._check_write_symbol("}")
        self._write_outer_tag("whileStatement", IS_ENDING)

    def compile_return(self):
        self._write_outer_tag(RETURN_STATEMENT)
        self._write_token(self.tokenizer.token_type())
        if not self.tokenizer.symbol() == ';':
            self.compile_expression()
        self._check_write_symbol(";")
        self._write_outer_tag(RETURN_STATEMENT, IS_ENDING)

    def compile_subroutine_call(self):
        self._check_write_name()
        if self.tokenizer.symbol() == ".":
            self._check_write_symbol(".")
            self._check_write_name()
        self._check_write_symbol("(")
        self.compile_expression_list()
        self._check_write_symbol(")")

    def compile_expression(self):
        self._write_outer_tag(EXPRESSION)
        self.compile_term()
        while self.tokenizer.symbol() in OPERATIONS:
            self._write_op()
            self.compile_term()
        self._write_outer_tag(EXPRESSION, IS_ENDING)

    def compile_term(self):
        self._write_outer_tag(TERM)
        cur_type = self.tokenizer.token_type()
        if self.tokenizer.token_type() in ["INT_CONST", "STRING_CONST"]:
            self._write_token(cur_type)
        elif self.tokenizer.key_word() in KEYWORD_CONST:
            self._write_token(cur_type)
        elif self.tokenizer.symbol() == '(':
            self._write_token(cur_type)
            self.compile_expression()
            self._check_write_symbol(")")
        elif self.tokenizer.symbol() in UNARY_OPS:
            self._write_op()
            self.compile_term()
        elif self.tokenizer.identifier():
            self._compile_term_identifier()
        else:
            print(COMPILE_TERM_ERROR)
            sys.exit()
        self._write_outer_tag(TERM, IS_ENDING)

    def _compile_term_identifier(self):
        if self.tokenizer.get_next_token() == '[':
            self._check_write_name()
            self._check_write_symbol("[")
            self.compile_expression()
            self._check_write_symbol("]")
        elif self.tokenizer.get_next_token() in [".", "("]:
            self.compile_subroutine_call()
        else:
            self._check_write_name()

    def compile_expression_list(self):
        self._write_outer_tag(EXPRESSION_LIST)
        if self.tokenizer.symbol() != ')':
            self.compile_expression()
            while self._check_if_comma():
                self._write_token(self.tokenizer.token_type())
                self.compile_expression()
        self._write_outer_tag(EXPRESSION_LIST, IS_ENDING)

    def _check_if_var_dec(self):
        return self.tokenizer.key_word() in CLASS_VAR_KEYWORDS

    def _check_subroutine_dec(self):
        return self.tokenizer.key_word() in SUBROUTINE

    def _check_if_comma(self):
        return self.tokenizer.symbol() == ','

    def _check_if_statement(self):
        return self.tokenizer.key_word() in STATEMENTS

    def _check_write_type(self):
        if self.tokenizer.key_word() in TYPE_KEYWORDS:
            self._write_token(self.tokenizer.token_type())
        else:
            self._check_write_name()

    def _check_write_symbol(self, expected_symbol):
        if self.tokenizer.symbol() != expected_symbol:
            print(ILLEGAL_STATEMENT_ERROR)
            sys.exit()
        self._write_token(self.tokenizer.token_type())

    def _check_write_name(self):
        if self.tokenizer.identifier():
            self._write_token("IDENTIFIER")
        else:
            print(ILLEGAL_STATEMENT_ERROR)
            sys.exit()

    def _write_outer_tag(self, tag_str, end=False):
        if end:
            self._indent_count -= 1
            self.out_file.write("\t" * self._indent_count)
            self.out_file.write("</" + tag_str + ">\n")
        else:
            self.out_file.write("\t" * self._indent_count)
            self.out_file.write("<" + tag_str + ">\n")
            self._indent_count += 1

    def _write_op(self):
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
        self.out_file.write(" </symbol>\n")
        self.tokenizer.advance()

    def _write_token(self, cur_type):
        self.out_file.write("\t" * self._indent_count)
        self.out_file.write("<" + TOKEN_TYPE_STR[cur_type] + "> ")
        self.out_file.write(str(self.tokenizer.get_token_string()))
        self.out_file.write(" </" + TOKEN_TYPE_STR[cur_type] + ">\n")
        self.tokenizer.advance()
