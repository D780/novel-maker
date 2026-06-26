# 辅助脚本

预处理章节数据和项目文件，将全文（~4000 token）压缩为结构化 JSON（~200 token），**节省约 90% token 消耗**。

所有脚本共用 `nw_utils.py` 公共模块，提供 Markdown 清理、字数统计、角色提取、地点提取、钩子检测、章节排序、摘要生成、节奏评级、大纲解析、真相文件读取等工具函数。

---

## nw_utils.py — 公共工具模块

所有脚本共用的基础函数，脚本通过 `from nw_utils import ...` 调用：

| 函数 | 说明 |
|------|------|
| `clean_markdown(text)` | 去除 Markdown 格式标记 |
| `count_chinese(text)` | 统计中文字符数 |
| `extract_title(content)` | 提取章节标题 |
| `read_chapter(filepath)` | 读取章节，返回 `(raw, title, clean, wc)` |
| `extract_content_from_chapter(path)` | 提取章节正文（跳过标题行） |
| `extract_characters(text)` | 从对话模式提取角色名（已过滤代词/动词噪音） |
| `extract_locations(text)` | 从位移模式提取地点名 |
| `detect_hook(text)` | 检测章节结尾钩子类型（6种） |
| `detect_hook_type_from_patterns(text)` | 用预编译正则快速检测钩子类型 |
| `generate_summary(text)` | 生成开头+结尾摘要 |
| `detect_structure(text)` | 检测对话/动作/描写比例 |
| `estimate_pacing(text)` | 估算章节节奏等级（S1-S5） |
| `parse_outline_headings(text)` | 解析 Markdown 大纲标题树 |
| `read_truth_section(filepath)` | 解析真相文件分段内容 |
| `chapter_sort_key(filepath)` | 章节文件名排序键（支持中文数字） |
| `list_chapters(dir, recent_n)` | 列出目录中排序后的章节文件 |

---

## init_guide.py — 初始化引导脚本

**用途：** 交互式引导脚本，帮助用户完成初始化流程

**使用方式：**
```bash
python scripts/init_guide.py [--ide trae|claude] [--auto] [--verify]
```

**参数说明：**
- `--ide`: 指定IDE类型（trae 或 claude）
- `--auto`: 自动模式，使用默认配置
- `--verify`: 验证安装是否成功

**示例：**
```bash
# 交互式引导
python scripts/init_guide.py

# 指定IDE类型
python scripts/init_guide.py --ide trae

# 自动模式
python scripts/init_guide.py --auto

# 验证安装
python scripts/init_guide.py --verify
```

---

## 统一分析脚本 (推荐)

### analyze.py — 三合一分析

整合了 `chapter_info.py` + `style_check.py` + `hook_report.py` 的功能,支持三种模式:

```bash
# 单章分析 (代替 chapter_info.py)
python scripts/analyze.py novels/volume-01/chapters/ch01.md --mode single --json

# 风格检测 (代替 style_check.py)
python scripts/analyze.py novels/volume-01/chapters/ch01.md --mode style --json

# 批量分析 (代替 hook_report.py + 卷级统计)
python scripts/analyze.py novels/volume-01/chapters/ --mode batch --recent 5 --json
```

**输出模式**:
- `--json`: 纯JSON格式(供AI读取)
- 默认: 人类可读格式

**批量模式增强功能**:
- 钩子类型分布 + 连续相同钩子警告
- 节奏S1-S5分布 + 连续高潮/平淡警告
- 总字数/均章字数统计

---

## 写作流程脚本

### check_wordcount.py — 字数检查

```bash
python scripts/check_wordcount.py novels/volume-01/chapters/ch01.md
python scripts/check_wordcount.py novels/volume-01/chapters/ch01.md 2500 3500  # 自定义区间
python scripts/check_wordcount.py --all novels/volume-01/chapters/              # 批量检查
```

### chapter_info.py — 单章结构化提取

```bash
python scripts/chapter_info.py novels/volume-01/chapters/ch01.md --json
```

输出：`word_count` / `characters` / `locations` / `structure` / `hook` / `summary`

### volume_batch.py — 卷级批量汇总

```bash
python scripts/volume_batch.py novels/volume-01/chapters/ --json
python scripts/volume_batch.py novels/volume-01/chapters/ --recent 5 --json
```

输出：`total_chapters` / `total_words` / `chapters[]` / `main_characters` / `character_matrix` / `foreshadowing_summary` / `hook_distribution`

---

## 审查脚本

### consistency_scan.py — 一致性扫描

```bash
python scripts/consistency_scan.py novels/volume-01/chapters/ novels/volume-01/truth-files/ --json
```

输出：`truth_characters_count` / `summary`（新角色/等级冲突/警告）

### style_check.py — AI味检测

```bash
python scripts/style_check.py novels/volume-01/chapters/ch01.md --json
python scripts/style_check.py novels/volume-01/chapters/ --recent 5 --json
```

输出：`ai_density_per_1000` / `ai_words_found` / `repetitive_words` / `dialogue_ratio_pct` / `issues`

### hook_report.py — 钩子密度报告

```bash
python scripts/hook_report.py novels/volume-01/chapters/ --json
python scripts/hook_report.py novels/volume-01/chapters/ --recent 5 --json
```

输出：`hook_distribution` / `warnings`（连续相同钩子/未知钩子）

### pacing_report.py — 卷级节奏报告

```bash
python scripts/pacing_report.py novels/volume-01/chapters/ --json
python scripts/pacing_report.py novels/volume-01/chapters/ --recent 10 --json
```

输出：`pacing_distribution`（S1-S5分布） / `problems`（连续高潮/平淡/峰值间隔） / `read_trends`（追读力趋势） / `suggestions`

---

## 统计与总结脚本

### stats_report.py — 项目统计报告

```bash
python scripts/stats_report.py novels/ --json
python scripts/stats_report.py novels/ --volume volume-01 --json
```

输出：`volumes` / `total_chapters` / `total_words` / `volume_details`（章节/角色/场景/节奏分布）

### summary_generator.py — 阶段总结辅助

```bash
python scripts/summary_generator.py novels/volume-01/chapters/ --range 1-10 --json
python scripts/summary_generator.py novels/volume-01/chapters/ --last 5 --json
```

输出：`timeline`（每章角色/开头/结尾/钩子） / `characters_involved` / `locations_visited`

---

## 大纲与实体脚本

### outline_extractor.py — 大纲快速提取

```bash
python scripts/outline_extractor.py novels/ --json
python scripts/outline_extractor.py novels/outline.md --json
```

输出：`outline` / `volume-01` / `volume-01/act-plan` 等文件的标题树

### truth_manager.py — 真相文件管理器

```bash
python scripts/truth_manager.py .novel-maker/truth-files/ --json
python scripts/truth_manager.py .novel-maker/truth-files/ --entity characters --json
```

输出：`characters`（角色名提取） / `pending-hooks`（伏笔提取） / `power-system` / `world-setting` / `current-state`

---

## 安装脚本

### install.py — Python 安装脚本

当 `npx novel-maker` 不可用时的备选方案：

```bash
python scripts/install.py [--tool trae|claude|cursor] [--list]
```

---

## 智能查询脚本

### query_engine.py — 智能查询引擎

4种查询类型：角色查询、设定查询、剧情查询、伏笔查询。

```bash
python scripts/query_engine.py '林风是什么等级？'
python scripts/query_engine.py --type character '林风'
python scripts/query_engine.py --type foreshadow '魔剑'
```

---

## 风格分析脚本

### style_anchor.py — 风格锚点提取

从最近5章提取句长分布、对话比例、高频词，输出 style-anchor.json。

```bash
python scripts/style_anchor.py novels/volume-01/chapters/
python scripts/style_anchor.py novels/volume-01/chapters/ --recent 10 --json
```

输出：`avg_sentence_length` / `dialogue_ratio` / `top_words` / `style_signature`

---

## 节奏可视化脚本

### pacing_visualize.py — 节奏可视化

支持单章/卷/全局三种模式，输出 emoji 标记和热力图数据。

```bash
python scripts/pacing_visualize.py --volume novels/volume-01/
python scripts/pacing_visualize.py --all novels/
python scripts/pacing_visualize.py --chapter novels/volume-01/chapters/ch01.md
```

输出：`pacing_map`（emoji标记） / `heatmap`（热力图数据） / `emotion_stats`（情绪统计）

---

## Token 优化脚本

### build_write_context.py — 写手上下文构建器

一键生成写作所需的精简上下文，将 15+ 个文件压缩为 ~3000 token 的 JSON。

```bash
python scripts/build_write_context.py novels/volume-01/chapters/ch15.md --json
python scripts/build_write_context.py --chapter 15 --volume 01 --json
```

输出：`truth_files`（精简真相文件） / `prev_chapters`（前章摘要） / `outline`（大纲目标） / `constitution`（宪法要点）

**节省：每章约 40,000-60,000 token**

### pre_audit.py — 预审计管线

一键运行所有可自动化的审计维度（字数/钩子/节奏/AI味/一致性）。

```bash
python scripts/pre_audit.py novels/volume-01/chapters/ch15.md --json
```

输出：`word_count` / `characters` / `hook` / `pacing` / `ai_style` / `consistency` / `summary`

**节省：每章约 20,000-30,000 token**

### truth_diff.py — 真相文件变更检测

自动检测章节变更并生成更新 diff（新角色/新地点/伏笔/情感）。

```bash
python scripts/truth_diff.py ch15.md --truth-dir .novel-maker/truth-files/ --prev ch14.md --json
```

输出：`new_characters` / `new_locations` / `hook_keywords` / `emotions` / `continuing_characters`

**节省：每章约 35,000-50,000 token**

### planner_context.py — 规划师上下文包

一键生成规划所需的精简上下文，将 10+ 个文件压缩为 ~5000 token 的 JSON。

```bash
python scripts/planner_context.py --volume 01 --act 2 --json
```

输出：`volume_progress`（卷进度） / `truth_files`（真相文件摘要） / `outline`（大纲目标） / `active_hooks`（活跃伏笔） / `active_subplots`（活跃支线）

**节省：每次规划约 25,000 token**

### chapter_diff.py — 章节修订对比

比较原稿和修订稿的结构化差异（角色/伏笔/字数/结构/节奏）。

```bash
python scripts/chapter_diff.py temp/draft.md temp/revised.md --json
```

输出：`word_count` / `characters` / `locations` / `hook` / `structure` / `pacing` / `summary`

**节省：每次修订约 8,000 token**

---

## 验证脚本

### validate.py — 技能完整性验证

验证所有技能文件的完整性和正确性（脚本语法/文件引用/角色/题材包/弧线模板/规则/模板/Hook）。

```bash
python scripts/validate.py
```

输出：134项检查结果（通过/警告/失败），覆盖8个维度。

---

## 在 NovelMaker 工作流中的位置

```
/novel-maker write 继续
    ↓ ① python scripts/chapter_info.py 前章.md --json  → AI 读 ~200 token 代替 ~4000 token
    ↓ ② AI 写作 → 审查 → 更新大纲/记忆
    ↓ ③ python scripts/check_wordcount.py 本章.md      → 验证字数达标

/novel-maker review
    ↓ ① python scripts/consistency_scan.py 章节/ 真相/ --json  → 一致性扫描
    ↓ ② python scripts/style_check.py 章节/ --json     → AI味检测
    ↓ ③ python scripts/hook_report.py 章节/ --json     → 钩子密度
    ↓ ④ python scripts/pacing_report.py 章节/ --json   → 节奏报告

/novel-maker act 下一幕怎么走
    ↓ ① python scripts/volume_batch.py chapters/ --recent 5 --json  → 批量上下文
    ↓ ② python scripts/hook_report.py chapters/ --recent 5 --json   → 钩子趋势
    ↓ ③ AI 展示现状 + 6条分支 → 用户选择 → 偏离检查 → 同步更新

/novel-maker stats
    ↓ python scripts/stats_report.py novels/ --json    → 项目统计

/novel-maker summary
    ↓ python scripts/summary_generator.py chapters/ --last 10 --json  → 阶段总结辅助

/novel-maker memory outline
    ↓ python scripts/outline_extractor.py novels/ --json → 大纲树

/novel-maker memory entity
    ↓ python scripts/truth_manager.py truth-files/ --json → 真相文件管理
```
