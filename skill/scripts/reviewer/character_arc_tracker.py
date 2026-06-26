#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
角色弧线追踪脚本
追踪角色在整卷中的成长轨迹、情感变化、能力演进。
供复盘师在卷末复盘时使用，或规划师在规划角色发展时参考。

用法:
    python scripts/reviewer/character_arc_tracker.py 章节目录 --chars 林风,苏婉 --json
    python scripts/reviewer/character_arc_tracker.py 章节目录 --all --json
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'common'))
from nm_utils import (
    list_chapters, read_chapter, extract_characters, count_chinese,
    chapter_sort_key
)

# ─── 角色情感关键词 ───────────────────────────────
EMOTION_KEYWORDS = {
    '愤怒': ['愤怒', '怒火', '暴怒', ' rage', '大怒', '恼怒', '愤然'],
    '悲伤': ['悲伤', '难过', '伤心', '落泪', '哭泣', '哀伤', '悲痛'],
    '喜悦': ['喜悦', '开心', '高兴', '欢笑', '欣喜', '愉悦', '快乐'],
    '恐惧': ['恐惧', '害怕', '惊恐', '畏惧', '胆怯', '惶恐', '不安'],
    '平静': ['平静', '淡然', '从容', '淡定', '安详', '宁静', '平和'],
    '紧张': ['紧张', '焦虑', '忐忑', '不安', '慌张', '焦急', '紧迫'],
}

# ─── 角色能力关键词 ───────────────────────────────
ABILITY_KEYWORDS = {
    '突破': ['突破', '晋升', '进阶', '升级', '领悟', '顿悟'],
    '战斗': ['战斗', '对决', '厮杀', '交锋', '激战', '搏杀'],
    '修炼': ['修炼', '修炼', '打坐', '运功', '吐纳', '冥想'],
    '失败': ['失败', '受伤', '败北', '溃败', '落败', '受挫'],
}


def track_character_in_chapter(filepath, target_chars=None):
    """Track character mentions and context in a single chapter."""
    raw, title, clean, wc = read_chapter(filepath)
    all_chars = extract_characters(clean)

    # Filter to target characters if specified
    if target_chars:
        chars = [c for c in all_chars if c in target_chars]
    else:
        chars = all_chars

    char_data = {}
    for char in chars:
        # Find all paragraphs mentioning this character
        paragraphs = [p for p in clean.split('\n') if p.strip() and char in p]
        char_text = ' '.join(paragraphs)

        # Emotion analysis
        emotions = {}
        for emotion, keywords in EMOTION_KEYWORDS.items():
            count = sum(char_text.count(kw) for kw in keywords)
            if count > 0:
                emotions[emotion] = count

        # Ability analysis
        abilities = {}
        for ability, keywords in ABILITY_KEYWORDS.items():
            count = sum(char_text.count(kw) for kw in keywords)
            if count > 0:
                abilities[ability] = count

        char_data[char] = {
            'mention_count': len(paragraphs),
            'emotions': emotions,
            'abilities': abilities,
            'word_count': count_chinese(char_text)
        }

    return {
        'chapter': title,
        'word_count': wc,
        'characters': char_data
    }


def build_character_arc(chapters_dir, target_chars=None, recent_n=None):
    """Build character arc across multiple chapters."""
    chapter_files = list_chapters(chapters_dir, recent_n)
    if not chapter_files:
        return {'error': '未找到章节文件'}

    arc = {}
    for idx, cf in enumerate(chapter_files):
        ch_data = track_character_in_chapter(cf, target_chars)
        ch_num = idx + 1

        for char, data in ch_data['characters'].items():
            if char not in arc:
                arc[char] = []
            arc[char].append({
                'chapter_num': ch_num,
                'chapter_title': ch_data['chapter'],
                'mention_count': data['mention_count'],
                'emotions': data['emotions'],
                'abilities': data['abilities'],
                'word_count': data['word_count']
            })

    # Generate summary for each character
    summary = {}
    for char, entries in arc.items():
        total_mentions = sum(e['mention_count'] for e in entries)
        all_emotions = defaultdict(int)
        all_abilities = defaultdict(int)
        for e in entries:
            for emo, cnt in e['emotions'].items():
                all_emotions[emo] += cnt
            for abi, cnt in e['abilities'].items():
                all_abilities[abi] += cnt

        # Dominant emotion
        dominant_emo = max(all_emotions, key=all_emotions.get) if all_emotions else '未检测'
        # Most frequent ability
        dominant_abi = max(all_abilities, key=all_abilities.get) if all_abilities else '未检测'

        summary[char] = {
            'total_chapters': len(entries),
            'total_mentions': total_mentions,
            'avg_mentions_per_chapter': round(total_mentions / max(len(entries), 1), 1),
            'dominant_emotion': dominant_emo,
            'emotion_distribution': dict(all_emotions),
            'dominant_ability': dominant_abi,
            'ability_distribution': dict(all_abilities),
            'arc_points': entries
        }

    return {
        'total_chapters_analyzed': len(chapter_files),
        'characters_tracked': len(arc),
        'summary': summary
    }


def main():
    parser = argparse.ArgumentParser(description='角色弧线追踪脚本')
    parser.add_argument('chapters_dir', help='章节目录路径')
    parser.add_argument('--chars', '-c', help='目标角色，逗号分隔')
    parser.add_argument('--all', '-a', action='store_true', help='追踪所有角色')
    parser.add_argument('--recent', type=int, help='仅分析最近N章')
    parser.add_argument('--json', action='store_true', help='JSON输出')
    args = parser.parse_args()

    if not os.path.isdir(args.chapters_dir):
        print(f"错误: 目录不存在: {args.chapters_dir}", file=sys.stderr)
        sys.exit(1)

    target_chars = args.chars.split(',') if args.chars else None
    result = build_character_arc(args.chapters_dir, target_chars, args.recent)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if 'error' in result:
            print(result['error'])
            return

        print(f"\n=== 角色弧线追踪 ===\n")
        print(f"分析章节数: {result['total_chapters_analyzed']}")
        print(f"追踪角色数: {result['characters_tracked']}")

        for char, summary in result['summary'].items():
            print(f"\n--- {char} ---")
            print(f"  出场章数: {summary['total_chapters']}")
            print(f"  总提及次数: {summary['total_mentions']}")
            print(f"  平均每章: {summary['avg_mentions_per_chapter']}次")
            print(f"  主导情绪: {summary['dominant_emotion']}")
            if summary['emotion_distribution']:
                emos = ', '.join(f"{k}({v})" for k, v in sorted(summary['emotion_distribution'].items(), key=lambda x: -x[1])[:5])
                print(f"  情绪分布: {emos}")
            print(f"  主导能力: {summary['dominant_ability']}")
            if summary['ability_distribution']:
                abis = ', '.join(f"{k}({v})" for k, v in sorted(summary['ability_distribution'].items(), key=lambda x: -x[1])[:5])
                print(f"  能力分布: {abis}")


if __name__ == '__main__':
    main()
