# Agent Harness 设计：释放 Claude 智能的三种模式

英文原标题：Agent Harness Design: 3 Patterns for Harnessing Claude's Intelligence

来源：[Anthropic 原文](https://claude.com/blog/harnessing-claudes-intelligence) · Lance Martin · 2026-04-02

整理日期：2026-09-12

## 核心结论

Harness 包含对模型能力的假设；模型进步后，应重测这些假设，删减失效的补偿，同时落实应用仍需要的边界。

## 为什么已有的 Harness 会过时？

Harness 是模型周围的循环、工具、上下文管理与护栏。作者关注的是：其中一些结构建立在“模型不能自行完成某事”的假设上，而模型能力会变化。

因此，设计工作既包括搭建支撑，也包括判断何时可以撤掉支撑。下面三种模式围绕这一问题展开，彼此关联，并非固定实施步骤。

图解：模型能力变化 → 重测 Harness 的设计理由。分支一：补偿能力不足，检查模型能否接管；分支二：落实应用要求，检查边界是否仍需保留。下一次升级继续重测。此图为阅读归纳，不是自动删减流程。

## 通用工具为什么能成为放手的基础？

模型已经熟悉 Bash 和文件编辑，就能用它们组合行为。原文将 Skills、程序化工具调用和记忆列为这种组合的例子。

阅读归纳：论证作用：先说明模型已有可利用的能力，才有理由检验外围逻辑是否仍需替它做决定。熟悉工具并不意味着可以省掉应用边界。

依据：[正文第 1 节](https://claude.com/blog/harnessing-claudes-intelligence)

## 把“模型不能做”拆开验证

原文依次检查动作编排、当前上下文和跨窗口记忆。关键变化是让模型获得选择权；下面按“旧假设 → 代价 → 替代方式”展开。

### 动作编排：中间数据必须经过模型吗？

- 旧假设：每个工具结果都回传模型，再决定下一步。
- 问题在哪里：大表只需一列，其余数据仍占用上下文并增加处理成本。
- 替代方式：让模型写代码筛选、串联工具，执行环境处理数据，仅所需输出回传。

数据流：原始工具结果 → 执行环境中的代码筛选／串联 → 所需输出进入模型上下文。被省去的是无关中间结果的回传。

原文报告：Opus 4.6 在 BrowseComp 中自行过滤工具输出后，准确率由 45.3% 升至 61.6%。这是该评测结果，不能当作所有任务的预期提升。

依据：[正文第 2 节](https://claude.com/blog/harnessing-claudes-intelligence)

### 当前上下文：所有任务知识都要预装吗？

- 旧假设：预先在提示中放入各类任务指令。
- 问题在哪里：多任务下持续占用注意力，少用的指令也要付出上下文代价。
- 替代方式：Skills 先提供简短描述，再按需读取正文；上下文编辑移除旧内容，子代理用独立窗口隔离工作。

原文第 2 节的上下文讨论：这些机制分别解决加载、清理和隔离问题。

依据：[正文第 2 节](https://claude.com/blog/harnessing-claudes-intelligence)

### 长期记忆：必须在模型外决定保留什么吗？

- 旧假设：长期记忆依赖围绕模型搭建的检索基础设施。
- 问题在哪里：跨窗口任务需要选择保留内容，单有存储并不解释如何选择。
- 替代方式：提供压缩与记忆文件，让模型选择摘要内容、写入并按需读取。

原文游戏案例中，较早模型偏向记录对话，较新模型能保存战术经验。阅读理解：工具相近时，记忆的有效使用仍取决于模型能力。

依据：[正文第 2 节](https://claude.com/blog/harnessing-claudes-intelligence)

## 模型会做，不等于应用要求已落实

Claude 未必知道产品的安全边界或界面要求。Harness 接收并执行工具调用，因而可以在动作发生时落实这些要求。

### 成本

上下文每轮重新打包，稳定前缀有助于复用缓存。

保留的支撑：稳定内容在前、变化在后；更新采用追加消息，并维护缓存断点。

### 交互与安全

Bash 只有命令字符串，应用需要识别具体动作。

保留的支撑：专用工具提供类型化参数，用于确认、界面呈现、审计或编辑前的新旧检查。

依据：[正文第 3 节](https://claude.com/blog/harnessing-claudes-intelligence)

## 模型升级后，再问一次：这段逻辑还需要吗？

原文末节给出直接例子：Sonnet 4.5 接近上下文限制时会提前收尾，团队曾加入重置来补偿；Opus 4.5 不再出现该行为，旧补偿就失去了作用。

阅读归纳：这回应了开篇：保留结构的理由需要随能力变化重新成立。不能由这些案例推出所有任务都应删掉编排、记忆检索或专用工具。

作者也保留了限制：自动审查 Bash 的方案以用户信任任务方向为前提，高风险动作仍可能需要专用工具。本文是设计经验与特定评测的报告，不是通用收益保证。

依据：[正文末节；第 3 节末尾](https://claude.com/blog/harnessing-claudes-intelligence)

## 原文定位

- [引言与第 1 节](https://claude.com/blog/harnessing-claudes-intelligence)：先指出能力假设会过时，再说明可依托模型熟悉的工具。

- [第 2 节](https://claude.com/blog/harnessing-claudes-intelligence)：围绕动作编排、当前上下文、长期记忆，检验三类假设。

- [第 3 节](https://claude.com/blog/harnessing-claudes-intelligence)：解释缓存与专用工具为何仍服务于应用要求。

- [末节](https://claude.com/blog/harnessing-claudes-intelligence)：用上下文重置失效的案例回应开篇，提出持续重测。

## HTML 图解阅读索引

图解是上述内容的可编辑视觉表达，不是新增实验：

- [能力变化触发重新评估](index.html#map-caption)
- [通用工具组合多种行为](index.html#tools-caption)
- [整表回传与先筛选后回传对照](index.html#flow-caption)
- [全部预装与按需加载对照，区分加载移除隔离](index.html#context-caption)
- [压缩与文件记忆延续上下文](index.html#memory-caption)
- [稳定前缀复用与追加更新](index.html#cache-caption)
- [环境承接动作边界](index.html#gate-caption)
- [模型升级使原补偿理由失效](index.html#upgrade-caption)
