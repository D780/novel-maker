#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
卷级批量章节分析
批处理卷内所有（或最近N章），输出卷级汇总 JSON。
"""

import os
import sys
import json
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'common'))
from nm_utils import (
    list_chapters, read_chapter, extract_characters,
    extract_locations, detect_hook, detect_hook_type_from_patterns,
    count_chinese
)

FORESHADOWING_KEYWORDS = {
    '血脉': ['血脉', '祖先', '传承', '遗传', '血统'],
    '身世': ['身世', '出身', '来历', '母亲', '父亲'],
    '预言': ['预言', '命中注定', '天意', '卦象', '命格'],
    '阴谋': ['阴谋', '暗算', '布局', '棋局', '幕后'],
    '身份': ['身份', '真实身份', '秘密', '隐藏'],
    '仇敌': ['仇人', '仇敌', '恩怨', '血海深仇', '宿敌'],
}


def analyze_volume(chapters_dir, recent_n=None):
    chapter_files = list_chapters(chapters_dir, recent_n)
    if not chapter_files:
        return {'error': f'No chapters found in {chapters_dir}'}

    chapter_summaries = []
    all_characters = Counter()
    foreshadowing_counter = Counter()
    hook_type_counter = Counter()
    character_matrix = {}

    for idx, filepath in enumerate(chapter_files):
        raw, title, clean, wc = read_chapter(filepath)
        chars = extract_characters(clean)
        hook = detect_hook_type_from_patterns(raw)

        chapter_num = idx + 1
        chapter_summaries.append({
            'chapter': chapter_num,
            'title': title,
            'word_count': wc,
            'within_range': 2200 <= wc <= 2800,
            'characters': chars[:6],
            'hook_type': hook,
        })

        for c in chars:
            all_characters[c] += 1
        hook_type_counter[hook] += 1
        character_matrix[f'ch{chapter_num}'] = chars

        for keyword in clean:
            for ftype, keywords in FORESHADOWING_KEYWORDS.items():
                if any(kw in keyword for kw in keywords):
                    foreshadowing_counter[ftype] += 1
                    break

    main_characters = [name for name, _ in all_characters.most_common(8)]

    return {
        'total_chapters': len(chapter_files),
        'total_words': sum(s['word_count'] for s in chapter_summaries),
        'avg_words': round(sum(s['word_count'] for s in chapter_summaries) / max(len(chapter_summaries), 1), 0),
        'chapters': chapter_summaries,
        'main_characters': main_characters,
        'character_matrix': character_matrix,
        'foreshadowing_summary': dict(foreshadowing_counter),
        'hook_distribution': dict(hook_type_counter),
    }


def main():
    if len(sys.argv) < 2:
        print('用法: python volume_batch.py <卷章节目录路径> [--recent N] [--json]')
        return
    chapters_dir = sys.argv[1]
    if not os.path.isdir(chapters_dir):
        print(f'错误: 目录不存在 - {chapters_dir}')
        return
    recent_n = None
    json_only = False
    if '--recent' in sys.argv:
        idx = sys.argv.index('--recent')
        if idx + 1 < len(sys.argv):
            recent_n = int(sys.argv[idx + 1])
    json_only = '--json' in sys.argv

    result = analyze_volume(chapters_dir, recent_n)

    if json_only:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"=== 卷级批量分析 ===\n")
        if 'error' in result:
            print(result['error'])
            return
        print(f"总章节: {result['total_chapters']} 章")
        print(f"总字数: {result['total_words']} 字")
        print(f"平均每章: {result['avg_words']} 字\n")
        print(f"主要角色: {', '.join(result['main_characters'][:8])}\n")
        print(f"钩子类型分布:")
        for ht, count in sorted(result.get('hook_distribution', {}).items(), key=lambda x: x[1], reverse=True):
            bar = "█" * count
            print(f"  {ht}: {bar} ({count})")
        print(f"\n章节概览:")
        for ch in result['chapters']:
            status = "✓" if ch['within_range'] else "⚠"
            print(f"  {status} 第{ch['chapter']}章: {ch['title']} ({ch['word_count']}字, 角色: {', '.join(ch['characters'][:3])})")


if __name__ == '__main__':
    main()
