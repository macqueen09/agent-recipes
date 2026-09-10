# Contributing a recipe

Start from [templates/recipe](templates/recipe/README.md). A contribution should solve a concrete task and produce an inspectable result.

1. Copy the template to `recipes/<category>/<id>/` and implement `main.py`.
2. Replace the placeholder metadata with actual input/output requirements and origins.
3. Add small original or licensed fixtures, pinned dependencies, and a generated example result.
4. Write English and Chinese usage instructions, limitations, and source attribution.
5. Add behavior checks that would catch a wrong result. Do not label a placeholder runnable.
6. Regenerate the index and verify:

```sh
python scripts/build_catalog.py
python scripts/check.py
```

When reusing source, record the upstream URL, commit or version, license, local files, and changes. Retain required notices. Downloading source never counts as verifying that it works.

Keep changes within the task a recipe describes. Human-facing documentation may use the project's short Star/Watch copy; generated artifacts should contain only the requested task result.

Before claiming support for a new operating system or Python version, run the relevant checks in that environment and add the evidence to the verification record.

