import asyncio
from typing import Annotated, Optional

import typer

from acidrunner.CorrosiveProcessor import CorrosiveProcessor
from acidrunner_cli.utils.config import load_runner

app = typer.Typer()


@app.command()
def run(
    config_file: Optional[
        Annotated[str, typer.Option("-f", help="File to scan for configs")]
    ] = None,
    runs: Annotated[
        int,
        typer.Option(
            "-r",
            help="Number of runs will override the amt of runs in the config file.",
        ),
    ] = 1,
):
    print(42 * "*")
    print(f"Amount of runs: {runs}")
    print(42 * "*")
    runner, settings = load_runner(config_file)
    results = asyncio.run(runner.run(runs))

    processor = CorrosiveProcessor(settings)
    processor.process(results)


if __name__ == "__main__":
    app()
