# NovelMaker - 全能网文写作助手

> **v2.0.0** - 6角色协作架构，用说话的方式写小说

## 快速开始

### 1. 安装技能

```bash
# 推荐：一键安装（自动检测 IDE）
npx novel-maker

# 或手动安装
cp -r skill/ .trae/skills/novel-maker/  # Trae
cp -r skill/ .claude/skills/novel-maker/  # Claude Code
```

> 详细安装指南见 [docs/installation.md](docs/installation.md)

### 2. 初始化项目

在 IDE 聊天框输入：

```
/novel-maker init 开始写一本修仙小说
```

AI 会引导你完成 6 问配置：情绪标签 → 题材 → 简介 → 主角 → 冲突 → 章节数

### 3. 开始写作

```
/novel-maker plan 帮我生成总大纲
/novel-maker write 写第一章
```

## 核心指令速查

| 指令 | 用途 |
|------|------|
| `/novel-maker init` | 初始化项目 |
| `/novel-maker write` | 写/续写章节 |
| `/novel-maker review` | 审查质量 |
| `/novel-maker plan` | 生成大纲 |
| `/novel-maker act` | 幕规划 |
| `/novel-maker memory` | 查看设定 |
| `/novel-maker help` | 帮助 |

## 详细文档

- [快速上手教程](docs/quickstart.md) - 5分钟从零到写出第一章
- [安装指南](docs/installation.md) - 多 IDE 安装方式
- [示例项目](docs/examples.md) - 完整示例参考
- [常见问题](docs/faq.md) - 问题排查
- [完整功能说明](SKILL.md) - AI 行为约束文档

## 6角色协作架构

```
用户输入 → [协调者] 意图识别 → [规划师] 大纲/剧情卡片 → [写手] 章节草稿
         → [审计师] 审计报告 → [修订师] 修订稿 → [复盘师] 真相文件更新 → 输出
```

| 角色 | 职责 |
|------|------|
| 协调者 | 解析用户意图，调度角色 |
| 规划师 | 大纲生成、幕规划、剧情推荐 |
| 写手 | 章节正文生成、文风应用 |
| 审计师 | 33维度审计、编辑视角审查 |
| 修订师 | 根据审计报告修复问题 |
| 复盘师 | 更新真相文件、生成总结 |

---

*NovelMaker v2.0.0 - 6角色协作架构，用说话的方式写小说*