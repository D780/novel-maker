# Chapter Complete Hook

## 概述

在章节完成后自动更新大纲、记忆文件、伏笔表等，确保项目状态与写作进度同步。

## 触发时机

- `/novel-maker write` 执行完成后
- 用户确认章节内容后

## 更新内容

### 1. 更新大纲

**操作**：标记当前章节为已完成状态

**文件**：`novels/outline.md`

**更新内容**：
- 将章节状态从"待写"改为"已完成"
- 添加章节完成时间
- 添加章节摘要

**示例**：
```markdown
## 第三幕：高潮

### 第50章 王都风云 [已完成] 2026-06-26
- 林风进入王都
- 遭遇皇室势力
- 古剑·风吟封印觉醒
- 字数：3200字
```

### 2. 更新记忆文件

**操作**：更新世界状态和角色状态

**文件**：`truth-files/current-state.md`

**更新内容**：
- 角色状态变化
- 世界状态变化
- 新获得的物品/技能

**示例**：
```markdown
## 世界状态

### 角色状态
- 林风：高级修士，当前在王都，获得古剑·风吟（已解封）
- 苏雨：医修，当前在林风身边

### 物品状态
- 古剑·风吟：已解封，剑灵觉醒
```

### 3. 更新伏笔表

**操作**：标记伏笔回收状态

**文件**：`truth-files/pending-hooks.md`

**更新内容**：
- 标记已回收的伏笔
- 添加新埋设的伏笔
- 更新伏笔状态

**示例**：
```markdown
## 伏笔表

### 古剑·风吟 [已回收]
- 埋设：第3章，神秘老人赠剑
- 回收：第50章，剑中封印觉醒
- 状态：已回收

### 神秘老人身份 [未回收]
- 埋设：第3章，老人身份成谜
- 预期回收：第80章
- 状态：未回收
```

### 4. 生成章节摘要

**操作**：生成本章摘要供后续参考

**文件**：`.novel-maker/summaries/chapter-XX-summary.md`

**摘要内容**：
- 章节主要事件
- 角色状态变化
- 新埋设的伏笔
- 关键转折点

**示例**：
```markdown
# 第50章摘要

## 主要事件
- 林风进入王都
- 遭遇皇室势力阻挠
- 古剑·风吟封印觉醒，剑灵现身

## 角色变化
- 林风：获得剑灵协助，实力提升
- 苏雨：与林风汇合

## 伏笔
- 新埋设：皇室势力的目的
- 已回收：古剑·风吟封印

## 关键转折
- 剑灵觉醒，揭示古剑来历
```

## 实现逻辑

```python
def chapter_complete(project_dir: str, chapter_num: int, chapter_content: str):
    """章节完成后的自动更新"""
    
    # 1. 更新大纲
    update_outline(project_dir, chapter_num, status="已完成")
    
    # 2. 更新记忆文件
    update_current_state(project_dir, chapter_content)
    
    # 3. 更新伏笔表
    update_pending_hooks(project_dir, chapter_num, chapter_content)
    
    # 4. 生成章节摘要
    generate_chapter_summary(project_dir, chapter_num, chapter_content)
```

## 输出格式

```markdown
【章节完成更新】

✅ 大纲已更新：第50章标记为已完成
✅ 记忆文件已更新：角色状态、世界状态
✅ 伏笔表已更新：标记1个伏笔回收，新增1个伏笔
✅ 章节摘要已生成：.novel-maker/summaries/chapter-50-summary.md

【幕内进度】
当前幕：第三幕 - 高潮
进度：第50章 / 共60章（83%）
下一章：第51章 - 皇室阴谋
```

## 配置选项

```json
{
  "chapter-complete": {
    "enabled": true,
    "priority": 2,
    "options": {
      "update_outline": true,
      "update_memory": true,
      "update_hooks": true,
      "generate_summary": true,
      "show_progress": true
    }
  }
}
```

## 强制检查清单（每章必做）

章节完成后，必须按顺序执行以下检查：

### 1. 字数检查（强制）
- [ ] 字数在 2500-4000 字范围内
- [ ] 若低于 2500 字，必须扩写
- [ ] 若高于 4000 字，必须精简

### 2. 红线自检（强制）
- [ ] 对话占比 ≤50%
- [ ] 称呼密度 ≤8次/千字
- [ ] 无重复对话、连续短问句、复读机对话
- [ ] 无无意义省略号
- [ ] AI高频词 ≤3处
- [ ] 无称呼堆砌、情绪标签化、公式化转场

### 3. Truth-Files 更新清单（强制）
每章完成后必须勾选：
- [ ] `current-state.md` - 更新世界状态
- [ ] `pending-hooks.md` - 更新伏笔状态（如有新伏笔/回收）
- [ ] 是否有新角色/地点/势力？→ 更新 `characters.md` / `world-setting.md`
- [ ] 是否跨5章？→ 更新 `timeline.md` / `emotional-arcs.md` / `characters.md`
- [ ] 是否跨幕？→ 更新 `subplot-board.md` / `emotional-arcs.md`

### 4. 总结检查（强制）
- [ ] 当前章节是否为10的倍数？→ 必须生成小总结
- [ ] 当前章节是否为50的倍数？→ 必须生成大总结
- [ ] 当前章节是否为卷末？→ 必须生成卷总结

### 5. 规划偏离检查（每10章必做）
- [ ] 对比 `plan.md` 与实际剧情
- [ ] 若剧情偏离原计划，提示用户："当前剧情与 plan.md 第X幕规划不一致，是否更新计划？"

## 注意事项

1. 章节完成后必须执行此 Hook，确保项目状态同步
2. 如果某些文件不存在，会跳过对应更新
3. 更新操作是增量的，不会覆盖已有内容
4. 章节摘要会保存供后续章节参考
5. **所有强制检查项必须完成，否则不能交付章节**

## 步骤衔接规则

章节完成后，复盘师必须：

1. 读取写手输出的【步骤交接摘要】
2. 执行本 hook 的所有强制检查
3. 更新相关 truth-files
4. 输出【步骤交接摘要 - 复盘师】：

```markdown
【步骤交接摘要 - 复盘师】
- 章节：chXX
- truth-files 更新状态：全部完成 / 待补充
- 伏笔状态：X个未回收
- 规划偏离：无 / [偏离点描述]
- 下一步骤：写手继续写 chXX+1 / 审计师深度审查 / 规划师调整 plan.md
```

5. 将摘要保存到 `.novel-maker/state/last-step-summary.md`
