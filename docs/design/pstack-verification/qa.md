# pstack Verification · 制作方验收

## 本轮目标

按 article-distillation 标准入库流程，将 Lauren Tan 的《The Complete Guide to pstack Pt. 1》重组为“验证闭环 → 可复现控制工具 → Feature Map → 从闭环到规模化 → 证据边界”的渐进阅读路径。重点避免把 pstack 的工具清单当成主线，也不把作者自述的 PR 规模和 100–1000x 增益改写成普遍效果证明。

## 内容自检

- 已读取 Thread Navigator 展开的完整正文，覆盖系列背景、verification skill、控制 CLI、Cloud Agents、Feature Map、使用示例与维护建议。
- K1–K7 与原文位置、证据类型、条件和页面位置已写入 `content-plan.md`。
- 核心结论保持为“先闭合真实运行反馈，再扩大自主性与并行”，没有改写成“用了 pstack 就能获得 100–1000x 效率”。
- “每月 2,000 PR”“100–1000x”明确标为作者实践主张；正文没有提供对照组、统一质量指标或失败率，因此未作为效果证明。
- HTML、README、metadata 使用同一主标题、核心结论、章节与来源 URL。

## 图解预检

- `verification-loop`：Human 提供目标与边界；Agent 在“实现修改 → 真实运行 → 观察证据”之间执行；失败/不确定返回继续修正，成功输出可检查证据。反馈关系在几何上明确返回实现侧，而不是只用文字声称存在循环。
- `verification-stack`：Runtime / Debugging substrate → Control CLI → Verification Skill，表达依赖层级，不表示时间顺序。
- `feature-memory`：Codebase → 压缩/索引 → Feature Map → 按需查询 → Agent，明确 Feature Map 是紧凑索引而非第二事实源。
- `scale-ladder`：单 Agent 闭环 → 隔离并行 → 批量验证 → 自动触发，表示作者建议的能力依赖关系，不表示所有团队都必须经历这些阶段。
- 手机断点 CSS 将四类多列图重排为单列，并旋转方向标记；文字容器本身不旋转。

## 结构与浏览器验证

- `python3 .agents/skills/article-distillation/scripts/validate_article.py ai/agents/poteto/pstack-verification` 通过：20 个 ID、7 个目录标签、7 个 metadata outline 条目。
- `git diff --check` 通过，`metadata.json` 可由 `python3 -m json.tool` 正常解析。
- 首页已同步 AI Engineering 数量为 7，并新增 `Verification First` 分类入口；`Latest Distill` 已更新为本次文章。
- 使用本机 Google Chrome headless 实际渲染文章页 1440×960 与首页 1440×960，截图保存为 `desktop-1440.png` 与 `home-desktop-1440.png`。
- 桌面运行时测量：`innerWidth = 1440`，页面 `scrollWidth = 1425`；四个主图均位于 `left = 340 / right = 1120 / width = 780`，未越出视口；7 个目录 hash 均存在；7 个 `details` 初始全部关闭。
- Chrome headless 在本机直接传入 `--window-size=390,960` 时，实际 CSS viewport 被提升到 500px；运行时测量为 `innerWidth = 500`、`scrollWidth = 485`，四个主图位于 20–465px。对应截图保留为 `mobile-headless-500css.png`，不将其冒充“390 CSS px 已验证”。
- 尝试通过 CDP `Emulation.setDeviceMetricsOverride` 做真实 390px 设备模拟，但当前 headless target 返回 `Target does not support metrics override`，因此本轮没有足够证据宣称严格的 390px 浏览器验收已完成。

## 残余限制

- 已有 CSS 断点为 `max-width: 800px`，500px headless 渲染已经覆盖移动端重排规则；但仓库规范要求的严格 390px CSS viewport 仍缺浏览器证据，交付时应如实说明。
- 当前工具链能够保存截图、测量几何和 DOM 状态，但本轮模型侧无法直接视觉读取 Mac 工作区中的 PNG，因此不宣称完成了人工像素级视觉审查。
- 原文是个人工程实践文章，笔记只能判断作者提供了什么机制与案例，不能独立验证其团队产出倍数。
