# Summary Trigger Hook

## 概述

在每10章或50章完成后自动生成阶段总结，回顾剧情进展、角色成长、伏笔状态等。

## 触发时机

- 每10章完成后（小总结）
- 每50章完成后（大总结）
- 每卷完成后（卷总结）

## 总结类型

### 1. 小总结（每10章）

**触发条件**：章节号为10的倍数

**总结内容**：
- 剧情进展摘要
- 角色状态变化
- 伏笔状态更新
- 下一阶段预告

**输出文件**：`.novel-maker/summaries/summary-10chapters-XX.md`

**示例**：
```markdown
# 第1-10章小总结

## 剧情进展
- 第1-3章：主角林风出场，获得神秘老人赠剑
- 第4-6章：林风拜师学艺，初入江湖
- 第7-10章：首次实战，击败山贼，获得名声

## 角色状态
- 林风：初级修士 → 中级修士
- 苏雨：尚未出场
- 张天：林风师兄，尚未黑化

## 伏笔状态
- 已埋设：神秘老人身份、古剑封印、林风怪病
- 已回收：无
- 未回收：3个

## 下一阶段预告
- 第11-20章：林风进入学院，结识苏雨，张天开始黑化
```

### 2. 大总结（每50章）

**触发条件**：章节号为50的倍数

**总结内容**：
- 完整剧情回顾
- 角色成长轨迹
- 世界观展开情况
- 伏笔回收统计
- 读者反馈预测

**输出文件**：`.novel-maker/summaries/summary-50chapters-XX.md`

**示例**：
```markdown
# 第1-50章大总结

## 剧情回顾

### 第一幕：起始（1-20章）
- 林风出场，获得古剑
- 拜师学艺，初入江湖
- 结识苏雨，建立关系

### 第二幕：发展（21-40章）
- 进入学院，学习修炼
- 张天黑化，兄弟反目
- 发现古剑秘密

### 第三幕：高潮（41-50章）
- 进入王都，遭遇皇室
- 古剑封印觉醒
- 剑灵现身，揭示真相

## 角色成长

### 林风
- 等级：初级 → 高级
- 技能：基础剑法 → 御风术 + 剑气
- 武器：古剑·风吟（已解封）
- 关系：获得苏雨、剑灵等伙伴

### 苏雨
- 等级：初级 → 中级
- 技能：基础医术 → 高级医术
- 关系：与林风确立恋人关系

## 伏笔统计
- 总伏笔：12个
- 已回收：5个（42%）
- 未回收：7个（58%）

## 读者反馈预测
- 爽点：古剑觉醒、击败张天
- 虐点：兄弟反目、林风受伤
- 讨论点：神秘老人身份、皇室目的
```

### 3. 卷总结

**触发条件**：每卷完成后

**总结内容**：
- 本卷剧情回顾
- 角色成长总结
- 伏笔回收情况
- 下卷衔接建议

**输出文件**：`.novel-maker/summaries/summary-volume-XX.md`

## 实现逻辑

```python
def summary_trigger(project_dir: str, chapter_num: int):
    """触发阶段总结"""
    
    # 检查是否需要生成总结
    if chapter_num % 10 == 0:
        # 生成小总结
        generate_10_chapters_summary(project_dir, chapter_num)
    
    if chapter_num % 50 == 0:
        # 生成大总结
        generate_50_chapters_summary(project_dir, chapter_num)
    
    # 检查是否是卷末
    if is_volume_end(project_dir, chapter_num):
        # 生成卷总结
        generate_volume_summary(project_dir, chapter_num)
```

## 输出格式

```markdown
【阶段总结触发】

📊 已生成第1-10章小总结
   保存位置：.novel-maker/summaries/summary-10chapters-10.md

📊 已生成第1-50章大总结
   保存位置：.novel-maker/summaries/summary-50chapters-50.md

📊 已生成第一卷总结
   保存位置：.novel-maker/summaries/summary-volume-01.md

【总结概要】
- 剧情进展：完成第一幕和第二幕
- 角色成长：林风从初级升至高级
- 伏笔回收：5/12（42%）
- 下一阶段：进入第三幕高潮
```

## 配置选项

```json
{
  "summary-trigger": {
    "enabled": true,
    "priority": 4,
    "options": {
      "summary_10_interval": 10,
      "summary_50_interval": 50,
      "auto_detect_volume_end": true,
      "save_summary": true,
      "show_summary": true
    }
  }
}
```

## 注意事项

1. 总结会保存供后续章节参考
2. 总结内容会自动提取关键信息
3. 可以通过配置调整总结间隔
4. 卷总结需要手动触发或自动检测卷末
