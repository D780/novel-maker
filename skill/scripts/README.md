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

## 统一分析脚本 (推荐)

### analyze.py — 三合一分析 (新增)

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
- `--format table`: 表格格式(供人类阅读)
- `--format text`: 简洁文本(供AI快速解析)

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
python scripts/truth_manager.py .novel-weaver/truth-files/ --json
python scripts/truth_manager.py .novel-weaver/truth-files/ --entity characters --json
```

输出：`characters`（角色名提取） / `pending-hooks`（伏笔提取） / `power-system` / `world-setting` / `current-state`

---

## 在 NovelWeaver 工作流中的位置

```
/novel-weaver write 继续
    ↓ ① python scripts/chapter_info.py 前章.md --json  → AI 读 ~200 token 代替 ~4000 token
    ↓ ② AI 写作 → 审查 → 更新大纲/记忆
    ↓ ③ python scripts/check_wordcount.py 本章.md      → 验证字数达标

/novel-weaver review
    ↓ ① python scripts/consistency_scan.py 章节/ 真相/ --json  → 一致性扫描
    ↓ ② python scripts/style_check.py 章节/ --json     → AI味检测
    ↓ ③ python scripts/hook_report.py 章节/ --json     → 钩子密度
    ↓ ④ python scripts/pacing_report.py 章节/ --json   → 节奏报告

/novel-weaver act 下一幕怎么走
    ↓ ① python scripts/volume_batch.py chapters/ --recent 5 --json  → 批量上下文
    ↓ ② python scripts/hook_report.py chapters/ --recent 5 --json   → 钩子趋势
    ↓ ③ AI 展示现状 + 6条分支 → 用户选择 → 偏离检查 → 同步更新

/novel-weaver stats
    ↓ python scripts/stats_report.py novels/ --json    → 项目统计

/novel-weaver summary
    ↓ python scripts/summary_generator.py chapters/ --last 10 --json  → 阶段总结辅助

/novel-weaver memory outline
    ↓ python scripts/outline_extractor.py novels/ --json → 大纲树

/novel-weaver memory entity
    ↓ python scripts/truth_manager.py truth-files/ --json → 真相文件管理
```
