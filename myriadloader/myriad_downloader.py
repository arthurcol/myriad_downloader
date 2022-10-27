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
    Check if the setup has been done correctly and needed exec are installed.
    """

    script = """
for program in curl tar git gh ; do
  if ! type "$program" &>/dev/null ; then
    echo "$program" is not installed. Please review your setup: https://github.com/lewagon/setup#in-english
    exit 1
fi
done
    """
    subprocess.run(script, shell=True, check=True, executable="/bin/bash")


def challenge_downloader(
    token: str,
    gh_username: str,
    batch: str,
    path: str,
    github_name: str,
    is_student=False,
) -> subprocess.CompletedProcess:
    """
    Download a challenge given its path
    """

    script = f"""
mkdir -p ~/code/lewagon/{path} && cd $_
if [ "$(ls -A .)" ] ; then
  echo "$(pwd)" folder is not empty. Overwrite existing challenge ? [Y/n]
  read input
  if [[ $input == "Y" || $input == "y" ]]; then
    curl --silent -L -H "Authorization: Token {token}" "https://kitt.lewagon.com/camps/{batch}/challenges/download?gh={gh_username}&path={path.replace('/','%2F')}" |tar -xz --strip 1
    echo "✅ {path} downloaded"
  else
    echo "❌ Challenge not downloaded"
    exit 0
  fi
else
  curl --silent -L -H "Authorization: Token {token}" "https://kitt.lewagon.com/camps/{batch}/challenges/download?gh={gh_username}&path={path.replace('/','%2F')}" | tar -xz --strip 1
  echo "✅ {path} downloaded"
fi
    """
    if is_student:
        script += f"""

git init
gh repo create data-{github_name} --private --source=.

git add . && git commit -m 'Initiate challenge'
if ! [ "$(git remote)" ] ; then
  git remote add origin git@github.com:{gh_username}/data-{github_name}.git
fi
        """

    subprocess.run(script, shell=True, check=True, executable="/bin/bash")


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


def get_varenv():
    """
    Get environment variables KITT_TOKEN, GH_USERNAME and DEFAULT_BATCH. If they do
    not exist, will prompt the user to set them.
    """
    if os.getenv("KITT_TOKEN") == None:
        token = input("Enter your KITT token\n")
        cmd = f"""
        echo '# LeWagon Kitt token to download Myriad challenges' >> ~/.zshrc
        echo 'export KITT_TOKEN="{token}"' >> ~/.zshrc
        export KITT_TOKEN="{token}"
        """
        subprocess.run(cmd, shell=True, check=True)
        print("Saved. Restart zsh to avoid this prompt next time.")
    else:
        token = os.getenv("KITT_TOKEN")
    if os.getenv("GH_USERNAME") == None:
        gh_username = subprocess.run(
            "gh api 'https://api.github.com/user' | jq .login",
            capture_output=True,
            shell=True,
            text=True,
        ).stdout
        cmd = f"""
        echo '# GitHub Username' >> ~/.zshrc
        echo 'export GH_USERNAME={gh_username}' >> ~/.zshrc
        export GH_USERNAME=${gh_username}
        """
        subprocess.run(cmd, shell=True, check=True)
        print("GitHub username saved. Restart zsh to avoid this prompt next time.")
    else:
        gh_username = os.getenv("GH_USERNAME")
    if os.getenv("DEFAULT_BATCH") == None:
        batch = input("Enter the batch number to use by default\n")
        cmd = f"""
        echo '# LeWagon batch number to use to download Myriad challenges' >> ~/.zshrc
        echo 'export DEFAULT_BATCH="{batch}"' >> ~/.zshrc
        export DEFAULT_BATCH="{batch}"
        """
        subprocess.run(cmd, shell=True, check=True)
        print("Saved. Restart zsh to avoid this prompt next time.")
    else:
        batch = os.getenv("DEFAULT_BATCH")
    return token, gh_username, batch


def create_parser():

    parser = argparse.ArgumentParser(
        description="Helper to download challenges with Myriad", add_help=True
    )
    parser.add_argument(
        "challenge",
        metavar="challenges_path_code",
        type=str,
        help="Path of the challenges to download. Format : xx-yy or xx, with x being module number and y day number.",
    )
    parser.add_argument(
        "--batch",
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
    setup_checker()

    parser = create_parser()
    args = parser.parse_args()

    if args.syllabus_update:
        update_syllabus()
    syllabus = syllabus_loader()

    paths = paths_finder(
        args.challenge,
        syllabus=syllabus,
    )

    if args.batch:
        kitt_token, gh_username, _ = get_varenv()
        batch = args.batch
    else:
        kitt_token, gh_username, batch = get_varenv()

    for challenge in paths:
        challenge_downloader(
            token=kitt_token,
            gh_username=gh_username,
            batch=batch,
            path=challenge["path"],
            github_name=challenge["github_name"],
            is_student=args.student,
        )
