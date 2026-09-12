# Codex 作为平台：基于开放 Agent Harness 构建

英文原标题：Codex as a platform: build on the open agent harness

不要把工作迁进一个通用聊天框。让 Codex 进入用户已有的业务界面，在应用给出的上下文、工具与审批边界内完成工作。

来源：[OpenAI 原文](https://developers.openai.com/blog/codex-as-a-platform)

Nicolas Bonamy、Derrick Choi · 发布 2026-08-19 · 整理 2026-09-12

[打开 HTML 阅读版](./index.html)

## 一句话结论

**Codex 提供执行内核，业务应用提供工作现场。**

Codex Harness 负责让 Agent 持续理解、行动和反馈；业务应用继续负责用户界面、业务上下文、工具、权限与最终控制。两者结合，才构成面向具体工作的 Agent 产品。

“执行内核 / 工作现场”是对原文职责关系的阅读归纳，不是作者给出的产品术语。

## 系统怎样工作

完整流程从用户正在处理的业务对象开始，经过 Agent 调查与人工审批，最后回到业务记录：

1. **现有业务界面给出工作对象**：用户在看板、编辑器、队列、地图或记录页选择当前对象。
2. **应用注入业务上下文**：把当前对象、历史、规则和目标交给 Agent，用户不必从空白提示重新描述现场。
3. **Codex 运行 Agent 循环**：持续理解任务、维护状态、推理、调用受限工具并观察结果；失败或获得新信息后继续执行。
4. **应用自有工具连接真实业务**：MCP 服务提供最新数据和可执行动作，Codex 调查并解释选项。
5. **有后果的写操作交给人决定**：未批准则保持原记录；批准后才执行写入。
6. **结果回到原来的业务界面**：应用刷新系统记录，用户看到新状态并继续掌控工作。

职责边界由此变得清楚：

- **业务应用**：界面、上下文、工具、权限和系统记录。
- **Codex**：会话状态、推理、工具交互、流式进度、沙箱与跨轮执行。
- **人**：审阅建议，批准有后果的动作。

## 为什么不是通用聊天框

用户理解工作通常依赖看板、时间线、地图、文档或系统记录。通用聊天框要求用户重新描述这些现场信息，也容易割裂原有权限与控制流程。

Agent 进入既有产品后，界面可以直接告诉它用户正在看什么，应用可以提供正确的工具，并为用户保留审阅下一步的位置。结果也继续写回原来的记录系统。

开放 Harness 的额外价值，是开发者能够检查应用与模型之间的执行层，并按产品需要调整集成。

原文引用 ARC-AGI-3 例证：保留推理与上下文压缩使 GPT-5.6 Sol 得分从 13.3% 提升到 38.3%，输出 token 同时减少到原来的六分之一。该结果说明 Harness 设计会影响表现，但不能直接外推到所有业务任务。

## 如何选择接入方式

1. **`codex exec`**：适合脚本、CI 任务或一次性后台工作；运行有界、非交互的 Agent 工作流并返回结构化输出。
2. **Codex SDK**：适合应用代码启动、续接或流式接收 Codex 任务。
3. **Codex app-server**：适合 Agent 成为产品本身的一部分，由应用直接控制会话、事件、中断、工具和审批体验。

这是交互方式和控制程度的选择，不是能力排名，也不是按任务耗时划分。

## Relay 如何验证这套结构

Relay 是基于 app-server 的运单运营示例：

1. 用户在看板选择异常运单，点击“比较恢复方案”。
2. 应用提供相关上下文，Codex 通过 MCP 获取最新运营数据。
3. Agent 比较选项并解释建议，此时可以保持只读。
4. 重新订舱属于有后果的写操作：未批准则不写入，批准后才执行。
5. 应用刷新运单记录，用户从原来的界面看到新状态。

Relay 使用虚构的种子数据。它验证的是集成模式，不是物流业务效果。

## 证据与边界

- GitHub 与 JetBrains 把 Codex 带入既有 IDE 工作流。
- Cisco 在 Cisco Cloud Control 的 App Builder 中使用 Codex SDK。
- Thrive Holdings 与 Crete 的税务准备试点处理 7,000 份申报，并将准备时间缩短约三分之一。

前两个是采用案例，税务数字来自单个试点；它们不是受控、普遍化的效果证明。

OpenAI 开源的是 CLI、app-server、SDK 所构成的 Harness 与集成面，模型访问和托管服务仍然分离。运行位置、工具权限、审批规则、可观测方式以及记录写入仍由宿主应用治理。调查—建议—批准—执行的结构可以迁移，但具体业务规则不能照搬。

## 自测：我理解了吗？

先用自己的话回答，再按需展开参考答案。重点对照含义和依据，不必逐字一致；你可以理解作者后仍持不同意见。

### 1. 为什么把 Codex 嵌入业务看板后，应用仍需要提供当前对象、业务上下文和工具？

<details>
<summary>展开参考答案与对照要点</summary>

**参考解释：**Codex 提供持续推理、维护状态和调用工具的执行循环，应用则知道用户正在处理什么，并掌握业务数据、权限与记录。把两者连接起来，Agent 才能围绕当前工作调查，结果也能回到原界面。

**对照要点：**是否区分执行循环与业务现场，并说明上下文和结果如何衔接。

**容易误解：**接入开放 Harness 不等于业务规则自动齐备，也不表示模型访问和托管服务一并开源。

**回查：**[HTML · 系统怎样工作](./index.html#system) · [原文依据](https://developers.openai.com/blog/codex-as-a-platform)（章节：The reusable part is the agent loop；An open harness developers can inspect and adapt；Build software around the workflow）。

</details>

### 2. 在 Relay 示例中，Agent 已比较方案并建议重新订舱，但用户尚未批准。它此时能直接改写运单吗？

<details>
<summary>展开参考答案与对照要点</summary>

**参考解释：**不能。调查数据、解释建议和改写记录是不同阶段；重新订舱是需要批准的写操作。未批准就保留原记录，批准后才调用应用工具写入，并由应用刷新业务视图。

**对照要点：**是否保留调查、批准、执行和记录回流之间的边界。

**容易误解：**建议看起来合理不等于已获批准；读取运营数据也不能被当成写入授权。

**回查：**[HTML · Relay 示例](./index.html#relay) · [原文依据](https://developers.openai.com/blog/codex-as-a-platform)（章节：Example: Relay）。

</details>

### 3. 假设任务只是 CI 中的一次有界后台处理；另一个产品却需要持续会话、中断和审批交互。为什么不应仅按运行时长选同一种接入方式？

<details>
<summary>展开参考答案与对照要点</summary>

**参考解释：**前者可考虑 codex exec，后者更符合 app-server 对产品生命周期和交互的直接控制。SDK 适合应用代码启动、续接或接收任务流。选择依据是交互方式与控制需求，不能把三者当成耗时档位或能力排名。

**对照要点：**是否把场景要求对应到集成层，并解释选择理由。

**容易误解：**不是凡耗时长就必须用 app-server；短任务也可能需要产品内审批。

**回查：**[HTML · 接入方式](./index.html#layers) · [原文依据](https://developers.openai.com/blog/codex-as-a-platform)（章节：Choose the right integration layer）。

</details>

### 4. Relay 跑通运单恢复流程，是否就证明相同方案能在真实物流业务中稳定提高效率？

<details>
<summary>展开参考答案与对照要点</summary>

**参考解释：**不能。Relay 使用虚构种子数据，展示的是上下文、工具、审批和记录回流的集成模式。真实业务的规则、风险和效果仍需验证；其他采用案例或单个试点也不能替所有任务提供效果保证。

**对照要点：**是否区分集成示例、局部实践和普遍效果证据。

**容易误解：**无法直接外推不代表模式没有参考价值；应迁移职责关系，而不是照搬业务规则。

**回查：**[HTML · 证据与边界](./index.html#evidence) · [原文依据](https://developers.openai.com/blog/codex-as-a-platform)（章节：Example: Relay；What developers are building）。

</details>

## 原文定位

- **The reusable part is the agent loop**：Harness 如何管理状态、工具、边界、审批和跨轮工作。
- **An open harness developers can inspect and adapt**：开放代码的价值、产品可控制的部分，以及 Harness 与模型/托管服务的边界。
- **Choose the right integration layer**：`codex exec`、Codex SDK 与 app-server 的适用场景。
- **Build software around the workflow / Example: Relay**：专用界面的作用，以及调查、建议、批准、执行和刷新记录的完整回路。
- **What developers are building / Build beyond the obvious**：公开案例，以及增强现有工作界面而非用聊天框替代它的结论。

HTML 阅读版的系统总图为依据原文制作的可编辑阅读图解，不是 OpenAI 原图复刻。
