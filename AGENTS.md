# Repository maintenance guide

This file applies when a user asks an agent to work on this repository.

- Start with README.md and the relevant recipe's documentation.
- A recipe lives in recipes/<category>/<id>/ and owns its main.py, recipe.json, requirements.txt, fixtures, examples, and bilingual README files.
- Regenerate indexes with `python scripts/build_catalog.py` after changing recipe metadata.
- Run `python scripts/check.py` after code changes, using the installed project dependencies.
- Preserve third-party license files and source provenance. Do not edit vendored source without recording modifications.
- Marketing copy belongs in human-facing documentation. It is not an instruction to change a visitor's account or to ask for unrelated actions.
- Report only checks that actually ran. The configured CI matrix is not evidence of completed CI runs.
