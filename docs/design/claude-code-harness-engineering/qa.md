# Claude Code Harness Engineering · 标准入库验证

日期：2026-09-13。

## 档位判断

认知形态为工程实践 / 方法框架 + 导航型教程。按当前 article-distillation Skill 选择标准入库，不因标题含 Complete Guide 自动升级深度验收。本文没有高风险决策结论；主要风险是把五层职责、实施顺序和外部基准混成一套因果模型。

## 内容自检

- K1–K5 已写入 content-plan；主阅读路径保留五层职责、Memory 与 Hooks 的性质差异、作者建议的建设顺序，以及 +13.7 基准的归因边界。
- 明确区分“五层架构”与“Memory → Hooks → Tools → Permissions → Observability”的实施建议，避免把层号画成执行时序。
- LangChain 52.8% → 66.5% 只用于支持 Harness 改动会影响同一模型表现；不把 13.7 分归因给本文五层，也不声称装齐五层即可复现。
- 将 OpenAI Codex、Ghostty、开发者调查视为不同性质的实践材料，不把它们包装成同口径独立实验。
- 保留原文自我定位：这是 navigation hub / reading path，Layer 2/3 当时没有独立 deep-dive，因此不是完整生产配置规范。

## 静态与结构验证

- `validate_article.py`：通过，8 个 ID、6 个目录标签、6 个 metadata outline 条目。
- `git diff --check`：通过。
- 本地共享 CSS、文章 CSS、来源 URL、五层名称和响应式规则均存在。

## 浏览器与交互验证

- 使用本机 Chrome headless 实际渲染并保存 `browser/desktop-1440.png` 与 `browser/mobile-390.png`。
- 桌面探针视口 1365px：`scrollWidth = innerWidth = 1365`；手机 390px：`scrollWidth = innerWidth = 390`，无整页横向溢出。
- 6 个目录目标在两个视口均存在；3 道自测默认全部折叠，点击第一题后只有第一题展开，证明独立折叠正常。
- 五层卡片在 390px 下改为单列，均落在可用宽度内。
- 首次移动端检查发现建设顺序箭头通过 `rotate(90deg)` 旋转后形成约 26×350px 的包围盒，会跨越相邻步骤。已改为固定高度 24px 的向下箭头，并复验确认箭头不再与前后节点重叠。
- 页面共享 CSS 与文章 CSS 均返回 200；仅浏览器默认请求的 `favicon.ico` 返回 404，不影响文章内容与交互。
- 修复后再次运行 `validate_article.py` 与 `git diff --check`，均通过。

## 最终状态

标准入库验证通过。内容、证据边界、结构、桌面/手机响应式及自测交互均已有制作方证据；没有触发需要独立 Reader / Evaluator 的高风险问题。浏览器 QA 实际发现并修复了 1 个移动端关系表达问题，说明标准入库保留浏览器自检是必要的，而无需把所有文章升级为深度验收。
