# NovelWeaver - 全能网文写作助手

## 一句话介绍

整合业界优秀网文写作工具理念,通过简洁指令+自然语言,帮你从零创作高质量长篇小说。

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

使用 `/novel-weaver` 指令前缀（支持缩写）：

```
/novel-weaver init 开始写一本修仙小说
/novel-weaver write 写第一章
/novel-weaver review
/novel-weaver memory 主角什么等级
/novel-weaver plan 帮我生成总大纲
/novel-weaver act 下一幕怎么走
```

***

## 核心能力

### 1. 智能创作引导

| 能力    | 说明                                   | 指令                  |
| ----- | ------------------------------------ | ------------------- |
| 项目初始化 | 6问引导：情绪标签→题材→一句话简介→主角姓名+反差点→核心冲突→章节数 | `/novel-weaver init`          |
| 大纲生成  | 基于设定生成含节奏蓝图、幕规划的结构大纲                 | `/novel-weaver plan`          |
| 卷计划   | 分卷规划章节安排                             | `/novel-weaver plan 规划第一卷`    |
| 幕规划   | 卷内剧情弧规划，展示现状+6条分支走向+推荐+幕大纲，支持分段处理偏离提醒 | `/novel-weaver act`           |
| 黄金开篇  | 写第一章时自动生成3版开篇50字+避雷针检查               | `/novel-weaver write` 第一章自动触发 |
| 章节写作  | 自动读取上下文，应用文风写作                       | `/novel-weaver write`         |

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

> 详见 [audit-core.md](references/audit-core.md)

### 5. 记忆与实体（RAG 检索增强）

- **三重记忆**: 真相文件 + 长程上下文 + 实体关系
- **智能检索**: 写作前自动检索相关设定、前文、角色档案
- **实体管理**: 角色/物品/地点/势力的自动提取与管理
- **伏笔追踪**: 自动记录埋设/回收状态
- **状态同步**: 每章后自动更新世界状态

#### 检索规则（AI 自动执行，用户无感知）

| 用户指令         | AI 自动检索范围                                     | 检索目标                       |
| ------------ | --------------------------------------------- | -------------------------- |
| `/novel-weaver write`  | truth-files/、novels/、.novel-weaver/summaries/ | 角色设定、世界观、力量体系、前文相关章节、大纲    |
| `/novel-weaver memory` | truth-files/ | 角色档案、世界状态、伏笔表 |
| `/novel-weaver review` | 被审查章节、truth-files/、前3章                        | 角色设定、前文情节、审查规则、一致性验证所需全部设定 |
| `/novel-weaver plan`   | outline.md、truth-files/、已写卷                   | 总大纲、当前设定、已有内容              |
| `/novel-weaver act`    | outline.md、truth-files/、pending-hooks.md、前3章摘要 | 大纲、角色状态、伏笔表、情绪曲线位置 |
| `/novel-weaver stats`  | novels/volume-XX/chapters/                    | 章节文件统计字数                   |

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

***

## 快速上手

### 第一步：初始化项目

```
/novel-weaver init 开始写小说
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
/novel-weaver plan 帮我生成总大纲
```

AI会根据你的设定生成完整故事大纲（三幕结构）、角色设定、世界观框架、分卷大纲。

### 第三步：开始写作

```
/novel-weaver write 写第一章
```

AI自动完成：
- **黄金开篇**（仅第一章时）：生成3版开篇50字，用户选择最佳版本
- 读取创作宪法和大纲，应用目标文风，生成章节内容
- **自动审查质量**（AI味检测、一致性检查、追读力分析）
- **更新大纲**（标记章节完成状态、更新进度看板）
- **更新记忆文件**（世界状态、角色状态、伏笔追踪）
- **字数检查**（必须符合设定区间，不达标自动提醒 `/novel-weaver expand`）
- **输出本章摘要**和**幕内进度提示**（当前幕第X/Y章）

***

## 推荐工作流

### 从零到一（新书启动）

```
/novel-weaver init 开始写一本修仙小说
    ↓ AI引导6问：情绪标签→题材→简介→主角+反差点→冲突→章节数
/novel-weaver plan 帮我生成总大纲
    ↓ AI生成：三幕结构大纲 + 角色设定 + 世界观 + 幕规划表
/novel-weaver write 写第一章
    ↓ 自动触发黄金开篇 → 写作 → 检查字数 → 更新大纲 → 更新记忆 → 进度提示
/novel-weaver write 继续
    ↓ 运行 chapter_info.py → 获取前章结构 → 日常循环...
/novel-weaver act 下一幕怎么走
    ↓ 运行 volume_batch.py --recent 5 → 现状上下文 + 6条分支 → 用户选择 → 偏离检查 → 同步 → /novel-weaver write
```

### 日常写作循环（核心）

```
/novel-weaver write 继续写，主角发现了敌人
    ↓ AI自动：构建上下文 → 写作 → 审查 → 字数检查 → 更新大纲/记忆 → 摘要 → 进度提示
[看结果] → 满意 → /novel-weaver write 继续
            → 字数不达标 → /novel-weaver expand 扩充本章
            → 不满意 → /novel-weaver review fix 帮我改一下
当期幕章节写完（或中途想调整）→ /novel-weaver act 下一幕怎么走
    ↓ AI展示：现状 + 6条分支走向 + 推荐 + 幕大纲 → 用户选择+调整章节数
    ↓ 偏离检查：若影响整体大纲则提醒 → 同步更新大纲/卷计划/记忆 → 继续写作
```

#### 写作前自动构建上下文 (用户无感知)

AI在写作时自动检索并构建以下上下文，无需用户手动指定：

```markdown
【写作上下文】
## 角色状态 → 来自 truth-files/characters.md + current-state.md
## 世界设定 → 来自 truth-files/world-setting.md + power-system.md  
## 前情摘要 → 来自 .novel-weaver/summaries/ + 前2章摘要
## 本章目标 → 来自 outline.md / volume-XX/plan.md
```

> 详细工作流程请查阅 [references/usage-guide.md](references/usage-guide.md)
> 快速参考请查阅 [QUICK-REF.md](QUICK-REF.md)

***

## 指令参考

> 指令分三级：**核心**（每天用）→ **扩展**（经常用）→ **高级**（极少用，作为子指令）

### 核心指令（写作流程）

| 指令 | 说明 | 示例 |
| ---- | ---- | ---- |
| `/novel-weaver init` | **开始写小说** | `/novel-weaver init 开始写一本修仙小说` |
| `/novel-weaver write` | **写/续写章节** | `/novel-weaver write 写第一章` |
| `/novel-weaver review` | **审查质量** | `/novel-weaver review` |
| `/novel-weaver memory` | **查看/管理设定** | `/novel-weaver memory 主角什么等级` |
| `/novel-weaver plan` | **生成大纲/卷计划** | `/novel-weaver plan 帮我生成总大纲` |
| `/novel-weaver act` | **下一幕剧情规划** | `/novel-weaver act 下一幕怎么走` |
| `/novel-weaver help` | **帮助信息** | `/novel-weaver help` |

### 二级：扩展指令（经常用，5个）

| 指令            | 一句话说明            | 使用示例                               |
| ------------- | ---------------- | ---------------------------------- |
| `/novel-weaver style`   | 切换/推荐文风          | `/novel-weaver style 换辰东风格`                  |
| `/novel-weaver expand`  | 扩写章节             | `/novel-weaver expand` 或 `/novel-weaver expand 增加500字` |
| `/novel-weaver inspire` | 灵感建议             | `/novel-weaver inspire`                      |
| `/novel-weaver stats`   | 字数统计             | `/novel-weaver stats` 或 `/novel-weaver stats volume`   |
| `/novel-weaver summary` | 阶段总结             | `/novel-weaver summary`                      |

### 三级：高级指令（极少用，作为子指令存在）

| 子指令                      | 归属           | 说明      | 等效说法                 |
| ------------------------ | ------------ | ------- | -------------------- |
| `/novel-weaver review consistency` | `/novel-weaver review` | 一致性检查   | `/novel-weaver review 有没有矛盾`   |
| `/novel-weaver review pacing`      | `/novel-weaver review` | 节奏分析    | `/novel-weaver review 节奏怎么样`   |
| `/novel-weaver review constraint`  | `/novel-weaver review` | 约束检查    | `/novel-weaver review 有没有套路重复` |
| `/novel-weaver review fix`         | `/novel-weaver review` | AI 自动修复 | `/novel-weaver review 帮我改一下`   |
| `/novel-weaver memory entity`      | `/novel-weaver memory` | 实体管理    | `/novel-weaver memory 列出所有角色`  |
| `/novel-weaver memory outline`     | `/novel-weaver memory` | 查看大纲    | `/novel-weaver memory 大纲是什么`   |
| `/novel-weaver analyze`            | `/novel-weaver review` | 追读力分析   | `/novel-weaver review 这章好看吗`   |

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
├── QUICK-REF.md                # 快速参考卡（新增）
├── references/                 # 参考文档（优化后15个）
│   ├── rhythm-system.md        # 节奏与情绪控制系统（合并）
│   ├── audit-core.md           # 15维度核心审计（精简）
│   ├── audit-dimensions.md     # 33维度完整审计（保留）
│   ├── anti-ai-patterns.md     # 反AI味指南
│   ├── style-imitation.md      # 文风模仿指南
│   ├── memory-system.md        # 记忆系统说明
│   ├── writing-methods.md      # 写作方法
│   ├── usage-guide.md          # 使用指南
│   ├── creative-constraints.md # 创意约束系统
│   ├── consistency-checker.md  # 一致性检查器
│   ├── data-agent.md           # 实体管理代理
│   ├── golden-opening.md       # 黄金开篇锻造术
│   ├── content-expansion.md    # 内容扩充技巧
│   ├── dialogue-writing.md     # 对话写作规范
│   ├── plot-structures.md      # 情节结构模板
│   └── act-guidance.md         # 幕引导系统
├── styles/                     # 文风库
│   ├── author-styles.md        # 文风汇总
│   └── authors/                # 22位作者文风（按流派分类）
├── templates/                  # 模板文件（14个）
│   ├── chapter.md              # 章节模板
│   ├── constitution.md         # 创作宪法
│   ├── outline.md              # 大纲模板（含幕层级）
│   ├── act-plan.md             # 幕计划模板
│   ├── volume-plan.md          # 卷计划模板
│   └── ...
└── scripts/                    # 脚本工具（13个文件）
    ├── README.md               # 使用说明
    ├── nw_utils.py             # 公共工具模块
    ├── check_wordcount.py      # 字数检查脚本
    ├── chapter_info.py         # 单章结构化提取
    ├── volume_batch.py         # 卷级批量汇总
    ├── hook_report.py          # 钩子密度报告
    ├── consistency_scan.py     # 一致性扫描
    ├── style_check.py          # AI味检测
    ├── stats_report.py         # 项目统计报告
    ├── pacing_report.py        # 卷级节奏报告
    ├── summary_generator.py    # 阶段总结辅助
    ├── outline_extractor.py    # 大纲快速提取
    └── truth_manager.py        # 真相文件管理器
```

### 项目运行时数据（用户项目生成）

```
.novel-weaver/              # 创作元数据（AI内部使用）
├── memory/
│   ├── constitution.md     # 创作宪法
│   └── personal-voice.md   # 个人语料
├── truth-files/            # 真相文件
│   ├── current-state.md    # 世界状态
│   ├── characters.md       # 角色档案
│   ├── world-setting.md    # 世界观
│   ├── pending-hooks.md    # 伏笔表
│   └── power-system.md     # 力量体系
├── reviews/                # 审查报告
└── summaries/              # 阶段总结（10章/50章/卷）

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
| [rhythm-system.md](references/rhythm-system.md)                   | 节奏与情绪控制系统（合并新增） |
| [audit-core.md](references/audit-core.md)                         | 15维度核心审计（精简新增） |
| [genre-rules.md](references/genre-rules.md)                   | 37种题材写作规则 |
| [audit-dimensions.md](references/audit-dimensions.md)         | 33维度完整审计  |
| [anti-ai-patterns.md](references/anti-ai-patterns.md)         | 反AI味指南    |
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

## 脚本工具

| 脚本 | 说明 |
|------|------|
| [check_wordcount.py](scripts/check_wordcount.py) | 字数检查 |
| [chapter_info.py](scripts/chapter_info.py)   | 单章结构化提取，AI可代替读全文 |
| [volume_batch.py](scripts/volume_batch.py)   | 卷级批量汇总，供 `/novel-weaver act` 使用 |
| [hook_report.py](scripts/hook_report.py)     | 钩子密度报告，供 `/novel-weaver review pacing` 使用 |
| [consistency_scan.py](scripts/consistency_scan.py) | 一致性扫描，供 `/novel-weaver review consistency` 使用 |
| [style_check.py](scripts/style_check.py)     | AI味检测，供 `/novel-weaver review ai味` 使用 |
| [stats_report.py](scripts/stats_report.py)   | 项目统计，供 `/novel-weaver stats` 使用 |
| [pacing_report.py](scripts/pacing_report.py) | 节奏报告，供 `/novel-weaver review pacing volume` 使用 |
| [summary_generator.py](scripts/summary_generator.py) | 阶段总结辅助，供 `/novel-weaver summary` 使用 |
| [outline_extractor.py](scripts/outline_extractor.py) | 大纲提取，供 `/novel-weaver memory outline` 使用 |
| [truth_manager.py](scripts/truth_manager.py) | 真相文件管理，供 `/novel-weaver memory entity` 使用 |
| [nw_utils.py](scripts/nw_utils.py)           | 公共模块：所有脚本共用的工具函数 |

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
| 1.2.0 | 2026-04 | 指令精简 - 三级指令体系（5核心+6扩展+7子指令）、合并审查/节奏/约束/一致性到 /novel-weaver review               |
| 1.3.0 | 2026-05 | 结构优化 - 消除SKILL.md重复内容、文风库按流派分类、精简至350行                               |
| 1.4.0 | 2026-05 | 实战增强 - 情绪标签系统、黄金开篇锻造术、情绪曲线"压-小扬-压-爆"、内容扩充/对话写作/情节结构参考文档、Python字数检查脚本 |
| 1.5.0 | 2026-05 | 幕系统 + 脚本 - 引入"幕"概念（卷内剧情弧），`/novel-weaver act`展示现状+6条剧情走向；Python预处理脚本12个+公共模块1个，节省约90% token消耗 |
| 1.6.0 | 2026-05 | 文档优化 - 新增QUICK-REF快速参考卡、合并节奏与情绪文档、精简审计为15核心维度、SKILL.md去重 |

***

*NovelWeaver v1.6.0 - 指令* *`/nw`* *+ 语义，用说话的方式写小说*
