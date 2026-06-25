# 安装指南

> NovelMaker 支持 18 款主流 AI 编程工具

## 一键安装（推荐）

```bash
cd /your/project
npx novel-maker
```

脚本会自动检测你项目中使用的 IDE，将技能安装到正确位置。

### 指定 IDE

如果自动检测失败，可以显式指定：

```bash
npx novel-maker --tool trae
```

### 支持的 IDE 列表

| IDE | 类型 | 安装路径 |
|-----|------|----------|
| Claude Code | CLI | `.claude/skills/novel-maker/` |
| Copilot CLI | CLI | `.claude/skills/novel-maker/` |
| Hermes Agent | CLI | `.hermes/skills/novel-maker/` |
| Cursor | IDE | `.cursor/rules/novel-maker/` |
| Windsurf | IDE | `.windsurf/skills/novel-maker/` |
| Kiro | IDE | `.kiro/steering/` |
| Gemini CLI | CLI | `.gemini/skills/novel-maker/` |
| Codex CLI | CLI | `.codex/skills/novel-maker/` |
| Aider | CLI | `.aider/skills/novel-maker/` |
| Trae | IDE | `.trae/skills/novel-maker/` |
| VS Code (Copilot) | IDE 插件 | `.github/superpowers/` |
| DeerFlow | Agent 框架 | `skills/custom/novel-maker/` |
| OpenCode | CLI | `.opencode/skills/novel-maker/` |
| OpenClaw | CLI | `skills/novel-maker/` |
| Qwen Code | IDE 插件 | `.qwen/skills/novel-maker/` |
| Antigravity | CLI | `.agents/skills/novel-maker/` |
| Claw Code | CLI (Rust) | `.claw/skills/novel-maker/` |
| Qoder | IDE | `.qoder/skills/novel-maker/` |

## 手动安装

如果 npx 不可用，可以手动复制：

```bash
# Trae
cp -r skill/* .trae/skills/novel-maker/

# Claude Code
cp -r skill/* .claude/skills/novel-maker/

# Cursor
cp -r skill/* .cursor/rules/novel-maker/
```

## 卸载

```bash
npx novel-maker --uninstall
```

## 安装验证

安装完成后，在 IDE 聊天框输入：

```
/novel-maker help
```

如果返回帮助信息，说明安装成功。

## 常见问题

### Q: 安装后 AI 没识别到技能？

1. 确认路径正确
2. 确认 `SKILL.md` 存在于目录根
3. 重启 IDE 会话
4. 输入 `/novel-maker help` 手动触发

### Q: 可以全局安装吗？

可以。全局路径一般为 `~/.<ide>/skills/novel-maker/`，所有项目都能使用。
