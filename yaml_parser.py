import yaml

with open("syllabus.yml", "r") as file:
    syllabus = yaml.load(file, Loader=yaml.Loader)

paths = {}

for module in syllabus["default"]["modules"].values():
    n_path = module["path"][:2]
    full_path = module["path"]
    name = module["name"]
    paths[n_path] = dict(name=name, full_path=full_path, days=dict())

for day in syllabus["default"]["days"].values():
    print(day["path"])
    if day["path"][:2] == "00":
        n_module = "00"
        n_day = "00"
    else:
        n_module = day["path"].split("/")[0][:2]
        n_day = day["path"].split("/")[1][:2]
    full_path = day["path"]
    exercises = [
        {"path": p["path"], "github_name": p["github_url"].split("/")[-1]}
        for p in day["exercises"]
    ]
    paths[n_module]["days"][n_day] = dict(daily_path=full_path, exercises=exercises)


with open("short_syllabus.yml", "w") as file:
    yaml.dump(paths, file)
