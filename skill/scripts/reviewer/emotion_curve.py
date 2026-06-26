#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
情绪曲线分析脚本
分析章节或整卷的情绪变化曲线，检测情绪波动是否合理。
供复盘师在卷末复盘时使用，或审计师在审查情绪节奏时参考。

用法:
    python scripts/reviewer/emotion_curve.py 章节文件 --json
    python scripts/reviewer/emotion_curve.py 章节目录 --volume --json
    python scripts/reviewer/emotion_curve.py 章节目录 --recent 10
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

# ─── 情绪分类 ───────────────────────────────
EMOTION_CATEGORIES = {
    'positive': {
        'name': '积极',
        'keywords': ['开心', '快乐', '喜悦', '兴奋', '激动', '幸福', '满足', '欣慰', '自豪', '感动',
                     '爱', '喜欢', '温暖', '希望', '期待', '惊喜', '欣慰', '释然', '轻松', '愉快']
    },
    'negative': {
        'name': '消极',
        'keywords': ['悲伤', '难过', '痛苦', '绝望', '愤怒', '恐惧', '焦虑', '担忧', '失望', '沮丧',
                     '恨', '厌恶', '嫉妒', '后悔', '自责', '内疚', '羞愧', '孤独', '无助', '迷茫']
    },
    'neutral': {
        'name': '中性',
        'keywords': ['平静', '淡然', '从容', '淡定', '思考', '观察', '分析', '计划', '准备', '等待']
    },
    'tense': {
        'name': '紧张',
        'keywords': ['紧张', '危急', '危险', '紧迫', '焦虑', '不安', '忐忑', '慌张', '急促', '激烈']
    }
}


def analyze_emotion_in_text(text):
    """Analyze emotion distribution in text."""
    emotion_scores = defaultdict(int)

    for category, config in EMOTION_CATEGORIES.items():
        for keyword in config['keywords']:
            count = text.count(keyword)
            if count > 0:
                emotion_scores[category] += count

    total = sum(emotion_scores.values())
    if total == 0:
        return {'dominant': 'neutral', 'scores': {k: 0 for k in EMOTION_CATEGORIES}, 'total': 0}

    # Calculate percentages
    percentages = {k: round(v / total * 100, 1) for k, v in emotion_scores.items()}

    # Find dominant emotion
    dominant = max(emotion_scores, key=emotion_scores.get)

    return {
        'dominant': dominant,
        'dominant_name': EMOTION_CATEGORIES[dominant]['name'],
        'scores': dict(emotion_scores),
        'percentages': percentages,
        'total': total
    }


def analyze_chapter_emotion(filepath):
    """Analyze emotion in a single chapter."""
    raw, title, clean, wc = read_chapter(filepath)

    # Analyze different parts
    head = clean[:1000] if len(clean) > 1000 else clean
    middle = clean[len(clean)//3:2*len(clean)//3] if len(clean) > 3000 else clean
    tail = clean[-1000:] if len(clean) > 1000 else clean

    head_emotion = analyze_emotion_in_text(head)
    middle_emotion = analyze_emotion_in_text(middle)
    tail_emotion = analyze_emotion_in_text(tail)
    full_emotion = analyze_emotion_in_text(clean)

    return {
        'chapter': title,
        'word_count': wc,
        'full': full_emotion,
        'structure': {
            'head': head_emotion,
            'middle': middle_emotion,
            'tail': tail_emotion
        }
    }


def build_emotion_curve(chapters_dir, recent_n=None):
    """Build emotion curve across multiple chapters."""
    chapter_files = list_chapters(chapters_dir, recent_n)
    if not chapter_files:
        return {'error': '未找到章节文件'}

    curve = []
    for idx, cf in enumerate(chapter_files):
        ch_data = analyze_chapter_emotion(cf)
        curve.append({
            'chapter_num': idx + 1,
            'chapter_title': ch_data['chapter'],
            'dominant_emotion': ch_data['full']['dominant_name'],
            'emotion_scores': ch_data['full']['scores'],
            'word_count': ch_data['word_count']
        })

    # Analyze curve patterns
    emotions_sequence = [c['dominant_emotion'] for c in curve]

    # Detect monotony (same emotion for too long)
    monotony_issues = []
    current_emotion = emotions_sequence[0] if emotions_sequence else None
    streak_start = 0
    for i, emo in enumerate(emotions_sequence):
        if emo != current_emotion:
            streak_length = i - streak_start
            if streak_length >= 3:
                monotony_issues.append({
                    'emotion': current_emotion,
                    'chapters': f"第{streak_start+1}-{i}章",
                    'length': streak_length
                })
            current_emotion = emo
            streak_start = i

    # Check final streak
    if len(emotions_sequence) - streak_start >= 3:
        monotony_issues.append({
            'emotion': current_emotion,
            'chapters': f"第{streak_start+1}-{len(emotions_sequence)}章",
            'length': len(emotions_sequence) - streak_start
        })

    # Emotion transition analysis
    transitions = []
    for i in range(len(emotions_sequence) - 1):
        transitions.append({
            'from': emotions_sequence[i],
            'to': emotions_sequence[i+1],
            'chapter': i + 1
        })

    return {
        'total_chapters': len(curve),
        'curve': curve,
        'emotions_sequence': emotions_sequence,
        'monotony_issues': monotony_issues,
        'transitions': transitions,
        'summary': {
            'emotion_distribution': defaultdict(int),
            'most_common': max(set(emotions_sequence), key=emotions_sequence.count) if emotions_sequence else 'N/A'
        }
    }


def main():
    parser = argparse.ArgumentParser(description='情绪曲线分析脚本')
    parser.add_argument('path', help='章节文件或章节目录路径')
    parser.add_argument('--volume', '-v', action='store_true', help='分析整卷（目录模式）')
    parser.add_argument('--recent', type=int, help='仅分析最近N章')
    parser.add_argument('--json', action='store_true', help='JSON输出')
    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"错误: 路径不存在: {args.path}", file=sys.stderr)
        sys.exit(1)

    if args.volume or os.path.isdir(args.path):
        result = build_emotion_curve(args.path, args.recent)
    else:
        result = analyze_chapter_emotion(args.path)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if 'error' in result:
            print(result['error'])
            return

        if 'curve' in result:
            # Volume mode
            print(f"\n=== 情绪曲线分析 (最近{result['total_chapters']}章) ===\n")

            print("情绪序列:")
            print("  " + " → ".join(result['emotions_sequence']))

            if result['monotony_issues']:
                print(f"\n单调性问题:")
                for issue in result['monotony_issues']:
                    print(f"  ⚠ {issue['chapters']}: 连续{issue['length']}章{issue['emotion']}")
            else:
                print(f"\n✓ 情绪变化丰富，无明显单调问题")

            print(f"\n情绪分布:")
            dist = result['summary']['emotion_distribution']
            for emo in result['emotions_sequence']:
                dist[emo] += 1
            for emo, count in sorted(dist.items(), key=lambda x: -x[1]):
                bar = "█" * count
                print(f"  {emo}: {bar} ({count}章)")

            print(f"\n最常见情绪: {result['summary']['most_common']}")
        else:
            # Single chapter mode
            print(f"\n=== 情绪分析: {result['chapter']} ===\n")
            print(f"字数: {result['word_count']}")
            print(f"主导情绪: {result['full']['dominant_name']}")

            print(f"\n情绪得分:")
            for cat, score in result['full']['scores'].items():
                name = EMOTION_CATEGORIES[cat]['name']
                pct = result['full']['percentages'].get(cat, 0)
                bar = "█" * max(1, score // 2)
                print(f"  {name}: {bar} ({score}次, {pct}%)")

            print(f"\n章节结构情绪:")
            for part, data in result['structure'].items():
                part_name = {'head': '开头', 'middle': '中间', 'tail': '结尾'}[part]
                print(f"  {part_name}: {data['dominant_name']}")


if __name__ == '__main__':
    main()
