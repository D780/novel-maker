# 智能查询规则

## 核心原则

智能查询系统提供4种意图的快速查询，帮助用户快速获取小说相关信息，无需手动翻阅文档。

---

## 查询类型

### 1. 角色查询

**查询内容**：
- 角色设定（姓名、身份、背景）
- 角色状态（等级、位置、情绪）
- 角色关系（血缘、师徒、敌对、恋人）
- 角色技能（能力、功法、武器）

**示例查询**：
```
用户：林风是什么等级？
AI：林风当前等级为高级修士，擅长剑法，拥有"御风术"技能。

用户：苏雨和林风什么关系？
AI：苏雨和林风是恋人关系，第3章相遇，第20章表白。

用户：列出所有反派角色
AI：当前主要反派角色：
1. 张天（林风的师兄，黑化叛变）
2. 魔尊（终极BOSS，幕后黑手）
```

**查询来源**：
- `truth-files/characters.md` - 角色档案
- `truth-files/current-state.md` - 世界状态
- `novels/volume-XX/chapters/` - 章节内容

### 2. 设定查询

**查询内容**：
- 世界观设定（地理、历史、文化）
- 力量体系（等级、修炼、技能）
- 社会制度（等级、法律、习俗）
- 特殊设定（魔法、科技、规则）

**示例查询**：
```
用户：这个世界有几种修炼体系？
AI：本世界有3种修炼体系：
1. 剑修体系（初级→中级→高级→大师→宗师）
2. 法修体系（初级→中级→高级→大师→宗师）
3. 体修体系（初级→中级→高级→大师→宗师）

用户：王都在哪里？
AI：王都位于大陆中央，是政治、经济、文化中心。从北境骑马需要7天，从东海坐船需要3天。
```

**查询来源**：
- `truth-files/world-setting.md` - 世界观设定
- `truth-files/power-system.md` - 力量体系
- `skill/genre-packs/` - 题材包设定

### 3. 剧情查询

**查询内容**：
- 章节摘要（某章发生了什么）
- 事件追踪（某事件的详细过程）
- 角色经历（某角色遇到过什么）
- 剧情进展（当前剧情到哪里）

**示例查询**：
```
用户：第三章发生了什么？
AI：第三章主要内容：
- 林风在山林中遇到神秘老人
- 老人赠予林风一把古剑
- 林风发现古剑有封印
- 章末伏笔：老人身份成谜

用户：主角遇到过哪些敌人？
AI：林风遇到的主要敌人：
1. 第5章：山贼（被林风击败）
2. 第15章：张天（师兄，黑化后成为敌人）
3. 第30章：魔尊手下（试探性攻击）
```

**查询来源**：
- `novels/volume-XX/chapters/` - 章节内容
- `.novel-maker/summaries/` - 阶段总结
- `novels/outline.md` - 总大纲

### 4. 伏笔查询

**查询内容**：
- 伏笔状态（已埋设/已回收/未回收）
- 伏笔详情（埋设章节、内容、预期回收）
- 伏笔关联（与其他伏笔的关系）
- 回收建议（如何回收某个伏笔）

**示例查询**：
```
用户：有哪些未回收的伏笔？
AI：当前未回收的伏笔：
1. 第3章：神秘老人赠剑（预期第50章回收）
2. 第10章：古籍预言（预期第80章回收）
3. 第15章：林风的怪病（未设定回收点）

用户：神秘老人的剑后来怎样了？
AI：神秘老人的剑（古剑·风吟）：
- 第3章埋设：老人赠剑，剑有封印
- 第20章进展：林风尝试解封，失败
- 第50章回收：剑中封印觉醒，释放剑灵
- 当前状态：已回收
```

**查询来源**：
- `truth-files/pending-hooks.md` - 伏笔表
- `novels/volume-XX/chapters/` - 章节内容

---

## 查询引擎实现

### 查询意图识别

```python
def detect_query_intent(query: str) -> str:
    """识别查询意图"""
    # 角色相关关键词
    character_keywords = ["角色", "人物", "主角", "反派", "等级", "技能", "关系", "谁", "名字"]
    
    # 设定相关关键词
    setting_keywords = ["世界", "设定", "体系", "规则", "地理", "历史", "制度", "魔法", "修炼"]
    
    # 剧情相关关键词
    plot_keywords = ["剧情", "章节", "发生", "事件", "遇到", "经历", "进展", "故事"]
    
    # 伏笔相关关键词
    hook_keywords = ["伏笔", "埋设", "回收", "悬念", "谜团", "暗示", "铺垫"]
    
    # 关键词匹配
    for keyword in character_keywords:
        if keyword in query:
            return "character"
    
    for keyword in setting_keywords:
        if keyword in query:
            return "setting"
    
    for keyword in plot_keywords:
        if keyword in query:
            return "plot"
    
    for keyword in hook_keywords:
        if keyword in query:
            return "hook"
    
    # 默认为剧情查询
    return "plot"
```

### 查询路由

```python
def route_query(intent: str, query: str) -> str:
    """根据意图路由查询"""
    if intent == "character":
        return query_character(query)
    elif intent == "setting":
        return query_setting(query)
    elif intent == "plot":
        return query_plot(query)
    elif intent == "hook":
        return query_hook(query)
    else:
        return "抱歉，我无法理解您的查询。请尝试更具体的描述。"
```

### 查询结果格式化

```python
def format_query_result(intent: str, result: dict) -> str:
    """格式化查询结果"""
    if intent == "character":
        return format_character_result(result)
    elif intent == "setting":
        return format_setting_result(result)
    elif intent == "plot":
        return format_plot_result(result)
    elif intent == "hook":
        return format_hook_result(result)
    else:
        return str(result)
```

---

## 使用方式

### 指令触发

```
/novel-maker query 林风是什么等级？
/novel-maker query 有哪些未回收的伏笔？
/novel-maker query 第三章发生了什么？
```

### 自然语言触发

```
用户：主角现在什么境界？
AI：[自动识别为角色查询] 林风当前等级为高级修士...

用户：这个世界有几种修炼体系？
AI：[自动识别为设定查询] 本世界有3种修炼体系...
```

### 查询结果展示

```markdown
## 查询结果

**查询**：林风是什么等级？

**结果**：
- **当前等级**：高级修士
- **擅长技能**：剑法、御风术
- **武器**：古剑·风吟（已解封）
- **状态**：健康，正在前往王都

**来源**：
- 角色档案：truth-files/characters.md
- 世界状态：truth-files/current-state.md
- 最新章节：第50章
```

---

## 查询优化

### 1. 缓存机制

- 缓存常用查询结果
- 缓存失效策略：章节更新后自动失效

### 2. 模糊匹配

- 支持角色别名（如"主角"→"林风"）
- 支持同义词（如"等级"→"境界"）

### 3. 上下文关联

- 记忆用户之前的查询
- 支持追问（如"他有什么技能？"）

---

## 参考资源

- 角色档案：`truth-files/characters.md`
- 世界状态：`truth-files/current-state.md`
- 伏笔表：`truth-files/pending-hooks.md`
- 章节内容：`novels/volume-XX/chapters/`
