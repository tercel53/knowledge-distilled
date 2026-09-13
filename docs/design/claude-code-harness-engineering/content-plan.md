# 内容计划：Claude Code Harness Engineering

## 认知形态

工程实践 / 方法框架 + 导航型教程。标准入库；不因“Complete Guide”标题自动升级深度验收。

## 五问

- 问题：只有 CLAUDE.md 的团队仍缺少能力边界、运行时约束和诊断反馈。
- 结论：用 Memory、Tools、Permissions、Hooks、Observability 五层区分 Harness 职责，并按失败模式渐进建设。
- 机制：信息、能力、授权、运行时强制和事后证据分别解决不同失败来源；作者建议先 Memory 和 Hooks，再扩大工具能力。
- 证据：引用 LangChain Terminal Bench 2.0、OpenAI Codex、Ghostty 与开发者调查；本文自身主要是教程/导航汇总。
- 边界：不同引用并非同口径实验；+13.7 不能归因于五层模型；具体 Claude Code 配置会随版本变化。

## K 点

- K1：Harness 不等于模型或提示词，而是模型周围的运行系统。
- K2：五层分别回答知道什么、能触达什么、允许什么、强制什么、能观察什么。
- K3：Memory 中的建议与 Hooks 的运行时强制性质不同。
- K4：五层编号不是建设顺序；作者建议 guardrails before capabilities。
- K5：基准支持 Harness 重要，但不能证明五层各自贡献或
“装齐五层”的固定收益。

## 图解任务

- 五层图：并列职责，不画成执行顺序。
- 建设顺序：单独表达作者建议的 Memory → Hooks → Tools → Permissions → Observability，明确这是风险控制路径，不是架构层级。
