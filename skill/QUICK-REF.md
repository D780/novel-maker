# NovelMaker 快速参考卡

> **v2.2.0** - 6角色协作架构

## 核心指令 (7个)

| 指令 | 用途 | 示例 |
|------|------|------|
| `/novel-maker init` | 初始化项目 | `/novel-maker init 开始写修仙小说` |
| `/novel-maker write` | 写/续写章节 | `/novel-maker write 写第一章` |
| `/novel-maker review` | 审查质量 | `/novel-maker review` |
| `/novel-maker memory` | 查看设定 | `/novel-maker memory 主角等级` |
| `/novel-maker plan` | 生成大纲 | `/novel-maker plan 生成总大纲` |
| `/novel-maker act` | 幕规划 | `/novel-maker act 下一幕怎么走` |
| `/novel-maker help` | 帮助 | `/novel-maker help` |

## 扩展指令 (5个)

`/novel-maker style` 文风 | `/novel-maker expand` 扩写 | `/novel-maker inspire` 灵感 | `/novel-maker stats` 统计 | `/novel-maker summary` 总结

## 6角色协作架构

```
用户输入
   ↓
[协调者] 意图识别
   ↓
[规划师] → 大纲/剧情卡片
   ↓
[写手] → 章节草稿
   ↓
[审计师] → 审计报告
   ↓
[修订师] → 修订稿
   ↓
[复盘师] → 真相文件更新
   ↓
[协调者] 输出
```

## 剧情卡片 6 要素

| 要素 | 用途 |
|------|------|
| 方向类型 | 剧情走向分类 |
| 剧情预演 | 未来章节预览 |
| 优点分析 | 剧情优势评估 |
| 参考小说 | 同类型作品对标 |
| 预计章节数 | 篇幅预估 |
| 偏离影响评估 | 跑偏风险预警 |

## 日常写作循环

```
/novel-maker write 继续写
  ↓ AI自动: 写作 → 审查 → 字数检查 → 更新大纲/记忆 → 进度提示
满意 → /novel-maker write 继续
不满意 → /novel-maker review fix 帮我改一下
字数不足 → /novel-maker expand 扩充本章
写完当前幕 → /novel-maker act 下一幕怎么走
```

## 脚本速查

| 场景 | 命令 | 用途 |
|------|------|------|
| 写前上下文 | `python scripts/writer/chapter_info.py 前章.md --json` | 获取前章结构(~200 token) |
| **写手上文** | `python scripts/writer/build_write_context.py ch15.md --json` | **一键构建写作上下文(~3000 token)** |
| **预审计** | `python scripts/auditor/pre_audit.py ch15.md --json` | **一键运行所有自动化审计** |
| **真相变更** | `python scripts/reviewer/truth_diff.py ch15.md -t 真相/ --json` | **检测需更新的真相文件** |
| **规划上下文** | `python scripts/planner/planner_context.py --volume 01 --json` | **规划师精简上下文(~5000 token)** |
| **修订对比** | `python scripts/reviewer/chapter_diff.py .novel-maker/temp/ch017-draft.md .novel-maker/temp/ch017-revised.md --json` | **比较原稿和修订稿差异** |
| 幕规划 | `python scripts/coordinator/volume_batch.py 卷目录 --recent 5 --json` | 获取最近5章汇总 |
| 字数检查 | `python scripts/writer/check_wordcount.py 本章.md` | 验证字数达标 |
| 一致性扫描 | `python scripts/auditor/consistency_scan.py 章节/ 真相/ --json` | 检测设定冲突 |
| AI味检测 | `python scripts/auditor/style_check.py 本章.md --json` | 检测套话密度 |
| 节奏报告 | `python scripts/auditor/pacing_report.py 章节/ --json` | S1-S5分布分析 |
| 项目统计 | `python scripts/coordinator/stats_report.py novels/ --json` | 卷/章/字数统计 |
| 风格锚点 | `python scripts/writer/style_anchor.py 章节/` | 提取句长/对话/高频词 |
| 节奏可视化 | `python scripts/auditor/pacing_report.py 卷目录 --visualize` | emoji标记+热力图+情绪统计 |
| 智能查询 | `python scripts/planner/query_engine.py '林风什么等级'` | 角色/设定/伏笔查询 |
| **场景构建** | `python scripts/writer/scene_builder.py --type 冲突 --chars 林风,苏婉` | 生成场景结构建议 |
| **对话检查** | `python scripts/auditor/dialogue_checker.py 本章.md --json` | 检测对话质量问题 |
| **角色弧线** | `python scripts/reviewer/character_arc_tracker.py 章节/ --chars 林风` | 追踪角色成长轨迹 |
| **支线追踪** | `python scripts/reviewer/subplot_tracker.py 章节/ --json` | 检测支线发展状态 |
| **衔接检查** | `python scripts/auditor/chapter_transition.py 章节/ --json` | 检查章节衔接问题 |
| **情绪曲线** | `python scripts/reviewer/emotion_curve.py 章节/ --volume --json` | 分析情绪变化曲线 |
| **伏笔追踪** | `python scripts/reviewer/foreshadowing_tracker.py 章节/ --json` | 追踪伏笔设置与回收 |
| **世界观检查** | `python scripts/auditor/worldbuilding_checker.py 章节/ --truth 真相/ --fix` | 检测世界观矛盾 |
| **世界观自动修复** | `python scripts/auditor/worldbuilding_checker.py 章节/ --truth 真相/ --apply` | 自动修复世界观矛盾 |
| **节奏优化** | `python scripts/auditor/pacing_optimizer.py 章节/ --json` | 生成节奏优化建议 |

## 文风推荐

| 题材 | 推荐作者 |
|------|---------|
| 玄幻修仙 | 天蚕土豆、辰东 |
| 都市搞笑 | 弈青峰、会说话的肘子 |
| 仙侠探案 | 卖报小郎君 |
| 悬疑诡秘 | 爱潜水的乌贼 |
| 历史权谋 | 猫腻、愤怒的香蕉 |

## 节奏规则

- ❌ 不能连续3章S4/S5(疲劳)
- ❌ 不能连续3章S1/S2(弃读)
- ✅ 每5-8章必须有S4或S5
- ✅ 每3章必须有S3或更高
- 📊 情绪单元: 每3章"压-小扬-压-爆"

## 爽点密度追踪

| 核心要素 | 说明 |
|----------|------|
| 爽点类型 | 打脸/装逼/逆袭/升级 |
| 出现频率 | 每N章必须出现 |
| 密度阈值 | 上限/下限预警 |

📄 详细规则: `skill/references/sweet-spot-tracking.md`

## 文件位置

```
创作元数据: .novel-maker/ (宪法/真相文件/报告/总结)
小说正文:   novels/ (大纲+分卷章节)
技能目录:   skill/ (agents/references/templates/styles/scripts)
```

## 真相文件 (8个)

- `characters.md` - 角色档案
- `current-state.md` - 世界状态
- `world-setting.md` - 世界观
- `pending-hooks.md` - 伏笔表
- `power-system.md` - 力量体系
- `emotional-arcs.md` - 情感弧线追踪
- `subplot-board.md` - 支线看板
- `timeline.md` - 时间线追踪

## 角色语音卡

| 核心要素 | 说明 |
|----------|------|
| 口癖 | 标志性口头禅 |
| 句式 | 说话习惯/句式结构 |
| 情感表达 | 情绪外露方式 |
| 思维模式 | 决策/反应模式 |

📄 详细规则: `skill/references/character-voice-card.md`

## 场景规划卡

| 核心要素 | 说明 |
|----------|------|
| 场景目标 | 本场景核心目的 |
| 情感基调 | 本场景主情绪 |
| 节奏等级 | S1-S5 对应 |
| 伏笔埋设 | 埋/收/推进 |

## 编辑视角审查

| 核心要素 | 说明 |
|----------|------|
| 编辑视角 | 商业编辑审稿标准 |
| 读者体验 | 可读性/代入感评估 |
| 商业价值 | 市场潜力/卖点分析 |

📄 详细规则: `skill/references/editorial-perspective.md`
