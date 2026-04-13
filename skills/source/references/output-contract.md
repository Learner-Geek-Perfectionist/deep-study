# Deep Study Source Output Contract

源码实现分析的产出目录必须严格匹配下面这套结构。

## 必需文件

研究输出目录 `study/<topic>/` 中必须存在：

- `00-overview.md`
- `01-core-data-structures.md`
- `02-core-functions.md`
- `03-mechanisms.md`
- `04-control-flow-and-state.md`
- `05-end-to-end-trace.md`
- `06-failure-and-edge-cases.md`
- `07-synthesis.md`
- `README.md`

不允许用其他文件名替代这些文件。不允许把 `01-core-data-structures.md` 和 `02-core-functions.md` 折叠进 `03-mechanisms.md`。

## 必需二级标题

### `00-overview.md`

- `## 研究范围与核心问题`
- `## 入口与材料地图`
- `## 核心概念`
- `## 组件关系与分层`
- `## 主要数据流`

### `01-core-data-structures.md`

- `## 数据结构清单`
- `## 字段与职责`
- `## 不变量`
- `## 所有权与生命周期关系`
- `## 结构之间的依赖关系`

### `02-core-functions.md`

- `## 关键函数清单`
- `## 函数职责与输入输出`
- `## 关键状态变化`
- `## 调用关系`
- `## 异常路径与失败处理`

### `03-mechanisms.md`

- `## 机制列表`
- `## 机制详述`
- `## 机制之间如何协作`
- `## 设计约束与 Trade-off`

### `04-control-flow-and-state.md`

- `## 主控制流`
- `## 关键状态转换`
- `## 跨模块控制交接`

如果项目涉及并发，建议增加 `## 并发与同步` 章节，但不作为必需标题强制校验。

### `05-end-to-end-trace.md`

- `## 场景定义`
- `## 入口条件`
- `## 执行步骤`
- `## 状态变化`
- `## 场景结论`

### `06-failure-and-edge-cases.md`

- `## 异常路径清单`
- `## 边界条件`
- `## 资源释放与清理`
- `## 易错点`

### `07-synthesis.md`

- `## 设计哲学`
- `## 关键 Trade-off`
- `## 反复出现的模式`
- `## 核心结论`

## 条目格式与最低要求

以下文件的条目必须使用指定的三级标题前缀，且至少包含 1 个条目：

- `01-core-data-structures.md` — 每个条目以 `### 结构：` 开头
- `02-core-functions.md` — 每个条目以 `### 函数：` 开头
- `03-mechanisms.md` — 每个条目以 `### 机制：` 开头
- `05-end-to-end-trace.md` — 每个条目以 `### 场景：` 开头
- `06-failure-and-edge-cases.md` — 每个条目以 `### 条目：` 开头

不限制最大数量，根据项目实际规模决定条目数。

## Mermaid 规则

除 `README.md` 之外，所有阶段文件都必须至少包含一个 Mermaid 代码块。

## README 规则

`README.md` 必须：

- 用相对链接链接到其余全部 8 个文件（校验脚本检查）
- 给出建议阅读顺序（由 skill 指令约束，脚本不检查）
- 给出每个文件的一句话摘要（由 skill 指令约束，脚本不检查）

## 校验命令

在宣称研究完成前，必须从工作区根目录运行：

```bash
python3 deep-study/scripts/validate-study.py study/<topic>
```

如果校验失败：

1. 不得宣称完成
2. 不得用"内容已经基本覆盖"替代修复
3. 必须修正文档后重新运行校验，直到退出码为 `0`

## 视为不合格的情况

- 缺少任一必需文件
- 缺少任一必需二级标题
- `01-core-data-structures.md` 中没有显式的数据结构条目
- `02-core-functions.md` 中没有显式的函数条目
- 把函数解析、数据结构解析折叠进机制文档
- README 没有完整链接所有文件
- 任一阶段文件没有 Mermaid 图
