import pathlib
from setuptools import setup, find_packages
import os
import subprocess

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]


setup(
    name="myriad_downloader",
    version="1.0.0",
    description="Helper to download Le Wagon data challenges with nice repo architecture.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/arthurcol/myriad_downloader",
    author="Arthur Collard",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": ["myriadloader = myriadloader.myriad_downloader:main"]
    },
    zip_safe=False,
    data_files=[("scripts", "scripts/")],
)


# downloading syllabus and executing parser
script_path = os.path.join(
    pathlib.Path(__file__).parent, "scripts/download_syllabus.sh"
)
subprocess.run(
    ["/bin/bash", script_path],
    env={"PARSER_PATH": "myriadloader", **os.environ},
)
