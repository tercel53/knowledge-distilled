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

是否需要 Evaluator 不是一个固定答案：任务处在模型的可靠范围内时，评估者带来的价值可能低于成本；任务接近或超出能力边界时，独立评估仍能发现关键缺口。维护 Harness 时，应阅读真实运行记录，找出模型判断与人工判断的分歧，然后一次只移除一个组件并检查最终影响。

依据：原文 **Iterating on the harness** 与 **Removing the sprint construct**。

## 条件与边界

- 独立 Evaluator 也会放宽标准或只做表面测试，需要结合日志和人工判断持续校准。
- 达到最低通过线不等于测试充分；深层交互和未探索的功能仍可能漏检。
- Playwright 只能覆盖它可以观察和操作的信号；Claude 无法听见音乐，因此很难可靠评价 DAW 的音乐质量。
- Planner、Evaluator、重置和 sprint 都增加成本，必须用当前模型、当前任务上的真实增益证明其必要性。

## HTML 图解阅读索引

- [三种职责形成反馈闭环](index.html#thesis-caption)
- [主观质量的评分与迭代](index.html#grading-caption)
- [产品方案、验收约定、构建与 QA 的信息流](index.html#architecture-caption)
- [Harness 随模型能力演化](index.html#evolution-caption)
