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
            "## 研究范围与核心问题",
            "## 入口与材料地图",
            "## 核心概念",
            "## 组件关系与分层",
            "## 主要数据流",
        ],
        "01-core-data-structures.md": [
            "## 数据结构清单",
            "## 字段与职责",
            "## 不变量",
            "## 所有权与生命周期关系",
            "## 结构之间的依赖关系",
        ],
        "02-core-functions.md": [
            "## 关键函数清单",
            "## 函数职责与输入输出",
            "## 关键状态变化",
            "## 调用关系",
            "## 异常路径与失败处理",
        ],
        "03-mechanisms.md": [
            "## 机制列表",
            "## 机制详述",
            "## 机制之间如何协作",
            "## 设计约束与 Trade-off",
        ],
        "04-control-flow-and-state.md": [
            "## 主控制流",
            "## 关键状态转换",
            "## 跨模块控制交接",
        ],
        "05-end-to-end-trace.md": [
            "## 场景定义",
            "## 入口条件",
            "## 执行步骤",
            "## 状态变化",
            "## 场景结论",
        ],
        "06-failure-and-edge-cases.md": [
            "## 异常路径清单",
            "## 边界条件",
            "## 资源释放与清理",
            "## 易错点",
        ],
        "07-synthesis.md": [
            "## 设计哲学",
            "## 关键 Trade-off",
            "## 反复出现的模式",
            "## 核心结论",
        ],
    },
    "protocol": {
        "00-scope-and-plan.md": [
            "## 研究范围",
            "## 主题分类",
            "## 核心问题",
            "## 材料清单",
            "## 输出计划",
        ],
        "01-landscape.md": [
            "## 主题概况",
            "## 材料地图",
            "## 入口与关键文件",
            "## 核心概念",
            "## 初始问题清单",
        ],
        "02-architecture.md": [
            "## 核心抽象",
            "## 组件关系",
            "## 主要数据流",
            "## 分层与边界",
            "## 接口契约",
        ],
        "03-message-formats.md": [
            "## 消息格式清单",
            "## 字段语义与编码规则",
            "## 层次结构与扩展性",
            "## 兼容约束",
            "## 格式之间的关系",
        ],
        "04-state-machines.md": [
            "## 状态清单",
            "## 转换条件与触发事件",
            "## 转换副作用",
            "## 状态分类",
            "## 状态机之间的协作",
        ],
        "05-exchange-sequences.md": [
            "## 交互流程列表",
            "## 流程一",
            "## 流程二",
            "## 流程之间如何衔接",
            "## 设计约束与 Trade-off",
        ],
        "06-reliability-and-timing.md": [
            "## 可靠性机制",
            "## 超时与重传策略",
            "## 流控与拥塞控制",
            "## 时序约束",
        ],
        "07-end-to-end-trace.md": [
            "## 场景定义",
            "## 入口条件",
            "## 执行步骤",
            "## 状态变化",
            "## 场景结论",
        ],
        "08-failure-and-edge-cases.md": [
            "## 异常路径清单",
            "## 边界条件",
            "## 资源释放与清理",
            "## 易错点",
        ],
        "09-synthesis.md": [
            "## 设计哲学",
            "## 关键 Trade-off",
            "## 反复出现的模式",
            "## 核心结论",
        ],
    },
    "language": {
        "00-scope-and-plan.md": [
            "## 研究范围",
            "## 主题分类",
            "## 核心问题",
            "## 材料清单",
            "## 输出计划",
        ],
        "01-landscape.md": [
            "## 主题概况",
            "## 材料地图",
            "## 入口与关键文件",
            "## 核心概念",
            "## 初始问题清单",
        ],
        "02-architecture.md": [
            "## 核心抽象",
            "## 组件关系",
            "## 主要数据流",
            "## 分层与边界",
            "## 接口契约",
        ],
        "03-representations.md": [
            "## 表示清单",
            "## 节点结构与字段语义",
            "## 阶段归属",
            "## 不变量与约束",
            "## 表示之间的转换关系",
        ],
        "04-pipeline-stages.md": [
            "## 管线阶段清单",
            "## 阶段输入与输出",
            "## 阶段内关键操作",
            "## 阶段间信息传递",
            "## 错误检测与诊断点",
        ],
        "05-evaluation-rules.md": [
            "## 规则列表",
            "## 规则一",
            "## 规则二",
            "## 规则之间如何协作",
            "## 设计约束与 Trade-off",
        ],
        "06-runtime-mechanics.md": [
            "## 运行时机制",
            "## 内存管理",
            "## 调度与执行模型",
            "## 外部接口与 FFI",
        ],
        "07-end-to-end-trace.md": [
            "## 场景定义",
            "## 入口条件",
            "## 执行步骤",
            "## 状态变化",
            "## 场景结论",
        ],
        "08-failure-and-edge-cases.md": [
            "## 异常路径清单",
            "## 边界条件",
            "## 资源释放与清理",
            "## 易错点",
        ],
        "09-synthesis.md": [
            "## 设计哲学",
            "## 关键 Trade-off",
            "## 反复出现的模式",
            "## 核心结论",
        ],
    },
}

MIN_ENTRY_RULES = {
    "source": {
        "01-core-data-structures.md": ("### 结构：", 1),
        "02-core-functions.md": ("### 函数：", 1),
        "03-mechanisms.md": ("### 机制：", 1),
        "05-end-to-end-trace.md": ("### 场景：", 1),
        "06-failure-and-edge-cases.md": ("### 条目：", 1),
    },
    "protocol": {
        "03-message-formats.md": ("### 格式：", 5),
        "04-state-machines.md": ("### 状态：", 5),
        "05-exchange-sequences.md": ("### 流程：", 3),
        "07-end-to-end-trace.md": ("### 场景：", 1),
        "08-failure-and-edge-cases.md": ("### 条目：", 4),
    },
    "language": {
        "03-representations.md": ("### 表示：", 5),
        "04-pipeline-stages.md": ("### 阶段：", 4),
        "05-evaluation-rules.md": ("### 规则：", 3),
        "07-end-to-end-trace.md": ("### 场景：", 1),
        "08-failure-and-edge-cases.md": ("### 条目：", 4),
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
            errors.append(f"{filename} 至少包含 {minimum} 个以 '{prefix}' 开头的条目")

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
