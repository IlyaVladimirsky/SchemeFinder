import types


def conjunction(self, *args):
    return all(args)


def disjunction(self, *args):
    return any(args)


def negation(self, *args):
    return not args[0]


def mod(self, *args):
    return sum(args) % 2

operations = {
    'negation': negation,
    'conjunction': conjunction,
    'disjunction': disjunction,
    'mod': mod
}


class Operation:
    def __init__(self, func, in_count):
        self.func = types.MethodType(operations[func], self)
        self.in_count = in_count

neg = Operation('negation', 1)
