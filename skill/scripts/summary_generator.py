#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阶段总结辅助脚本
从各章结构化数据中提取摘要，拼接剧情时间线。
供 `/novel-weaver summary` 指令使用，AI 读取此输出代替读全文。
"""

import os
import sys
import json

from nw_utils import (
    list_chapters, read_chapter, extract_characters, extract_locations,
    detect_hook, count_chinese, clean_markdown
)


def build_chapter_timeline(chapter_path):
    """Extract a structured timeline entry from a single chapter."""
    raw, title, clean, wc = read_chapter(chapter_path)
    chars = extract_characters(clean)
    locs = extract_locations(clean)
    hook = detect_hook(raw)

    # Extract first and last paragraph summaries
    paragraphs = [p.strip() for p in clean.split('\n') if p.strip()]
    first_para = paragraphs[0][:100] if paragraphs else ''
    last_para = paragraphs[-1][-150:] if paragraphs else ''

    return {
        'title': title,
        'words': wc,
        'characters': chars[:6],
        'locations': locs[:3],
        'hook_type': hook['type'],
        'first_para_summary': first_para,
        'last_para_summary': last_para,
    }


def generate_summary(chapters_dir, start_n=1, end_n=None):
    """Generate a structured summary for chapters start_n through end_n."""
    all_chapters = list_chapters(chapters_dir)
    if not all_chapters:
        return {'error': 'No chapters found'}

    if end_n is None:
        end_n = len(all_chapters)
    start_idx = max(0, start_n - 1)
    end_idx = min(len(all_chapters), end_n)
    target_chapters = all_chapters[start_idx:end_idx]

    timeline = []
    all_chars = set()
    all_locs = set()

    for cf in target_chapters:
        entry = build_chapter_timeline(cf)
        timeline.append(entry)
        all_chars.update(entry['characters'])
        all_locs.update(entry['locations'])

    total_words = sum(t['words'] for t in timeline)

    return {
        'chapter_range': f"第{start_n}-{start_n + len(timeline) - 1}章",
        'total_chapters': len(timeline),
        'total_words': total_words,
        'avg_words': round(total_words / max(len(timeline), 1), 0),
        'timeline': timeline,
        'characters_involved': sorted(all_chars),
        'locations_visited': sorted(all_locs),
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Summary generator")
    parser.add_argument("chapters_dir", help="Chapters directory")
    parser.add_argument("--range", type=str, help="Chapter range, e.g. '1-10' or '11-20'", default=None)
    parser.add_argument("--last", type=int, help="Last N chapters", default=None)
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    if not os.path.isdir(args.chapters_dir):
        print(f"Error: {args.chapters_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    start_n = 1
    end_n = None

    if args.range:
        parts = args.range.split('-')
        if len(parts) == 2:
            start_n = int(parts[0])
            end_n = int(parts[1])
    elif args.last:
        all_chapters = list_chapters(args.chapters_dir)
        start_n = max(1, len(all_chapters) - args.last + 1)

    result = generate_summary(args.chapters_dir, start_n, end_n)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if 'error' in result:
            print(result['error'])
            return

        print(f"\n{'=' * 60}")
        print(f"📋 阶段总结 ({result['chapter_range']})")
        print(f"{'=' * 60}")
        print(f"章节数: {result['total_chapters']}")
        print(f"总字数: {result['total_words']:,}")
        print(f"平均字数: {result['avg_words']}/章")
        print(f"涉及角色: {', '.join(result['characters_involved'][:8])}")
        print(f"涉及场景: {', '.join(result['locations_visited'][:5])}")
        print(f"\n剧情时间线:")
        for t in result['timeline']:
            print(f"\n  {t['title']} ({t['words']}字)")
            print(f"    角色: {', '.join(t['characters'][:4])}")
            print(f"    开头: {t['first_para_summary'][:60]}...")
            print(f"    结尾: ...{t['last_para_summary'][-60:]}")
            print(f"    钩子: {t['hook_type']}")


if __name__ == "__main__":
    main()
