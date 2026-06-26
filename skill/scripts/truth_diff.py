#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
真相文件变更检测 — 自动检测章节变更并生成更新 diff

对比定稿章节与真相文件，检测需要更新的内容（新角色、新地点、
伏笔变化、情感变化等），输出结构化 diff 供复盘师审核。

用法:
    python scripts/truth_diff.py ch15.md --truth-dir .novel-maker/truth-files/
    python scripts/truth_diff.py ch15.md --prev ch14.md --truth-dir .novel-maker/truth-files/ --json
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from nw_utils import (
    read_chapter, extract_characters, extract_locations,
    detect_hook, clean_markdown, read_truth_section
)


def _load_known_names(truth_dir, filename='characters.md'):
    """从真相文件中提取已知角色名"""
    fpath = os.path.join(truth_dir, filename)
    sections = read_truth_section(fpath)
    if not sections:
        return set()
    names = set()
    for title, content in sections.items():
        for m in re.finditer(r'\*\*([^*]{1,10})\*\*', content):
            name = m.group(1).strip()
            if len(name) >= 2 and not any(c in name for c in '（）()'):
                names.add(name)
        for m in re.finditer(r'[:：]\s*([^\s,，。]{2,6})', content):
            name = m.group(1).strip()
            if len(name) >= 2:
                names.add(name)
    return names


def _load_known_hooks(truth_dir, filename='pending-hooks.md'):
    """从伏笔表中提取已知伏笔"""
    fpath = os.path.join(truth_dir, filename)
    sections = read_truth_section(fpath)
    if not sections:
        return {'pending': [], 'recovered': []}
    hooks = {'pending': [], 'recovered': []}
    for title, content in sections.items():
        if '已回收' in title or '已解决' in title:
            for m in re.finditer(r'H\[(\d+)\]', content):
                hooks['recovered'].append(m.group(1))
        elif 'header' not in title:
            for m in re.finditer(r'H\[(\d+)\]', content):
                hooks['pending'].append(m.group(1))
    return hooks


def _load_known_locations(truth_dir, filename='world-setting.md'):
    """从世界观设定中提取已知地点"""
    fpath = os.path.join(truth_dir, filename)
    sections = read_truth_section(fpath)
    if not sections:
        return set()
    locs = set()
    for title, content in sections.items():
        if '地' in title or '区域' in title or '地点' in title:
            for m in re.finditer(r'\*\*([^*]{2,8})\*\*', content):
                locs.add(m.group(1))
    return locs


def _detect_hook_keywords(text):
    """检测伏笔相关关键词"""
    hook_keywords = {
        'reveal': ['原来', '竟然', '居然', '真相', '秘密', '身份'],
        'setup': ['记住', '将来', '总有一天', '等着', '约定'],
        'foreshadow': ['似乎', '隐约', '感觉', '仿佛', '好像'],
    }
    found = {}
    for htype, keywords in hook_keywords.items():
        matches = [kw for kw in keywords if kw in text]
        if matches:
            found[htype] = matches
    return found


def _detect_emotion_keywords(text):
    """检测情感关键词"""
    emotion_map = {
        '愤怒': ['怒', '火', '恨', '咬牙', '攥拳', '瞪'],
        '悲伤': ['泪', '哭', '泣', '哽咽', '心痛', '悲伤'],
        '喜悦': ['笑', '喜', '乐', '高兴', '兴奋', '激动'],
        '恐惧': ['怕', '恐', '惊', '颤', '抖', '畏惧'],
        '惊讶': ['惊', '没想到', '居然', '竟然', '不敢相信'],
        '平静': ['平静', '淡然', '从容', '沉稳', '泰然'],
    }
    found = {}
    for emotion, keywords in emotion_map.items():
        count = sum(1 for kw in keywords if kw in text)
        if count >= 2:
            found[emotion] = count
    return found


def detect_changes(chapter_path, truth_dir, prev_chapter_path=None):
    """检测章节变更"""
    if not os.path.exists(chapter_path):
        return {'error': f'章节文件不存在: {chapter_path}'}
    if not os.path.isdir(truth_dir):
        return {'error': f'真相文件目录不存在: {truth_dir}'}

    raw, title, clean, wc = read_chapter(chapter_path)
    changes = {
        'chapter': os.path.basename(chapter_path),
        'title': title,
        'word_count': wc,
        'detected': {}
    }

    # 1. 新角色检测
    known_chars = _load_known_names(truth_dir)
    chapter_chars = set(extract_characters(clean))
    new_chars = chapter_chars - known_chars
    if new_chars:
        changes['detected']['new_characters'] = sorted(new_chars)

    # 2. 新地点检测
    known_locs = _load_known_locations(truth_dir)
    chapter_locs = set(extract_locations(clean))
    new_locs = chapter_locs - known_locs
    if new_locs:
        changes['detected']['new_locations'] = sorted(new_locs)

    # 3. 伏笔检测
    hook_keywords = _detect_hook_keywords(clean)
    if hook_keywords:
        changes['detected']['hook_keywords'] = hook_keywords

    # 4. 章末钩子
    hook = detect_hook(raw)
    if hook['type'] not in ('未检测', '未知'):
        changes['detected']['chapter_hook'] = {
            'type': hook['type'],
            'tail_preview': hook.get('tail_preview', '')
        }

    # 5. 情感变化
    emotions = _detect_emotion_keywords(clean)
    if emotions:
        changes['detected']['emotions'] = emotions

    # 6. 与前章对比
    if prev_chapter_path and os.path.exists(prev_chapter_path):
        prev_raw, prev_title, prev_clean, prev_wc = read_chapter(prev_chapter_path)
        prev_chars = set(extract_characters(prev_clean))
        prev_locs = set(extract_locations(prev_clean))
        continuing_chars = chapter_chars & prev_chars
        new_in_chapter = chapter_chars - prev_chars
        changes['detected']['continuing_characters'] = sorted(continuing_chars)
        if new_in_chapter:
            changes['detected']['new_vs_prev'] = sorted(new_in_chapter)

    # 7. 伏笔表状态
    known_hooks = _load_known_hooks(truth_dir)
    changes['detected']['hook_status'] = {
        'pending_count': len(known_hooks['pending']),
        'recovered_count': len(known_hooks['recovered'])
    }

    # 汇总
    change_count = len([v for v in changes['detected'].values() if v])
    changes['summary'] = {
        'total_changes': change_count,
        'has_new_characters': 'new_characters' in changes['detected'],
        'has_new_locations': 'new_locations' in changes['detected'],
        'has_hook_keywords': 'hook_keywords' in changes['detected'],
        'has_emotions': 'emotions' in changes['detected'],
    }

    return changes


def main():
    parser = argparse.ArgumentParser(description='真相文件变更检测')
    parser.add_argument('chapter', help='定稿章节文件路径')
    parser.add_argument('--truth-dir', '-t', required=True, help='真相文件目录')
    parser.add_argument('--prev', '-p', help='前一章文件路径')
    parser.add_argument('--json', action='store_true', help='JSON输出')
    args = parser.parse_args()

    changes = detect_changes(args.chapter, args.truth_dir, args.prev)

    if args.json:
        print(json.dumps(changes, ensure_ascii=False, indent=2))
    else:
        if 'error' in changes:
            print(f"错误: {changes['error']}")
            return
        print(f"=== 变更检测: {changes['chapter']} ({changes['title']}) ===\n")

        detected = changes['detected']
        if 'new_characters' in detected:
            print(f"新角色: {', '.join(detected['new_characters'])}")
        if 'new_locations' in detected:
            print(f"新地点: {', '.join(detected['new_locations'])}")
        if 'hook_keywords' in detected:
            for htype, keywords in detected['hook_keywords'].items():
                print(f"伏笔({htype}): {', '.join(keywords)}")
        if 'chapter_hook' in detected:
            print(f"章末钩子: {detected['chapter_hook']['type']}")
        if 'emotions' in detected:
            for emotion, count in detected['emotions'].items():
                print(f"情感({emotion}): {count}次")
        if 'continuing_characters' in detected:
            print(f"延续角色: {', '.join(detected['continuing_characters'])}")

        if changes['summary']['total_changes'] == 0:
            print("未检测到需要更新的内容")


if __name__ == '__main__':
    main()
