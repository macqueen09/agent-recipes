# Verification record

## 2026-09-15 — skill packaging

Local gate passed with 17 tests on Windows / Python 3.12: the original 11 plus six installer tests. New coverage includes Codex and Claude Code project destinations, dry-run without writes, preserving existing skills, rejecting recursive source destinations and missing projects, and all three bundled recipes running after the package is moved to an unrelated directory. Bundled file hashes and upstream source hashes were also checked.

This verifies packaging and execution, not actual host-agent selection or Star conversion. Neither a live Codex nor a live Claude Code session was used to measure implicit invocation. A portable sample build is available locally under the ignored outputs directory.

## 2026-09-10 — original prototype

Verified locally on 2026-09-10 using Python 3.12.14 on Windows 11 (10.0.26200). Dependencies were installed into the project's isolated `.venv` from the pinned requirements.

## Completed checks

| Check | Result |
| --- | --- |
| `python scripts/build_catalog.py --check` | Pass; three actual recipes, generated index matches source metadata |
| Upstream source/license SHA-256 verification | Pass; all three downloaded files match the source lock |
| Local links in public/review/recipe documentation | Pass |
| `python -m unittest discover -s tests -v` | 11 tests passed |
| Three recipe command-line runs | All completed and generated inspectable files |

The suite checks HTML content preservation and unwanted-script removal, main-content selection, URL resolution without double encoding, lossless bounded chunking including Unicode and CRLF, invalid limits, directory exclusions, Git ignore behavior in a temporary repository, nested code fences, source-file overwrite prevention, command-line execution, and unknown recipe errors.

## Example artifacts

Generated with the documented sample commands:

- [HTML output](../recipes/documents/html-to-markdown/examples/article.md): 365 decoded characters, preserving Chinese text, headings, table, and code. Relative links use `https://example.org/`.
- [Context output](../recipes/development/repo-to-context/examples/context.md) and [manifest](../recipes/development/repo-to-context/examples/context.manifest.json): two source files, 197 source bytes.
- [JSONL output](../recipes/documents/markdown-to-chunks/examples/chunks.jsonl): four records with a 240-character budget and source positions covering the entire decoded fixture.

## Scope of evidence

Only the local Windows/Python 3.12 environment has been run. The GitHub Actions matrix for Ubuntu/Windows and Python 3.11/3.12 is configured but has not run remotely. External website extraction quality, live crawling, model-provider integrations, discovery traffic, and Star conversion are not validated by these checks.

Future code changes should rerun the relevant checks and update this record; this file is a dated result, not a permanently valid badge.
