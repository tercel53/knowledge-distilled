# 静态自评内容计划

日期：2026-09-12。仅新增自测、目录入口及同步 Markdown/metadata，保留原文主线与已认可图解。

原文：[来源](https://claude.com/blog/harnessing-claudes-intelligence)。题目以原文与当前笔记共同核对，假设情境不冒充作者案例。

| 题号 | 检查的问题 | 正文回查 | 原文依据 |
| --- | --- | --- | --- |
| 1 / check-filter | 任务只需要工具结果表中的一列，为什么让模型写代码先筛选再回传，会改变原来的编排方式？ | orchestration | 第 2 节 · Let Claude orchestrate its own actions |
| 2 / check-context | 假设应用预装了许多任务的完整指令，但当前只处理其中一类任务。按需加载 Skills 与清理旧内容、使用子代理分别解决什么问题？ | context | 第 2 节 · Let Claude manage its own context |
| 3 / check-boundary | 模型已经很会用 Bash，是否就可以取消应用中的专用工具和动作确认？ | boundaries | 第 3 节 · Use declarative tools for UX, observability, or security boundaries |
| 4 / check-upgrade | 某次升级后模型不再提前收尾，因此删除了旧的上下文重置。能否推断后续所有 Harness 组件都应该越少越好？ | limits | The future of agent harness design；第 3 节 |

答案仅核对上述已解释机制；自评独立折叠，无答题状态、提交或 AI 集成。原文入口采用已核实 URL 加章节名，不编造锚点。
