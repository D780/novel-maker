#!/usr/bin/env python3
"""NovelMaker 技能验证脚本

验证所有技能文件的完整性和正确性：
- Python 脚本语法检查
- 文件引用完整性检查
- 角色定义完整性检查
- 题材包完整性检查
- 弧线模板完整性检查
"""

import ast
import os
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent.parent
PROJECT_DIR = SKILL_DIR.parent


def check_python_syntax():
    """检查所有 Python 脚本的语法"""
    results = []
    scripts_dir = SKILL_DIR / "scripts"
    for py_file in sorted(scripts_dir.rglob("*.py")):
        try:
            with open(py_file, encoding="utf-8") as f:
                ast.parse(f.read())
            results.append(("PASS", py_file.name, "语法正确"))
        except SyntaxError as e:
            results.append(("FAIL", py_file.name, f"语法错误: {e.msg} 行{e.lineno}"))
    return results


def check_markdown_references():
    """检查 SKILL.md 和 QUICK-REF.md 中的文件引用"""
    results = []
    patterns = [
        (SKILL_DIR / "SKILL.md", r'\[.*?\]\(([^)]+)\)'),
        (SKILL_DIR / "QUICK-REF.md", r'`scripts/(\S+\.py)`'),
    ]

    for md_file, pattern in patterns:
        if not md_file.exists():
            results.append(("FAIL", md_file.name, "文件不存在"))
            continue

        with open(md_file, encoding="utf-8") as f:
            content = f.read()

        for match in re.finditer(pattern, content):
            ref = match.group(1)
            if ref.startswith(("http://", "https://", "#")):
                continue
            ref_path = md_file.parent / ref
            if not ref_path.exists():
                results.append(("WARN", md_file.name, f"断裂引用: {ref}"))
            else:
                results.append(("PASS", md_file.name, f"引用有效: {ref}"))
    return results


def check_agents():
    """检查角色定义完整性"""
    results = []
    agents_dir = SKILL_DIR / "agents"
    expected = ["coordinator.md", "planner.md", "writer.md",
                "auditor.md", "reviser.md", "reviewer.md"]

    for agent in expected:
        agent_path = agents_dir / agent
        if not agent_path.exists():
            results.append(("FAIL", f"agents/{agent}", "文件不存在"))
            continue
        with open(agent_path, encoding="utf-8") as f:
            content = f.read()
        required_sections = ["职责", "触发"]
        missing = [s for s in required_sections if s not in content]
        if missing:
            results.append(("WARN", f"agents/{agent}", f"缺少章节: {', '.join(missing)}"))
        else:
            results.append(("PASS", f"agents/{agent}", "定义完整"))
    return results


def check_genre_packs():
    """检查题材包完整性"""
    results = []
    packs_dir = SKILL_DIR / "genre-packs"
    required_files = ["rules.md", "templates.md", "arc-types.md"]

    for pack_dir in sorted(packs_dir.iterdir()):
        if not pack_dir.is_dir() or pack_dir.name.startswith("_"):
            continue
        for req_file in required_files:
            file_path = pack_dir / req_file
            if not file_path.exists():
                results.append(("FAIL", f"genre-packs/{pack_dir.name}/{req_file}", "文件不存在"))
            else:
                results.append(("PASS", f"genre-packs/{pack_dir.name}/{req_file}", "存在"))
    return results


def check_arc_templates():
    """检查弧线模板完整性"""
    results = []
    templates_dir = SKILL_DIR / "arc-templates"

    for genre_dir in sorted(templates_dir.iterdir()):
        if not genre_dir.is_dir():
            continue
        md_files = list(genre_dir.glob("*.md"))
        if not md_files:
            results.append(("WARN", f"arc-templates/{genre_dir.name}", "目录为空"))
        else:
            results.append(("PASS", f"arc-templates/{genre_dir.name}", f"{len(md_files)}个模板"))
    return results


def check_rules():
    """检查规则文件完整性"""
    results = []
    rules_dir = SKILL_DIR / "rules"
    expected = ["anti-ai-expressions.md", "character-voice.md", "consistency-check.md", "smart-query.md"]

    for rule in expected:
        rule_path = rules_dir / rule
        if not rule_path.exists():
            results.append(("FAIL", f"rules/{rule}", "文件不存在"))
        else:
            results.append(("PASS", f"rules/{rule}", "存在"))
    return results


def check_templates():
    """检查模板文件完整性"""
    results = []
    templates_dir = SKILL_DIR / "templates"
    required = ["constitution.md", "outline.md", "chapter.md", "character-profile.md"]

    for tpl in required:
        tpl_path = templates_dir / tpl
        if not tpl_path.exists():
            results.append(("FAIL", f"templates/{tpl}", "文件不存在"))
        else:
            results.append(("PASS", f"templates/{tpl}", "存在"))
    return results


def check_hooks():
    """检查 Hook 文件完整性"""
    results = []
    hooks_dir = SKILL_DIR / "hooks"
    expected = ["context-injection.md", "intent-detection.md", "chapter-complete.md",
                "review-trigger.md", "summary-trigger.md"]

    for hook in expected:
        hook_path = hooks_dir / hook
        if not hook_path.exists():
            results.append(("FAIL", f"hooks/{hook}", "文件不存在"))
        else:
            results.append(("PASS", f"hooks/{hook}", "存在"))
    return results


def run_all_checks():
    """运行所有检查"""
    checks = [
        ("Python 脚本语法", check_python_syntax),
        ("Markdown 文件引用", check_markdown_references),
        ("角色定义", check_agents),
        ("题材包", check_genre_packs),
        ("弧线模板", check_arc_templates),
        ("规则文件", check_rules),
        ("模板文件", check_templates),
        ("Hook 文件", check_hooks),
    ]

    total_pass = 0
    total_warn = 0
    total_fail = 0

    print("=" * 60)
    print("NovelMaker 技能验证报告")
    print("=" * 60)

    for check_name, check_func in checks:
        results = check_func()
        passes = [r for r in results if r[0] == "PASS"]
        warns = [r for r in results if r[0] == "WARN"]
        fails = [r for r in results if r[0] == "FAIL"]

        total_pass += len(passes)
        total_warn += len(warns)
        total_fail += len(fails)

        status = "✓" if not fails else "✗"
        print(f"\n{status} {check_name} ({len(passes)}通过 {len(warns)}警告 {len(fails)}失败)")

        for level, name, msg in fails:
            print(f"  ✗ {name}: {msg}")
        for level, name, msg in warns:
            print(f"  ⚠ {name}: {msg}")

    print("\n" + "=" * 60)
    print(f"总计: {total_pass}通过 {total_warn}警告 {total_fail}失败")
    print("=" * 60)

    return total_fail == 0


if __name__ == "__main__":
    success = run_all_checks()
    sys.exit(0 if success else 1)
