import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load_recipe(name, folder):
    path = ROOT / "recipes" / folder / name / "main.py"
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sys.path.pop(0)
    return module


html_recipe = load_recipe("html-to-markdown", "documents")
context_recipe = load_recipe("repo-to-context", "development")
chunk_recipe = load_recipe("markdown-to-chunks", "documents")


class RecipeTests(unittest.TestCase):
    def test_html_preserves_content_and_removes_scripts(self):
        result = html_recipe.convert_html('<main><h1>Title</h1><p>中文 <b>bold</b></p><script>bad()</script><a href="javascript:bad()">label</a></main>')
        self.assertIn("# Title", result)
        self.assertIn("中文 **bold**", result)
        self.assertIn("label", result)
        self.assertNotIn("bad()", result)

    def test_html_links_are_resolved_without_double_encoding(self):
        result = html_recipe.convert_html('<main><a href="/a%20b">Guide</a></main>', "https://example.org/docs/")
        self.assertIn("https://example.org/a%20b", result)
        self.assertNotIn("%2520", result)
        with self.assertRaises(ValueError):
            html_recipe.convert_html("<p>x</p>", "file:///tmp/")

    def test_html_prefers_main_content(self):
        result = html_recipe.convert_html("<body><nav>Noise</nav><main><p>Keep</p></main></body>")
        self.assertIn("Keep", result)
        self.assertNotIn("Noise", result)

    def test_chunking_is_lossless_and_bounded(self):
        text = ("# Title\r\n\r\n中文🙂 with whitespace.\n" * 60) + "trailing  \n"
        chunks = list(chunk_recipe.split_markdown(text, 71, "source.md"))
        self.assertEqual("".join(row["text"] for row in chunks), text)
        self.assertGreater(len(chunks), 1)
        for row in chunks:
            self.assertLessEqual(len(row["text"]), 71)
            self.assertEqual(text[row["start_char"]:row["end_char"]], row["text"])
        self.assertEqual(chunks, list(chunk_recipe.split_markdown(text, 71, "source.md")))

    def test_chunking_empty_and_invalid_limit(self):
        self.assertEqual(list(chunk_recipe.split_markdown("")), [])
        with self.assertRaises(ValueError):
            list(chunk_recipe.split_markdown("text", 0))

    def test_context_filters_and_preserves_nested_fences(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "project"
            root.mkdir()
            (root / "readme.md").write_text("中文\n```python\nprint(1)\n```\n", encoding="utf-8")
            (root / ".env").write_text("TOKEN=example-fixture")
            (root / "credentials.json").write_text('{"fixture": true}')
            (root / "big.txt").write_text("x" * 200)
            (root / "raw.txt").write_bytes(b"\x00binary")
            output = Path(temporary) / "context.md"
            report = context_recipe.build_context(root, output, 100, 500)
            self.assertEqual(report["included"], ["readme.md"])
            content = output.read_text(encoding="utf-8")
            self.assertIn("````", content)
            self.assertIn("中文", content)
            self.assertNotIn("TOKEN", content)
            self.assertEqual(len(report["skipped"]), 4)

    def test_context_uses_git_ignore_rules(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "project"
            root.mkdir()
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / ".gitignore").write_text("ignored/\n")
            (root / "ignored").mkdir()
            (root / "ignored" / "example.py").write_text("ignored = True")
            (root / "app.py").write_text("included = True")
            report = context_recipe.build_context(root, Path(temporary) / "context.md")
            self.assertEqual(report["mode"], "git-ls-files")
            self.assertEqual(report["included"], ["app.py"])

    def test_context_rejects_overwriting_a_source_file(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            original = root / "README.md"
            original.write_text("original content", encoding="utf-8")
            with self.assertRaises(ValueError):
                context_recipe.build_context(root, original)
            self.assertEqual(original.read_text(encoding="utf-8"), "original content")

    def test_all_recipe_commands_produce_artifacts(self):
        with tempfile.TemporaryDirectory() as temporary:
            for name in ("html-to-markdown", "repo-to-context", "markdown-to-chunks"):
                extension = ".jsonl" if name == "markdown-to-chunks" else ".md"
                output = Path(temporary) / (name + extension)
                completed = subprocess.run([sys.executable, str(ROOT / "scripts/run_recipe.py"), name, "--output", str(output)], cwd=temporary, capture_output=True, text=True, encoding="utf-8")
                self.assertEqual(completed.returncode, 0, completed.stderr)
                self.assertGreater(output.stat().st_size, 0)
                if extension == ".jsonl":
                    self.assertTrue(all(json.loads(line)["source"] == "notes.md" for line in output.read_text(encoding="utf-8").splitlines()))

    def test_commands_reject_overwriting_input(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "source.md"
            path.write_text("keep original")
            result = subprocess.run([sys.executable, str(ROOT / "scripts/run_recipe.py"), "markdown-to-chunks", "--input", str(path), "--output", str(path)], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(path.read_text(), "keep original")

    def test_unknown_recipe_fails(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/run_recipe.py"), "unknown"], capture_output=True)
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
