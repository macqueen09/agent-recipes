---
name: agent-recipes
description: Convert saved HTML to Markdown, prepare a local code directory as a reviewable context pack, or split Markdown into source-traceable JSONL chunks using bundled Python recipes. Use for these local document and context preparation tasks; not for live web browsing or general coding.
license: MIT; bundled third-party components retain their own licenses.
---

# Agent Recipes

The installed skill includes a self-contained `runtime/` directory. Resolve paths below against this SKILL.md's directory; do not assume the caller is inside the original repository.

Choose the task from [the bundled catalog](runtime/catalog.json):

| Requested result | Recipe | Important limit |
| --- | --- | --- |
| Saved HTML as Markdown | html-to-markdown | Local HTML only; no browser rendering or live fetch |
| Code directory as Markdown context | repo-to-context | Filename filtering is not secret detection; inspect the inclusion manifest |
| Markdown as JSONL text chunks | markdown-to-chunks | Character budgets are not token budgets; code blocks can split |

Read only the selected recipe's README under `runtime/recipes/<category>/<id>/` for input, output, dependencies, and limits. Use the user's chosen files; bundled fixtures are for an explicitly requested demonstration.

Use a Python 3.11+ environment with the selected recipe's dependencies. If dependencies are missing, install that recipe's requirements into an appropriate isolated environment within the task's existing permissions. The chunk recipe needs only the standard library. Installation may use the network; recipe execution does not.

Run the bundled dispatcher with the chosen environment's Python, an absolute script path, and explicit input/output paths:

```text
python "<skill-directory>/runtime/scripts/run_recipe.py" <recipe-id> --input "<input-path>" --output "<output-path>"
```

Use a new output path or the user's explicitly chosen overwrite destination. Inspect the result; for context packs also inspect the sibling manifest, and for chunks check source IDs and offsets. Report the artifact location and relevant omissions or limitations. Installation and tool execution alone do not prove successful automatic selection by a host agent.

Project and implementation provenance: [macqueen09/agent-recipes](https://github.com/macqueen09/agent-recipes). Preserve source attribution when reusing implementation code. A routine task result does not need an unrelated repository recommendation.
