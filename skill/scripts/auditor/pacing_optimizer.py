#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
节奏优化建议脚本
基于节奏分析结果，提供具体的优化建议，帮助改善故事节奏。
供审计师在审查时使用，或写手在修改时参考。

用法:
    python scripts/auditor/pacing_optimizer.py 章节目录 --json
    python scripts/auditor/pacing_optimizer.py 章节目录 --recent 10
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'common'))
from nm_utils import (
    list_chapters, read_chapter, estimate_pacing, count_chinese,
    detect_hook_type_from_patterns
)

# ─── 节奏规则 ───────────────────────────────
PACING_RULES = {
    'max_consecutive_high': 3,  # 不能连续3章S4+
    'max_consecutive_low': 3,   # 不能连续3章S2-
    'max_no_peak_interval': 8,  # 每8章必须有S4/S5
    'max_no_mid_interval': 3,   # 每3章必须有S3+
    'ideal_peak_ratio': 0.15,   # 理想高潮比例 15%
    'ideal_mid_ratio': 0.35,    # 理想上升比例 35%
    'ideal_low_ratio': 0.25,    # 理想平缓比例 25%
    'ideal_valley_ratio': 0.10  # 理想低谷比例 10%
}

# ─── 优化建议模板 ──────────────────────────────
OPTIMIZATION_SUGGESTIONS = {
    'consecutive_high': {
        'problem': '连续高潮',
        'suggestion': '在高潮后插入1-2章平缓或低谷章节，让读者有喘息空间',
        'example': '可以在第{chapter}章后加入角色日常、内心反思或环境描写'
    },
    'consecutive_low': {
        'problem': '连续平淡',
        'suggestion': '在平淡章节中插入小冲突或悬念，提升节奏',
        'example': '可以在第{chapter}章加入意外事件、新角色登场或旧伏笔回收'
    },
    'no_peak': {
        'problem': '缺乏高潮',
        'suggestion': '在适当位置安排高潮章节，提升故事张力',
        'example': '建议在第{chapter}章安排一次重要对决或关键转折'
    },
    'no_mid': {
        'problem': '缺乏上升',
        'suggestion': '增加上升章节，为高潮做铺垫',
        'example': '可以在第{chapter}章加入角色成长、实力提升或关系进展'
    },
    'peak_ratio_low': {
        'problem': '高潮比例过低',
        'suggestion': '增加高潮章节数量，提升故事吸引力',
        'example': '当前高潮比例{current}%，建议提升到{ideal}%'
    },
    'peak_ratio_high': {
        'problem': '高潮比例过高',
        'suggestion': '适当降低高潮频率，避免读者疲劳',
        'example': '当前高潮比例{current}%，建议降低到{ideal}%'
    },
    'hook_missing': {
        'problem': '章节结尾缺乏钩子',
        'suggestion': '在章节结尾设置悬念或转折，吸引读者继续阅读',
        'example': '可以在第{chapter}章结尾加入未解之谜或突发事件'
    },
    'pacing_jump': {
        'problem': '节奏跳跃过大',
        'suggestion': '在节奏突变处增加过渡章节，使变化更自然',
        'example': '第{chapter}章从{from_pacing}直接跳到{to_pacing}，建议加入过渡'
    }
}


def analyze_pacing_with_suggestions(chapters_dir, recent_n=None):
    """Analyze pacing and generate optimization suggestions."""
    chapter_files = list_chapters(chapters_dir, recent_n)
    if not chapter_files:
        return {'error': '未找到章节文件'}

    # Analyze each chapter
    chapters = []
    pacing_sequence = []

    for idx, cf in enumerate(chapter_files):
        raw, title, clean, wc = read_chapter(cf)
        pacing_label, pacing_score = estimate_pacing(clean)
        hook = detect_hook_type_from_patterns(raw)

        chapters.append({
            'chapter_num': idx + 1,
            'title': title,
            'word_count': wc,
            'pacing': pacing_label,
            'pacing_score': pacing_score,
            'hook': hook if isinstance(hook, str) else hook.get('type', '未知')
        })
        pacing_sequence.append(pacing_label)

    # Calculate distribution
    pacing_dist = defaultdict(int)
    for p in pacing_sequence:
        pacing_dist[p] += 1

    total = len(pacing_sequence)
    ratios = {k: round(v / max(total, 1) * 100, 1) for k, v in pacing_dist.items()}

    # Detect issues and generate suggestions
    issues = []
    suggestions = []

    # 1. Check consecutive high/low
    current_pacing = pacing_sequence[0] if pacing_sequence else None
    streak_start = 0

    for i, pacing in enumerate(pacing_sequence):
        if pacing != current_pacing:
            streak_length = i - streak_start

            if current_pacing in ['S4', 'S5'] and streak_length >= PACING_RULES['max_consecutive_high']:
                issues.append({
                    'type': 'consecutive_high',
                    'chapters': f"第{streak_start+1}-{i}章",
                    'length': streak_length
                })
                suggestions.append({
                    'type': 'consecutive_high',
                    'chapter': streak_start + 1,
                    'detail': OPTIMIZATION_SUGGESTIONS['consecutive_high']['suggestion'],
                    'example': OPTIMIZATION_SUGGESTIONS['consecutive_high']['example'].format(chapter=streak_start + 1)
                })

            elif current_pacing in ['S1', 'S2'] and streak_length >= PACING_RULES['max_consecutive_low']:
                issues.append({
                    'type': 'consecutive_low',
                    'chapters': f"第{streak_start+1}-{i}章",
                    'length': streak_length
                })
                suggestions.append({
                    'type': 'consecutive_low',
                    'chapter': streak_start + 1,
                    'detail': OPTIMIZATION_SUGGESTIONS['consecutive_low']['suggestion'],
                    'example': OPTIMIZATION_SUGGESTIONS['consecutive_low']['example'].format(chapter=streak_start + 1)
                })

            current_pacing = pacing
            streak_start = i

    # 2. Check peak interval
    last_peak = None
    for i, pacing in enumerate(pacing_sequence):
        if pacing in ['S4', 'S5']:
            if last_peak is not None and (i - last_peak) > PACING_RULES['max_no_peak_interval']:
                issues.append({
                    'type': 'no_peak',
                    'gap': i - last_peak,
                    'chapters': f"第{last_peak+1}-{i}章"
                })
                suggestions.append({
                    'type': 'no_peak',
                    'chapter': last_peak + PACING_RULES['max_no_peak_interval'] // 2,
                    'detail': OPTIMIZATION_SUGGESTIONS['no_peak']['suggestion'],
                    'example': OPTIMIZATION_SUGGESTIONS['no_peak']['example'].format(
                        chapter=last_peak + PACING_RULES['max_no_peak_interval'] // 2
                    )
                })
            last_peak = i

    # 3. Check mid interval
    last_mid = None
    for i, pacing in enumerate(pacing_sequence):
        if pacing in ['S3', 'S4', 'S5']:
            if last_mid is not None and (i - last_mid) > PACING_RULES['max_no_mid_interval']:
                issues.append({
                    'type': 'no_mid',
                    'gap': i - last_mid,
                    'chapters': f"第{last_mid+1}-{i}章"
                })
                suggestions.append({
                    'type': 'no_mid',
                    'chapter': last_mid + PACING_RULES['max_no_mid_interval'] // 2,
                    'detail': OPTIMIZATION_SUGGESTIONS['no_mid']['suggestion'],
                    'example': OPTIMIZATION_SUGGESTIONS['no_mid']['example'].format(
                        chapter=last_mid + PACING_RULES['max_no_mid_interval'] // 2
                    )
                })
            last_mid = i

    # 4. Check ratios
    peak_ratio = ratios.get('S4', 0) + ratios.get('S5', 0)
    if peak_ratio < PACING_RULES['ideal_peak_ratio'] * 100 * 0.7:  # 30% below ideal
        suggestions.append({
            'type': 'peak_ratio_low',
            'current': round(peak_ratio, 1),
            'ideal': round(PACING_RULES['ideal_peak_ratio'] * 100, 1),
            'detail': OPTIMIZATION_SUGGESTIONS['peak_ratio_low']['suggestion'],
            'example': OPTIMIZATION_SUGGESTIONS['peak_ratio_low']['example'].format(
                current=round(peak_ratio, 1),
                ideal=round(PACING_RULES['ideal_peak_ratio'] * 100, 1)
            )
        })

    # 5. Check hooks
    hook_missing_chapters = [ch for ch in chapters if ch['hook'] == '未检测']
    if hook_missing_chapters:
        suggestions.append({
            'type': 'hook_missing',
            'count': len(hook_missing_chapters),
            'chapters': [ch['chapter_num'] for ch in hook_missing_chapters[:5]],
            'detail': OPTIMIZATION_SUGGESTIONS['hook_missing']['suggestion'],
            'example': f"以下章节缺少钩子：{', '.join(f'第{ch}章' for ch in hook_missing_chapters[:5])}"
        })

    # 6. Check pacing jumps
    for i in range(len(pacing_sequence) - 1):
        from_score = chapters[i]['pacing_score']
        to_score = chapters[i+1]['pacing_score']
        if abs(to_score - from_score) > 2:  # Jump of more than 2 levels
            issues.append({
                'type': 'pacing_jump',
                'from_chapter': i + 1,
                'to_chapter': i + 2,
                'from_pacing': chapters[i]['pacing'],
                'to_pacing': chapters[i+1]['pacing']
            })
            suggestions.append({
                'type': 'pacing_jump',
                'chapter': i + 1,
                'from_pacing': chapters[i]['pacing'],
                'to_pacing': chapters[i+1]['pacing'],
                'detail': OPTIMIZATION_SUGGESTIONS['pacing_jump']['suggestion'],
                'example': OPTIMIZATION_SUGGESTIONS['pacing_jump']['example'].format(
                    chapter=i + 1,
                    from_pacing=chapters[i]['pacing'],
                    to_pacing=chapters[i+1]['pacing']
                )
            })

    return {
        'total_chapters': total,
        'pacing_distribution': dict(pacing_dist),
        'ratios': ratios,
        'chapters': chapters,
        'issues': issues,
        'suggestions': suggestions,
        'issue_count': len(issues),
        'suggestion_count': len(suggestions)
    }


def main():
    parser = argparse.ArgumentParser(description='节奏优化建议脚本')
    parser.add_argument('chapters_dir', help='章节目录路径')
    parser.add_argument('--recent', type=int, help='仅分析最近N章')
    parser.add_argument('--json', action='store_true', help='JSON输出')
    args = parser.parse_args()

    if not os.path.isdir(args.chapters_dir):
        print(f"错误: 目录不存在: {args.chapters_dir}", file=sys.stderr)
        sys.exit(1)

    result = analyze_pacing_with_suggestions(args.chapters_dir, args.recent)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if 'error' in result:
            print(result['error'])
            return

        print(f"\n=== 节奏优化建议 (最近{result['total_chapters']}章) ===\n")

        print("节奏分布:")
        dist = result['pacing_distribution']
        for label in ['S5', 'S4', 'S3', 'S2', 'S1']:
            count = dist.get(label, 0)
            ratio = result['ratios'].get(label, 0)
            bar = "█" * count
            print(f"  {label}: {bar} ({count}章, {ratio}%)")

        print(f"\n问题数: {result['issue_count']}")
        print(f"建议数: {result['suggestion_count']}")

        if result['suggestions']:
            print(f"\n优化建议:")
            for i, suggestion in enumerate(result['suggestions'], 1):
                print(f"\n  {i}. [{suggestion['type']}]")
                print(f"     {suggestion['detail']}")
                print(f"     示例: {suggestion['example']}")
        else:
            print(f"\n✓ 节奏良好，无需优化")


if __name__ == '__main__':
    main()
