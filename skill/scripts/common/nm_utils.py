#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NovelMaker 脚本公共工具模块
提供所有脚本共用的函数，消除重复代码。
"""

import os
import re
import sys
import json
from collections import Counter

# ─── 字符编码兼容 ───────────────────────────────
if sys.platform == 'win32':
    import io
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'buffer'):
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# ─── Markdown 清理 ───────────────────────────────
_MARKDOWN_PATTERNS = [
    (r'#{1,6}\s*', ''),
    (r'\*\*(.*?)\*\*', r'\1'),
    (r'\*(.*?)\*', r'\1'),
    (r'~~(.*?)~~', r'\1'),
    (r'`(.*?)`', r'\1'),
    (r'\[(.*?)\]\(.*?\)', r'\1'),
    (r'>\s?', ''),
    (r'-{3,}', ''),
    (r'\*{3,}', ''),
]


def clean_markdown(text):
    """Remove markdown formatting from text."""
    for pattern, repl in _MARKDOWN_PATTERNS:
        text = re.sub(pattern, repl, text)
    return text


def count_chinese(text):
    """Count Chinese characters in text."""
    return len(re.findall(r'[\u4e00-\u9fff]', text))


def extract_title(content):
    """Extract chapter title from markdown heading."""
    m = re.search(r'^#\s*(.+)$', content, re.MULTILINE)
    return m.group(1).strip() if m else None


def read_chapter(filepath):
    """Read a chapter file and return (raw_text, title, clean_text, word_count)."""
    with open(filepath, 'r', encoding='utf-8') as f:
        raw = f.read()
    title = extract_title(raw)
    clean = clean_markdown(raw)
    wc = count_chinese(clean)
    return raw, title, clean, wc


def extract_content_from_chapter(file_path):
    """Extract body content after the chapter heading line."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    lines = content.split('\n')
    content_start = 0
    for i, line in enumerate(lines):
        if line.startswith('#') and '章' in line:
            content_start = i + 1
            break
    return '\n'.join(lines[content_start:])


# ─── 角色提取 ───────────────────────────────
_STOP_PREFIXES = ('他', '她', '我', '你', '它', '这', '那', '一', '几', '每', '各', '有', '是', '不', '又', '也', '就', '便', '被', '把', '向', '对', '从', '跟', '将', '让', '却', '只')
_STOP_SUFFIXES = ('道', '说', '问', '笑', '喊', '怒', '叫', '哭', '叹', '喃', '咕', '叨', '呼', '喝')
_STOP_WORDS = {
    '说道', '问道', '喊道', '笑道', '怒道', '冷冷道', '淡淡道', '低声道', '大声道',
    '心中', '忽然', '这个时候', '就在这', '只听得', '眼看', '原来',
    '可以', '没有', '已经', '这个', '那个', '什么', '怎么', '为什么',
    '如果', '因为', '所以', '但是', '而且', '然后', '虽然', '不过',
    '只是', '还是', '或者', '一定', '可能', '应该', '必须', '能够',
    '他们', '自己', '我们', '你们', '这些', '那些', '所有', '每个',
    '现在', '刚才', '以前', '以后', '之前', '之后', '一直', '终于',
    '看着', '听到', '发现', '感觉', '觉得', '知道', '想到', '看到',
    '继续', '开始', '已经', '准备', '打算', '决定', '选择', '同意',
    '掌门', '宗主', '长老', '堂主', '舵主',
    '摆了摆手', '点了点头', '摇了摇头', '挥了挥手', '拱了拱手',
    '老者淡淡', '少年笑', '中年笑', '大汉道', '老妪道', '少妇道',
}
_GENERIC_TITLES = ('老者', '少年', '中年', '大汉', '老妪', '少妇', '壮汉', '妇人', '男子', '女子')


def extract_characters(text):
    """Extract character names from dialogue patterns, filtering noise."""
    candidates = set()
    for m in re.finditer(r'([\u4e00-\u9fff]{2,4})(?:说道|问道|喊道|笑道|怒道|冷冷道|淡淡道|低声道|大声道|心想|暗道|思忖|暗想|心说)', text):
        candidates.add(m.group(1))
    for m in re.finditer(r'([\u4e00-\u9fff]{2,4})[：:]["\u201c]', text):
        candidates.add(m.group(1))
    for m in re.finditer(r'["\u201d]([\u4e00-\u9fff]{2,4})[说问道喊笑怒冷淡淡低大]', text):
        candidates.add(m.group(1))

    filtered = []
    for c in sorted(candidates):
        if c in _STOP_WORDS:
            continue
        if c.startswith(_STOP_PREFIXES):
            continue
        if c.endswith(_STOP_SUFFIXES) and len(c) <= 3:
            continue
        if len(c) >= 4 and re.search(r'[了的得地着过]', c[1:-1]):
            continue
        if any(c.startswith(t) for t in _GENERIC_TITLES):
            continue
        filtered.append(c)
    return filtered


def extract_locations(text):
    """Extract location names from movement/position patterns."""
    locs = set()
    for m in re.finditer(r'(?:在|到|去|进入|来到|回到)([\u4e00-\u9fff]{2,6})(?:中|里|内|外|前|后|上|下|边|旁)?(?:[，。！？\s]|$)', text):
        locs.add(m.group(1))
    return sorted(locs)[:10]


# ─── 钩子检测 ───────────────────────────────
_HOOK_CUES = {
    '揭示': ['原来', '竟然是', '才发现', '终于明白', '真相', '秘密', '身份'],
    '危机': ['突然', '忽然', '就在这时', '猛地', '危险', '不好', '糟糕', '惊变', '杀意'],
    '选择': ['怎么办', '选哪', '两难', '不得', '必须', '只能', '要么', '是否'],
    '期待': ['下次', '明天', '等着', '一定', '会回来', '再来', '不会放'],
    '反转': ['没想到', '不料', '却', '反而', '居然', '竟'],
    '悬念': ['到底', '究竟', '为什么', '怎么', '是否', '会不会', '难道'],
}

_HOOK_PATTERN_MAP = {
    "揭示": re.compile(r'(原来|竟然|居然|没想到|真相|秘密|隐藏|真相大白|揭露)'),
    "危机": re.compile(r'(危险|危机|追杀|暗杀|陷阱|包围|生死|命悬一线|千钧一发)'),
    "选择": re.compile(r'(选择|决定|犹豫|两难|何去何从|必须做出)'),
    "期待": re.compile(r'(明天|明天就|明天开始|等着|等着我|三天后|约定|届时)'),
    "反转": re.compile(r'(但是|然而|却|没想到|谁知|岂料|不料|偏偏|可是)'),
    "悬念": re.compile(r'(他不知道|她没看到|没有人知道|神秘|未知|谜团|未解|尚未)'),
}


def detect_hook(text, last_n=400):
    """Detect chapter ending hook type from text tail."""
    tail = ''.join(re.findall(r'[\u4e00-\u9fff，。！？、：""\u201c\u201d\u2026\uff01\uff1f]', text[-last_n:]))
    found = {}
    for ctype, keywords in _HOOK_CUES.items():
        score = sum(1 for kw in keywords if kw in tail)
        if score:
            found[ctype] = score
    best = max(found, key=found.get) if found else '未检测'
    return {'type': best, 'cues': found, 'tail_preview': tail[-80:] if tail else ''}


def detect_hook_type_from_patterns(text):
    """Detect hook type using compiled regex patterns (for batch scanning)."""
    scores = {}
    for hook_type, pattern in _HOOK_PATTERN_MAP.items():
        scores[hook_type] = len(pattern.findall(text))
    if not scores or max(scores.values()) == 0:
        return "未知"
    return max(scores, key=scores.get)


# ─── 章节排序 ───────────────────────────────
_CHAPTER_PATTERN = re.compile(r'第([零一二三四五六七八九十百\d]+)章.*\.md$')
_CN_MAP = {'零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
           '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10}


def chapter_sort_key(filepath):
    """Sort key for chapter filenames (handles Chinese numerals)."""
    m = _CHAPTER_PATTERN.search(os.path.basename(filepath))
    if m:
        num_str = m.group(1)
        if num_str.isdigit():
            return int(num_str)
        val = 0
        for ch in num_str:
            val = val * 10 + _CN_MAP.get(ch, 0)
        return val
    return 9999


def list_chapters(chapters_dir, recent_n=None):
    """List chapter files in a directory, sorted by chapter number."""
    if not os.path.isdir(chapters_dir):
        return []
    files = [os.path.join(chapters_dir, f) for f in os.listdir(chapters_dir)
             if _CHAPTER_PATTERN.search(f)]
    files.sort(key=chapter_sort_key)
    if recent_n:
        files = files[-recent_n:]
    return files


# ─── 摘要生成 ───────────────────────────────
def generate_summary(text, first_n=150, last_n=200):
    """Generate head/tail summary from chapter text."""
    clean = clean_markdown(text)
    chinese_only = ''.join(re.findall(r'[\u4e00-\u9fff，。！？、：""\u201c\u201d]', clean))
    head = chinese_only[:first_n]
    tail = chinese_only[-last_n:] if len(chinese_only) > last_n else chinese_only[first_n:]
    return {'开头': head, '结尾': tail}


# ─── 结构检测 ───────────────────────────────
def detect_structure(text):
    """Detect chapter structure: dialogue/action/description ratios."""
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    dialogue_lines = sum(1 for l in lines if re.search(r'["\u201c\u201d]|[\u300c\u300d]|[：:][\u201c]', l))
    action_keywords = ['打', '砍', '刺', '踢', '冲', '跑', '跳', '飞', '击', '轰', '斩', '劈', '砸', '撞']
    description_keywords = ['阳光', '月光', '山', '水', '云', '风', '雨', '雪', '花', '树', '雾', '光', '影',
                            '宫殿', '阁楼', '庭院', '房间', '大厅', '森林', '沙漠', '河流', '山谷']
    action_count = sum(1 for l in lines if any(kw in l for kw in action_keywords))
    desc_count = sum(1 for l in lines if any(kw in l for kw in description_keywords))
    total = len(lines)
    return {
        'dialogue_pct': round(dialogue_lines / total * 100, 1) if total else 0,
        'action_pct': round(action_count / total * 100, 1) if total else 0,
        'description_pct': round(desc_count / total * 100, 1) if total else 0,
        'total_paragraphs': total
    }


# ─── 节奏评级 ───────────────────────────────
_HIGHEST_INTENSITY_KEYWORDS = ['生死', '对决', '终极', '决战', '毁灭', '崩塌', '同归于尽', '最后一击']
_HIGH_INTENSITY_KEYWORDS = ['战斗', '突破', '打脸', '击杀', '轰杀', '爆发', '碾压', '秒杀']
_MID_INTENSITY_KEYWORDS = ['准备', '计划', '修炼', '提升', '领悟', '探索']
_LOW_INTENSITY_KEYWORDS = ['日常', '对话', '闲聊', '休息', '散步', '喝茶']


def estimate_pacing(text):
    """Estimate chapter pacing level S1-S5 based on content keywords."""
    clean = clean_markdown(text)
    lines = [l.strip() for l in clean.split('\n') if l.strip()]
    total = max(len(lines), 1)
    highest = sum(1 for l in lines if any(kw in l for kw in _HIGHEST_INTENSITY_KEYWORDS))
    high = sum(1 for l in lines if any(kw in l for kw in _HIGH_INTENSITY_KEYWORDS))
    mid = sum(1 for l in lines if any(kw in l for kw in _MID_INTENSITY_KEYWORDS))
    low = sum(1 for l in lines if any(kw in l for kw in _LOW_INTENSITY_KEYWORDS))
    score = highest * 5 + high * 4 + mid * 3 + low * 1
    avg = score / total
    if avg >= 2.5:
        return 'S5', 5
    elif avg >= 1.8:
        return 'S4', 4
    elif avg >= 1.2:
        return 'S3', 3
    elif avg >= 0.6:
        return 'S2', 2
    else:
        return 'S1', 1


# ─── Markdown 大纲解析 ───────────────────────────────
def parse_outline_headings(text, max_level=4):
    """Parse markdown outline into a tree of headings."""
    tree = []
    for line in text.split('\n'):
        m = re.match(r'^(#{1,' + str(max_level) + r'})\s+(.+)', line)
        if m:
            level = len(m.group(1))
            title = m.group(2).strip()
            tree.append({'level': level, 'title': title})
    return tree


# ─── Truth文件读取 ───────────────────────────────
def read_truth_section(filepath):
    """Read a truth file and return structured sections."""
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    sections = {}
    current_section = 'header'
    sections[current_section] = []
    for line in text.split('\n'):
        if line.startswith('## '):
            current_section = line[3:].strip()
            sections[current_section] = []
        elif line.startswith('# '):
            current_section = line[2:].strip()
            sections[current_section] = []
        else:
            sections[current_section].append(line)
    return {k: '\n'.join(v).strip() for k, v in sections.items() if v}
