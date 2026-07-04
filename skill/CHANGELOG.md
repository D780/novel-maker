# 变更日志

## v2.3.0 (2026-07-04)

### 核心架构变更

- **Sub-Agent 调度机制**：agent.md 从工具定义重构为 Sub-Agent 合同，协调者统一通过 Task 工具调度，sub-agent 不切换角色、不发起新 sub-agent
- **角色声明前置**：SKILL.md 开头声明 AI 角色为协调者，强制规则改为"你是协调者"
- **Task 工具调用模板**：coordinator.md 伪代码改为实际 Task 工具参数模板（description/query/subagent_type/response_language）
- **协调者评估检查点**：字数检查、红线自检、P0/P1 判定均由协调者在主 session 评估

### 新增功能

- **TodoWrite 待办管理**：协调者每次流程开始时主动创建结构化待办列表，按步骤生成、完成后标记 completed
- **自动版本检查**：每日首次/间隔5小时检查 npm 新版本，发现新版时 AskUserQuestion 是否升级
- **系统/金手指角色支持**：character-profile.md 新增"系统/金手指档案"章节（系统等级/功能/规则/人格/界面元素/成长记录），chapter-complete.md 新增检测和更新规则
- **Truth-File 迁移机制**：技能升级后自动检测缺失的 truth-file 并从模板创建，含迁移状态记录和回填脚本支持
- **数据流规则**：写手只写入 temp/、审计师只审查 temp/、复盘师归档到 novel/ 后清理

### 改进

- **Truth-File 更新强化**：chapter-complete.md 加入每个 truth-file 的模板引用和详细更新字段，复盘师按模板结构更新
- **Hook 引用完善**：coordinator.md 引用 context-injection.md 和 intent-detection.md hooks
- **一致性检查通过 167 项**：validate.py 覆盖 Python 语法、Markdown 引用、角色定义、题材包、弧线模板、规则文件、模板文件、Hook 文件

---

## v2.2.0 (2026-06-26)

### 新增功能

- **智能查询系统**：4种查询类型（角色/设定/剧情/伏笔），意图识别 + 自然语言支持
- **Hook 系统**：5个自动化 Hook（上下文注入/意图检测/章节完成/审查触发/总结触发）
- **Web UI 增强**：设置页面、项目管理、多项目切换、配置导出/导入
- **Token 优化脚本**：build_write_context.py（~45k/章）、pre_audit.py（~25k/章）、truth_diff.py（~40k/章）
- **技能验证脚本**：validate.py（137项检查，8个维度）

### 改进

- **Web UI 现代化**：采用智汇协同风格，暖色极简设计
- **快速操作按钮**：复制提示词到剪贴板，一键触发 Trae 对话
- **项目全面审查**：修复25处问题（版本号/引用/目录树/文档）
- **全部版本号统一到 v2.2.0**

---

## v2.1.0 (2026-06-25)

### 新增功能

- **反AI表达规则**：7层检测体系，60+常见AI-slop模式识别
- **风格锚点系统**：从最近5章提取句长分布、对话比例、高频词（style_anchor.py）
- **角色声音检查**：5维度检查（语言习惯/情感表达/知识边界/行为逻辑/关系互动）
- **5维度一致性检查**：时间线、人物关系、世界观、伏笔回收、能力等级
- **11个题材包**：修仙/都市/无限流/悬疑/历史/科幻/游戏/末世/西幻/武侠/言情
- **篇章弧线模板**：6种通用弧线 + 42种题材特定弧线
- **节奏可视化**：emoji标记 + 卷级热力图 + 多维度情绪统计（pacing_visualize.py）

---

## v2.0.0 (2026-06-25)

### 新增功能

- **剧情卡片 6 要素**：方向类型、剧情预演、优点分析、参考小说、预计章节数、偏离影响评估
- **角色语音卡**：确保角色对话区分度
- **场景规划卡**：确保场景描写丰富度
- **爽点密度追踪**：10类爽点、S1-S5强度、平台适配
- **编辑视角审查**：开篇吸引力、节奏曲线、角色商业价值
- **读者反馈模拟**：模拟读者评论、评论区诱导设计
- **真相文件扩展**：新增 emotional-arcs.md、subplot-board.md、timeline.md

### 改进

- **analyze.py 三合一脚本**：整合 chapter_info.py + style_check.py + hook_report.py
- **剧情卡片模板**：6 个走向全部展开完整结构
- **规划师 JSON 结构**：补充 preview、advantages、reference、deviation_impact 字段
- **复盘师总结频率**：统一为每章后/每5章后/每10章后/每50章后/每卷末
- **字数要求说明**：新增平台适配（番茄/起点/晋江）

### 文档整理

- **删除过时文件**：OPTIMIZATION-LOG.md（v1.6.0）
- **合并重复文档**：anti-ai-patterns.md + anti-ai-techniques.md → rules/anti-ai-expressions.md
- **删除冗余文件**：pacing-analysis.md、emotion-curve.md（已整合到 rhythm-system.md）
- **更新参考文档表**：从 22 个精简为 19 个
- **创建模板索引**：templates/INDEX.md

### 脚本更新

- **analyze.py**：实现三合一功能（single/style/batch 模式）
- **hook_report.py**：修复变量名拼写 bug

---

## v1.6.0 (2026-05)

### 优化内容

- 文档精简整合
- 脚本功能增强
- 模板优化
- 工作流优化

---

*完整变更历史请查看 Git 提交记录*
