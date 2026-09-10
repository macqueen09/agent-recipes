"""Split UTF-8 Markdown into lossless character-bounded JSONL records."""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def split_markdown(text, max_chars=1200, source="document.md"):
    if max_chars < 32:
        raise ValueError("max-chars must be at least 32")
    start = 0
    index = 1
    while start < len(text):
        end = min(start + max_chars, len(text))
        if end < len(text):
            # Prefer a paragraph or line boundary in the last half of this window.
            floor = start + max_chars // 2
            for separator in ("\n\n", "\n", " "):
                boundary = text.rfind(separator, floor, end)
                if boundary >= floor:
                    end = boundary + len(separator)
                    break
        chunk = text[start:end]
        digest = hashlib.sha256((source + "\0" + str(start) + "\0" + chunk).encode("utf-8")).hexdigest()[:16]
        yield {"id": digest, "index": index, "source": source, "start_char": start, "end_char": end, "text": chunk}
        start = end
        index += 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=HERE / "fixtures" / "notes.md")
    parser.add_argument("--output", type=Path, default=Path("outputs/chunks.jsonl"))
    parser.add_argument("--max-chars", type=int, default=1200)
    parser.add_argument("--source", help="Stable source ID, URL, or filename recorded in each chunk")
    args = parser.parse_args()
    try:
        if args.input.resolve() == args.output.resolve():
            raise ValueError("input and output must be different files")
        if args.input.stat().st_size > 10_000_000:
            raise ValueError("document exceeds the prototype's 10 MB limit")
        # Preserve CRLF and all whitespace so offsets remain exact for decoded input.
        text = args.input.read_bytes().decode("utf-8-sig")
        records = list(split_markdown(text, args.max_chars, args.source or args.input.name))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in records), encoding="utf-8")
    except (OSError, ValueError) as error:
        parser.exit(2, f"Error: {error}\n")
    print(f"Wrote {args.output}: {len(records)} chunks")


if __name__ == "__main__":
    main()

