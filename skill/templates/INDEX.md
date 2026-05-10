# 模板使用索引

## 核心模板 (日常使用)

| 模板 | 用途 | 使用时机 | 必填字段 |
|------|------|---------|---------|
| [constitution.md](constitution.md) | 创作宪法 | `/novel-weaver init` 时创建,持续更新 | 书名/题材/文风/核心原则 |
| [outline.md](outline.md) | 总大纲 | `/novel-weaver plan` 时生成 | 作品基因/角色/世界观/分卷 |
| [chapter.md](chapter.md) | 章节模板 | `/novel-weaver write` 时使用 | 大纲目标/本章核心/正文 |
| [character-profile.md](character-profile.md) | 角色档案 | 新角色出场时创建 | 姓名/性格/能力/关系/目标 |

## 规划模板 (阶段性使用)

| 模板 | 用途 | 使用时机 |
|------|------|---------|
| [volume-plan.md](volume-plan.md) | 卷计划 | `/novel-weaver plan 规划第X卷` 时 |
| [act-plan.md](act-plan.md) | 幕计划 | `/novel-weaver act` 时自动生成 |
| [scene-template.md](scene-template.md) | 场景规划 | 复杂场景写作前 |

## 总结模板 (定期使用)

| 模板 | 用途 | 使用时机 |
|------|------|---------|
| [summary-10chapters.md](summary-10chapters.md) | 10章小总结 | 每10章自动生成 |
| [summary-50chapters.md](summary-50chapters.md) | 50章大总结 | 每50章自动生成 |
| [summary-volume.md](summary-volume.md) | 卷总结 | 每卷结束时 |

## 辅助模板 (按需使用)

| 模板 | 用途 | 使用时机 |
|------|------|---------|
| [world-setting.md](world-setting.md) | 世界观设定 | 新设定时 |
| [power-system.md](power-system.md) | 力量体系 | 修炼/能力体系 |
| [hook-template.md](hook-template.md) | 伏笔管理 | 埋设/回收伏笔时 |
| [review-report.md](review-report.md) | 审查报告 | `/novel-weaver review` 时 |

## 使用建议

1. **日常写作**: 只需要 `chapter.md` + 更新 `constitution.md`
2. **规划阶段**: 使用 `outline.md` + `volume-plan.md` + `act-plan.md`
3. **定期总结**: 使用对应总结模板自动生成
