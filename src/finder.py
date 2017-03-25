import itertools

from src.bool_var import BoolVar
from src.schema import Schema

BOOL_COMBINATIONS = {}


class SchemeFinder:
    def __init__(self, var_count, unipolar, wf, basis):
        self.bool_vars = [BoolVar(i + 1) for i in range(var_count)]
        self.datasets = list(itertools.product(range(2), repeat=var_count))

        self.var_count = var_count
        self.is_polar = unipolar
        self.wf = wf
        self.basis = basis

    def find(self):
        current_schemes = []

        for base_node in self.basis:
            current_schemes.append(Schema(base_node))

        while True:
            for scheme in current_schemes:
                ins_count = scheme.free_wares_count
                varset = BOOL_COMBINATIONS.get(
                    str(ins_count),
                    list(itertools.product(self.bool_vars, repeat=ins_count))  # == var^ins
                )

                for comb in varset:
                    scheme.connect_vars(comb)

                    wf = []
                    for dataset in self.datasets:
                        for data_unit, var in zip(dataset, self.bool_vars):
                            var.value = data_unit

                        wf.append(scheme.calculate())

                    if self.wf == wf:
                        return scheme

            current_schemes = [
                new
                for curr_schema in current_schemes
                for new in curr_schema.get_derivatives(self.basis)
            ]
