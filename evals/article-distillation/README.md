# 文章蒸馏效果评估工具

独立于被测 skill 的标准库 Python 工具。固定版本、案例与评分标准，调度隔离任务，冻结首版，匿名盲读，再核对原文。支持中断恢复和报告；不会自动宣称候选更好。

## 与文章验收的区别

文章独立验收仍是蒸馏 skill 的交付步骤。这里比较两个版本的首次可交付产物，允许通常自检，但在外部反馈之前冻结。后续验收修复不能覆盖首版；如需比较修复成本应另开运行并记录，不混入首次胜率。

## 运行

从仓库根目录执行。baseline 和 candidate 是完整 skill 目录，可使用历史版本导出的目录；旧试跑 zip 需先解压为目录。以下命令中的路径需替换成实际路径。

```sh
python3 evals/article-distillation/runner.py prepare \
  --baseline /path/to/baseline-skill \
  --candidate .agents/skills/article-distillation \
  --run-dir evals/article-distillation/runs/my-run \
  --cases approval-workflow --repeats 1
```

省略 `--cases` 运行全部五个案例；正式对比建议 `--repeats 3`，但必须在用户授权的工作量内运行。`--model` 记录期望模型/设置，执行后端负责实际执行；未明确时继承当前模型，报告不声称严格模型控制。

### 在支持 subAgent 的会话里执行

1. `next --run-dir <运行目录>` 领取一个任务，输出中含 prompt、cwd、output_dir、id。每个任务必须启动全新 subAgent，`fork_turns: "none"`，只传该 prompt；不得传主会话、版本身份或预期答案。可连续领取独立生成任务并行执行。
2. 任务完成后保存 receipt JSON，例如 `{"agent_id":"实际上下文标识","backend":"subAgent","usage":null}`。未知模型与用量不编造。
3. `complete --run-dir <运行目录> --job <id> --receipt <receipt.json>` 验证和冻结产物。重复调用不能覆盖已完成产物，生成者不能复用为评审。
4. 继续领取任务。两组生成完成后才开放盲读；盲读冻结后才开放原文、评分标准及评分任务。这里评分者采用新上下文，读取冻结的原始复述，不继承前一代理上下文。
5. `report --run-dir <运行目录>` 输出 JSON，并生成 report/report.md、summary.json、judgments.json。漏跑会明确列出，不能算通过。

没有新的 pending 任务但有 active 任务时应等待在途任务。中断后用 `next --run-dir <运行目录> --job <id>` 恢复原任务材料；先判断已有代理是否仍运行，不重复启动。worker 报错后保持 active，可修复未冻结输出再完成；已冻结材料不允许修改。复制采用临时目录再原子提交；状态保存中断后，同内容的冻结副本可继续登记，不覆盖首版。

### 独立进程后端

```sh
python3 evals/article-distillation/runner.py run \
  --run-dir evals/article-distillation/runs/my-run \
  --worker /absolute/path/to/agent-worker --its-options
```

运行器对每个任务启动一次 worker 进程，工作目录设为该任务 cwd。stdin 为 next 同样的 JSON；worker 调用所接模型/代理，在 output_dir 写产物，然后仅向 stdout 返回 receipt JSON（必须有唯一 agent_id），日志写 stderr。receipt 可以记录实际 model、reasoning、tools、backend 和 usage；未知填 null，不能把请求参数当作实际观测。worker 必须为每个任务创建全新模型上下文，并落实模型参数、工具范围及浏览器能力；仅启动新进程不足以证明模型上下文隔离。超时默认600秒，可用 `--timeout` 调整。命令参数通过数组传递，不执行 shell 拼接。

本工具不内置特定供应商的模型 SDK，也不会绕过登录或自行调用付费 API。当前会话可以使用上述 subAgent 桥接方式；普通终端全自动运行需要提供已配置的 worker。测试目录中的假 worker 仅用于运行器测试，不能产生语义评估结论。

一次运行只允许一个协调进程管理状态；多个独立代理可并行处理已领取任务。receipt 身份检查与读取范围依赖后端如实执行，不是操作系统安全沙箱。

## 输入与隔离

- cases/：固定正文、任务、范围和必需产物。合成正文不冒充研究。
- rubrics/：固定的通用尺度和案例评分要点。生成者不会收到这些文件。
- check_article.py：评估侧独立固定的结构检查器；不执行候选 skill 自带的校验脚本来给它自己打分。
- 每次 prepare 复制两个完整 skill、输入及评分标准，记录哈希；后续命令检验快照和已冻结产物是否被篡改。
- 每个生成任务只有自己的 skill、source.md 和输出目录。HTML 使用统一的独立静态环境，不读取现有文章或首页资产，避免历史笔记泄漏答案。生产仓库样式集成不在这组案例的覆盖范围内。
- 评审只收到匿名 A/B，不收到 skill 或映射。盲读阶段不收到原文和评分要点；第二阶段才提供。匿名只隐藏版本标识，正文风格仍可能暴露线索，不保证数学意义的盲化。
- 评估代码也固定：升级工具后继续旧运行会被拒绝，应改用该运行的 `control/suite/runner.py` 恢复和出报告。
- 原始状态及 worker receipt 可能含机器路径，仅放在忽略的 runs/ 或临时目录，不直接提交。报告与原始证据在清理机器路径后可保存到 docs/evals/。历史试跑记录保留原样。

## 结果如何解释

先看覆盖率、阻断问题和分维度退步，再看盲评胜负。report 将 plan/html、development/holdout 分组；inconclusive 不进入均值。结构校验失败单列，不由生成者悄悄修复。运行器只验证证据格式和截图文件存在，语义仍由独立评审判断。

- incomparable_conditions：生成者回执报告了不同模型、推理设置或工具，不能据此归因于 skill。未知条件如实标记 unknown。
- incomplete：缺任务或存在无法比较。
- regression_or_blocker：存在维度退步、候选阻断问题或候选结构失败，需要人工查看证据。
- candidate_favored_in_this_sample：完整的本次样本中更受偏好，不等于证明总体提升。
- no_demonstrated_improvement：本次未证明提升，可以是平局。

现有短合成案例覆盖历史失败类型，可能出现评分天花板。总体判断需更长、关系分散的固定正文，以及保留集和多次生成。评分标准改变后应重跑两个版本；不能把不同尺度的历史分数直接比较。已用于调参的保留案例应转为开发集，另补未见案例。

## 测试工具自身

```sh
python3 -m unittest discover -s evals/article-distillation/tests -v
```

测试不调用模型，检查隔离数据交接、阶段门槛、冻结防篡改、错误恢复、漏跑与分组，以及 worker 协议。它证明运行器行为，不证明 skill 效果。
