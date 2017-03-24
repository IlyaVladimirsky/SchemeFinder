class BoolVar:
    def __init__(self, var_id, value=None):
        self.var_id = var_id
        self.value = value

    def __repr__(self):
        return 'x' + str(self.var_id)

def cor():
    d = yield
    print(d)

c = cor()
next(c)
# c.send(1)
# c.send(2)
