# Knowledge Distilled 仓库落地

以下路径均相对仓库根目录。先定位当前仓库，不依赖某台机器的绝对路径。

## 现有结构

- 规范：AGENTS.md。
- 首页与导航：index.html。
- 共享视觉样式：assets/css/style.css。
- 图标与许可证：assets/icons/。
- 文章示例：ai/agents/openai/harness-engineering/。
- 视觉验收：docs/design/<主题>/。

分类路径沿仓库现有结构选择，不把所有新文章都放进 OpenAI 或 agents 目录。复用首页视觉，不重建整个站点。templates/article.html 是旧模板，使用前核对；若其结构与本 skill 的递进阅读方式冲突，改用当前文章的组织方式，不能把旧的八段式内容重新带回页面。

## 文章产物

通常维护：
- index.html：阅读页及来源入口。
- README.md：相同核心内容的 Markdown 版本。
- metadata.json：来源、时间、分类和可追溯大纲。
- 局部 CSS、JavaScript 或图形资源：仅在需要时增加。

保留已有元数据字段并更新实际含义。新文章至少记录标题、来源名称、source_url、language、status；作者、发布日期确认后记录，未知时不猜测。learned_date 使用实际整理日期。outline 根据实际核心章节生成；只有页面使用图解时才添加对应 visuals 等扩展字段。

不要从示例复制作者、日期、原文标题、固定章节数、哈希或未经确认的实验数据。图解是阅读归纳时显式注明。

## 运行与验证

本站为静态页面，无需引入打包器。复用已在运行的服务；需要启动时，从仓库根目录运行：

    python3 -m http.server 8000 --bind 127.0.0.1

端口被占用时先检查现有服务是否可用，不随意终止其他进程。浏览器打开目标文章，按 AGENTS.md 检查桌面与 390px 手机布局；新增复杂断点时检查附近宽度。

核对文件与链接时：
- 确认内部 ID 唯一、hash 目标存在、图片及本地样式脚本存在。
- 检查资源路径时去除查询串和片段，如 note.css?v=2。
- JSON 能解析不代表内容一致；对照 outline 与 HTML 中的章节，图示元数据与实际图。
- 目录链接文字与目标章节的眉题默认逐字一致；metadata.outline 的标题对应目标章节主标题。不要依赖人工肉眼发现近义词漂移。
- 检查删掉的板块没有遗留失效按钮、空 DOM 查询或过时的 Markdown 说明。
- git diff --check 只检查补丁格式；不能代替浏览器和内容验收。

新建或重构文章后，从仓库根目录运行：

    python3 .agents/skills/article-distillation/scripts/validate_article.py <文章目录>

该检查覆盖 HTML 内部 ID、页内目标、目录/眉题一致性、metadata 大纲与本地资源。若文章有意使用另一套导航分类，可在实现与验收记录中说明理由，人工核对后使用 `--allow-label-differences`；不要为了绕过检查悄悄改动脚本或跳过失败项。

若新增或更新首页入口，摘要须与文章核心结论一致。预览、截图和验收记录不等于已发布到 GitHub Pages。

## 可参考的已完成实例

- ai/agents/openai/harness-engineering/index.html：观点、机制、实践、边界和折叠章节。
- ai/agents/openai/harness-engineering/diagrams.css：可编辑总览与局部图形的样式。
- ai/agents/openai/harness-engineering/note.js：章节深链接展开及目录定位。
- docs/design/harness-visual/qa.md：图形优先版本的验收记录。

仅按需读取这些文件，借鉴方法而非复制整篇内容。docs/design/harness/ 等更早记录是历史设计，不能用来覆盖后来确认的用户偏好。
