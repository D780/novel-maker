#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
三合一分析脚本
整合 chapter_info / style_check / hook_report 的功能。

用法:
  python analyze.py ch01.md --mode single [--json]
  python analyze.py ch01.md --mode style  [--json]
  python analyze.py chapters/ --mode batch [--recent N] [--json]
"""

import argparse
import json
import os
import sys

from chapter_info import analyze_chapter
from style_check import analyze_chapter_style
from hook_report import analyze_volume


def _print_single(result):
    """人类可读格式输出 single 模式结果。"""
    if 'error' in result:
        print(result['error'])
        return
    print(f"章节: {result['title'] or result['file']}")
    print(f"字数: {result['word_count']}")
    print(f"角色: {', '.join(result['characters'][:8]) if result['characters'] else '未检测到'}")
    print(f"地点: {', '.join(result['locations'][:5]) if result['locations'] else '未检测到'}")
    s = result['structure']
    print(f"结构: 对话{s['dialogue_pct']}% / 动作{s['action_pct']}% / 描写{s['description_pct']}% ({s['total_paragraphs']}段)")
    h = result['hook']
    print(f"钩子: {h['type']} (结尾预览: {h['tail_preview'][:40]}...)")
    print(f"摘要: 开头={result['summary']['开头'][:50]}...")
    print(f"      结尾={result['summary']['结尾'][-50:]}...")


def _print_style(result):
    """人类可读格式输出 style 模式结果。"""
    print(f"\n=== {result['title']} ({result['word_count']}字) ===")
    print(f"  对话占比: {result['dialogue_ratio_pct']}%  |  平均句长: {result['avg_sentence_length']}字  |  AI词密度: {result['ai_density_per_1000']}/千字")
    if result['issues']:
        for issue in result['issues']:
            if issue['type'] == 'ai_pattern':
                print(f"  ⚠ {issue['pattern']}: 出现{issue['count']}次")
            elif issue['type'] == 'repetitive_word':
                print(f"  ⚠ 重复词汇: 「{issue['word']}」出现{issue['count']}次")
            elif issue['type'] == 'ai_density':
                print(f"  ⚠ AI词密度过高: {issue['ai_words_per_1000']}/千字")
    else:
        print("  ✅ 无明显AI味")


def _print_batch(result):
    """人类可读格式输出 batch 模式结果。"""
    if 'error' in result:
        print(result['error'])
        return
    print(f"=== 钩子密度报告 (最近{result.get('total_chapters', 0)}章) ===\n")
    print("钩子类型分布:")
    for hook_type, count in sorted(result["hook_distribution"].items(),
                                    key=lambda x: x[1], reverse=True):
        bar = "█" * count
        print(f"  {hook_type:4s}: {bar} ({count})")
    print()
    if result["warnings"]["consecutive_same_hook"]:
        print("⚠ 警告 - 连续相同钩子:")
        for w in result["warnings"]["consecutive_same_hook"]:
            print(f"  {w}")
    if result["warnings"]["unknown_hooks"] > 0:
        print(f"\n⚠ {result['warnings']['unknown_hooks']} 章钩子类型未知，建议手动标记")
    print()
    for ch in result["chapters"]:
        print(f"  第{ch['chapter']}章 [{ch['hook_type']}]: {ch['ending_summary'][:80]}...")


def main():
    parser = argparse.ArgumentParser(description='三合一分析脚本')
    parser.add_argument('path', help='章节文件(single/style)或章节目录(batch)')
    parser.add_argument('--mode', required=True, choices=['single', 'style', 'batch'],
                        help='分析模式: single=章节结构, style=AI味检测, batch=批量钩子')
    parser.add_argument('--json', action='store_true', help='JSON 格式输出')
    parser.add_argument('--recent', type=int, default=None, help='仅分析最近 N 章 (仅 batch 模式)')
    args = parser.parse_args()

    # ── batch 模式：path 必须是目录 ──
    if args.mode == 'batch':
        if not os.path.isdir(args.path):
            print(f"错误: 目录不存在: {args.path}", file=sys.stderr)
            sys.exit(1)
        result = analyze_volume(args.path, recent_n=args.recent)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            _print_batch(result)
        return

    # ── single / style 模式：path 必须是文件 ──
    if not os.path.isfile(args.path):
        print(f"错误: 文件不存在: {args.path}", file=sys.stderr)
        sys.exit(1)

    if args.mode == 'single':
        result = analyze_chapter(args.path)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            _print_single(result)

    elif args.mode == 'style':
        with open(args.path, 'r', encoding='utf-8') as f:
            text = f.read()
        result = analyze_chapter_style(text, args.path)
        if result is None:
            print(f"错误: 无法分析文件 (字数为 0): {args.path}", file=sys.stderr)
            sys.exit(1)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            _print_style(result)


if __name__ == '__main__':
    main()
