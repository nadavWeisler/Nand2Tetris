class Symbol:
    def __init__(self, name, var_type, kind, number):
        self._name = name
        self._type = var_type
        self._kind = kind
        self._number = number

    def get_kind(self):
        if self._kind == 'field':
            return 'this'
        return self._kind

    def get_number(self):
        return self._number

    def get_type(self):
        return self._type

    def get_name(self):
        return self._name
