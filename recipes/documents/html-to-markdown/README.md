# Saved HTML → Markdown

[中文](README.zh-CN.md) · [All recipes](../../../docs/CATALOG.md)

Use this recipe when you already have a saved HTML page and want headings, paragraphs, links, lists, tables, and code in Markdown.

## Run

From the repository root after installing requirements:

```sh
python scripts/run_recipe.py html-to-markdown
python scripts/run_recipe.py html-to-markdown --input page.html --base-url https://example.org/ --output outputs/page.md
```

To copy out this recipe, keep the complete folder including `vendor/`, install its requirements, and run `python main.py`.

Input: one UTF-8 HTML file, at most 5 MB. Output: one Markdown file; default `outputs/article.md`. `--base-url` resolves relative links and never fetches a page.

Compare the [original fixture](fixtures/article.html) with the [generated example](examples/article.md). The example was produced with `--base-url https://example.org/`.

## How it works and limits

Beautiful Soup parses the document. The wrapper removes script/style/noscript/template elements and prefers the first `main` or `article` element. Microsoft's conversion module then renders Markdown. This handles simple saved documents; it does not execute JavaScript, log into sites, perform OCR, or guarantee perfect main-content extraction. Reading a converted document still requires evaluating its content; conversion is not a prompt-injection filter.

## Reuse

`vendor/markitdown_markdownify.py` is an unmodified source module from [Microsoft MarkItDown](https://github.com/microsoft/markitdown), fixed to commit `6270920c28000d217774ea29fa7a9262d7d5c65b`. Its [MIT license](vendor/LICENSE.markitdown) travels with the file. The wrapper and fixture are original. Installed dependencies are pinned in [requirements.txt](requirements.txt).

> Useful for your work? Star the growing recipe collection to find it again. For new-release notifications, use Watch → Custom → Releases.

