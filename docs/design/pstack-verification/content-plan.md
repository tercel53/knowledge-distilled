# The Complete Guide to pstack Pt. 1 · 内容骨架

## 五问

- 问题：Agent 即使能快速写代码，为什么团队仍然会被人工验收拖住，难以扩大并行和自主性？
- 结论：作者认为 verification 应当被当作关键基础设施。Agent 必须能控制真实运行环境、观察结果并收集证据，从而自己闭合实现—验证—修正循环；在此基础上再扩展并行与自动化。
- 理由/机制：真实运行提供反馈；Agent 友好的控制 CLI 把重复操作变成稳定工具；Feature Map 提供功能入口和使用上下文；持续维护保证这些压缩上下文不过期。闭环稳定后，同一能力才能被复制到 Cloud Agents、swarm 与 routines。
- 证据：Grok Bot / Cursor 实践、示例控制 CLI、Feature Map 示例、作者给出的新功能/性能/用户反馈工作流，以及作者自述的 PR 规模和效率增益。文章不是对照实验，也没有统一质量指标或失败率数据。
- 边界与代价：验证脚本可能验证错误条件；运行时工具、测试数据和环境需要持续投入；Feature Map 会漂移；Cloud Agents 与 Automations 是具体产品实现；“2000 PR/月”“100–1000x”不能从本文外推为普遍效果。

## 连续解释

作者的核心判断是：Agent 的自主性受限于反馈，而不是受限于生成代码的速度。如果 Agent 修改之后仍需要人替它启动应用、复现、操作 UI、看日志和判断是否正确，人就仍然是闭环里的关键节点。verification skill 要做的是把这些手工动作工程化：先保证应用有足够好的运行时可观测性，再把导航、交互、截图、trace、健康检查等操作封装成稳定 CLI，让 Agent 可以重复调用。随着应用变大，仅有工具还不够，因此再用 Feature Map 把“有哪些功能、用户如何到达、怎样控制、有哪些坑”压缩成可搜索的共享记忆。因为工具和产品都会变化，这套验证能力需要像基础设施一样维护。只有当单个 Agent 已经能稳定完成闭环时，作者才建议把同一能力复制到 Cloud Agents、swarm 和自动化流程。文章提供的是强工程经验和具体机制，不是验证其效率倍数的独立实验。

## K 点与证据对应

| K 点 | 作者实际主张与类型 | 依据及原文位置 | 连接理由 | 条件/未知 | 默认呈现与展开位置 | 自评 |
| --- | --- | --- | --- | --- | --- | --- |
| K1 | verification 的核心是 Agent 能验证自己的工作并持续迭代（作者主张） | Part 1 – Verification is all you need | 真实反馈让“修改→检查→修正”不再依赖人逐步介入 | 能执行检查不代表检查目标一定正确 | loop 主图 + 展开 | Q1/Q3 |
| K2 | 验证依赖可控制、可调试、可观测的运行时（作者工程建议） | build verification skill；tech stack / CDP / simulator | 没有真实运行反馈，Agent 无法判断行为结果 | 不同技术栈的可观测能力差异很大 | lever 底层 | Q1 |
| K3 | 应把重复调试动作做成 Agent 友好的 CLI（作者工程建议） | Make it Reproducible；CLI examples | 稳定工具降低重复探索和临时脚本成本，并可复用/测试 | CLI 自身需要维护，命令设计质量影响效果 | lever 主图 + 细节 | Q1 |
| K4 | Feature Map 是功能与控制方式的紧凑索引 / materialized memory（作者概念） | Keep agents smart with Feature Maps | CLI 解决动作能力，Feature Map 补充“去哪里、怎么到达、有什么坑”的产品上下文 | 它会过期，不能替代代码源事实 | memory 主图 | Q2 |
| K5 | verification skill 必须持续维护（作者建议） | maintain-verification-skill；Invest... | 产品变化会让控制工具和功能索引漂移 | 每日维护是作者建议，不是普遍必要频率 | memory 短说明 | Q2 |
| K6 | 稳定验证闭环之后才适合扩大并行和自动化（作者工作流） | Cloud Agents；swarm；routines / automations | 并行复制的是已有能力，先有闭环才有可扩展性 | 成本、安全、权限、协调开销正文未系统讨论 | scale 主图 | Q4 |
| K7 | 高 PR 数和 100–1000x 是作者实践主张，不是独立效果证明（阅读判断） | 开头与 Invest... | 无对照、统一质量指标或失败率，不能外推 | 不否定作者可能真实获得增益，只限定本文证据范围 | boundaries | Q3/Q4 |

## 图解任务

1. `verification-loop`：回答“为什么 verification 能减少人工瓶颈？” K1/K2；人给目标，Agent 在实现—运行—观察之间闭环，失败返回实现，成功输出证据。反馈线必须真实返回实现节点。
2. `verification-stack`：回答“一套 verification skill 由什么工程能力支撑？” K2/K3；用三层堆叠表达 Runtime → Control CLI → Verification Skill，层级表示依赖，不表示时间顺序。
3. `feature-memory`：回答“Feature Map 在哪里补足 CLI？” K4/K5；用 Codebase → 压缩索引 → Feature Map → 按需查询 → Agent，明确 Feature Map 不是第二事实源。
4. `scale-ladder`：回答“为什么先验证再并行？” K6；按能力依赖展示单 Agent 闭环 → 隔离并行 → 批量验证 → 自动触发。表示作者建议的成熟顺序，不表示所有团队必须经历这些阶段。

## 省略与后置

- CLI 完整命令列表只保留代表性类别，不逐项复制。
- 安装 pstack、Dr Eggbot 的产品引导与链接不进入主线。
- worktree 与 Cursor Cloud Agents 的产品比较压缩到“隔离并行”层，避免把产品选型当作核心结论。
- Grok Bot 的具体组织背景只作为实践证据，不展开团队细节。
- 保留作者 PR 规模与 100–1000x 说法的证据边界，不把它们放进核心结论或视觉比例。
