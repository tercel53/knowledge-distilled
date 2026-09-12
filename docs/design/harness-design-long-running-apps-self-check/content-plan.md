# 静态自评内容计划

日期：2026-09-12。仅新增自测、目录入口及同步 Markdown/metadata，保留原文主线与已认可图解。

原文：[来源](https://www.anthropic.com/engineering/harness-design-long-running-apps)。题目以原文与当前笔记共同核对，假设情境不冒充作者案例。

| 题号 | 检查的问题 | 正文回查 | 原文依据 |
| --- | --- | --- | --- |
| 1 / check-contract | 已经有 Planner 写出的产品方案，为什么第一版 Harness 仍让 Generator 和 Evaluator 在编码前协商本轮验收约定？ | architecture | Scaling to full-stack coding / The architecture；Removing the sprint construct |
| 2 / check-evaluation | 假设一个独立 Evaluator 只看页面截图，认为“整体不错”就放行。仅仅与 Generator 分开，是否已经满足本文的评估思路？ | boundaries | Why naive implementations fall short；Frontend design: making subjective quality gradable；Running the harness |
| 3 / check-evolution | 模型升级后连续开发能力变强，是否应一次性删掉重置、sprint 和 Evaluator？怎样判断？ | evolution | Iterating on the harness；Removing the sprint construct |
| 4 / check-limits | 假设浏览器 DAW 已通过一轮 QA，能否据此认定它达到专业级音乐制作质量？ | boundaries | Running the harness；Results from the updated harness |

答案仅核对上述已解释机制；自评独立折叠，无答题状态、提交或 AI 集成。原文入口采用已核实 URL 加章节名，不编造锚点。

原文核对修正：正文曾写作者没有一次性大改，原文实际是先大改失败后改为逐项移除；HTML/Markdown 已同步纠正。第 4 题明确标为假设，避免暗示原文首轮 QA 已通过。
