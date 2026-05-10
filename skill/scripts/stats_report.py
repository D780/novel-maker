#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目统计报告
快速扫描 novels/ 和 .novel-weaver/ 目录，输出完整的写作进度统计。
供 `/novel-weaver stats` 指令使用。
"""

import os
import sys
import json
from collections import Counter

from nw_utils import (
    list_chapters, read_chapter, count_chinese,
    extract_characters, extract_locations, estimate_pacing
)


def scan_volume(volume_path):
    """Scan a single volume directory."""
    vol_name = os.path.basename(volume_path)
    chapters_dir = os.path.join(volume_path, 'chapters')
    if not os.path.isdir(chapters_dir):
        return None

    chapter_files = list_chapters(chapters_dir)
    if not chapter_files:
        return None

    chapters = []
    all_chars = Counter()
    all_locs = Counter()
    pacing_dist = Counter()
    total_words = 0

    for idx, filepath in enumerate(chapter_files):
        raw, title, clean, wc = read_chapter(filepath)
        pacing_label, _ = estimate_pacing(raw)
        chars = extract_characters(clean)
        locs = extract_locations(clean)

        chapters.append({
            'num': idx + 1,
            'title': title,
            'words': wc,
            'pacing': pacing_label,
            'characters': chars[:4],
        })

        total_words += wc
        for c in chars:
            all_chars[c] += 1
        for loc in locs:
            all_locs[loc] += 1
        pacing_dist[pacing_label] += 1

    return {
        'name': vol_name,
        'total_chapters': len(chapters),
        'total_words': total_words,
        'avg_words': round(total_words / max(len(chapters), 1), 0),
        'chapters': chapters,
        'main_characters': [name for name, _ in all_chars.most_common(8)],
        'character_appearances': dict(all_chars.most_common(10)),
        'main_locations': [loc for loc, _ in all_locs.most_common(5)],
        'pacing_distribution': dict(pacing_dist),
    }


def scan_project(novels_dir):
    """Scan the entire novels directory."""
    if not os.path.isdir(novels_dir):
        return {'error': f'目录不存在: {novels_dir}'}

    # Check for outline
    outline_path = os.path.join(novels_dir, 'outline.md')
    has_outline = os.path.exists(outline_path)
    outline_word_count = 0
    if has_outline:
        with open(outline_path, 'r', encoding='utf-8') as f:
            outline_word_count = count_chinese(f.read())

    # Scan volumes
    volumes = []
    for entry in sorted(os.listdir(novels_dir)):
        vol_path = os.path.join(novels_dir, entry)
        if os.path.isdir(vol_path) and entry.startswith('volume'):
            result = scan_volume(vol_path)
            if result:
                volumes.append(result)

    # Aggregate stats
    total_chapters = sum(v['total_chapters'] for v in volumes)
    total_words = sum(v['total_words'] for v in volumes)

    return {
        'has_outline': has_outline,
        'outline_words': outline_word_count,
        'volumes': len(volumes),
        'total_chapters': total_chapters,
        'total_words': total_words,
        'volume_details': volumes,
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Project stats report")
    parser.add_argument("novels_dir", nargs='?', default='novels', help="Novels directory")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--volume", type=str, help="Show only specific volume")
    args = parser.parse_args()

    novels_dir = args.novels_dir
    if not os.path.isdir(novels_dir):
        # Try to find novels dir
        base = os.path.dirname(os.path.abspath(novels_dir))
        alt = os.path.join(base, 'novels')
        if os.path.isdir(alt):
            novels_dir = alt
        else:
            print(f"错误: 目录不存在 - {novels_dir}", file=sys.stderr)
            sys.exit(1)

    result = scan_project(novels_dir)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if 'error' in result:
        print(result['error'])
        return

    print(f"\n{'=' * 60}")
    print(f"📚 NovelWeaver 项目统计")
    print(f"{'=' * 60}")
    print(f"大纲: {'✅ 已生成' if result['has_outline'] else '❌ 未生成'} ({result['outline_words']}字)")
    print(f"卷数: {result['volumes']}")
    print(f"总章节: {result['total_chapters']}")
    print(f"总字数: {result['total_words']:,}")
    print()

    for vol in result['volume_details']:
        if args.volume and vol['name'] != args.volume:
            continue
        print(f"  📖 {vol['name']}")
        print(f"     章节: {vol['total_chapters']} 章 | 字数: {vol['total_words']:,} | 平均: {vol['avg_words']}字/章")
        print(f"     主要角色: {', '.join(vol['main_characters'][:5])}")
        print(f"     主要场景: {', '.join(vol['main_locations'][:3])}")
        pacing = vol['pacing_distribution']
        pacing_str = ' | '.join(f"{k}:{v}章" for k, v in sorted(pacing.items()))
        print(f"     节奏分布: {pacing_str}")

        if args.volume == vol['name']:
            print(f"\n     章节明细:")
            for ch in vol['chapters']:
                print(f"       第{ch['num']}章: {ch['title']} ({ch['words']}字, {ch['pacing']})")
        print()


if __name__ == "__main__":
    main()
