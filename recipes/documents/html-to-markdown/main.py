"""Convert a saved HTML document into Markdown, without network requests."""
import argparse
from pathlib import Path
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from vendor.markitdown_markdownify import _CustomMarkdownify

HERE = Path(__file__).resolve().parent


def convert_html(html, base_url=None):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "template"]):
        tag.decompose()
    # Prefer author-declared main content. This is not universal article extraction.
    content = soup.find("main") or soup.find("article") or soup.body or soup
    if base_url:
        if urlparse(base_url).scheme not in {"http", "https"}:
            raise ValueError("base-url must use http or https")
        for tag in content.find_all(True):
            for attribute in ("href", "src", "data-src"):
                if tag.get(attribute):
                    tag[attribute] = urljoin(base_url, tag[attribute])
    return _CustomMarkdownify(heading_style="ATX").convert_soup(content).strip() + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=HERE / "fixtures" / "article.html")
    parser.add_argument("--output", type=Path, default=Path("outputs/article.md"))
    parser.add_argument("--base-url", help="Resolve relative links; does not fetch this URL")
    args = parser.parse_args()
    try:
        if args.input.resolve() == args.output.resolve():
            raise ValueError("input and output must be different files")
        if args.input.stat().st_size > 5_000_000:
            raise ValueError("HTML exceeds the prototype's 5 MB input limit")
        text = convert_html(args.input.read_text(encoding="utf-8-sig"), args.base_url)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    except (OSError, ValueError) as error:
        parser.exit(2, f"Error: {error}\n")
    print(f"Wrote {args.output} ({len(text)} characters)")


if __name__ == "__main__":
    main()

