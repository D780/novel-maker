#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
章节字数检查脚本
检查中文字数是否符合项目设定的字数区间（默认2200-2800字，可自定义）
"""

import sys
from pathlib import Path

from nw_utils import count_chinese, extract_content_from_chapter


def check_chapter(file_path, min_words=2200, max_words=2800):
    path = Path(file_path)
    if not path.exists():
        return {'file': str(path), 'exists': False, 'word_count': 0, 'status': 'error', 'message': f'文件不存在: {file_path}'}
    main_content = extract_content_from_chapter(path)
    word_count = count_chinese(main_content)
    if word_count < min_words:
        status = 'short'
        message = f'字数: {word_count} (✗ 不足，需要至少 {min_words} 字)'
    elif word_count > max_words:
        status = 'long'
        message = f'字数: {word_count} (⚠ 超标，建议精简至 {max_words} 字以内)'
    else:
        status = 'pass'
        message = f'字数: {word_count} (✓ 符合区间 {min_words}-{max_words} 字)'
    return {'file': str(path), 'exists': True, 'word_count': word_count, 'status': status, 'message': message}


def check_all_chapters(directory, pattern='第*.md', min_words=2200, max_words=2800):
    dir_path = Path(directory)
    if not dir_path.exists():
        print(f'错误: 目录不存在 - {directory}')
        return []
    chapter_files = sorted(dir_path.glob(pattern))
    return [check_chapter(str(f), min_words, max_words) for f in chapter_files]


def print_results(results, min_words=2200, max_words=2800):
    if not results:
        print('没有找到章节文件')
        return
    total_words = 0
    passed = short = long = error = 0
    print('\n' + '=' * 60)
    print('章节字数检查报告')
    print(f'目标区间: {min_words}-{max_words} 字')
    print('=' * 60)
    for result in results:
        if not result['exists']:
            error += 1
            icon = '✗'
        elif result['status'] == 'pass':
            passed += 1
            icon = '✓'
            total_words += result['word_count']
        elif result['status'] == 'short':
            short += 1
            icon = '⚠'
            total_words += result['word_count']
        elif result['status'] == 'long':
            long += 1
            icon = '▲'
            total_words += result['word_count']
        else:
            error += 1
            icon = '✗'
        print(f'\n{icon} {Path(result["file"]).name}')
        print(f'   {result["message"]}')
    print('\n' + '-' * 60)
    print(f'总计: {len(results)} 章 | {passed} 达标 | {short} 不足 | {long} 超标 | 总字数: {total_words:,}')
    print('-' * 60)
    if short > 0:
        print(f'\n⚠ 有 {short} 章内容不足，可使用 /novel-weaver expand 扩充')
    if long > 0:
        print(f'\n▲ 有 {long} 章内容超标，建议精简')


def main():
    min_words = 2200
    max_words = 2800
    if len(sys.argv) < 2:
        print('用法: python check_wordcount.py <章节文件路径> [最小字数] [最大字数]')
        print('      python check_wordcount.py --all <目录路径> [最小字数] [最大字数]')
        print(f'      默认字数区间: {min_words}-{max_words}')
        return
    if sys.argv[1] == '--all':
        if len(sys.argv) < 3:
            print('错误: 使用 --all 时需要指定目录路径')
            return
        directory = sys.argv[2]
        if len(sys.argv) >= 5:
            min_words = int(sys.argv[3])
            max_words = int(sys.argv[4])
        elif len(sys.argv) == 4:
            min_words = int(sys.argv[3])
        results = check_all_chapters(directory, min_words=min_words, max_words=max_words)
        print_results(results, min_words, max_words)
    else:
        file_path = sys.argv[1]
        if len(sys.argv) >= 4:
            min_words = int(sys.argv[2])
            max_words = int(sys.argv[3])
        elif len(sys.argv) == 3:
            min_words = int(sys.argv[2])
        result = check_chapter(file_path, min_words, max_words)
        print_results([result], min_words, max_words)


if __name__ == '__main__':
    main()
