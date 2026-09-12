# 面向长时应用开发的 Harness 设计

英文原标题：Harness design for long-running application development

来源：[Anthropic 原文](https://www.anthropic.com/engineering/harness-design-long-running-apps) · Prithvi Rajasekaran · 2026-03-24

整理日期：2026-09-12

## 核心结论

将规划、生成和评估分开；先约定怎样才算完成，再让评估者像用户一样操作运行中的应用，形成反馈闭环。模型升级后，还要逐项移除 Harness 组件，验证哪些仍有必要。

长时自主编码不应由同一个 Agent 一路生成并自我验收。Planner 把简短需求扩展成完整的产品方案文档，Generator 负责实现，Evaluator 则像用户一样操作运行中的应用，按照预先约定的标准验收并反馈问题，由此推动下一轮修复或调整方向。

## 为什么只让一个 Agent 长时间运行会失败？

原文观察到两类问题：

1. 随着上下文不断累积，模型可能逐渐失去连贯性；Sonnet 4.5 甚至会在认为自己接近上下文上限时提前结束工作。清空上下文，再用结构化交接文件把必要状态传给新的 Agent，可以缓解这个问题，但会增加编排复杂度、token 消耗和运行延迟。
2. 同一个 Agent 生成并评价自己的成果时，往往会放宽标准。把生成和评估交给不同 Agent，更容易单独把评估者调校得严格；但职责分离本身不够，仍需要明确标准、少量带评分示例和持续调参。

压缩和重置并不相同：压缩在同一会话内总结历史，保留连续性；重置提供干净上下文，依赖交接文件恢复状态。

依据：原文 **Why naive implementations fall short**。

## 如何评估主观质量？

作者先在前端设计中设置四项标准：设计质量、原创性、工艺和功能，并提高前两项权重。Generator 与 Evaluator 使用同一套标准；Evaluator 用 Playwright 导航、截图和操作真实页面，再给出逐项评价。Generator 根据评分趋势决定继续打磨，还是切换设计方向。

每次生成会迭代 5–15 轮，完整运行最长约四小时。结果整体上有所改善，但不保证每一轮都比上一轮更好；作者有时更喜欢中间轮次，方案复杂度也会随迭代增加。评估标准的措辞还会影响生成风格，因此评分并不是客观、中立的审美尺度。

依据：原文 **Frontend design: making subjective quality gradable**。

## 三 Agent 全栈 Harness

- **Planner**：把 1–4 句输入扩展成完整的产品方案文档，内容包括产品背景、功能范围、用户故事和总体技术方案；避免过早写死实现细节并影响后续工作。
- **Generator**：第一版按 sprint 推进，每次只实现一项功能，并在交给 QA 前自检。
- **Evaluator**：用 Playwright 像用户一样操作运行中的应用，检查 UI 功能、API 端点和数据库状态；再从功能范围与实现深度、功能可用性、视觉设计和代码质量四个方面评分。任一评分未达到最低通过线，这一 sprint 就判定为未通过，并返回具体反馈。

编码前，Generator 和 Evaluator 先协商 sprint contract，也就是共同确认本轮要做什么、怎样才算完成，直到双方达成一致。这一步将产品方案中的用户故事转化为可以验证的行为。不同角色通过文件交换产品方案、本轮验收约定和反馈。

依据：原文 **Scaling to full-stack coding / The architecture**。

## 两个案例提供了什么证据？

### 复古游戏制作器（Opus 4.5）

| 方式 | 时长 | token 成本 | 观察 |
| --- | ---: | ---: | --- |
| Solo | 20 分钟 | $9 | 界面能打开，但游戏模式无法正常操作 |
| Full harness | 6 小时 | $200 | 16 项功能、10 个 sprint，核心玩法可运行；仍有流程、碰撞和关卡问题 |

完整 Harness 的成本超过单 Agent 方案的 20 倍。Evaluator 能准确定位拖拽填充、删除条件和 API 路由顺序等缺陷，但操作流程、物理碰撞和关卡设计等问题仍然存在。

### 浏览器 DAW（Opus 4.6）

简化版 Harness 共运行 3 小时 50 分钟，token 成本为 $124.70。Generator 连续工作两小时以上；QA 仍发现录音只是占位功能、片段不能拖动、缩放或切分、效果器缺少可视化编辑等核心缺口。最终应用已经具备编排、混音、播放和 Agent 工具调用，但离专业级 DAW 仍有很大距离；Claude 不能真正听见音乐，也限制了它对音乐质量的评价。

证据边界：这是作者对少量构建案例的经验报告，不是受控基准；成本与效果不能外推为固定收益。

依据：原文 **Running the harness** 与 **Results from the updated harness**。

## Harness 为什么要随模型演化？

每个 Harness 组件都建立在一项关于模型能力的假设上：

- Sonnet 4.5：需要单功能构建、上下文重置和结构化交接，缓解长时间运行时的失稳问题。
- Opus 4.5：context anxiety 大幅减弱，自动压缩足以维持连续会话，因此去掉重置；保留 Planner、sprint 和每个 sprint 结束后的 QA。
- Opus 4.6：原生长程规划和代码审查更强，作者移除 sprint，改为连续完成整项构建，再通过 QA 反馈反复修正。

是否需要 Evaluator 不是一个固定答案：任务处在模型的可靠范围内时，评估者带来的价值可能低于成本；任务接近或超出能力边界时，独立评估仍能发现关键缺口。作者最初大幅简化 Harness 未能复现原有表现，也难以分辨哪些组件仍在发挥作用；随后改为一次只移除一个组件，观察最终结果。阅读真实运行记录、核对模型与人工判断的分歧，则用于持续校准评估者。

依据：原文 **Iterating on the harness** 与 **Removing the sprint construct**。

## 条件与边界

- 独立 Evaluator 也会放宽标准或只做表面测试，需要结合日志和人工判断持续校准。
- 达到最低通过线不等于测试充分；深层交互和未探索的功能仍可能漏检。
- Playwright 只能覆盖它可以观察和操作的信号；Claude 无法听见音乐，因此很难可靠评价 DAW 的音乐质量。
- Planner、Evaluator、重置和 sprint 都增加成本，必须用当前模型、当前任务上的真实增益证明其必要性。

## 自测：我理解了吗？

先用自己的话回答，再按需展开参考答案。重点对照含义和依据，不必逐字一致；你可以理解作者后仍持不同意见。

### 1. 已经有 Planner 写出的产品方案，为什么第一版 Harness 仍让 Generator 和 Evaluator 在编码前协商本轮验收约定？

<details>
<summary>展开参考答案与对照要点</summary>

**参考解释：**产品方案给出方向和范围，验收约定则把用户故事落实为本轮可验证的行为。生成者提出做什么、怎样验证，评估者检查是否符合方案，达成一致后再实现，减少做完后才争论完成标准的情况。

**对照要点：**是否区分产品方向与可验证行为，并说清双方为何在编码前对齐。

**容易误解：**这不要求 Planner 提前写死全部实现细节，也不意味着所有后续模型都要保留 sprint。

**回查：**[HTML · 三 Agent 架构](./index.html#architecture) · [原文依据](https://www.anthropic.com/engineering/harness-design-long-running-apps)（章节：Scaling to full-stack coding / The architecture；Removing the sprint construct）。

</details>

### 2. 假设一个独立 Evaluator 只看页面截图，认为“整体不错”就放行。仅仅与 Generator 分开，是否已经满足本文的评估思路？

<details>
<summary>展开参考答案与对照要点</summary>

**参考解释：**还没有。独立角色更容易单独校准判断，但仍需明确标准、示例和实际操作。评估者应像用户一样检查运行中的应用，给出具体缺陷供修复；只看截图无法证明交互可用，独立身份也不保证判断严格。

**对照要点：**是否同时说明职责分离、共同标准、实际操作和反馈的作用。

**容易误解：**评分或截图不能替代行为验证；达到通过线也不等于没有未覆盖的问题。

**回查：**[HTML · 评估的条件与边界](./index.html#boundaries) · [原文依据](https://www.anthropic.com/engineering/harness-design-long-running-apps)（章节：Why naive implementations fall short；Frontend design: making subjective quality gradable；Running the harness）。

</details>

### 3. 模型升级后连续开发能力变强，是否应一次性删掉重置、sprint 和 Evaluator？怎样判断？

<details>
<summary>展开参考答案与对照要点</summary>

**参考解释：**不应仅凭升级就全部删除。应逐项移除组件并观察最终影响，避免一次大改后无法判断原因；阅读运行记录、比较模型与人工判断，则有助于校准评估者。旧补偿可能失效，而接近模型能力边界的任务仍可能需要独立评估；保留与否要比较当前任务上的收益和成本。

**对照要点：**是否解释了逐项验证的目的，并保留任务能力边界。

**容易误解：**作者在特定版本取消某个组件，不是对所有项目的统一删减指令。

**回查：**[HTML · 随模型演化](./index.html#evolution) · [原文依据](https://www.anthropic.com/engineering/harness-design-long-running-apps)（章节：Iterating on the harness；Removing the sprint construct）。

</details>

### 4. 假设浏览器 DAW 已通过一轮 QA，能否据此认定它达到专业级音乐制作质量？

<details>
<summary>展开参考答案与对照要点</summary>

**参考解释：**不能。验收只覆盖实际检查过的行为和可观测信号，深层功能仍可能漏检；Claude 不能真正听见音乐，也限制了音乐质量判断。作者的少量案例说明部分能力改善，同时保留成本与功能缺口，不是专业质量的保证。

**对照要点：**是否区分界面与功能检查、听觉判断，以及实际测试覆盖范围。

**容易误解：**通过 QA 不等于全部功能完整，更不等于在所有任务中获得固定收益。

**回查：**[HTML · 条件与边界](./index.html#boundaries) · [原文依据](https://www.anthropic.com/engineering/harness-design-long-running-apps)（章节：Running the harness；Results from the updated harness）。

</details>

## HTML 图解阅读索引

- [三种职责形成反馈闭环](index.html#thesis-caption)
- [主观质量的评分与迭代](index.html#grading-caption)
- [产品方案、验收约定、构建与 QA 的信息流](index.html#architecture-caption)
- [Harness 随模型能力演化](index.html#evolution-caption)
