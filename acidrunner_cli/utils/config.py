from acidrunner.settings import Settings
from acidrunner.CorrosiveRunner import CorrosiveRunner

def load_runner(config_file: str | None):
    if config_file:
        try:
            settings = Settings.load_settings(config_file)
            runner = CorrosiveRunner(settings)

            return runner, settings
        except Exception as e:
            print(f"Couldn't open {config_file}")
            raise Exception(f"Couldn't open {config_file}\n\r{e}")
    else:
        try:
            settings = Settings.load_settings("Acidfile.yaml")
            runner = CorrosiveRunner(settings)

            return runner, 
        except Exception as e:
            print("Couldn't open Acidfile.yaml try and specify one with --config-filef")
            raise Exception(f"Couldn't open {config_file}\n\r{e}")


