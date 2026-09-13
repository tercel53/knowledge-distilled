# Delusional Goals · 制作方验收

## 本轮目标

按 article-distillation 标准入库流程，将 Dan Koe 的观点文章重组为“目标过滤器 → 打断线性优化 → 定向/删减/杠杆 → 证据边界”的渐进阅读路径。重点区分作者的注意力框架与文章没有来源支撑的神经科学强断言。

## 内容自检

- 已读取原文正文到 Step 3 与结尾；排除了评论、推广和页面导航。
- K1–K6 与原文位置、证据类型和限定已写入 content-plan.md。
- 核心结论没有改写为“目标越大越容易成功”；页面明确保留“过滤器不是预测器”和案例证据边界。
- neuroplasticity、flow、dopamine、serotonin、oxytocin、cortisol 等具体机制未作为已证实事实呈现。
- HTML、README、metadata 使用相同标题、核心结论、章节和来源。

## 图解预检

- filter-map：目标 → 注意力过滤 → 行动选择 → 结果与经验；箭头表示作者提出的影响关系，不表示充分条件。
- nonlinear-map：巨大/短期/自选/单一目标 → 判断当前方法是否足够 → 当前方法不够时重新搜索路径；“够用”的分支通过短说明保留，没有伪造成唯一流程。
- practice-map：定向 → 删减 → 杠杆；是作者方法整理，不代表实证效果。
- 手机布局全部改为纵向，关系方向保持不变。

## 浏览器与结构验证

- `validate_article.py life/behavior-change/delusional-goals` 通过：17 个 ID、6 个目录标签、6 个 metadata outline 条目。
- 使用本机 Google Chrome headless 实际渲染 1440×960 与 390×960，截图保存为 `desktop-1440.png`、`mobile-390.png`。
- Chrome DevTools Protocol 实测：桌面 `scrollWidth = innerWidth = 1440`，手机 `scrollWidth = innerWidth = 390`，均无横向溢出。
- 四个 figure 在桌面均位于 340–1120px（宽 780px）；手机均位于 20–370px（宽 350px），没有越出视口。
- 6 个目录 hash 均有目标；5 个 `details` 默认全部关闭；页面运行期间未捕获 JavaScript exception。
- 手机 CSS 将过滤链、三步实践与证据对照改为纵向；nonlinear-map 同样纵向排列，文字分支仍显式区分“当前方法够用/不够用”，没有把判断关系压成单一路径。

## 残余限制

- 当前自动化证据可确认实际渲染、几何范围、折叠/锚点与运行时错误；没有用户指定视觉参考图，因此不做像素级视觉对照，也不宣称像素级一致。
- Chrome headless 在 macOS 输出 `CVDisplayLinkCreateWithCGDisplay` 环境警告，但截图成功生成，页面未出现 JavaScript exception。
