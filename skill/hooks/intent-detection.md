# Intent Detection Hook

## 概述

在用户输入时自动检测意图，将自然语言请求路由到对应的功能模块，提供更智能的交互体验。

## 触发时机

- 用户输入任何文本时
- 在其他 Hook 执行前

## 意图类型

### 1. 写作意图

**关键词**：写、创作、续写、继续、下一章、开始写

**路由目标**：`/novel-maker write`

**示例**：
```
用户：帮我写第一章
→ 识别为写作意图
→ 执行 /novel-maker write 写第一章

用户：继续写，主角遇到了敌人
→ 识别为写作意图
→ 执行 /novel-maker write 继续写，主角遇到了敌人
```

### 2. 查询意图

**关键词**：什么、谁、哪里、怎么、为什么、查询、查看

**路由目标**：`/novel-maker query`

**示例**：
```
用户：林风是什么等级？
→ 识别为查询意图（角色查询）
→ 执行 /novel-maker query 林风是什么等级？

用户：第三章发生了什么？
→ 识别为查询意图（剧情查询）
→ 执行 /novel-maker query 第三章发生了什么？
```

### 3. 审查意图

**关键词**：检查、审查、看看、有没有问题、质量、矛盾

**路由目标**：`/novel-maker review`

**示例**：
```
用户：帮我看看这一章
→ 识别为审查意图
→ 执行 /novel-maker review

用户：检查有没有矛盾
→ 识别为审查意图
→ 执行 /novel-maker review consistency
```

### 4. 规划意图

**关键词**：大纲、规划、计划、下一幕、走向、剧情

**路由目标**：`/novel-maker plan` 或 `/novel-maker act`

**示例**：
```
用户：帮我生成总大纲
→ 识别为规划意图
→ 执行 /novel-maker plan 帮我生成总大纲

用户：下一幕怎么走
→ 识别为规划意图
→ 执行 /novel-maker act 下一幕怎么走
```

### 5. 设置意图

**关键词**：文风、风格、切换、设置、配置

**路由目标**：`/novel-maker style`

**示例**：
```
用户：换个文风
→ 识别为设置意图
→ 执行 /novel-maker style

用户：用辰东的风格
→ 识别为设置意图
→ 执行 /novel-maker style 用辰东的风格
```

## 实现逻辑

```python
def detect_intent(user_input: str) -> dict:
    """检测用户意图"""
    intent_keywords = {
        "write": ["写", "创作", "续写", "继续", "下一章", "开始写"],
        "query": ["什么", "谁", "哪里", "怎么", "为什么", "查询", "查看"],
        "review": ["检查", "审查", "看看", "有没有问题", "质量", "矛盾"],
        "plan": ["大纲", "规划", "计划", "下一幕", "走向", "剧情"],
        "style": ["文风", "风格", "切换", "设置", "配置"]
    }
    
    # 统计每个意图的关键词匹配数
    intent_scores = {}
    for intent, keywords in intent_keywords.items():
        score = sum(1 for keyword in keywords if keyword in user_input)
        intent_scores[intent] = score
    
    # 返回得分最高的意图
    if max(intent_scores.values()) > 0:
        primary_intent = max(intent_scores, key=intent_scores.get)
        return {
            "intent": primary_intent,
            "confidence": intent_scores[primary_intent],
            "input": user_input
        }
    
    # 默认为写作意图
    return {
        "intent": "write",
        "confidence": 0,
        "input": user_input
    }
```

## 路由逻辑

```python
def route_to_function(intent: str, user_input: str) -> str:
    """根据意图路由到对应功能"""
    routes = {
        "write": "/novel-maker write",
        "query": "/novel-maker query",
        "review": "/novel-maker review",
        "plan": "/novel-maker plan",
        "style": "/novel-maker style"
    }
    
    command = routes.get(intent, "/novel-maker write")
    return f"{command} {user_input}"
```

## 输出格式

```markdown
【意图检测】
- 输入：帮我写第一章
- 检测意图：write（写作意图）
- 置信度：3
- 路由命令：/novel-maker write 帮我写第一章
```

## 配置选项

```json
{
  "intent-detection": {
    "enabled": true,
    "priority": 0,
    "options": {
      "default_intent": "write",
      "confidence_threshold": 1,
      "show_detection_result": false
    }
  }
}
```

## 注意事项

1. 意图检测是第一优先级的 Hook，最先执行
2. 如果置信度低于阈值，使用默认意图
3. 可以通过配置显示检测结果，方便调试
4. 意图检测结果会影响后续 Hook 的执行
