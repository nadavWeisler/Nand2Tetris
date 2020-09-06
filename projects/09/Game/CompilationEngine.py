from Tokenizer import TokenType
import sys


def print_error():
    """print error msg"""
    print("error msg", file=sys.stderr)


# operator set
op = {
    '+', '-', '*', '/', '&', '|',
    '<', '>', '='
}

# unary operator set
unary_op = {
    '-', '~'
}

# keywords that can be used as statements
statements_keyword = {
    "do", "if", "while", "let", "return"
}


class CompilationEngine:
    """compile file into xml with the same name"""
    def __init__(self, tokenizer, output_file):
        self.tokenizer = tokenizer
        self.output_file = output_file
        self.token_type = ''
        self.current_token = ''
        self.prev_token = ''
        self.generator = self.tokenizer.read_line()

    def compile_class(self):
        """main method, should be called after initalizing class"""
        self.__get_next_token()
        if not (self.token_type == TokenType.KEYWORD and self.current_token
                == "class"):
            print_error()
        self.__write_tag("class", new_line=True)
        self.write_keyword("class")
        self.__get_next_token()
        if self.token_type == TokenType.IDENTIFIER:
            self.write_identifier(self.current_token)
        self.__get_next_token()
        if self.token_type == TokenType.SYMBOL:
            self.write_symbol(self.current_token)
        self.__get_next_token()
        while self.current_token == "static" or self.current_token == "field":
            self.compile_class_var_dec()
        while self.current_token == "constructor" or self.current_token == \
                "function" or self.current_token == "method":
            self.compile_subroutine_dec()
        self.write_symbol(self.current_token)
        self.__write_end_tag("class")

    def __get_next_token(self):
        """get next tokenizer from tokenizer generator"""
        self.current_token = self.generator.__next__()
        self.token_type = self.tokenizer.token_type()

    def compile_class_var_dec(self):
        """compile the class variable declartions"""
        self.__write_tag("classVarDec", new_line=True)
        if self.token_type == TokenType.KEYWORD:
            self.write_keyword(self.current_token)
        self.__compile_variable()
        self.__write_end_tag("classVarDec", new_line=True)

    def __compile_variable(self):
        """compile variable"""
        self.__get_next_token()
        self.compile_type()
        self.__get_next_token()
        self.write_identifier(self.current_token)
        self.__get_next_token()
        while self.current_token == ",":
            self.write_symbol(self.current_token)
            self.__get_next_token()
            self.write_identifier(self.current_token)
            self.__get_next_token()
        self.write_symbol(self.current_token)
        self.__get_next_token()

    def compile_subroutine_dec(self):
        """compile the subroutine declarations"""
        self.__write_tag("subroutineDec", new_line=True)
        self.write_keyword(self.current_token)
        self.__get_next_token()
        if self.current_token == "void":
            self.write_keyword(self.current_token)
        else:
            self.compile_type()
        self.__get_next_token()
        self.write_identifier(self.current_token)
        self.__get_next_token()
        self.write_symbol(self.current_token)
        self.__get_next_token()
        if self.current_token != "(":
            self.compile_parameters_list()
        self.write_symbol(self.current_token)
        self.__get_next_token()
        self.compile_subroutine_body()
        self.__write_end_tag("subroutineDec", new_line=True)

    def compile_parameters_list(self):
        """compile the class variable declarations"""
        self.__write_tag("parameterList", new_line=True)
        if self.current_token != ")":
            self.compile_type()
            self.__get_next_token()
            self.write_identifier(self.current_token)
            self.__get_next_token()
        while self.current_token == ",":
            self.write_symbol(self.current_token)
            self.__get_next_token()
            self.compile_type()
            self.__get_next_token()
            self.write_identifier(self.current_token)
            self.__get_next_token()
        self.__write_end_tag("parameterList", new_line=True)

    def compile_subroutine_body(self):
        """compile the subroutine body"""
        self.__write_tag("subroutineBody", new_line=True)
        self.write_symbol(self.current_token)
        self.__get_next_token()
        while self.current_token == "var":
            self.compile_var_dec()
        if self.token_type == TokenType.KEYWORD:
            self.compile_statements()
        self.write_symbol(self.current_token)
        self.__get_next_token()
        self.__write_end_tag("subroutineBody", new_line=True)

    def compile_subroutine_call(self, prev_chosen = False):
        """compile the subroutine call"""
        if prev_chosen:
            self.write_identifier(self.prev_token)
        else:
            self.write_identifier(self.current_token)
            self.__get_next_token()
        if self.current_token == '.':
            self.write_symbol(self.current_token)
            self.__get_next_token()
            self.write_identifier(self.current_token)
            self.__get_next_token()
        self.write_symbol(self.current_token)
        self.__get_next_token()
        self.compile_expression_list()
        self.write_symbol(self.current_token)
        self.__get_next_token()

    def compile_statements(self):
        """compile statements"""
        self.__write_tag("statements", new_line=True)
        while self.current_token in statements_keyword:
            if self.current_token == "let":
                self.compile_let()
            elif self.current_token == "if":
                self.compile_if()
            elif self.current_token == "while":
                self.compile_while()
            elif self.current_token == "do":
                self.compile_do()
            elif self.current_token == "return":
                self.compile_return()
        self.__write_end_tag("statements", new_line=True)
        # return the next toke from the sub functions

    def compile_var_dec(self):
        self.__write_tag("varDec", new_line=True)
        self.write_keyword(self.current_token)
        self.__compile_variable()
        self.__write_end_tag("varDec", new_line=True)

    def compile_let(self):
        """compile let statement"""
        self.__write_tag("letStatement", new_line=True)
        self.write_keyword(self.current_token)
        self.__get_next_token()
        self.write_identifier(self.current_token)
        self.__get_next_token()
        if self.current_token == "[":
            self.write_symbol(self.current_token)
            self.__get_next_token()
            self.compile_expression()
            self.write_symbol(self.current_token)
            self.__get_next_token()
        self.write_symbol(self.current_token)
        self.__get_next_token()
        self.compile_expression()
        self.write_symbol(self.current_token)
        self.__write_end_tag("letStatement", new_line=True)
        self.__get_next_token()

    def compile_if(self):
        """compile if statement"""
        self.__write_tag("ifStatement", new_line=True)
        self.compile_condition()
        if self.current_token == "else":
            self.write_keyword(self.current_token)
            self.__get_next_token()
            self.write_symbol(self.current_token)
            self.__get_next_token()
            self.compile_statements()
            self.write_symbol(self.current_token)
            self.__get_next_token()
        self.__write_end_tag("ifStatement", new_line=True)

    def compile_condition(self):
        """compile condition"""
        self.write_keyword(self.current_token)
        self.__get_next_token()
        self.write_symbol(self.current_token)
        self.__get_next_token()
        self.compile_expression()
        self.write_symbol(self.current_token)
        self.__get_next_token()
        self.write_symbol(self.current_token)
        self.__get_next_token()
        self.compile_statements()
        self.write_symbol(self.current_token)
        self.__get_next_token()

    def compile_return(self):
        """compile return statement"""
        self.__write_tag("returnStatement", new_line=True)
        self.write_keyword(self.current_token)
        self.__get_next_token()
        if self.current_token != ";":
            self.compile_expression()
        self.write_symbol(self.current_token)
        self.__write_end_tag("returnStatement", new_line=True)
        self.__get_next_token()

    def compile_while(self):
        """compile while statement"""
        self.__write_tag("whileStatement", new_line=True)
        self.compile_condition()
        self.__write_end_tag("whileStatement", new_line=True)

    def compile_do(self):
        """compile do statement"""
        self.__write_tag("doStatement", new_line=True)
        self.write_keyword(self.current_token)
        self.__get_next_token()
        self.compile_subroutine_call()
        self.write_symbol(self.current_token)
        self.__get_next_token()
        self.__write_end_tag("doStatement", new_line=True)

    def compile_expression(self):
        """compile expression"""
        self.__write_tag("expression", new_line=True)
        self.compile_term()
        while self.current_token in op:
            self.write_symbol(self.current_token)
            self.__get_next_token()
            self.compile_term()
        self.__write_end_tag("expression", new_line=True)

    def compile_term(self):
        """compile term"""
        self.__write_tag("term", new_line=True)
        if self.token_type == TokenType.INT_CONST:
            self.write_integer_constant(self.current_token)
            self.__get_next_token()
        elif self.token_type == TokenType.STRING_CONST:
            self.write_string_constant(self.current_token)
            self.__get_next_token()
        elif self.token_type == TokenType.KEYWORD:
            self.write_keyword(self.current_token)
            self.__get_next_token()
        elif self.current_token == "(":
            self.write_symbol(self.current_token)
            self.__get_next_token()
            self.compile_expression()
            self.write_symbol(self.current_token)
            self.__get_next_token()
        elif self.current_token in unary_op:
            self.write_symbol(self.current_token)
            self.__get_next_token()
            self.compile_term()
        else: # from here option that require LL(1)
            self.prev_token = self.current_token
            self.__get_next_token()
            if self.current_token == '(' or self.current_token == '.':
                self.compile_subroutine_call(prev_chosen=True)
            elif self.current_token == '[':
                self.write_identifier(self.prev_token)
                self.write_symbol(self.current_token)
                self.__get_next_token()
                self.compile_expression()
                self.write_symbol(self.current_token)
                self.__get_next_token()
            else:
                self.write_identifier(self.prev_token)
        self.__write_end_tag("term", new_line=True)

    def compile_expression_list(self):
        """compile expression list"""
        self.__write_tag("expressionList", new_line=True)
        while self.current_token != ')':
            self.compile_expression()
            while self.current_token == ',':
                self.write_symbol(self.current_token)
                self.__get_next_token()
                self.compile_expression()
        self.__write_end_tag("expressionList", new_line=True)

    def __write_tag(self, tag, new_line=False):
        """write tag to xml file, mark new_line=True for new line after tag"""
        self.output_file.write("<" + tag + ">")
        if new_line:
            self.output_file.write("\n")

    def __write_end_tag(self, end_tag, new_line=False):
        """write end tag to xml file, mark new_line=True for new line after
        tag"""
        self.output_file.write("</" + end_tag + ">")
        if new_line:
            self.output_file.write("\n")

    def write_keyword(self, keyword):
        """write keyword to xml file"""
        self.__write_tag("keyword")
        self.output_file.write(keyword)
        self.__write_end_tag("keyword", new_line=True)

    def write_identifier(self, identifier):
        """write identifier to xml file"""
        self.__write_tag("identifier")
        self.output_file.write(identifier)
        self.__write_end_tag("identifier", new_line=True)

    def write_symbol(self, symbol):
        """write symbol to xml file"""
        self.__write_tag("symbol")
        if symbol == '<':
            symbol = "&lt;"
        if symbol == '>':
            symbol = "&gt;"
        if symbol == '&':
            symbol = "&amp;"
        self.output_file.write(symbol)
        self.__write_end_tag("symbol", new_line=True)

    def write_integer_constant(self, integer_constant):
        """write int constant to xml file"""
        self.__write_tag("integerConstant")
        self.output_file.write(integer_constant)
        self.__write_end_tag("integerConstant", new_line=True)

    def write_string_constant(self, string_constant):
        """write string constant to xml file"""
        self.__write_tag("stringConstant")
        self.output_file.write(string_constant)
        self.__write_end_tag("stringConstant", new_line=True)

    def compile_type(self):
        """compile type"""
        if self.current_token == "int" or self.current_token == "char" or \
                self.current_token == "boolean":
            self.write_keyword(self.current_token)
        else:
            self.write_identifier(self.current_token)
