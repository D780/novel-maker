#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI写作风格检测
检测 AI 高频词密度、连续"了/的"、句式重复、对话比例。
"""

import os
import sys
import json
import re
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'common'))
from nm_utils import list_chapters, extract_title, count_chinese


AI_FREQ_WORDS = [
    '苦涩', '复杂', '微妙', '难以言喻', '心中涌起', '内心深处',
    '五味杂陈', '百感交集', '缓缓', '默默', '轻轻',
    '深吸一口气', '苦笑一声', '皱了皱眉', '点了点头',
    '犹如', '宛若', '好似', '映入眼帘', '传入耳中',
    '不知何时', '不知不觉', '不禁', '不由得',
    '一丝', '一抹', '仿佛', '似乎',
]

AI_PATTERNS = {
    "连续'了'字": re.compile(r'了.{0,3}了.{0,3}了'),
    "连续'的'字": re.compile(r'的.{0,3}的.{0,3}的'),
    "不禁": re.compile(r'不禁[感到觉得想起]'),
    "不由得": re.compile(r'不由得[想起觉得]'),
    "仿佛一般": re.compile(r'仿佛.{1,10}一般'),
    "似乎样子": re.compile(r'似乎.{1,10}的样子'),
}


def analyze_chapter_style(text, filepath=''):
    """Analyze a single chapter for AI-like patterns."""
    word_count = count_chinese(text)
    if word_count == 0:
        return None

    title = extract_title(text) or os.path.basename(filepath)
    issues = []

    for pattern_name, pattern in AI_PATTERNS.items():
        matches = pattern.findall(text)
        if matches:
            issues.append({
                "type": "ai_pattern",
                "pattern": pattern_name,
                "count": len(matches),
                "examples": [m[:30] for m in matches[:2]]
            })

    word_freq = Counter(re.findall(r'[\u4e00-\u9fff]{2}', text))
    top_words = word_freq.most_common(15)
    repetitive = [(w, c) for w, c in top_words if c > 5 and w not in ('我们', '你们', '他们', '自己', '什么')]
    for w, c in repetitive:
        issues.append({
            "type": "repetitive_word",
            "word": w,
            "count": c
        })

    ai_word_count = 0
    ai_found_words = []
    for word in AI_FREQ_WORDS:
        count = len(re.findall(re.escape(word), text))
        if count > 0:
            ai_word_count += count
            ai_found_words.append({"word": word, "count": count})

    ai_density = ai_word_count / max(word_count / 1000, 1)
    if ai_density > 3:
        issues.append({
            "type": "ai_density",
            "ai_words_per_1000": round(ai_density, 1),
            "found_words": ai_found_words
        })

    paragraphs = [p.strip() for p in text.split('\n') if p.strip() and not p.strip().startswith('#')]
    dialogue_lines = sum(1 for p in paragraphs if re.match(r'^["\u201c]', p))
    dialogue_ratio = dialogue_lines / max(len(paragraphs), 1) * 100

    sentences = re.split(r'[。！？]', text)
    avg_sentence_len = sum(len(s) for s in sentences) / max(len(sentences), 1)

    return {
        "file": os.path.basename(filepath),
        "title": title,
        "word_count": word_count,
        "paragraphs": len(paragraphs),
        "dialogue_ratio_pct": round(dialogue_ratio, 1),
        "avg_sentence_length": round(avg_sentence_len, 1),
        "ai_density_per_1000": round(ai_density, 1),
        "ai_words_found": ai_found_words,
        "repetitive_words": [{"word": w, "count": c} for w, c in repetitive],
        "issues": issues,
        "top_words": [{"word": w, "count": c} for w, c in top_words[:8]],
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="AI style check")
    parser.add_argument("path", help="Chapter file or chapters directory")
    parser.add_argument("--all", action="store_true", help="Analyze all chapters in directory")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--recent", type=int, help="Only analyze last N chapters")
    args = parser.parse_args()

    path = args.path
    if not os.path.exists(path):
        print(f"Error: {path} does not exist", file=sys.stderr)
        sys.exit(1)

    if os.path.isdir(path) or args.all:
        if os.path.isfile(path):
            chapters_dir = os.path.dirname(path)
        else:
            chapters_dir = path
        chapter_files = list_chapters(chapters_dir, recent_n=args.recent)
    else:
        chapter_files = [path]

    results = []
    for cf in chapter_files:
        try:
            with open(cf, 'r', encoding='utf-8') as f:
                text = f.read()
            analysis = analyze_chapter_style(text, cf)
            if analysis:
                results.append(analysis)
        except Exception as e:
            if args.json:
                results.append({"file": os.path.basename(cf), "error": str(e)})

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for r in results:
            print(f"\n=== {r['title']} ({r['word_count']}字) ===")
            print(f"  对话占比: {r['dialogue_ratio_pct']}%  |  平均句长: {r['avg_sentence_length']}字  |  AI词密度: {r['ai_density_per_1000']}/千字")
            if r['issues']:
                for issue in r['issues']:
                    if issue['type'] == 'ai_pattern':
                        print(f"  ⚠ {issue['pattern']}: 出现{issue['count']}次")
                    elif issue['type'] == 'repetitive_word':
                        print(f"  ⚠ 重复词汇: 「{issue['word']}」出现{issue['count']}次")
                    elif issue['type'] == 'ai_density':
                        print(f"  ⚠ AI词密度过高: {issue['ai_words_per_1000']}/千字")
            else:
                print("  ✅ 无明显AI味")


if __name__ == "__main__":
    main()
