#!/usr/bin/env python3
"""
NovelWeaver 交互式引导脚本

使用方式：
    python scripts/init_guide.py [--ide trae|claude] [--auto] [--verify]

参数说明：
    --ide: 指定IDE类型（trae 或 claude）
    --auto: 自动模式，使用默认配置
    --verify: 验证安装是否成功
"""

import os
import sys
import json
import argparse
from pathlib import Path


# 情绪标签选项
EMOTION_LABELS = {
    "A": {"name": "打脸爽文", "desc": "扮猪吃虎、逆袭碾压", "interval": "≤3章"},
    "B": {"name": "极致虐恋", "desc": "追妻火葬场", "interval": "5-8章"},
    "C": {"name": "爆笑反套路", "desc": "沙雕吐槽、神转折", "interval": "3-5章"},
    "D": {"name": "悬疑惊悚", "desc": "细思极恐、烧脑", "interval": "5-8章"},
    "E": {"name": "治愈甜宠", "desc": "日常温馨、双向奔赴", "interval": "3-5章"},
    "F": {"name": "脑洞大开", "desc": "系统流、末日囤货", "interval": "5-10章"},
}

# 文风推荐
STYLE_RECOMMENDATIONS = {
    "玄幻修仙": ["天蚕土豆", "辰东"],
    "都市搞笑": ["弈青峰", "会说话的肘子"],
    "仙侠探案": ["卖报小郎君"],
    "悬疑诡秘": ["爱潜水的乌贼"],
    "历史权谋": ["猫腻", "愤怒的香蕉"],
    "凡人流": ["忘语", "言归正传"],
    "电竞网游": ["蝴蝶蓝"],
    "无限流": ["三天两觉", "杀虫队队员"],
    "盗墓探险": ["天下霸唱"],
    "极道诡异": ["滚开"],
    "稳健搞笑": ["言归正传"],
    "多神话热血": ["三九音域"],
    "悬疑推理": ["杀虫队队员"],
}


def print_banner():
    """打印欢迎横幅"""
    print("\n" + "=" * 60)
    print("  NovelWeaver v2.0.0 - 全能网文写作助手")
    print("  6角色协作架构，用说话的方式写小说")
    print("=" * 60 + "\n")


def detect_environment():
    """检测当前环境"""
    print("🔍 检测环境...\n")

    # 检查是否在正确的目录
    cwd = Path.cwd()
    skill_dir = cwd / "skill"
    if not skill_dir.exists():
        print("❌ 错误：当前目录下未找到 skill/ 目录")
        print("   请确保在 NovelWeaver 仓库根目录下运行此脚本")
        return False

    # 检查 SKILL.md 是否存在
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        print("❌ 错误：skill/SKILL.md 不存在")
        print("   请确保技能文件完整")
        return False

    print("✅ 环境检测通过")
    print(f"   当前目录：{cwd}")
    print(f"   技能目录：{skill_dir}")
    print()

    return True


def detect_ide():
    """检测IDE类型"""
    print("🔍 检测IDE类型...\n")

    # 检查 .trae 目录
    if Path(".trae").exists():
        print("✅ 检测到 Trae IDE")
        return "trae"

    # 检查 .claude 目录
    if Path(".claude").exists():
        print("✅ 检测到 Claude Code")
        return "claude"

    print("⚠️  未检测到IDE类型，请手动指定")
    return None


def select_emotion_label():
    """选择情绪标签"""
    print("\n📋 第一步：选择情绪标签\n")
    print("请选择你想要的核心情绪体验：\n")

    for key, value in EMOTION_LABELS.items():
        print(f"  {key}. {value['name']} - {value['desc']}")

    print()

    while True:
        choice = input("请输入选项字母 (A-F): ").strip().upper()
        if choice in EMOTION_LABELS:
            selected = EMOTION_LABELS[choice]
            print(f"\n✅ 已选择：{selected['name']}")
            print(f"   说明：{selected['desc']}")
            print(f"   爽点间隔：{selected['interval']}")
            return selected
        else:
            print("❌ 无效选项，请重新输入")


def input_book_info():
    """输入书籍信息"""
    print("\n📋 第二步：填写书籍信息\n")

    book_name = input("书名（如：废材逆天记）: ").strip()
    genre = input("题材（如：玄幻修仙、都市搞笑）: ").strip()
    synopsis = input("一句话简介（如：废材逆袭成仙帝）: ").strip()

    print(f"\n✅ 书籍信息：")
    print(f"   书名：{book_name}")
    print(f"   题材：{genre}")
    print(f"   简介：{synopsis}")

    return {
        "book_name": book_name,
        "genre": genre,
        "synopsis": synopsis,
    }


def input_protagonist():
    """输入主角信息"""
    print("\n📋 第三步：设置主角信息\n")

    name = input("主角姓名（如：林轩）: ").strip()
    contrast = input("核心反差点（如：表面废物实际天才）: ").strip()
    goal = input("核心目标（如：成为仙帝）: ").strip()

    print(f"\n✅ 主角信息：")
    print(f"   姓名：{name}")
    print(f"   反差点：{contrast}")
    print(f"   目标：{goal}")

    return {
        "name": name,
        "contrast": contrast,
        "goal": goal,
    }


def input_conflict():
    """输入核心冲突"""
    print("\n📋 第四步：确定核心冲突\n")

    conflict = input("核心冲突（如：与宗门天才的宿命对决）: ").strip()

    print(f"\n✅ 核心冲突：{conflict}")

    return conflict


def input_chapters():
    """输入章节数"""
    print("\n📋 第五步：设定章节数\n")

    while True:
        try:
            chapters = int(input("目标章节数（如：100）: ").strip())
            if chapters > 0:
                print(f"\n✅ 目标章节数：{chapters}章")
                return chapters
            else:
                print("❌ 章节数必须大于0")
        except ValueError:
            print("❌ 请输入有效的数字")


def select_style(genre):
    """选择文风"""
    print("\n📋 第六步：选择文风\n")

    # 根据题材推荐文风
    recommendations = STYLE_RECOMMENDATIONS.get(genre, [])
    if recommendations:
        print(f"根据题材「{genre}」，推荐以下文风：")
        for i, style in enumerate(recommendations, 1):
            print(f"  {i}. {style}")
        print()

    print("可选文风：")
    styles = [
        "天蚕土豆", "辰东", "弈青峰", "会说话的肘子", "卖报小郎君",
        "爱潜水的乌贼", "猫腻", "愤怒的香蕉", "忘语", "言归正传",
        "蝴蝶蓝", "三天两觉", "杀虫队队员", "天下霸唱", "滚开", "三九音域"
    ]
    for i, style in enumerate(styles, 1):
        print(f"  {i}. {style}")

    print()

    while True:
        choice = input("请输入文风名称或序号: ").strip()

        # 检查是否是序号
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(styles):
                selected = styles[idx]
                print(f"\n✅ 已选择文风：{selected}")
                return selected
        except ValueError:
            pass

        # 检查是否是文风名称
        if choice in styles:
            print(f"\n✅ 已选择文风：{choice}")
            return choice

        print("❌ 无效选项，请重新输入")


def confirm_config(config):
    """确认配置"""
    print("\n" + "=" * 60)
    print("  配置摘要")
    print("=" * 60 + "\n")

    print(f"  情绪标签：{config['emotion_label']['name']}")
    print(f"  书名：{config['book_name']}")
    print(f"  题材：{config['genre']}")
    print(f"  简介：{config['synopsis']}")
    print(f"  主角：{config['protagonist']['name']}")
    print(f"  反差点：{config['protagonist']['contrast']}")
    print(f"  目标：{config['protagonist']['goal']}")
    print(f"  核心冲突：{config['conflict']}")
    print(f"  章节数：{config['chapters']}章")
    print(f"  文风：{config['style']}")
    print()

    while True:
        choice = input("确认配置？(y/n): ").strip().lower()
        if choice in ["y", "yes", "是", "确认"]:
            return True
        elif choice in ["n", "no", "否", "取消"]:
            return False
        else:
            print("❌ 请输入 y 或 n")


def generate_config_files(config):
    """生成配置文件"""
    print("\n📁 生成配置文件...\n")

    # 创建 .novel-weaver 目录
    novel_weaver_dir = Path(".novel-weaver")
    novel_weaver_dir.mkdir(exist_ok=True)

    # 创建 truth-files 目录
    truth_files_dir = novel_weaver_dir / "truth-files"
    truth_files_dir.mkdir(exist_ok=True)

    # 创建 memory 目录
    memory_dir = novel_weaver_dir / "memory"
    memory_dir.mkdir(exist_ok=True)

    # 创建 novels 目录
    novels_dir = Path("novels")
    novels_dir.mkdir(exist_ok=True)

    # 生成 constitution.md
    constitution_content = f"""# 创作宪法

## 基本信息

- **书名**：{config['book_name']}
- **题材**：{config['genre']}
- **情绪标签**：{config['emotion_label']['name']}
- **文风**：{config['style']}
- **目标章节数**：{config['chapters']}章

## 一句话简介

{config['synopsis']}

## 主角设定

- **姓名**：{config['protagonist']['name']}
- **核心反差点**：{config['protagonist']['contrast']}
- **核心目标**：{config['protagonist']['goal']}

## 核心冲突

{config['conflict']}

## 写作约束

- 字数范围：2500-3500字/章
- 平台适配：默认
- 节奏控制：S1-S5五级评级
- 质量审计：15维度核心审计

## 情绪标签规则

- **爽点间隔**：{config['emotion_label']['interval']}
- **节奏要求**：根据情绪标签自动调整
"""
    constitution_path = memory_dir / "constitution.md"
    constitution_path.write_text(constitution_content, encoding="utf-8")

    # 生成 characters.md
    characters_content = f"""# 角色档案

## 主角

### {config['protagonist']['name']}

- **核心反差点**：{config['protagonist']['contrast']}
- **核心目标**：{config['protagonist']['goal']}
- **当前状态**：初始状态
- **能力等级**：待设定
- **性格特点**：待设定

## 配角

（待添加）

## 反派

（待添加）
"""
    characters_path = truth_files_dir / "characters.md"
    characters_path.write_text(characters_content, encoding="utf-8")

    # 生成 current-state.md
    current_state_content = f"""# 世界状态

## 当前时间

- **卷**：第1卷
- **章**：第0章
- **幕**：第1幕

## 主角状态

- **姓名**：{config['protagonist']['name']}
- **位置**：待设定
- **状态**：初始状态

## 世界状态

（待更新）
"""
    current_state_path = truth_files_dir / "current-state.md"
    current_state_path.write_text(current_state_content, encoding="utf-8")

    # 生成 world-setting.md
    world_setting_content = f"""# 世界观设定

## 世界背景

（待设定）

## 力量体系

（待设定）

## 势力分布

（待设定）

## 地理环境

（待设定）
"""
    world_setting_path = truth_files_dir / "world-setting.md"
    world_setting_path.write_text(world_setting_content, encoding="utf-8")

    # 生成 pending-hooks.md
    pending_hooks_content = """# 伏笔表

## 待回收伏笔

| ID | 伏笔内容 | 埋设章节 | 状态 | 优先级 |
|----|---------|---------|------|--------|
| H001 | （示例）主角隐藏血脉 | 第1章 | 待回收 | 高 |

## 已回收伏笔

| ID | 伏笔内容 | 埋设章节 | 回收章节 | 说明 |
|----|---------|---------|---------|------|
"""
    pending_hooks_path = truth_files_dir / "pending-hooks.md"
    pending_hooks_path.write_text(pending_hooks_content, encoding="utf-8")

    # 生成 power-system.md
    power_system_content = """# 力量体系

## 等级划分

（待设定）

## 能力类型

（待设定）

## 突破条件

（待设定）

## 特殊规则

（待设定）
"""
    power_system_path = truth_files_dir / "power-system.md"
    power_system_path.write_text(power_system_content, encoding="utf-8")

    print("✅ 配置文件生成完成")
    print(f"   .novel-weaver/memory/constitution.md")
    print(f"   .novel-weaver/truth-files/characters.md")
    print(f"   .novel-weaver/truth-files/current-state.md")
    print(f"   .novel-weaver/truth-files/world-setting.md")
    print(f"   .novel-weaver/truth-files/pending-hooks.md")
    print(f"   .novel-weaver/truth-files/power-system.md")


def print_next_steps():
    """打印下一步指引"""
    print("\n" + "=" * 60)
    print("  🎉 初始化完成！")
    print("=" * 60 + "\n")

    print("接下来，你可以：\n")
    print("  1. 生成大纲")
    print("     /novel-weaver plan 帮我生成总大纲\n")
    print("  2. 开始写作")
    print("     /novel-weaver write 写第一章\n")
    print("  3. 查看帮助")
    print("     /novel-weaver help\n")
    print("  4. 查看快速上手教程")
    print("     参考 skill/QUICKSTART.md\n")


def verify_installation():
    """验证安装"""
    print("\n🔍 验证安装...\n")

    # 检查 SKILL.md
    skill_md = Path("skill/SKILL.md")
    if skill_md.exists():
        print("✅ skill/SKILL.md 存在")
    else:
        print("❌ skill/SKILL.md 不存在")
        return False

    # 检查 scripts 目录
    scripts_dir = Path("skill/scripts")
    if scripts_dir.exists():
        print("✅ skill/scripts/ 目录存在")
    else:
        print("❌ skill/scripts/ 目录不存在")
        return False

    # 检查 QUICKSTART.md
    quickstart_md = Path("skill/QUICKSTART.md")
    if quickstart_md.exists():
        print("✅ skill/QUICKSTART.md 存在")
    else:
        print("⚠️  skill/QUICKSTART.md 不存在（可选）")

    print("\n✅ 安装验证通过")
    return True


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="NovelWeaver 交互式引导脚本")
    parser.add_argument("--ide", choices=["trae", "claude"], help="指定IDE类型")
    parser.add_argument("--auto", action="store_true", help="自动模式，使用默认配置")
    parser.add_argument("--verify", action="store_true", help="验证安装是否成功")
    args = parser.parse_args()

    print_banner()

    # 验证模式
    if args.verify:
        success = verify_installation()
        sys.exit(0 if success else 1)

    # 检测环境
    if not detect_environment():
        sys.exit(1)

    # 检测IDE
    ide = args.ide or detect_ide()
    if ide:
        print(f"   IDE类型：{ide}")
    print()

    # 自动模式
    if args.auto:
        print("🚀 自动模式：使用默认配置\n")
        config = {
            "emotion_label": EMOTION_LABELS["A"],
            "book_name": "默认书名",
            "genre": "玄幻修仙",
            "synopsis": "默认简介",
            "protagonist": {
                "name": "主角",
                "contrast": "表面废物实际天才",
                "goal": "成为最强",
            },
            "conflict": "与强敌的宿命对决",
            "chapters": 100,
            "style": "天蚕土豆",
        }
    else:
        # 交互式引导
        emotion_label = select_emotion_label()
        book_info = input_book_info()
        protagonist = input_protagonist()
        conflict = input_conflict()
        chapters = input_chapters()
        style = select_style(book_info["genre"])

        config = {
            "emotion_label": emotion_label,
            "book_name": book_info["book_name"],
            "genre": book_info["genre"],
            "synopsis": book_info["synopsis"],
            "protagonist": protagonist,
            "conflict": conflict,
            "chapters": chapters,
            "style": style,
        }

        # 确认配置
        if not confirm_config(config):
            print("\n❌ 已取消配置")
            sys.exit(0)

    # 生成配置文件
    generate_config_files(config)

    # 打印下一步指引
    print_next_steps()


if __name__ == "__main__":
    main()
