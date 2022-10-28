Download Le Wagon challenges with nice repo architecture (like we used to have before Myriad).

## Installation
Before installing `myriadloader` make sure you have access to `lewagon/data-meta` repo [here](https://github.com/lewagon/data-meta/blob/master/syllabus.yml).

```bash
pip install git+https://github.com/arthurcol/myriad_downloader.git
```

## Usage
You will need to first run
```bash
myriadloader --auth
```

To download a specific day for batch 1002:
```bash
myriadloader --challenge 05-01 --batch 1002
```

To download a full module for your default batch:
```bash
myriadloader --challenge 05
```

If you are running myriadloader as a student, it will also create github repositories in your GitHub with a webhook for KITT.

If the syllabus is updated and you want to take those changes into account:
```bash
myriadloader 00 --syllabus_update
```
This will execute again the loading of the syllabus from `lewagon/data-meta`.
