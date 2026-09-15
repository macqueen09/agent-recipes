"""Build a portable skill or install it into an explicitly selected project."""
import argparse
import hashlib
import json
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[1]
AGENT_DIRS = {"codex": ".agents", "claude": ".claude"}
ROOT_FILES = ("catalog.json", "requirements.txt", "LICENSE", "THIRD_PARTY_NOTICES.md", "README.md", "README.zh-CN.md", "REVIEW.zh-CN.md", "CHANGELOG.md", "CONTRIBUTING.md", "TODO.md")
EXTENSIONS = {".py", ".md", ".json", ".jsonl", ".html", ".txt", ".markitdown", ".LICENSE"}


def payload(root=ROOT):
    """Explicit runtime allowlist; never copy environments or project settings."""
    root = Path(root).resolve()
    paths = [root / name for name in ROOT_FILES]
    paths += list((root / "scripts").glob("*.py")) + list((root / "tests").glob("*.py"))
    paths += [root / "skills/agent-recipes/SKILL.md"]
    for directory in ("recipes", "docs", "third_party", "templates"):
        paths += [p for p in (root / directory).rglob("*") if p.is_file()
                  and p.suffix in EXTENSIONS
                  and not any(part.startswith(".") or part in {"__pycache__", "outputs", "node_modules"} for part in p.relative_to(root).parts)]
    files = {"SKILL.md": (root / "skills/agent-recipes/SKILL.md").read_bytes()}
    for path in sorted(set(paths)):
        if path.is_symlink() or not path.resolve().is_relative_to(root):
            raise ValueError(f"Runtime source must stay inside the repository: {path}")
        data = path.read_bytes()
        if len(data) > 5_000_000:
            raise ValueError(f"Unexpectedly large runtime source: {path}")
        files["runtime/" + path.relative_to(root).as_posix()] = data
    return files


def install(destination, dry_run=False, root=ROOT):
    destination = Path(destination).expanduser().absolute()
    for directory in ("recipes", "docs", "third_party", "templates", "scripts", "tests", "skills"):
        if destination.resolve().is_relative_to((Path(root) / directory).resolve()):
            raise ValueError("Install outside source folders; use outputs/ for a portable build")
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(f"Destination already exists; preserve your existing skill and choose a new location: {destination}")
    files = payload(root)
    manifest = {"schema_version": 1, "project_url": "https://github.com/macqueen09/agent-recipes",
                "files": {name: hashlib.sha256(data).hexdigest() for name, data in sorted(files.items())}}
    if dry_run:
        return {"destination": str(destination), "files": len(files), "dry_run": True}
    destination.parent.mkdir(parents=True, exist_ok=True)
    # Assemble beside the destination so the final rename stays on one volume.
    # TemporaryDirectory owns only its newly created staging folder.
    with tempfile.TemporaryDirectory(prefix=".agent-recipes-build-", dir=destination.parent) as temporary:
        staging = Path(temporary) / "agent-recipes"
        staging.mkdir()
        for name, data in files.items():
            target = staging / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        (staging / "bundle.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        if destination.exists() or destination.is_symlink():
            raise FileExistsError(f"Destination appeared during installation: {destination}")
        staging.rename(destination)
    return {"destination": str(destination), "files": len(files), "dry_run": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--project", type=Path, help="Existing project to receive the skill")
    target.add_argument("--output", type=Path, help="New portable skill folder, without installing into a host")
    parser.add_argument("--agent", choices=sorted(AGENT_DIRS), help="Required with --project")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.project is not None:
        if not args.agent or not args.project.expanduser().is_dir():
            parser.error("--project requires an existing directory and --agent codex or claude")
        destination = args.project.expanduser().resolve() / AGENT_DIRS[args.agent] / "skills" / "agent-recipes"
    else:
        if args.agent:
            parser.error("--agent is only used with --project")
        destination = args.output
    try:
        result = install(destination, args.dry_run)
    except (OSError, ValueError) as error:
        parser.exit(2, f"Error: {error}\n")
    print(json.dumps(result, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
