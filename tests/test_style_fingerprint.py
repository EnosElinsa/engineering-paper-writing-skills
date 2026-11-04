from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import pathlib
import re
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "shared" / "scripts" / "style_fingerprint.py"
STYLE = ROOT / "shared" / "styles" / "team-house-style.md"
ZH = ROOT / "shared" / "languages" / "zh.md"


def _load():
    spec = importlib.util.spec_from_file_location("style_fingerprint", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


F = _load()

LONG = (
    "The controller assigns every robot to one delivery zone in each planning cycle according to the "
    "remaining battery level, the zone demand, and the distance to the charging station."
)

TEX = r"""
\documentclass{article}
\begin{document}
\begin{abstract}
Delivery robots serve campus zones. However, existing planners fix the station before operation.
\end{abstract}
\section{Introduction}
Campus delivery has emerged as a key service for large sites \cite{a,b}. Existing planners fix the
charging station before operation \cite{a}, which leaves robots far from the station late in the day.
Smith et al. studied the zone layout in Fig.~\ref{fig:x}, where $x_i$ denotes the zone load.

\section{Experimental Studies}
The robots move to their zones. They stop at the hover points. They charge at the station. The
station waits for them before the next cycle starts.
We compare four methods because they share one budget; the baselines follow their papers, but the
proposed algorithm uses the same population size and the same number of generations in every run.
Hence, the comparison is fair. Future work is open, and we will extend the model to larger fleets.
\end{document}
"""


class SentenceSplitTests(unittest.TestCase):
    def test_protects_abbreviations_and_initials(self) -> None:
        text = "Smith et al. reported it in Fig. 3, e.g. on the U.S. map. The next sentence starts here."
        self.assertEqual(len(F.split_sentences(text)), 2)

    def test_splits_after_acronym(self) -> None:
        self.assertEqual(len(F.split_sentences("The robots use MEC. The station charges them.")), 2)

    def test_inline_math_counts_in_sentence_length_not_in_words(self) -> None:
        cleaned = F.clean_tex(r"The load $x_i$ of zone $i$ is bounded by the capacity of the station.")
        self.assertEqual(F.sentence_length(cleaned), 14)
        self.assertEqual(len(F.words(cleaned)), 12)


class FingerprintTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.path = pathlib.Path(self.temp.name) / "draft.tex"
        self.path.write_text(TEX, encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_sections_are_classified(self) -> None:
        result = F.fingerprint(self.path)
        self.assertIn("intro", result)
        self.assertIn("exp", result)
        self.assertIn("abstract", result)
        self.assertIn("body", result)

    def test_banned_constructions_are_reported(self) -> None:
        banned = F.fingerprint(self.path)["exp"]["banned"]
        for name in ("because", "semicolon", ", but", "Hence", "we/our outside future work"):
            self.assertIn(name, banned, name)
        we_hits = banned["we/our outside future work"]
        self.assertFalse(any("we will extend" in sentence for sentence in we_hits))

    def test_short_run_is_flagged(self) -> None:
        exp = F.fingerprint(self.path)["exp"]
        self.assertTrue(exp["short_runs"], "three consecutive short sentences were not detected")

    def test_band_flags_cover_body_and_banned_words(self) -> None:
        flags = F.band_flags(F.fingerprint(self.path))
        self.assertTrue(any("because" in flag for flag in flags))
        self.assertTrue(any("run(s) of three or more" in flag for flag in flags))

    def test_citation_reuse_within_section(self) -> None:
        self.assertEqual(F.citation_reuse(self.path), {"intro": {"a": 2}})

    def test_markdown_citation_ranges_expand(self) -> None:
        path = pathlib.Path(self.temp.name) / "paper.md"
        path.write_text(
            "# I. INTRODUCTION\n\n" + LONG + " [3], [2, 5], [4-6].\n\n" + LONG + " [5].\n",
            encoding="utf-8",
        )
        self.assertEqual(F.citation_reuse(path), {"intro": {"5": 3}})

    def test_cli_json_runs(self) -> None:
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            self.assertEqual(F.main([str(self.path), "--json"]), 0)
        data = json.loads(buffer.getvalue())
        self.assertIn("flags", data)
        self.assertIn("body", data["sections"])


ZH_MD = """# 校园配送机器人的充电站协同规划

## I. 引言
校园配送机器人在大型园区中承担快递和餐食配送任务，其续航决定了单次出行能够覆盖的配送区域范围 [1]。现有研究通常在任务开始前固定充电站的位置，配送需求随时间变化时，机器人往返充电站的距离随之增加 [2]–[4]。据此，本文研究充电站随配送需求移动的协同规划问题，并给出相应的约束多目标进化算法。

## IV. 实验设计
机器人出发。机器人到达区域。机器人开始配送。充电站在每个规划周期开始时根据各区域的剩余需求重新选择停靠位置。本文比较四种算法；所有算法使用相同的种群规模。我们在三个实例上分别运行三十次，以评估各算法在不同规模下的可行率和超体积。
因此，本文首先在小规模实例上检查约束满足情况，再在大规模实例上比较各算法的平均超体积。因此，各算法的比较结果均按三十次独立运行取平均值后报告。其中最早就绪派遣规则作为基线：选择最早到达的候选机器人并立即派出，用于检验学习方法的必要性。
"""


class ChineseModeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.path = pathlib.Path(self.temp.name) / "draft.md"
        self.path.write_text(ZH_MD, encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_language_and_sections_are_detected(self) -> None:
        self.assertEqual(F.resolve_language(self.path), "zh")
        result = F.fingerprint(self.path)
        self.assertEqual(result["body"]["unit"], "chars")
        self.assertIn("intro", result)
        self.assertIn("exp", result)

    def test_sentence_length_counts_ideographs(self) -> None:
        self.assertEqual(F.sentence_length("本文比较四种 UAV 算法。", "zh"), 8)
        self.assertEqual(len(F.split_sentences("第一句结束。第二句结束！第三句？", "zh")), 3)

    def test_chinese_banned_constructions(self) -> None:
        result = F.fingerprint(self.path)
        intro, exp = result["intro"]["banned"], result["exp"]["banned"]
        self.assertIn("weak connective 可见/据此", intro)
        self.assertIn("full-width semicolon", exp)
        self.assertIn("我们 outside future work", exp)
        self.assertIn("colon inside a sentence", exp)

    def test_run_in_label_colon_is_allowed(self) -> None:
        self.assertFalse(F._zh_prose_colon("*最早就绪派遣*（Nearest-Ready）：选择最早到达的候选。"))
        self.assertFalse(F._zh_prose_colon("本文的主要贡献如下：（1）建立模型。"))
        self.assertTrue(F._zh_prose_colon("其中最早就绪派遣规则作为基线，用于对比：选择最早到达的候选。"))
        self.assertTrue(F._zh_prose_colon("本节综述三方面研究：电量约束、服务迁移和约束处理。"))

    def test_short_run_and_repeated_opener(self) -> None:
        exp = F.fingerprint(self.path)["exp"]
        self.assertTrue(exp["short_runs"])
        self.assertEqual(exp["repeated_openers"][0][0], "因此")

    def test_citation_range_across_brackets(self) -> None:
        self.assertEqual(F.citation_reuse(self.path), {})
        path = pathlib.Path(self.temp.name) / "ranges.md"
        path.write_text("# I. INTRODUCTION\n\n" + LONG + " [2]–[4].\n\n" + LONG + " [3].\n", encoding="utf-8")
        self.assertEqual(F.citation_reuse(path), {"intro": {"3": 2}})

    def test_flags_mark_the_band_as_a_weak_prior(self) -> None:
        flags = F.band_flags(F.fingerprint(self.path))
        band_flags = [flag for flag in flags if "band" in flag and "weak prior" in flag]
        self.assertTrue(band_flags)


ABBR_MAIN = r"""
\begin{document}
\begin{abstract}
Uncrewed aerial vehicles (UAVs) deliver parcels, and the PPO agent plans their routes for the robots in each zone.
\end{abstract}
\section{Introduction}
Campus delivery uses uncrewed aerial vehicles (UAVs) and ground robots in every zone of the site. A hybrid PPO
(H-PPO) method has been applied to such planning, and the routes are then refined with mixed-integer linear programming.
Later, proximal policy optimization (PPO) is adopted as the learner, and the PPO agent observes the queue of every
zone. The hypervolume (HV) metric is reported, and the channel state information (CSI) is assumed to be perfect.
The HV values are compared across all instances, and MILP solvers and MILP warm starts are used in Section S-IV.
Again, the hypervolume (HV) is defined for the reader of this paragraph.
\end{document}
"""

ABBR_SUPPLEMENT = r"""
\begin{document}
\section{Introduction}
This supplement studies the unmanned aerial vehicles (UAVs) of the main manuscript and the routes of every robot
in each zone of the campus, and the UAVs return to the station after every planning cycle of the mission.
\end{document}
"""


class AbbreviationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        root = pathlib.Path(self.temp.name)
        self.main = root / "main.tex"
        self.supplement = root / "supplement.tex"
        self.main.write_text(ABBR_MAIN, encoding="utf-8")
        self.supplement.write_text(ABBR_SUPPLEMENT, encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_long_form_detection(self) -> None:
        self.assertEqual(F._best_long_form("PPO", "is adopted with proximal policy optimization"), "proximal policy optimization")
        self.assertEqual(F._best_long_form("NLoS", "the non-line-of-sight"), "non line of sight")
        self.assertEqual(F._best_long_form("HV", "the hypervolume"), "hypervolume")

    def test_single_document_findings(self) -> None:
        report = F.abbreviation_report(self.main)
        self.assertIn("PPO", report["used_before_definition"])
        self.assertIn("HV", report["defined_more_than_once"])
        self.assertIn("CSI", report["rarely_used"])
        self.assertIn("PPO", report["abstract_undefined"])
        self.assertNotIn("UAV", report["abstract_undefined"])
        self.assertIn("MILP", report["never_defined"])
        self.assertNotIn("S-IV", report["never_defined"])

    def test_cross_document_long_forms(self) -> None:
        audit = F.abbreviation_audit([self.main, self.supplement])
        self.assertIn("UAV", audit["long_form_mismatches"])
        self.assertNotIn("HV", audit["long_form_mismatches"])

    def test_cli_accepts_several_files_only_with_abbrev(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(F.main(["--abbrev", str(self.main), str(self.supplement)]), 0)
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                F.main([str(self.main), str(self.supplement)])


class SectionRoleTests(unittest.TestCase):
    def test_method_section_named_after_the_algorithm(self) -> None:
        titles = ["Introduction", "Related Work", "System Model", "Problem Formulation",
                  "MAPPO-Based Joint Offloading for Delivery Robots", "Simulation Results", "Conclusion"]
        self.assertEqual(
            F.resolve_roles(titles),
            ["intro", "related", "model", "model", "method", "exp", "concl"],
        )

    def test_unclassified_section_between_model_and_experiments_is_method(self) -> None:
        titles = ["Introduction", "Related Work", "Temporal Sequence of Constraint Handling", "Experimental Setup", "Conclusion"]
        self.assertEqual(F.resolve_roles(titles)[2], "method")

    def test_sections_after_experiments_stay_unclassified(self) -> None:
        titles = ["Introduction", "System Model", "Numerical Results", "Discussion of Limits", "Conclusion"]
        self.assertEqual(F.resolve_roles(titles)[3], "other")

    def test_markdown_paper_title_is_not_a_method_section(self) -> None:
        text = (
            "# Station Planning for Robots: A Multi-Objective Optimization Approach\n\nAuthor list\n\n"
            "Abstract—" + LONG + "\n\n## I. INTRODUCTION\n\n" + LONG + "\n\n"
            "## IV. DEPENDENCY-AWARE GENERATION FOR STATION PLANNING\n\n" + LONG + "\n\n"
            "## III. SYSTEM MODEL\n\n" + LONG + "\n\n## V. EXPERIMENTAL STUDIES\n\n" + LONG + "\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "paper.md"
            path.write_text(text, encoding="utf-8")
            sections, _ = F.load(path)
        self.assertNotIn("Author list", " ".join(sections.get("method", [])))
        self.assertIn("intro", sections)
        self.assertIn("exp", sections)


class MultiFileTests(unittest.TestCase):
    def test_inputs_are_expanded_and_commented_inputs_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            (root / "sections").mkdir()
            (root / "main.tex").write_text(
                "\\begin{document}\n\\input{sections/intro}\n% \\input{sections/old}\n\\include{sections/exp.tex}\n"
                "\\input{sections/missing}\n\\end{document}\n",
                encoding="utf-8",
            )
            (root / "sections" / "intro.tex").write_text("\\section{Introduction}\n" + LONG + "\n", encoding="utf-8")
            (root / "sections" / "old.tex").write_text("\\section{Related Work}\n" + LONG + "\n", encoding="utf-8")
            (root / "sections" / "exp.tex").write_text(
                "\\section{Experimental Studies}\n\\input{sections/table-note}\n", encoding="utf-8"
            )
            (root / "sections" / "table-note.tex").write_text(LONG + "\n", encoding="utf-8")
            result = F.fingerprint(root / "main.tex")
            missing = F.MISSING_INCLUDES.get(str(root.resolve()), [])
        self.assertIn("intro", result)
        self.assertIn("exp", result)
        self.assertNotIn("related", result)
        self.assertIn("sections/missing", missing)

    def test_include_cycle_terminates(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            (root / "a.tex").write_text("\\begin{document}\\section{Introduction}" + LONG + "\\input{b}\\end{document}", encoding="utf-8")
            (root / "b.tex").write_text("\\input{a}", encoding="utf-8")
            self.assertIn("intro", F.fingerprint(root / "a.tex"))


class SpineTests(unittest.TestCase):
    def test_tex_spine_groups_openers_by_heading(self) -> None:
        tex = (
            "\\begin{document}\n\\section{Introduction}\n" + LONG + " Second sentence of the first paragraph.\n\n"
            + "However, " + LONG.lower() + "\n\n\\section{Experimental Studies}\n\\subsection{Overall Comparison}\n"
            + "As shown in Table~\\ref{tab:x}, " + LONG.lower() + "\n\\end{document}\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "draft.tex"
            path.write_text(tex, encoding="utf-8")
            entries = F.spine(path)
            only_exp = F.spine(path, section="exp")
        self.assertEqual([e["heading"] for e in entries], ["Introduction", "Overall Comparison"])
        self.assertEqual(len(entries[0]["openers"]), 2)
        self.assertTrue(entries[0]["openers"][1].startswith("However,"))
        self.assertNotIn("Second sentence", " ".join(entries[0]["openers"]))
        self.assertEqual(len(only_exp), 1)

    def test_markdown_spine_in_chinese(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "draft.md"
            path.write_text(ZH_MD, encoding="utf-8")
            entries = F.spine(path, section="intro")
        self.assertEqual(len(entries), 1)
        self.assertTrue(entries[0]["openers"][0].startswith("校园配送机器人"))


class ReportTests(unittest.TestCase):
    def test_report_covers_every_check(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            main = root / "main.tex"
            main.write_text(TEX, encoding="utf-8")
            letter = root / "reply.tex"
            letter.write_text(
                "\\begin{document}\nWe thank the reviewer. We have revised Section V; the table is updated because "
                "the rerun changed it, and we report the new values in every row of the table.\n\\end{document}\n",
                encoding="utf-8",
            )
            out = root / "report.md"
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(F.main(["--report", str(main), str(letter), "--out", str(out)]), 0)
            report = out.read_text(encoding="utf-8")
        for heading in ("## 1. Section scale", "## 2. Flags", "## 3. Banned constructions", "## 4. Over-splitting",
                        "## 5. Captions, subsection titles", "## 6. Paragraph-opening sentences",
                        "## 7. Citations repeated", "## 8. Abbreviations", "## 9. Further documents"):
            self.assertIn(heading, report)
        self.assertIn("because", report)
        self.assertIn("intro: a x2", report)
        letter_line = next(line for line in report.splitlines() if line.startswith("- **reply.tex**:"))
        self.assertIn("semicolon", letter_line)
        self.assertNotIn("we/our", letter_line)


SINCE = "Since the station moves with the demand, the controller assigns every robot to the nearest zone in each cycle."
HOWEVER = "However, the controller cannot observe the battery level of every robot before the planning cycle starts."
SHORT = "The robot waits at the hover point for the next task."


class ScopeAndMergeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def flags_for(self, name: str, text: str) -> tuple[str, list[str]]:
        path = self.root / name
        path.write_text(text, encoding="utf-8")
        result = F.fingerprint(path)
        return F.measurement_scope(result), F.band_flags(result)

    def test_comparison_and_shared_subject_pairs_are_merge_candidates(self) -> None:
        pairs = F.measure([
            "The mobile depot shortens the return trips. The static depot, in contrast, keeps them long. " + LONG
            + " The proposed algorithm converges within 300 generations. The proposed algorithm keeps every run feasible."
            + " The depot moves with the robots. Each robot reports its battery level."
        ])["merge_pairs"]
        self.assertEqual(len(pairs), 2)
        self.assertIn("in contrast", pairs[0][1])
        self.assertTrue(pairs[1][1].startswith("The proposed algorithm keeps"))
        zh = F.measure(["移动仓库缩短了机器人的返回路程。相比之下，静态仓库使返回路程保持较长。"], "zh")["merge_pairs"]
        self.assertEqual(len(zh), 1)

    def test_merge_candidates_reach_flags_and_report(self) -> None:
        text = "# I. Introduction\n\n" + LONG + " The mobile depot shortens the return trips. The static depot, in contrast, keeps them long. " + LONG + "\n"
        _scope, flags = self.flags_for("merge.md", text)
        self.assertTrue(any("could merge" in flag for flag in flags))
        report = F.submission_report([self.root / "merge.md"])
        self.assertIn("merge candidate", report)

    def test_paper_level_shares_are_not_flagged_on_one_section(self) -> None:
        paragraph = " ".join([SHORT] * 8)
        scope, flags = self.flags_for("one.md", "# I. Introduction\n\n" + paragraph + "\n")
        self.assertEqual(scope, "sections")
        self.assertFalse(any(flag.startswith("body ") for flag in flags), flags)
        self.assertTrue(any(flag.startswith("intro mean sentence length") for flag in flags))
        whole = "".join(f"# {title}\n\n{paragraph}\n\n" for title in ("I. Introduction", "II. Related Work", "V. Experimental Studies"))
        scope, flags = self.flags_for("whole.md", whole)
        self.assertEqual(scope, "paper")
        self.assertTrue(any(flag.startswith("body share_short") for flag in flags), flags)

    def test_connectives_are_counted_on_one_section(self) -> None:
        paragraph = " ".join([SINCE, LONG, SINCE, HOWEVER, LONG, HOWEVER, LONG, HOWEVER])
        _scope, flags = self.flags_for("conn.md", "# I. Introduction\n\n" + paragraph + "\n")
        self.assertTrue(any(flag.startswith("sentence-initial Since: 2 in 8 sentences") for flag in flags), flags)
        self.assertFalse(any("However" in flag for flag in flags), flags)

    def test_unclassified_text_lists_banned_constructions(self) -> None:
        scope, flags = self.flags_for("plain.txt", LONG + " The station moves because the demand changes over the day.\n")
        self.assertEqual(scope, "text")
        self.assertTrue(any(flag.startswith("body: 1 sentence(s) with because") for flag in flags), flags)


DOC_TEX = r"""
\begin{document}
\section{Introduction}
In this scenario, the controller assigns every robot to one delivery zone in each planning cycle of the day.
Existing planners can be categorized into two categories according to the depot model used in each cycle.
In this scenario, the controller also selects the depot position for the next planning cycle of the day.
The remainder of this study is organized as follows. Section~\ref{s2} presents the system model.
The model couples the robots, the zones, and the depot through the remaining battery level of each robot.
Section~\ref{s3} concludes this study.
\section{Experimental Studies}
\subsection{Comparison of the Proposed Algorithm with Five Existing Algorithms on Larger Instances}
""" + LONG + r"""
\begin{table}
\caption{Comparison Results of the Five Algorithms on HV}
\end{table}
\begin{table}
\caption{Comparison results of the five algorithms based on the mean and standard deviation (in parentheses) of HV and IGD over thirty independent runs on the three test instances.}
\end{table}
\begin{table}
\caption{Comparison results of the five algorithms based on HV. The best value is shown in bold. The test instances follow Section~\ref{s2}.}
\end{table}
\begin{algorithm}
\caption{Framework of the proposed algorithm}
\end{algorithm}
\end{document}
"""


class DocumentCheckTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.temp.name)
        self.path = self.root / "doc.tex"
        self.path.write_text(DOC_TEX, encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def audit(self, path: pathlib.Path | None = None, **options) -> tuple[dict, list[str]]:
        path = path or self.path
        audit = F.document_audit(path, F.fingerprint(path), **options)
        return audit, F.document_flags(audit)

    def test_captions_titles_roadmap_and_templates(self) -> None:
        audit, flags = self.audit()
        issues = [caption["issues"] for caption in audit["captions"]]
        self.assertEqual(len(issues), 4)
        self.assertIn("no final period", issues[0])
        self.assertIn("title case", issues[0])
        self.assertTrue(any("noun phrase of" in issue for issue in issues[1]))
        self.assertEqual(issues[2], [], "note sentences after a short noun phrase are allowed")
        self.assertEqual(issues[3], [], "algorithm captions take no final period")
        self.assertTrue(any(flag.startswith("subsection title of 12 words") for flag in flags), flags)
        self.assertTrue(any("'In this scenario' starts 2 sentences" in flag for flag in flags), flags)
        self.assertTrue(any("count noun" in flag for flag in flags), flags)
        self.assertTrue(any(flag.startswith("roadmap: 1 sentence(s) name no section") for flag in flags), flags)

    def test_markdown_captions_skip_reporting_sentences(self) -> None:
        path = self.root / "doc.md"
        path.write_text(
            "# V. Experimental Studies\n\n" + LONG + "\n\nTABLE II. Test instance configurations with varying problem scales.\n\n"
            "Table II lists the instances used in every experiment of this section.\n",
            encoding="utf-8",
        )
        audit, _flags = self.audit(path)
        self.assertEqual([c["text"] for c in audit["captions"]], ["Test instance configurations with varying problem scales."])

    def test_declared_scale(self) -> None:
        scale = F.parse_scale(["exp=5-10", "exp.paragraphs=1-2", "related=100-200"])
        _audit, flags = self.audit(scale=scale)
        self.assertTrue(any(flag.startswith("exp words = ") and "above the declared 5-10" in flag for flag in flags), flags)
        self.assertFalse(any(flag.startswith("exp paragraphs") for flag in flags), flags)
        self.assertTrue(any(flag.startswith("related words: section not found") for flag in flags), flags)
        with self.assertRaises(ValueError):
            F.parse_scale(["exp:900-1900"])

    def test_ledger_terms(self) -> None:
        ledger = self.root / "terms.txt"
        ledger.write_text("# ledger\ncase: test instance, instance\nrobot, vehicle\n", encoding="utf-8")
        terms = F.read_terms(ledger)
        self.assertEqual(terms, [("case", ["test instance", "instance"]), ("robot", ["vehicle"])])
        _audit, flags = self.audit(terms=terms)
        self.assertTrue(any(flag.startswith("term 'test instance' appears 2 times (captions 2)") for flag in flags), flags)
        self.assertFalse(any(flag.startswith("term 'instance'") for flag in flags), "a longer term must mask its parts")
        self.assertFalse(any("'vehicle'" in flag for flag in flags), flags)

    def test_cli_options_reach_the_output(self) -> None:
        ledger = self.root / "terms.txt"
        ledger.write_text("case: instance\n", encoding="utf-8")
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            self.assertEqual(F.main([str(self.path), "--scale", "exp=5-10", "--terms", str(ledger), "--json"]), 0)
        data = json.loads(buffer.getvalue())
        self.assertTrue(any("above the declared" in flag for flag in data["document_flags"]))
        self.assertTrue(data["document"]["captions"])


class CountingAndNoteTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write(self, name: str, text: str) -> pathlib.Path:
        path = self.root / name
        path.write_text(text, encoding="utf-8")
        return path

    def test_list_items_join_their_lead_in_except_contributions(self) -> None:
        path = self.write("lists.md", (
            "# I. Introduction\n\n" + LONG + " The main contributions of this study are summarized as follows:\n\n"
            "- " + LONG + "\n\n- " + LONG + "\n\n# V. Experimental Studies\n\n" + LONG + " The settings are listed below.\n\n"
            "- Population size 100.\n\n- Generations 300.\n"
        ))
        result = F.fingerprint(path)
        self.assertEqual(result["intro"]["paragraphs"], 3)
        self.assertEqual(result["exp"]["paragraphs"], 1)
        tex = self.write("lists.tex", (
            "\\begin{document}\n\\section{Experimental Studies}\n" + LONG + " The settings are listed below.\n"
            "\\begin{itemize}\n\\item Population size 100.\n\\item Generations 300.\n\\end{itemize}\n\\end{document}\n"
        ))
        self.assertEqual(F.fingerprint(tex)["exp"]["paragraphs"], 1)

    def test_text_after_a_display_joins_its_lead_in(self) -> None:
        path = self.write("where.md", (
            "# III. System Model\n\n" + LONG + " The delay is given by:\n\n$$d = a + b$$\n\n"
            "where a denotes the waiting time and b denotes the service time of the robot in the zone.\n"
        ))
        self.assertEqual(F.fingerprint(path)["model"]["paragraphs"], 1)

    def test_caption_lengths_and_algorithm_period(self) -> None:
        path = self.write("captions.tex", (
            "\\begin{document}\n\\section{Experimental Studies}\n" + LONG + "\n"
            "\\begin{table}\\caption{Comparison results of the five algorithms based on HV. The best value of every instance "
            "is shown in bold, the second best is underlined, and the symbols mark the results of the Wilcoxon rank-sum "
            "test at the 0.05 level over thirty runs.}\\end{table}\n"
            "\\begin{algorithm}\\caption{Framework of the proposed algorithm.}\\end{algorithm}\n\\end{document}\n"
        ))
        audit = F.document_audit(path, F.fingerprint(path))
        self.assertEqual(audit["captions"][0]["issues"], [])
        self.assertTrue(any("runs" in note and "words in total" in note for note in F.document_notes(audit)))
        self.assertEqual(audit["captions"][1]["issues"], ["final period on an algorithm caption"])
        caps = self.write("caps.md", (
            "# V. Experimental Studies\n\n" + LONG + "\n\nTABLE III COMPARISON RESULTS OF THE FIVE ALGORITHMS BASED ON THE "
            "MEAN AND STANDARD DEVIATION IN PARENTHESES OF HV AND IGD OVER THIRTY INDEPENDENT RUNS ON THREE INSTANCES\n"
        ))
        audit = F.document_audit(caps, F.fingerprint(caps))
        self.assertTrue(audit["captions"][0]["issues"][0].startswith("noun phrase of"))

    def test_notes_cover_unjudged_measures_tolerance_and_quota(self) -> None:
        since = "Since the station moves with the demand, the controller assigns every robot to the nearest zone again."
        path = self.write("notes.md", "# V. Experimental Studies\n\n" + " ".join([since] + [LONG] * 21) + "\n")
        notes = F.band_notes(F.fingerprint(path))
        self.assertTrue(any("not judged below a whole paper" in note for note in notes), notes)
        self.assertTrue(any("0% of sentences under 12" in note for note in notes), notes)
        self.assertTrue(any("reaches the single-section limit" in note for note in notes), notes)

    def test_opener_templates_count_per_verb_and_need_an_introduction(self) -> None:
        considers = "To address this limitation, this study considers a mobile depot that follows the delivery demand."
        proposes = "To address this challenge, this study proposes an algorithm that relocates the depot in each cycle."
        path = self.write("open.md", "# I. Introduction\n\n" + " ".join([LONG, considers, proposes]) + "\n")
        audit = F.document_audit(path, F.fingerprint(path))
        self.assertFalse(any("opener template" in flag for flag in F.document_flags(audit)))
        path = self.write("open2.md", "# I. Introduction\n\n" + " ".join([LONG, considers, considers]) + "\n")
        audit = F.document_audit(path, F.fingerprint(path))
        self.assertTrue(any("this study considers' starts 2" in flag for flag in F.document_flags(audit)))
        path = self.write("related.md", "# II. Related Work\n\n" + " ".join([LONG, considers, considers]) + "\n")
        audit = F.document_audit(path, F.fingerprint(path))
        self.assertIsNone(audit["templates"])
        self.assertIn("opener templates not checked: no Introduction", F.document_notes(audit))

    def test_terms_skip_definitions_cover_the_abstract_and_give_sentences(self) -> None:
        path = self.write("terms.md", (
            "Abstract—Internet of Things devices (IoTDs) offload tasks, and every Internet of Things device pays a charge.\n\n"
            "# I. Introduction\n\n" + LONG + " Each IoTD offloads its task to a nearby server in every slot of the day.\n"
        ))
        ledger = self.write("terms.txt", "IoTD: Internet of Things device\n")
        audit = F.document_audit(path, F.fingerprint(path), terms=F.read_terms(ledger))
        row = audit["terms"][0]
        self.assertEqual(row["counts"]["Internet of Things device"], {"abstract": 1})
        self.assertIn("every Internet of Things device", row["examples"]["Internet of Things device"][0])
        self.assertTrue(F.term_flags(audit["terms"])[0].startswith("term 'Internet of Things device' appears 1 times"))

    def test_scale_measures_and_headingless_text(self) -> None:
        path = self.write("scale.md", "# V. Experimental Studies\n\n" + " ".join([LONG] * 3) + "\n\n" + LONG + "\n")
        scale = F.parse_scale(["exp.sentences=1-2", "exp.first_paragraph_words=1-5", "exp.last_paragraph_words=20-40"])
        flags = F.document_flags(F.document_audit(path, F.fingerprint(path), scale=scale))
        self.assertTrue(any(flag.startswith("exp sentences = 4") for flag in flags), flags)
        self.assertTrue(any(flag.startswith("exp first paragraph words") for flag in flags), flags)
        self.assertFalse(any(flag.startswith("exp last paragraph words") for flag in flags), flags)
        plain = self.write("plain.txt", LONG + " " + LONG + "\n")
        audit = F.document_audit(plain, F.fingerprint(plain), scale=F.parse_scale(["intro=1-5"]))
        self.assertTrue(any(flag.startswith("intro words = ") for flag in F.document_flags(audit)))
        self.assertTrue(any("measured on the whole text" in note for note in F.document_notes(audit)))

    def test_citations_ignore_inline_intervals(self) -> None:
        path = self.write("cite.md", "# I. Introduction\n\n" + LONG + " The weight lies in $[0,1]$ and again in $[0,1]$ [3].\n")
        self.assertEqual(F.citation_reuse(path), {})

    def test_subsection_label_ends_a_sentence_and_e_notation_is_one_token(self) -> None:
        self.assertEqual(len(F.split_sentences("The settings follow Section V-A. The results are reported next.")), 2)
        self.assertEqual(F.sentence_length("The HV is 5.83e+04 on the first instance."), 7)


class DiffTests(unittest.TestCase):
    def test_merge_and_split_are_classified(self) -> None:
        old = "The robots return to a distant station. This increases their travel distance. " + LONG
        new = (
            "The robots return to a distant station, increasing their travel distance. " + LONG
            + " The station then waits for the slowest robot. Each robot reports its battery level."
        )
        with tempfile.TemporaryDirectory() as directory:
            old_path = pathlib.Path(directory) / "old.txt"
            new_path = pathlib.Path(directory) / "new.txt"
            old_path.write_text(old, encoding="utf-8")
            new_path.write_text(new, encoding="utf-8")
            report = F.diff_report(old_path, new_path)
        self.assertEqual(report["kinds"].get("merge"), 1)
        self.assertEqual(report["kinds"].get("insert"), 1)
        self.assertGreater(report["changed_mean_new"], report["changed_mean_old"])


class BandDocumentationTests(unittest.TestCase):
    def test_script_band_matches_house_style_tables(self) -> None:
        text = STYLE.read_text(encoding="utf-8")
        for (low, high) in F.TEAM_BAND["section_mean"].values():
            self.assertIn(f"{low:.1f}–{high:.1f}", text)
        body = F.TEAM_BAND["body"]
        self.assertIn(f"{body['mean'][0]:.1f}–{body['mean'][1]:.1f}", text)
        self.assertIn(f"{body['median'][0]:.0f}–{body['median'][1]:.0f}", text)
        self.assertIn(f"{body['p90'][0]:.0f}–{body['p90'][1]:.0f}", text)
        for key in ("share_long", "share_short"):
            low, high = body[key]
            self.assertIn(f"{round(low * 100)}%–{round(high * 100)}%", text)
        for key in ("abstract_words", "conclusion_words"):
            low, high = F.TEAM_BAND[key]
            self.assertIn(f"{low}–{high} words", text)
        for key in ("abstract_sentences", "conclusion_sentences"):
            low, high = F.TEAM_BAND[key]
            self.assertIn(f"{low}–{high} sentences", text)

    def test_chinese_band_matches_adapter_table(self) -> None:
        text = ZH.read_text(encoding="utf-8")
        band = F.TEAM_BAND_ZH
        for key in ("mean", "median", "p90"):
            low, high = band["body"][key]
            self.assertIn(f"{low}–{high}", text, key)
        for (low, high) in band["section_mean"].values():
            self.assertIn(f"{low}–{high}", text)
        for key in ("abstract_words", "conclusion_words"):
            low, high = band[key]
            self.assertIn(f"{low}–{high} ideographs", text, key)
        self.assertIn(f"under {F.LANGUAGES['zh']['short']} ideographs", text)
        self.assertIn(f"over {F.LANGUAGES['zh']['long']} ideographs", text)
        self.assertIn(f"{F.ZH_RATIO[0]} to {F.ZH_RATIO[1]}", text)

    def test_style_gate_ids_are_well_formed(self) -> None:
        ids = re.findall(r"\[(G-STY-[a-z]+)\]", STYLE.read_text(encoding="utf-8"))
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(ids), 10)


if __name__ == "__main__":
    unittest.main()
