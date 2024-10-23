import sys

from setuptools import find_packages, setup

extras = {
    "cli": ["typer"],
    "decorators_only": [],  # No extra dependencies for noop decorator
}

# Check if the noop_decorators_only option is being used
# Only include bucketlib
if "decorators_only" in sys.argv:
    packages = find_packages(include=["acidrunner.decorators"])
else:
    packages = find_packages(exclude=["tests*", "__pycache__"])

setup(
    name="acidrunner",
    version="0.1.0",
    description="A benchmarking and testing suite focused on AI development",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="drat3",
    author_email="drat3@protonmail.ch",
    url="https://github.com/dRAT3/AcidRunner",
    packages=packages,
    include_package_data=True,
    install_requires=[
        "pyyaml",
        "numpy",
        "typer",
        "asyncio",
    ],
    extras_require=extras,
    entry_points={
        "console_scripts": [
            "acidrunner=acidrunner_cli.cli:app",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)
