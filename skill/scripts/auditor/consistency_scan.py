#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一致性扫描
提取章节中的角色、等级、地点，与真相文件比对，输出冲突报告。
"""

import os
import sys
import json
import re
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'common'))
from nm_utils import (
    list_chapters, read_chapter, extract_characters, extract_locations
)


def read_truth_file(filepath):
    """Read a truth file and return its content."""
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return None


def extract_characters_from_truth(text):
    """Extract character names from truth files."""
    if not text:
        return set()
    names = set()
    for m in re.finditer(r'[#|*\-]*\s*([\u4e00-\u9fff]{2,4})(?:[：:]\s*[^\n]*|的角色)', text):
        name = m.group(1)
        if not name.startswith(('#', '!', ' ', '-', '|', '*')):
            names.add(name)
    return names


def extract_power_levels(text):
    """Extract power level mentions from text."""
    levels = {}
    for m in re.finditer(r'([\u4e00-\u9fff]{2,4})[：:]?\s*([\u4e00-\u9fff]+(?:[初期|中期|后期|巅峰|大圆满]*))', text):
        name, level = m.group(1), m.group(2)
        if len(name) >= 2 and len(name) <= 4:
            levels[name] = level
    return levels


def extract_power_mentions(text):
    """Extract power level mentions from chapter."""
    mentions = {}
    for m in re.finditer(r'([\u4e00-\u9fff]{2,4})(?:已是|达到|突破到|升至|晋升为|修为|境界)\s*([\u4e00-\u9fff]{2,10})', text):
        mentions[m.group(1)] = m.group(2)
    return mentions


def scan_volume(chapters_dir, truth_dir, recent_n=None):
    """Scan all chapters and compare with truth files."""
    chapter_files = list_chapters(chapters_dir, recent_n)
    if not chapter_files:
        return {'error': f'No chapters found in {chapters_dir}'}

    characters_md = read_truth_file(os.path.join(truth_dir, 'characters.md'))
    current_state = read_truth_file(os.path.join(truth_dir, 'current-state.md'))

    truth_text = ""
    if characters_md:
        truth_text += characters_md
    if current_state:
        truth_text += "\n" + current_state

    truth_chars = extract_characters_from_truth(truth_text)
    truth_levels = extract_power_levels(truth_text)

    results = []
    total_issues = []
    new_chars_all = set()
    level_conflicts_all = []

    for idx, filepath in enumerate(chapter_files):
        raw, title, clean, wc = read_chapter(filepath)
        chapter_chars = extract_characters(clean)
        power_mentions = extract_power_mentions(raw)

        issues = []
        new_chars = [c for c in chapter_chars if c not in truth_chars]
        level_conflicts = []
        for char, level in power_mentions.items():
            if char in truth_levels and truth_levels[char] != level:
                level_conflicts.append({
                    "character": char,
                    "truth_level": truth_levels[char],
                    "mentioned_level": level
                })

        if new_chars:
            issues.append({
                "type": "new_character",
                "severity": "info",
                "message": f"新角色出场: {', '.join(new_chars[:5])}"
            })

        for lc in level_conflicts:
            issues.append({
                "type": "level_conflict",
                "severity": "warning",
                "message": f"{lc['character']} 等级冲突: 真相文件={lc['truth_level']}, 正文={lc['mentioned_level']}"
            })

        results.append({
            "chapter": idx + 1,
            "title": title,
            "word_count": wc,
            "characters": chapter_chars[:10],
            "issues": issues,
            "new_characters": new_chars,
            "level_conflicts": level_conflicts,
        })
        total_issues.extend(issues)
        new_chars_all.update(new_chars)
        level_conflicts_all.extend(level_conflicts)

    return {
        "total_chapters": len(results),
        "truth_files_available": {
            "characters.md": characters_md is not None,
            "current-state.md": current_state is not None,
        },
        "truth_characters_count": len(truth_chars),
        "truth_levels_count": len(truth_levels),
        "chapters": [{"chapter": r["chapter"], "title": r["title"], "word_count": r["word_count"],
                      "characters": r["characters"], "issues": r["issues"]} for r in results],
        "summary": {
            "total_issues": len(total_issues),
            "new_characters": sorted(new_chars_all),
            "level_conflicts": level_conflicts_all,
            "warnings": [i for i in total_issues if i["severity"] == "warning"],
            "info": [i for i in total_issues if i["severity"] == "info"],
        }
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Consistency scan")
    parser.add_argument("chapters_dir", help="Chapters directory")
    parser.add_argument("truth_dir", nargs='?', default=None, help="Truth files directory")
    parser.add_argument("--recent", type=int, help="Only scan last N chapters")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    if not os.path.isdir(args.chapters_dir):
        print(f"Error: {args.chapters_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    truth_dir = args.truth_dir
    if truth_dir is None:
        truth_dir = os.path.join(os.path.dirname(args.chapters_dir.rstrip('/')), 'truth-files')

    result = scan_volume(args.chapters_dir, truth_dir, recent_n=args.recent)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"=== 一致性扫描报告 (最近{result.get('total_chapters', 0)}章) ===\n")
        if 'error' in result:
            print(result['error'])
            return
        chars_ok = '✅' if result['truth_files_available']['characters.md'] else '❌'
        state_ok = '✅' if result['truth_files_available']['current-state.md'] else '❌'
        print(f"真相文件: characters.md={chars_ok}  current-state.md={state_ok}")
        print(f"已知角色: {result['truth_characters_count']}个 | 已知等级: {result['truth_levels_count']}条\n")
        if result["summary"]["warnings"]:
            print("⚠ 等级冲突:")
            for w in result["summary"]["warnings"]:
                print(f"  {w['message']}")
        if result["summary"]["new_characters"]:
            print(f"\n📝 新角色 ({len(result['summary']['new_characters'])}个):")
            for c in result["summary"]["new_characters"][:10]:
                print(f"  {c}")
        if not result["summary"]["warnings"] and not result["summary"]["new_characters"]:
            print("✅ 无一致性问题")
        print()
        for ch in result["chapters"]:
            issues_str = f" [{len(ch['issues'])} issue(s)]" if ch["issues"] else ""
            print(f"  第{ch['chapter']}章: {ch['title']} ({ch['word_count']}字, 角色: {', '.join(ch['characters'][:3])}){issues_str}")


if __name__ == "__main__":
    main()
