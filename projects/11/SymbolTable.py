class SymbolTable:
    def __init__(self, class_table=None):
        self._class_table = class_table
        self._symbols = []
        self._counters = {
            'static': 0,
            'field': 0,
            'argument': 0,
            'local': 0
        }

    def get_counters(self):
        return self._counters

    def get_symbol(self, name):
        for symbol in self._symbols:
            if symbol.get_name() == name:
                return symbol
        if self._class_table:
            for symbol in self._class_table:
                if name == symbol.get_name():
                    return symbol

    def add_symbol(self, symbol):
        self._symbols.append(symbol)
