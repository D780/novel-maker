#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
场景构建辅助脚本
根据场景类型、角色、情绪目标，生成场景结构建议。
供写手在写作前快速构建场景骨架，减少构思时间。

用法:
    python scripts/writer/scene_builder.py --type 冲突 --chars 林风,苏婉 --emotion 紧张 --json
    python scripts/writer/scene_builder.py --type 日常 --chars 林风 --emotion 温馨
    python scripts/writer/scene_builder.py --list  # 列出所有场景类型
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'common'))

# ─── 场景类型模板 ───────────────────────────────
SCENE_TYPES = {
    '冲突': {
        'description': '角色间的对抗、争执或战斗',
        'structure': [
            '1. 冲突起因（导火索/积累爆发）',
            '2. 对抗升级（言语→行动→高潮）',
            '3. 转折点（意外因素/第三方介入）',
            '4. 结果（胜负/妥协/两败俱伤）',
            '5. 余波（关系变化/后续影响）'
        ],
        'tips': [
            '冲突要有层次，不要一步到位',
            '给双方合理的动机',
            '用动作和对话推动，减少内心独白',
            '结局要有意外但合理'
        ],
        'word_distribution': {'起因': '15%', '升级': '35%', '转折': '20%', '结果': '20%', '余波': '10%'}
    },
    '日常': {
        'description': '角色间的日常互动、生活场景',
        'structure': [
            '1. 场景设定（时间/地点/氛围）',
            '2. 角色互动（对话/动作/细节）',
            '3. 情感推进（关系变化/内心感受）',
            '4. 小高潮（意外/趣事/感悟）',
            '5. 收尾（自然过渡到下一场景）'
        ],
        'tips': [
            '用细节展现角色性格',
            '对话要符合角色身份',
            '适当加入环境描写烘托氛围',
            '日常中埋下后续伏笔'
        ],
        'word_distribution': {'设定': '10%', '互动': '40%', '情感': '25%', '高潮': '15%', '收尾': '10%'}
    },
    '修炼': {
        'description': '角色修炼、突破、领悟的场景',
        'structure': [
            '1. 修炼背景（为何修炼/当前瓶颈）',
            '2. 修炼过程（方法/困难/坚持）',
            '3. 突破契机（领悟/外力帮助/生死关头）',
            '4. 突破结果（实力提升/新技能）',
            '5. 后续影响（实力变化/他人反应）'
        ],
        'tips': [
            '修炼过程要有具体描写',
            '突破要有铺垫，不要突兀',
            '可以加入内心挣扎或回忆',
            '突破后要有实力展示'
        ],
        'word_distribution': {'背景': '15%', '过程': '35%', '契机': '20%', '结果': '20%', '影响': '10%'}
    },
    '揭秘': {
        'description': '揭露真相、身份或秘密的场景',
        'structure': [
            '1. 线索积累（之前的伏笔/疑点）',
            '2. 关键证据（决定性线索出现）',
            '3. 推理过程（角色分析/逻辑推导）',
            '4. 真相揭露（核心秘密公开）',
            '5. 各方反应（震惊/愤怒/释然）'
        ],
        'tips': [
            '之前要埋好伏笔',
            '揭露要有冲击力',
            '给读者"原来如此"的感觉',
            '真相要影响后续剧情'
        ],
        'word_distribution': {'线索': '20%', '证据': '20%', '推理': '25%', '揭露': '20%', '反应': '15%'}
    },
    '离别': {
        'description': '角色分离、告别或牺牲的场景',
        'structure': [
            '1. 离别原因（任务/危险/误会）',
            '2. 告别场景（对话/动作/情感）',
            '3. 内心独白（不舍/决心/回忆）',
            '4. 分离时刻（转身/远去/消失）',
            '5. 后续影响（思念/成长/重逢伏笔）'
        ],
        'tips': [
            '情感要真挚，避免矫情',
            '用细节表现不舍',
            '可以加入回忆闪回',
            '为重逢埋下伏笔'
        ],
        'word_distribution': {'原因': '15%', '告别': '30%', '独白': '20%', '分离': '20%', '影响': '15%'}
    },
    '重逢': {
        'description': '角色再次相遇的场景',
        'structure': [
            '1. 重逢背景（时间流逝/各自经历）',
            '2. 相遇瞬间（意外/期待/紧张）',
            '3. 情感碰撞（喜悦/尴尬/复杂）',
            '4. 交流互动（对话/试探/坦白）',
            '5. 关系重建（和解/疏远/新开始）'
        ],
        'tips': [
            '突出时间带来的变化',
            '情感要复杂，不要单一',
            '可以加入对比（过去vs现在）',
            '为后续发展定调'
        ],
        'word_distribution': {'背景': '15%', '相遇': '20%', '情感': '25%', '交流': '25%', '重建': '15%'}
    }
}

# ─── 情绪目标建议 ───────────────────────────────
EMOTION_TIPS = {
    '紧张': ['加快节奏', '短句为主', '多用动作描写', '减少环境描写'],
    '温馨': ['放慢节奏', '加入细节', '多用感官描写', '对话柔和'],
    '悲伤': ['节奏缓慢', '环境烘托', '内心独白', '回忆穿插'],
    '兴奋': ['快节奏', '感叹句', '动作连贯', '情绪高涨'],
    '悬疑': ['制造疑问', '信息控制', '氛围营造', '节奏起伏'],
    '愤怒': ['短句爆发', '动作激烈', '对话尖锐', '情绪递进']
}


def build_scene(scene_type, characters=None, emotion=None):
    """Build a scene structure based on type, characters, and emotion."""
    if scene_type not in SCENE_TYPES:
        return {'error': f'未知场景类型: {scene_type}。可用类型: {", ".join(SCENE_TYPES.keys())}'}

    template = SCENE_TYPES[scene_type]
    result = {
        'scene_type': scene_type,
        'description': template['description'],
        'characters': characters or [],
        'emotion_target': emotion,
        'structure': template['structure'],
        'word_distribution': template['word_distribution'],
        'tips': template['tips'].copy()
    }

    if emotion and emotion in EMOTION_TIPS:
        result['emotion_tips'] = EMOTION_TIPS[emotion]
        result['tips'].extend([f'[情绪:{emotion}] {tip}' for tip in EMOTION_TIPS[emotion]])

    return result


def list_scene_types():
    """List all available scene types."""
    return {
        'available_types': list(SCENE_TYPES.keys()),
        'types_detail': {
            name: info['description']
            for name, info in SCENE_TYPES.items()
        }
    }


def main():
    parser = argparse.ArgumentParser(description='场景构建辅助脚本')
    parser.add_argument('--type', '-t', help='场景类型')
    parser.add_argument('--chars', '-c', help='角色列表，逗号分隔')
    parser.add_argument('--emotion', '-e', help='情绪目标')
    parser.add_argument('--list', '-l', action='store_true', help='列出所有场景类型')
    parser.add_argument('--json', action='store_true', help='JSON输出')
    args = parser.parse_args()

    if args.list:
        result = list_scene_types()
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("\n=== 可用场景类型 ===\n")
            for name, desc in result['types_detail'].items():
                print(f"  {name}: {desc}")
            print(f"\n共 {len(result['available_types'])} 种场景类型")
        return

    if not args.type:
        parser.print_help()
        return

    characters = args.chars.split(',') if args.chars else []
    result = build_scene(args.type, characters, args.emotion)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if 'error' in result:
            print(result['error'])
            return

        print(f"\n=== {result['scene_type']}场景构建 ===\n")
        print(f"描述: {result['description']}")
        if result['characters']:
            print(f"角色: {', '.join(result['characters'])}")
        if result['emotion_target']:
            print(f"情绪目标: {result['emotion_target']}")

        print(f"\n场景结构:")
        for item in result['structure']:
            print(f"  {item}")

        print(f"\n字数分配建议:")
        for part, pct in result['word_distribution'].items():
            print(f"  {part}: {pct}")

        print(f"\n写作要点:")
        for tip in result['tips']:
            print(f"  • {tip}")


if __name__ == '__main__':
    main()
