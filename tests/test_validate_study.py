import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = ROOT / "deep-study" / "scripts" / "validate-study.py"


# ---------------------------------------------------------------------------
# Per-type definitions mirroring the validator
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


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_validator_module():
    spec = importlib.util.spec_from_file_location("validate_study", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def write_markdown(path: Path, headings, mermaid=True, entry_prefix=None, entry_count=0):
    lines = ["# Title", ""]
    for heading in headings:
        lines.extend([heading, "", "content", ""])
    for i in range(entry_count):
        lines.extend([f"{entry_prefix}{i + 1}", "", "details", ""])
    if mermaid:
        lines.extend(["```mermaid", "flowchart TD", "A-->B", "```", ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def make_valid_study(root: Path, study_type: str):
    all_files = REQUIRED_FILES[study_type]
    all_headings = REQUIRED_HEADINGS[study_type]
    all_entry_rules = MIN_ENTRY_RULES[study_type]

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
# Tests — Source
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
            (study_dir / "02-core-functions.md").unlink()
            errors = module.validate_study(study_dir)
            self.assertTrue(any("02-core-functions.md" in e for e in errors))

    def test_missing_heading_fails(self):
        module = load_validator_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            study_dir = Path(tmpdir)
            make_valid_study(study_dir, "source")
            target = study_dir / "01-core-data-structures.md"
            target.write_text(
                target.read_text(encoding="utf-8").replace("## 不变量", "## 字段列表"),
                encoding="utf-8",
            )
            errors = module.validate_study(study_dir)
            self.assertTrue(any("## 不变量" in e for e in errors))

    def test_empty_entries_fails(self):
        module = load_validator_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            study_dir = Path(tmpdir)
            make_valid_study(study_dir, "source")
            # Rewrite 01 with headings and mermaid but zero ### 结构： entries
            headings = REQUIRED_HEADINGS["source"]["01-core-data-structures.md"]
            write_markdown(study_dir / "01-core-data-structures.md", headings, mermaid=True, entry_prefix=None, entry_count=0)
            errors = module.validate_study(study_dir)
            self.assertTrue(any("01-core-data-structures.md" in e and "结构：" in e for e in errors))

    def test_missing_mermaid_fails(self):
        module = load_validator_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            study_dir = Path(tmpdir)
            make_valid_study(study_dir, "source")
            headings = REQUIRED_HEADINGS["source"]["00-overview.md"]
            write_markdown(study_dir / "00-overview.md", headings, mermaid=False)
            errors = module.validate_study(study_dir)
            self.assertTrue(any("00-overview.md" in e and "Mermaid" in e for e in errors))

    def test_readme_missing_link_fails(self):
        module = load_validator_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            study_dir = Path(tmpdir)
            make_valid_study(study_dir, "source")
            (study_dir / "README.md").write_text("# README\n", encoding="utf-8")
            errors = module.validate_study(study_dir)
            self.assertTrue(any("README.md" in e for e in errors))


# ---------------------------------------------------------------------------
# Tests — Protocol
# ---------------------------------------------------------------------------

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
                target.read_text(encoding="utf-8").replace("## 状态清单", "## 其他标题"),
                encoding="utf-8",
            )
            errors = module.validate_study(study_dir)
            self.assertTrue(any("## 状态清单" in e for e in errors))

    def test_missing_format_entry_count_fails(self):
        module = load_validator_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            study_dir = Path(tmpdir)
            make_valid_study(study_dir, "protocol")
            headings = REQUIRED_HEADINGS["protocol"]["03-message-formats.md"]
            write_markdown(
                study_dir / "03-message-formats.md",
                headings,
                mermaid=True,
                entry_prefix="### 格式：",
                entry_count=2,
            )
            errors = module.validate_study(study_dir)
            self.assertTrue(any("至少包含 5 个" in e for e in errors))


# ---------------------------------------------------------------------------
# Tests — Language
# ---------------------------------------------------------------------------

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
                target.read_text(encoding="utf-8").replace("## 管线阶段清单", "## 其他标题"),
                encoding="utf-8",
            )
            errors = module.validate_study(study_dir)
            self.assertTrue(any("## 管线阶段清单" in e for e in errors))

    def test_missing_stage_entry_count_fails(self):
        module = load_validator_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            study_dir = Path(tmpdir)
            make_valid_study(study_dir, "language")
            headings = REQUIRED_HEADINGS["language"]["04-pipeline-stages.md"]
            write_markdown(
                study_dir / "04-pipeline-stages.md",
                headings,
                mermaid=True,
                entry_prefix="### 阶段：",
                entry_count=1,
            )
            errors = module.validate_study(study_dir)
            self.assertTrue(any("至少包含 4 个" in e for e in errors))


# ---------------------------------------------------------------------------
# Tests — Auto-detection
# ---------------------------------------------------------------------------

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
            (study_dir / "random-file.md").write_text("# Test", encoding="utf-8")
            errors = module.validate_study(study_dir)
            self.assertTrue(any("Cannot detect study type" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
