Download Le Wagon challenges with nice repo architecture (like we used to have before Myriad).

## Installation
Before using `myriad_downloader.py` you need to run `yaml_parser.py` file after downloading the `syllabus.yml`
file from `lewagon/data-meta` repo [here](https://github.com/lewagon/data-meta/blob/master/syllabus.yml). Put it in this folder.

## Usage
First time you run the script, you will be asked to enter your Kitt Token and the batch number you want to use by default.
For this not to be prompted again, restart your zsh (your `.zshrc` has been appended with these variables)

To download a specific day for batch 1002:
```bash
python myriad_downloader.py 05-01 --batch 1002
```

To download a full module for your default batch:
```bash
python myriad_downloader.py 05
```

To download a full module for your default batch as a student:
```bash
python myriad_downloader.py 05 --student
```
In addition to downloading the challenges, it will also create github repositories in your GitHub with a webhook for KITT. __WIP__ : only create a repo on GitHub for now.
