#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
规划师上下文包 — 一键生成规划所需的精简上下文

将规划师需要读取的 10+ 个文件压缩为一个结构化 JSON（~5000 token），
替代手动读取全部真相文件+大纲（~30,000 token）。

用法:
    python scripts/planner_context.py --volume 01 --json
    python scripts/planner_context.py --volume 01 --act 2 --json
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from nw_utils import (
    read_truth_section, list_chapters, read_chapter,
    extract_characters, generate_summary, parse_outline_headings,
    chapter_sort_key
)

NOVEL_MAKER_DIR = '.novel-maker'
TRUTH_DIR = os.path.join(NOVEL_MAKER_DIR, 'truth-files')


def _find_project_root(start_path):
    path = os.path.abspath(start_path)
    for _ in range(10):
        if os.path.isdir(os.path.join(path, NOVEL_MAKER_DIR)):
            return path
        parent = os.path.dirname(path)
        if parent == path:
            break
        path = parent
    return None


def _read_truth_compact(filepath, max_chars=600):
    sections = read_truth_section(filepath)
    if not sections:
        return None
    result = {}
    for title, content in sections.items():
        if title == 'header':
            continue
        lines = [l.strip() for l in content.split('\n') if l.strip() and not l.startswith('#')]
        compact = '\n'.join(lines[:10])
        if len(compact) > max_chars:
            compact = compact[:max_chars] + '...'
        if compact:
            result[title] = compact
    return result


def _get_volume_progress(volume_dir):
    chapters_dir = os.path.join(volume_dir, 'chapters')
    if not os.path.isdir(chapters_dir):
        return {'total': 0, 'chapters': []}
    all_chapters = list_chapters(chapters_dir)
    chapters = []
    total_wc = 0
    for ch_path in all_chapters:
        raw, title, clean, wc = read_chapter(ch_path)
        ch_num = chapter_sort_key(ch_path)
        chars = extract_characters(clean)[:5]
        summary = generate_summary(raw, first_n=50, last_n=50)
        chapters.append({
            'number': ch_num,
            'title': title,
            'word_count': wc,
            'characters': chars,
            'summary': summary
        })
        total_wc += wc
    return {
        'total': len(chapters),
        'total_word_count': total_wc,
        'chapters': chapters[-5:]  # 只返回最近5章
    }


def _get_outline_context(outline_path, current_chapter=None):
    if not os.path.exists(outline_path):
        return None
    with open(outline_path, encoding='utf-8') as f:
        text = f.read()
    headings = parse_outline_headings(text)
    if current_chapter:
        result = []
        found = False
        for h in headings:
            if f'第{current_chapter}章' in h['title']:
                found = True
            if found:
                result.append(h)
                if len(result) >= 10:
                    break
        if not result:
            result = headings[-10:] if len(headings) > 10 else headings
    else:
        result = headings[-10:] if len(headings) > 10 else headings
    return [{'level': h['level'], 'title': h['title']} for h in result]


def _get_active_hooks(truth_dir):
    fpath = os.path.join(truth_dir, 'pending-hooks.md')
    sections = read_truth_section(fpath)
    if not sections:
        return []
    hooks = []
    for title, content in sections.items():
        if 'header' in title or '已回收' in title or '已解决' in title:
            continue
        lines = [l.strip() for l in content.split('\n') if l.strip() and not l.startswith('#')]
        for line in lines:
            if 'H[' in line or '伏笔' in line or '钩子' in line:
                hooks.append(line[:100])
    return hooks[:10]


def _get_active_subplots(truth_dir):
    fpath = os.path.join(truth_dir, 'subplot-board.md')
    sections = read_truth_section(fpath)
    if not sections:
        return []
    subplots = []
    for title, content in sections.items():
        if '活跃' in title:
            lines = [l.strip() for l in content.split('\n') if l.strip() and not l.startswith('#')]
            for line in lines:
                if line.startswith('-') or line.startswith('*'):
                    subplots.append(line[:100])
    return subplots[:5]


def build_planner_context(volume='01', act=None, root=None, truth_dir=None):
    if root:
        pass
    else:
        root = _find_project_root('.')
    if not root:
        return {'error': '未找到 .novel-maker 目录'}

    truth_path = truth_dir or os.path.join(root, TRUTH_DIR)
    volume_dir = os.path.join(root, 'novels', f'volume-{volume.zfill(2)}')

    context = {
        'meta': {'volume': volume, 'act': act},
        'volume_progress': {},
        'truth_files': {},
        'outline': None,
        'active_hooks': [],
        'active_subplots': []
    }

    # 卷进度
    context['volume_progress'] = _get_volume_progress(volume_dir)

    # 真相文件摘要
    truth_files = {
        'characters': 'characters.md',
        'current_state': 'current-state.md',
        'world_setting': 'world-setting.md',
        'power_system': 'power-system.md',
        'emotional_arcs': 'emotional-arcs.md',
    }
    for key, filename in truth_files.items():
        fpath = os.path.join(truth_path, filename)
        compact = _read_truth_compact(fpath)
        if compact:
            context['truth_files'][key] = compact

    # 大纲
    outline_path = os.path.join(volume_dir, 'outline.md')
    current_ch = context['volume_progress']['total'] + 1 if context['volume_progress']['total'] > 0 else None
    context['outline'] = _get_outline_context(outline_path, current_ch)

    # 活跃伏笔
    context['active_hooks'] = _get_active_hooks(truth_path)

    # 活跃支线
    context['active_subplots'] = _get_active_subplots(truth_path)

    return context


def main():
    parser = argparse.ArgumentParser(description='规划师上下文包')
    parser.add_argument('--volume', '-v', default='01', help='卷号（默认01）')
    parser.add_argument('--act', '-a', type=int, help='当前幕号')
    parser.add_argument('--root', help='项目根目录')
    parser.add_argument('--truth-dir', help='真相文件目录')
    parser.add_argument('--json', action='store_true', help='JSON输出')
    args = parser.parse_args()

    ctx = build_planner_context(args.volume, args.act, args.root, args.truth_dir)

    if args.json:
        print(json.dumps(ctx, ensure_ascii=False, indent=2))
    else:
        if 'error' in ctx:
            print(f"错误: {ctx['error']}")
            return
        print(f"=== 规划师上下文: 卷{ctx['meta']['volume']} ===\n")
        prog = ctx['volume_progress']
        print(f"进度: {prog['total']}章, {prog.get('total_word_count', 0)}字")
        if ctx['truth_files']:
            print(f"真相文件: {len(ctx['truth_files'])}个")
        if ctx['active_hooks']:
            print(f"活跃伏笔: {len(ctx['active_hooks'])}个")
        if ctx['active_subplots']:
            print(f"活跃支线: {len(ctx['active_subplots'])}条")


if __name__ == '__main__':
    main()
