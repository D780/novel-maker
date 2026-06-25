#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
钩子密度报告
分析卷内所有章节的结尾钩子，输出类型分布、连续相同钩子警告。
"""

import os
import sys
import json
from collections import Counter

from nw_utils import (
    list_chapters, read_chapter, detect_hook, detect_hook_type_from_patterns
)


def extract_last_paragraphs(text, n=3):
    """Extract last N paragraphs (likely contains chapter ending hook)."""
    paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    if not paragraphs:
        return text[-300:]
    return '\n'.join(paragraphs[-n:])


def analyze_volume(chapters_dir, recent_n=None):
    chapter_files = list_chapters(chapters_dir, recent_n)
    if not chapter_files:
        return {'error': f'No chapters found in {chapters_dir}'}

    results = []
    for idx, filepath in enumerate(chapter_files):
        raw, title, clean, wc = read_chapter(filepath)
        ending = extract_last_paragraphs(raw)
        hook_type = detect_hook_type_from_patterns(ending)

        hook_sentences = []
        import re
        for m in re.finditer(r'[^。！？\n]{5,50}[。！？]', raw):
            sentence = m.group(0)
            from nw_utils import _HOOK_PATTERN_MAP
            if any(pattern.search(sentence) for pattern in _HOOK_PATTERN_MAP.values()):
                hook_sentences.append(sentence.strip())

        results.append({
            "chapter": idx + 1,
            "title": title,
            "word_count": wc,
            "hook_type": hook_type,
            "hook_sentences": hook_sentences[:3],
            "ending_summary": ending[:200],
        })

    hook_types = [r["hook_type"] for r in results]
    hook_dist = dict(Counter(hook_types))

    consecutive_same = []
    if len(hook_types) >= 3:
        for i in range(len(hook_types) - 2):
            if hook_types[i] == hook_types[i+1] == hook_types[i+2]:
                consecutive_same.append(f"第{results[i]['chapter']}-{results[i+2]['chapter']}章连续使用「{hook_types[i]}」钩子")

    return {
        "total_chapters": len(results),
        "hook_distribution": hook_dist,
        "chapters": results,
        "warnings": {
            "consecutive_same_hook": consecutive_same,
            "unknown_hooks": sum(1 for h in hook_types if h == "未知"),
        }
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Hook density report")
    parser.add_argument("chapters_dir", help="Chapters directory")
    parser.add_argument("--recent", type=int, help="Only analyze last N chapters")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    chapters_dir = args.chapters_dir
    if not os.path.isdir(chapters_dir):
        print(f"Error: {chapters_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    result = analyze_volume(chapters_dir, recent_n=args.recent)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"=== 钩子密度报告 (最近{result.get('total_chapters', 0)}章) ===\n")
        if 'error' in result:
            print(result['error'])
            return
        print("钩子类型分布:")
        for hook_type, count in sorted(result["hook_distribution"].items(),
                                        key=lambda x: x[1], reverse=True):
            bar = "█" * count
            print(f"  {hook_type:4s}: {bar} ({count})")
        print()
        if result["warnings"]["consecutive_same_hook"]:
            print("⚠ 警告 - 连续相同钩子:")
            for w in result["warnings"]["consecutive_same_hook"]:
                print(f"  {w}")
        if result["warnings"]["unknown_hooks"] > 0:
            print(f"\n⚠ {result['warnings']['unknown_hooks']} 章钩子类型未知，建议手动标记")
        print()
        for ch in result["chapters"]:
            print(f"  第{ch['chapter']}章 [{ch['hook_type']}]: {ch['ending_summary'][:80]}...")


if __name__ == "__main__":
    main()
