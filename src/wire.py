class Wire:
    def __init__(self, value=None, label=-1):
        self.value = value
        self.label = label

    def __eq__(self, other):
        return self.value is other.value
