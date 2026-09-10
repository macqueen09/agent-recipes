# Quickstart / 快速开始

Use Python 3.11 or newer. Initial dependency installation uses the network. All current sample runs then work locally without model credentials. Git is needed for the verification suite and recommended for code-directory ignore rules.

## Windows PowerShell

From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe scripts/run_recipe.py html-to-markdown
.\.venv\Scripts\python.exe scripts/run_recipe.py repo-to-context
.\.venv\Scripts\python.exe scripts/run_recipe.py markdown-to-chunks --max-chars 240
.\.venv\Scripts\python.exe scripts/check.py
```

No activation command is required. If `python` resolves to an unrelated application, use the full path to your Python installation when creating the environment.

## macOS / Linux

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/run_recipe.py html-to-markdown
.venv/bin/python scripts/run_recipe.py repo-to-context
.venv/bin/python scripts/run_recipe.py markdown-to-chunks --max-chars 240
.venv/bin/python scripts/check.py
```

## Use your own inputs

Substitute the Python executable from your environment:

```sh
python scripts/run_recipe.py html-to-markdown --input saved-page.html --base-url https://example.org/ --output outputs/my-page.md
python scripts/run_recipe.py repo-to-context --input path/to/project --output outputs/my-context.md
python scripts/run_recipe.py markdown-to-chunks --input outputs/my-page.md --source my-page --max-chars 1200 --output outputs/my-chunks.jsonl
```

The HTML command reads the saved file; `--base-url` only resolves links. The context command writes an adjacent manifest listing included and skipped files. The chunk command records offsets in decoded Unicode characters, not bytes or tokens.

## Copy only one recipe

Copy its entire folder, including `vendor/` and upstream license files when present. Inside that folder:

```sh
python -m pip install -r requirements.txt
python main.py
```

The standalone recipe does not import a private module from the repository root. It uses its own bundled fixture by default and writes under the current directory's `outputs/`.

> 配方库持续扩充中。欢迎 Star 收藏，方便回访；新版本通知请使用 Watch → Custom → Releases。

