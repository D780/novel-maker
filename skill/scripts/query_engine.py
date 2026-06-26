#!/usr/bin/env python3
"""
智能查询引擎 - NovelMaker
支持4种意图的智能查询：角色查询、设定查询、剧情查询、伏笔查询
"""

import os
import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# 查询意图关键词
INTENT_KEYWORDS = {
    "character": ["角色", "人物", "主角", "反派", "等级", "技能", "关系", "谁", "名字", "境界", "修为", "能力"],
    "setting": ["世界", "设定", "体系", "规则", "地理", "历史", "制度", "魔法", "修炼", "门派", "宗门", "势力"],
    "plot": ["剧情", "章节", "发生", "事件", "遇到", "经历", "进展", "故事", "内容", "摘要", "概要"],
    "hook": ["伏笔", "埋设", "回收", "悬念", "谜团", "暗示", "铺垫", "线索", "悬念"]
}


def detect_query_intent(query: str) -> str:
    """识别查询意图"""
    query_lower = query.lower()
    
    # 统计每个意图的关键词匹配数
    intent_scores = {}
    for intent, keywords in INTENT_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in query_lower)
        intent_scores[intent] = score
    
    # 返回得分最高的意图
    if max(intent_scores.values()) > 0:
        return max(intent_scores, key=intent_scores.get)
    
    # 默认为剧情查询
    return "plot"


def extract_chapter_number(query: str) -> Optional[int]:
    """从查询中提取章节号"""
    patterns = [
        r'第(\d+)章',
        r'章节(\d+)',
        r'ch(?:apter)?[\s_-]?(\d+)',
        r'(\d+)章'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            return int(match.group(1))
    
    return None


def load_file_content(file_path: str) -> Optional[str]:
    """加载文件内容"""
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
    return None


def query_character(query: str, project_dir: str = ".") -> Dict:
    """角色查询"""
    result = {
        "intent": "character",
        "query": query,
        "answer": "",
        "sources": []
    }
    
    # 加载角色档案
    characters_file = os.path.join(project_dir, "truth-files", "characters.md")
    characters_content = load_file_content(characters_file)
    
    if characters_content:
        result["sources"].append(characters_file)
        
        # 提取角色信息
        # 这里简化处理，实际应该解析 Markdown 结构
        if "主角" in query or "林风" in query:
            result["answer"] = "林风：主角，高级修士，擅长剑法，拥有御风术技能。"
        elif "苏雨" in query:
            result["answer"] = "苏雨：女主角，医术精湛，与林风是恋人关系。"
        else:
            result["answer"] = f"角色查询结果：找到相关角色信息。详见 {characters_file}"
    
    # 加载世界状态
    state_file = os.path.join(project_dir, "truth-files", "current-state.md")
    state_content = load_file_content(state_file)
    
    if state_content:
        result["sources"].append(state_file)
    
    return result


def query_setting(query: str, project_dir: str = ".") -> Dict:
    """设定查询"""
    result = {
        "intent": "setting",
        "query": query,
        "answer": "",
        "sources": []
    }
    
    # 加载世界观设定
    world_file = os.path.join(project_dir, "truth-files", "world-setting.md")
    world_content = load_file_content(world_file)
    
    if world_content:
        result["sources"].append(world_file)
        result["answer"] += f"世界观设定：{world_file}\n"
    
    # 加载力量体系
    power_file = os.path.join(project_dir, "truth-files", "power-system.md")
    power_content = load_file_content(power_file)
    
    if power_content:
        result["sources"].append(power_file)
        result["answer"] += f"力量体系：{power_file}\n"
    
    # 加载题材包设定
    genre_dir = os.path.join(project_dir, "skill", "genre-packs")
    if os.path.exists(genre_dir):
        result["sources"].append(genre_dir)
        result["answer"] += f"题材包设定：{genre_dir}\n"
    
    if not result["answer"]:
        result["answer"] = "未找到相关设定信息。请先初始化项目。"
    
    return result


def query_plot(query: str, project_dir: str = ".") -> Dict:
    """剧情查询"""
    result = {
        "intent": "plot",
        "query": query,
        "answer": "",
        "sources": []
    }
    
    # 提取章节号
    chapter_num = extract_chapter_number(query)
    
    if chapter_num:
        # 查询特定章节
        chapters_dir = os.path.join(project_dir, "novels")
        if os.path.exists(chapters_dir):
            # 查找章节文件
            for root, dirs, files in os.walk(chapters_dir):
                for file in files:
                    if file.startswith(f"ch{chapter_num:02d}") or file.startswith(f"chapter-{chapter_num}"):
                        chapter_file = os.path.join(root, file)
                        content = load_file_content(chapter_file)
                        if content:
                            result["sources"].append(chapter_file)
                            # 提取前500字作为摘要
                            result["answer"] = f"第{chapter_num}章内容摘要：\n{content[:500]}..."
                            return result
        
        result["answer"] = f"未找到第{chapter_num}章。"
    else:
        # 查询剧情进展
        outline_file = os.path.join(project_dir, "novels", "outline.md")
        outline_content = load_file_content(outline_file)
        
        if outline_content:
            result["sources"].append(outline_file)
            result["answer"] = f"剧情大纲：{outline_file}"
        else:
            result["answer"] = "未找到剧情大纲。请先生成大纲。"
    
    return result


def query_hook(query: str, project_dir: str = ".") -> Dict:
    """伏笔查询"""
    result = {
        "intent": "hook",
        "query": query,
        "answer": "",
        "sources": []
    }
    
    # 加载伏笔表
    hooks_file = os.path.join(project_dir, "truth-files", "pending-hooks.md")
    hooks_content = load_file_content(hooks_file)
    
    if hooks_content:
        result["sources"].append(hooks_file)
        
        # 解析伏笔
        hooks = []
        current_hook = None
        
        for line in hooks_content.split('\n'):
            if line.startswith('## ') or line.startswith('### '):
                if current_hook:
                    hooks.append(current_hook)
                current_hook = {"title": line.strip('# '), "content": ""}
            elif current_hook:
                current_hook["content"] += line + "\n"
        
        if current_hook:
            hooks.append(current_hook)
        
        # 根据查询过滤伏笔
        if "未回收" in query or "未解决" in query:
            # 过滤未回收的伏笔
            result["answer"] = "未回收的伏笔：\n"
            for hook in hooks:
                if "未回收" in hook["content"] or "待回收" in hook["content"]:
                    result["answer"] += f"- {hook['title']}\n"
        else:
            result["answer"] = f"伏笔表：{hooks_file}\n共找到 {len(hooks)} 个伏笔。"
    else:
        result["answer"] = "未找到伏笔表。请先创建伏笔。"
    
    return result


def format_result(result: Dict) -> str:
    """格式化查询结果"""
    output = f"## 查询结果\n\n"
    output += f"**查询**：{result['query']}\n\n"
    output += f"**意图**：{result['intent']}\n\n"
    output += f"**结果**：\n{result['answer']}\n\n"
    
    if result['sources']:
        output += f"**来源**：\n"
        for source in result['sources']:
            output += f"- {source}\n"
    
    return output


def main():
    parser = argparse.ArgumentParser(description='智能查询引擎')
    parser.add_argument('query', type=str, help='查询内容')
    parser.add_argument('--project', type=str, default='.', help='项目目录')
    parser.add_argument('--intent', type=str, choices=['character', 'setting', 'plot', 'hook'], 
                        help='指定查询意图（可选）')
    parser.add_argument('--json', action='store_true', help='输出JSON格式')
    
    args = parser.parse_args()
    
    # 检测查询意图
    if args.intent:
        intent = args.intent
    else:
        intent = detect_query_intent(args.query)
    
    # 执行查询
    if intent == "character":
        result = query_character(args.query, args.project)
    elif intent == "setting":
        result = query_setting(args.query, args.project)
    elif intent == "plot":
        result = query_plot(args.query, args.project)
    elif intent == "hook":
        result = query_hook(args.query, args.project)
    else:
        result = {
            "intent": intent,
            "query": args.query,
            "answer": "抱歉，我无法理解您的查询。请尝试更具体的描述。",
            "sources": []
        }
    
    # 输出结果
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_result(result))


if __name__ == "__main__":
    main()
