# Third-party notices

Original Agent Recipes code and fixtures use the root MIT license. Third-party code keeps the terms listed below; the root license does not replace them. This project is independent of the upstream maintainers.

| Upstream | Reuse in this prototype | License | Local record |
| --- | --- | --- | --- |
| [microsoft/markitdown](https://github.com/microsoft/markitdown) | Exact copy of converters/_markdownify.py, used by the HTML recipe | MIT; Copyright Microsoft Corporation | [Original license](recipes/documents/html-to-markdown/vendor/LICENSE.markitdown), [module](recipes/documents/html-to-markdown/vendor/markitdown_markdownify.py) |
| [simonw/files-to-prompt](https://github.com/simonw/files-to-prompt) | Installed package 0.6; call print_as_markdown for fence-safe code formatting | Apache-2.0 | [License snapshot](third_party/licenses/files-to-prompt.LICENSE), [dependency pins](recipes/development/repo-to-context/requirements.txt) |
| [python-markdownify](https://github.com/matthewwithanm/python-markdownify) | Installed package 1.2.3; HTML conversion engine | MIT | [Dependency pins](recipes/documents/html-to-markdown/requirements.txt) |
| [OpenClaw Cookbook](https://github.com/openclaw/cookbook) | Organizational reference only; no code or prose copied | MIT in inspected repository | [Research notes](docs/research/PROJECTS.zh-CN.md) |
| [Microsoft AgenticCookBook](https://github.com/microsoft/AgenticCookBook) | Comparative research only; no files copied | MIT in inspected repository | [Research notes](docs/research/PROJECTS.zh-CN.md) |

Dependencies installed from PyPI also include Beautiful Soup, six, soupsieve, typing_extensions, Click, and (on Windows) colorama. Their distributions contain their own licenses. We do not vendor those distributions in this repository.

The [source lock](third_party/sources.lock.json) records exact upstream commits, original URLs, local paths, SHA-256 hashes, and modification status for downloaded source/license files. It is a source-file lock, not a package dependency lock. Python requirements separately pin the installed package versions.

The copied MarkItDown module has no local changes. The CLI wrapper, HTML fixture, directory selection and manifest logic, JSONL chunker, catalog tools, tests, and documentation were created for this prototype. Re-fetching the fixed source is optional with `python scripts/fetch_sources.py`; normal setup does not need that step.

