from schemedb import SchemeDB


class SchemeFinder:
    def __init__(self, var_count, is_polar, wf, basis):
        self.db = SchemeDB

        self.var_count = var_count
        self.is_polar = is_polar
        self.wf = wf
        self.basis = basis

    def find(self):
        # fetch schemes of specific length from db
        schemes = self.db.fetch_schemes()
        schemes = [
            '({}&{})&{}',
            '({}&{})∨{}',
            '({}∨{})∨{}',
            '({}∨{})&{}'
        ]
        #  need a function to find all derivative schemes for every parent scheme
        derivative_schemes = []
        for scheme in schemes:
            # 1: find all ins of the scheme
            var_combs = self.get_variable_combinations()
            binary_combs = self.get_all_binary_combinations()

            for base_element in self.basis:
                builded_with_base = self.find_derivatives(base_element)
                derivative_schemes += builded_with_base

                for var_comb in var_combs:  # reduce var combs
                    # calc w(f)
                    for bin_comb in binary_combs:
                        pass

    def find_derivatives(self, parents, build_elem):
        #
        return []

    def get_all_variable_combinations(self):
        return []

    def get_all_binary_combinations(self, length):
        return []
