#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一章节分析脚本 - 整合 chapter_info/style_check/hook_report 功能

支持三种模式:
  - single: 单章分析(代替 chapter_info.py)
  - style: AI味检测(代替 style_check.py)  
  - batch: 批量汇总(代替 hook_report.py + 卷级分析)

输出格式统一,支持 --json/table/text 三种格式。
"""

import sys
import os
import json
import re
import argparse
from collections import Counter

from nw_utils import (
    clean_markdown, count_chinese, extract_title, read_chapter,
    extract_characters, extract_locations, detect_structure,
    detect_hook, detect_hook_type_from_patterns, generate_summary,
    estimate_pacing, list_chapters
)

# ─── AI味检测 ───────────────────────────────
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


def analyze_single_chapter(filepath):
    """单章结构化分析 - 代替 chapter_info.py"""
    raw, title, clean, wc = read_chapter(filepath)
    pacing_level, pacing_score = estimate_pacing(raw)
    
    return {
        'file': os.path.basename(filepath),
        'title': title,
        'word_count': wc,
        'pacing_level': pacing_level,
        'pacing_score': pacing_score,
        'characters': extract_characters(clean)[:10],  # 限制Top-10,减少噪音
        'locations': extract_locations(clean)[:8],
        'structure': detect_structure(raw),
        'hook': detect_hook(raw),
        'hook_type': detect_hook_type_from_patterns(raw[-400:]),
        'summary': generate_summary(raw)
    }


def analyze_style(text, filepath=''):
    """AI味检测分析 - 代替 style_check.py"""
    word_count = count_chinese(text)
    if word_count == 0:
        return None

    title = extract_title(text) or os.path.basename(filepath)
    issues = []

    # 检测AI套话模式
    for pattern_name, pattern in AI_PATTERNS.items():
        matches = pattern.findall(text)
        if matches:
            issues.append({
                "type": "ai_pattern",
                "pattern": pattern_name,
                "count": len(matches),
                "examples": [m[:30] for m in matches[:2]]
            })

    # 检测重复词汇
    word_freq = Counter(re.findall(r'[\u4e00-\u9fff]{2}', text))
    top_words = word_freq.most_common(15)
    repetitive = [(w, c) for w, c in top_words if c > 5 and w not in ('我们', '你们', '他们', '自己', '什么')]
    for w, c in repetitive:
        issues.append({"type": "repetitive_word", "word": w, "count": c})

    # AI词密度计算
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

    # 对话比例
    paragraphs = [p.strip() for p in text.split('\n') if p.strip() and not p.strip().startswith('#')]
    dialogue_lines = sum(1 for p in paragraphs if re.match(r'^["\u201c]', p))
    dialogue_ratio = dialogue_lines / max(len(paragraphs), 1) * 100

    # 平均句长
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


def analyze_batch(chapters_dir, recent_n=None):
    """批量卷级分析 - 整合 hook_report + 基础统计"""
    chapter_files = list_chapters(chapters_dir, recent_n)
    if not chapter_files:
        return {'error': f'在 {chapters_dir} 中未找到章节'}

    results = []
    total_words = 0
    hook_types = []
    pacing_levels = []

    for idx, filepath in enumerate(chapter_files):
        raw, title, clean, wc = read_chapter(filepath)
        ending = raw[-400:] if len(raw) > 400 else raw
        hook_type = detect_hook_type_from_patterns(ending)
        pacing_level, _ = estimate_pacing(raw)
        
        total_words += wc
        hook_types.append(hook_type)
        pacing_levels.append(pacing_level)

        # 提取钩子句子
        hook_sentences = []
        for m in re.finditer(r'[^。！？\n]{5,50}[。！？]', raw[-600:] if len(raw) > 600 else raw):
            sentence = m.group(0)
            from nw_utils import _HOOK_PATTERN_MAP
            if any(pattern.search(sentence) for pattern in _HOOK_PATTERN_MAP.values()):
                hook_sentences.append(sentence.strip())

        results.append({
            "chapter": idx + 1,
            "title": title,
            "word_count": wc,
            "hook_type": hook_type,
            "pacing_level": pacing_level,
            "hook_sentences": hook_sentences[:3],
            "ending_preview": raw[-150:] if len(raw) > 150 else raw,
        })

    # 统计分析
    hook_dist = dict(Counter(hook_types))
    pacing_dist = dict(Counter(pacing_levels))

    # 连续相同钩子检测
    consecutive_same = []
    if len(hook_types) >= 3:
        for i in range(len(hook_types) - 2):
            if hook_types[i] == hook_types[i+1] == hook_types[i+2]:
                consecutive_same.append(f"第{results[i]['chapter']}-{results[i+2]['chapter']}章连续使用「{hook_types[i]}」钩子")

    # 连续高潮/平淡检测
    pacing_warnings = []
    if len(pacing_levels) >= 3:
        high_keywords = ['S4', 'S5']
        low_keywords = ['S1', 'S2']
        for i in range(len(pacing_levels) - 2):
            chunk = pacing_levels[i:i+3]
            if all(p in high_keywords for p in chunk):
                pacing_warnings.append(f"第{results[i]['chapter']}-{results[i+2]['chapter']}连续高潮,可能读者疲劳")
            if all(p in low_keywords for p in chunk):
                pacing_warnings.append(f"第{results[i]['chapter']}-{results[i+2]['chapter']}连续平淡,可能读者弃读")

    return {
        "total_chapters": len(results),
        "total_words": total_words,
        "avg_words_per_chapter": round(total_words / max(len(results), 1)),
        "hook_distribution": hook_dist,
        "pacing_distribution": pacing_dist,
        "chapters": results,
        "warnings": {
            "consecutive_same_hook": consecutive_same,
            "pacing_issues": pacing_warnings,
            "unknown_hooks": sum(1 for h in hook_types if h == "未知"),
        }
    }


def format_output(data, fmt='json'):
    """统一输出格式"""
    if fmt == 'json':
        print(json.dumps(data, ensure_ascii=False, indent=2))
    elif fmt == 'table':
        _print_table(data)
    else:
        _print_text(data)


def _print_table(data):
    """表格格式输出"""
    if 'chapters' in data:
        # 批量模式
        print(f"\n{'章序':<6} {'标题':<20} {'字数':<8} {'钩子':<8} {'节奏':<6}")
        print("-" * 50)
        for ch in data['chapters']:
            print(f"第{ch['chapter']:<4}章 {ch['title'] or '未知':<20} {ch['word_count']:<8} {ch['hook_type']:<8} {ch['pacing_level']:<6}")
        print(f"\n总计: {data['total_chapters']}章 / {data['total_words']}字")
    elif 'word_count' in data:
        # 单章模式
        print(f"章节: {data.get('title', '未知')}")
        print(f"字数: {data['word_count']}")
        print(f"节奏: {data.get('pacing_level', 'N/A')}")
        print(f"角色: {', '.join(data.get('characters', [])[:6]) or '未检测到'}")
        print(f"钩子: {data.get('hook_type', '未知')}")
    elif 'ai_density_per_1000' in data:
        # 风格检测模式
        print(f"章节: {data.get('title', '未知')} ({data['word_count']}字)")
        print(f"AI词密度: {data['ai_density_per_1000']}/千字")
        print(f"对话占比: {data['dialogue_ratio_pct']}%")
        if data.get('issues'):
            print("\n问题:")
            for issue in data['issues']:
                print(f"  ⚠ {issue.get('pattern', issue.get('type', '未知'))}")


def _print_text(data):
    """文本格式输出(供AI读取)"""
    if 'chapters' in data:
        parts = []
        parts.append(f"卷统计: {data['total_chapters']}章 / {data['total_words']}字 / 均章{data.get('avg_words_per_chapter', 0)}字")
        parts.append(f"节奏分布: {data.get('pacing_distribution', {})}")
        parts.append(f"钩子分布: {data.get('hook_distribution', {})}")
        if data.get('warnings', {}).get('pacing_issues'):
            parts.append(f"节奏警告: {data['warnings']['pacing_issues']}")
        print('\n'.join(parts))
    elif 'word_count' in data:
        parts = [
            f"章节: {data.get('title', '未知')}",
            f"字数: {data['word_count']}",
            f"节奏: {data.get('pacing_level', 'N/A')}",
            f"角色: {', '.join(data.get('characters', [])[:5]) or '无'}",
            f"地点: {', '.join(data.get('locations', [])[:3]) or '无'}",
            f"钩子: {data.get('hook_type', '未知')}",
        ]
        print('\n'.join(parts))


def main():
    parser = argparse.ArgumentParser(description="NovelWeaver 统一分析脚本")
    parser.add_argument("path", help="章节文件或章节目录路径")
    parser.add_argument("--mode", choices=['single', 'style', 'batch'], 
                       default='single', help="分析模式: single(单章)/style(风格)/batch(批量)")
    parser.add_argument("--json", action="store_true", help="输出JSON格式(供AI读取)")
    parser.add_argument("--format", choices=['json', 'table', 'text'],
                       default=None, help="输出格式: json/table/text(默认根据--json自动选择)")
    parser.add_argument("--recent", type=int, help="仅分析最近N章(批量模式)")
    args = parser.parse_args()

    path = args.path
    if not os.path.exists(path):
        error_data = {'error': f'路径不存在: {path}'}
        print(json.dumps(error_data, ensure_ascii=False))
        sys.exit(1)

    # 确定输出格式
    fmt = 'json' if args.json else (args.format or 'text')

    # 执行分析
    if args.mode == 'single':
        if os.path.isfile(path):
            result = analyze_single_chapter(path)
        else:
            result = {'error': '单章模式需要指定文件路径'}
    elif args.mode == 'style':
        if os.path.isfile(path):
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()
            result = analyze_style(text, path)
        else:
            # 目录模式:批量分析
            chapter_files = list_chapters(path, recent_n=args.recent)
            results = []
            for cf in chapter_files:
                with open(cf, 'r', encoding='utf-8') as f:
                    text = f.read()
                analysis = analyze_style(text, cf)
                if analysis:
                    results.append(analysis)
            result = results
    elif args.mode == 'batch':
        if os.path.isdir(path):
            result = analyze_batch(path, recent_n=args.recent)
        else:
            result = {'error': '批量模式需要指定目录路径'}

    # 输出结果
    format_output(result, fmt)


if __name__ == '__main__':
    main()
