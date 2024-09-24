from dataclasses import dataclass, field
from typing import List, Optional, Dict
import yaml

@dataclass
class SystemUnderTest:
    name: str
    entrypoint: str

@dataclass
class Bucket:
    name: str
    rpm: int

@dataclass
class FileSetting:
    data_dir: str
    sqlite_enable: bool

@dataclass
class Settings:
    systems_under_test: List[SystemUnderTest] = field(default_factory=list)
    buckets: List[Bucket] = field(default_factory=list)
    file_settings: List[FileSetting] = field(default_factory=list)

    @classmethod
    def from_dict(cls, config_dict: Dict) -> "Settings":
        return cls(
            systems_under_test=cls._parse_systems_under_test(config_dict.get('systems_under_test', [])),
            buckets=cls._parse_buckets(config_dict.get('buckets', [])),
            file_settings=cls._parse_file_settings(config_dict.get('file_settings', []))
        )

    @staticmethod
    def _parse_systems_under_test(systems_list: List[Dict]) -> List[SystemUnderTest]:
        return [
            SystemUnderTest(
                name=system['name'],
                entrypoint=system['entrypoint'],
            ) for system in systems_list if 'name' in system and 'entrypoint' in system
        ]

    @staticmethod
    def _parse_buckets(buckets_list: List[Dict]) -> List[Bucket]:
        return [
            Bucket(
                name=bucket['name'],
                rpm=bucket['rpm']
            ) for bucket in buckets_list if 'name' in bucket and 'rpm' in bucket
        ]

    @staticmethod
    def _parse_file_settings(file_settings_list: List[Dict]) -> List[FileSetting]:
        return [
            FileSetting(
                data_dir=setting['data_dir'],
                sqlite_enable=setting['sqlite_enable']
            ) for setting in file_settings_list if 'data_dir' in setting and 'sqlite_enable' in setting
        ]

    @staticmethod
    def load_settings(config_path: str) -> "Settings":
        with open(config_path, 'r') as file:
            config_dict = yaml.safe_load(file)
        return Settings.from_dict(config_dict)

    def __repr__(self):
        return (f"Settings(systems_under_test={self.systems_under_test}, "
                f"buckets={self.buckets}, file_settings={self.file_settings})")
