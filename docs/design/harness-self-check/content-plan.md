# Harness 静态自评试点内容计划

## 范围

2026-09-12：增加初读定位、重要省略说明与静态自评；保留总览及三张机制图。补足规则检查正文的修正与重查说明，Markdown 同步条件与边界。发布后不调用 AI，不记录答题状态。

主线：人建设知识入口、规则检查和观察反馈环境，支撑 Agent 交付；人的判断、持续维护和特定实验条件仍然存在。

## 理解点、证据与题目

原文：<https://openai.com/index/harness-engineering/>，Ryan Lopopolo，2026-02-11。核对正文而非导航摘要；以下使用章节名定位，不假造网页锚点。

| 理解点 | 机制与依据 | 正文解释位置 | 自评题 |
| --- | --- | --- | --- |
| 知识存在不等于可用 | 短入口连接结构化知识，供任务查找；原文 We made repository knowledge the system of record、Agent legibility is the goal | practice-understand | check-knowledge |
| 文档不等于执行约束 | 检查发现违规并提供修正反馈，约束边界而允许实现自由；原文 Enforcing architecture and taste | practice-constrain | check-rules |
| 修改完成不等于验证完成 | 开放观察能力，让结果进入修复与验证循环；原文 Increasing application legibility、Increasing levels of autonomy | practice-verify | check-feedback |
| 局部经验不能普遍外推 | 环境投入、人的职责、持续维护、长期未知；原文 We started with an empty git repository、What “agent-generated” actually means、Entropy and garbage collection、What we’re still learning | boundaries，辅以 chapter-1、2、8、10、11 | check-boundary |

第 3 题为明确标示的假设场景，不冒充作者案例。各题答案区只对照已有解释；第 2 题所需的检查边界、修正及重查已补在主阅读路径。

## 内容安排

初读定位放在标题下，补足 Harness 含义与实践报告类型。省略说明指出未展开目录布局、工具接线和全部实验数据；按原文章节回查。自评在条件与边界后、原文章节索引前。答案分别折叠，问题始终可见。详细实现仍后置，不增加固定应用或复习板块。

## 验收边界

逐题核对依据、材料可回答性、HTML/Markdown 一致性；浏览器检查桌面和 390px 折叠、键盘、回查及溢出。图解结构未改，不开展历史参考图重新设计或声称像素级一致。真实读者理解速度、长期掌握效果不在本次验证范围。
