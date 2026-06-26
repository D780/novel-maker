#!/usr/bin/env python3
"""
NovelMaker 安装脚本（Python 版）

当 npx 不可用时的备选安装方案。

使用方式：
    python scripts/common/install.py [--ide trae|claude|cursor|...] [--uninstall]
"""

import sys
import argparse
from pathlib import Path


# 支持的 IDE 列表
TARGETS = [
    {"name": "Claude Code",   "dir": ".claude/skills/novel-maker",  "detect": [".claude"]},
    {"name": "Cursor",        "dir": ".cursor/rules/novel-maker",   "detect": [".cursor", ".cursorrules"]},
    {"name": "Trae",          "dir": ".trae/skills/novel-maker",    "detect": [".trae"]},
    {"name": "Windsurf",      "dir": ".windsurf/skills/novel-maker", "detect": [".windsurf"]},
    {"name": "Gemini CLI",    "dir": ".gemini/skills/novel-maker",  "detect": ["GEMINI.md"]},
    {"name": "Codex CLI",     "dir": ".codex/skills/novel-maker",   "detect": [".codex"]},
    {"name": "OpenCode",      "dir": ".opencode/skills/novel-maker", "detect": [".opencode"]},
    {"name": "Aider",         "dir": ".aider/skills/novel-maker",   "detect": [".aider"]},
    {"name": "Hermes Agent",  "dir": ".hermes/skills/novel-maker",  "detect": [".hermes", "HERMES.md"]},
    {"name": "Qwen Code",     "dir": ".qwen/skills/novel-maker",    "detect": [".qwen"]},
    {"name": "Claw Code",     "dir": ".claw/skills/novel-maker",    "detect": [".claw", "CLAW.md"]},
    {"name": "Qoder",         "dir": ".qoder/skills/novel-maker",   "detect": [".qoder"]},
    {"name": "Antigravity",   "dir": ".agents/skills/novel-maker",  "detect": [".agents"]},
    {"name": "OpenClaw",      "dir": "skills/novel-maker",          "detect": [".openclaw"]},
    {"name": "Kiro",          "dir": ".kiro/steering/novel-maker",  "detect": [".kiro"]},
    {"name": "VS Code",       "dir": ".github/superpowers/novel-maker", "detect": [".github/copilot-instructions.md"]},
    {"name": "DeerFlow",      "dir": "skills/custom/novel-maker",   "detect": ["deer_flow"]},
    {"name": "Copilot CLI",   "dir": ".claude/skills/novel-maker",  "detect": [".claude"]},
]

# 工具别名
TOOL_ALIASES = {
    "claude": "Claude Code",
    "cursor": "Cursor",
    "trae": "Trae",
    "windsurf": "Windsurf",
    "gemini": "Gemini CLI",
    "codex": "Codex CLI",
    "opencode": "OpenCode",
    "aider": "Aider",
    "hermes": "Hermes Agent",
    "qwen": "Qwen Code",
    "claw": "Claw Code",
    "qoder": "Qoder",
    "antigravity": "Antigravity",
    "openclaw": "OpenClaw",
    "kiro": "Kiro",
}


def detect_ides():
    """检测当前项目中的 IDE"""
    detected = []
    cwd = Path.cwd()
    
    for target in TARGETS:
        for detect in target["detect"]:
            if (cwd / detect).exists():
                detected.append(target)
                break
    
    return detected


def copy_dir(src, dest):
    """递归复制目录"""
    import shutil
    src = Path(src)
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    
    for item in src.iterdir():
        if item.name == '.DS_Store':
            continue
        dest_item = dest / item.name
        if item.is_dir():
            copy_dir(item, dest_item)
        else:
            shutil.copy2(item, dest_item)


def install_skill(target):
    """安装技能到指定 IDE"""
    cwd = Path.cwd()
    skill_dir = cwd / "skill"
    
    if not skill_dir.exists():
        print(f"❌ 错误：未找到 skill/ 目录")
        return False
    
    dest_dir = cwd / target["dir"]
    print(f"  安装到 {target['name']}: {target['dir']}")
    
    try:
        copy_dir(skill_dir, dest_dir)
        print(f"  ✅ {target['name']} 安装成功")
        return True
    except Exception as e:
        print(f"  ❌ {target['name']} 安装失败: {e}")
        return False


def uninstall_skill():
    """卸载技能"""
    import shutil
    cwd = Path.cwd()
    
    print("🗑️  卸载 NovelMaker...\n")
    
    for target in TARGETS:
        dest_dir = cwd / target["dir"]
        if dest_dir.exists():
            shutil.rmtree(dest_dir)
            print(f"  ✅ {target['name']} 已卸载")
    
    print("\n✅ 卸载完成")


def main():
    parser = argparse.ArgumentParser(description="NovelMaker 安装脚本")
    parser.add_argument("--ide", help="指定 IDE 的类型")
    parser.add_argument("--uninstall", action="store_true", help="卸载技能")
    args = parser.parse_args()
    
    print("\n  NovelMaker v2.0.0 - 全能网文写作助手")
    print("  6角色协作架构，用说话的方式写小说\n")
    
    if args.uninstall:
        uninstall_skill()
        return
    
    if args.ide:
        tool_name = TOOL_ALIASES.get(args.ide.lower())
        if not tool_name:
            print(f"❌ 未知的工具: {args.ide}")
            print(f"支持的: {', '.join(TOOL_ALIASES.keys())}")
            sys.exit(1)
        targets = [t for t in TARGETS if t["name"] == tool_name]
    else:
        targets = detect_ides()
    
    if not targets:
        print("❌ 未检测到 IDE，请使用 --ide 参数指定")
        print(f"支持的: {', '.join(TOOL_ALIASES.keys())}")
        sys.exit(1)
    
    print(f"检测到 {len(targets)} 个 IDE:\n")
    for t in targets:
        print(f"  - {t['name']}")
    print()
    
    for target in targets:
        install_skill(target)
    
    print("\n✅ 安装完成！")
    print("\n在 IDE 聊天框输入以下指令开始创作：")
    print("  /novel-maker init 开始写小说")
    print("  /novel-maker help 查看帮助\n")


if __name__ == "__main__":
    main()
