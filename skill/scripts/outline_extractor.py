#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大纲快速提取
解析 outline.md 和 vol*/plan.md 的标题层级，输出结构化大纲树。
供 `/novel-maker memory outline` 指令使用。
"""

import os
import sys
import json

from nw_utils import parse_outline_headings, count_chinese


def extract_outline(filepath):
    """Extract structured outline from a markdown file."""
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    wc = count_chinese(text)
    tree = parse_outline_headings(text)
    return {'file': os.path.basename(filepath), 'words': wc, 'headings': tree}


def extract_all_outlines(base_dir):
    """Extract all outline-related files."""
    results = {}

    # Main outline
    outline_path = os.path.join(base_dir, 'outline.md')
    if os.path.exists(outline_path):
        results['outline'] = extract_outline(outline_path)

    # Volume plans
    for entry in sorted(os.listdir(base_dir)):
        vol_path = os.path.join(base_dir, entry)
        if os.path.isdir(vol_path) and entry.startswith('volume'):
            plan_path = os.path.join(vol_path, 'plan.md')
            if os.path.exists(plan_path):
                results[entry] = extract_outline(plan_path)

            # Act plans
            act_path = os.path.join(vol_path, 'act-plan.md')
            if os.path.exists(act_path):
                results[f"{entry}/act-plan"] = extract_outline(act_path)

    return results


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Outline extractor")
    parser.add_argument("base_dir", nargs='?', default='novels', help="Novels base directory")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--file", type=str, help="Specific file to extract")
    args = parser.parse_args()

    if args.file:
        if not os.path.isfile(args.file):
            print(f"Error: {args.file} not found", file=sys.stderr)
            sys.exit(1)
        result = {args.file: extract_outline(args.file)}
    else:
        if not os.path.isdir(args.base_dir):
            print(f"Error: {args.base_dir} is not a directory", file=sys.stderr)
            sys.exit(1)
        result = extract_all_outlines(args.base_dir)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for key, val in result.items():
            if val is None:
                print(f"\n❌ {key}: 文件不存在")
                continue
            print(f"\n{'=' * 50}")
            print(f"📄 {key} ({val['words']}字, {len(val['headings'])}个标题)")
            print(f"{'=' * 50}")
            for h in val['headings']:
                indent = "  " * (h['level'] - 1)
                marker = {1: '📖', 2: '📑', 3: '📝', 4: '•'}.get(h['level'], '•')
                print(f"{indent}{marker} {h['title']}")


if __name__ == "__main__":
    main()
