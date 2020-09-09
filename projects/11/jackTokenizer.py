import re
from utils import *


class JackTokenizer:

    def __init__(self, file_name):
        self._file = open(file_name, 'r')
        self._data = []
        self._types = []
        self._tokens = []
        self._xml = ['<tokens>']
        self._tokens_iterator = iter(self._tokens)
        self._token_types_iterator = iter(self._types)
        self._current_token = ""
        self._current_token_type = ""

    def got_more_tokens(self):
        try:
            self._current_token = next(self._tokens_iterator)
            self._current_token_type = next(self._token_types_iterator)
            return True
        except:
            return False

    def get_token(self):
        return self._current_token_type, self._current_token

    @staticmethod
    def is_keyword(token):
        return token in KEYWORDS

    @staticmethod
    def is_symbol(token):
        return token in SYMBOLS

    def is_identifier(self, token):
        return len(token) >= 1 and not token[0].isdigit() and \
               re.match(r'^[A-Za-z0-9_]+', token) is not None and \
               not self.is_keyword(token)

    @staticmethod
    def is_int(token):
        return token.isdigit() and 0 <= int(token) <= MAX_INT

    @staticmethod
    def is_string(token):
        return len(token) >= 2 and \
               (token[0] == '\"' and
                token[-1] == '\"' and
                '\"' not in token[1:-1] and
                NEW_LINE not in token[1:-1])

    def get_token_type(self, token):
        if self.is_keyword(token):
            return 'keyword'
        elif self.is_symbol(token):
            return 'symbol'
        elif self.is_identifier(token):
            return 'identifier'
        elif self.is_int(token):
            return 'integerConstant'
        elif self.is_string(token):
            return 'stringConstant'

    def filter(self):
        start = False
        for line in self._file:
            segment1 = ""
            segment2 = ""
            temp = line.strip()
            matcher1 = re.match('.*\"[^\"]*//[^\"]*\".*', temp)
            matcher2 = re.match('.*\"[^\"]*/\*{1,2}[^\"]*\".*', temp)
            matcher3 = re.match('.*\"[^\"]*\*/[^\"]*\".*', temp)
            if matcher1 is not None or matcher2 is not None or matcher3 is not None:
                self._data.append(temp[:])
                continue

            arr = temp.split('/*')
            if len(arr) > 1:
                start = True
                segment1 = arr[0]
            if start:
                arr = temp.split('*/')
                if len(arr) > 1:
                    segment2 = arr[1]
                    start = False
                result = segment1[:] + segment2[:]
                if len(result):
                    self._data.append(segment1[:] + segment2[:])
            else:
                temp = ' '.join(temp.split('//')[0].split())
                if len(temp):
                    self._data.append(temp[:])

    @staticmethod
    def convert_lt_gt_quot_amp(char):
        if char == '<':
            return '&lt;'
        elif char == '>':
            return '&gt;'
        elif char == '\"':
            return '&quot;'
        elif char == '&':
            return '&amp;'

    @staticmethod
    def split_line_by_symbols(line):
        result = list()
        idx = 0
        temp = ""
        while idx < len(line):
            if line[idx] == ' ':
                result.append(temp)
                temp = ""
            elif line[idx] in SYMBOLS and line[idx] != '\"':
                if len(temp):
                    result.append(temp)
                    result.append(line[idx])
                    temp = ""
                else:
                    result.append(line[idx])
            elif line[idx] == '\"':
                next_idx = line.find('\"', idx + 1)
                while line[next_idx - 1] == '\\':
                    next_idx = line.find('\"', next_idx)
                segment = line[idx:next_idx + 1]
                result.append(segment)
                temp = ""
                idx = next_idx + 1
                continue
            else:
                temp += line[idx]
            idx += 1

        return result

    def tokenize(self):
        self.filter()
        for line in self._data:
            segments = self.split_line_by_symbols(line)
            for segment in segments:
                current_type = self.get_token_type(segment)
                if current_type is not None:
                    self._types.append(current_type)
                    self._tokens.append(segment)
                    if current_type not in {'stringConstant', 'integerConstant'}:
                        current_type = current_type.lower()
                    else:
                        if current_type == 'stringConstant':
                            current_type = 'stringConstant'
                            self._tokens[-1] = self._tokens[-1].strip('\"')
                            segment = segment.strip('\"')
                        else:
                            current_type = 'integerConstant'
                    if segment in {'<', '>', '\"', '&'}:
                        self._tokens[-1] = self.convert_lt_gt_quot_amp(segment)
                        segment = self.convert_lt_gt_quot_amp(segment)
                    self._xml.append('<' + current_type + '> ' + segment + ' </' + current_type + '>')
                elif len(segment.strip()):
                    print(segment)
                    raise Exception("Invalid Token")
        self._xml.append('</tokens>')
