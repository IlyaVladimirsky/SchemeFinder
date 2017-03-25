import types


def conjunction(self, *args):
    return all(args[1:])


def disjunction(self, *args):
    return any(args[1:])


def negation(self, *args):
    return not args[1]

operations = {
    'negation': negation,
    'conjunction': conjunction,
    'disjunction': disjunction
}


class Operation:
    def __init__(self, func, in_count):
        self.func = types.MethodType(operations[func], self)
        self.in_count = in_count

neg = Operation('negation', 1)
