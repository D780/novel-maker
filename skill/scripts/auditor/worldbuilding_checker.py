#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
世界观一致性检查脚本
检测世界观设定的前后矛盾，包括力量体系、地理、历史、社会制度等。
供审计师在审查时使用，或复盘师在卷末复盘时参考。

用法:
    python scripts/auditor/worldbuilding_checker.py 章节目录 --truth 真相文件目录 --json
    python scripts/auditor/worldbuilding_checker.py 章节目录 --truth 真相文件目录 --recent 10
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'common'))
from nm_utils import (
    list_chapters, read_chapter, count_chinese, clean_markdown,
    read_truth_section
)

# ─── 世界观检查维度 ──────────────────────────────
WORLDBUILDING_DIMENSIONS = {
    'power_system': {
        'name': '力量体系',
        'keywords': ['等级', '境界', '修为', '实力', '突破', '晋升', '阶位', '段位'],
        'check_patterns': [
            r'(\w+)\s*(?:从|由)\s*(\w+)\s*(?:突破|晋升|进阶)\s*(?:到|为)\s*(\w+)',
            r'(\w+)\s*(?:是|为)\s*(\w+)\s*(?:级别|等级|境界)'
        ]
    },
    'geography': {
        'name': '地理设定',
        'keywords': ['城市', '国家', '大陆', '山脉', '河流', '森林', '沙漠', '海洋'],
        'check_patterns': [
            r'(?:位于|在)\s*(\w+)\s*(?:的|方向|方位)',
            r'(\w+)\s*(?:距离|相距)\s*(\w+)\s*(?:有|约)\s*(\d+)\s*(?:里|公里)'
        ]
    },
    'history': {
        'name': '历史设定',
        'keywords': ['年前', '年前', '历史', '传说', '古老', '过去', '曾经', '当年'],
        'check_patterns': [
            r'(\d+)\s*(?:年前|百年前|千年前)',
            r'(?:在|于)\s*(\w+)\s*(?:时期|时代|年代)'
        ]
    },
    'social_system': {
        'name': '社会制度',
        'keywords': ['宗门', '门派', '家族', '朝廷', '帝国', '王国', '组织', '势力'],
        'check_patterns': [
            r'(\w+)\s*(?:是|属于)\s*(\w+)\s*(?:的|宗门|门派|家族)',
            r'(\w+)\s*(?:担任|是)\s*(\w+)\s*(?:职位|职务|身份)'
        ]
    },
    'items': {
        'name': '物品设定',
        'keywords': ['宝物', '神器', '丹药', '武器', '装备', '秘籍', '功法'],
        'check_patterns': [
            r'(\w+)\s*(?:具有|拥有)\s*(\w+)\s*(?:效果|功能|作用)',
            r'(\w+)\s*(?:需要|要求)\s*(\w+)\s*(?:才能|方可)\s*(?:使用|激活)'
        ]
    }
}


def extract_worldbuilding_facts(text, dimension_config):
    """Extract worldbuilding facts from text based on dimension config."""
    facts = []

    for pattern in dimension_config['check_patterns']:
        matches = re.finditer(pattern, text)
        for match in matches:
            facts.append({
                'pattern': pattern,
                'match': match.group(0),
                'groups': match.groups(),
                'position': match.start()
            })

    return facts


def check_worldbuilding_consistency(chapters_dir, truth_dir=None, recent_n=None):
    """Check worldbuilding consistency across chapters."""
    chapter_files = list_chapters(chapters_dir, recent_n)
    if not chapter_files:
        return {'error': '未找到章节文件'}

    # Load truth files if provided
    truth_facts = {}
    if truth_dir and os.path.isdir(truth_dir):
        for dimension in WORLDBUILDING_DIMENSIONS.keys():
            truth_file = os.path.join(truth_dir, f'{dimension}.md')
            if os.path.exists(truth_file):
                with open(truth_file, 'r', encoding='utf-8') as f:
                    truth_facts[dimension] = f.read()

    # Analyze each chapter
    chapter_facts = defaultdict(lambda: defaultdict(list))
    issues = []

    for idx, cf in enumerate(chapter_files):
        raw, title, clean, wc = read_chapter(cf)
        ch_num = idx + 1

        for dimension, config in WORLDBUILDING_DIMENSIONS.items():
            facts = extract_worldbuilding_facts(clean, config)
            chapter_facts[ch_num][dimension] = facts

            # Check against truth files
            if dimension in truth_facts:
                truth_content = truth_facts[dimension]
                for fact in facts:
                    # Simple consistency check: verify key terms appear in truth
                    for group in fact['groups']:
                        if group and group not in truth_content:
                            issues.append({
                                'type': '设定冲突',
                                'dimension': config['name'],
                                'chapter': ch_num,
                                'chapter_title': title,
                                'fact': fact['match'],
                                'message': f"「{group}」未在真相文件「{dimension}.md」中找到",
                                'severity': 'warning'
                            })

    # Detect internal contradictions (same entity with different descriptions)
    entity_descriptions = defaultdict(list)
    for ch_num, dimensions in chapter_facts.items():
        for dimension, facts in dimensions.items():
            for fact in facts:
                if fact['groups'] and len(fact['groups']) >= 2:
                    entity = fact['groups'][0]
                    description = fact['groups'][1]
                    entity_descriptions[entity].append({
                        'chapter': ch_num,
                        'dimension': dimension,
                        'description': description
                    })

    # Find contradictions
    for entity, descriptions in entity_descriptions.items():
        unique_descriptions = set(d['description'] for d in descriptions)
        if len(unique_descriptions) > 1:
            issues.append({
                'type': '内部矛盾',
                'dimension': WORLDBUILDING_DIMENSIONS[descriptions[0]['dimension']]['name'],
                'entity': entity,
                'descriptions': descriptions,
                'message': f"「{entity}」在不同章节有不同描述",
                'severity': 'error'
            })

    # Summary statistics
    dimension_stats = {}
    for dimension, config in WORLDBUILDING_DIMENSIONS.items():
        total_facts = sum(len(chapter_facts[ch][dimension]) for ch in chapter_facts)
        dimension_stats[dimension] = {
            'name': config['name'],
            'total_facts': total_facts,
            'chapters_with_facts': sum(1 for ch in chapter_facts if chapter_facts[ch][dimension])
        }

    return {
        'total_chapters': len(chapter_files),
        'dimensions_checked': len(WORLDBUILDING_DIMENSIONS),
        'dimension_stats': dimension_stats,
        'issues': issues,
        'issue_count': len(issues),
        'error_count': sum(1 for i in issues if i['severity'] == 'error'),
        'warning_count': sum(1 for i in issues if i['severity'] == 'warning')
    }


def main():
    parser = argparse.ArgumentParser(description='世界观一致性检查脚本')
    parser.add_argument('chapters_dir', help='章节目录路径')
    parser.add_argument('--truth', '-t', help='真相文件目录路径')
    parser.add_argument('--recent', type=int, help='仅检查最近N章')
    parser.add_argument('--json', action='store_true', help='JSON输出')
    args = parser.parse_args()

    if not os.path.isdir(args.chapters_dir):
        print(f"错误: 目录不存在: {args.chapters_dir}", file=sys.stderr)
        sys.exit(1)

    result = check_worldbuilding_consistency(args.chapters_dir, args.truth, args.recent)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if 'error' in result:
            print(result['error'])
            return

        print(f"\n=== 世界观一致性检查 ===\n")
        print(f"检查章节数: {result['total_chapters']}")
        print(f"检查维度数: {result['dimensions_checked']}")
        print(f"问题总数: {result['issue_count']}")
        print(f"  错误: {result['error_count']}")
        print(f"  警告: {result['warning_count']}")

        print(f"\n各维度统计:")
        for dimension, stats in result['dimension_stats'].items():
            print(f"  {stats['name']}: {stats['total_facts']}个设定, 涉及{stats['chapters_with_facts']}章")

        if result['issues']:
            print(f"\n问题详情:")
            for issue in result['issues'][:20]:  # Show first 20 issues
                icon = '' if issue['severity'] == 'error' else '⚠'
                print(f"\n  {icon} [{issue['type']}] {issue['dimension']}")
                print(f"     {issue['message']}")
                if 'chapter' in issue:
                    print(f"     章节: 第{issue['chapter']}章 {issue.get('chapter_title', '')}")
                if 'fact' in issue:
                    print(f"     原文: {issue['fact'][:60]}...")
        else:
            print(f"\n✓ 未检测到世界观一致性问题")


if __name__ == '__main__':
    main()
