#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对话质量检查脚本
检测对话中的常见问题：重复用词、AI味表达、角色声音不一致等。
供审计师在审查时使用，或写手自查。

用法:
    python scripts/auditor/dialogue_checker.py 章节文件 --json
    python scripts/auditor/dialogue_checker.py 章节文件 --verbose
"""

import argparse
import json
import os
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'common'))
from nm_utils import read_chapter, extract_characters


# ─── 对话提取 ───────────────────────────────
def extract_dialogues(text):
    """Extract all dialogues from text."""
    dialogues = []
    # 匹配 "xxx" 或 "xxx" 格式
    for m in re.finditer(r'["\u201c]([^"\u201d]+)["\u201d]', text):
        content = m.group(1).strip()
        if content:
            dialogues.append(content)
    return dialogues


# ─── 重复用词检测 ──────────────────────────────
def check_repetitive_words(dialogues, threshold=3):
    """Check for repetitive words in dialogues."""
    word_counter = Counter()
    for dialogue in dialogues:
        # 分词（简单按2-3字切分）
        words = re.findall(r'[\u4e00-\u9fff]{2,3}', dialogue)
        word_counter.update(words)

    repetitive = []
    for word, count in word_counter.most_common():
        if count >= threshold and word not in ['说道', '问道', '笑道']:
            repetitive.append({'word': word, 'count': count})

    return repetitive[:10]  # 返回前10个


# ─── AI味表达检测 ───────────────────────────────
_AI_PATTERNS = [
    (r'(?:心中|暗[自]?|心[中里])\s*(?:想|道|思忖|思虑)', '内心独白过多'),
    (r'(?:嘴角|唇角)\s*(?:勾起|上扬|微[微扬])', '嘴角勾起套路'),
    (r'(?:眼眸|眼睛)\s*(?:闪过|掠过)\s*(?:一丝|一抹)', '眼眸闪过套路'),
    (r'(?:淡淡|冷冷|微微)\s*(?:一笑|说道|道)', '副词+动词套路'),
    (r'(?:不禁|不由得)\s*(?:心中|感到)', '不禁/不由得套路'),
    (r'(?:只见|但见)', '只见/但见套路'),
    (r'(?:原来|竟然|居然)\s*(?:是|如此)', '原来/竟然套路'),
]


def check_ai_patterns(dialogues):
    """Check for AI-style patterns in dialogues."""
    issues = []
    for pattern, description in _AI_PATTERNS:
        for i, dialogue in enumerate(dialogues):
            if re.search(pattern, dialogue):
                issues.append({
                    'pattern': description,
                    'example': dialogue[:50],
                    'index': i
                })
    return issues[:10]  # 返回前10个


# ─── 对话长度分析 ───────────────────────────────
def analyze_dialogue_length(dialogues):
    """Analyze dialogue length distribution."""
    if not dialogues:
        return {'error': '未检测到对话'}

    lengths = [len(d) for d in dialogues]
    avg_length = sum(lengths) / len(lengths)

    # 统计分布
    short = sum(1 for l in lengths if l < 10)
    medium = sum(1 for l in lengths if 10 <= l < 30)
    long = sum(1 for l in lengths if 30 <= l < 60)
    very_long = sum(1 for l in lengths if l >= 60)

    return {
        'total_dialogues': len(dialogues),
        'avg_length': round(avg_length, 1),
        'distribution': {
            'short(<10字)': short,
            'medium(10-30字)': medium,
            'long(30-60字)': long,
            'very_long(>60字)': very_long
        },
        'warnings': []
    }


# ─── 主检查函数 ───────────────────────────────
def check_dialogue_quality(filepath, verbose=False):
    """Check dialogue quality in a chapter file."""
    if not os.path.exists(filepath):
        return {'error': f'文件不存在: {filepath}'}

    raw, title, clean, wc = read_chapter(filepath)
    dialogues = extract_dialogues(clean)

    result = {
        'file': os.path.basename(filepath),
        'title': title,
        'word_count': wc,
        'dialogue_count': len(dialogues),
        'dialogue_ratio': round(len(dialogues) / max(wc, 1) * 100, 1),
        'checks': {}
    }

    # 1. 重复用词检测
    repetitive = check_repetitive_words(dialogues)
    result['checks']['repetitive_words'] = {
        'count': len(repetitive),
        'items': repetitive,
        'severity': 'warning' if len(repetitive) > 3 else 'info'
    }

    # 2. AI味表达检测
    ai_patterns = check_ai_patterns(dialogues)
    result['checks']['ai_patterns'] = {
        'count': len(ai_patterns),
        'items': ai_patterns,
        'severity': 'warning' if len(ai_patterns) > 5 else 'info'
    }

    # 3. 对话长度分析
    length_analysis = analyze_dialogue_length(dialogues)
    result['checks']['length_analysis'] = length_analysis

    # 4. 总体评估
    total_issues = len(repetitive) + len(ai_patterns)
    result['overall'] = {
        'score': max(0, 100 - total_issues * 5),
        'grade': '优秀' if total_issues < 5 else '良好' if total_issues < 10 else '需改进',
        'issue_count': total_issues
    }

    if verbose:
        result['sample_dialogues'] = dialogues[:5]

    return result


def main():
    parser = argparse.ArgumentParser(description='对话质量检查脚本')
    parser.add_argument('filepath', help='章节文件路径')
    parser.add_argument('--json', action='store_true', help='JSON输出')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细信息')
    args = parser.parse_args()

    result = check_dialogue_quality(args.filepath, args.verbose)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if 'error' in result:
            print(result['error'])
            return

        print(f"\n=== 对话质量检查: {result['title']} ===\n")
        print(f"字数: {result['word_count']}")
        print(f"对话数: {result['dialogue_count']}")
        print(f"对话占比: {result['dialogue_ratio']}%")

        print(f"\n检查结果:")
        for check_name, check_result in result['checks'].items():
            count = check_result.get('count', 0)
            severity = check_result.get('severity', 'info')
            icon = '⚠' if severity == 'warning' else '✓'
            print(f"  {icon} {check_name}: {count}个问题")

        print(f"\n总体评估:")
        print(f"  得分: {result['overall']['score']}/100")
        print(f"  等级: {result['overall']['grade']}")
        print(f"  问题总数: {result['overall']['issue_count']}")


if __name__ == '__main__':
    main()
