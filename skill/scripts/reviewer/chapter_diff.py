#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
章节修订对比 — 比较原稿和修订稿的结构化差异

输出角色/伏笔/字数/结构的变化，供复盘师快速了解修订内容。

用法:
    python scripts/reviewer/chapter_diff.py .novel-maker/temp/ch017-draft.md .novel-maker/temp/ch017-revised.md --json
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'common'))
from nm_utils import (
    read_chapter, extract_characters, extract_locations,
    detect_hook, detect_structure, estimate_pacing,
    clean_markdown, count_chinese
)


def _diff_sets(old_set, new_set):
    added = sorted(new_set - old_set)
    removed = sorted(old_set - new_set)
    kept = sorted(old_set & new_set)
    return {'added': added, 'removed': removed, 'kept': kept}


def _diff_values(old_val, new_val):
    if old_val == new_val:
        return {'changed': False, 'old': old_val, 'new': new_val}
    return {'changed': True, 'old': old_val, 'new': new_val}


def compare_chapters(draft_path, revised_path):
    if not os.path.exists(draft_path):
        return {'error': f'原稿不存在: {draft_path}'}
    if not os.path.exists(revised_path):
        return {'error': f'修订稿不存在: {revised_path}'}

    draft_raw, draft_title, draft_clean, draft_wc = read_chapter(draft_path)
    revised_raw, revised_title, revised_clean, revised_wc = read_chapter(revised_path)

    result = {
        'draft': os.path.basename(draft_path),
        'revised': os.path.basename(revised_path),
        'changes': {}
    }

    # 1. 字数变化
    result['changes']['word_count'] = _diff_values(draft_wc, revised_wc)

    # 2. 标题变化
    result['changes']['title'] = _diff_values(draft_title, revised_title)

    # 3. 角色变化
    draft_chars = set(extract_characters(draft_clean))
    revised_chars = set(extract_characters(revised_clean))
    result['changes']['characters'] = _diff_sets(draft_chars, revised_chars)

    # 4. 地点变化
    draft_locs = set(extract_locations(draft_clean))
    revised_locs = set(extract_locations(revised_clean))
    result['changes']['locations'] = _diff_sets(draft_locs, revised_locs)

    # 5. 章末钩子变化
    draft_hook = detect_hook(draft_raw)
    revised_hook = detect_hook(revised_raw)
    result['changes']['hook'] = _diff_values(
        draft_hook['type'], revised_hook['type']
    )

    # 6. 结构变化
    draft_struct = detect_structure(draft_raw)
    revised_struct = detect_structure(revised_raw)
    result['changes']['structure'] = {
        'draft': draft_struct,
        'revised': revised_struct
    }

    # 7. 节奏变化
    draft_pacing, draft_score = estimate_pacing(draft_raw)
    revised_pacing, revised_score = estimate_pacing(revised_raw)
    result['changes']['pacing'] = _diff_values(
        f'{draft_pacing}({draft_score})', f'{revised_pacing}({revised_score})'
    )

    # 汇总
    significant = []
    wc_change = result['changes']['word_count']
    if wc_change['changed']:
        diff = wc_change['new'] - wc_change['old']
        significant.append(f"字数变化: {diff:+d}")

    char_change = result['changes']['characters']
    if char_change['added']:
        significant.append(f"新增角色: {', '.join(char_change['added'])}")
    if char_change['removed']:
        significant.append(f"移除角色: {', '.join(char_change['removed'])}")

    hook_change = result['changes']['hook']
    if hook_change['changed']:
        significant.append(f"钩子变化: {hook_change['old']} → {hook_change['new']}")

    result['summary'] = {
        'significant_changes': significant,
        'change_count': len(significant)
    }

    return result


def main():
    parser = argparse.ArgumentParser(description='章节修订对比')
    parser.add_argument('draft', help='原稿文件路径')
    parser.add_argument('revised', help='修订稿文件路径')
    parser.add_argument('--json', action='store_true', help='JSON输出')
    args = parser.parse_args()

    result = compare_chapters(args.draft, args.revised)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if 'error' in result:
            print(f"错误: {result['error']}")
            return
        print(f"=== 章节修订对比 ===\n")
        print(f"原稿: {result['draft']}")
        print(f"修订: {result['revised']}\n")

        for change in result['summary']['significant_changes']:
            print(f"  {change}")

        if not result['summary']['significant_changes']:
            print("  无显著变化")


if __name__ == '__main__':
    main()
