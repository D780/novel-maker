# NovelWeaver 快速参考卡

## 核心指令 (7个)

| 指令 | 用途 | 示例 |
|------|------|------|
| `/novel-weaver init` | 初始化项目 | `/novel-weaver init 开始写修仙小说` |
| `/novel-weaver write` | 写/续写章节 | `/novel-weaver write 写第一章` |
| `/novel-weaver review` | 审查质量 | `/novel-weaver review` |
| `/novel-weaver memory` | 查看设定 | `/novel-weaver memory 主角等级` |
| `/novel-weaver plan` | 生成大纲 | `/novel-weaver plan 生成总大纲` |
| `/novel-weaver act` | 幕规划 | `/novel-weaver act 下一幕怎么走` |
| `/novel-weaver help` | 帮助 | `/novel-weaver help` |

## 扩展指令 (5个)

`/novel-weaver style` 文风 | `/novel-weaver expand` 扩写 | `/novel-weaver inspire` 灵感 | `/novel-weaver stats` 统计 | `/novel-weaver summary` 总结

## 日常写作循环

```
/novel-weaver write 继续写
  ↓ AI自动: 写作 → 审查 → 字数检查 → 更新大纲/记忆 → 进度提示
满意 → /novel-weaver write 继续
不满意 → /novel-weaver review fix 帮我改一下
字数不足 → /novel-weaver expand 扩充本章
写完当前幕 → /novel-weaver act 下一幕怎么走
```

## 脚本速查

| 场景 | 命令 | 用途 |
|------|------|------|
| 写前上下文 | `python scripts/chapter_info.py 前章.md --json` | 获取前章结构(~200 token) |
| 幕规划 | `python scripts/volume_batch.py 卷目录 --recent 5 --json` | 获取最近5章汇总 |
| 字数检查 | `python scripts/check_wordcount.py 本章.md` | 验证字数达标 |
| 一致性扫描 | `python scripts/consistency_scan.py 章节/ 真相/ --json` | 检测设定冲突 |
| AI味检测 | `python scripts/style_check.py 本章.md --json` | 检测套话密度 |
| 节奏报告 | `python scripts/pacing_report.py 章节/ --json` | S1-S5分布分析 |
| 项目统计 | `python scripts/stats_report.py novels/ --json` | 卷/章/字数统计 |

## 文风推荐

| 题材 | 推荐作者 |
|------|---------|
| 玄幻修仙 | 天蚕土豆、辰东 |
| 都市搞笑 | 弈青峰、会说话的肘子 |
| 仙侠探案 | 卖报小郎君 |
| 悬疑诡秘 | 爱潜水的乌贼 |
| 历史权谋 | 猫腻、愤怒的香蕉 |

## 节奏规则

- ❌ 不能连续3章S4/S5(疲劳)
- ❌ 不能连续3章S1/S2(弃读)
- ✅ 每5-8章必须有S4或S5
- ✅ 每3章必须有S3或更高
- 📊 情绪单元: 每3章"压-小扬-压-爆"

## 文件位置

```
创作元数据: .novel-weaver/ (宪法/真相文件/报告/总结)
小说正文:   novels/ (大纲+分卷章节)
技能目录:   skill/ (references/templates/styles/scripts)
```
