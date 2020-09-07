class SymbolsTable:
    def __init__(self):
        self.symbol_table = {}

    def add_variable(self, var_name, var_type, var_kind):
        var_id = self.variable_count(var_kind)
        self.symbol_table[var_name] = (Variable(var_name, var_type, var_kind, var_id))

    def variable_count(self, var_kind):
        count = 0
        for variable in self.symbol_table:
            if self.symbol_table[variable].variable_kind == var_kind:
                count += 1
        return count

    def get_type(self, var_name):
        return self.symbol_table[var_name].variable_type

    def get_id(self, var_name):
        return self.symbol_table[var_name].variable_id

    def get_kind(self, var_name):
        return self.symbol_table[var_name].variable_kind

    def clear(self):
        self.symbol_table.clear()

    def is_in_table(self, var_name):
        return var_name in self.symbol_table


class Variable:
    def __init__(self, var_name, var_type, var_kind, var_id):
        self.variable_name = var_name
        self.variable_type = var_type
        self.variable_kind = var_kind
        self.variable_id = var_id
