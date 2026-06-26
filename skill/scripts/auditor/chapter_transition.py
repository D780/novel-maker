#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
章节衔接检查脚本
检测章节之间的衔接问题：时间跳跃、地点突变、角色消失、情绪断裂等。
供审计师在审查时使用，或写手在连续写作时自查。

用法:
    python scripts/auditor/chapter_transition.py 章节目录 --json
    python scripts/auditor/chapter_transition.py 章节目录 --recent 5
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'common'))
from nm_utils import (
    list_chapters, read_chapter, extract_characters, extract_locations,
    detect_hook, count_chinese, generate_summary
)

# ─── 时间表达关键词 ───────────────────────────────
TIME_EXPRESSIONS = {
    '瞬间': ['突然', '忽然', '刹那间', '瞬间', '立刻', '马上'],
    '短期': ['第二天', '次日', '当晚', '傍晚', '清晨', '午后', '片刻', '一会儿'],
    '中期': ['几天后', '一周后', '半月后', '一个月后', '数月后'],
    '长期': ['一年后', '数年后', '多年后', '几年后', '十年后']
}

# ─── 地点转换关键词 ───────────────────────────────
LOCATION_TRANSITIONS = ['来到', '到达', '回到', '前往', '进入', '离开', '返回', '抵达']


def analyze_chapter_ending(filepath, last_n=500):
    """Analyze the ending of a chapter."""
    raw, title, clean, wc = read_chapter(filepath)
    tail = clean[-last_n:] if len(clean) > last_n else clean

    # Extract ending characters
    ending_chars = extract_characters(tail)

    # Extract ending locations
    ending_locs = extract_locations(tail)

    # Detect hook
    hook = detect_hook(raw)

    # Detect time expressions
    time_expressions = []
    for category, keywords in TIME_EXPRESSIONS.items():
        for kw in keywords:
            if kw in tail:
                time_expressions.append({'category': category, 'keyword': kw})

    return {
        'title': title,
        'word_count': wc,
        'ending_chars': ending_chars[:5],
        'ending_locations': ending_locs[:3],
        'hook': hook['type'],
        'time_expressions': time_expressions,
        'tail_preview': tail[-100:]
    }


def analyze_chapter_beginning(filepath, first_n=500):
    """Analyze the beginning of a chapter."""
    raw, title, clean, wc = read_chapter(filepath)
    head = clean[:first_n] if len(clean) > first_n else clean

    # Extract beginning characters
    beginning_chars = extract_characters(head)

    # Extract beginning locations
    beginning_locs = extract_locations(head)

    # Detect time expressions
    time_expressions = []
    for category, keywords in TIME_EXPRESSIONS.items():
        for kw in keywords:
            if kw in head:
                time_expressions.append({'category': category, 'keyword': kw})

    # Detect location transitions
    location_transitions = []
    for transition in LOCATION_TRANSITIONS:
        if transition in head:
            location_transitions.append(transition)

    return {
        'title': title,
        'word_count': wc,
        'beginning_chars': beginning_chars[:5],
        'beginning_locations': beginning_locs[:3],
        'time_expressions': time_expressions,
        'location_transitions': location_transitions,
        'head_preview': head[:100]
    }


def check_transition(chapter_files):
    """Check transitions between consecutive chapters."""
    transitions = []

    for i in range(len(chapter_files) - 1):
        curr_file = chapter_files[i]
        next_file = chapter_files[i + 1]

        curr_ending = analyze_chapter_ending(curr_file)
        next_beginning = analyze_chapter_beginning(next_file)

        issues = []

        # 1. Character continuity check
        curr_chars = set(curr_ending['ending_chars'])
        next_chars = set(next_beginning['beginning_chars'])
        if curr_chars and not (curr_chars & next_chars):
            issues.append({
                'type': '角色断裂',
                'message': f"上章结尾角色({', '.join(curr_ending['ending_chars'][:3])})未在下章开头出现",
                'severity': 'warning'
            })

        # 2. Location continuity check
        curr_locs = set(curr_ending['ending_locations'])
        next_locs = set(next_beginning['beginning_locations'])
        if curr_locs and not (curr_locs & next_locs) and not next_beginning['location_transitions']:
            issues.append({
                'type': '地点突变',
                'message': f"上章地点({', '.join(curr_ending['ending_locations'][:2])})到下章地点({', '.join(next_beginning['beginning_locations'][:2])})无过渡",
                'severity': 'info'
            })

        # 3. Time expression check
        if next_beginning['time_expressions']:
            time_cats = [t['category'] for t in next_beginning['time_expressions']]
            if '长期' in time_cats:
                issues.append({
                    'type': '时间跳跃',
                    'message': f"下章开头有长期时间跳跃（{', '.join(t['keyword'] for t in next_beginning['time_expressions'] if t['category']=='长期')}）",
                    'severity': 'info'
                })

        # 4. Hook resolution check
        if curr_ending['hook'] != '未检测':
            issues.append({
                'type': '钩子待回收',
                'message': f"上章钩子类型: {curr_ending['hook']}",
                'severity': 'info'
            })

        transitions.append({
            'from_chapter': curr_ending['title'],
            'to_chapter': next_beginning['title'],
            'issues': issues,
            'issue_count': len(issues)
        })

    return transitions


def main():
    parser = argparse.ArgumentParser(description='章节衔接检查脚本')
    parser.add_argument('chapters_dir', help='章节目录路径')
    parser.add_argument('--recent', type=int, help='仅检查最近N章的衔接')
    parser.add_argument('--json', action='store_true', help='JSON输出')
    args = parser.parse_args()

    if not os.path.isdir(args.chapters_dir):
        print(f"错误: 目录不存在: {args.chapters_dir}", file=sys.stderr)
        sys.exit(1)

    chapter_files = list_chapters(args.chapters_dir, args.recent)
    if len(chapter_files) < 2:
        print("错误: 至少需要2个章节才能检查衔接", file=sys.stderr)
        sys.exit(1)

    transitions = check_transition(chapter_files)

    # Calculate summary
    total_issues = sum(t['issue_count'] for t in transitions)
    warning_count = sum(1 for t in transitions for i in t['issues'] if i['severity'] == 'warning')

    result = {
        'total_chapters': len(chapter_files),
        'transitions_checked': len(transitions),
        'total_issues': total_issues,
        'warning_count': warning_count,
        'transitions': transitions
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"\n=== 章节衔接检查 ===\n")
        print(f"章节数: {result['total_chapters']}")
        print(f"检查衔接数: {result['transitions_checked']}")
        print(f"问题总数: {result['total_issues']}")
        print(f"警告数: {result['warning_count']}")

        print(f"\n衔接详情:")
        for trans in transitions:
            if trans['issues']:
                print(f"\n  {trans['from_chapter']} → {trans['to_chapter']}:")
                for issue in trans['issues']:
                    icon = '⚠' if issue['severity'] == 'warning' else 'ℹ'
                    print(f"    {icon} {issue['type']}: {issue['message']}")
            else:
                print(f"\n  ✓ {trans['from_chapter']} → {trans['to_chapter']}: 无问题")


if __name__ == '__main__':
    main()
