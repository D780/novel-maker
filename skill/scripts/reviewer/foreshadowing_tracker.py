#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
伏笔追踪器
追踪小说中伏笔的设置和回收情况，检测未回收的伏笔。
供复盘师在卷末复盘时使用，或规划师在规划伏笔时参考。

用法:
    python scripts/reviewer/foreshadowing_tracker.py 章节目录 --json
    python scripts/reviewer/foreshadowing_tracker.py 章节目录 --recent 20
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'common'))
from nm_utils import (
    list_chapters, read_chapter, count_chinese, clean_markdown
)

# ─── 伏笔关键词模式 ───────────────────────────────
FORESHADOWING_PATTERNS = {
    '悬念型': {
        'setup_keywords': ['秘密', '真相', '隐藏', '未知', '谜团', '疑问', '为什么', '怎么回事'],
        'resolution_keywords': ['原来', '竟然', '居然', '真相大白', '揭晓', '揭示', '发现']
    },
    '预言型': {
        'setup_keywords': ['预言', '传说', '古老', '命运', '注定', '将会', '总有一天'],
        'resolution_keywords': ['应验', '实现', '果然', '如预言般', '命中注定']
    },
    '物品型': {
        'setup_keywords': ['宝物', '神器', '秘籍', '钥匙', '信物', '遗物', '传承'],
        'resolution_keywords': ['使用', '激活', '开启', '获得', '继承', '发挥']
    },
    '人物型': {
        'setup_keywords': ['神秘人', '陌生人', '身份', '来历', '背景', '过去'],
        'resolution_keywords': ['身份揭晓', '原来是', '竟然是', '真实身份']
    },
    '危机型': {
        'setup_keywords': ['危险', '威胁', '隐患', '危机', '不安', '预感'],
        'resolution_keywords': ['爆发', '降临', '到来', '发生', '应验']
    }
}


def detect_foreshadowing_in_chapter(filepath):
    """Detect foreshadowing setups and resolutions in a chapter."""
    raw, title, clean, wc = read_chapter(filepath)

    setups = []
    resolutions = []

    for foreshadowing_type, config in FORESHADOWING_PATTERNS.items():
        # Detect setups
        for keyword in config['setup_keywords']:
            positions = [m.start() for m in re.finditer(keyword, clean)]
            for pos in positions:
                # Get context around the keyword
                start = max(0, pos - 50)
                end = min(len(clean), pos + 50)
                context = clean[start:end].replace('\n', ' ')

                setups.append({
                    'type': foreshadowing_type,
                    'keyword': keyword,
                    'context': context,
                    'position': pos
                })

        # Detect resolutions
        for keyword in config['resolution_keywords']:
            positions = [m.start() for m in re.finditer(keyword, clean)]
            for pos in positions:
                start = max(0, pos - 50)
                end = min(len(clean), pos + 50)
                context = clean[start:end].replace('\n', ' ')

                resolutions.append({
                    'type': foreshadowing_type,
                    'keyword': keyword,
                    'context': context,
                    'position': pos
                })

    return {
        'chapter': title,
        'word_count': wc,
        'setups': setups[:10],  # Limit to 10 per chapter
        'resolutions': resolutions[:10]
    }


def track_foreshadowing_across_chapters(chapters_dir, recent_n=None):
    """Track foreshadowing across multiple chapters."""
    chapter_files = list_chapters(chapters_dir, recent_n)
    if not chapter_files:
        return {'error': '未找到章节文件'}

    all_setups = []
    all_resolutions = []
    chapter_data = []

    for idx, cf in enumerate(chapter_files):
        ch_data = detect_foreshadowing_in_chapter(cf)
        chapter_data.append(ch_data)

        for setup in ch_data['setups']:
            setup['chapter_num'] = idx + 1
            setup['chapter_title'] = ch_data['chapter']
            all_setups.append(setup)

        for resolution in ch_data['resolutions']:
            resolution['chapter_num'] = idx + 1
            resolution['chapter_title'] = ch_data['chapter']
            all_resolutions.append(resolution)

    # Analyze foreshadowing status
    setup_types = defaultdict(int)
    resolution_types = defaultdict(int)

    for setup in all_setups:
        setup_types[setup['type']] += 1

    for resolution in all_resolutions:
        resolution_types[resolution['type']] += 1

    # Calculate resolution rate
    total_setups = len(all_setups)
    total_resolutions = len(all_resolutions)
    resolution_rate = round(total_resolutions / max(total_setups, 1) * 100, 1)

    # Detect unresolved foreshadowing (setups without matching resolutions)
    unresolved_by_type = {}
    for foreshadowing_type in FORESHADOWING_PATTERNS.keys():
        setup_count = setup_types.get(foreshadowing_type, 0)
        resolution_count = resolution_types.get(foreshadowing_type, 0)
        unresolved = setup_count - resolution_count
        if unresolved > 0:
            unresolved_by_type[foreshadowing_type] = {
                'setups': setup_count,
                'resolutions': resolution_count,
                'unresolved': unresolved
            }

    # Generate auto-recovery suggestions
    suggestions = generate_recovery_suggestions(unresolved_by_type, all_setups, len(chapter_files))

    return {
        'total_chapters': len(chapter_files),
        'total_setups': total_setups,
        'total_resolutions': total_resolutions,
        'resolution_rate': resolution_rate,
        'setup_types': dict(setup_types),
        'resolution_types': dict(resolution_types),
        'unresolved_by_type': unresolved_by_type,
        'recent_setups': all_setups[-10:],
        'recent_resolutions': all_resolutions[-10:],
        'chapter_data': chapter_data[-5:],  # Last 5 chapters
        'suggestions': suggestions
    }


def generate_recovery_suggestions(unresolved_by_type, all_setups, total_chapters):
    """Generate automatic recovery suggestions for unresolved foreshadowing."""
    suggestions = []

    # Recovery templates for each foreshadowing type
    recovery_templates = {
        '悬念型': {
            'suggestion': '在后续章节中安排真相揭露场景',
            'example': '可以安排一个关键角色揭示秘密，或者主角通过调查发现真相',
            'timing': '建议在5-10章内回收'
        },
        '预言型': {
            'suggestion': '让预言在关键时刻应验',
            'example': '可以在高潮章节让预言成真，增强戏剧性',
            'timing': '建议在卷末或重要转折点回收'
        },
        '物品型': {
            'suggestion': '让物品在关键时刻发挥作用',
            'example': '可以在危机时刻激活宝物/神器，扭转局势',
            'timing': '建议在3-8章内回收'
        },
        '人物型': {
            'suggestion': '揭示神秘人物的真实身份',
            'example': '可以安排身份揭露场景，制造意外转折',
            'timing': '建议在5-15章内回收'
        },
        '危机型': {
            'suggestion': '让预感的危机真正降临',
            'example': '可以在平静章节后突然爆发危机，制造紧张感',
            'timing': '建议在3-10章内回收'
        }
    }

    for foreshadowing_type, data in unresolved_by_type.items():
        if foreshadowing_type in recovery_templates:
            template = recovery_templates[foreshadowing_type]

            # Find the earliest setup for this type
            earliest_setup = None
            for setup in all_setups:
                if setup['type'] == foreshadowing_type:
                    earliest_setup = setup
                    break

            suggestion = {
                'type': foreshadowing_type,
                'unresolved_count': data['unresolved'],
                'suggestion': template['suggestion'],
                'example': template['example'],
                'timing': template['timing']
            }

            if earliest_setup:
                suggestion['first_setup_chapter'] = earliest_setup.get('chapter_num', '未知')
                suggestion['context_preview'] = earliest_setup.get('context', '')[:50]

            suggestions.append(suggestion)

    return suggestions


def main():
    parser = argparse.ArgumentParser(description='伏笔追踪器')
    parser.add_argument('chapters_dir', help='章节目录路径')
    parser.add_argument('--recent', type=int, help='仅分析最近N章')
    parser.add_argument('--json', action='store_true', help='JSON输出')
    args = parser.parse_args()

    if not os.path.isdir(args.chapters_dir):
        print(f"错误: 目录不存在: {args.chapters_dir}", file=sys.stderr)
        sys.exit(1)

    result = track_foreshadowing_across_chapters(args.chapters_dir, args.recent)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if 'error' in result:
            print(result['error'])
            return

        print(f"\n=== 伏笔追踪报告 ===\n")
        print(f"分析章节数: {result['total_chapters']}")
        print(f"伏笔设置数: {result['total_setups']}")
        print(f"伏笔回收数: {result['total_resolutions']}")
        print(f"回收率: {result['resolution_rate']}%")

        print(f"\n伏笔类型分布:")
        for foreshadowing_type in FORESHADOWING_PATTERNS.keys():
            setup_count = result['setup_types'].get(foreshadowing_type, 0)
            resolution_count = result['resolution_types'].get(foreshadowing_type, 0)
            if setup_count > 0:
                print(f"  {foreshadowing_type}: 设置{setup_count}次, 回收{resolution_count}次")

        if result['unresolved_by_type']:
            print(f"\n未回收伏笔:")
            for foreshadowing_type, data in result['unresolved_by_type'].items():
                print(f"  ⚠ {foreshadowing_type}: {data['unresolved']}个未回收 (设置{data['setups']}次, 回收{data['resolutions']}次)")
        else:
            print(f"\n✓ 所有伏笔类型均有回收")

        print(f"\n最近伏笔设置:")
        for setup in result['recent_setups'][-5:]:
            print(f"  第{setup['chapter_num']}章 [{setup['type']}]: {setup['context'][:60]}...")

        print(f"\n最近伏笔回收:")
        for resolution in result['recent_resolutions'][-5:]:
            print(f"  第{resolution['chapter_num']}章 [{resolution['type']}]: {resolution['context'][:60]}...")

        # 输出回收建议
        if result.get('suggestions'):
            print(f"\n回收建议:")
            for suggestion in result['suggestions']:
                print(f"  [{suggestion['type']}] {suggestion['suggestion']}")
                print(f"    示例: {suggestion['example']}")
                print(f"    时机: {suggestion['timing']}")


if __name__ == '__main__':
    main()
