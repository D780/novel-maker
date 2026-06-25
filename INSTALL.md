# NovelWeaver 安装指南

> 这是一个**技能仓库**，包含完整的网文创作技能定义，支持多种主流 AI IDE。

---

## 快速安装

### 一键安装（推荐）

```bash
cd /your/project
npx novel-weaver
```

脚本会自动检测你项目中使用的 IDE，将技能安装到正确位置。支持 18 款主流 AI 编程工具。

如果自动检测失败，可以显式指定：

```bash
npx novel-weaver --tool trae
```

卸载：

```bash
npx novel-weaver --uninstall
```

### 通用方式：复制安装（适用于所有 IDE）

将整个 `skill/` 目录复制到对应 IDE 的技能/规则目录中：

```bash
# macOS / Linux
cp -r skill/* <目标路径>/

# Windows PowerShell
Copy-Item -Path "skill\*" -Destination "<目标路径>" -Recurse
```

---

## 各 IDE 安装方式

| IDE | 类型 | 目标路径 |
|-----|------|----------|
| **Trae** | 技能 | `.trae/skills/novel-weaver/` |
| **Claude Code** | 技能 | `.claude/skills/novel-weaver/` |
| **Copilot CLI** | 技能 | `.claude/skills/novel-weaver/` |
| **Cursor** | 规则 | `.cursor/rules/novel-weaver/` |
| **Windsurf** | 技能 | `.windsurf/skills/novel-weaver/` |
| **Kiro** | 技能 | `.kiro/steering/novel-weaver/` |
| **Gemini CLI** | 技能 | `.gemini/skills/novel-weaver/` |
| **Codex CLI** | 技能 | `.codex/skills/novel-weaver/` |
| **Aider** | 技能 | `.aider/skills/novel-weaver/` |
| **OpenCode** | 技能 | `.opencode/skills/novel-weaver/` |
| **OpenClaw** | 技能 | `skills/novel-weaver/` |
| **Qwen Code** | 技能 | `.qwen/skills/novel-weaver/` |
| **Hermes Agent** | 技能 | `.hermes/skills/novel-weaver/` |
| **Claw Code** | 技能 | `.claw/skills/novel-weaver/` |
| **Qoder** | 技能 | `.qoder/skills/novel-weaver/` |
| **Antigravity** | 技能 | `.agents/skills/novel-weaver/` |
| **VS Code (Copilot)** | 自定义指令 | `.github/superpowers/novel-weaver/` |
| **DeerFlow** | 技能 | `skills/custom/novel-weaver/` |

---

### Trae（推荐）

```bash
# 项目内安装
cp -r skill/* .trae/skills/novel-weaver/

# 全局安装（所有项目可用）
cp -r skill/ ~/.trae/skills/novel-weaver/
```

安装后，在 Trae 聊天框输入 `/novel-weaver` 即可触发技能。

---

### Claude Code

```bash
# 项目内安装
cp -r skill/ .claude/skills/novel-weaver/

# 全局安装
cp -r skill/ ~/.claude/skills/novel-weaver/
```

Claude Code 的 Skill 支持**三级渐进加载**：
1. 启动时只读取 `name` + `description`（~100 token）
2. 需要时读取 `SKILL.md` 全文（<5000 token）
3. 按需加载 `references/`、`templates/`、`scripts/`

安装后说 "帮我写小说" 或输入 `/novel-weaver init` 即可触发。

---

### Cursor

Cursor 使用的是 `.mdc`（Markdown with Cursor frontmatter）规则文件，需要将 NovelWeaver 的内容转换为规则格式。

```bash
mkdir -p .cursor/rules/novel-weaver
```

推荐创建以下文件：

**`novel-writing.mdc`**（主规则）：
```
---
description: 网文写作技能，包含大纲生成、文风系统、节奏控制、质量审计
globs: **/*.md
---

# NovelWeaver 网文写作规则

当用户提到写小说、创作小说、写章节、写大纲时，使用以下指令体系：

- `/novel-weaver init` - 初始化小说项目
- `/novel-weaver write` - 写/续写章节
- `/novel-weaver review` - 审查质量
- `/novel-weaver memory` - 查看/管理设定
- `/novel-weaver plan` - 生成大纲
- `/novel-weaver act` - 下一幕剧情规划
- `/novel-weaver style` - 切换文风

完整规则请参考 skill/SKILL.md 和 references/ 目录下的文档。
```

---

### GitHub Copilot（VS Code）

```bash
mkdir -p .github/superpowers/novel-weaver
```

创建 **`.github/superpowers/novel-weaver/copilot-instructions.md`**：

```markdown
# NovelWeaver - 网文写作规则

当用户提到写小说、创作内容时，使用以下指令体系：

- `/novel-weaver init` - 初始化项目（6问引导：情绪标签→题材→简介→主角→冲突→章节数）
- `/novel-weaver write` - 写章节（自动触发黄金开篇、文风应用、质量审查、字数检查）
- `/novel-weaver review` - 质量审计（33维度：AI味、一致性、节奏、追读力）
- `/novel-weaver memory` - 管理设定（角色档案、世界状态、伏笔表）
- `/novel-weaver plan` - 生成大纲（三幕结构、分卷规划）
- `/novel-weaver act` - 幕规划（6条分支走向：A主线/B危机/C支线/D缓冲/E回环/F颠覆）

详细规则见 skill/ 目录。
```

Copilot 的指令是**全局被动生效**的，当聊天内容匹配时自动应用。

---

### Cline / Roo Code

**方式一：目录模式（推荐，多文件）**

```bash
cp -r skill/ .clinerules/novel-weaver/
```

**方式二：单文件模式**

将 `SKILL.md` 的内容直接复制到项目根目录的 `.clinerules` 文件中（如已存在则追加内容）。

Cline 会自动检测 `.clinerules` 目录或文件，也兼容 `.cursorrules`、`.windsurfrules`、`AGENTS.md` 等格式。

---

### Continue

```bash
mkdir -p .continue/rules
cp -r skill/ .continue/rules/novel-weaver/
```

或使用 YAML 配置方式，在 `config.yaml` 中添加：

```yaml
rules:
  - uses: file://.continue/rules/novel-weaver/
```

Continue 支持 `alwaysApply: true` 让规则全局生效，或使用 `globs: "**/*.md"` 限定文件类型。

---

### OpenCode

```bash
# OpenCode 原生路径
mkdir -p .opencode/skills/novel-weaver
cp -r skill/* .opencode/skills/novel-weaver/

# 或 Claude 兼容路径
cp -r skill/ .claude/skills/novel-weaver/
```

OpenCode 同时搜索 `.opencode/skills/`、`.claude/skills/`、`.agents/skills/` 三个路径。

---

## 符号链接（开发调试模式）

如果你要开发或调试这个技能，建议用符号链接指向仓库：

```bash
# 任意 IDE
ln -s $(pwd)/skill /path/to/project/.<ide>/skills/novel-weaver

# Windows (管理员权限)
mklink /D .trae\skills\novel-weaver d:\AITEST\novel-weaver\skill
```

这样修改仓库代码后会立即生效，无需重新复制。

---

## 安装验证

安装完成后，执行以下命令验证：

### Trae
输入 `/novel-weaver help`，如果返回帮助信息，说明安装成功。

### Claude Code
说 "帮我写小说"，如果AI询问你要写什么，说明安装成功。

### 自动验证（可选）
```bash
python scripts/init_guide.py --verify
```

---

## 目录结构说明

```
skill/                          # 技能根目录（整个复制到目标路径）
├── SKILL.md                    # 主技能文件（YAML frontmatter + Markdown）
├── README.md                   # 技能使用说明
├── agents/                     # 角色定义（6个）
│   ├── coordinator.md          # 协调者
│   ├── planner.md              # 规划师
│   ├── writer.md               # 写手
│   ├── auditor.md              # 审计师
│   ├── reviser.md              # 修订师
│   └── reviewer.md             # 复盘师
├── references/                 # 参考文档（24个）
│   ├── rhythm-system.md        # 节奏与情绪控制系统
│   ├── audit-core.md           # 15维度核心审计
│   ├── audit-dimensions.md     # 33维度完整审计
│   ├── anti-ai-patterns.md     # 反AI味指南
│   ├── anti-ai-techniques.md   # 去AI味技巧详解
│   ├── platform-rules.md       # 平台适配规则
│   ├── editorial-perspective.md # 编辑视角审查
│   ├── sweet-spot-tracking.md  # 爽点密度追踪
│   ├── character-voice-card.md # 角色语音卡指南
│   ├── style-imitation.md      # 文风模仿指南
│   ├── memory-system.md        # 记忆系统
│   ├── writing-methods.md      # 写作方法
│   ├── usage-guide.md          # 使用指南
│   ├── creative-constraints.md # 创意约束
│   ├── consistency-checker.md  # 一致性检查
│   ├── data-agent.md           # 实体管理
│   ├── golden-opening.md       # 黄金开篇
│   ├── content-expansion.md    # 内容扩充
│   ├── dialogue-writing.md     # 对话写作
│   ├── plot-structures.md      # 情节结构
│   ├── act-guidance.md         # 幕引导
│   ├── genre-rules.md          # 37种题材写作规则
│   ├── pacing-analysis.md      # 节奏分析
│   └── emotion-curve.md        # 情绪曲线
├── styles/                     # 文风库（22位作者，7大流派）
│   ├── author-styles.md
│   └── authors/
├── templates/                  # 模板文件（21个）
│   ├── INDEX.md                # 模板索引
│   ├── constitution.md         # 创作宪法
│   ├── outline.md              # 大纲（含幕层级）
│   ├── act-plan.md             # 幕计划
│   ├── volume-plan.md          # 卷计划
│   ├── chapter.md              # 章节模板
│   ├── character-profile.md    # 角色档案
│   ├── character-voice.md      # 角色语音卡
│   ├── scene-template.md       # 场景模板
│   ├── scene-plan.md           # 场景规划卡
│   ├── hook-template.md        # 伏笔管理
│   ├── plot-card.md            # 剧情卡片
│   ├── review-report.md        # 审查报告
│   ├── world-setting.md        # 世界观
│   ├── power-system.md         # 力量体系
│   ├── emotional-arcs.md       # 情感弧线追踪
│   ├── subplot-board.md        # 支线看板
│   ├── timeline.md             # 时间线追踪
│   ├── summary-10chapters.md   # 10章小总结
│   ├── summary-50chapters.md   # 50章大总结
│   └── summary-volume.md       # 卷总结
└── scripts/                    # Python 预处理脚本（14个文件）
    ├── README.md               # 脚本使用说明
    ├── nw_utils.py             # 公共工具模块
    ├── check_wordcount.py      # 字数检查
    ├── chapter_info.py         # 单章结构化提取（节省 ~90% token）
    ├── volume_batch.py         # 卷级批量汇总
    ├── hook_report.py          # 钩子密度报告
    ├── consistency_scan.py     # 一致性扫描
    ├── style_check.py          # AI味检测
    ├── stats_report.py         # 项目统计
    ├── pacing_report.py        # 节奏报告
    ├── summary_generator.py    # 阶段总结辅助
    ├── outline_extractor.py    # 大纲提取
    ├── truth_manager.py        # 真相文件管理
    └── analyze.py              # 综合分析
```

> **注意**：仓库中的 `docs/` 目录是开发文档，安装时无需复制。只需复制 `skill/` 目录即可。

---

## 常见问题

### Q: 安装后 AI 没识别到技能？

A: 检查以下几点：
1. 确认路径正确（注意是 `skills/novel-weaver/` 不是直接 `skills/`）
2. 确认 `SKILL.md` 存在于目录根
3. 重启 IDE 会话
4. 输入 `/novel-weaver help` 手动触发

### Q: 可以全局安装吗？

A: 可以。全局路径一般为 `~/.<ide>/skills/novel-weaver/`，所有项目都能使用。

### Q: 脚本需要额外安装依赖吗？

A: 不需要。所有 Python 脚本只使用标准库（`os`、`re`、`json`、`argparse`、`pathlib`）。

### Q: 这个技能仓库和 MCP 有什么区别？

A: MCP 是外部服务接口协议，需要运行额外进程；Skill 是纯 Markdown 指令包，零依赖、零配置、无需启动，开箱即用。
