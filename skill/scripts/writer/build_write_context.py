#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
写手上下文构建器 — 一键生成写作所需的精简上下文

将写手需要读取的 15+ 个文件压缩为一个结构化 JSON（~3000 token），
每章节省约 40,000-60,000 token 的文件读取消耗。

用法:
    python scripts/writer/build_write_context.py novels/volume-01/chapters/ch15.md
    python scripts/writer/build_write_context.py --chapter 15 --volume 01
    python scripts/writer/build_write_context.py --chapter 15 --json
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'common'))
from nm_utils import (
    read_truth_section, list_chapters, read_chapter,
    extract_characters, generate_summary, detect_hook,
    parse_outline_headings
)

NOVEL_MAKER_DIR = '.novel-maker'
TRUTH_DIR = os.path.join(NOVEL_MAKER_DIR, 'truth-files')


def _find_project_root(start_path):
    """向上查找包含 .novel-maker 的项目根目录"""
    path = os.path.abspath(start_path)
    for _ in range(10):
        if os.path.isdir(os.path.join(path, NOVEL_MAKER_DIR)):
            return path
        parent = os.path.dirname(path)
        if parent == path:
            break
        path = parent
    return None


def _read_truth_compact(filepath, max_chars=800):
    """读取真相文件并压缩为精简摘要"""
    sections = read_truth_section(filepath)
    if not sections:
        return None
    result = {}
    for title, content in sections.items():
        if title == 'header':
            continue
        lines = [l.strip() for l in content.split('\n') if l.strip() and not l.startswith('#')]
        compact = '\n'.join(lines[:15])  # 每个section最多15行
        if len(compact) > max_chars:
            compact = compact[:max_chars] + '...'
        if compact:
            result[title] = compact
    return result


def _get_prev_chapters_info(chapters_dir, current_chapter_num, count=2):
    """获取前N章的结构化摘要"""
    all_chapters = list_chapters(chapters_dir)
    prev = []
    for ch_path in all_chapters:
        raw, title, clean, wc = read_chapter(ch_path)
        # 判断是否在当前章之前
        from nm_utils import chapter_sort_key
        ch_num = chapter_sort_key(ch_path)
        if ch_num >= current_chapter_num:
            break
        prev.append((ch_num, ch_path, raw, title, clean, wc))

    # 只取最近N章
    prev = prev[-count:]
    results = []
    for ch_num, ch_path, raw, title, clean, wc in prev:
        chars = extract_characters(clean)[:8]
        summary = generate_summary(raw, first_n=100, last_n=100)
        hook = detect_hook(raw)
        results.append({
            'chapter': os.path.basename(ch_path),
            'number': ch_num,
            'title': title,
            'word_count': wc,
            'characters': chars,
            'hook': hook['type'],
            'summary': summary
        })
    return results


def _get_outline_context(outline_path, chapter_num):
    """从大纲中提取当前章节的目标"""
    if not os.path.exists(outline_path):
        return None
    with open(outline_path, encoding='utf-8') as f:
        text = f.read()
    headings = parse_outline_headings(text)
    # 找到当前章节附近的大纲节点
    result = []
    found_current = False
    for h in headings:
        if f'第{chapter_num}章' in h['title'] or f'第{_to_cn(chapter_num)}章' in h['title']:
            found_current = True
        if found_current:
            result.append(h)
            if len(result) >= 5:
                break
    # 如果没找到精确匹配，返回最后几个节点
    if not result:
        result = headings[-5:] if len(headings) > 5 else headings
    return [{'level': h['level'], 'title': h['title']} for h in result]


def _to_cn(n):
    """数字转中文"""
    cn = '零一二三四五六七八九十'
    if n <= 10:
        return cn[n]
    if n < 20:
        return '十' + (cn[n - 10] if n > 10 else '')
    return str(n)


def _get_constitution_summary(constitution_path):
    """提取创作宪法要点"""
    if not os.path.exists(constitution_path):
        return None
    sections = read_truth_section(constitution_path)
    if not sections:
        return None
    key_sections = ['字数要求', '文风配置', '核心创作原则', '禁忌清单']
    result = {}
    for title, content in sections.items():
        if any(k in title for k in key_sections):
            lines = [l.strip() for l in content.split('\n') if l.strip() and not l.startswith('#')]
            result[title] = '\n'.join(lines[:8])
    return result


def build_context(chapter_path=None, chapter_num=None, volume=None,
                  novel_root=None, truth_dir=None, recent_count=2):
    """构建写手上下文"""

    # 确定项目根目录
    if novel_root:
        root = novel_root
    elif chapter_path:
        root = _find_project_root(os.path.dirname(chapter_path))
    else:
        root = _find_project_root('.')

    if not root:
        return {'error': '未找到 .novel-maker 目录，请先运行 /novel-maker init'}

    truth_path = truth_dir or os.path.join(root, TRUTH_DIR)
    context = {'meta': {}, 'truth_files': {}, 'prev_chapters': [], 'outline': None, 'constitution': None}

    # 确定章节号和卷号
    if chapter_path and os.path.exists(chapter_path):
        from nm_utils import chapter_sort_key
        chapter_num = chapter_num or chapter_sort_key(chapter_path)
        chapters_dir = os.path.dirname(chapter_path)
        volume = volume or os.path.basename(os.path.dirname(chapters_dir))
    elif chapter_num and volume:
        chapters_dir = os.path.join(root, 'novels', f'volume-{volume.zfill(2)}', 'chapters')
        chapter_path = None
    else:
        return {'error': '请指定章节路径或章节号+卷号'}

    context['meta'] = {
        'chapter_num': chapter_num,
        'volume': volume,
        'chapters_dir': chapters_dir
    }

    # 1. 读取精简版真相文件
    truth_files = {
        'characters': 'characters.md',
        'current_state': 'current-state.md',
        'world_setting': 'world-setting.md',
        'power_system': 'power-system.md',
        'pending_hooks': 'pending-hooks.md',
        'emotional_arcs': 'emotional-arcs.md',
    }
    for key, filename in truth_files.items():
        fpath = os.path.join(truth_path, filename)
        compact = _read_truth_compact(fpath)
        if compact:
            context['truth_files'][key] = compact

    # 2. 前N章摘要
    if os.path.isdir(chapters_dir):
        context['prev_chapters'] = _get_prev_chapters_info(chapters_dir, chapter_num, recent_count)

    # 3. 大纲目标
    outline_path = os.path.join(root, 'novels', f'volume-{volume.zfill(2) if volume else "01"}', 'outline.md')
    if not os.path.exists(outline_path):
        outline_path = os.path.join(root, 'novels', 'outline.md')
    context['outline'] = _get_outline_context(outline_path, chapter_num)

    # 4. 创作宪法要点
    constitution_path = os.path.join(root, NOVEL_MAKER_DIR, 'constitution.md')
    if not os.path.exists(constitution_path):
        constitution_path = os.path.join(root, 'constitution.md')
    context['constitution'] = _get_constitution_summary(constitution_path)

    return context


def main():
    parser = argparse.ArgumentParser(description='写手上下文构建器')
    parser.add_argument('chapter', nargs='?', help='章节文件路径')
    parser.add_argument('--chapter-num', '-n', type=int, help='章节号')
    parser.add_argument('--volume', '-v', help='卷号')
    parser.add_argument('--root', help='项目根目录')
    parser.add_argument('--truth-dir', help='真相文件目录')
    parser.add_argument('--recent', type=int, default=2, help='前N章摘要（默认2）')
    parser.add_argument('--json', action='store_true', help='JSON输出')
    args = parser.parse_args()

    ctx = build_context(
        chapter_path=args.chapter,
        chapter_num=args.chapter_num,
        volume=args.volume,
        novel_root=args.root,
        truth_dir=args.truth_dir,
        recent_count=args.recent
    )

    if args.json:
        print(json.dumps(ctx, ensure_ascii=False, indent=2))
    else:
        if 'error' in ctx:
            print(f"错误: {ctx['error']}")
            return
        print(f"=== 写手上下文: 第{ctx['meta']['chapter_num']}章 ===\n")
        if ctx['truth_files']:
            print("【真相文件摘要】")
            for name, data in ctx['truth_files'].items():
                print(f"  {name}: {len(data)}个section")
        if ctx['prev_chapters']:
            print(f"\n【前{len(ctx['prev_chapters'])}章摘要】")
            for ch in ctx['prev_chapters']:
                print(f"  {ch['chapter']}: {ch['title']} ({ch['word_count']}字) 钩子:{ch['hook']}")
        if ctx['outline']:
            print(f"\n【大纲目标】")
            for h in ctx['outline']:
                print(f"  {'  ' * (h['level'] - 1)}{h['title']}")


if __name__ == '__main__':
    main()
