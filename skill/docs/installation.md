# 安装指南

> NovelWeaver 支持 18 款主流 AI 编程工具

## 一键安装（推荐）

```bash
cd /your/project
npx novel-weaver
```

脚本会自动检测你项目中使用的 IDE，将技能安装到正确位置。

### 指定 IDE

如果自动检测失败，可以显式指定：

```bash
npx novel-weaver --tool trae
```

### 支持的 IDE 列表

| IDE | 类型 | 安装路径 |
|-----|------|----------|
| Claude Code | CLI | `.claude/skills/novel-weaver/` |
| Copilot CLI | CLI | `.claude/skills/novel-weaver/` |
| Hermes Agent | CLI | `.hermes/skills/novel-weaver/` |
| Cursor | IDE | `.cursor/rules/novel-weaver/` |
| Windsurf | IDE | `.windsurf/skills/novel-weaver/` |
| Kiro | IDE | `.kiro/steering/` |
| Gemini CLI | CLI | `.gemini/skills/novel-weaver/` |
| Codex CLI | CLI | `.codex/skills/novel-weaver/` |
| Aider | CLI | `.aider/skills/novel-weaver/` |
| Trae | IDE | `.trae/skills/novel-weaver/` |
| VS Code (Copilot) | IDE 插件 | `.github/superpowers/` |
| DeerFlow | Agent 框架 | `skills/custom/novel-weaver/` |
| OpenCode | CLI | `.opencode/skills/novel-weaver/` |
| OpenClaw | CLI | `skills/novel-weaver/` |
| Qwen Code | IDE 插件 | `.qwen/skills/novel-weaver/` |
| Antigravity | CLI | `.agents/skills/novel-weaver/` |
| Claw Code | CLI (Rust) | `.claw/skills/novel-weaver/` |
| Qoder | IDE | `.qoder/skills/novel-weaver/` |

## 手动安装

如果 npx 不可用，可以手动复制：

```bash
# Trae
cp -r skill/* .trae/skills/novel-weaver/

# Claude Code
cp -r skill/* .claude/skills/novel-weaver/

# Cursor
cp -r skill/* .cursor/rules/novel-weaver/
```

## 卸载

```bash
npx novel-weaver --uninstall
```

## 安装验证

安装完成后，在 IDE 聊天框输入：

```
/novel-weaver help
```

如果返回帮助信息，说明安装成功。

## 常见问题

### Q: 安装后 AI 没识别到技能？

1. 确认路径正确
2. 确认 `SKILL.md` 存在于目录根
3. 重启 IDE 会话
4. 输入 `/novel-weaver help` 手动触发

### Q: 可以全局安装吗？

可以。全局路径一般为 `~/.<ide>/skills/novel-weaver/`，所有项目都能使用。
