#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
卷级节奏报告
分析卷内所有章节的节奏分布、问题区域、追读力趋势。
供 `/novel-maker review pacing volume` 使用。
"""

import os
import sys
import json
from collections import Counter

from nw_utils import (
    list_chapters, read_chapter, estimate_pacing, detect_hook_type_from_patterns
)

PACING_NAMES = {
    'S5': '极高潮', 'S4': '高潮', 'S3': '上升', 'S2': '平缓', 'S1': '低谷'
}

# 节奏规则
MAX_CONSECUTIVE_HIGH = 3  # 不能连续3章S4+
MAX_CONSECUTIVE_LOW = 3   # 不能连续3章S2-
MAX_NO_PEAK_INTERVAL = 8  # 每8章必须有S4/S5
MAX_NO_MID_INTERVAL = 3   # 每3章必须有S3+


def analyze_pacing_volume(chapters_dir, recent_n=None):
    chapter_files = list_chapters(chapters_dir, recent_n)
    if not chapter_files:
        return {'error': 'No chapters found'}

    chapters = []
    pacing_sequence = []

    for idx, filepath in enumerate(chapter_files):
        raw, title, clean, wc = read_chapter(filepath)
        pacing_label, pacing_num = estimate_pacing(raw)
        hook_type = detect_hook_type_from_patterns(raw[-500:] if len(raw) > 500 else raw)

        chapters.append({
            'num': idx + 1,
            'title': title,
            'words': wc,
            'pacing': pacing_label,
            'pacing_num': pacing_num,
            'hook_type': hook_type,
        })
        pacing_sequence.append(pacing_num)

    # 节奏分布统计
    pacing_dist = Counter(c['pacing'] for c in chapters)
    total = len(chapters)

    # 问题区域检测
    problems = []

    # 连续高潮检测
    run_start = 0
    for i in range(1, len(pacing_sequence)):
        if pacing_sequence[i] >= 4 and pacing_sequence[i-1] >= 4:
            if i - run_start >= MAX_CONSECUTIVE_HIGH - 1:
                problems.append({
                    'type': 'consecutive_high',
                    'chapters': f"第{run_start+1}-{i+1}章",
                    'severity': 'warning',
                    'message': f"连续{i-run_start+1}章S4/S5高潮，读者可能疲劳"
                })
        else:
            run_start = i

    # 连续平淡检测
    run_start = 0
    for i in range(1, len(pacing_sequence)):
        if pacing_sequence[i] <= 2 and pacing_sequence[i-1] <= 2:
            if i - run_start >= MAX_CONSECUTIVE_LOW - 1:
                problems.append({
                    'type': 'consecutive_low',
                    'chapters': f"第{run_start+1}-{i+1}章",
                    'severity': 'warning',
                    'message': f"连续{i-run_start+1}章S1/S2平淡，读者可能弃读"
                })
        else:
            run_start = i

    # 峰值间隔检测
    last_peak = -1
    for i, p in enumerate(pacing_sequence):
        if p >= 4:
            if last_peak >= 0 and (i - last_peak) > MAX_NO_PEAK_INTERVAL:
                problems.append({
                    'type': 'peak_gap',
                    'chapters': f"第{last_peak+2}-{i}章",
                    'severity': 'warning',
                    'message': f"超过{MAX_NO_PEAK_INTERVAL}章无S4/S5高潮"
                })
            last_peak = i

    # 追读力趋势评估（每5章一组）
    read_trends = []
    for start in range(0, total, 5):
        end = min(start + 5, total)
        chunk = chapters[start:end]
        avg_pacing = sum(c['pacing_num'] for c in chunk) / len(chunk)
        high_count = sum(1 for c in chunk if c['pacing_num'] >= 4)
        if avg_pacing >= 3.5:
            rating = '★★★★★'
        elif avg_pacing >= 3.0:
            rating = '★★★★☆'
        elif avg_pacing >= 2.5:
            rating = '★★★☆☆'
        elif avg_pacing >= 2.0:
            rating = '★★☆☆☆'
        else:
            rating = '★☆☆☆☆'
        read_trends.append({
            'range': f"第{start+1}-{end}章",
            'rating': rating,
            'avg_pacing': round(avg_pacing, 1),
            'peak_count': high_count,
        })

    # 钩子类型分布
    hook_dist = Counter(c['hook_type'] for c in chapters)

    # 后续建议
    suggestions = []
    if pacing_sequence[-3:] == [4, 4, 4] or pacing_sequence[-3:] == [5, 4, 5]:
        suggestions.append("下一章安排日常缓冲（S2）")
    if pacing_sequence[-3:] == [1, 1, 2] or pacing_sequence[-3:] == [2, 1, 1]:
        suggestions.append("下一章安排冲突/高潮（S3+）")
    if hook_dist.get('悬念', 0) + hook_dist.get('未知', 0) > total * 0.4:
        suggestions.append("钩子类型过于单一，建议丰富悬念类型")

    return {
        'total_chapters': total,
        'pacing_distribution': dict(pacing_dist),
        'chapters': chapters,
        'problems': problems,
        'read_trends': read_trends,
        'hook_distribution': dict(hook_dist),
        'suggestions': suggestions,
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Volume pacing report")
    parser.add_argument("chapters_dir", help="Chapters directory")
    parser.add_argument("--recent", type=int, help="Only analyze last N chapters")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    if not os.path.isdir(args.chapters_dir):
        print(f"Error: {args.chapters_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    result = analyze_pacing_volume(args.chapters_dir, recent_n=args.recent)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if 'error' in result:
        print(result['error'])
        return

    print(f"\n{'=' * 60}")
    print(f"📊 节奏报告 (最近{result['total_chapters']}章)")
    print(f"{'=' * 60}\n")

    print("节奏分布:")
    dist = result['pacing_distribution']
    total = result['total_chapters']
    for label in ['S5', 'S4', 'S3', 'S2', 'S1']:
        count = dist.get(label, 0)
        pct = round(count / max(total, 1) * 100, 0)
        bar = "█" * count
        name = PACING_NAMES.get(label, label)
        print(f"  {label}({name:4s}): {bar} ({count}章, {pct}%)")

    print(f"\n问题区域:")
    if result['problems']:
        for p in result['problems']:
            print(f"  ⚠ {p['chapters']}: {p['message']}")
    else:
        print("  ✅ 无明显问题")

    print(f"\n追读力趋势:")
    for t in result['read_trends']:
        print(f"  {t['range']}: {t['rating']} (平均节奏 {t['avg_pacing']}, 高潮{t['peak_count']}次)")

    print(f"\n钩子分布:")
    for h, c in sorted(result['hook_distribution'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {h}: {c}次")

    if result['suggestions']:
        print(f"\n改进建议:")
        for s in result['suggestions']:
            print(f"  → {s}")

    print(f"\n章节节奏明细:")
    for ch in result['chapters']:
        print(f"  第{ch['num']}章: {ch['title']} ({ch['pacing']}, {ch['words']}字)")


if __name__ == "__main__":
    main()
