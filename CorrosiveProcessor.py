from setting import Settings
from typing import List
from types_custom import CorrosiveTaskData
import os
from sys import exit

class CorrosiveProcessor:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.yaml_out = {'tests': {}}

    def process_task(self, task: CorrosiveTaskData):
        if 'write_to_yaml' in task.meta_data:
            self.yaml_out['test'].update(task.meta_data['write_to_yaml'])

    def process(self, task_data_list: List[List[CorrosiveTaskData]]):
        [self.process_task(res) for li in task_data_list for res in li if res]
        if len(self.yaml_out['tests']) > 0:
               self.write_to_yaml()

    def write_to_yaml(self):
         if not os.path.exists(self.settings.file_settings.data_dir):
            print("Data dir doesn't exist exiting")
            exit(0x00)
