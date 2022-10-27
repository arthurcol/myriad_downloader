Download Le Wagon challenges with nice repo architecture (like we used to have before Myriad).

## Installation
Before installing `myriadloader` make sure you have access to `lewagon/data-meta` repo [here](https://github.com/lewagon/data-meta/blob/master/syllabus.yml).

```bash
pip install git+https://github.com/arthurcol/myriad_downloader.git
```

## Usage
First time you run the script, you will be asked to enter your Kitt Token and the batch number you want to use by default.
For this not to be prompted again, restart your zsh (your `.zshrc` has been appended with these variables)

To download a specific day for batch 1002:
```bash
myriadloader 05-01 --batch 1002
```

To download a full module for your default batch:
```bash
myriadloader 05
```

To download a full module for your default batch as a student:
```bash
python myriad_downloader.py 05 --student
```
In addition to downloading the challenges, it will also create github repositories in your GitHub with a webhook for KITT. __WIP__ : only create a repo on GitHub for now.

If the syllabus is updated and you want to take those changes into account:
```bash
myriadloader 00 --syllabus_update
```
This will execute again the loading of the syllabus from `lewagon/data-meta`.
