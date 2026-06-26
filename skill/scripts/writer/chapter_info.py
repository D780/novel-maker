#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
章节结构化信息提取
将章节全文压缩为结构化数据，AI 可直接读取此输出代替全文，大幅减少 token 消耗。
"""

import sys
import json
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'common'))
from nm_utils import (
    clean_markdown, count_chinese, extract_title, read_chapter,
    extract_characters, extract_locations, detect_structure,
    detect_hook, generate_summary
)


def analyze_chapter(filepath):
    raw, title, clean, wc = read_chapter(filepath)
    return {
        'file': os.path.basename(filepath),
        'title': title,
        'word_count': wc,
        'characters': extract_characters(clean),
        'locations': extract_locations(clean),
        'structure': detect_structure(raw),
        'hook': detect_hook(raw),
        'summary': generate_summary(raw)
    }


def main():
    if len(sys.argv) < 2:
        print('用法: python chapter_info.py <章节文件路径> [--json]')
        print('      python chapter_info.py <文件> --json  # 纯JSON输出给AI用')
        return
    filepath = sys.argv[1]
    json_only = '--json' in sys.argv

    if not os.path.exists(filepath):
        result = {'error': f'文件不存在: {filepath}'}
    else:
        result = analyze_chapter(filepath)

    if json_only:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        info = result
        if 'error' in info:
            print(info['error'])
            return
        print(f"章节: {info['title'] or info['file']}")
        print(f"字数: {info['word_count']}")
        print(f"角色: {', '.join(info['characters'][:8]) if info['characters'] else '未检测到'}")
        print(f"地点: {', '.join(info['locations'][:5]) if info['locations'] else '未检测到'}")
        s = info['structure']
        print(f"结构: 对话{s['dialogue_pct']}% / 动作{s['action_pct']}% / 描写{s['description_pct']}% ({s['total_paragraphs']}段)")
        h = info['hook']
        print(f"钩子: {h['type']} (结尾预览: {h['tail_preview'][:40]}...)")
        print(f"摘要: 开头={info['summary']['开头'][:50]}...")
        print(f"      结尾={info['summary']['结尾'][-50:]}...")


if __name__ == '__main__':
    main()
