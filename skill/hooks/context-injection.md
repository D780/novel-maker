# Context Injection Hook

## 概述

在写作前自动注入上下文信息，包括角色状态、世界观设定、前情摘要等，确保 AI 写作时有足够的背景信息。

## 触发时机

- `/novel-maker write` 执行前
- 用户开始新章节写作时

## 注入内容

### 1. 角色状态

**来源**：`truth-files/characters.md` + `truth-files/current-state.md`

**注入内容**：
- 主要角色当前状态（等级、位置、情绪）
- 角色关系网络
- 角色近期经历

**示例**：
```markdown
【角色状态】
- 林风：高级修士，当前在王都，情绪：警惕
- 苏雨：医修，当前在林风身边，情绪：担忧
- 关系：林风与苏雨是恋人关系
```

### 2. 世界观设定

**来源**：`truth-files/world-setting.md` + `truth-files/power-system.md`

**注入内容**：
- 当前地点设定
- 相关力量体系规则
- 社会制度约束

**示例**：
```markdown
【世界观设定】
- 当前地点：王都，大陆中央，政治经济中心
- 修炼体系：剑修/法修/体修，等级：初级→中级→高级→大师→宗师
- 社会制度：皇权至上，修士有特权但受皇室约束
```

### 3. 前情摘要

**来源**：`.novel-maker/summaries/` + 前2章内容

**注入内容**：
- 前2章摘要
- 当前剧情进展
- 未解决的伏笔

**示例**：
```markdown
【前情摘要】
- 第48章：林风击败张天，获得古剑·风吟的线索
- 第49章：林风与苏雨汇合，准备前往王都
- 未解决伏笔：神秘老人身份、古籍预言、林风的怪病
```

### 4. 本章目标

**来源**：`outline.md` / `volume-XX/plan.md`

**注入内容**：
- 本章在大纲中的定位
- 预期剧情走向
- 需要埋设/回收的伏笔

**示例**：
```markdown
【本章目标】
- 大纲定位：第50章，第三幕高潮
- 预期走向：林风进入王都，遭遇皇室势力
- 伏笔回收：古剑·风吟封印觉醒
```

## 实现逻辑

```python
def context_injection(project_dir: str, chapter_num: int) -> str:
    """注入上下文信息"""
    context = []
    
    # 1. 加载角色状态
    characters = load_characters(project_dir)
    current_state = load_current_state(project_dir)
    context.append(format_character_status(characters, current_state))
    
    # 2. 加载世界观设定
    world_setting = load_world_setting(project_dir)
    power_system = load_power_system(project_dir)
    context.append(format_world_setting(world_setting, power_system))
    
    # 3. 加载前情摘要
    summaries = load_recent_summaries(project_dir, count=2)
    context.append(format_previous_summary(summaries))
    
    # 4. 加载本章目标
    outline = load_outline(project_dir)
    chapter_goal = extract_chapter_goal(outline, chapter_num)
    context.append(format_chapter_goal(chapter_goal))
    
    return "\n\n".join(context)
```

## 输出格式

```markdown
【写作上下文】
## 角色状态 → 来自 truth-files/characters.md + current-state.md
[角色状态内容]

## 世界设定 → 来自 truth-files/world-setting.md + power-system.md
[世界设定内容]

## 前情摘要 → 来自 .novel-maker/summaries/ + 前2章摘要
[前情摘要内容]

## 本章目标 → 来自 outline.md / volume-XX/plan.md
[本章目标内容]
```

## 配置选项

```json
{
  "context-injection": {
    "enabled": true,
    "priority": 1,
    "options": {
      "include_characters": true,
      "include_world_setting": true,
      "include_previous_summary": true,
      "include_chapter_goal": true,
      "summary_count": 2,
      "max_context_length": 2000
    }
  }
}
```

## 注意事项

1. 上下文注入不会修改任何文件，只读取信息
2. 如果某些文件不存在，会跳过对应部分
3. 上下文长度有上限，避免占用过多 token
4. 可以通过配置禁用不需要的部分
