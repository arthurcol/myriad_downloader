from typing import Dict, List
import yaml
import os
import sys
import argparse
import subprocess
import pathlib


def syllabus_loader() -> Dict:
    """
    Load the parsed version of the syllabus.yml file ; created with yaml_parser.py
    """
    HERE = pathlib.Path(__file__).parent
    SYLLABUS_PATH = os.path.join(HERE, "short_syllabus.yml")

    try:
        with open(SYLLABUS_PATH, "r") as file:
            syllabus = yaml.load(file, Loader=yaml.Loader)
    except FileNotFoundError:
        print("Run yaml_parser.py first")
        # return sys.exit()
    return syllabus


def setup_checker() -> subprocess.CompletedProcess:
    """
    Check setup is done and needed exec and environment variables are installed
    """
    script_path = os.path.join(
        os.path.dirname(pathlib.Path(__file__).parent), "scripts/setup_checker.sh"
    )
    return subprocess.run(["/bin/bash", script_path])


def kitt_challenge_downloader(
    path: str,
    batch: str = None,
) -> subprocess.CompletedProcess:

    script_path = os.path.join(
        os.path.dirname(pathlib.Path(__file__).parent),
        "scripts/challenge_downloader.sh",
    )
    env = {"CHA_PATH": path, **os.environ}
    if batch:
        env["DEFAULT_BATCH"] = batch
    subprocess.run(["/bin/bash", script_path], env=env)


def paths_finder(path_code: str, syllabus: Dict) -> List:
    if "-" in path_code:
        module = path_code.split("-")[0]
        day = path_code.split("-")[1]
        paths = syllabus[module]["days"][day]["exercises"]
    else:
        paths = []
        print("Downloading full module")
        for day in syllabus[path_code]["days"].values():
            paths += day["exercises"]

    return paths


def set_varenv() -> subprocess.CompletedProcess:
    """
    Set environment variables KITT_TOKEN, GH_USERNAME and DEFAULT_BATCH.
    """
    script_path = os.path.join(
        os.path.dirname(pathlib.Path(__file__).parent), "scripts/set_varenv.sh"
    )
    subprocess.run(["/bin/bash", script_path])
    subprocess.run("/bin/zsh")


def create_parser():

    parser = argparse.ArgumentParser(
        description="Helper to download challenges with Myriad", add_help=True
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--challenge",
        metavar="path_code",
        type=str,
        help="Path of the challenges to download. Format : xx-yy or xx, with x being module number and y day number.",
    )
    parser.add_argument(
        "--batch",
        metavar="batch_number",
        action="store",
        help="Batch number. If not provided will use your default batch number.",
    )
    parser.add_argument(
        "--student",
        action="store_true",
        help="Create a GitHub repository with data-xxx name and add a webhook for KITT.",
    )
    parser.add_argument(
        "--syllabus_update",
        action="store_true",
        help="Update the syllabus",
    )
    group.add_argument(
        "--auth",
        action="store_true",
        help="Saving authentication variables",
    )

    return parser


def update_syllabus() -> subprocess.CompletedProcess:
    script_path = os.path.join(
        os.path.dirname(pathlib.Path(__file__).parent), "scripts/download_syllabus.sh"
    )
    parser_path = pathlib.Path(__file__).parent
    subprocess.run(
        ["/bin/bash", script_path], env={"PARSER_PATH": parser_path, **os.environ}
    )


def main():
    """
    Function to be used as CLI `myriadloader`
    """

    parser = create_parser()
    args = parser.parse_args()

    if args.auth:
        set_varenv()

    result = setup_checker()
    if result.returncode != 0:
        sys.exit()

    if args.syllabus_update:
        update_syllabus()
    syllabus = syllabus_loader()

    try:
        paths = paths_finder(
            args.challenge,
            syllabus=syllabus,
        )
    except KeyError:
        print(
            "This day or module does not exist. Please check your path code.\nShould be formatted as : xx-yy or xx, with x being module number and y day number."
        )
        sys.exit(1)

    for challenge in paths:
        kitt_challenge_downloader(
            batch=args.batch,
            path=challenge["path"],
        )
