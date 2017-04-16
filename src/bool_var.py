class BoolVar:
    is_node = False

    def __init__(self, var_id, value=None):
        self.var_id = var_id
        self.value = value

    def __eq__(self, other):
        return self.var_id == other.var_id

    def __copy__(self):
        return self

    def __repr__(self):
        return 'x' + str(self.var_id)
