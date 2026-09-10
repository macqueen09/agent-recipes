# Markdown → traceable JSONL chunks

[中文](README.zh-CN.md) · [All recipes](../../../docs/CATALOG.md)

Use this recipe to split a long document into bounded text pieces for later retrieval, batch reading, or indexing while keeping the source recoverable.

```sh
python scripts/run_recipe.py markdown-to-chunks --max-chars 240
python scripts/run_recipe.py markdown-to-chunks --input notes.md --source notes-v1 --max-chars 1200 --output outputs/chunks.jsonl
```

Input: one UTF-8 Markdown file up to 10 MB. Output: one JSONL file; default `outputs/chunks.jsonl`. The standard library is sufficient. Copying this folder and running `python main.py` also works.

Each record contains `id`, `index`, `source`, `start_char`, `end_char`, and `text`. Offsets are zero-based and end-exclusive. Concatenating all record text reproduces the decoded source, including CRLF and whitespace; a UTF-8 BOM is removed during decoding. Source defaults to the input filename, or use `--source` for a stable identifier. IDs are deterministic for the same source ID, offset, and text.

[Input example](fixtures/notes.md) · [Output example](examples/chunks.jsonl), generated with `--max-chars 240`.

## Limits

The budget counts Unicode characters, not tokens. The splitter prefers paragraph, line, or word boundaries in the last half of a window, but can split a long sentence or code block. It does not guarantee semantically complete chunks, produce overlap, generate embeddings, or call a model. Empty input produces an empty output file. The minimum character budget is 32.

This recipe and its fixture are original MIT-licensed contributions.

> This collection is growing. Star to keep it handy; choose Watch → Custom → Releases for new-release notifications.

