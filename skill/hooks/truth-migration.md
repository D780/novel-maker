# Truth-File Migration Hook

## 概述

当技能升级后，新版本可能引入新的 truth-files，而旧项目没有这些文件。本 hook 定义了迁移检查规则和自动创建流程，由协调者在每次工作流开始时执行。

## 迁移清单

每个 truth-file 对应的模板和迁移策略：

| Truth-File | 模板 | 默认内容 | 迁移策略 |
|-----------|------|---------|---------|
| `current-state.md` | 无 | `# 当前状态\n\n- 世界状态：待初始化\n- 角色状态：待初始化\n- 剧情进展：待初始化` | 创建默认 |
| `pending-hooks.md` | `skill/templates/hook-template.md` | 空伏笔列表 | 创建默认 |
| `characters.md` | `skill/templates/character-profile.md` | 空角色列表 | 创建默认 |
| `world-setting.md` | `skill/templates/world-setting.md` | 空世界观列表 | 创建默认 |
| `power-system.md` | `skill/templates/power-system.md` | 空力量体系 | 创建默认 |
| `emotional-arcs.md` | `skill/templates/emotional-arcs.md` | 空情感弧线 | 创建默认 |
| `timeline.md` | `skill/templates/timeline.md` | 空时间线 | 创建默认 |
| `subplot-board.md` | `skill/templates/subplot-board.md` | 空支线看板 | 创建默认 |

## 迁移检测

### 检测时机

协调者每次开始工作流时，作为第一步执行（在任何 sub-agent 调度之前）。

### 检测方法

检查 `.novel-maker/truth-files/` 目录是否存在每个 truth-file：

```python
expected_files = [
    "current-state.md",
    "pending-hooks.md",
    "characters.md",
    "world-setting.md",
    "power-system.md",
    "emotional-arcs.md",
    "timeline.md",
    "subplot-board.md"
]

missing = [f for f in expected_files if not os.path.exists(f"truth-files/{f}")]
```

### 创建规则

#### 1. 有模板的 truth-file（7个）

从对应模板创建初始文件，替换占位符为默认值：

```
[文件名] → 读取 skill/templates/[模板].md → 将占位符替换为默认值 → 写入 truth-files/[文件名]
```

**默认值规则**：
- `[角色名]` → `(待创建)`
- `[地点]` → `(待创建)`
- 所有 `[占位符]` → 清空或置为 `(待创建)`
- 模板结构保留，以便后续直接填入数据

#### 2. 无模板的 truth-file（current-state.md）

创建最小初始版本：

```markdown
# 当前状态

- 世界状态：待初始化
- 角色状态：待初始化
- 剧情进展：待初始化
```

#### 3. 需要回填数据（可选）

如果已有已完成章节且需要从已有内容提取数据，可以通过脚本辅助。由协调者评估是否需要：

```bash
python skill/scripts/reviewer/character_arc_tracker.py --dir novels/volume-1/chapters/
python skill/scripts/reviewer/emotion_curve.py --dir novels/volume-1/chapters/
python skill/scripts/reviewer/foreshadowing_tracker.py --dir novels/volume-1/chapters/
python skill/scripts/reviewer/chapter_diff.py --dir novels/volume-1/chapters/
```

## 迁移流程

### 完整步骤

```
[协调者] 收到用户请求
  → 第一步：执行迁移检查
     1. 列出 truth-files/ 下缺失的文件
     2. 无缺失 → 跳过迁移，继续正常流程
     3. 有缺失 → 进入迁移流程
  → 第二步：创建缺失文件
     1. 有模板的 → 从模板创建
     2. 无模板的 → 创建默认内容
  → 第三步：记录迁移状态
  → 第四步：评估是否需要回填
     1. 缺失 1-3 个 → 创建后继续，不额外处理
     2. 缺失 4 个以上 → AskUserQuestion 是否运行脚本提取已有章节数据
  → 继续正常流程
```

### 迁移状态记录

迁移完成后，将记录写入 `.novel-maker/truth-files/.migration.json`：

```json
{
  "migration": {
    "version": "当前技能版本号",
    "date": "执行迁移的日期",
    "created": ["被创建的文件列表"],
    "total_missing": 2,
    "backfilled": false,
    "status": "completed"
  }
}
```

如果后续版本再次升级，检查 `.migration.json` 中的 `version` 字段与当前版本是否一致，不一致则触发新一轮迁移。

### 处理策略汇总

| 场景 | 处理方式 |
|------|---------|
| 无缺失文件 | 跳过迁移，继续正常流程 |
| 缺失 1-3 个 | 创建后继续，不额外处理 |
| 缺失 4 个以上 | 创建后 AskUserQuestion 是否回填已有数据 |
| 所有文件都缺失 | 视为全新项目，创建后正常初始化 |
| 已有迁移记录但版本不匹配 | 重新检查并创建新增的 truth-file，保留已有文件 |

## 注意事项

1. **只创建不覆盖**：如果文件已存在，绝不修改其内容
2. **增量升级**：如果 A 版本有 6 个文件、B 版本有 8 个文件，升级只创建新增的 2 个
3. **迁移记录留存**：`.migration.json` 记录每次升级，方便追溯
4. **回填非强制**：回填脚本是可选项，由用户决定是否执行
5. **模板保留结构**：从模板创建时保留完整的 Markdown 结构，方便后续直接填入