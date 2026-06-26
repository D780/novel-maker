---
name: novel-maker
version: 2.2.0
description: 全能网文写作助手 - 6角色协作架构，支持多AI IDE
tags: [writing, novel, chinese, web-novel, ai-assistant]
---

# NovelMaker - 全能网文写作助手

> **v2.2.0** - 6角色协作架构，融合业界最佳实践

## 一句话介绍

整合业界优秀网文写作工具理念，通过6角色协作架构+自然语言，帮你从零创作高质量长篇小说。

## 快速上手

### 新用户推荐流程

1. **安装技能** → 参考 [INSTALL.md](../INSTALL.md)
2. **快速上手** → 参考 [quickstart.md](docs/quickstart.md)
3. **完整文档** → 继续阅读本文档

### 5分钟快速体验

```
/novel-maker init 开始写一本修仙小说
/novel-maker plan 帮我生成总大纲
/novel-maker write 写第一章
```

> 详细步骤请参考 [quickstart.md](docs/quickstart.md)

***

## 触发方式

本技能支持两种触发方式（等价）：

### 方式一：自然语言触发

直接描述你的意图，AI 会自动识别并执行：

| 自然语言示例 | 触发功能 |
|------------|---------|
| "开始写小说" / "我想写一本修仙小说" | 项目初始化 |
| "帮我写第一章" / "继续写，主角遇到了敌人" | 章节写作 |
| "帮我看看这一章" / "检查有没有矛盾" | 质量审查 |
| "主角什么等级" / "列出所有角色" | 查看设定 |
| "帮我生成总大纲" / "规划第一卷" | 生成大纲 |
| "下一幕怎么走" / "给我剧情建议" | 幕规划 |
| "换个文风" / "统计字数" / "给我灵感" | 扩展功能 |

### 方式二：指令快捷触发

使用 `/novel-maker` 指令前缀（支持缩写）：

```
/novel-maker init 开始写一本修仙小说
/novel-maker write 写第一章
/novel-maker review
/novel-maker memory 主角什么等级
/novel-maker plan 帮我生成总大纲
/novel-maker act 下一幕怎么走
```

***

## 核心能力

### 1. 智能创作引导

| 能力    | 说明                                   | 指令                  |
| ----- | ------------------------------------ | ------------------- |
| 项目初始化 | 6问引导：情绪标签→题材→一句话简介→主角姓名+反差点→核心冲突→章节数 | `/novel-maker init`          |
| 大纲生成  | 基于设定生成含节奏蓝图、幕规划的结构大纲                 | `/novel-maker plan`          |
| 卷计划   | 分卷规划章节安排                             | `/novel-maker plan 规划第一卷`    |
| 幕规划   | 卷内剧情弧规划，展示现状+6条分支走向+推荐+幕大纲，支持分段处理偏离提醒 | `/novel-maker act`           |
| 黄金开篇  | 写第一章时自动生成3版开篇50字+避雷针检查               | `/novel-maker write` 第一章自动触发 |
| 章节写作  | 自动读取上下文，应用文风写作                       | `/novel-maker write`         |

### 2. 文风系统

- **22位作者文风库**: 覆盖搞笑、热血、文青、严谨等7大流派
- **智能推荐**: 根据题材自动推荐合适文风
- **场景切换**: 不同场景使用不同文风
- **自定义文风**: 支持学习用户个人写作风格

> 文风库详见 [styles/author-styles.md](styles/author-styles.md)

### 3. 节奏与情绪控制

- **情绪标签驱动**: 6大标签对应不同的节奏模板
- **情绪单元**: 每3章"压-小扬-压-爆"循环
- **双轨评级**: S1-S5五级节奏评级 + 情绪曲线
- **卷级节奏**: 整卷节奏曲线分析
- **五章报告**: 每5章生成节奏报告 + 评论区争论点预测

> 详见 [rhythm-system.md](references/rhythm-system.md)

### 4. 质量保障

- **15核心维度**: 角色、世界观、情节、叙事、文字全覆盖
- **33完整维度**: 深度审查时使用(每5章/卷末)
- **AI味检测**: 识别套话、情感空洞、描写模式化
- **一致性检查**: 角色OOC、设定冲突、时间线验证
- **追读力分析**: Hook质量、爽点、弃读风险评估
- **反AI表达规则**: 7层检测体系，60+常见AI-slop模式识别
- **风格锚点系统**: 从最近5章提取句长分布、对话比例、高频词
- **角色声音检查**: 5维度检查（语言习惯、情感表达、知识边界、行为逻辑、关系互动）
- **5维度一致性检查**: 时间线、人物关系、世界观、伏笔回收、能力等级

> 详见 [audit-core.md](references/audit-core.md)
> 反AI表达规则详见 [rules/anti-ai-expressions.md](rules/anti-ai-expressions.md)
> 角色声音检查详见 [rules/character-voice.md](rules/character-voice.md)
> 一致性检查详见 [rules/consistency-check.md](rules/consistency-check.md)

### 5. 记忆与实体（RAG 检索增强）

- **三重记忆**: 真相文件 + 长程上下文 + 实体关系
- **智能检索**: 写作前自动检索相关设定、前文、角色档案
- **实体管理**: 角色/物品/地点/势力的自动提取与管理
- **伏笔追踪**: 自动记录埋设/回收状态
- **状态同步**: 每章后自动更新世界状态

#### 检索规则（AI 自动执行，用户无感知）

| 用户指令         | AI 自动检索范围                                     | 检索目标                       |
| ------------ | --------------------------------------------- | -------------------------- |
| `/novel-maker write`  | truth-files/、novels/、.novel-maker/summaries/ | 角色设定、世界观、力量体系、前文相关章节、大纲    |
| `/novel-maker memory` | truth-files/ | 角色档案、世界状态、伏笔表 |
| `/novel-maker review` | 被审查章节、truth-files/、前3章                        | 角色设定、前文情节、审查规则、一致性验证所需全部设定 |
| `/novel-maker plan`   | outline.md、truth-files/、已写卷                   | 总大纲、当前设定、已有内容              |
| `/novel-maker act`    | outline.md、truth-files/、pending-hooks.md、前3章摘要 | 大纲、角色状态、伏笔表、情绪曲线位置 |
| `/novel-maker stats`  | novels/volume-XX/chapters/                    | 章节文件统计字数                   |

### 6. 创意约束

- **三轴混搭**: 风格轴+冲突轴+节奏轴组合防重复
- **反套路触发器**: 检测常见套路并自动改写
- **镜像对抗**: 确保冲突双方有对等合理性
- **约束继承**: 新章节继承前文约束，禁止随意发明设定

### 7. 总结与回顾

| 能力   | 说明                    |
| ---- | --------------------- |
| 小总结  | 每10章自动生成，记录剧情进展和伏笔状态  |
| 大总结  | 每50章全面回顾，包含角色成长和世界观展开 |
| 卷总结  | 每卷结束总结，包含下一卷衔接建议      |
| 剧情回顾 | 随时查看已写内容的剧情概要         |

### 8. 灵感助手

| 能力    | 说明                 |
| ----- | ------------------ |
| 剧情建议  | 基于当前剧情，给出短期/长期走向建议 |
| 冲突设计  | 设计人际/内在/外部冲突       |
| 爽点建议  | 设计多样化爽点（打脸、逆袭、突破等） |
| 评论区诱导 | 在关键节点设计留白，引导读者互动讨论 |
| 角色建议  | 新角色出场建议和角色关系设计     |

### 9. 6角色协作架构

NovelMaker v2.0 采用 6角色协作架构，每个角色专注特定职责：

| 角色 | 职责 | 触发时机 |
|------|------|---------|
| **协调者** | 解析用户意图，调度角色，管理流程状态 | 所有用户输入 |
| **规划师** | 大纲生成、幕规划、剧情走向推荐、灵感建议 | `/novel-maker plan` `/novel-maker act` `/novel-maker inspire` |
| **写手** | 章节正文生成、文风应用、角色模拟写作 | `/novel-maker write` |
| **审计师** | 33维度审计、编辑视角审查、爽点密度追踪 | `/novel-maker review` 每章自动 |
| **修订师** | 根据审计报告修复P0/P1问题 | `/novel-maker review fix` 审计后自动 |
| **复盘师** | 更新真相文件、生成总结、模拟读者评论、生成创作指导 | 章节定稿后自动 |

> 角色定义详见 [agents/](agents/) 目录

### 10. 题材包系统

- **11个核心题材包**: 修仙、都市、无限流、悬疑、历史、科幻、游戏、末世、西幻、武侠、言情
- **模块化设计**: 每个题材包含写作规则、模板、弧线类型、设定参考
- **智能推荐**: 根据题材自动加载对应题材包
- **可扩展**: 支持自定义题材包

> 详见 [genre-packs/](genre-packs/)

### 11. 篇章弧线模板

- **6种通用弧线**: 挑战弧、探索弧、冲突弧、悬疑弧、成长弧、关系弧
- **42种题材特定弧线**: 每个题材包有专属弧线模板（修仙4/都市4/无限流4/悬疑3/历史3/科幻4/游戏4/末世4/西幻4/武侠4/言情4）
- **结构化规划**: 阶段定义、章节建议、情绪曲线、关键场景
- **幕规划辅助**: 自动推荐合适的弧线模板

> 详见 [arc-templates/](arc-templates/)

### 12. 节奏可视化

- **章节级标记**: emoji 标记节奏强度（🟢平淡/🟡小高潮/🔴大高潮）
- **卷级热力图**: 可视化整卷节奏分布
- **情绪统计**: 多维度情绪点统计分析
- **问题检测**: 自动检测连续平淡/高潮等节奏问题

> 使用方式：`python scripts/pacing_visualize.py --volume novels/volume-01/`

### 13. 智能查询系统

- **4种查询类型**: 角色查询、设定查询、剧情查询、伏笔查询
- **意图识别**: 自动识别查询意图，路由到对应功能
- **自然语言支持**: 支持自然语言查询，如"林风是什么等级？"
- **结果格式化**: 查询结果格式化展示，包含来源信息

> 使用方式：`python skill/scripts/query_engine.py '林风是什么等级？'`

### 14. Hook 系统

- **5个自动化 Hook**: 上下文注入、意图检测、章节完成、审查触发、总结触发
- **自动上下文注入**: 写作前自动注入角色状态、世界观、前情摘要
- **意图检测**: 自动识别用户意图，路由到对应功能
- **章节完成更新**: 章节完成后自动更新大纲、记忆文件、伏笔表
- **质量审查触发**: 每章完成后自动触发质量审查
- **阶段总结触发**: 每10章/50章自动生成阶段总结

> 详见 [hooks/](hooks/)

### 15. Web UI

- **项目概览**: 总章节数、总字数、当前进度
- **章节列表**: 浏览和管理所有章节
- **角色档案**: 查看角色设定
- **节奏可视化**: Chart.js 图表展示节奏曲线
- **Markdown 编辑器**: 实时预览编辑
- **设置页面**: 模型配置、Hook 配置、项目管理
- **项目管理**: 多项目切换、项目导入/导出

> 启动方式：`cd web && python -m http.server 8000`，然后访问 http://localhost:8000

***

## 详细使用流程

### 第一步：初始化项目

```
/novel-maker init 开始写小说
```

AI会引导你完成以下配置：
- **情绪标签**：6大标签选择（打脸爽文/极致虐恋/爆笑反套路/悬疑惊悚/治愈甜宠/脑洞大开）
- **题材**：选定小说题材
- **一句话简介**：一句话概括故事核心
- **主角设定**：姓名、核心反差点（表面XX实际XX）、核心目标
- **核心冲突**：确定主要矛盾
- **章节数/文风/基调**：目标章节数、写作风格、故事氛围

### 第二步：生成大纲

```
/novel-maker plan 帮我生成总大纲
```

AI会根据你的设定生成完整故事大纲（三幕结构）、角色设定、世界观框架、分卷大纲。

### 第三步：开始写作

```
/novel-maker write 写第一章
```

AI自动完成：
- **黄金开篇**（仅第一章时）：生成3版开篇50字，用户选择最佳版本
- 读取创作宪法和大纲，应用目标文风，生成章节内容
- **自动审查质量**（AI味检测、一致性检查、追读力分析）
- **更新大纲**（标记章节完成状态、更新进度看板）
- **更新记忆文件**（世界状态、角色状态、伏笔追踪）
- **字数检查**（必须符合设定区间，不达标自动提醒 `/novel-maker expand`）
- **输出本章摘要**和**幕内进度提示**（当前幕第X/Y章）

***

## 推荐工作流

### 从零到一（新书启动）

```
/novel-maker init 开始写一本修仙小说
    ↓ AI引导6问：情绪标签→题材→简介→主角+反差点→冲突→章节数
/novel-maker plan 帮我生成总大纲
    ↓ AI生成：三幕结构大纲 + 角色设定 + 世界观 + 幕规划表
/novel-maker write 写第一章
    ↓ 自动触发黄金开篇 → 写作 → 检查字数 → 更新大纲 → 更新记忆 → 进度提示
/novel-maker write 继续
    ↓ 运行 chapter_info.py → 获取前章结构 → 日常循环...
/novel-maker act 下一幕怎么走
    ↓ 运行 volume_batch.py --recent 5 → 现状上下文 + 6条分支 → 用户选择 → 偏离检查 → 同步 → /novel-maker write
```

### 日常写作循环（核心）

```
/novel-maker write 继续写，主角发现了敌人
    ↓ AI自动：构建上下文 → 写作 → 审查 → 字数检查 → 更新大纲/记忆 → 摘要 → 进度提示
[看结果] → 满意 → /novel-maker write 继续
            → 字数不达标 → /novel-maker expand 扩充本章
            → 不满意 → /novel-maker review fix 帮我改一下
当期幕章节写完（或中途想调整）→ /novel-maker act 下一幕怎么走
    ↓ AI展示：现状 + 6条分支走向 + 推荐 + 幕大纲 → 用户选择+调整章节数
    ↓ 偏离检查：若影响整体大纲则提醒 → 同步更新大纲/卷计划/记忆 → 继续写作
```

#### 写作前自动构建上下文 (用户无感知)

AI在写作时自动检索并构建以下上下文，无需用户手动指定：

```markdown
【写作上下文】
## 角色状态 → 来自 truth-files/characters.md + current-state.md
## 世界设定 → 来自 truth-files/world-setting.md + power-system.md  
## 前情摘要 → 来自 .novel-maker/summaries/ + 前2章摘要
## 本章目标 → 来自 outline.md / volume-XX/plan.md
```

#### 字数强制检查规则（最高优先级）

**每一章写完后必须立即执行字数检查，不可跳过，不可延后。**

```
每章写完 → 检查字数 → 达标? 
    ├─ 是 → 继续后续步骤（审查/更新大纲/更新记忆）
    └─ 否 → 立即自动扩写 → 再次检查 → 直到达标为止
```

**强制规则**：
1. 写单章：写完后检查，不达标立即扩写，直到达标才输出结果
2. 连续写多章：**每章独立检查**，写完一章检查一章，达标后才写下一章
3. 禁止"全部写完再统一检查"——必须在写作流程中逐章检查
4. 扩写时仅增加内容，不删改已有正文
5. 字数标准：遵循创作宪法中设定的范围（默认2000-4000字，理想2500-3500字）
6. 平台适配字数：
   - 番茄小说：建议2000-3000字/章
   - 起点中文网：建议2500-4000字/章
   - 晋江文学城：建议2000-3500字/章
   - 未指定平台时，默认使用"默认值"范围

> 详细工作流程请查阅 [references/usage-guide.md](references/usage-guide.md)
> 快速参考请查阅 [QUICK-REF.md](QUICK-REF.md)

***

## 指令参考

> 指令分三级：**核心**（每天用）→ **扩展**（经常用）→ **高级**（极少用，作为子指令）

### 核心指令（写作流程）

| 指令 | 说明 | 示例 |
| ---- | ---- | ---- |
| `/novel-maker init` | **开始写小说** | `/novel-maker init 开始写一本修仙小说` |
| `/novel-maker write` | **写/续写章节** | `/novel-maker write 写第一章` |
| `/novel-maker review` | **审查质量** | `/novel-maker review` |
| `/novel-maker memory` | **查看/管理设定** | `/novel-maker memory 主角什么等级` |
| `/novel-maker plan` | **生成大纲/卷计划** | `/novel-maker plan 帮我生成总大纲` |
| `/novel-maker act` | **下一幕剧情规划** | `/novel-maker act 下一幕怎么走` |
| `/novel-maker help` | **帮助信息** | `/novel-maker help` |

### 二级：扩展指令（经常用，5个）

| 指令            | 一句话说明            | 使用示例                               |
| ------------- | ---------------- | ---------------------------------- |
| `/novel-maker style`   | 切换/推荐文风          | `/novel-maker style 换辰东风格`                  |
| `/novel-maker expand`  | 扩写章节             | `/novel-maker expand` 或 `/novel-maker expand 增加500字` |
| `/novel-maker inspire` | 灵感建议             | `/novel-maker inspire`                      |
| `/novel-maker stats`   | 字数统计             | `/novel-maker stats` 或 `/novel-maker stats volume`   |
| `/novel-maker summary` | 阶段总结             | `/novel-maker summary`                      |

### 三级：高级指令（极少用，作为子指令存在）

| 子指令                      | 归属           | 说明      | 等效说法                 |
| ------------------------ | ------------ | ------- | -------------------- |
| `/novel-maker review consistency` | `/novel-maker review` | 一致性检查   | `/novel-maker review 有没有矛盾`   |
| `/novel-maker review pacing`      | `/novel-maker review` | 节奏分析    | `/novel-maker review 节奏怎么样`   |
| `/novel-maker review constraint`  | `/novel-maker review` | 约束检查    | `/novel-maker review 有没有套路重复` |
| `/novel-maker review fix`         | `/novel-maker review` | AI 自动修复 | `/novel-maker review 帮我改一下`   |
| `/novel-maker memory entity`      | `/novel-maker memory` | 实体管理    | `/novel-maker memory 列出所有角色`  |
| `/novel-maker memory outline`     | `/novel-maker memory` | 查看大纲    | `/novel-maker memory 大纲是什么`   |
| `/novel-maker analyze`            | `/novel-maker review` | 追读力分析   | `/novel-maker review 这章好看吗`   |

***

## 文风推荐系统

在创建项目时，AI会根据题材自动推荐合适的文风：

| 题材    | 推荐文风       | 理由          |
| ----- | ---------- | ----------- |
| 玄幻修仙  | 天蚕土豆、辰东    | 热血升级，宏大世界观  |
| 都市搞笑  | 弈青峰、会说话的肘子 | 幽默接地气       |
| 仙侠探案  | 卖报小郎君      | 探案+仙侠+搞笑    |
| 悬疑诡秘  | 爱潜水的乌贼     | 设定严谨，逻辑严密   |
| 历史权谋  | 猫腻、愤怒的香蕉   | 文笔细腻，深度思考   |
| 凡人流   | 忘语、言归正传    | 严谨稳健        |
| 电竞网游  | 蝴蝶蓝        | 群像精彩，热血     |
| 无限流   | 三天两觉、杀虫队队员 | 吐槽玩梗/烧脑轮回   |
| 盗墓探险  | 天下霸唱       | 江湖气，民俗悬疑    |
| 极道诡异  | 滚开         | 黑暗杀伐，加点升级   |
| 稳健搞笑  | 言归正传       | 反套路，苟道      |
| 多神话热血 | 三九音域       | 多神话融合，守夜人家国 |
| 悬疑推理  | 杀虫队队员      | 反爽文，智商博弈    |

> 完整22位作者文风库详见 [styles/author-styles.md](styles/author-styles.md)

***

## 项目结构

### 技能静态内容

```
.
├── SKILL.md                    # 主技能文件
├── QUICK-REF.md                # 快速参考卡
├── agents/                     # 角色定义（6个）
│   ├── coordinator.md          # 协调者
│   ├── planner.md              # 规划师
│   ├── writer.md               # 写手
│   ├── auditor.md              # 审计师
│   ├── reviser.md              # 修订师
│   └── reviewer.md             # 复盘师
├── references/                 # 参考文档（22个）
│   ├── rhythm-system.md        # 节奏与情绪控制系统
│   ├── audit-core.md           # 15维度核心审计
│   ├── audit-dimensions.md     # 33维度完整审计
│   ├── platform-rules.md       # 平台适配规则
│   ├── editorial-perspective.md # 编辑视角审查
│   ├── sweet-spot-tracking.md  # 爽点密度追踪
│   ├── character-voice-card.md # 角色语音卡指南
│   ├── style-imitation.md      # 文风模仿指南
│   ├── memory-system.md        # 记忆系统说明
│   ├── writing-methods.md      # 写作方法
│   ├── usage-guide.md          # 使用指南
│   ├── creative-constraints.md # 创意约束系统
│   ├── consistency-checker.md  # 一致性检查器（执行流程）
│   ├── data-agent.md           # 实体管理代理
│   ├── golden-opening.md       # 黄金开篇锻造术
│   ├── content-expansion.md    # 内容扩充技巧
│   ├── dialogue-writing.md     # 对话写作规范
│   ├── plot-structures.md      # 情节结构模板
│   ├── act-guidance.md         # 幕引导系统
│   ├── genre-rules.md          # 题材写作规则
│   ├── pacing-analysis.md      # 节奏分析
│   ├── emotion-curve.md        # 情绪曲线
│   └── reader-feedback.md      # 读者反馈模拟
├── rules/                      # 规则文件（4个）
│   ├── anti-ai-expressions.md  # 反AI表达规则（7层检测+去AI味技巧）
│   ├── character-voice.md      # 角色声音检查规则（5维度）
│   ├── consistency-check.md    # 5维度一致性检查规则
│   └── smart-query.md          # 智能查询规则
├── styles/                     # 文风库
│   ├── author-styles.md        # 文风汇总
│   └── authors/                # 22位作者文风（按流派分类）
├── templates/                  # 模板文件（21个）
│   ├── chapter.md              # 章节模板
│   ├── constitution.md         # 创作宪法
│   ├── outline.md              # 大纲模板（含幕层级）
│   ├── act-plan.md             # 幕计划模板
│   ├── volume-plan.md          # 卷计划模板
│   ├── plot-card.md            # 剧情卡片模板
│   ├── character-voice.md      # 角色语音卡模板
│   ├── scene-plan.md           # 场景规划卡模板
│   ├── emotional-arcs.md       # 情感弧线追踪模板
│   ├── subplot-board.md        # 支线看板模板
│   ├── timeline.md             # 时间线追踪模板
│   └── ...
├── genre-packs/                # 题材包（11个 + 通用默认）
├── arc-templates/              # 篇章弧线模板（6通用 + 42题材特定）
├── hooks/                      # Hook 定义（5个）
└── scripts/                    # 脚本工具（22个）
    ├── README.md               # 使用说明
    ├── nw_utils.py             # 公共工具模块
    ├── validate.py             # 技能完整性验证
    ├── analyze.py              # 三合一分析（单章/风格/批量）
    ├── check_wordcount.py      # 字数检查
    ├── chapter_info.py         # 单章结构化提取
    ├── volume_batch.py         # 卷级批量汇总
    ├── hook_report.py          # 钩子密度报告
    ├── consistency_scan.py     # 一致性扫描
    ├── style_check.py          # AI味检测
    ├── stats_report.py         # 项目统计报告
    ├── pacing_report.py        # 卷级节奏报告
    ├── pacing_visualize.py     # 节奏可视化
    ├── summary_generator.py    # 阶段总结辅助
    ├── outline_extractor.py    # 大纲快速提取
    ├── truth_manager.py        # 真相文件管理器
    ├── query_engine.py         # 智能查询引擎
    ├── style_anchor.py         # 风格锚点提取
    ├── init_guide.py           # 初始化引导
    ├── install.py              # Python 安装脚本
    ├── build_write_context.py  # 写手上下文构建器（Token优化）
    ├── pre_audit.py            # 预审计管线（Token优化）
    └── truth_diff.py           # 真相文件变更检测（Token优化）
```

### 项目运行时数据（用户项目生成）

```
.novel-maker/              # 创作元数据（AI内部使用）
├── memory/
│   ├── constitution.md     # 创作宪法
│   └── personal-voice.md   # 个人语料
├── truth-files/            # 真相文件（8个）
│   ├── current-state.md    # 世界状态
│   ├── characters.md       # 角色档案
│   ├── world-setting.md    # 世界观
│   ├── pending-hooks.md    # 伏笔表
│   ├── power-system.md     # 力量体系
│   ├── emotional-arcs.md   # 情感弧线追踪
│   ├── subplot-board.md    # 支线看板
│   └── timeline.md         # 时间线追踪
├── reviews/                # 审查报告
├── summaries/              # 阶段总结（10章/50章/卷）
└── temp/                   # 角色间数据传递缓存

novels/                     # 小说正文（用户直接编辑）
├── outline.md              # 总大纲
└── volume-01/
    ├── plan.md             # 卷计划
    └── chapters/           # 章节正文（ch01.md, ch02.md...）
```

***

## 参考文档

| 文档                                                            | 说明        |
| ------------------------------------------------------------- | --------- |
| [rhythm-system.md](references/rhythm-system.md)                   | 节奏与情绪控制系统 |
| [audit-core.md](references/audit-core.md)                         | 15维度核心审计 |
| [genre-rules.md](references/genre-rules.md)                   | 37种题材写作规则 |
| [audit-dimensions.md](references/audit-dimensions.md)         | 33维度完整审计  |
| [anti-ai-expressions.md](rules/anti-ai-expressions.md) | 反AI表达规则（7层检测+去AI味技巧+自检清单） |
| [platform-rules.md](references/platform-rules.md)             | 平台适配规则（番茄/起点/晋江） |
| [style-imitation.md](references/style-imitation.md)           | 文风模仿指南    |
| [memory-system.md](references/memory-system.md)               | 记忆系统      |
| [writing-methods.md](references/writing-methods.md)           | 写作方法      |
| [usage-guide.md](references/usage-guide.md)                   | 使用指南      |
| [creative-constraints.md](references/creative-constraints.md) | 创意约束系统    |
| [consistency-checker.md](references/consistency-checker.md)   | 一致性检查器    |
| [data-agent.md](references/data-agent.md)                     | 实体管理代理    |
| [golden-opening.md](references/golden-opening.md)             | 黄金开篇锻造术   |
| [content-expansion.md](references/content-expansion.md)       | 内容扩充技巧    |
| [dialogue-writing.md](references/dialogue-writing.md)         | 对话写作规范    |
| [plot-structures.md](references/plot-structures.md)           | 情节结构模板    |
| [act-guidance.md](references/act-guidance.md)                 | 幕引导系统     |
| [editorial-perspective.md](references/editorial-perspective.md) | 编辑视角审查指南（开篇吸引力/节奏曲线/角色商业价值） |
| [sweet-spot-tracking.md](references/sweet-spot-tracking.md) | 爽点密度追踪系统（10类爽点/S1-S5强度/平台适配） |
| [character-voice-card.md](references/character-voice-card.md) | 角色语音卡使用指南（口头禅/常用词/语气特点） |

## 脚本工具

| 脚本 | 说明 |
|------|------|
| [check_wordcount.py](scripts/check_wordcount.py) | 字数检查 |
| [chapter_info.py](scripts/chapter_info.py)   | 单章结构化提取，AI可代替读全文 |
| [volume_batch.py](scripts/volume_batch.py)   | 卷级批量汇总，供 `/novel-maker act` 使用 |
| [hook_report.py](scripts/hook_report.py)     | 钩子密度报告，供 `/novel-maker review pacing` 使用 |
| [consistency_scan.py](scripts/consistency_scan.py) | 一致性扫描，供 `/novel-maker review consistency` 使用 |
| [style_check.py](scripts/style_check.py)     | AI味检测，供 `/novel-maker review ai味` 使用 |
| [stats_report.py](scripts/stats_report.py)   | 项目统计，供 `/novel-maker stats` 使用 |
| [pacing_report.py](scripts/pacing_report.py) | 节奏报告，供 `/novel-maker review pacing volume` 使用 |
| [summary_generator.py](scripts/summary_generator.py) | 阶段总结辅助，供 `/novel-maker summary` 使用 |
| [outline_extractor.py](scripts/outline_extractor.py) | 大纲提取，供 `/novel-maker memory outline` 使用 |
| [truth_manager.py](scripts/truth_manager.py) | 真相文件管理，供 `/novel-maker memory entity` 使用 |
| [nw_utils.py](scripts/nw_utils.py)           | 公共模块：所有脚本共用的工具函数 |
| [style_anchor.py](scripts/style_anchor.py)   | 风格锚点提取：从最近5章提取句长分布、对话比例、高频词 |

> 使用脚本预处理可节省约 **90% token 消耗**。详见 [scripts/README.md](scripts/README.md)

### 模板清单

| 模板                      | 用途        |
| ----------------------- | --------- |
| `constitution.md`       | 创作宪法      |
| `outline.md`            | 总大纲（含幕层级） |
| `act-plan.md`           | 幕计划       |
| `volume-plan.md`        | 卷计划       |
| `chapter.md`            | 章节模板      |
| `character-profile.md`  | 角色档案      |
| `plot-card.md`          | 剧情卡片      |
| `character-voice.md`    | 角色语音卡     |
| `scene-plan.md`         | 场景规划卡     |
| `emotional-arcs.md`     | 情感弧线追踪    |
| `subplot-board.md`      | 支线看板      |
| `timeline.md`           | 时间线追踪     |
| `scene-template.md`     | 场景规划      |
| `hook-template.md`      | 伏笔管理      |
| `review-report.md`      | 审查报告      |
| `world-setting.md`      | 世界观设定     |
| `power-system.md`       | 力量体系      |
| `summary-10chapters.md` | 10章小总结    |
| `summary-50chapters.md` | 50章大总结    |
| `summary-volume.md`     | 卷总结       |

***

## 版本历史

| 版本    | 日期      | 更新内容                                                                 |
| ----- | ------- | -------------------------------------------------------------------- |
| 1.0.0 | 2026-04 | 初始版本 - 完整创作流程、文风系统、质量保障、阶段总结、灵感助手                                    |
| 1.1.0 | 2026-04 | RAG 检索增强 - AI 自动检索规则、指令驱动检索矩阵、语义检索指引                                 |
| 1.2.0 | 2026-04 | 指令精简 - 三级指令体系（5核心+6扩展+7子指令）、合并审查/节奏/约束/一致性到 /novel-maker review               |
| 1.3.0 | 2026-05 | 结构优化 - 消除SKILL.md重复内容、文风库按流派分类、精简至350行                               |
| 1.4.0 | 2026-05 | 实战增强 - 情绪标签系统、黄金开篇锻造术、情绪曲线"压-小扬-压-爆"、内容扩充/对话写作/情节结构参考文档、Python字数检查脚本 |
| 1.5.0 | 2026-05 | 幕系统 + 脚本 - 引入"幕"概念（卷内剧情弧），`/novel-maker act`展示现状+6条剧情走向；Python预处理脚本12个+公共模块1个，节省约90% token消耗 |
| 1.6.0 | 2026-05 | 文档优化 - 新增QUICK-REF快速参考卡、合并节奏与情绪文档、精简审计为15核心维度、SKILL.md去重 |
| 2.0.0 | 2026-06 | **架构重构** - 6角色协作架构（协调者/规划师/写手/审计师/修订师/复盘师）、真相文件扩展至8个、新增去AI味技巧/平台适配规则/剧情卡片/角色语音卡/场景规划卡等模板 |
| 2.1.0 | 2026-06 | **质量增强** - 反AI表达规则（7层检测60+模式）、风格锚点脚本、角色声音检查（5维度）、5维度一致性检查、11个题材包、6种通用弧线+42种题材特定弧线、节奏可视化、Web UI |
| 2.2.0 | 2026-06 | **智能化增强** - 智能查询系统（4种查询类型）、Hook 系统（5个自动化 Hook）、Web UI 增强（设置页面、项目管理） |

***

*NovelMaker v2.2.0 - 6角色协作架构，用说话的方式写小说*
