# Thanks Vexed!
# https://github.com/Vexed01/Vex-Cogs/blob/master/bump.py

import datetime
import json
import re
import sys
from pathlib import Path

with open(Path(__file__).parent / "cogs.json", "r") as fp:
    COGS = json.load(fp)
UPDATE_LEVELS = ("major", "minor", "patch")
VER_REGEX = r".*__version__ = \"(\d*)\.(\d*)\.(\d*)\".*"
DOCS_REGEX = r"(\n[A-Z]*\n\**\n\n)"


def bump(cog_name: str, update_level: str):
    if cog_name == "calendar":
        to_open = Path(__file__).parent.parent / "calendarcog" / f"{cog_name}.py"
    else:
        to_open = Path(__file__).parent.parent / cog_name / f"{cog_name}.py"
    with open(to_open, "r") as fp:
        file_data = fp.read()
    match = re.match(VER_REGEX, file_data, flags=re.S)
    if not match or len(match.groups()) != 3:
        print("Something doesn't look right with that file.")
        return
    old_ver = [int(match.group(1)), int(match.group(2)), int(match.group(3))]
    if update_level == "major":
        new_ver = [old_ver[0] + 1, 0, 0]
    elif update_level == "minor":
        new_ver = [old_ver[0], old_ver[1] + 1, 0]
    elif update_level == "patch":
        new_ver = [old_ver[0], old_ver[1], old_ver[2] + 1]
    old = ".".join(str(i) for i in old_ver)
    new = ".".join(str(i) for i in new_ver)
    new_data = file_data.replace(old, new)
    with open(to_open, "w") as fp:
        fp.write(new_data)
    return new


def changelog(cog_name: str, new_version: str):
    equals = "=" * (len(new_version) + 8)  # Version major.minor.patch
    date = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    extra_changelog = f"{equals}\nVersion {new_version}\n{equals}\n\n{date}\n\n"
    print(
        "It's now time to write the changelog. Input each bullet point separately. "
        "Enter a blank entry to finish."
    )
    while True:
        new_bullet = input("- ")
        if not new_bullet:
            break
        extra_changelog += f"- {new_bullet}\n"
    to_open = Path(__file__).parent.parent / "docs" / "source" / "changelog" / f"{cog_name}.rst"
    with open(to_open, "r") as fp:
        file_data = fp.read()
    match = re.sub(DOCS_REGEX, r"\1" + extra_changelog + r"\n", file_data, flags=re.I)
    with open(to_open, "w") as fp:
        fp.write(match)
    print("Changelog updated.")


args = sys.argv
if len(args) != 3 or args[1] not in COGS or args[2] not in UPDATE_LEVELS:
    print("Usage: python bump.py <cog> <update_level>")
else:
    new = bump(args[1], args[2])
    if new:
        changelog(args[1], new)
        print(f"New version: {new}")
