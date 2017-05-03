import itertools
import json
import os
from copy import copy
from datetime import datetime
from time import sleep
from tkinter import Label

from src.bool_var import BoolVar
from src.schema import Schema

BOOL_COMBINATIONS = {}


class SchemeFinder:
    def __init__(self, var_count, unipolar, wf, basis, output=None):
        self.bool_vars = [BoolVar(i + 1) for i in range(var_count)]
        self.datasets = list(itertools.product(range(2), repeat=var_count))

        self.var_count = var_count
        self.is_polar = unipolar
        self.wf = wf
        self.basis = basis
        self.output = output or Label()

        self.running = True
        self.stop = False

        self.state_folder = 'states/'
        self.result_filename = None
        self.state_filename = None
        self.all_minimal_file = None

    def save_state(self):
        with open(self.state_filename, 'w') as sf:
            sf.write(json.dumps({'checked_schemas': self.checked_number}))

    def load_state(self):
        with open(self.state_filename, 'r') as sf:
            state = json.loads(sf.readline())

            return int(state['checked_schemas'])

    def load_wfs(self):
        with open(self.result_filename, 'r') as rf:
            dicts = [json.loads(line) for line in rf]

            return {key: value for d in dicts for key, value in d.items()} if dicts else {}

    def find(self):
        self.result_filename = self.state_folder + self._get_filename_from_basis() + '_sch.json'
        self.state_filename = self.state_folder + self._get_filename_from_basis() + '_state.json'
        saved_state_exists = os.path.exists(self.state_filename)

        self.all_minimal_file = open(self.result_filename, 'a')

        if not saved_state_exists:
            self.checked_number = 0

            self.save_state()
        else:
            self.checked_number = self.load_state()

        wfs = self.load_wfs()

        current_schemas = []
        for base_node in self.basis:
            current_schemas.append(Schema(base_node))

        checked_number = 0
        checked_number_loaded = self.checked_number
        level = 1
        previous_wfs_count = len(wfs)
        while True:
            print('current schemas length = %d' % len(current_schemas))

            for i, scheme in enumerate(current_schemas):
                while not self.running:
                    sleep(0.5)

                if checked_number >= checked_number_loaded:
                    ins_count = scheme.free_wares_count
                    varset = BOOL_COMBINATIONS.get(
                        str(ins_count),
                        list(itertools.product(self.bool_vars, repeat=ins_count))  # == var^ins
                    )

                    schema_wfs = []
                    for comb in varset:
                        scheme.connect_vars(comb)

                        wf = []
                        for dataset in self.datasets:
                            for data_unit, var in zip(dataset, self.bool_vars):
                                var.value = data_unit

                            wf.append(str(int(scheme.calculate())))

                        wf = ''.join(wf)
                        if wf not in wfs:
                            cp_schema = copy(scheme)
                            wfs[wf] = cp_schema
                            schema_wfs.append(json.dumps({wf: str(cp_schema), 'length': level}) + '\n')

                            # if self.wf == wf:
                            #     self.output['text'] = str(scheme)
                            #     return
                                # print(scheme)

                    if len(wfs) != previous_wfs_count:
                        self.all_minimal_file.writelines(schema_wfs)
                        # print(wfs[wf], wfs)
                        print('checked schemas = %d, level = %d, time = %s, wfs = %d' % (checked_number, level, datetime.now(), len(wfs)))
                        self.output['text'] = 'checked schemas = %d, level = %d, time = %s, wfs = %d' % (checked_number, level, datetime.now(), len(wfs))

                    previous_wfs_count = len(wfs)

                checked_number += 1
                if checked_number % 200 == 0:
                    self.checked_number = checked_number
                    # print(current_schemas[i-2000:i])
                    print('checked schemas = %d, level = %d, time = %s, wfs = %d' % (checked_number, level, datetime.now(), len(wfs)))
                    self.output['text'] = 'checked schemas = %d, level = %d, time = %s, wfs = %d' % (checked_number, level, datetime.now(), len(wfs))

            current_schemas = [new for curr_schema in current_schemas for new in curr_schema.get_derivatives(self.basis)]
            level += 1

    def _get_filename_from_basis(self):
        return ''.join(sorted(e.function.__name__[0] + str(len(e.children)) for e in self.basis)) + '_%d' % len(self.bool_vars)
