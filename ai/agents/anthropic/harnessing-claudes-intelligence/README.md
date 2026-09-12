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

## 自测：我理解了吗？

先用自己的话回答，再按需展开参考答案。重点对照含义和依据，不必逐字一致；你可以理解作者后仍持不同意见。

### 1. 任务只需要工具结果表中的一列，为什么让模型写代码先筛选再回传，会改变原来的编排方式？

<details>
<summary>展开参考答案与对照要点</summary>

**参考解释：**模型决定哪些结果需要保留或交给下一个工具，执行环境运行筛选逻辑，只有所需输出进入上下文。这样移走的是无关中间数据的回传和部分外围编排决定，工具执行本身仍由环境承接。

**对照要点：**是否分清模型作出选择、环境处理数据和输出进入上下文的职责。

**容易误解：**不是让模型先读完整张表再概括；特定评测的提升也不能直接当作所有任务的收益。

**回查：**[HTML · 动作编排](./index.html#orchestration) · [原文依据](https://claude.com/blog/harnessing-claudes-intelligence)（章节：第 2 节 · Let Claude orchestrate its own actions）。

</details>

### 2. 假设应用预装了许多任务的完整指令，但当前只处理其中一类任务。按需加载 Skills 与清理旧内容、使用子代理分别解决什么问题？

<details>
<summary>展开参考答案与对照要点</summary>

**参考解释：**Skills 先提供简介，在任务需要时读取正文，减少无关指令预装；上下文编辑移除过时内容；子代理用独立窗口隔离工作。它们分别管理内容的进入、离开与隔离，不能互相当作同一操作。

**对照要点：**是否解释了三种机制各自处理的上下文问题。

**容易误解：**按需加载不是完全不给任务知识，也不是要求三种机制每次都按固定顺序执行。

**回查：**[HTML · 当前上下文](./index.html#context) · [原文依据](https://claude.com/blog/harnessing-claudes-intelligence)（章节：第 2 节 · Let Claude manage its own context）。

</details>

### 3. 模型已经很会用 Bash，是否就可以取消应用中的专用工具和动作确认？

<details>
<summary>展开参考答案与对照要点</summary>

**参考解释：**不能由工具熟练度推出这个结论。应用仍可能需要识别具体动作并执行确认、呈现、审计或新旧检查；带类型化参数的专用工具提供这种入口。是否保留取决于应用边界，而不是只看模型会不会写命令。

**对照要点：**是否区分模型能力与应用要求，并说明专用工具的作用。

**容易误解：**不是每个动作都要经过所有检查；作者也没有要求对所有场景取消专用工具。

**回查：**[HTML · 应用边界](./index.html#boundaries) · [原文依据](https://claude.com/blog/harnessing-claudes-intelligence)（章节：第 3 节 · Use declarative tools for UX, observability, or security boundaries）。

</details>

### 4. 某次升级后模型不再提前收尾，因此删除了旧的上下文重置。能否推断后续所有 Harness 组件都应该越少越好？

<details>
<summary>展开参考答案与对照要点</summary>

**参考解释：**不能。这个案例说明应重测某项补偿所依赖的能力假设：问题消失后，原补偿可能成为负担。其他组件还可能承担上下文管理、成本或应用边界职责，需要分别判断，下一次能力变化后还要再检验。

**对照要点：**是否把“删除失效补偿”与“无条件减少组件”区分开。

**容易误解：**一个模型版本的案例不是普遍删减流程，三种设计模式也不是固定实施步骤。

**回查：**[HTML · 模型升级后的重测](./index.html#limits) · [原文依据](https://claude.com/blog/harnessing-claudes-intelligence)（章节：The future of agent harness design；第 3 节）。

</details>

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
