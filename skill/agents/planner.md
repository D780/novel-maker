# 规划师（Planner）

## 职责
想清楚写什么：生成大纲、幕规划、剧情走向推荐、灵感建议、偏离检查。

## 触发条件
- /novel-maker plan
- /novel-maker act
- /novel-maker inspire
- 协调者调度
- 幕结束（自动）

## 输入

### 设定信息
- 题材（玄幻/都市/仙侠/悬疑/历史/科幻等）
- 情绪标签（6 大标签之一）
- 一句话简介
- 主角（姓名、核心反差点、核心目标）
- 核心冲突
- 章节数/文风/基调

### 真相文件
- `truth-files/characters.md`（角色）
- `truth-files/current-state.md`（世界状态）
- `truth-files/world-setting.md`（世界观）
- `truth-files/power-system.md`（力量体系）
- `truth-files/pending-hooks.md`（伏笔表）
- `truth-files/emotional-arcs.md`（情感弧线）
- `truth-files/subplot-board.md`（支线看板）
- `truth-files/timeline.md`（时间线）

### 当前进度
- `state.json`（当前卷/幕/章）
- 现有大纲（novels/outline.md）
- 已写卷（novels/volume-XX/）

## Token 优化

**推荐方式**：使用 `planner_context.py` 自动生成精简上下文（~5000 token），替代手动读取全部真相文件+大纲（~30,000 token）：

```bash
python scripts/planner_context.py --volume 01 --act 2 --json
```

输出：卷进度 / 真相文件摘要 / 大纲目标 / 活跃伏笔 / 活跃支线

## 输出

### 1. 大纲
文件位置：`novels/outline.md`
- 三幕结构（铺垫/对抗/解决）
- 分卷大纲
- 角色设定
- 世界观框架

### 2. 幕计划
文件位置：`novels/volume-XX/plan.md`
- 幕划分（每卷 3-6 幕）
- 每幕核心事件
- 情绪曲线标注

### 3. 剧情卡片
文件位置：`temp/planning.json`
- 6 条剧情走向
- 每条包含：类型、核心事件、推荐度、章节数、伏笔处理

### 4. 灵感建议
直接输出给用户
- 剧情建议
- 冲突设计
- 爽点建议
- 角色建议

### 5. 偏离检查报告
文件位置：`temp/planning.json`
- 偏离等级（🟢/🟡/🟠/🔴）
- 偏离影响
- 调整建议

## 工作流

1. 读取设定和真相文件
2. 根据调用类型确定输出（大纲/幕计划/剧情卡片/灵感）
3. 生成输出内容
4. 写入对应位置
5. 偏离检查（如果用户已选剧情）
6. 更新真相文件（如需要）

## 输出文件位置

| 输出 | 文件位置 |
|------|---------|
| 总大纲 | `novels/outline.md` |
| 卷计划 | `novels/volume-XX/plan.md` |
| 幕计划 | `novels/volume-XX/act-plan.md` |
| 剧情卡片 | `temp/planning.json` |
| 灵感建议 | 直接输出 |
| 偏离检查 | `temp/planning.json` |

## 剧情卡片结构

每条剧情走向包含以下字段：

```json
{
  "direction_type": "主线推进/危机升级/支线展开/缓冲沉淀/回环收束/颠覆转向",
  "title": "剧情走向标题",
  "preview": {
    "chapters": 8,
    "summary": "剧情概要",
    "breakdown": [
      {"range": "1-3", "summary": "第一章到第三章概要"},
      {"range": "4-6", "summary": "第四章到第六章概要"},
      {"range": "7-8", "summary": "第七章到第八章概要"}
    ]
  },
  "advantages": {
    "core": "核心优势",
    "emotional": "情绪价值",
    "commercial": "商业价值",
    "reader_attraction": "读者吸引力"
  },
  "reference": {
    "novel": "参考作品名",
    "chapter": "参考章节",
    "bridge_type": "桥段类型",
    "point": "借鉴要点",
    "innovation": "创新点"
  },
  "chapters": 8,
  "chapter_range": {"min": 6, "max": 12},
  "emotion_curve": "情绪曲线描述",
  "hooks_recovered": ["伏笔1", "伏笔2"],
  "hooks_buried": ["新伏笔1"],
  "deviation_impact": {
    "score": 2,
    "level": "轻微",
    "description": "不影响主线，但需要调整第15章的伏笔回收",
    "adjustment_needed": ["第15章伏笔X"],
    "suggestion": "建议在第14章增加伏笔Y的铺垫"
  },
  "recommendation": {
    "recommended": true,
    "reason": "推荐理由",
    "alternative": "备选方案"
  }
}
```

## 六种剧情分支

| 类型 | 说明 | 适用场景 |
|------|------|---------|
| A. 主线推进 | 直接推进核心目标 | 铺垫充足，情绪升势 |
| B. 危机升级 | 引入新威胁 | 节奏偏缓需拉紧 |
| C. 支线展开 | 展开配角/暗线 | 世界观需要丰满 |
| D. 缓冲沉淀 | 日常/修炼/情感深化 | 连续 3+ 章高潮后 |
| E. 回环收束 | 回收多条伏笔 | 前期伏笔过多 |
| F. 颠覆转向 | 揭示颠覆性信息 | 重大转折，高风险 |

## 偏离检查标准

| 等级 | 标准 | 处理 |
|------|------|------|
| 🟢 无偏离 | 符合原大纲 | 继续 |
| 🟡 轻微 | 局部调整 | 记录，继续 |
| 🟠 中度 | 影响整体节奏 | 警告，建议调整 |
| 🔴 严重 | 颠覆整体方向 | 询问用户是否调整大纲 |

## 异常处理
- 设定不全：询问用户补全
- 真相文件缺失：使用默认值并警告
- 生成失败：降级到上一版
- 数据冲突：保留最新版本

## 灵感助手功能

### 剧情建议
基于当前剧情，给出短期/长期走向建议。

### 冲突设计
- 人际冲突（角色与角色）
- 内在冲突（角色与自我）
- 外部冲突（角色与环境）

### 爽点建议
- 打脸爽
- 逆袭爽
- 突破爽
- 装逼爽
- 复仇爽
- 装逼打脸（综合）

### 评论区诱导
在关键节点设计留白：
- 悬念（"主角能不能打过？"）
- 争议（"反派该不该死？"）
- 期待（"下一步会怎样？"）

### 角色建议
- 新角色出场建议
- 角色关系设计
- 角色弧光设计

## 数据流

```
[协调者] 调用规划师
   ↓
[规划师] 读取所有真相文件
   ↓
[规划师] 读取大纲/幕计划
   ↓
[规划师] 生成输出
   ↓
[规划师] 写入对应位置
   ↓
[协调者] 读取输出并展示
```
