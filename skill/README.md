# NovelWeaver - 全能网文写作助手

> 技能详细说明请查阅 [SKILL.md](SKILL.md)

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](SKILL.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 快速开始

### 新用户？

1. [安装技能](../INSTALL.md)
2. [快速上手教程](QUICKSTART.md)
3. [完整文档](SKILL.md)

### 老用户？

- [快速参考卡](QUICK-REF.md)
- [使用指南](references/usage-guide.md)

### 快速体验

初始化

```
/novel-weaver init 开始写小说
```

生成大纲

```
/novel-weaver plan 帮我生成总大纲
```

开始写作

```
/novel-weaver write 写第一章
```

## 核心指令

| 指令 | 说明 |
|------|------|
| `/novel-weaver init` | 开始写小说(6问引导) |
| `/novel-weaver write` | 写/续写章节 |
| `/novel-weaver review` | 审查质量(一致性+AI味+节奏+约束) |
| `/novel-weaver memory` | 查看/管理设定 |
| `/novel-weaver plan` | 生成大纲/卷计划 |
| `/novel-weaver act` | 下一幕剧情规划(6条分支) |
| `/novel-weaver help` | 帮助信息 |

扩展指令: `/novel-weaver style`(文风) `/novel-weaver expand`(扩写) `/novel-weaver stats`(字数) `/novel-weaver inspire`(灵感) `/novel-weaver summary`(总结)

## 6角色协作架构

NovelWeaver v2.0 采用 6角色协作架构：

- **协调者** - 解析用户意图，调度角色
- **规划师** - 大纲生成、幕规划、剧情推荐
- **写手** - 章节正文生成、文风应用
- **审计师** - 33维度审计、编辑视角审查
- **修订师** - 根据审计报告修复问题
- **复盘师** - 更新真相文件、生成总结

> 角色定义详见 [agents/](agents/) 目录

## v2.0 新增功能

- **剧情卡片 6 要素**：方向类型、剧情预演、优点分析、参考小说、预计章节数、偏离影响评估
- **角色语音卡**：确保角色对话区分度
- **场景规划卡**：确保场景描写丰富度
- **爽点密度追踪**：10类爽点、S1-S5强度、平台适配
- **编辑视角审查**：开篇吸引力、节奏曲线、角色商业价值
- **读者反馈模拟**：模拟读者评论、评论区诱导设计
- **真相文件扩展**：新增 emotional-arcs.md、subplot-board.md、timeline.md

## 脚本工具

| 脚本 | 说明 |
|------|------|
| `analyze.py` | 三合一分析（single/style/batch） |
| `check_wordcount.py` | 字数检查 |
| `consistency_scan.py` | 一致性扫描 |
| `pacing_report.py` | 节奏报告 |
| `stats_report.py` | 项目统计 |

> 完整脚本说明详见 [scripts/README.md](scripts/README.md)

## 多 IDE 兼容

完整安装指南见仓库 [INSTALL.md](../INSTALL.md)

| IDE | 安装路径 |
|-----|----------|
| Trae | `.trae/skills/novel-weaver/` |
| Claude Code | `.claude/skills/novel-weaver/` |
| Cline / Roo Code | `.clinerules/novel-weaver/` |
| OpenCode | `.opencode/skills/novel-weaver/` |
| Cursor | `.cursor/rules/` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Continue | `.continue/rules/` |

---

*NovelWeaver v2.0.0 - 6角色协作架构，用说话的方式写小说*
