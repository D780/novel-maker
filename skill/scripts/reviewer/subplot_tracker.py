#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
支线追踪器
追踪小说中的支线剧情发展状态，检测未回收的伏笔和断裂的支线。
供复盘师在卷末复盘时使用，或规划师在规划新支线时参考。

用法:
    python scripts/reviewer/subplot_tracker.py 章节目录 --json
    python scripts/reviewer/subplot_tracker.py 章节目录 --verbose
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
    detect_hook, count_chinese
)

# ─── 支线类型定义 ───────────────────────────────
SUBPLOT_PATTERNS = {
    '感情线': {
        'keywords': ['喜欢', '爱', '情', '心动', '暗恋', '表白', '分手', '复合', '婚姻'],
        'indicators': ['两人独处', '眼神交流', '心跳加速', '脸红', '牵手']
    },
    '复仇线': {
        'keywords': ['仇', '恨', '报复', '凶手', '仇人', '血债', '讨回'],
        'indicators': ['调查真相', '寻找证据', '准备复仇', ' confrontation']
    },
    '成长线': {
        'keywords': ['修炼', '突破', '进阶', '领悟', '提升', '实力'],
        'indicators': ['闭关', '顿悟', '突破瓶颈', '新技能']
    },
    '阴谋线': {
        'keywords': ['阴谋', '计划', '暗中', '秘密', '隐藏', '真相'],
        'indicators': ['密谋', '布局', '暗中观察', '设局']
    },
    '冒险线': {
        'keywords': ['探险', '寻宝', '秘境', '遗迹', '未知', '危险'],
        'indicators': ['出发', '探索', '发现', '遭遇危险']
    }
}


def detect_subplot_mentions(text):
    """Detect subplot mentions in text."""
    mentions = defaultdict(list)

    for subplot_type, config in SUBPLOT_PATTERNS.items():
        for keyword in config['keywords']:
            if keyword in text:
                mentions[subplot_type].append(keyword)
        for indicator in config['indicators']:
            if indicator in text:
                mentions[subplot_type].append(f"[{indicator}]")

    return dict(mentions)


def track_subplot_across_chapters(chapters_dir, recent_n=None):
    """Track subplot development across chapters."""
    chapter_files = list_chapters(chapters_dir, recent_n)
    if not chapter_files:
        return {'error': '未找到章节文件'}

    subplot_timeline = defaultdict(list)
    subplot_status = {}

    for idx, cf in enumerate(chapter_files):
        raw, title, clean, wc = read_chapter(cf)
        ch_num = idx + 1

        # Detect subplot mentions
        mentions = detect_subplot_mentions(clean)

        for subplot_type, keywords in mentions.items():
            subplot_timeline[subplot_type].append({
                'chapter_num': ch_num,
                'chapter_title': title,
                'keywords': list(set(keywords))[:5],  # Limit to 5 keywords
                'word_count': wc
            })

    # Analyze subplot status
    for subplot_type, timeline in subplot_timeline.items():
        total_chapters = len(timeline)
        first_chapter = timeline[0]['chapter_num'] if timeline else 0
        last_chapter = timeline[-1]['chapter_num'] if timeline else 0

        # Determine status
        if total_chapters == 0:
            status = '未出现'
        elif total_chapters == 1:
            status = '刚引入'
        elif last_chapter - first_chapter < 3:
            status = '发展中'
        elif total_chapters > len(chapter_files) * 0.3:
            status = '主要支线'
        else:
            status = '间歇性出现'

        subplot_status[subplot_type] = {
            'status': status,
            'total_chapters': total_chapters,
            'first_appearance': first_chapter,
            'last_appearance': last_chapter,
            'chapters_involved': [t['chapter_num'] for t in timeline],
            'timeline': timeline[-5:]  # Last 5 appearances
        }

    return {
        'total_chapters_analyzed': len(chapter_files),
        'subplots_detected': len(subplot_timeline),
        'subplot_status': subplot_status,
        'subplot_timeline': dict(subplot_timeline)
    }


def check_subplot_consistency(result):
    """Check for subplot consistency issues."""
    issues = []

    for subplot_type, status in result.get('subplot_status', {}).items():
        # Check for abandoned subplots
        if status['status'] == '刚引入' and result['total_chapters_analyzed'] > 10:
            issues.append({
                'type': '可能遗弃',
                'subplot': subplot_type,
                'message': f"{subplot_type}在第{status['first_appearance']}章引入后未再出现",
                'severity': 'warning'
            })

        # Check for inconsistent pacing
        if status['total_chapters'] > 0:
            chapters = status['chapters_involved']
            gaps = [chapters[i+1] - chapters[i] for i in range(len(chapters)-1)]
            if gaps and max(gaps) > 5:
                issues.append({
                    'type': '节奏不均',
                    'subplot': subplot_type,
                    'message': f"{subplot_type}章节间隔过大（最大{max(gaps)}章）",
                    'severity': 'info'
                })

    return issues


def main():
    parser = argparse.ArgumentParser(description='支线追踪器')
    parser.add_argument('chapters_dir', help='章节目录路径')
    parser.add_argument('--recent', type=int, help='仅分析最近N章')
    parser.add_argument('--json', action='store_true', help='JSON输出')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细信息')
    args = parser.parse_args()

    if not os.path.isdir(args.chapters_dir):
        print(f"错误: 目录不存在: {args.chapters_dir}", file=sys.stderr)
        sys.exit(1)

    result = track_subplot_across_chapters(args.chapters_dir, args.recent)

    # Add consistency check
    if not args.json:
        issues = check_subplot_consistency(result)
        result['consistency_issues'] = issues

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if 'error' in result:
            print(result['error'])
            return

        print(f"\n=== 支线追踪报告 ===\n")
        print(f"分析章节数: {result['total_chapters_analyzed']}")
        print(f"检测支线数: {result['subplots_detected']}")

        print(f"\n支线状态:")
        for subplot_type, status in result['subplot_status'].items():
            icon = '●' if status['status'] == '主要支线' else '○'
            print(f"  {icon} {subplot_type}: {status['status']}")
            print(f"     出场章数: {status['total_chapters']}, 首次: 第{status['first_appearance']}章, 最近: 第{status['last_appearance']}章")

        if result.get('consistency_issues'):
            print(f"\n一致性问题:")
            for issue in result['consistency_issues']:
                icon = '' if issue['severity'] == 'warning' else 'ℹ'
                print(f"  {icon} {issue['subplot']}: {issue['message']}")

        if args.verbose and result.get('subplot_timeline'):
            print(f"\n详细时间线:")
            for subplot_type, timeline in result['subplot_timeline'].items():
                print(f"\n  {subplot_type}:")
                for entry in timeline[-5:]:  # Last 5 entries
                    print(f"    第{entry['chapter_num']}章: {entry['chapter_title']}")
                    if entry['keywords']:
                        print(f"      关键词: {', '.join(entry['keywords'])}")


if __name__ == '__main__':
    main()
