# Review Trigger Hook

## 概述

在每章完成后自动触发质量审查，检查内容质量、一致性、AI味等问题，生成审查报告。

## 触发时机

- `chapter-complete` Hook 执行完成后
- 每章写作完成后

## 审查维度

### 1. AI味检测

**检查内容**：
- 广告词过度使用
- 情感标签化
- 对话形式化
- 结构闭合化
- 转场公式化
- 总结倾向
- 信息曝光过度

**参考规则**：`skill/rules/anti-ai-expressions.md`

**输出示例**：
```markdown
## AI味检测

### 发现的问题
1. 第15行："他的眼中闪过一丝坚定" - 情感标签化
2. 第23行："他深吸一口气，心中暗道" - 对话形式化
3. 第45行："就这样，他们成功了" - 结构闭合化

### 建议
1. 改为具体描写："他攥紧拳头，指节发白"
2. 改为内心独白："不行，必须这么做"
3. 改为开放式结尾："故事还没结束..."
```

### 2. 一致性检查

**检查内容**：
- 时间线一致性
- 人物关系一致性
- 世界观一致性
- 伏笔回收情况
- 能力等级一致性

**参考规则**：`skill/rules/consistency-check.md`

**输出示例**：
```markdown
## 一致性检查

### 时间线
✅ 时间线一致，无矛盾

### 人物关系
✅ 角色称呼一致
⚠️ 林风对苏雨的称呼从"苏姑娘"变为"雨儿"，需确认是否有铺垫

### 世界观
✅ 修炼体系一致
✅ 地理设定一致

### 伏笔回收
✅ 古剑·风吟伏笔已回收
⚠️ 神秘老人身份伏笔未回收（预期第80章）

### 能力等级
✅ 林风实力提升有铺垫
✅ 战斗结果符合实力对比
```

### 3. 角色声音检查

**检查内容**：
- 语言习惯一致性
- 情感表达合理性
- 知识边界遵守
- 行为逻辑一致
- 关系互动正确

**参考规则**：`skill/rules/character-voice.md`

**输出示例**：
```markdown
## 角色声音检查

### 林风
✅ 语言习惯：短句、口语化，符合战士人设
✅ 情感表达：愤怒时直接表达，符合性格
⚠️ 第30行使用了"此乃"等书面语，与人设不符

### 苏雨
✅ 语言习惯：长句、书面化，符合医修人设
✅ 情感表达：内敛含蓄，符合性格
```

### 4. 风格锚点检查

**检查内容**：
- 句长分布是否符合设定
- 对话比例是否合理
- 高频词是否一致

**参考脚本**：`skill/scripts/style_anchor.py`

**输出示例**：
```markdown
## 风格锚点检查

### 句长分布
- 平均句长：18字（目标：15-20字）✅
- 短句比例：35%（目标：30-40%）✅
- 长句比例：15%（目标：10-20%）✅

### 对话比例
- 对话占比：42%（目标：35-50%）✅

### 高频词
- 与前5章一致性：85%（目标：>80%）✅
```

## 实现逻辑

```python
def review_trigger(project_dir: str, chapter_num: int, chapter_content: str):
    """触发质量审查"""
    
    report = []
    
    # 1. AI味检测
    ai_slop_report = detect_ai_slop(chapter_content)
    report.append(format_ai_slop_report(ai_slop_report))
    
    # 2. 一致性检查
    consistency_report = check_consistency(project_dir, chapter_num, chapter_content)
    report.append(format_consistency_report(consistency_report))
    
    # 3. 角色声音检查
    voice_report = check_character_voice(project_dir, chapter_content)
    report.append(format_voice_report(voice_report))
    
    # 4. 风格锚点检查
    style_report = check_style_anchor(project_dir, chapter_content)
    report.append(format_style_report(style_report))
    
    # 保存审查报告
    save_review_report(project_dir, chapter_num, report)
    
    return report
```

## 输出格式

```markdown
【质量审查报告】

## 第50章审查结果

### 总体评分：B+

### AI味检测
- 发现3个问题
- 严重程度：低

### 一致性检查
- 时间线：✅ 通过
- 人物关系：⚠️ 1个警告
- 世界观：✅ 通过
- 伏笔回收：⚠️ 1个警告
- 能力等级：✅ 通过

### 角色声音检查
- 林风：✅ 通过
- 苏雨：✅ 通过

### 风格锚点检查
- 句长分布：✅ 通过
- 对话比例：✅ 通过
- 高频词：✅ 通过

### 建议
1. 修复3个AI味问题
2. 确认林风对苏雨称呼变化是否有铺垫
3. 记录神秘老人身份伏笔待回收

【审查报告已保存】.novel-maker/reviews/chapter-50-review.md
```

## 配置选项

```json
{
  "review-trigger": {
    "enabled": true,
    "priority": 3,
    "options": {
      "check_ai_slop": true,
      "check_consistency": true,
      "check_voice": true,
      "check_style": true,
      "save_report": true,
      "show_report": true,
      "auto_fix": false
    }
  }
}
```

## 注意事项

1. 审查报告会保存供后续参考
2. 可以通过配置禁用不需要的审查维度
3. `auto_fix` 选项可以自动修复一些简单问题
4. 审查结果会影响后续的修订流程
