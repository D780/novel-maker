# NovelWeaver - 全能网文写作助手

> 整合业界优秀网文写作工具理念，通过简洁指令+自然语言，帮你从零创作高质量长篇小说。
> **这是一个技能仓库**，兼容多种主流 AI IDE。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](skill/SKILL.md)

## 核心能力

- **6角色协作架构** - 协调者→规划师→写手→审计师→修订师→复盘师，流水线创作
- **智能创作引导** - 从书名、题材到角色设定，AI 引导你完成创作准备
- **22位作者文风库** - 覆盖搞笑、热血、文青、严谨等 7 大流派，支持智能推荐
- **幕系统** - 卷内剧情弧规划，6条分支走向（A主线/B危机/C支线/D缓冲/E回环/F颠覆）
- **33维度质量审计** - AI味检测、一致性检查、追读力分析全覆盖
- **去AI味技巧** - 表层（词汇/句式）+ 深层（对话区分度/情感行为化）双重处理
- **平台适配规则** - 番茄小说/起点中文网/晋江文学城，满足不同平台要求
- **RAG 记忆增强** - 三重记忆架构，8个真相文件，自动检索设定、追踪伏笔
- **创意约束系统** - 三轴混搭、反套路触发器、镜像对抗防重复
- **Token 优化** - Python 预处理脚本，AI 读 JSON 代替全文，节省 ~90% token

## 快速开始

### 安装方式

详细安装指南请查阅 [INSTALL.md](INSTALL.md)，这里列出常用方式：

#### 方式0：一键安装（推荐）

```bash
npx novel-weaver
```

自动检测 IDE 并安装，支持 18 款主流 AI 编程工具。

#### 方式1：Trae

```bash
cp -r skill/ .trae/skills/novel-weaver/
```

#### 方式2：Claude Code

```bash
cp -r skill/ .claude/skills/novel-weaver/
```

#### 方式3：Cline / Roo Code

```bash
cp -r skill/ .clinerules/novel-weaver/
```

#### 其他 IDE

| IDE | 路径 |
|-----|------|
| Cursor | `.cursor/rules/`（需转换为 .mdc 格式） |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Continue | `.continue/rules/` |
| OpenCode | `.opencode/skills/novel-weaver/` |
| Windsurf | `.windsurfrules` |

完整安装步骤、验证方法和常见问题见 [INSTALL.md](INSTALL.md)

### 使用

安装成功后，在 IDE 聊天框输入以下指令开始创作：

```
/novel-weaver init 开始写小说
```

AI 会引导你完成：
1. 情绪标签选择（打脸爽文/极致虐恋/爆笑反套路/悬疑惊悚/治愈甜宠/脑洞大开）
2. 题材选择
3. 一句话简介
4. 主角设定（姓名、核心反差点）
5. 核心冲突
6. 章节数与文风选择

## 指令速查

| 指令 | 说明 |
|------|------|
| `/novel-weaver init` | 开始写小说（6问引导） |
| `/novel-weaver write` | 写/续写章节 |
| `/novel-weaver review` | 审查质量 |
| `/novel-weaver memory` | 查看/管理设定 |
| `/novel-weaver plan` | 生成大纲 |
| `/novel-weaver act` | 下一幕剧情规划（6条分支） |
| `/novel-weaver style` | 切换文风 |
| `/novel-weaver help` | 帮助信息 |
| `/novel-weaver expand` | 扩写章节 |
| `/novel-weaver stats` | 字数统计 |
| `/novel-weaver inspire` | 灵感建议 |
| `/novel-weaver summary` | 阶段总结 |

完整指令体系（三级：7核心+5扩展+7高级子指令）详见 [SKILL.md](skill/SKILL.md)

## 6角色协作架构

NovelWeaver v2.0 采用 6角色协作架构，每个角色专注特定职责：

```
用户输入 → [协调者] 意图识别 → [规划师] 大纲/剧情卡片 → [写手] 章节草稿
         → [审计师] 审计报告 → [修订师] 修订稿 → [复盘师] 真相文件更新 → 输出
```

| 角色 | 职责 | 触发时机 |
|------|------|---------|
| **协调者** | 解析用户意图，调度角色 | 所有用户输入 |
| **规划师** | 大纲生成、幕规划、剧情推荐 | `/novel-weaver plan` `/novel-weaver act` |
| **写手** | 章节正文生成、文风应用 | `/novel-weaver write` |
| **审计师** | 33维度审计、编辑视角审查 | `/novel-weaver review` 每章自动 |
| **修订师** | 根据审计报告修复P0/P1问题 | `/novel-weaver review fix` |
| **复盘师** | 更新真相文件、生成总结 | 章节定稿后自动 |

> 角色定义详见 [agents/](skill/agents/) 目录

## 项目结构

```
.
├── skill/                  # 技能核心（安装到对应 IDE 的技能目录）
│   ├── SKILL.md            # 主技能文件
│   ├── README.md           # 技能使用说明
│   ├── agents/             # 角色定义（6个：协调者/规划师/写手/审计师/修订师/复盘师）
│   ├── references/         # 参考文档（24个，含去AI味技巧、平台适配规则、编辑视角、爽点追踪）
│   ├── styles/             # 文风库（22位作者，7大流派）
│   ├── templates/          # 模板文件（21个，含剧情卡片、角色语音卡、场景规划卡）
│   └── scripts/            # 脚本工具（14个文件，公共模块+13个脚本）
├── docs/                   # 项目文档
│   ├── CHANGELOG.md        # 版本历史
│   └── CONTRIBUTING.md     # 贡献指南
├── INSTALL.md              # 多 IDE 安装指南
├── LICENSE                 # MIT 许可证
└── README.md               # 项目说明
```

## 文风库

内置 22 位知名网文作者文风，按流派分类：

| 流派 | 代表作者 |
|------|---------|
| 搞笑幽默流 | 弈青峰、会说话的肘子、三天两觉、卖报小郎君 |
| 热血升级流 | 天蚕土豆、唐家三少、我吃西红柿、辰东、滚开 |
| 细腻文青流 | 猫腻、烽火戏诸侯、愤怒的香蕉、耳根 |
| 严谨设定流 | 爱潜水的乌贼、忘语、言归正传 |
| 特色领域流 | 蝴蝶蓝、天下霸唱、月关、萧鼎 |
| 多神话热血流 | 三九音域 |
| 悬疑推理流 | 杀虫队队员 |

详细文风库见 [skill/styles/author-styles.md](skill/styles/author-styles.md)

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| 1.0.0 | 2026-04 | 初始版本 |
| 1.1.0 | 2026-04 | RAG 检索增强 |
| 1.2.0 | 2026-04 | 指令精简 - 三级指令体系 |
| 1.3.0 | 2026-05 | 结构优化 - 消除重复、文风库分类 |
| 1.4.0 | 2026-05 | 实战增强 - 情绪标签系统、黄金开篇、情绪曲线、内容扩充技巧 |
| 1.5.0 | 2026-05 | 幕系统 + 脚本 - 6条分支走向、Python预处理脚本、多IDE兼容 |
| 2.0.0 | 2026-06 | 6角色协作架构 - 协调者/规划师/写手/审计师/修订师/复盘师，8个真相文件，去AI味技巧，平台适配规则 |

完整更新记录见 [CHANGELOG](docs/CHANGELOG.md)

## 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交变更 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

详细贡献指南请参阅 [CONTRIBUTING.md](docs/CONTRIBUTING.md)

## 许可证

本项目基于 [MIT License](LICENSE) 开源。

## Star History

如果你觉得这个项目有帮助，请给一个 Star！
