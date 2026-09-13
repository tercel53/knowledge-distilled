# Claude Code Harness Engineering：五层 Harness 与渐进建设路径

英文原标题：Claude Code Harness Engineering: The Complete Guide

来源：[ShipWithAI 原文](https://shipwithai.io/blog/claude-code-harness-engineering-guide/) · ShipWithAI · 2026-04-20

## 一句话结论

**这篇文章真正有用的不是“必须一次装齐五层”，而是把 Claude Code 的生产可靠性拆成五个不同问题：记忆、工具、权限、运行时约束与可观测性；再根据当前失败模式逐层补齐。**

文章把 Harness 定义为模型之外的运行系统，并用 Memory、Tools、Permissions、Hooks、Observability 五层组织 Claude Code 的配置与阅读路径。它同时强调从 Memory 和一个 PreToolUse guard 起步，而不是先堆满所有能力。

## 五层分别解决什么

| 层 | 要回答的问题 | 文章中的 Claude Code 载体 |
| --- | --- | --- |
| Memory | Agent 进入任务前知道什么？ | `CLAUDE.md`、`MEMORY.md` |
| Tools | Agent 能接触什么能力？ | MCP / `settings.json` |
| Permissions | 已接入能力里允许做什么？ | allow / deny |
| Hooks | 哪些规则必须在运行时强制执行？ | `PreToolUse` / `PostToolUse` |
| Observability | 事后怎样知道 Agent 做了什么、为何失败？ | session logs、cost tracking、verification |

五层不是五个同义的“规则文件”。Memory 提供信息，Tools 扩展可达能力，Permissions 缩小授权范围，Hooks 在工具执行路径上做运行时检查，Observability 留下可诊断证据。

## 关键机制：建议与强制不是一回事

文章最值得保留的连接是 **Memory → Hooks 的性质变化**：写在 `CLAUDE.md` 里的约束仍是模型需要遵循的上下文；PreToolUse hook 则位于工具调用之前，可以在运行时阻断动作。因而危险动作不应只靠“请不要这样做”的文字约束。

但这里要保留边界：文章把 hooks 描述为最强的强制层，是作者对 Claude Code 配置面的实践归纳；具体权限与 hook 行为仍应以当前 Claude Code 官方文档为准。

## 建设顺序不是层号顺序

文章给出的实践顺序是：**Memory → Hooks → Tools → Permissions → Observability**。理由不是“第 4 层比第 2 层重要”，而是先给必要上下文，再在扩大能力之前建立运行时护栏，然后按最小权限收窄范围，最后用观测验证真实行为。

因此“五层架构”和“实施顺序”是两个不同概念：前者分类职责，后者表达作者建议的风险控制路径。

## 证据与边界

文章引用 LangChain 在 Terminal Bench 2.0 上从 52.8% 到 66.5% 的提升，作为 Harness 设计能影响结果的证据。但该提升来自多项 Harness 改进共同作用，不能证明这篇文章定义的五层各自贡献多少，也不能推出“装齐五层必然提升 13.7 分”。

文章还引用 OpenAI Codex、Ghostty、开发者采用率等材料支持“约束比单纯增加模型能力更重要”的观点。这些材料来源、任务和评价口径不同，更适合视为实践动机，而不是三组独立实验共同证明一个普遍因果定律。

此外，本文自己明确定位为 **navigation hub / reading path**：Layer 2 和 Layer 3 当时甚至没有独立 deep-dive。因此它更适合作为 Claude Code Harness 的导航框架，而不是完整的生产配置规范。

## 自测：我理解了吗？

<details><summary>1. 为什么已有 CLAUDE.md 仍不等于有完整 Harness？</summary>因为它主要解决 Memory/上下文问题，不能替代工具范围、权限、运行时阻断和事后观测。</details>

<details><summary>2. 为什么作者建议先加 Hook，再扩展 Tools？</summary>先建立危险动作的运行时边界，再扩大 Agent 可触达的能力，避免能力增长先于护栏。</details>

<details><summary>3. LangChain 的 +13.7 能证明五层模型本身有效吗？</summary>不能直接证明。它说明 Harness 改动可以显著影响同一模型的表现，但改动包含多种机制，不能把增益归因给本文五层中的某一层或“装齐五层”。</details>

## 原文定位

重点阅读：What is Claude Code harness engineering?；What are the 5 layers...；Layer 1；Layer 4；Layer 5；Why does this actually work?；Where should you start reading?。
