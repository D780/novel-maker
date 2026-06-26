#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
预审计管线 — 一键运行所有可自动化的审计维度

将审计师需要手动执行的 5 个检查脚本整合为一个命令，
输出结构化 JSON，审计师只需读取结果做 AI 判断，无需读取全文。

用法:
    python scripts/pre_audit.py novels/volume-01/chapters/ch15.md
    python scripts/pre_audit.py novels/volume-01/chapters/ch15.md --json
"""

import argparse
import json
import os
import sys
import subprocess

sys.path.insert(0, os.path.dirname(__file__))
from nw_utils import (
    read_chapter, extract_characters, detect_hook,
    detect_structure, estimate_pacing,
    clean_markdown, generate_summary
)


def _run_script(script_name, args_list):
    """运行子脚本并返回结果"""
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    if not os.path.exists(script_path):
        return {'error': f'{script_name} 不存在'}
    try:
        result = subprocess.run(
            [sys.executable, script_path] + args_list,
            capture_output=True, text=True, encoding='utf-8', timeout=30
        )
        if result.returncode == 0:
            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError:
                return {'output': result.stdout.strip()}
        else:
            return {'error': result.stderr.strip() or f'{script_name} 返回码 {result.returncode}'}
    except subprocess.TimeoutExpired:
        return {'error': f'{script_name} 执行超时'}
    except Exception as e:
        return {'error': str(e)}


def _check_wordcount(chapter_path, min_words=2000, max_words=4000):
    """字数检查"""
    raw, title, clean, wc = read_chapter(chapter_path)
    status = 'OK'
    if wc < min_words:
        status = f'不足（{wc}<{min_words}）'
    elif wc > max_words:
        status = f'超标（{wc}>{max_words}）'
    return {'word_count': wc, 'min': min_words, 'max': max_words, 'status': status}


def _check_hook(chapter_path):
    """章末钩子检查"""
    with open(chapter_path, encoding='utf-8') as f:
        text = f.read()
    hook = detect_hook(text)
    has_hook = hook['type'] not in ('未检测', '未知')
    return {
        'has_hook': has_hook,
        'hook_type': hook['type'],
        'cues': hook.get('cues', {}),
        'tail_preview': hook.get('tail_preview', '')
    }


def _check_pacing(chapter_path):
    """节奏评估"""
    with open(chapter_path, encoding='utf-8') as f:
        text = f.read()
    pacing_label, pacing_score = estimate_pacing(text)
    structure = detect_structure(text)
    return {
        'pacing': pacing_label,
        'pacing_score': pacing_score,
        'structure': structure
    }


def _check_ai_style(chapter_path):
    """AI味检测（调用 style_check.py）"""
    return _run_script('style_check.py', [chapter_path, '--json'])


def _check_consistency(chapter_path, truth_dir=None):
    """一致性扫描（调用 consistency_scan.py）"""
    args = [chapter_path]
    if truth_dir:
        args.extend(['--truth-dir', truth_dir])
    args.append('--json')
    return _run_script('consistency_scan.py', args)


def _check_characters(chapter_path):
    """角色提取"""
    with open(chapter_path, encoding='utf-8') as f:
        text = f.read()
    clean = clean_markdown(text)
    chars = extract_characters(clean)
    return {'characters': chars, 'count': len(chars)}


def _check_summary(chapter_path):
    """章节摘要"""
    with open(chapter_path, encoding='utf-8') as f:
        text = f.read()
    summary = generate_summary(text, first_n=150, last_n=150)
    return summary


def run_pre_audit(chapter_path, truth_dir=None, min_words=2000, max_words=4000):
    """运行完整预审计管线"""
    if not os.path.exists(chapter_path):
        return {'error': f'章节文件不存在: {chapter_path}'}

    results = {
        'chapter': os.path.basename(chapter_path),
        'checks': {}
    }

    # 1. 字数检查
    results['checks']['word_count'] = _check_wordcount(chapter_path, min_words, max_words)

    # 2. 角色提取
    results['checks']['characters'] = _check_characters(chapter_path)

    # 3. 章末钩子
    results['checks']['hook'] = _check_hook(chapter_path)

    # 4. 节奏评估
    results['checks']['pacing'] = _check_pacing(chapter_path)

    # 5. 章节摘要
    results['checks']['summary'] = _check_summary(chapter_path)

    # 6. AI味检测
    results['checks']['ai_style'] = _check_ai_style(chapter_path)

    # 7. 一致性扫描（可选）
    if truth_dir:
        results['checks']['consistency'] = _check_consistency(chapter_path, truth_dir)

    # 汇总
    issues = []
    wc = results['checks']['word_count']
    if wc['status'] != 'OK':
        issues.append(f"字数: {wc['status']}")
    if not results['checks']['hook']['has_hook']:
        issues.append("章末无钩子")
    if results['checks']['pacing']['pacing_score'] >= 4:
        issues.append(f"节奏偏高: {results['checks']['pacing']['pacing']}")

    results['summary'] = {
        'total_checks': len(results['checks']),
        'issues': issues,
        'issue_count': len(issues)
    }

    return results


def main():
    parser = argparse.ArgumentParser(description='预审计管线')
    parser.add_argument('chapter', help='章节文件路径')
    parser.add_argument('--truth-dir', help='真相文件目录')
    parser.add_argument('--min-words', type=int, default=2000, help='最少字数（默认2000）')
    parser.add_argument('--max-words', type=int, default=4000, help='最多字数（默认4000）')
    parser.add_argument('--json', action='store_true', help='JSON输出')
    args = parser.parse_args()

    results = run_pre_audit(args.chapter, args.truth_dir, args.min_words, args.max_words)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        if 'error' in results:
            print(f"错误: {results['error']}")
            return
        print(f"=== 预审计报告: {results['chapter']} ===\n")
        for name, check in results['checks'].items():
            if isinstance(check, dict) and 'error' not in check:
                print(f"✓ {name}: OK")
            elif isinstance(check, dict) and 'error' in check:
                print(f"✗ {name}: {check['error']}")
        if results['summary']['issues']:
            print(f"\n发现 {results['summary']['issue_count']} 个问题:")
            for issue in results['summary']['issues']:
                print(f"  - {issue}")
        else:
            print("\n全部通过!")


if __name__ == '__main__':
    main()
