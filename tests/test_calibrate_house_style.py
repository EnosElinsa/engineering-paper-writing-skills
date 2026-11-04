from __future__ import annotations

import contextlib
import importlib.util
import io
import pathlib
import shutil
import tempfile
import unittest

from scripts import calibrate_house_style as C


ROOT = pathlib.Path(__file__).resolve().parents[1]
FILES = (C.SCRIPT, C.STYLE, C.ZH)


def sentence(words: int, topic: str) -> str:
    filler = "the controller assigns every robot to one delivery zone of the campus in each planning cycle".split()
    body = [topic] + [filler[i % len(filler)] for i in range(words - 1)]
    return " ".join(body).capitalize() + "."


def paragraph(lengths: list[int], topic: str) -> str:
    return " ".join(sentence(n, topic) for n in lengths)


def paper(scale: int) -> str:
    """A synthetic paper in the Markdown layout of the reference corpus; scale shifts sentence lengths."""
    sections = [
        ("I. INTRODUCTION", [18, 22, 26, 20]),
        ("II. RELATED WORK", [22, 24, 28, 21]),
        ("III. SYSTEM MODEL AND PROBLEM FORMULATION", [19, 23, 21, 25]),
        ("IV. PROPOSED ALGORITHM", [20, 22, 24, 18]),
        ("V. EXPERIMENTAL STUDIES", [23, 25, 21, 27]),
        ("VI. CONCLUSION", [24, 26, 28, 22, 25, 27, 23]),
    ]
    lines = ["# Synthetic Paper", "", "Abstract—" + paragraph([28 + scale] * 8, "campus"), ""]
    for title, lengths in sections:
        lines += [f"## {title}", ""]
        for index in range(3 if "CONCLUSION" not in title else 1):
            lines += [paragraph([n + scale + index for n in lengths], "robots"), ""]
    lines.append("## REFERENCES")
    return "\n".join(lines) + "\n"


class CalibrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.temp.name)
        for relative in FILES:
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, target)
        self.refs = self.root / "refs"
        self.refs.mkdir()
        for scale in (0, 2, 4):
            (self.refs / f"paper-{scale}.md").write_text(paper(scale), encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_tool(self, *extra: str) -> tuple[int, str]:
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code = C.main(["--root", str(self.root), "--references", str(self.refs), "--abstract-limit", "250", *extra])
        return code, buffer.getvalue()

    def module(self):
        spec = importlib.util.spec_from_file_location("calibrated", self.root / C.SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_write_updates_all_generated_blocks_consistently(self) -> None:
        code, _ = self.run_tool("--check")
        self.assertEqual(code, 1, "synthetic corpus should differ from the shipped band")
        code, output = self.run_tool("--write")
        self.assertEqual(code, 0)
        self.assertIn("note:", output)
        code, _ = self.run_tool("--check")
        self.assertEqual(code, 0, "a second run must find no difference")

        module = self.module()
        band = module.TEAM_BAND
        self.assertIn("initial_per_100", band, "connective rules must survive recalibration")
        style = (self.root / C.STYLE).read_text(encoding="utf-8")
        zh = (self.root / C.ZH).read_text(encoding="utf-8")
        low, high = band["body"]["mean"]
        self.assertIn(f"{low:.1f}–{high:.1f}", style)
        self.assertIn("Reference papers (three)", style)
        for (low, high) in band["section_mean"].values():
            self.assertIn(f"{low:.1f}–{high:.1f}", style)
        for key in ("abstract_words", "conclusion_words"):
            self.assertIn(f"{band[key][0]}–{band[key][1]} words", style)
        self.assertEqual(band["abstract_words"][1], 250)
        zh_band = module.TEAM_BAND_ZH
        low, high = zh_band["body"]["mean"]
        self.assertIn(f"{low}–{high}", zh)

    def test_requires_two_references(self) -> None:
        for path in list(self.refs.iterdir())[1:]:
            path.unlink()
        with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(ValueError):
            C.main(["--root", str(self.root), "--references", str(self.refs)])


class ShippedBlocksTests(unittest.TestCase):
    def test_shipped_files_carry_the_generated_blocks(self) -> None:
        script = (ROOT / C.SCRIPT).read_text(encoding="utf-8")
        self.assertIn("# calibrate:begin band", script)
        self.assertIn("# calibrate:end band", script)
        for relative, name in ((C.STYLE, "rhythm"), (C.ZH, "zh-rhythm")):
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn(f"<!-- calibrate:begin {name} -->", text)
            self.assertIn(f"<!-- calibrate:end {name} -->", text)

    def test_rendering_reproduces_the_shipped_band_literal(self) -> None:
        module = C.load_fingerprint(ROOT)
        rendered = C.render_band(C.current_band(module))
        script = (ROOT / C.SCRIPT).read_text(encoding="utf-8")
        self.assertIn(rendered, script)


if __name__ == "__main__":
    unittest.main()
