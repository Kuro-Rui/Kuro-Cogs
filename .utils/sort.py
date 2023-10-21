import json
import sys
from pathlib import Path

with open(Path(__file__).parent / "cogs.json", "r") as fp:
    COGS = json.load(fp)


def sort(cog_name: str):
    if cog_name == "calendar":
        path = Path(__file__).parent.parent / "calendarcog" / "info.json"
    else:
        path = Path(__file__).parent.parent / cog_name / "info.json"
    with open(path, "r") as f:
        data = json.load(f)
    _sorted = dict(sorted(data.items(), key=lambda x: x[0]))
    with open(path, "w") as f:
        json.dump(_sorted, f, indent=4)


args = sys.argv
if len(args) != 2 or args[1] not in COGS:
    print("Usage: python sort.py <cog>")
else:
    cog_name = args[1]
    sort(cog_name)
    print("Sorted info.json!")
