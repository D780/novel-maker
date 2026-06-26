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


def generate_fix_suggestions(issues, truth_facts=None):
    """Generate automatic fix suggestions for worldbuilding issues."""
    suggestions = []

    # Fix templates for each issue type
    fix_templates = {
        '设定冲突': {
            'action': '更新真相文件或修正章节内容',
            'steps': [
                '确认该设定是否为有意的新增设定',
                '如果是新设定，将其添加到对应的真相文件中',
                '如果是笔误，修正章节中的描述使其与真相文件一致'
            ]
        },
        '内部矛盾': {
            'action': '统一实体描述，消除前后矛盾',
            'steps': [
                '确定以哪个章节的描述为准（通常以首次出现为准）',
                '修正后续章节中不一致的描述',
                '将统一后的描述更新到真相文件中'
            ]
        }
    }

    for issue in issues:
        issue_type = issue['type']
        if issue_type not in fix_templates:
            continue

        template = fix_templates[issue_type]
        suggestion = {
            'type': issue_type,
            'dimension': issue.get('dimension', '未知'),
            'message': issue['message'],
            'action': template['action'],
            'steps': template['steps'],
            'severity': issue['severity']
        }

        if issue_type == '设定冲突':
            suggestion['missing_term'] = issue.get('fact', '')
            suggestion['chapter'] = issue.get('chapter', '未知')
            suggestion['fix_options'] = [
                f"将「{issue.get('fact', '')}」添加到真相文件对应维度中",
                f"修正第{issue.get('chapter', '?')}章中的描述使其与真相文件一致"
            ]

        elif issue_type == '内部矛盾':
            entity = issue.get('entity', '')
            descriptions = issue.get('descriptions', [])
            suggestion['entity'] = entity
            suggestion['conflict_count'] = len(descriptions)

            # Build specific fix based on descriptions
            if descriptions:
                first_desc = descriptions[0]
                suggestion['recommended_fix'] = (
                    f"以第{first_desc['chapter']}章的描述「{first_desc['description']}」为准，"
                    f"统一其他{len(descriptions)-1}处描述"
                )
                suggestion['conflict_details'] = [
                    {
                        'chapter': d['chapter'],
                        'description': d['description']
                    }
                    for d in descriptions
                ]

        suggestions.append(suggestion)

    return suggestions


def auto_fix_truth_files(issues, truth_dir, dry_run=True):
    """Auto-fix truth files by adding missing terms from chapters.
    
    Args:
        issues: List of detected issues
        truth_dir: Path to truth files directory
        dry_run: If True, only report what would be fixed; if False, actually modify files
    
    Returns:
        List of fix actions performed
    """
    fix_actions = []
    
    if not truth_dir or not os.path.isdir(truth_dir):
        return fix_actions
    
    # Group issues by dimension
    missing_by_dimension = defaultdict(set)
    for issue in issues:
        if issue['type'] == '设定冲突' and 'dimension' in issue:
            # Extract dimension key from display name
            dim_key = None
            for k, v in WORLDBUILDING_DIMENSIONS.items():
                if v['name'] == issue['dimension']:
                    dim_key = k
                    break
            
            if dim_key and 'fact' in issue:
                # Extract the missing term from the fact
                fact_text = issue['fact']
                # Try to extract key terms from the fact
                for group in re.findall(r'[\u4e00-\u9fa5]+', fact_text):
                    if len(group) >= 2:  # Only terms with 2+ chars
                        missing_by_dimension[dim_key].add(group)
    
    # Add missing terms to truth files
    for dim_key, terms in missing_by_dimension.items():
        truth_file = os.path.join(truth_dir, f'{dim_key}.md')
        
        if os.path.exists(truth_file):
            with open(truth_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check which terms are actually missing
            new_terms = [t for t in terms if t not in content]
            
            if new_terms:
                if not dry_run:
                    # Check if auto-fix section already exists
                    auto_fix_header = '## 自动补充设定'
                    if auto_fix_header in content:
                        # Append to existing section
                        with open(truth_file, 'a', encoding='utf-8') as f:
                            for term in sorted(new_terms):
                                f.write(f'- {term}\n')
                    else:
                        # Create new section
                        with open(truth_file, 'a', encoding='utf-8') as f:
                            f.write('\n\n## 自动补充设定\n')
                            for term in sorted(new_terms):
                                f.write(f'- {term}\n')
                
                fix_actions.append({
                    'action': '补全真相文件',
                    'dimension': WORLDBUILDING_DIMENSIONS[dim_key]['name'],
                    'file': truth_file,
                    'added_terms': sorted(new_terms),
                    'count': len(new_terms),
                    'status': '待修复（dry-run）' if dry_run else '已修复'
                })
    
    return fix_actions


def auto_fix_chapter_contradictions(issues, chapters_dir, dry_run=True):
    """Auto-fix contradictions in chapter files by standardizing entity descriptions.
    
    Args:
        issues: List of detected issues
        chapters_dir: Path to chapters directory
        dry_run: If True, only report what would be fixed; if False, actually modify files
    
    Returns:
        List of fix actions performed or proposed
    """
    fix_actions = []
    
    # Get chapter files
    chapter_files = list_chapters(chapters_dir)
    if not chapter_files:
        return fix_actions
    
    # Process internal contradictions
    for issue in issues:
        if issue['type'] != '内部矛盾':
            continue
        
        entity = issue.get('entity', '')
        descriptions = issue.get('descriptions', [])
        
        if not entity or len(descriptions) < 2:
            continue
        
        # Use first description as the canonical one
        canonical = descriptions[0]
        canonical_desc = canonical['description']
        
        # Skip if description is too short (risk of false positives)
        if len(canonical_desc) < 4:
            continue
        
        # Find chapters that need fixing
        chapters_to_fix = []
        for desc in descriptions[1:]:
            if desc['description'] != canonical_desc:
                chapters_to_fix.append({
                    'chapter': desc['chapter'],
                    'wrong_desc': desc['description'],
                    'right_desc': canonical_desc
                })
        
        if chapters_to_fix:
            fix_action = {
                'action': '修正章节矛盾',
                'entity': entity,
                'canonical_description': canonical_desc,
                'canonical_chapter': canonical['chapter'],
                'fixes': []
            }
            
            for fix_info in chapters_to_fix:
                ch_idx = fix_info['chapter'] - 1
                if 0 <= ch_idx < len(chapter_files):
                    ch_file = chapter_files[ch_idx]
                    
                    if not dry_run:
                        # Read and fix the chapter
                        with open(ch_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Use word boundary matching to avoid false replacements
                        # Only replace if the wrong description appears as a distinct phrase
                        wrong = fix_info['wrong_desc']
                        right = fix_info['right_desc']
                        
                        # Count occurrences to detect scope
                        count = content.count(wrong)
                        if count > 0 and count <= 3:  # Only fix if 1-3 occurrences
                            fixed_content = content.replace(wrong, right)
                            
                            if fixed_content != content:
                                with open(ch_file, 'w', encoding='utf-8') as f:
                                    f.write(fixed_content)
                                
                                fix_action['fixes'].append({
                                    'chapter': fix_info['chapter'],
                                    'file': ch_file,
                                    'replaced': wrong,
                                    'with': right,
                                    'occurrences': count,
                                    'status': '已修复'
                                })
                        else:
                            fix_action['fixes'].append({
                                'chapter': fix_info['chapter'],
                                'file': ch_file,
                                'replaced': wrong,
                                'with': right,
                                'occurrences': count,
                                'status': '跳过（出现次数过多，需人工确认）'
                            })
                    else:
                        fix_action['fixes'].append({
                            'chapter': fix_info['chapter'],
                            'file': ch_file,
                            'replaced': fix_info['wrong_desc'],
                            'with': fix_info['right_desc'],
                            'status': '待修复（dry-run）'
                        })
            
            if fix_action['fixes']:
                fix_actions.append(fix_action)
    
    return fix_actions


def generate_fix_report(truth_fixes, chapter_fixes, issues):
    """Generate a structured fix report for reviewer.
    
    Args:
        truth_fixes: List of truth file fix actions
        chapter_fixes: List of chapter fix actions
        issues: Original list of issues
    
    Returns:
        Dict containing structured fix report
    """
    report = {
        'summary': {
            'total_issues': len(issues),
            'truth_files_fixed': len(truth_fixes),
            'chapters_fixed': len(chapter_fixes),
            'remaining_issues': 0
        },
        'truth_file_fixes': truth_fixes,
        'chapter_fixes': chapter_fixes,
        'unfixed_issues': []
    }
    
    # Track which issues were actually fixed
    fixed_issue_indices = set()
    
    # Check truth file fixes
    for fix in truth_fixes:
        dim_name = fix.get('dimension')
        added_terms = fix.get('added_terms', [])
        for idx, issue in enumerate(issues):
            if issue['type'] == '设定冲突' and issue.get('dimension') == dim_name:
                fact_text = issue.get('fact', '')
                for term in re.findall(r'[\u4e00-\u9fa5]+', fact_text):
                    if term in added_terms:
                        fixed_issue_indices.add(idx)
                        break
    
    # Check chapter fixes
    fixed_entities = set()
    for fix in chapter_fixes:
        if 'entity' in fix:
            fixed_entities.add(fix['entity'])
    
    for idx, issue in enumerate(issues):
        if issue['type'] == '内部矛盾' and issue.get('entity') in fixed_entities:
            fixed_issue_indices.add(idx)
    
    # Calculate remaining issues
    report['summary']['remaining_issues'] = len(issues) - len(fixed_issue_indices)
    
    # Collect unfixed issues
    for idx, issue in enumerate(issues):
        if idx not in fixed_issue_indices:
            report['unfixed_issues'].append(issue)
    
    return report


def main():
    parser = argparse.ArgumentParser(description='世界观一致性检查脚本')
    parser.add_argument('chapters_dir', help='章节目录路径')
    parser.add_argument('--truth', '-t', help='真相文件目录路径')
    parser.add_argument('--recent', type=int, help='仅检查最近N章')
    parser.add_argument('--json', action='store_true', help='JSON输出')
    parser.add_argument('--fix', action='store_true', help='显示自动修复建议')
    parser.add_argument('--apply', action='store_true', help='应用自动修复（需配合--truth）')
    parser.add_argument('--dry-run', action='store_true', help='仅预览修复内容，不实际修改文件')
    args = parser.parse_args()

    if not os.path.isdir(args.chapters_dir):
        print(f"错误: 目录不存在: {args.chapters_dir}", file=sys.stderr)
        sys.exit(1)

    result = check_worldbuilding_consistency(args.chapters_dir, args.truth, args.recent)

    # Generate fix suggestions if requested
    if args.fix and result.get('issues'):
        result['fix_suggestions'] = generate_fix_suggestions(result['issues'])

    # Apply auto-fix if requested
    if args.apply and result.get('issues'):
        if not args.truth:
            print("错误: --apply 需要配合 --truth 参数使用", file=sys.stderr)
            sys.exit(1)
        
        # Load truth facts for reference
        truth_facts = {}
        if os.path.isdir(args.truth):
            for dimension in WORLDBUILDING_DIMENSIONS.keys():
                truth_file = os.path.join(args.truth, f'{dimension}.md')
                if os.path.exists(truth_file):
                    with open(truth_file, 'r', encoding='utf-8') as f:
                        truth_facts[dimension] = f.read()
        
        # Auto-fix truth files
        dry_run = args.dry_run
        truth_fixes = auto_fix_truth_files(result['issues'], args.truth, dry_run=dry_run)
        
        # Auto-fix chapter contradictions
        chapter_fixes = auto_fix_chapter_contradictions(result['issues'], args.chapters_dir, dry_run=dry_run)
        
        # Generate fix report
        fix_report = generate_fix_report(truth_fixes, chapter_fixes, result['issues'])
        
        result['fix_report'] = fix_report

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

            # Show fix suggestions if requested
            if args.fix and result.get('fix_suggestions'):
                print(f"\n{'='*60}")
                print(f"自动修复建议:")
                print(f"{'='*60}")
                for i, suggestion in enumerate(result['fix_suggestions'], 1):
                    print(f"\n  [{i}] {suggestion['type']} - {suggestion['dimension']}")
                    print(f"     问题: {suggestion['message']}")
                    print(f"     操作: {suggestion['action']}")
                    for j, step in enumerate(suggestion['steps'], 1):
                        print(f"       {j}. {step}")

                    if 'fix_options' in suggestion:
                        print(f"     修复选项:")
                        for opt in suggestion['fix_options']:
                            print(f"       - {opt}")

                    if 'recommended_fix' in suggestion:
                        print(f"     推荐修复: {suggestion['recommended_fix']}")
                        if 'conflict_details' in suggestion:
                            print(f"     冲突详情:")
                            for detail in suggestion['conflict_details']:
                                print(f"       第{detail['chapter']}章: {detail['description']}")
            
            # Show fix report if applied
            if args.apply and result.get('fix_report'):
                report = result['fix_report']
                print(f"\n{'='*60}")
                print(f"自动修复报告:")
                print(f"{'='*60}")
                print(f"\n修复统计:")
                print(f"  总问题数: {report['summary']['total_issues']}")
                print(f"  真相文件修复: {report['summary']['truth_files_fixed']}")
                print(f"  章节修复: {report['summary']['chapters_fixed']}")
                print(f"  剩余问题: {report['summary']['remaining_issues']}")
                
                if report['truth_file_fixes']:
                    print(f"\n真相文件修复详情:")
                    for fix in report['truth_file_fixes']:
                        status = fix.get('status', '已修复')
                        status_icon = '✓' if '已修复' in status else '○'
                        print(f"  {status_icon} [{fix['dimension']}] 补全 {fix['count']} 个设定")
                        for term in fix['added_terms']:
                            print(f"      - {term}")
                
                if report['chapter_fixes']:
                    print(f"\n章节修复详情:")
                    for fix in report['chapter_fixes']:
                        print(f"  [{fix['entity']}] 以第{fix['canonical_chapter']}章为准")
                        for ch_fix in fix['fixes']:
                            status_icon = '✓' if '已修复' in ch_fix['status'] else '○'
                            print(f"    {status_icon} 第{ch_fix['chapter']}章: {ch_fix['replaced']} → {ch_fix['with']}")
                
                if report['unfixed_issues']:
                    print(f"\n未修复问题（需人工处理）:")
                    for issue in report['unfixed_issues'][:10]:
                        print(f"  - [{issue['type']}] {issue['message']}")
        else:
            print(f"\n✓ 未检测到世界观一致性问题")


if __name__ == '__main__':
    main()
