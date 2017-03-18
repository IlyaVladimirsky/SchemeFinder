from collections import namedtuple


def conjunction(*args):
    return all(args)


def disjunction(*args):
    return any(args)


def negation(*args):
    return not args

operations = {
    'negation': negation,
    'conjunction': conjunction,
    'disjunction': disjunction
}


class Operation:
    def __init__(self, func, in_count):
        self.func = operations[func]
        self.in_count = in_count

negation = Operation('negation', 1)
