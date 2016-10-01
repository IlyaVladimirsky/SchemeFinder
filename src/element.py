class Element:
    def __init__(self, element_type, in_count):
        self.type = element_type
        self.in_count = in_count
        self.inputs = []

    def output_signal(self, input_signals):
        pass
