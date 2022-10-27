import pathlib
from setuptools import setup
import os
import subprocess

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


setup(
    name="myriad_downloader",
    version="1.0.0",
    description="Helper to download Le Wagon data challenges with nice repo architecture.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/arthurcol/myriad_downloader",
    author="Arthur Collard",
    entry_points={
        "console_scripts": ["myriadloader = myriadloader.myriad_downloader:main"]
    },
    zip_safe=False,
)

script_path = os.path.join(
    pathlib.Path(__file__).parent, "scripts/download_syllabus.sh"
)
subprocess.run(
    ["/bin/bash", script_path],
    env={"PARSER_PATH": "myriadloader", **os.environ},
)
