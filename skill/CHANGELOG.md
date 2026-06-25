# 变更日志

## v2.0.0 (2026-06-25)

### 新增功能

- **剧情卡片 6 要素**：方向类型、剧情预演、优点分析、参考小说、预计章节数、偏离影响评估
- **角色语音卡**：确保角色对话区分度
- **场景规划卡**：确保场景描写丰富度
- **爽点密度追踪**：10类爽点、S1-S5强度、平台适配
- **编辑视角审查**：开篇吸引力、节奏曲线、角色商业价值
- **读者反馈模拟**：模拟读者评论、评论区诱导设计
- **真相文件扩展**：新增 emotional-arcs.md、subplot-board.md、timeline.md

### 改进

- **analyze.py 三合一脚本**：整合 chapter_info.py + style_check.py + hook_report.py
- **剧情卡片模板**：6 个走向全部展开完整结构
- **规划师 JSON 结构**：补充 preview、advantages、reference、deviation_impact 字段
- **复盘师总结频率**：统一为每章后/每5章后/每10章后/每50章后/每卷末
- **字数要求说明**：新增平台适配（番茄/起点/晋江）

### 文档整理

- **删除过时文件**：OPTIMIZATION-LOG.md（v1.6.0）
- **合并重复文档**：anti-ai-patterns.md + anti-ai-techniques.md → anti-ai-techniques.md
- **删除冗余文件**：pacing-analysis.md、emotion-curve.md（已整合到 rhythm-system.md）
- **更新参考文档表**：从 22 个精简为 19 个
- **创建模板索引**：templates/INDEX.md

### 脚本更新

- **analyze.py**：实现三合一功能（single/style/batch 模式）
- **hook_report.py**：修复变量名拼写 bug

---

## v1.6.0 (2026-05)

### 优化内容

- 文档精简整合
- 脚本功能增强
- 模板优化
- 工作流优化

---

*完整变更历史请查看 Git 提交记录*
