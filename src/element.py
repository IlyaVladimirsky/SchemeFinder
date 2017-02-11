class LogicalElement:
    def __init__(self, element_type, in_count):
        self.type = element_type
        self.in_count = in_count
        self.inputs = []

    def output_signal(self, input_signals):
        pass

    def get_inputs_count(self):
        return self.in_count
