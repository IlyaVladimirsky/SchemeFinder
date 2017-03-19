import types


def conjunction(self, *args):
    return all(args)


def disjunction(self, *args):
    return any(args)


def negation(self, *args):
    print(len(args))
    return not args

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
