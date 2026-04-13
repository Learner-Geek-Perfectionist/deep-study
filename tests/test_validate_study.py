import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "validate-study.py"


# ---------------------------------------------------------------------------
# Per-type definitions mirroring the validator
# ---------------------------------------------------------------------------

COMMON_FILES = [
    "00-scope-and-plan.md",
    "01-landscape.md",
    "02-architecture.md",
    "07-end-to-end-trace.md",
    "08-failure-and-edge-cases.md",
    "09-synthesis.md",
    "README.md",
]

TYPE_SPECIFIC_FILES = {
    "source": [
        "03-core-data-structures.md",
        "04-core-functions.md",
        "05-mechanisms.md",
        "06-control-flow-and-state.md",
    ],
    "protocol": [
        "03-message-formats.md",
        "04-state-machines.md",
        "05-exchange-sequences.md",
        "06-reliability-and-timing.md",
    ],
    "language": [
        "03-representations.md",
        "04-pipeline-stages.md",
        "05-evaluation-rules.md",
        "06-runtime-mechanics.md",
    ],
}

COMMON_HEADINGS = {
    "00-scope-and-plan.md": [
        "## \u7814\u7a76\u8303\u56f4",
        "## \u4e3b\u9898\u5206\u7c7b",
        "## \u6838\u5fc3\u95ee\u9898",
        "## \u6750\u6599\u6e05\u5355",
        "## \u8f93\u51fa\u8ba1\u5212",
    ],
    "01-landscape.md": [
        "## \u4e3b\u9898\u6982\u51b5",
        "## \u6750\u6599\u5730\u56fe",
        "## \u5165\u53e3\u4e0e\u5173\u952e\u6587\u4ef6",
        "## \u6838\u5fc3\u6982\u5ff5",
        "## \u521d\u59cb\u95ee\u9898\u6e05\u5355",
    ],
    "02-architecture.md": [
        "## \u6838\u5fc3\u62bd\u8c61",
        "## \u7ec4\u4ef6\u5173\u7cfb",
        "## \u4e3b\u8981\u6570\u636e\u6d41",
        "## \u5206\u5c42\u4e0e\u8fb9\u754c",
        "## \u63a5\u53e3\u5951\u7ea6",
    ],
    "07-end-to-end-trace.md": [
        "## \u573a\u666f\u5b9a\u4e49",
        "## \u5165\u53e3\u6761\u4ef6",
        "## \u6267\u884c\u6b65\u9aa4",
        "## \u72b6\u6001\u53d8\u5316",
        "## \u573a\u666f\u7ed3\u8bba",
    ],
    "08-failure-and-edge-cases.md": [
        "## \u5f02\u5e38\u8def\u5f84\u6e05\u5355",
        "## \u8fb9\u754c\u6761\u4ef6",
        "## \u8d44\u6e90\u91ca\u653e\u4e0e\u6e05\u7406",
        "## \u6613\u9519\u70b9",
    ],
    "09-synthesis.md": [
        "## \u8bbe\u8ba1\u54f2\u5b66",
        "## \u5173\u952e Trade-off",
        "## \u53cd\u590d\u51fa\u73b0\u7684\u6a21\u5f0f",
        "## \u6838\u5fc3\u7ed3\u8bba",
    ],
}

TYPE_SPECIFIC_HEADINGS = {
    "source": {
        "03-core-data-structures.md": [
            "## \u6570\u636e\u7ed3\u6784\u6e05\u5355",
            "## \u5b57\u6bb5\u4e0e\u804c\u8d23",
            "## \u4e0d\u53d8\u91cf",
            "## \u6240\u6709\u6743\u4e0e\u751f\u547d\u5468\u671f\u5173\u7cfb",
            "## \u7ed3\u6784\u4e4b\u95f4\u7684\u4f9d\u8d56\u5173\u7cfb",
        ],
        "04-core-functions.md": [
            "## \u5173\u952e\u51fd\u6570\u6e05\u5355",
            "## \u51fd\u6570\u804c\u8d23\u4e0e\u8f93\u5165\u8f93\u51fa",
            "## \u5173\u952e\u72b6\u6001\u53d8\u5316",
            "## \u8c03\u7528\u5173\u7cfb",
            "## \u5f02\u5e38\u8def\u5f84\u4e0e\u5931\u8d25\u5904\u7406",
        ],
        "05-mechanisms.md": [
            "## \u673a\u5236\u5217\u8868",
            "## \u673a\u5236\u4e00",
            "## \u673a\u5236\u4e8c",
            "## \u673a\u5236\u4e4b\u95f4\u5982\u4f55\u534f\u4f5c",
            "## \u8bbe\u8ba1\u7ea6\u675f\u4e0e Trade-off",
        ],
        "06-control-flow-and-state.md": [
            "## \u4e3b\u63a7\u5236\u6d41",
            "## \u5173\u952e\u72b6\u6001\u8f6c\u6362",
            "## \u5e76\u53d1\u4e0e\u540c\u6b65\u70b9",
            "## \u8de8\u6a21\u5757\u63a7\u5236\u4ea4\u63a5",
        ],
    },
    "protocol": {
        "03-message-formats.md": [
            "## \u6d88\u606f\u683c\u5f0f\u6e05\u5355",
            "## \u5b57\u6bb5\u8bed\u4e49\u4e0e\u7f16\u7801\u89c4\u5219",
            "## \u5c42\u6b21\u7ed3\u6784\u4e0e\u6269\u5c55\u6027",
            "## \u517c\u5bb9\u7ea6\u675f",
            "## \u683c\u5f0f\u4e4b\u95f4\u7684\u5173\u7cfb",
        ],
        "04-state-machines.md": [
            "## \u72b6\u6001\u6e05\u5355",
            "## \u8f6c\u6362\u6761\u4ef6\u4e0e\u89e6\u53d1\u4e8b\u4ef6",
            "## \u8f6c\u6362\u526f\u4f5c\u7528",
            "## \u72b6\u6001\u5206\u7c7b",
            "## \u72b6\u6001\u673a\u4e4b\u95f4\u7684\u534f\u4f5c",
        ],
        "05-exchange-sequences.md": [
            "## \u4ea4\u4e92\u6d41\u7a0b\u5217\u8868",
            "## \u6d41\u7a0b\u4e00",
            "## \u6d41\u7a0b\u4e8c",
            "## \u6d41\u7a0b\u4e4b\u95f4\u5982\u4f55\u8854\u63a5",
            "## \u8bbe\u8ba1\u7ea6\u675f\u4e0e Trade-off",
        ],
        "06-reliability-and-timing.md": [
            "## \u53ef\u9760\u6027\u673a\u5236",
            "## \u8d85\u65f6\u4e0e\u91cd\u4f20\u7b56\u7565",
            "## \u6d41\u63a7\u4e0e\u62e5\u585e\u63a7\u5236",
            "## \u65f6\u5e8f\u7ea6\u675f",
        ],
    },
    "language": {
        "03-representations.md": [
            "## \u8868\u793a\u6e05\u5355",
            "## \u8282\u70b9\u7ed3\u6784\u4e0e\u5b57\u6bb5\u8bed\u4e49",
            "## \u9636\u6bb5\u5f52\u5c5e",
            "## \u4e0d\u53d8\u91cf\u4e0e\u7ea6\u675f",
            "## \u8868\u793a\u4e4b\u95f4\u7684\u8f6c\u6362\u5173\u7cfb",
        ],
        "04-pipeline-stages.md": [
            "## \u7ba1\u7ebf\u9636\u6bb5\u6e05\u5355",
            "## \u9636\u6bb5\u8f93\u5165\u4e0e\u8f93\u51fa",
            "## \u9636\u6bb5\u5185\u5173\u952e\u64cd\u4f5c",
            "## \u9636\u6bb5\u95f4\u4fe1\u606f\u4f20\u9012",
            "## \u9519\u8bef\u68c0\u6d4b\u4e0e\u8bca\u65ad\u70b9",
        ],
        "05-evaluation-rules.md": [
            "## \u89c4\u5219\u5217\u8868",
            "## \u89c4\u5219\u4e00",
            "## \u89c4\u5219\u4e8c",
            "## \u89c4\u5219\u4e4b\u95f4\u5982\u4f55\u534f\u4f5c",
            "## \u8bbe\u8ba1\u7ea6\u675f\u4e0e Trade-off",
        ],
        "06-runtime-mechanics.md": [
            "## \u8fd0\u884c\u65f6\u673a\u5236",
            "## \u5185\u5b58\u7ba1\u7406",
            "## \u8c03\u5ea6\u4e0e\u6267\u884c\u6a21\u578b",
            "## \u5916\u90e8\u63a5\u53e3\u4e0e FFI",
        ],
    },
}

TYPE_SPECIFIC_ENTRY_RULES = {
    "source": {
        "03-core-data-structures.md": ("### \u7ed3\u6784\uff1a", 5),
        "04-core-functions.md": ("### \u51fd\u6570\uff1a", 8),
        "05-mechanisms.md": ("### \u673a\u5236\uff1a", 3),
    },
    "protocol": {
        "03-message-formats.md": ("### \u683c\u5f0f\uff1a", 5),
        "04-state-machines.md": ("### \u72b6\u6001\uff1a", 5),
        "05-exchange-sequences.md": ("### \u6d41\u7a0b\uff1a", 3),
    },
    "language": {
        "03-representations.md": ("### \u8868\u793a\uff1a", 5),
        "04-pipeline-stages.md": ("### \u9636\u6bb5\uff1a", 4),
        "05-evaluation-rules.md": ("### \u89c4\u5219\uff1a", 3),
    },
}

COMMON_ENTRY_RULES = {
    "07-end-to-end-trace.md": ("### \u573a\u666f\uff1a", 1),
    "08-failure-and-edge-cases.md": ("### \u6761\u76ee\uff1a", 4),
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_validator_module():
    spec = importlib.util.spec_from_file_location("validate_study", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def get_all_files(study_type):
    return COMMON_FILES + TYPE_SPECIFIC_FILES[study_type]


def get_all_headings(study_type):
    headings = dict(COMMON_HEADINGS)
    headings.update(TYPE_SPECIFIC_HEADINGS[study_type])
    return headings


def get_all_entry_rules(study_type):
    rules = dict(COMMON_ENTRY_RULES)
    rules.update(TYPE_SPECIFIC_ENTRY_RULES[study_type])
    return rules


def write_markdown(path, headings, mermaid=True, entry_prefix=None, entry_count=0):
    lines = ["# Title", ""]
    for heading in headings:
        lines.extend([heading, "", "content", ""])
    for i in range(entry_count):
        lines.extend([f"{entry_prefix}{i + 1}", "", "details", ""])
    if mermaid:
        lines.extend(["```mermaid", "flowchart TD", "A-->B", "```", ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def make_valid_study(root, study_type):
    all_files = get_all_files(study_type)
    all_headings = get_all_headings(study_type)
    all_entry_rules = get_all_entry_rules(study_type)

    for name in all_files:
        path = root / name
        headings = all_headings.get(name, [])
        entry_prefix = None
        entry_count = 0
        if name in all_entry_rules:
            entry_prefix, entry_count = all_entry_rules[name]
        if name == "README.md":
            links = [f"- [{target}](./{target})" for target in all_files if target != "README.md"]
            path.write_text("# README\n\n" + "\n".join(links) + "\n", encoding="utf-8")
        else:
            write_markdown(path, headings, mermaid=True, entry_prefix=entry_prefix, entry_count=entry_count)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class ValidateSourceTests(unittest.TestCase):
    def test_valid_source_study_passes(self):
        module = load_validator_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            study_dir = Path(tmpdir)
            make_valid_study(study_dir, "source")
            errors = module.validate_study(study_dir)
            self.assertEqual(errors, [])

    def test_missing_required_file_fails(self):
        module = load_validator_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            study_dir = Path(tmpdir)
            make_valid_study(study_dir, "source")
            (study_dir / "04-core-functions.md").unlink()
            errors = module.validate_study(study_dir)
            self.assertTrue(any("04-core-functions.md" in e for e in errors))

    def test_missing_heading_fails(self):
        module = load_validator_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            study_dir = Path(tmpdir)
            make_valid_study(study_dir, "source")
            target = study_dir / "03-core-data-structures.md"
            target.write_text(
                target.read_text(encoding="utf-8").replace("## \u4e0d\u53d8\u91cf", "## \u5b57\u6bb5\u5217\u8868"),
                encoding="utf-8",
            )
            errors = module.validate_study(study_dir)
            self.assertTrue(any("## \u4e0d\u53d8\u91cf" in e for e in errors))

    def test_missing_entry_count_fails(self):
        module = load_validator_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            study_dir = Path(tmpdir)
            make_valid_study(study_dir, "source")
            all_headings = get_all_headings("source")
            write_markdown(
                study_dir / "04-core-functions.md",
                all_headings["04-core-functions.md"],
                mermaid=True,
                entry_prefix="### \u51fd\u6570\uff1a",
                entry_count=3,
            )
            errors = module.validate_study(study_dir)
            self.assertTrue(any("\u81f3\u5c11\u5305\u542b 8 \u4e2a" in e for e in errors))

    def test_missing_mermaid_fails(self):
        module = load_validator_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            study_dir = Path(tmpdir)
            make_valid_study(study_dir, "source")
            all_headings = get_all_headings("source")
            write_markdown(
                study_dir / "02-architecture.md",
                all_headings["02-architecture.md"],
                mermaid=False,
            )
            errors = module.validate_study(study_dir)
            self.assertTrue(any("02-architecture.md" in e and "Mermaid" in e for e in errors))

    def test_readme_missing_link_fails(self):
        module = load_validator_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            study_dir = Path(tmpdir)
            make_valid_study(study_dir, "source")
            (study_dir / "README.md").write_text("# README\n", encoding="utf-8")
            errors = module.validate_study(study_dir)
            self.assertTrue(any("README.md" in e for e in errors))


class ValidateProtocolTests(unittest.TestCase):
    def test_valid_protocol_study_passes(self):
        module = load_validator_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            study_dir = Path(tmpdir)
            make_valid_study(study_dir, "protocol")
            errors = module.validate_study(study_dir)
            self.assertEqual(errors, [])

    def test_missing_message_formats_fails(self):
        module = load_validator_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            study_dir = Path(tmpdir)
            make_valid_study(study_dir, "protocol")
            (study_dir / "03-message-formats.md").unlink()
            errors = module.validate_study(study_dir, study_type="protocol")
            self.assertTrue(any("03-message-formats.md" in e for e in errors))

    def test_missing_protocol_heading_fails(self):
        module = load_validator_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            study_dir = Path(tmpdir)
            make_valid_study(study_dir, "protocol")
            target = study_dir / "04-state-machines.md"
            target.write_text(
                target.read_text(encoding="utf-8").replace("## \u72b6\u6001\u6e05\u5355", "## \u5176\u4ed6\u6807\u9898"),
                encoding="utf-8",
            )
            errors = module.validate_study(study_dir)
            self.assertTrue(any("## \u72b6\u6001\u6e05\u5355" in e for e in errors))

    def test_missing_format_entry_count_fails(self):
        module = load_validator_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            study_dir = Path(tmpdir)
            make_valid_study(study_dir, "protocol")
            all_headings = get_all_headings("protocol")
            write_markdown(
                study_dir / "03-message-formats.md",
                all_headings["03-message-formats.md"],
                mermaid=True,
                entry_prefix="### \u683c\u5f0f\uff1a",
                entry_count=2,
            )
            errors = module.validate_study(study_dir)
            self.assertTrue(any("\u81f3\u5c11\u5305\u542b 5 \u4e2a" in e for e in errors))


class ValidateLanguageTests(unittest.TestCase):
    def test_valid_language_study_passes(self):
        module = load_validator_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            study_dir = Path(tmpdir)
            make_valid_study(study_dir, "language")
            errors = module.validate_study(study_dir)
            self.assertEqual(errors, [])

    def test_missing_representations_fails(self):
        module = load_validator_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            study_dir = Path(tmpdir)
            make_valid_study(study_dir, "language")
            (study_dir / "03-representations.md").unlink()
            errors = module.validate_study(study_dir, study_type="language")
            self.assertTrue(any("03-representations.md" in e for e in errors))

    def test_missing_language_heading_fails(self):
        module = load_validator_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            study_dir = Path(tmpdir)
            make_valid_study(study_dir, "language")
            target = study_dir / "04-pipeline-stages.md"
            target.write_text(
                target.read_text(encoding="utf-8").replace("## \u7ba1\u7ebf\u9636\u6bb5\u6e05\u5355", "## \u5176\u4ed6\u6807\u9898"),
                encoding="utf-8",
            )
            errors = module.validate_study(study_dir)
            self.assertTrue(any("## \u7ba1\u7ebf\u9636\u6bb5\u6e05\u5355" in e for e in errors))

    def test_missing_stage_entry_count_fails(self):
        module = load_validator_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            study_dir = Path(tmpdir)
            make_valid_study(study_dir, "language")
            all_headings = get_all_headings("language")
            write_markdown(
                study_dir / "04-pipeline-stages.md",
                all_headings["04-pipeline-stages.md"],
                mermaid=True,
                entry_prefix="### \u9636\u6bb5\uff1a",
                entry_count=1,
            )
            errors = module.validate_study(study_dir)
            self.assertTrue(any("\u81f3\u5c11\u5305\u542b 4 \u4e2a" in e for e in errors))


class AutoDetectTests(unittest.TestCase):
    def test_auto_detect_source(self):
        module = load_validator_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            study_dir = Path(tmpdir)
            make_valid_study(study_dir, "source")
            detected = module.detect_study_type(study_dir)
            self.assertEqual(detected, "source")

    def test_auto_detect_protocol(self):
        module = load_validator_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            study_dir = Path(tmpdir)
            make_valid_study(study_dir, "protocol")
            detected = module.detect_study_type(study_dir)
            self.assertEqual(detected, "protocol")

    def test_auto_detect_language(self):
        module = load_validator_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            study_dir = Path(tmpdir)
            make_valid_study(study_dir, "language")
            detected = module.detect_study_type(study_dir)
            self.assertEqual(detected, "language")

    def test_undetectable_type_fails(self):
        module = load_validator_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            study_dir = Path(tmpdir)
            (study_dir / "00-scope-and-plan.md").write_text("# Test", encoding="utf-8")
            errors = module.validate_study(study_dir)
            self.assertTrue(any("Cannot detect study type" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
