# Deep Study Language Output Contract

编程语言机制分析的产出目录必须严格匹配下面这套结构。

## 必需文件

研究输出目录 `study/<topic>/` 中必须存在：

- `00-scope-and-plan.md`
- `01-landscape.md`
- `02-architecture.md`
- `03-representations.md`
- `04-pipeline-stages.md`
- `05-evaluation-rules.md`
- `06-runtime-mechanics.md`
- `07-end-to-end-trace.md`
- `08-failure-and-edge-cases.md`
- `09-synthesis.md`
- `README.md`

不允许用其他文件名替代这些文件。不允许把 `03-representations.md` 和 `04-pipeline-stages.md` 折叠进 `05-evaluation-rules.md`。

## 必需二级标题

### `00-scope-and-plan.md`

- `## 研究范围`
- `## 主题分类`
- `## 核心问题`
- `## 材料清单`
- `## 输出计划`

### `01-landscape.md`

- `## 主题概况`
- `## 材料地图`
- `## 入口与关键文件`
- `## 核心概念`
- `## 初始问题清单`

### `02-architecture.md`

- `## 核心抽象`
- `## 组件关系`
- `## 主要数据流`
- `## 分层与边界`
- `## 接口契约`

### `03-representations.md`

- `## 表示清单`
- `## 节点结构与字段语义`
- `## 阶段归属`
- `## 不变量与约束`
- `## 表示之间的转换关系`

### `04-pipeline-stages.md`

- `## 管线阶段清单`
- `## 阶段输入与输出`
- `## 阶段内关键操作`
- `## 阶段间信息传递`
- `## 错误检测与诊断点`

### `05-evaluation-rules.md`

- `## 规则列表`
- `## 规则一`
- `## 规则二`
- `## 规则之间如何协作`
- `## 设计约束与 Trade-off`

### `06-runtime-mechanics.md`

- `## 运行时机制`
- `## 内存管理`
- `## 调度与执行模型`
- `## 外部接口与 FFI`

### `07-end-to-end-trace.md`

- `## 场景定义`
- `## 入口条件`
- `## 执行步骤`
- `## 状态变化`
- `## 场景结论`

### `08-failure-and-edge-cases.md`

- `## 异常路径清单`
- `## 边界条件`
- `## 资源释放与清理`
- `## 易错点`

### `09-synthesis.md`

- `## 设计哲学`
- `## 关键 Trade-off`
- `## 反复出现的模式`
- `## 核心结论`

## 最小条目数

以下文件必须达到最小条目数，条目必须使用指定的三级标题前缀：

- `03-representations.md`
  - 至少 5 个条目
  - 每个条目以 `### 表示：` 开头
- `04-pipeline-stages.md`
  - 至少 4 个条目
  - 每个条目以 `### 阶段：` 开头
- `05-evaluation-rules.md`
  - 至少 3 个条目
  - 每个条目以 `### 规则：` 开头
- `07-end-to-end-trace.md`
  - 至少 1 个条目
  - 每个条目以 `### 场景：` 开头
- `08-failure-and-edge-cases.md`
  - 至少 4 个条目
  - 每个条目以 `### 条目：` 开头

## Mermaid 规则

除 `README.md` 之外，所有阶段文件都必须至少包含一个 Mermaid 代码块。

## README 规则

`README.md` 必须：

- 用相对链接链接到其余全部 10 个文件
- 给出建议阅读顺序
- 给出每个文件的一句话摘要

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
- `03-representations.md` 中没有显式的表示条目
- `04-pipeline-stages.md` 中没有显式的阶段条目
- 把表示和管线分析折叠进求值规则文档
- README 没有完整链接所有文件
- 任一阶段文件没有 Mermaid 图
