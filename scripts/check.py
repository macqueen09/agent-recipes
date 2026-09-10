"""Run the prototype's offline verification gate after dependency installation."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]


def main():
    subprocess.run([sys.executable, "scripts/build_catalog.py", "--check"], cwd=ROOT, check=True)
    source_manifest = json.loads((ROOT / "third_party/sources.lock.json").read_text(encoding="utf-8"))
    for entry in source_manifest["files"]:
        path = ROOT / entry["local_path"]
        if hashlib.sha256(path.read_bytes()).hexdigest() != entry["sha256"]:
            raise SystemExit(f"Upstream file changed without provenance update: {path}")
    broken = []
    documents = [ROOT / "README.md", ROOT / "README.zh-CN.md", ROOT / "REVIEW.zh-CN.md", ROOT / "CONTRIBUTING.md", ROOT / "THIRD_PARTY_NOTICES.md"]
    documents += list((ROOT / "docs").rglob("*.md")) + list((ROOT / "recipes").glob("*/*/README*.md"))
    for document in documents:
        for target in re.findall(r"\]\(([^\s)]+)\)", document.read_text(encoding="utf-8")):
            if target.startswith(("https://", "http://", "mailto:", "#")):
                continue
            path = unquote(target.split("#", 1)[0])
            if path and not (document.parent / path).exists():
                broken.append(f"{document.relative_to(ROOT)}: {target}")
    if broken:
        raise SystemExit("Broken local links:\n" + "\n".join(broken))
    subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], cwd=ROOT, check=True)
    print(f"PASS: catalog, {len(source_manifest['files'])} upstream hashes, local document links, and recipe tests")


if __name__ == "__main__":
    main()

