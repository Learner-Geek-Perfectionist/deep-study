#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Per-type complete definitions
# ---------------------------------------------------------------------------

REQUIRED_FILES = {
    "source": [
        "00-overview.md",
        "01-core-data-structures.md",
        "02-core-functions.md",
        "03-mechanisms.md",
        "04-control-flow-and-state.md",
        "05-end-to-end-trace.md",
        "06-failure-and-edge-cases.md",
        "07-synthesis.md",
        "README.md",
    ],
    "protocol": [
        "00-scope-and-plan.md",
        "01-landscape.md",
        "02-architecture.md",
        "03-message-formats.md",
        "04-state-machines.md",
        "05-exchange-sequences.md",
        "06-reliability-and-timing.md",
        "07-end-to-end-trace.md",
        "08-failure-and-edge-cases.md",
        "09-synthesis.md",
        "README.md",
    ],
    "language": [
        "00-scope-and-plan.md",
        "01-landscape.md",
        "02-architecture.md",
        "03-representations.md",
        "04-pipeline-stages.md",
        "05-evaluation-rules.md",
        "06-runtime-mechanics.md",
        "07-end-to-end-trace.md",
        "08-failure-and-edge-cases.md",
        "09-synthesis.md",
        "README.md",
    ],
}

# Signature file used to auto-detect study type
TYPE_SIGNATURES = {
    "source": "00-overview.md",
    "protocol": "03-message-formats.md",
    "language": "03-representations.md",
}

REQUIRED_HEADINGS = {
    "source": {
        "00-overview.md": [
            "## \u7814\u7a76\u8303\u56f4\u4e0e\u6838\u5fc3\u95ee\u9898",
            "## \u5165\u53e3\u4e0e\u6750\u6599\u5730\u56fe",
            "## \u6838\u5fc3\u6982\u5ff5",
            "## \u7ec4\u4ef6\u5173\u7cfb\u4e0e\u5206\u5c42",
            "## \u4e3b\u8981\u6570\u636e\u6d41",
        ],
        "01-core-data-structures.md": [
            "## \u6570\u636e\u7ed3\u6784\u6e05\u5355",
            "## \u5b57\u6bb5\u4e0e\u804c\u8d23",
            "## \u4e0d\u53d8\u91cf",
            "## \u6240\u6709\u6743\u4e0e\u751f\u547d\u5468\u671f\u5173\u7cfb",
            "## \u7ed3\u6784\u4e4b\u95f4\u7684\u4f9d\u8d56\u5173\u7cfb",
        ],
        "02-core-functions.md": [
            "## \u5173\u952e\u51fd\u6570\u6e05\u5355",
            "## \u51fd\u6570\u804c\u8d23\u4e0e\u8f93\u5165\u8f93\u51fa",
            "## \u5173\u952e\u72b6\u6001\u53d8\u5316",
            "## \u8c03\u7528\u5173\u7cfb",
            "## \u5f02\u5e38\u8def\u5f84\u4e0e\u5931\u8d25\u5904\u7406",
        ],
        "03-mechanisms.md": [
            "## \u673a\u5236\u5217\u8868",
            "## \u673a\u5236\u4e00",
            "## \u673a\u5236\u4e8c",
            "## \u673a\u5236\u4e4b\u95f4\u5982\u4f55\u534f\u4f5c",
            "## \u8bbe\u8ba1\u7ea6\u675f\u4e0e Trade-off",
        ],
        "04-control-flow-and-state.md": [
            "## \u4e3b\u63a7\u5236\u6d41",
            "## \u5173\u952e\u72b6\u6001\u8f6c\u6362",
            "## \u5e76\u53d1\u4e0e\u540c\u6b65\u70b9",
            "## \u8de8\u6a21\u5757\u63a7\u5236\u4ea4\u63a5",
        ],
        "05-end-to-end-trace.md": [
            "## \u573a\u666f\u5b9a\u4e49",
            "## \u5165\u53e3\u6761\u4ef6",
            "## \u6267\u884c\u6b65\u9aa4",
            "## \u72b6\u6001\u53d8\u5316",
            "## \u573a\u666f\u7ed3\u8bba",
        ],
        "06-failure-and-edge-cases.md": [
            "## \u5f02\u5e38\u8def\u5f84\u6e05\u5355",
            "## \u8fb9\u754c\u6761\u4ef6",
            "## \u8d44\u6e90\u91ca\u653e\u4e0e\u6e05\u7406",
            "## \u6613\u9519\u70b9",
        ],
        "07-synthesis.md": [
            "## \u8bbe\u8ba1\u54f2\u5b66",
            "## \u5173\u952e Trade-off",
            "## \u53cd\u590d\u51fa\u73b0\u7684\u6a21\u5f0f",
            "## \u6838\u5fc3\u7ed3\u8bba",
        ],
    },
    "protocol": {
        "00-scope-and-plan.md": ["## \u7814\u7a76\u8303\u56f4", "## \u4e3b\u9898\u5206\u7c7b", "## \u6838\u5fc3\u95ee\u9898", "## \u6750\u6599\u6e05\u5355", "## \u8f93\u51fa\u8ba1\u5212"],
        "01-landscape.md": ["## \u4e3b\u9898\u6982\u51b5", "## \u6750\u6599\u5730\u56fe", "## \u5165\u53e3\u4e0e\u5173\u952e\u6587\u4ef6", "## \u6838\u5fc3\u6982\u5ff5", "## \u521d\u59cb\u95ee\u9898\u6e05\u5355"],
        "02-architecture.md": ["## \u6838\u5fc3\u62bd\u8c61", "## \u7ec4\u4ef6\u5173\u7cfb", "## \u4e3b\u8981\u6570\u636e\u6d41", "## \u5206\u5c42\u4e0e\u8fb9\u754c", "## \u63a5\u53e3\u5951\u7ea6"],
        "03-message-formats.md": ["## \u6d88\u606f\u683c\u5f0f\u6e05\u5355", "## \u5b57\u6bb5\u8bed\u4e49\u4e0e\u7f16\u7801\u89c4\u5219", "## \u5c42\u6b21\u7ed3\u6784\u4e0e\u6269\u5c55\u6027", "## \u517c\u5bb9\u7ea6\u675f", "## \u683c\u5f0f\u4e4b\u95f4\u7684\u5173\u7cfb"],
        "04-state-machines.md": ["## \u72b6\u6001\u6e05\u5355", "## \u8f6c\u6362\u6761\u4ef6\u4e0e\u89e6\u53d1\u4e8b\u4ef6", "## \u8f6c\u6362\u526f\u4f5c\u7528", "## \u72b6\u6001\u5206\u7c7b", "## \u72b6\u6001\u673a\u4e4b\u95f4\u7684\u534f\u4f5c"],
        "05-exchange-sequences.md": ["## \u4ea4\u4e92\u6d41\u7a0b\u5217\u8868", "## \u6d41\u7a0b\u4e00", "## \u6d41\u7a0b\u4e8c", "## \u6d41\u7a0b\u4e4b\u95f4\u5982\u4f55\u8854\u63a5", "## \u8bbe\u8ba1\u7ea6\u675f\u4e0e Trade-off"],
        "06-reliability-and-timing.md": ["## \u53ef\u9760\u6027\u673a\u5236", "## \u8d85\u65f6\u4e0e\u91cd\u4f20\u7b56\u7565", "## \u6d41\u63a7\u4e0e\u62e5\u585e\u63a7\u5236", "## \u65f6\u5e8f\u7ea6\u675f"],
        "07-end-to-end-trace.md": ["## \u573a\u666f\u5b9a\u4e49", "## \u5165\u53e3\u6761\u4ef6", "## \u6267\u884c\u6b65\u9aa4", "## \u72b6\u6001\u53d8\u5316", "## \u573a\u666f\u7ed3\u8bba"],
        "08-failure-and-edge-cases.md": ["## \u5f02\u5e38\u8def\u5f84\u6e05\u5355", "## \u8fb9\u754c\u6761\u4ef6", "## \u8d44\u6e90\u91ca\u653e\u4e0e\u6e05\u7406", "## \u6613\u9519\u70b9"],
        "09-synthesis.md": ["## \u8bbe\u8ba1\u54f2\u5b66", "## \u5173\u952e Trade-off", "## \u53cd\u590d\u51fa\u73b0\u7684\u6a21\u5f0f", "## \u6838\u5fc3\u7ed3\u8bba"],
    },
    "language": {
        "00-scope-and-plan.md": ["## \u7814\u7a76\u8303\u56f4", "## \u4e3b\u9898\u5206\u7c7b", "## \u6838\u5fc3\u95ee\u9898", "## \u6750\u6599\u6e05\u5355", "## \u8f93\u51fa\u8ba1\u5212"],
        "01-landscape.md": ["## \u4e3b\u9898\u6982\u51b5", "## \u6750\u6599\u5730\u56fe", "## \u5165\u53e3\u4e0e\u5173\u952e\u6587\u4ef6", "## \u6838\u5fc3\u6982\u5ff5", "## \u521d\u59cb\u95ee\u9898\u6e05\u5355"],
        "02-architecture.md": ["## \u6838\u5fc3\u62bd\u8c61", "## \u7ec4\u4ef6\u5173\u7cfb", "## \u4e3b\u8981\u6570\u636e\u6d41", "## \u5206\u5c42\u4e0e\u8fb9\u754c", "## \u63a5\u53e3\u5951\u7ea6"],
        "03-representations.md": ["## \u8868\u793a\u6e05\u5355", "## \u8282\u70b9\u7ed3\u6784\u4e0e\u5b57\u6bb5\u8bed\u4e49", "## \u9636\u6bb5\u5f52\u5c5e", "## \u4e0d\u53d8\u91cf\u4e0e\u7ea6\u675f", "## \u8868\u793a\u4e4b\u95f4\u7684\u8f6c\u6362\u5173\u7cfb"],
        "04-pipeline-stages.md": ["## \u7ba1\u7ebf\u9636\u6bb5\u6e05\u5355", "## \u9636\u6bb5\u8f93\u5165\u4e0e\u8f93\u51fa", "## \u9636\u6bb5\u5185\u5173\u952e\u64cd\u4f5c", "## \u9636\u6bb5\u95f4\u4fe1\u606f\u4f20\u9012", "## \u9519\u8bef\u68c0\u6d4b\u4e0e\u8bca\u65ad\u70b9"],
        "05-evaluation-rules.md": ["## \u89c4\u5219\u5217\u8868", "## \u89c4\u5219\u4e00", "## \u89c4\u5219\u4e8c", "## \u89c4\u5219\u4e4b\u95f4\u5982\u4f55\u534f\u4f5c", "## \u8bbe\u8ba1\u7ea6\u675f\u4e0e Trade-off"],
        "06-runtime-mechanics.md": ["## \u8fd0\u884c\u65f6\u673a\u5236", "## \u5185\u5b58\u7ba1\u7406", "## \u8c03\u5ea6\u4e0e\u6267\u884c\u6a21\u578b", "## \u5916\u90e8\u63a5\u53e3\u4e0e FFI"],
        "07-end-to-end-trace.md": ["## \u573a\u666f\u5b9a\u4e49", "## \u5165\u53e3\u6761\u4ef6", "## \u6267\u884c\u6b65\u9aa4", "## \u72b6\u6001\u53d8\u5316", "## \u573a\u666f\u7ed3\u8bba"],
        "08-failure-and-edge-cases.md": ["## \u5f02\u5e38\u8def\u5f84\u6e05\u5355", "## \u8fb9\u754c\u6761\u4ef6", "## \u8d44\u6e90\u91ca\u653e\u4e0e\u6e05\u7406", "## \u6613\u9519\u70b9"],
        "09-synthesis.md": ["## \u8bbe\u8ba1\u54f2\u5b66", "## \u5173\u952e Trade-off", "## \u53cd\u590d\u51fa\u73b0\u7684\u6a21\u5f0f", "## \u6838\u5fc3\u7ed3\u8bba"],
    },
}

MIN_ENTRY_RULES = {
    "source": {
        "01-core-data-structures.md": ("### \u7ed3\u6784\uff1a", 5),
        "02-core-functions.md": ("### \u51fd\u6570\uff1a", 8),
        "03-mechanisms.md": ("### \u673a\u5236\uff1a", 3),
        "05-end-to-end-trace.md": ("### \u573a\u666f\uff1a", 1),
        "06-failure-and-edge-cases.md": ("### \u6761\u76ee\uff1a", 4),
    },
    "protocol": {
        "03-message-formats.md": ("### \u683c\u5f0f\uff1a", 5),
        "04-state-machines.md": ("### \u72b6\u6001\uff1a", 5),
        "05-exchange-sequences.md": ("### \u6d41\u7a0b\uff1a", 3),
        "07-end-to-end-trace.md": ("### \u573a\u666f\uff1a", 1),
        "08-failure-and-edge-cases.md": ("### \u6761\u76ee\uff1a", 4),
    },
    "language": {
        "03-representations.md": ("### \u8868\u793a\uff1a", 5),
        "04-pipeline-stages.md": ("### \u9636\u6bb5\uff1a", 4),
        "05-evaluation-rules.md": ("### \u89c4\u5219\uff1a", 3),
        "07-end-to-end-trace.md": ("### \u573a\u666f\uff1a", 1),
        "08-failure-and-edge-cases.md": ("### \u6761\u76ee\uff1a", 4),
    },
}

MERMAID_PATTERN = re.compile(r"```mermaid\s+.*?```", re.DOTALL)
LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def normalize_link_target(target: str) -> str:
    target = target.strip()
    if target.startswith("./"):
        target = target[2:]
    return target


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def detect_study_type(study_dir: Path) -> str | None:
    """Auto-detect study type by checking which signature file exists."""
    for study_type, signature_file in TYPE_SIGNATURES.items():
        if (study_dir / signature_file).is_file():
            return study_type
    return None


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_study(study_dir: Path, study_type: str | None = None) -> list[str]:
    errors: list[str] = []

    if not study_dir.exists():
        return [f"Study directory does not exist: {study_dir}"]
    if not study_dir.is_dir():
        return [f"Study path is not a directory: {study_dir}"]

    # Auto-detect or validate type
    if study_type is None:
        study_type = detect_study_type(study_dir)
        if study_type is None:
            return [
                "Cannot detect study type. Expected one of: "
                "00-overview.md (source), "
                "03-message-formats.md (protocol), "
                "03-representations.md (language)"
            ]

    if study_type not in REQUIRED_FILES:
        return [f"Unknown study type: {study_type}. Must be one of: source, protocol, language"]

    required_files = REQUIRED_FILES[study_type]
    required_headings = REQUIRED_HEADINGS[study_type]
    entry_rules = MIN_ENTRY_RULES[study_type]

    # Check required files
    for filename in required_files:
        path = study_dir / filename
        if not path.is_file():
            errors.append(f"Missing required file: {filename}")

    # Check required headings
    for filename, headings in required_headings.items():
        path = study_dir / filename
        if not path.is_file():
            continue
        text = read_text(path)
        for heading in headings:
            if heading not in text:
                errors.append(f"{filename} is missing required heading: {heading}")

    # Check Mermaid blocks
    for filename in required_files:
        if filename == "README.md":
            continue
        path = study_dir / filename
        if not path.is_file():
            continue
        text = read_text(path)
        if not MERMAID_PATTERN.search(text):
            errors.append(f"{filename} must contain at least one Mermaid block")

    # Check minimum entry counts
    for filename, (prefix, minimum) in entry_rules.items():
        path = study_dir / filename
        if not path.is_file():
            continue
        text = read_text(path)
        count = sum(1 for line in text.splitlines() if line.startswith(prefix))
        if count < minimum:
            errors.append(f"{filename} \u81f3\u5c11\u5305\u542b {minimum} \u4e2a\u4ee5 '{prefix}' \u5f00\u5934\u7684\u6761\u76ee")

    # Check README links
    readme_path = study_dir / "README.md"
    if readme_path.is_file():
        readme = read_text(readme_path)
        targets = {normalize_link_target(target) for target in LINK_PATTERN.findall(readme)}
        for filename in required_files:
            if filename == "README.md":
                continue
            if filename not in targets:
                errors.append(f"README.md must link to {filename}")

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate a deep-study output directory against the type-specific contract."
    )
    parser.add_argument("study_dir", help="Path to study/<topic> directory")
    parser.add_argument(
        "--type",
        choices=["source", "protocol", "language"],
        default=None,
        help="Study type (auto-detected from files if omitted)",
    )
    args = parser.parse_args(argv)

    errors = validate_study(Path(args.study_dir), args.type)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"Validation failed: {len(errors)} issue(s)")
        return 1

    print("Validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
