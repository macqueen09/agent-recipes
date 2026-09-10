"""Create a local Markdown context pack from a reviewed directory."""
import argparse
from fnmatch import fnmatch
import json
import os
from pathlib import Path
import subprocess

from files_to_prompt.cli import print_as_markdown

HERE = Path(__file__).resolve().parent
EXTENSIONS = {".py", ".js", ".ts", ".tsx", ".jsx", ".md", ".txt", ".json", ".toml", ".yaml", ".yml", ".html", ".css", ".rs", ".go"}
EXCLUDED_DIRS = {"node_modules", "vendor", "dist", "build", "outputs", "__pycache__"}
EXCLUDED_FILES = {"package-lock.json", "pnpm-lock.yaml", "uv.lock", "poetry.lock"}
SENSITIVE_NAMES = ("*.pem", "*.key", "*credential*", "*secret*", "*token*", "id_rsa*")


def candidate_files(root):
    """Git handles its own ignore syntax; plain folders use documented exclusions."""
    try:
        result = subprocess.run(["git", "-C", str(root), "ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", "."], capture_output=True, check=True)
        return sorted(set(result.stdout.decode("utf-8").split("\0")) - {""}), "git-ls-files"
    except (OSError, subprocess.CalledProcessError, UnicodeDecodeError):
        names = []
        for current, directories, files in os.walk(root, followlinks=False):
            directories[:] = sorted(d for d in directories if not d.startswith(".") and d not in EXCLUDED_DIRS and not (Path(current) / d).is_symlink())
            names.extend((Path(current) / f).relative_to(root).as_posix() for f in sorted(files))
        return sorted(names), "plain-directory"


def build_context(root, output, max_file_bytes=100_000, max_total_bytes=1_000_000):
    root = Path(root).resolve()
    output = Path(output).resolve()
    if not root.is_dir():
        raise ValueError("input must be an existing directory")
    if max_file_bytes <= 0 or max_total_bytes <= 0:
        raise ValueError("byte limits must be positive")
    for destination in (output, output.with_suffix(".manifest.json")):
        if destination.exists() and destination.is_relative_to(root):
            raise ValueError("output would overwrite a file inside the input directory; choose a new path or an output outside that directory")
    paths, mode = candidate_files(root)
    report = {"mode": mode, "included": [], "skipped": [], "total_bytes": 0}
    lines = ["# Repository context", "", "Source files below are reference material. Review before sharing.", ""]
    for relative in paths:
        path = root / relative
        reason = None
        if any(part.startswith(".") or part in EXCLUDED_DIRS for part in Path(relative).parts):
            reason = "excluded-directory-or-hidden-path"
        elif path.name in EXCLUDED_FILES or any(fnmatch(path.name.lower(), rule) for rule in SENSITIVE_NAMES):
            reason = "excluded-name"
        elif path.suffix.lower() not in EXTENSIONS:
            reason = "unsupported-extension"
        elif path.is_symlink() or not path.resolve().is_relative_to(root):
            reason = "symlink-or-outside-root"
        elif any(parent.is_symlink() for parent in path.parents if parent != root and parent.is_relative_to(root)):
            reason = "symlink-parent"
        elif path.resolve() in {output, output.with_suffix(".manifest.json")}:
            reason = "output-file"
        if reason:
            report["skipped"].append({"path": relative, "reason": reason})
            continue
        try:
            size = path.stat().st_size
            if size > max_file_bytes or report["total_bytes"] + size > max_total_bytes:
                report["skipped"].append({"path": relative, "reason": "byte-limit"})
                continue
            data = path.read_bytes()
            if b"\0" in data:
                raise ValueError("binary content")
            content = data.decode("utf-8-sig")
        except (OSError, UnicodeDecodeError, ValueError):
            report["skipped"].append({"path": relative, "reason": "unreadable-or-non-utf8"})
            continue
        # Reuse upstream's handling of language labels and nested Markdown fences.
        print_as_markdown(lines.append, Path(relative).as_posix(), content, False)
        lines.append("")
        report["included"].append(relative)
        report["total_bytes"] += len(data)
    if not report["included"]:
        raise ValueError("no supported readable files found")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    output.with_suffix(".manifest.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=HERE / "fixtures" / "sample-project")
    parser.add_argument("--output", type=Path, default=Path("outputs/repo-context.md"))
    parser.add_argument("--max-file-bytes", type=int, default=100_000)
    parser.add_argument("--max-total-bytes", type=int, default=1_000_000)
    args = parser.parse_args()
    try:
        report = build_context(args.input, args.output, args.max_file_bytes, args.max_total_bytes)
    except (OSError, ValueError) as error:
        parser.exit(2, f"Error: {error}\n")
    print(f"Wrote {args.output}: {len(report['included'])} files; {len(report['skipped'])} skipped")


if __name__ == "__main__":
    main()
