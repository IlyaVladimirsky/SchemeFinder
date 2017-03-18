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
