import itertools
from copy import copy
from datetime import datetime

from src.bool_var import BoolVar
from src.schema import Schema




class SchemeFinder:
    def __init__(self, var_count, unipolar, wf, basis):
        self.bool_vars = [BoolVar(i + 1) for i in range(var_count)]
        self.datasets = list(itertools.product(range(2), repeat=var_count))

        self.var_count = var_count
        self.is_polar = unipolar
        self.wf = wf
        self.basis = basis

    def find(self):
        current_schemas = []

        for base_node in self.basis:
            for var_comb in itertools.combinations(self.bool_vars, len(base_node.children)):
                c = copy(base_node)
                c.children = list(var_comb)
                current_schemas.append(Schema(c))

        checked_count = 0
        level = 1
        while True:
            print('current schemas length = %d' % len(current_schemas))

            new_schemas = []

            for schema in current_schemas:
                for sub_schema in schema.get_derivatives(self.basis, self.bool_vars):
                    if self.wf == sub_schema.calculate():
                        return sub_schema

                    new_schemas.append(sub_schema)

                checked_count += 1
                if checked_count % 2000 == 0:
                    print('checked schemas = %d, level = %d, time = %s' % (checked_count, level, datetime.now()))

            current_schemas = new_schemas

            level += 1
