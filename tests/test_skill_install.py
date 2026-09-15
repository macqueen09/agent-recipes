import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("install_skill", ROOT / "scripts/install_skill.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class SkillInstallTests(unittest.TestCase):
    def test_portable_bundle_runs_all_recipes_after_relocation(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            installer.install(base / "built")
            (base / "built").rename(base / "relocated")
            bundle = base / "relocated"
            manifest = json.loads((bundle / "bundle.json").read_text())
            for name, expected in manifest["files"].items():
                self.assertEqual(hashlib.sha256((bundle / name).read_bytes()).hexdigest(), expected)
            self.assertFalse(any(".venv" in name or "__pycache__" in name for name in manifest["files"]))
            source_lock = json.loads((bundle / "runtime/third_party/sources.lock.json").read_text())
            for entry in source_lock["files"]:
                self.assertEqual(hashlib.sha256((bundle / "runtime" / entry["local_path"]).read_bytes()).hexdigest(), entry["sha256"])
            for recipe in ("html-to-markdown", "repo-to-context", "markdown-to-chunks"):
                output = base / (recipe + ".out")
                result = subprocess.run([sys.executable, str(bundle / "runtime/scripts/run_recipe.py"), recipe, "--output", str(output)], cwd=base, capture_output=True, text=True, encoding="utf-8")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertGreater(output.stat().st_size, 0)
                if recipe == "markdown-to-chunks":
                    rows = [json.loads(line) for line in output.read_text(encoding="utf-8").splitlines()]
                    expected = (bundle / "runtime/recipes/documents/markdown-to-chunks/fixtures/notes.md").read_text(encoding="utf-8")
                    self.assertEqual("".join(row["text"] for row in rows), expected)

    def test_both_project_locations(self):
        with tempfile.TemporaryDirectory() as temporary:
            for agent, folder in (("codex", ".agents"), ("claude", ".claude")):
                result = subprocess.run([sys.executable, str(ROOT / "scripts/install_skill.py"), "--agent", agent, "--project", temporary], capture_output=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertTrue((Path(temporary) / folder / "skills/agent-recipes/SKILL.md").is_file())

    def test_dry_run_does_not_create_directories(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "new-parent" / "skill"
            self.assertTrue(installer.install(output, dry_run=True)["dry_run"])
            self.assertFalse(output.parent.exists())

    def test_existing_skill_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "existing"
            target.mkdir()
            original = target / "SKILL.md"
            original.write_text("custom skill")
            with self.assertRaises(FileExistsError):
                installer.install(target)
            self.assertEqual(original.read_text(), "custom skill")

    def test_source_directories_are_not_install_destinations(self):
        with self.assertRaises(ValueError):
            installer.install(ROOT / "recipes" / "nested-skill", dry_run=True)

    def test_cli_requires_an_existing_project(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "absent"
            result = subprocess.run([sys.executable, str(ROOT / "scripts/install_skill.py"), "--agent", "codex", "--project", str(target)], capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(target.exists())
