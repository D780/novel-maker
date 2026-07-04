# NovelMaker 变更日志

所有重要变更将记录在此文件中。

格式参考 [Keep a Changelog](https://keepachangelog.com/)。

## [Unreleased]

---

## [2.2.5] - 2026-07-04

### Changed
- 引入 Agent 唤起机制，使用 `[[role:xxx]]` 标记显式切换 6 角色
- 为每个角色文件增加"被唤起时的行为"规范
- 协调者增加完整流程模板和强制规则
- 临时文件路径统一迁移到 `.novel-maker/temp/`，并按章节区分命名
- reviewer 增加归档后清理临时草稿文件的规则

### Fixed
- 修复实际使用中无法唤起 sub-agent 执行多角色流程的问题
- 修复临时草稿文件路径不集中、不分章节的问题

---

## [2.2.4] - 2026-07-04

### Changed
- 强化技能执行严格性：每章/每5章/每10章/每幕固定检查清单
- 整合写作红线到 writer.md、constitution.md、SKILL.md
- 添加 truth-files 更新清单和规划同步机制
- 添加步骤交接摘要机制，确保步骤无缝衔接

### Added
- SKILL.md 增加脚本安装流程说明
- outline.md 增加"实际执行"列用于规划同步
- memory-system.md 简化 truth-files 更新规则

---

## [2.2.2] - 2026-07-04

### 新增
- **辅助脚本增强**：emotion_curve.py 可视化输出（ASCII曲线+热力图）、foreshadowing_tracker.py 自动回收建议、worldbuilding_checker.py 自动修复功能
- **世界观自动修复**：`--fix` 显示修复建议、`--apply` 执行修复、`--dry-run` 预览模式
- **伏笔回收建议**：5种伏笔类型模板，自动输出回收建议

### 修复
- worldbuilding_checker.py: `--dry-run` 参数无效、`replace()` 误替换、`chapter_facts` 未使用参数、`remaining_issues` 计算不准、重复追加段落、truth file 不支持 dry-run
- emotion_curve.py: 热力图中间层级不可见
- foreshadowing_tracker.py: suggestions 文本模式未输出

### 优化
- 完善 package.json 元数据（author/repository/homepage/bugs）
- README.md 添加 npm/downloads/stars 徽章
- `.npmignore` 修复 `__pycache__` 排除规则

---

## [2.2.1] - 2026-07-04

### 优化
- 完善项目元数据：GitHub 仓库链接、npm 徽章、author 信息
- `.npmignore` 更新 `__pycache__` 排除规则

---

## [2.2.0] - 2026-06-26

### 新增
- **智能查询系统**：4种查询类型（角色/设定/剧情/伏笔），query_engine.py
- **Hook 系统**：5个自动化 Hook（上下文注入/意图检测/章节完成/审查触发/总结触发）
- **Web UI 增强**：设置页面、项目管理、多项目切换
- **技能验证脚本**：validate.py（137项检查：脚本语法/文件引用/角色/题材包/弧线模板/规则/模板/Hook）
- **技能全面审查**：合并3个冗余反AI文件为1个，修复25处问题
- **Token 优化脚本**：build_write_context.py（~45k/章）、pre_audit.py（~25k/章）、truth_diff.py（~40k/章）

### 优化
- Web UI 采用智汇协同风格（暖色极简设计）
- 快速操作按钮（复制提示词到剪贴板）
- 明确一致性检查/角色语音的职责划分（rules=检查规则，references=执行流程）
- 全部版本号统一到 v2.2.0（package.json/SKILL.md/README.md/QUICK-REF.md）

---

## [2.1.0] - 2026-06-25

### 新增
- **反AI表达规则**：7层检测体系，60+常见AI-slop模式（rules/anti-ai-expressions.md）
- **风格锚点系统**：style_anchor.py（从最近5章提取句长分布、对话比例、高频词）
- **角色声音检查**：5维度检查（rules/character-voice.md）
- **5维度一致性检查**：时间线、人物关系、世界观、伏笔回收、能力等级（rules/consistency-check.md）
- **11个题材包**：修仙/都市/无限流/悬疑/历史/科幻/游戏/末世/西幻/武侠/言情
- **篇章弧线模板**：6种通用弧线 + 42种题材特定弧线
- **节奏可视化**：pacing_visualize.py（emoji标记+热力图+情绪统计）

---

## [2.0.0] - 2026-06

### 新增（架构重构）
- **6角色协作架构**：协调者 → 规划师 → 写手 → 审计师 → 修订师 → 复盘师
- `skill/agents/` 目录：6 个角色定义文件（coordinator/planner/writer/auditor/reviser/reviewer）
- **3 个新真相文件**（扩展至 8 个）：emotional-arcs.md、subplot-board.md、timeline.md
- **3 个新模板**：plot-card.md（剧情卡片）、character-voice.md（角色语音卡）、scene-plan.md（场景规划卡）
- `rules/anti-ai-expressions.md`：反AI表达规则（7层检测+去AI味技巧）
- `references/platform-rules.md`：平台适配规则（番茄/起点/晋江）
- `references/editorial-perspective.md`：编辑视角审查指南
- `references/sweet-spot-tracking.md`：爽点密度追踪系统
- `references/character-voice-card.md`：角色语音卡使用指南

### 优化
- 根目录 README.md 全面更新到 v2.0.0（6角色架构 + 新特性）
- INSTALL.md 目录结构补充至完整（24 references / 21 templates / 14 scripts）
- SKILL.md 指令体系完整化（7 核心 + 5 扩展 + 7 高级子指令）
- skill/README.md 重写为 v2.0 快速参考
- QUICK-REF.md 新增 6 角色协作流程图

### 设计文档
- 完整架构设计文档：`docs/superpowers/specs/2026-06-24-novel-maker-v2-architecture-redesign.md`
- 8 个关键架构决策：概念角色 / 简短协议 / 修订升级 / 复盘时机 / 用户决策点 / 上下文管理 / 失败恢复 / 协作模式

---

## [1.5.0] - 2026-05

### 新增
- 幕系统完善：6条分支走向（A主线/B危机/C支线/D缓冲/E回环/F颠覆）
- 偏离影响分析（🟢🟡🟠🔴四级）
- 大幕分段机制、幕大纲、AI推荐、可调章节数
- Python 预处理脚本：chapter_info.py（单章结构化提取）、volume_batch.py（卷级批量汇总）
- 每次写入后强制更新链：写作→审查→字数检查→更新大纲→更新记忆→摘要→进度
- 多 IDE 兼容支持（Trae/Claude/Cursor/Cline/Roo/Copilot/Continue/OpenCode/Windsurf）
- INSTALL.md 多 IDE 安装指南
- 3个新脚本：hook_report.py、consistency_scan.py、style_check.py

### 修复
- 字符提取过滤：修复代词+动词模式导致的噪音识别
- 工作流程整合：脚本在 /novel-maker write 和 /novel-maker act 时自动运行
- SKILL.md 指令层级统一（核心7个，扩展5个）
- .gitignore 增加各 IDE 规则目录排除

---

## [1.4.0] - 2026-05

### 新增
- 情绪标签系统：6大情绪标签对应不同节奏模板
- 黄金开篇锻造术：写第一章时自动生成3版开篇+避雷针检查
- 情绪曲线"压-小扬-压-爆"3章循环
- content-expansion.md：7种内容扩充技巧
- dialogue-writing.md：对话写作规范
- plot-structures.md：情节结构模板
- emotion-curve.md：情绪曲线系统
- golden-opening.md：黄金开篇参考文档
- Python字数检查脚本（check_wordcount.py）

### 优化
- 情绪曲线与节奏分析连接
- 统一init流程6问顺序
- 修正黄金开篇触发时机
- 去除重复内容

---

## [1.3.0] - 2026-05

### 重构
- 消除 SKILL.md 中的重复内容（指令速查表、工作流描述）
- 将详细工作流程移到 references/usage-guide.md，SKILL.md 中保留引用
- 将完整文风库内容移到 styles/author-styles.md，SKILL.md 中保留精简版

### 优化
- 文风库按 7 大流派分类组织（原 22 个文件平铺）
- SKILL.md 从 718 行精简至 363 行（约 50% 缩减）
- 更新 styles/author-styles.md 中文风文件的链接路径

### 新增
- 独立开源项目结构（skill/ 目录 + docs/ 文档）
- README.md（面向 GitHub 访问者）
- CONTRIBUTING.md（贡献指南）
- LICENSE（MIT 许可证）
- .gitignore（排除运行时数据）

---

## [1.2.0] - 2026-04

### 重构
- 三级指令体系：核心（5个）→ 扩展（6个）→ 高级（7个子指令）
- 合并 `/novel-maker check`、`/novel-maker analyze`、`/novel-maker pacing`、`/novel-maker constraint`、`/novel-maker consistency`、`/novel-maker fix` 到 `/novel-maker review`
- 合并 `/novel-maker entity`、`/novel-maker outline` 到 `/novel-maker memory`
- `/novel-maker stats wordcount` → `/novel-maker stats`

### 优化
- 核心指令从 19 个精简到 5 个
- 用户只需记住 `/novel-maker init`、`/novel-maker write`、`/novel-maker review`、`/novel-maker memory`、`/novel-maker help`
- 其余功能用自然语言或二级扩展指令调用

## [1.1.0] - 2026-04

### 新增
- RAG 检索增强：AI 自动检索规则、指令驱动检索矩阵、语义检索指引
- `/novel-maker consistency` 指令：实时一致性校验
- `/novel-maker fix` 指令：AI 自动修复审查发现的问题

### 优化
- 简化指令系统：合并冗余子命令，用户只需记住核心指令
- 统一 `/novel-maker review`、`/novel-maker check`、`/novel-maker analyze` 的使用方式
- 移除 `/novel-maker check wordcount` 等重叠指令
- 优化指令速查表，减少用户记忆负担

### 修复
- 模板计数不一致（SKILL.md 说 10 个，实际 13 个）
- 脚本计数不一致（SKILL.md 说 4 个，实际 5 个）
- 描述文案错误（"46 个参考文档"）
- 指令速查表缺少 `/novel-maker summary`、`/novel-maker inspire`、`/novel-maker consistency`、`/novel-maker fix`

---

## [1.0.0] - 2026-04

### 新增
- 完整创作流程：初始化 → 大纲 → 写作 → 审查 → 记忆更新
- 22 位作者文风库：搞笑、热血、文青、严谨等 6 大流派
- 33 维度质量审计：角色、世界观、情节、叙事、文字全覆盖
- 三重记忆系统：真相文件 + 长程上下文 + 实体关系
- S1-S5 五级节奏评级
- 三轴混搭创意约束系统
- 阶段总结：每 10 章/50 章/卷末自动生成
- 灵感助手：剧情走向建议、冲突设计、爽点建议
- 字数统计与自动扩写
- 11 个参考文档、13 个创作模板、5 个脚本工具
