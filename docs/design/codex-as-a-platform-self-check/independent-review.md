# Codex as a platform 自测独立验收

## 第一阶段：默认正文盲读

仅浏览当前文章默认正文，四题答案全部保持折叠。未读取源码、Markdown、原文、内容计划、旧验收或历史。

页面主线复述：Codex Harness 管理通用理解、推理、调用工具和观察结果的循环；业务应用提供用户选中的工作对象、上下文、工具、权限和记录。调查提出建议后，涉及有后果的写操作要由人批准，再回到业务界面刷新记录。接入选择依据交互与生命周期控制需求。Relay 为虚构数据示例，只证明集成模式。

### 原始回答（展开答案前保存，不后改）

1. Harness 并不知道具体业务现场。应用需要告诉它用户当前处理的对象、历史和目标，并提供读写该业务所需工具和权限；Harness 才能在这组边界内推理、调用工具、返回结果。嵌入看板本身不等于已接通所有业务数据。
2. 不能直接改写。可以继续只读调查和解释方案，但重新订舱是有后果的写操作，须等待用户批准；未批准保持原记录，批准后 MCP 执行动作并刷新界面。
3. 接入方式按所需交互与控制程度区分。一次有界、非交互的 CI 处理可用 codex exec；需要持续会话、中断和审批的产品可选 app-server 直接管理生命周期。SDK 适合程序化启动、续接与流式接收。运行多久并不是这个分类的依据。
4. 不能。Relay 使用虚构种子数据，跑通的是调查、建议、批准、执行、刷新业务记录的集成结构；真实物流的效率与稳定性还需要真实数据、权限与风险规则以及实际运行证据。单个其他行业试点也不能替代此验证。

### 材料缺口

四题所需机制与边界均在默认正文中可找到，未发现必须先展开答案才能回答的核心知识。第 4 题补充的真实运行验证需求是我基于“虚构种子数据”和“不是物流业务效果”的推论，尚待第二阶段确认参考答案是否明确区分此性质。

第二阶段待执行：来源与 HTML/Markdown 同步、实际桌面/390px 截图、独立展开、键盘、回查及无 JavaScript 检查。

## 第二阶段：忠实性与实现核对

日期：2026-09-12。定向验收本轮新增自测；未重做未变更图解的参考图保真。阅读材料：文章 index.html、README.md、metadata.json，适用的 note.js，共享 assets/css/self-check.css，本目录 content-plan.md，以及[完整原文](https://developers.openai.com/blog/codex-as-a-platform)。

### 被验版本（SHA-256）

- `ai/agents/openai/codex-as-a-platform/index.html`：`be14642e4bfb602d1e7f0e691329b4104d31fe028c9f59ec70a5fa1f5c4e8063`
- `ai/agents/openai/codex-as-a-platform/README.md`：`5be57c9adfe309c796109bca646ddba9bd0ee8ca4d314be41af99dfa1330d74b`
- `ai/agents/openai/codex-as-a-platform/metadata.json`：`cc9c54113c21e401c298e202d7fedc9b843d76e0ac48ccb194659c01bbc2ca83`

### 内容与同步

Q1 职责划分；Q2 审批；Q3 接入层选择；Q4 虚构示例的证据边界。原文章节与每题标注相符。Q4 的“真实效果仍需验证”属于从证据范围得出的谨慎推论，未冒充原文实测。 第一阶段原始回答与展开答案含义吻合，没有发现需从答案区首次学习的必需机制。四题均具备参考解释、对照要点、容易误解与笔记/原文回查。逐项核对 HTML 的 12 段解释/对照/误解与 Markdown 完全一致；四题题目与回查目的地一致。metadata 含自测条目并明确非原文问答。

### 实际浏览器检查

- 桌面 1280×720、手机 390×844；手机实际 innerWidth 与文档 scrollWidth 均为 390。自测文字自然换行，未见横向溢出或遮挡。
- 默认四题问题直接可见，四个答案初始关闭；Enter 打开第一题、Space 打开第二题后状态为 `[true, true, false, false]`，证明独立折叠。焦点轮廓可见。
- 桌面笔记回查以键盘 Enter 激活，确认导航至正文并看到目标区；原文 URL 已单独打开核实，章节标注匹配；不是将本地索引冒充原文。
- 禁用脚本服务响应头经独立读取确认为 `Content-Security-Policy: script-src 'none'`；手机实测初始折叠、键盘展开与笔记回查均可用。
- HTML 使用原生 details/summary，无自测表单、提交、成绩、进度、个人状态或 AI 接口。

### 截图证据

- [桌面默认](review/desktop-collapsed.png)、[桌面展开与焦点](review/desktop-expanded.png)、[桌面回查](review/desktop-backlink.png)。
- [390px 默认](review/mobile-collapsed.png)、[390px 展开](review/mobile-expanded.png)。
- [390px 无脚本展开](review/mobile-nojs-expanded.png)、[390px 无脚本回查](review/mobile-nojs-backlink.png)。截图仅用于受影响自测与回查检查；部分正文图超出视口，不据此宣称整图保真。

### 问题、限制与最终状态

未发现阻断或重要问题。本轮定向验收通过。未对 GitHub 线上 Markdown 渲染或全量图解保真作运行验证；Markdown 已检查原生折叠语义和内容同步。没有产品修正，因此无修正复验记录。此验收只说明制作质量，不证明真实读者已掌握知识。
