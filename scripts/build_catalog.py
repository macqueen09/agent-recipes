"""Build the machine-readable catalog and human-readable recipe index."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {"id", "title", "title_zh", "summary", "category", "tags", "input", "output", "entrypoint", "requires_network", "requires_credentials", "origin"}


def collect():
    recipes = []
    seen = set()
    for path in sorted((ROOT / "recipes").glob("*/*/recipe.json")):
        recipe = json.loads(path.read_text(encoding="utf-8"))
        missing = REQUIRED - recipe.keys()
        if missing:
            raise ValueError(f"{path}: missing {sorted(missing)}")
        if recipe["id"] in seen or recipe["id"] != path.parent.name:
            raise ValueError(f"Duplicate ID or folder/ID mismatch: {path}")
        if recipe["category"] != path.parent.parent.name:
            raise ValueError(f"Category/folder mismatch: {path}")
        if not isinstance(recipe["tags"], list) or not all(isinstance(t, str) for t in recipe["tags"]):
            raise ValueError(f"Invalid tags: {path}")
        for key in ("requires_network", "requires_credentials"):
            if not isinstance(recipe[key], bool):
                raise ValueError(f"{key} must be a JSON boolean: {path}")
        entry = (path.parent / recipe["entrypoint"]).resolve()
        if not entry.is_relative_to(path.parent.resolve()) or not entry.is_file():
            raise ValueError(f"Invalid entrypoint: {path}")
        for filename in ("README.md", "README.zh-CN.md", "requirements.txt"):
            if not (path.parent / filename).is_file():
                raise ValueError(f"Missing {filename}: {path.parent}")
        seen.add(recipe["id"])
        recipe["path"] = path.parent.relative_to(ROOT).as_posix()
        recipe["run"] = ["python", f"{recipe['path']}/{recipe['entrypoint']}"]
        recipes.append(recipe)
    if not recipes:
        raise ValueError("No runnable recipes found")
    return recipes


def render():
    recipes = collect()
    catalog = {"schema_version": 1, "project": "Agent Recipes", "stage": "review-prototype", "recipes": recipes}
    lines = ["# Recipe catalog / 配方目录", "", "Generated from each recipe.json; edit the source manifest to add a recipe.", "", "| Recipe | Task / 任务 | Category |", "| --- | --- | --- |"]
    for recipe in recipes:
        lines.append(f"| [{recipe['id']}](../{recipe['path']}/README.md) | {recipe['title_zh']} | {recipe['category']} |")
    lines += ["", "> This collection is growing. Star to keep it handy; use Watch → Custom → Releases for release notifications.", ""]
    return {ROOT / "catalog.json": json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", ROOT / "docs" / "CATALOG.md": "\n".join(lines)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs = render()
    for path, content in outputs.items():
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                raise SystemExit(f"Stale catalog: {path.name}; run python scripts/build_catalog.py")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    print(f"Catalog {'checked' if args.check else 'built'}: {len(collect())} recipes")


if __name__ == "__main__":
    main()

