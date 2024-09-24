from setting import Settings
from typing import List, Dict
from types_custom import CorrosiveTaskData
import os
from sys import exit
from uuid import uuid4
import yaml

class CorrosiveProcessor:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.yaml_out = {'tests': []}

    def process_task(self, task: CorrosiveTaskData):
        if 'write_to_yaml' in task.meta_data:
            self.yaml_out['tests'].append(task.meta_data['write_to_yaml'])

    def process(self, task_data_list: List[List[CorrosiveTaskData]]):
        self.clear_data()

        succes_rate_total = 0.0
        succes_rate_run = []
        avg_runtime = 0
        total_runtime = 0
        failed_test = []
        succeeded_tests = []

        [self.process_task(res) for li in task_data_list for res in li if res]

        if len(self.yaml_out['tests']) > 0:
               self.write_to_yaml()

    def clear_data(self):
        self.yaml_out['tests'] = []

    def write_to_yaml(self):
        directory = str(self.settings.file_settings.data_dir) + "/yaml_out/" 
        path = directory + str(uuid4()) + ".yaml"
        print("Writing to yaml file {drctry}")

        os.makedirs(directory, exist_ok=True) 
        with open(path, 'w') as file:
            yaml.dump(self.yaml_out, file, default_flow_style=False)

        print(f"write_to_yaml written to file {path}")
