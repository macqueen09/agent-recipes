"""Fetch the small, pinned upstream files used by this prototype.

This script downloads source and license text only; it never runs upstream code.
"""
import hashlib
from datetime import date
import json
from pathlib import Path
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    {
        "project": "microsoft/markitdown",
        "commit": "6270920c28000d217774ea29fa7a9262d7d5c65b",
        "license": "MIT",
        "files": {
            "packages/markitdown/src/markitdown/converters/_markdownify.py": "recipes/documents/html-to-markdown/vendor/markitdown_markdownify.py",
            "LICENSE": "recipes/documents/html-to-markdown/vendor/LICENSE.markitdown",
        },
    },
    {
        "project": "simonw/files-to-prompt",
        "commit": "1b234ff6dccb2ca3e56b5c256696558fb85306dc",
        "license": "Apache-2.0",
        "files": {
            "LICENSE": "third_party/licenses/files-to-prompt.LICENSE",
        },
    },
]


def fetch(url):
    for attempt in range(3):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "AgentRecipes-source-review/0.1"})
            with urllib.request.urlopen(request, timeout=20) as response:
                return response.read()
        except Exception:
            if attempt == 2:
                raise
            time.sleep(1)


def main():
    manifest = {"retrieved_on": date.today().isoformat(), "files": []}
    for source in SOURCES:
        for remote, local in source["files"].items():
            url = f"https://raw.githubusercontent.com/{source['project']}/{source['commit']}/{remote}"
            data = fetch(url)
            destination = ROOT / local
            if destination.exists() and destination.read_bytes() != data:
                raise RuntimeError(f"Refusing to overwrite modified local source: {local}")
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
            manifest["files"].append({"project": source["project"], "commit": source["commit"], "license": source["license"], "source_url": url, "local_path": local, "sha256": hashlib.sha256(data).hexdigest(), "modified": False})
            print(f"Fetched {local}", flush=True)
    output = ROOT / "third_party" / "sources.lock.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
