# Agent Recipes

**Small, runnable recipes that turn everyday tasks into inspectable files.**

[简体中文](README.zh-CN.md) · [Browse recipes](docs/CATALOG.md) · [Machine-readable catalog](catalog.json) · [Contribute](CONTRIBUTING.md)

Save a web page as Markdown. Pack a code directory for review. Split a long document while keeping its source and exact positions.

Each recipe includes runnable Python, a sample input, an example output, dependency pins, and a clear account of what was reused. Run it yourself or ask your coding agent to use it for your task.

> This collection is growing. **Star to keep useful recipes close at hand and support the project.** For new-release notifications, choose **Watch → Custom → Releases**. Star is a bookmark, not a notification subscription.

## Try a recipe

Requires Python 3.11+; Git is recommended for repository context packs. Initial dependency installation needs internet access. The three included recipes then run locally without API keys or network requests.

From this repository's root, using your chosen Python environment:

```sh
python -m pip install -r requirements.txt
python scripts/run_recipe.py
python scripts/run_recipe.py html-to-markdown
python scripts/run_recipe.py repo-to-context
python scripts/run_recipe.py markdown-to-chunks --max-chars 240
```

Results appear in `outputs/`. See [environment setup](docs/QUICKSTART.md) for isolated Windows and macOS/Linux environments.

## Choose by outcome

| I need to… | Recipe | Example result |
| --- | --- | --- |
| Make a saved HTML page easy to read and reuse | [HTML → Markdown](recipes/documents/html-to-markdown/README.md) | [article.md](recipes/documents/html-to-markdown/examples/article.md) |
| Give an agent selected code with file boundaries | [Directory → context](recipes/development/repo-to-context/README.md) | [context.md](recipes/development/repo-to-context/examples/context.md) |
| Prepare a document for retrieval or batch reading | [Markdown → JSONL](recipes/documents/markdown-to-chunks/README.md) | [chunks.jsonl](recipes/documents/markdown-to-chunks/examples/chunks.jsonl) |

These are task tools an agent can use, with deterministic outputs. The prototype does not include an autonomous agent runtime, a hosted search service, or an LLM summarizer.

## Use with an agent

**Install as a project skill:** [Codex / Claude Code setup](docs/AGENT_SKILL.md). From this checkout, with an existing target project:

```sh
python scripts/install_skill.py --agent codex --project /path/to/your/project
python scripts/install_skill.py --agent claude --project /path/to/your/project
```

The installed skill bundles all three recipes and can run independently of this checkout. Dependency installation remains separate. [Feature priorities and growth TODO](TODO.md).

Describe the task and provide this repository. For example:

> Use the html-to-markdown recipe to convert my saved HTML file. Keep the original unchanged, show me the generated Markdown, and report any limitations.

Agents can inspect [catalog.json](catalog.json) to choose a recipe by input, output, tags, and requirements. Read that recipe's setup and limitations before running it. Available commands can be searched locally:

```sh
python scripts/run_recipe.py --search context
```

## Built to grow

Recipes live in `recipes/<category>/<recipe-id>/`. Each owns its code, sample input, dependencies, and documentation. Adding a recipe regenerates the catalog; no framework registration or central application rewrite is needed.

[Architecture](docs/ARCHITECTURE.md) · [Roadmap](docs/ROADMAP.md) · [Changelog](CHANGELOG.md) · [Verification](docs/VERIFICATION.md)

## Credits and license

The HTML recipe includes an unmodified MIT-licensed conversion module from [Microsoft MarkItDown](https://github.com/microsoft/markitdown). The context recipe uses [Simon Willison's files-to-prompt](https://github.com/simonw/files-to-prompt), licensed under Apache-2.0. Recipe organization was informed by [OpenClaw Cookbook](https://github.com/openclaw/cookbook).

Original contributions are [MIT licensed](LICENSE). Upstream material retains its own licenses and attribution. See [third-party notices](THIRD_PARTY_NOTICES.md) and the [source lock](third_party/sources.lock.json).

Status: initial prototype, version 0.1.0. Recipe coverage and the ongoing maintenance cadence are still evolving.
