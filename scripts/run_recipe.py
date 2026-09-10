"""List, find, and run a recipe from the generated catalog."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("recipe", nargs="?", help="Recipe ID; omit to list recipes")
    parser.add_argument("--search", help="Find recipes by task, title, or tag")
    args, extra = parser.parse_known_args()
    recipes = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))["recipes"]
    if args.recipe is None:
        if extra:
            parser.error(f"unrecognized arguments: {' '.join(extra)}")
        for recipe in recipes:
            searchable = " ".join([recipe["id"], recipe["title"], recipe["title_zh"], recipe["summary"], *recipe["tags"]]).casefold()
            if not args.search or args.search.casefold() in searchable:
                print(f"{recipe['id']}: {recipe['title']}")
        return
    matches = [recipe for recipe in recipes if recipe["id"] == args.recipe]
    if not matches:
        parser.error(f"unknown recipe: {args.recipe}")
    recipe = matches[0]
    entry = (ROOT / recipe["path"] / recipe["entrypoint"]).resolve()
    if not entry.is_relative_to(ROOT / "recipes") or not entry.is_file():
        parser.error("catalog entrypoint is outside recipes or does not exist")
    if extra and extra[0] == "--":
        extra = extra[1:]
    # Keep caller-relative paths meaningful. No shell interpolation is used.
    raise SystemExit(subprocess.run([sys.executable, str(entry), *extra]).returncode)


if __name__ == "__main__":
    main()

