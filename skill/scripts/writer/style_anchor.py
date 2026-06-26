#!/usr/bin/env python3
"""
风格锚点提取脚本

从最近的章节中提取写作风格特征，生成 style-anchor.json

使用方式：
    python skill/scripts/style_anchor.py --chapters novels/volume-01/chapters/
    python skill/scripts/style_anchor.py --chapter novels/volume-01/chapters/ch01.md
"""

import argparse
import json
import re
from pathlib import Path
from collections import Counter


def extract_style_features(content: str) -> dict:
    """提取单个章节的风格特征"""
    lines = content.strip().split('\n')
    sentences = re.split(r'[。！？]', content)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # 对话行
    dialogue_lines = [l for l in lines if l.strip().startswith('"') or l.strip().startswith('\u201c')]
    
    # 非对话行
    narrative_lines = [l for l in lines if not (l.strip().startswith('"') or l.strip().startswith('\u201c'))]
    
    # 句子长度分布
    sentence_lengths = [len(s) for s in sentences]
    
    # 高频词（去除停用词）
    words = re.findall(r'[\u4e00-\u9fff]+', content)
    word_counter = Counter(words)
    
    # 标点频率
    punctuation = re.findall(r'[，。！？、；：""''（）]', content)
    punct_counter = Counter(punctuation)
    
    # 对话比例
    dialogue_chars = sum(len(l) for l in dialogue_lines)
    total_chars = len(content)
    dialogue_ratio = dialogue_chars / total_chars if total_chars > 0 else 0
    
    return {
        'sentence_count': len(sentences),
        'avg_sentence_length': round(sum(sentence_lengths) / len(sentence_lengths), 1) if sentence_lengths else 0,
        'max_sentence_length': max(sentence_lengths) if sentence_lengths else 0,
        'dialogue_ratio': round(dialogue_ratio, 3),
        'dialogue_line_count': len(dialogue_lines),
        'narrative_line_count': len(narrative_lines),
        'top50_words': dict(word_counter.most_common(50)),
        'punctuation_freq': dict(punct_counter),
        'paragraph_count': len([l for l in lines if l.strip()]),
    }


def extract_style_anchor(chapter_paths: list[Path]) -> dict:
    """从多个章节提取风格锚点"""
    all_features = []
    
    for path in chapter_paths:
        if path.exists():
            content = path.read_text(encoding='utf-8')
            features = extract_style_features(content)
            features['chapter'] = path.stem
            all_features.append(features)
    
    if not all_features:
        return {}
    
    # 汇总统计
    avg_sentence_lengths = [f['avg_sentence_length'] for f in all_features]
    dialogue_ratios = [f['dialogue_ratio'] for f in all_features]
    
    # 合并高频词
    all_words = Counter()
    for f in all_features:
        all_words.update(f['top50_words'])
    
    # 合并标点频率
    all_punct = Counter()
    for f in all_features:
        all_punct.update(f['punctuation_freq'])
    
    return {
        'chapter_count': len(all_features),
        'avg_sentence_length': round(sum(avg_sentence_lengths) / len(avg_sentence_lengths), 1),
        'dialogue_ratio': round(sum(dialogue_ratios) / len(dialogue_ratios), 3),
        'top50_words': dict(all_words.most_common(50)),
        'punctuation_freq': dict(all_punct.most_common()),
        'chapters': all_features,
    }


def main():
    parser = argparse.ArgumentParser(description='风格锚点提取脚本')
    parser.add_argument('--chapters', help='章节目录')
    parser.add_argument('--chapter', help='单个章节文件')
    parser.add_argument('--output', default='style-anchor.json', help='输出文件')
    args = parser.parse_args()
    
    chapter_paths = []
    
    if args.chapters:
        chapters_dir = Path(args.chapters)
        chapter_paths = sorted(chapters_dir.glob('ch*.md'))
    elif args.chapter:
        chapter_paths = [Path(args.chapter)]
    else:
        parser.print_help()
        return
    
    if not chapter_paths:
        print('未找到章节文件')
        return
    
    # 只取最近5章
    chapter_paths = chapter_paths[-5:]
    
    anchor = extract_style_anchor(chapter_paths)
    
    output_path = Path(args.output)
    output_path.write_text(json.dumps(anchor, ensure_ascii=False, indent=2), encoding='utf-8')
    
    print(f'风格锚点已保存到 {output_path}')
    print(f'分析了 {anchor["chapter_count"]} 个章节')
    print(f'平均句长: {anchor["avg_sentence_length"]} 字')
    print(f'对话比例: {anchor["dialogue_ratio"]*100:.1f}%')


if __name__ == '__main__':
    main()
