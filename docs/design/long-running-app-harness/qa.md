# 长时应用开发 Harness 笔记验收

日期：2026-09-12

## 范围与来源

本轮蒸馏 Anthropic 文章 [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)，作者 Prithvi Rajasekaran，发布于 2026-03-24。读取文章正文、表格、案例限制与 Appendix 说明；导航、newsletter 等页面模块未作为论据。

没有用户指定的视觉参考。页面中的职责闭环、评分循环、第一版全栈架构和模型演化图均为可编辑 HTML/CSS 阅读图解，不是 Anthropic 原图复刻，也不作为像素级还原任务。

## 内容与证据对应

| 归纳观点 | 机制关系 | 原文位置 | 条件与限制 |
| --- | --- | --- | --- |
| 长时自主编码需要可检查的外部反馈 | 简短需求先整理成完整产品方案，再通过本轮验收约定转化为可测行为；独立 Evaluator 操作运行中的应用并反馈 | 引言；The architecture | 是作者的 Harness 经验，不是所有任务的固定架构 |
| 长上下文失稳与自我评估过于宽松是两类不同问题 | 重置缓解特定模型的长程失稳；职责分离让严格评估更容易校准 | Why naive implementations fall short | 分离不自动带来严格判断；重置增加复杂度、token 和延迟 |
| 主观设计可以沿明确原则改进 | 四项标准、少量带评分示例、Playwright 操作页面、5–15 轮反馈 | Frontend design: making subjective quality gradable | 美感不能被分数穷尽，结果不一定逐轮改善，措辞会影响风格 |
| Planner、Generator、Evaluator 分别补足方案、执行与验证 | Sprint 前共同确认本轮验收约定；构建后按最低通过线验收；通过文件交换信息 | Scaling to full-stack coding / The architecture | 第一版架构使用 sprint；后续 Opus 4.6 版本已移除 |
| Harness 以高成本换取案例中的可用性提升 | 游戏制作器 Full harness 对比 Solo；DAW 多轮 build/QA | Running the harness；Results from the updated harness | 少量案例、非受控基准，仍有未发现缺陷与产品直觉问题 |
| 模型升级会改变组件是否仍有必要 | 逐个移除组件并观察结果；4.6 可以取消 sprint，Evaluator 主要在任务接近模型能力边界时提供价值 | Iterating on the harness；Removing the sprint construct | 删除项与具体模型、任务有关，不能直接外推 |

## 语义验收

- 总览图用包含关系表示三种职责同属 Harness，用底部返回线表示评估反馈回到生成；输入、输出箭头只表示信息流，不承诺一次通过。
- 问题诊断将“长上下文失稳”与“自评宽松”并列，分别对应重置/交接和独立评估；没有画成互为因果。
- 评分图左侧是共同的评价标准，右侧是生成—操作运行中页面—反馈问题—打磨/转向循环；默认状态即可看出反馈机制。折叠内容只补案例和限制。
- 架构图把完整产品方案、编码前的本轮验收约定、运行中的应用与 QA 分成三个区域；失败返回和通过出口都有文字标注。手机端纵排后，区域和职责标签仍保留，未把 Planner、Generator、Evaluator 误写成产品运行步骤。
- 模型演化图按原文实验时间排列；删除线只表示作者在后续版本移除的支撑。图注明确不代表所有团队都应删除。
- 两个案例的数值保留模型、时长和 token 成本条件；页面明确标注为经验报告，未将观察改写成普遍因果结论。

## 浏览器与交互验收

- [桌面整页 1440px](desktop.png)：Chrome 实际渲染，`scrollWidth = innerWidth = 1440`；页面引用的 CSS/JS 均成功加载，无运行时异常。
- [手机整页 390px](mobile.png)：Chrome 模拟 390 × 844 视口后的全页截图，`scrollWidth = innerWidth = 390`；页面引用的 CSS/JS 均成功加载，无运行时异常。
- [800px](800.png) 与 [801px](801.png)：检查响应式断点两侧，最终均无横向溢出。
- [桌面总览](overview-desktop.png)、[桌面架构图](architecture-desktop.png)、[手机架构图](architecture-mobile.png)、[手机模型演化图](evolution-mobile.png) 用于逐项检查节点、箭头、边界、字号和重排。
- 两个 `details` 控件可点击展开；`summary` 可获得键盘焦点。页面标题、返回首页链接、页内 hash 目标与本地样式脚本均存在。
- HTML 中 19 个 ID 唯一；Markdown、HTML 和 metadata 的标题、作者、日期、核心结论、章节与来源一致。metadata 可被 `jq` 解析。

## 修正与残余限制

首轮 801px 检查发现总览图最小列宽使页面横向溢出 110px。已将 801–1150px 的总览改为纵向输入/输出，保留 Harness 内三职责并列，并重新截图；修正后 `scrollWidth = innerWidth = 801`。对应组件截图为 [overview-801.png](overview-801.png)。

未进行跨浏览器覆盖，也未复现作者的代码、应用和评分实验。图中的 DAW 阶段条按原文报告时长约为 Planner 2%、Build 87%、QA 11%，用于显示耗时重心，不代表精密性能测量。

## 中文表达校订

根据用户反馈，对整篇页面做第二轮语言检查，并同步修改 HTML、Markdown、metadata 和首页摘要。主要处理：

- 将“契约定义当前完成”改为“契约定义完成标准”。继续对照原文后，进一步把 `sprint contract` 解释为 Generator 与 Evaluator 在编码前共同确认的“本轮验收约定”。
- 删除“朴素长跑”“自产自评”“更深的可用性”“趋于平台”等需要二次理解或带有直译痕迹的表达。
- 把省略关系的短语还原为完整语义。对照原文的上下文，将 `full product spec` 译为包含产品背景、功能范围、用户故事和总体技术方案的“完整产品方案文档”，将 `running application` 表述为“运行中的应用”。
- 将“承重组件”“能力边缘”等抽象说法改为“组件是否仍有必要”“任务是否接近模型能力边界”。
- 改写图中短标签与图注，使桌面和手机视图采用同一套自然中文。

校订后重新渲染全部验收截图。Chrome 检查 390、800、801、1440px，四个宽度均满足 `scrollWidth = innerWidth`；CSS/JS 无加载失败或运行时异常。目视检查总览、全栈架构和模型演化图，增长后的文字没有造成遮挡、穿线或难以辨认的缩放。
