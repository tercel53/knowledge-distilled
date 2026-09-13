# Codex CLI 的上下文工程：写入、选择、压缩与隔离

> 原文：*Context Engineering for Codex CLI in June 2026: The Write-Select-Compress-Isolate Playbook*  
> 来源：Codex Knowledge Base，发布于 2026-06-10，更新于 2026-09-09  
> 阅读整理：2026-09-13

## 核心结论

上下文工程不是把所有信息塞进提示词，而是持续控制信息的去向：把需要长期保留的内容**写到窗口外**，在需要时**选择性取回**，在窗口趋满时**压缩但保留关键状态**，并把无须共享的信息**隔离到独立上下文与权限边界**。

这四个动作不是固定步骤。它们分别解决不同故障，并通过组合形成系统：外部记录让压缩不必承担全部记忆；按需选择避免工具定义预占窗口；隔离让不同任务只看到各自需要的内容。

## 四个动作共同管理有限上下文

| 动作 | 信息如何移动 | 主要解决的问题 | 文中的 Codex 机制 |
| --- | --- | --- | --- |
| 写入 Write | 从当前窗口写到持久载体 | 跨轮次、跨窗口不丢工作约定与进度 | `AGENTS.md`、本地 memories、Skills、`PLANS.md` |
| 选择 Select | 从外部信息源按需取回 | 避免无关文档和工具定义占满窗口 | Tool Search、MCP 工具范围、Web Search |
| 压缩 Compress | 把已有内容提炼成更短表示 | 接近窗口上限时保留关键状态 | 自动上下文压缩、工具 schema 压缩、token budget 收尾 |
| 隔离 Isolate | 把工作分到不同窗口和访问边界 | 防止互不相关的任务、工具与文件互相污染 | Subagents、权限 profiles、OS sandbox |

关键区别：写入是“保存到外部”，选择是“需要时再读入”，压缩是“缩短当前表示”，隔离是“让内容根本不进入同一边界”。

## 每个动作改变不同的信息流

### 写入：把易失会话变成可再次读取的状态

作者把 `AGENTS.md` 视为可执行的操作策略，而非背景介绍；把 memories 与 `PLANS.md` 视为跨会话或跨压缩延续状态的载体。其机制是：重要信息不再只依赖对话历史，后续窗口可以重新读取。

这不意味着“写得越多越好”。持久内容仍需准确、可查找，并避免把短期噪声长期化。

### 选择：在下一步需要时才加载

Tool Search、MCP `enabled_tools` / `disabled_tools` 与 Web Search 分别在运行时或配置层控制哪些工具和资料进入窗口。它们处理的是相关性与时机：完整目录可以存在，但不必每轮全部出现。

### 压缩：缩短表示，而不是保证无损

自动上下文压缩会把较早内容变成摘要；schema 压缩减少工具定义占用；预算接近上限时的收尾引导促使 Agent 留下状态。压缩能延长任务，但摘要必然有信息损失风险，因此关键约定和进度仍应写入可复核的外部文件。

### 隔离：把无关信息和能力挡在边界之外

子代理让子任务拥有独立对话历史；工具范围和权限 profile 限定它能接触的能力；操作系统 sandbox 再限制可读写资源。三者强度不同：独立会话是上下文组织，工具/权限范围是能力约束，OS sandbox 才是更硬的访问边界。

## 组合使用让上下文管理形成系统

- **写入 + 选择**：`AGENTS.md` 规定先用 Tool Search，再调用 MCP 工具；保存的策略指导按需取用。
- **写入 + 压缩**：会话压缩后，Agent 重读 `PLANS.md` 恢复关键状态。
- **选择 + 隔离**：每个子任务只暴露自己的工具与资料，既减少占用，也减少串扰。
- **压缩 + 隔离**：各窗口独立压缩，一个子任务的摘要不会覆盖另一个子任务的历史。

作者最后把这种上下文编排放入更大的 Harness 工程：提示词只描述一次请求；上下文工程管理模型每次推理看到什么；Harness 工程进一步设计权限、沙箱、事件钩子和多代理协调，让上下文管理成为运行系统的一部分。

## 条件与边界

这是一篇将既有四策略框架映射到 Codex CLI 功能的观点/实践综述，不是受控实验。

- 文章对若干 Codex 机制的描述可由 OpenAI 官方文档核对，例如 `AGENTS.md` 层级、memories、压缩、子代理与工具范围。
- “Tool Search 减少 85–98% 工具定义开销”“完整采用四策略后可在累计 100,000 tokens 以上保持连贯，而单窗口在 30,000–40,000 后退化”等数字来自文章引用的二手基准或行业指南。原文没有给出统一任务、模型、团队和评价方法，不能据此得到普遍阈值。
- “超过两个领域就使用 subagents”与每个里程碑更新 `PLANS.md` 是作者的操作清单，不是 Codex 的必要条件。简单任务中，隔离与协调本身也有成本。
- 配置名称、默认值和版本能力会变化；真正采用前应以当前 OpenAI Docs 为准。

## 自测：我理解了吗？

### 1. 为什么把完整 MCP 工具目录写进 `AGENTS.md`，不能同时替代“写入”和“选择”？

<details>
<summary>展开参考答案与对照要点</summary>

**参考解释：** 写入只解决信息有稳定载体的问题；如果每轮把整个目录都放进窗口，仍会消耗大量上下文。选择要求只在当前任务需要时加载相关工具定义。

**对照要点：** 是否区分“外部存在”与“当前载入”，并指出无关内容的窗口成本。

**容易误解：** 选择并不要求删除完整目录，而是控制它何时、以多大范围进入窗口。

**回查：** [四个动作共同管理有限上下文](#四个动作共同管理有限上下文)；[原文](https://codex.danielvaughan.com/2026/06/10/context-engineering-codex-cli-write-select-compress-isolate-june-2026/)（*Strategy 1: Write*；*Strategy 2: Select*）。
</details>

### 2. 自动压缩已经存在，为什么多文件长任务仍可能需要外部计划文件？

<details>
<summary>展开参考答案与对照要点</summary>

**参考解释：** 压缩把历史提炼成摘要，可能省略关键约定或精确进度；外部计划文件提供可再次读取、可检查的状态。两者组合比只依赖会话摘要更稳健。

**对照要点：** 是否说明压缩有损，以及“写入 + 压缩”的恢复路径。

**容易误解：** 外部计划也会过时，仍需维护；它不是自动正确的永久记忆。

**回查：** [压缩：缩短表示，而不是保证无损](#压缩缩短表示而不是保证无损)；[原文](https://codex.danielvaughan.com/2026/06/10/context-engineering-codex-cli-write-select-compress-isolate-june-2026/)（*Strategy 3: Compress*；*The Compounding Effect*）。
</details>

### 3. 子代理拥有独立上下文，是否等于它已经获得了安全隔离？

<details>
<summary>展开参考答案与对照要点</summary>

**参考解释：** 不等于。独立会话历史减少信息串扰；工具范围和权限 profile 限定能力；OS sandbox 才进一步限制文件与系统资源访问。它们是不同强度的边界。

**对照要点：** 是否区分上下文组织、能力约束与资源访问控制。

**容易误解：** 不能因为使用了 subagent，就推断它无法访问不相关文件或工具；这取决于实际配置。

**回查：** [隔离：把无关信息和能力挡在边界之外](#隔离把无关信息和能力挡在边界之外)；[原文](https://codex.danielvaughan.com/2026/06/10/context-engineering-codex-cli-write-select-compress-isolate-june-2026/)（*Strategy 4: Isolate*）。
</details>

### 4. 能否把文章的 30,000–40,000 与 100,000 token 数字当作自己项目的可靠切换阈值？

<details>
<summary>展开参考答案与对照要点</summary>

**参考解释：** 不能直接照搬。原文没有提供足以复现和外推的统一实验条件。这些数字可作为风险提示，但项目阈值应基于自己的模型、任务、工具负载和质量评价实测。

**对照要点：** 是否保留证据强度与外推边界。

**容易误解：** 证据较弱不等于框架无用；它限制的是效果数字的确定性。

**回查：** [条件与边界](#条件与边界)；[原文](https://codex.danielvaughan.com/2026/06/10/context-engineering-codex-cli-write-select-compress-isolate-june-2026/)（*The Compounding Effect*）。
</details>

## 原文、核对来源与阅读范围

- [原文全文](https://codex.danielvaughan.com/2026/06/10/context-engineering-codex-cli-write-select-compress-isolate-june-2026/)
- [OpenAI Docs：AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [OpenAI Docs：Memories](https://learn.chatgpt.com/docs/customization/memories)
- [OpenAI Docs：Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)

本笔记覆盖原文从范式变化、四策略、组合效应到最小清单与 Harness 工程展望的完整主线；省略了大部分配置示例和逐条引用目录。具体配置应回到当前官方文档核对。
