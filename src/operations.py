def conj(*args):
    return 0 in args


def disj(*args):
    return 1 in args

operations = {
    '&': conj,
    '∨': disj
}
