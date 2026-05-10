#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
真相文件管理器
解析 truth-files 目录，快速查看角色、伏笔、世界观、力量体系等实体信息。
供 `/novel-weaver memory entity` 指令使用。
"""

import os
import sys
import json
import re

from nw_utils import read_truth_section, count_chinese


TRUTH_FILES = {
    'characters': '角色档案',
    'world-setting': '世界观',
    'power-system': '力量体系',
    'current-state': '当前状态',
    'pending-hooks': '伏笔表',
    'constitution': '创作宪法',
}


def scan_truth_files(truth_dir):
    """Scan all truth files and return structured data."""
    if not os.path.isdir(truth_dir):
        return {'error': f'目录不存在: {truth_dir}'}

    result = {}
    for key, label in TRUTH_FILES.items():
        filepath = os.path.join(truth_dir, f'{key}.md')
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
            wc = count_chinese(text)
            sections = read_truth_section(filepath)
            result[key] = {
                'label': label,
                'words': wc,
                'sections': list(sections.keys()) if sections else [],
                'sections_content': sections,
            }

    # Extract character names from characters.md
    if 'characters' in result:
        content = result['characters'].get('sections_content', {})
        char_names = []
        for section_text in content.values():
            for m in re.finditer(r'[*\-]?\s*\*\*?([\u4e00-\u9fff]{2,4})\*\*?', section_text):
                name = m.group(1)
                if name not in ('角色', '人物', '主角', '配角', '反派', '姓名'):
                    char_names.append(name)
        result['characters']['extracted_names'] = list(set(char_names))[:20]

    # Extract hook info from pending-hooks.md
    if 'pending-hooks' in result:
        content = result['pending-hooks'].get('sections_content', {})
        hooks = []
        for section_text in content.values():
            for m in re.finditer(r'\[([^\]]+)\]', section_text):
                hooks.append(m.group(1))
        result['pending-hooks']['extracted_hooks'] = hooks[:10]

    return result


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Truth files manager")
    parser.add_argument("truth_dir", nargs='?', default=None, help="Truth files directory")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--entity", type=str, help="Show specific entity (characters/world/power/hooks/state)")
    args = parser.parse_args()

    truth_dir = args.truth_dir
    if truth_dir is None:
        # Try common locations
        for candidate in ['.novel-weaver/truth-files', 'novels/truth-files', 'truth-files']:
            if os.path.isdir(candidate):
                truth_dir = candidate
                break
        if truth_dir is None:
            print("错误: 未找到 truth-files 目录，请指定路径", file=sys.stderr)
            sys.exit(1)

    result = scan_truth_files(truth_dir)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if 'error' in result:
        print(result['error'])
        return

    print(f"\n{'=' * 60}")
    print(f"📁 真相文件管理 ({truth_dir})")
    print(f"{'=' * 60}\n")

    for key, info in result.items():
        if args.entity and key != args.entity:
            continue
        print(f"📄 {info['label']} ({key}.md, {info['words']}字)")
        if info['sections']:
            print(f"   章节: {', '.join(info['sections'])}")
        if key == 'characters' and info.get('extracted_names'):
            print(f"   角色: {', '.join(info['extracted_names'][:10])}")
        if key == 'pending-hooks' and info.get('extracted_hooks'):
            print(f"   伏笔 ({len(info['extracted_hooks'])}条):")
            for h in info['extracted_hooks'][:5]:
                print(f"     • {h}")
        print()


if __name__ == "__main__":
    main()
