# Harnessing Claude’s intelligence 自测独立验收

## 第一阶段：默认正文盲读

仅浏览当前页面默认正文与图示文字；解释、原文定位详文与四题参考答案全部折叠。未读取原文、源码、Markdown、内容计划、其他验收或历史。

页面主线复述：Harness 的部分设计补偿旧模型的能力不足；能力改变后要重测设计理由。通用工具给模型组合行为的基础，随后可分别重测动作编排、当前上下文、跨窗口记忆的选择权。但成本、交互、安全等应用要求仍需环境承接。最后以旧上下文重置补偿失效的前后对照回到再次重测，而非一路删减。

### 原始回答（展开答案前保存，不后改）

1. 原来把整张结果表连同无关列带进模型上下文；新方式由模型编写筛选逻辑，在执行环境处理表格，只把所需一列送回上下文。因此模型拥有选择和编排权，处理数据与实际工具执行仍在环境中，减少不相关信息进入上下文。
2. Skills 先提供简介索引，按当前任务加载所需正文，避免预装少用指令持续占用上下文；上下文编辑移除过时内容；子代理通过独立窗口隔离其他工作。三者分别管理进入、离开、隔离，不是同一种扩容，也不必固定串行。
3. 不能据此一概取消。会用 Bash 是能力，应用仍有确认、呈现、审计、新旧检查等具体要求，专用工具与类型化参数可以承接这些边界；按动作需要落实，并不是每次动作都要全部检查。
4. 不能。该例证明特定旧问题消失后，对应补偿可能多余；下一轮升级仍要逐项检验设计理由。用于成本、交互、安全和任务支撑的部分可能仍必要，组件越少不是独立目标。

### 材料缺口

默认正文中的对照图、简短图注已足够回答四题。未发现答题必须依赖折叠解释的内容。问题未直接检验长期记忆，但现有四题覆盖主要选择权、上下文和应用边界，是否需增加覆盖留到第二阶段评估。

第二阶段待执行：来源与 HTML/Markdown 同步、实际桌面/390px 截图、独立展开、键盘、回查及无 JavaScript 检查。

## 第二阶段：忠实性与实现核对

日期：2026-09-12。定向验收本轮新增自测；未重做未变更图解的参考图保真。阅读材料：文章 index.html、README.md、metadata.json，适用的 note.js，共享 assets/css/self-check.css，本目录 content-plan.md，以及[完整原文](https://claude.com/blog/harnessing-claudes-intelligence)。

### 被验版本（SHA-256）

- `ai/agents/anthropic/harnessing-claudes-intelligence/index.html`：`660dffc6c863c760387e9045c98ac96d6646b2d95a63106cf9e611b7af5db9df`
- `ai/agents/anthropic/harnessing-claudes-intelligence/README.md`：`ce08d6215a4c0cfe3cd24bd732285c4496a512b484620dfad5c08c6b0d51841a`
- `ai/agents/anthropic/harnessing-claudes-intelligence/metadata.json`：`46fb3d1d3c42be9702412a3c2e7c2a39c06bd763b311954a972228681cff4e7d`

### 内容与同步

Q1 编排选择权；Q2 上下文进入/移除/隔离；Q3 应用动作边界；Q4 重测失效补偿。原文第 2、3 节及末节支持答案。长期记忆、缓存的细节未逐项出题，属于少量自评的覆盖范围，不是本轮缺陷。 第一阶段原始回答与展开答案含义吻合，没有发现需从答案区首次学习的必需机制。四题均具备参考解释、对照要点、容易误解与笔记/原文回查。逐项核对 HTML 的 12 段解释/对照/误解与 Markdown 完全一致；四题题目与回查目的地一致。metadata 含自测条目并明确非原文问答。

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
