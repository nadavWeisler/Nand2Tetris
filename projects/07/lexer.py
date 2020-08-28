import re

NUM = 1
ID = 2
ERROR = 3


def _is_match(re_str, word):
    return re.match(re_str, word) is not None


class Lexer(object):
    _comment = re.compile('//.*$')
    _num_regex = r'\d+'
    _id_regex = r'[\w\-.]+'
    _word = re.compile(_num_regex + '|' + _id_regex)

    def __init__(self, file_name):
        file = open(file_name, 'r')
        self._lines = file.read()
        self._tokens = self._tokenize_lines(self._lines.split('\n'))
        self.current_command = []
        self.current_token = (ERROR, 0)

    def has_more(self):
        return self._tokens != []

    def next(self):
        self.current_command = self._tokens.pop(0)
        self.next_token()
        return self.current_command

    def has_next_token(self):
        return self.current_command != []

    def next_token(self):
        if self.has_next_token():
            self.current_token = self.current_command.pop(0)
        else:
            self.current_token = (ERROR, 0)
        return self.current_token

    def get_token(self):
        if self.has_next_token():
            return self.current_command[0]
        else:
            return ERROR, 0

    def _remove_comment(self, line):
        return self._comment.sub('', line)

    def _is_num(self, word):
        return _is_match(self._num_regex, word)

    def _is_id(self, word):
        return _is_match(self._id_regex, word)

    def _split(self, line):
        return self._word.findall(line)

    def _token(self, word):
        if self._is_num(word):
            return NUM, word
        elif self._is_id(word):
            return ID, word
        else:
            return ERROR, word

    def _tokenize_lines(self, lines):
        return [token for token in [self._tokenize_line(line) for line in lines] if token != []]

    def _tokenize_line(self, line):
        return [self._token(word) for word in self._split(self._remove_comment(line))]
