# Hook 系统

## 概述

Hook 系统提供5个自动化钩子，在写作流程的关键节点自动执行预定义操作，提升写作效率。

## Hook 列表

| Hook | 触发时机 | 功能 |
|------|----------|------|
| [context-injection](context-injection.md) | 写作前 | 自动注入上下文（角色状态、世界观、前情摘要） |
| [intent-detection](intent-detection.md) | 用户输入时 | 检测用户意图，自动路由到对应功能 |
| [chapter-complete](chapter-complete.md) | 章节完成后 | 自动更新大纲、记忆文件、伏笔表 |
| [review-trigger](review-trigger.md) | 每章完成后 | 自动触发质量审查 |
| [summary-trigger](summary-trigger.md) | 每10章/50章后 | 自动生成阶段总结 |

## 工作原理

```
用户输入 → [intent-detection] → 识别意图 → 路由到对应功能
                                        ↓
写作前 → [context-injection] → 注入上下文 → 开始写作
                                        ↓
写作中 → AI 生成内容 → 用户确认
                                        ↓
章节完成 → [chapter-complete] → 更新大纲/记忆/伏笔
                                        ↓
           [review-trigger] → 质量审查 → 生成报告
                                        ↓
           [summary-trigger] → 检查是否需要总结 → 生成总结
```

## 使用方式

### 自动触发

Hook 会在对应时机自动触发，无需手动调用。

### 手动触发

```
/novel-maker hook context-injection  # 手动注入上下文
/novel-maker hook chapter-complete   # 手动触发章节完成流程
/novel-maker hook review-trigger     # 手动触发质量审查
/novel-maker hook summary-trigger    # 手动触发阶段总结
```

### 禁用 Hook

```
/novel-maker hook disable context-injection  # 禁用上下文注入
/novel-maker hook enable context-injection   # 启用上下文注入
/novel-maker hook status                     # 查看 Hook 状态
```

## 配置

Hook 配置文件位于 `.novel-maker/config.json`：

```json
{
  "hooks": {
    "context-injection": {
      "enabled": true,
      "priority": 1
    },
    "intent-detection": {
      "enabled": true,
      "priority": 0
    },
    "chapter-complete": {
      "enabled": true,
      "priority": 2
    },
    "review-trigger": {
      "enabled": true,
      "priority": 3
    },
    "summary-trigger": {
      "enabled": true,
      "priority": 4
    }
  }
}
```

## 执行顺序

Hook 按优先级顺序执行：

1. **intent-detection** (优先级 0) - 最先执行，识别用户意图
2. **context-injection** (优先级 1) - 写作前注入上下文
3. **chapter-complete** (优先级 2) - 章节完成后更新状态
4. **review-trigger** (优先级 3) - 触发质量审查
5. **summary-trigger** (优先级 4) - 检查是否需要总结

## 注意事项

1. Hook 执行不影响主流程，即使 Hook 失败也不会中断写作
2. Hook 结果会自动应用到项目中
3. 可以通过配置禁用不需要的 Hook
4. Hook 执行日志保存在 `.novel-maker/logs/hooks.log`
