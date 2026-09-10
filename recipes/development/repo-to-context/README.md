# Code directory → context pack

[中文](README.zh-CN.md) · [All recipes](../../../docs/CATALOG.md)

Use this recipe to prepare a code directory for a review or an agent conversation, with relative filenames and Markdown code fences.

## Run

```sh
python scripts/run_recipe.py repo-to-context
python scripts/run_recipe.py repo-to-context --input path/to/project --output outputs/context.md
```

From a copied-out recipe folder: install its requirements, then run `python main.py`. No private root package is required.

Outputs: a Markdown context file and an adjacent `.manifest.json` that lists included files, skipped files, reasons, and total bytes. Defaults are `outputs/repo-context.md` and `outputs/repo-context.manifest.json`. See the [example](examples/context.md) and [manifest](examples/context.manifest.json).

An existing output file inside the input directory is rejected to avoid replacing source material. For repeated runs, choose an output location outside the input directory.

## Selection rules

When Git is available and recognizes the directory, `git ls-files --cached --others --exclude-standard` selects tracked and nonignored untracked files. Tracked files remain candidates even if an ignore rule matches them. Ordinary directories fall back to filesystem traversal with the exclusions below; `.gitignore` syntax is not interpreted in that fallback.

The recipe excludes hidden paths, common dependency/build directories, lockfiles, symlinks, unsupported extensions, binary/non-UTF-8 data, and some sensitive filename patterns. It enforces a default 100 KB per-file and 1 MB total source limit; change them with `--max-file-bytes` and `--max-total-bytes`.

Omitted files are not represented in the context. Git-ignored and pruned directories are not individually enumerated in the manifest. Filename rules are not a secret scanner: inspect the generated pack before sharing it. Nothing is uploaded. Syntax trees, semantic selection, token estimation, and model review are outside this prototype.

## Reuse

Markdown formatting calls `print_as_markdown` from [files-to-prompt](https://github.com/simonw/files-to-prompt) 0.6, an Apache-2.0 package. This preserves the upstream handling of nested fences. Traversal, selection, byte limits, and manifest generation are original. [Attribution and license](../../../THIRD_PARTY_NOTICES.md).

> Keep this growing collection handy with a Star. For new-release notifications, use Watch → Custom → Releases.
