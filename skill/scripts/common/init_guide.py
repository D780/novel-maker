#!/usr/bin/env python3
"""
NovelMaker 交互式引导脚本

使用方式：
    python scripts/common/init_guide.py [--ide trae|claude] [--auto] [--verify]

参数说明：
    --ide: 指定IDE类型（trae 或 claude）
    --auto: 自动模式，使用默认配置
    --verify: 验证安装是否成功
"""

import sys
import argparse
import json
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


def load_presets():
    """加载预设模板"""
    presets_path = Path(__file__).parent.parent / "templates" / "presets.json"
    try:
        with open(presets_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get("presets", {})
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def show_progress(current_step, total_steps, step_name):
    """显示进度指示器"""
    progress = current_step / total_steps
    bar_length = 30
    filled_length = int(bar_length * progress)
    bar = '█' * filled_length + '░' * (bar_length - filled_length)
    print(f"\n进度：[{bar}] {current_step}/{total_steps} - {step_name}")


def select_preset_template(presets):
    """选择预设模板"""
    print("\n📋 可用预设模板：\n")
    preset_list = list(presets.items())
    for i, (key, preset) in enumerate(preset_list, 1):
        print(f"  {i}. {preset['name']} - {preset['description']}")
    print()

    while True:
        choice = input(f"请选择预设模板 (1-{len(preset_list)}): ").strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(preset_list):
                key, preset = preset_list[idx]
                print(f"\n✅ 已选择：{preset['name']}")
                emotion_key = preset.get("emotion_label", "A")
                emotion_data = EMOTION_LABELS.get(emotion_key, EMOTION_LABELS["A"])
                protag = preset.get("protagonist_template", {})
                config = {
                    "emotion_label": emotion_data,
                    "book_name": input("书名: ").strip() or preset.get("name", "示例"),
                    "genre": preset.get("genre", "玄幻修仙"),
                    "synopsis": input("一句话简介: ").strip() or f"{preset.get('name', '示例')}故事",
                    "protagonist": {
                        "name": input("主角姓名: ").strip() or "主角",
                        "contrast": protag.get("contrast", ""),
                        "goal": protag.get("goal", ""),
                    },
                    "conflict": preset.get("conflict_template", ""),
                    "chapters": preset.get("chapters", 100),
                    "style": preset.get("style", "天蚕土豆"),
                }
                return config
        except ValueError:
            print("❌ 无效选择，请重新输入")


def export_configuration(config, filename="novel-maker-config.json"):
    """导出配置到JSON文件"""
    export_config = config.copy()
    if isinstance(export_config.get('emotion_label'), dict):
        export_config['emotion_label'] = export_config['emotion_label']['name']
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(export_config, f, ensure_ascii=False, indent=2)
    print(f"✅ 配置已导出到 {filename}")


def import_configuration(filename=None):
    """从JSON文件导入配置"""
    if filename is None:
        filename = input("请输入配置文件路径: ").strip()
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            config = json.load(f)
        if isinstance(config.get('emotion_label'), str):
            matched = False
            for label in EMOTION_LABELS.values():
                if label['name'] == config['emotion_label']:
                    config['emotion_label'] = label
                    matched = True
                    break
            if not matched:
                print(f"⚠️  未知的 emotion_label: {config['emotion_label']}，使用默认值 A")
                config['emotion_label'] = EMOTION_LABELS["A"]
        print(f"✅ 已从 {filename} 导入配置")
        return config
    except FileNotFoundError:
        print(f"❌ 文件 {filename} 不存在")
        return None
    except json.JSONDecodeError:
        print(f"❌ 文件 {filename} 格式错误")
        return None


# 题材包选项
GENRE_PACKS = {
    "xianxia": {"name": "修仙", "desc": "境界体系、宗门设定、秘境模板、渡劫规则"},
    "urban": {"name": "都市", "desc": "商战模板、复仇套路、崛起路径、感情线"},
    "infinite-flow": {"name": "无限流", "desc": "副本设计、强化体系、团队配置、BOSS战"},
    "mystery": {"name": "悬疑", "desc": "案件设计、推理线索、反转技巧、伏笔布局"},
    "history": {"name": "历史", "desc": "权谋模板、战役描写、改革路线、朝堂设定"},
    "sci-fi": {"name": "科幻", "desc": "科技体系、星际设定、AI描写、时间线管理"},
    "game": {"name": "游戏", "desc": "游戏系统、等级体系、装备设计、副本攻略"},
    "apocalypse": {"name": "末世", "desc": "生存体系、异能设定、势力分布、资源管理"},
    "western-fantasy": {"name": "西幻", "desc": "魔法体系、种族设定、骑士精神、王国政治"},
    "wuxia": {"name": "武侠", "desc": "武功体系、江湖规矩、侠义精神、门派纷争"},
    "romance": {"name": "言情", "desc": "感情线设计、人物关系、情感冲突、甜蜜互动"},
}


def select_genre_pack():
    """选择题材包"""
    print("\n📋 选择题材包\n")
    print("可选题材包：\n")
    
    for key, value in GENRE_PACKS.items():
        print(f"  {key}: {value['name']} - {value['desc']}")
    
    print()
    
    while True:
        choice = input("请输入题材包名称（如 xianxia）或直接输入自定义题材: ").strip()
        if choice in GENRE_PACKS:
            selected = GENRE_PACKS[choice]
            print(f"\n✅ 已选择题材包：{selected['name']}")
            return choice, selected['name']
        elif choice:
            print(f"\n✅ 使用自定义题材：{choice}")
            return None, choice
        else:
            print("❌ 请输入题材包名称或自定义题材")


def custom_configuration():
    """自定义配置流程（带进度指示器）"""
    total_steps = 7
    show_progress(1, total_steps, "选择情绪标签")
    emotion_label = select_emotion_label()
    show_progress(2, total_steps, "选择题材包")
    genre_pack_key, genre_pack_name = select_genre_pack()
    show_progress(3, total_steps, "填写书籍信息")
    book_info = input_book_info()
    show_progress(4, total_steps, "设置主角信息")
    protagonist = input_protagonist()
    show_progress(5, total_steps, "确定核心冲突")
    conflict = input_conflict()
    show_progress(6, total_steps, "设定章节数")
    chapters = input_chapters()
    show_progress(7, total_steps, "选择文风")
    style = select_style(book_info["genre"])
    return {
        "emotion_label": emotion_label,
        "genre_pack_key": genre_pack_key,
        "genre_pack_name": genre_pack_name,
        "book_name": book_info["book_name"],
        "genre": book_info["genre"],
        "synopsis": book_info["synopsis"],
        "protagonist": protagonist,
        "conflict": conflict,
        "chapters": chapters,
        "style": style,
    }


def print_banner():
    """打印欢迎横幅"""
    print("\n" + "=" * 60)
    print("  NovelMaker v2.0.0 - 全能网文写作助手")
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
        print("   请确保在 NovelMaker 仓库根目录下运行此脚本")
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


# 支持的 IDE 检测列表（与 install.py / bin/novel-maker.js 保持一致）
IDE_DETECT = [
    ("Trae",          "trae",    [".trae"]),
    ("Claude Code",   "claude",  [".claude"]),
    ("Cursor",        "cursor",  [".cursor", ".cursorrules"]),
    ("Windsurf",      "windsurf", [".windsurf"]),
    ("Gemini CLI",    "gemini",  ["GEMINI.md"]),
    ("Codex CLI",     "codex",   [".codex"]),
    ("OpenCode",      "opencode", [".opencode"]),
    ("Aider",         "aider",   [".aider"]),
    ("Hermes Agent",  "hermes",  [".hermes", "HERMES.md"]),
    ("Qwen Code",     "qwen",    [".qwen"]),
    ("Claw Code",     "claw",    [".claw", "CLAW.md"]),
    ("Qoder",         "qoder",   [".qoder"]),
    ("Antigravity",   "antigravity", [".agents"]),
    ("OpenClaw",      "openclaw", [".openclaw"]),
    ("Kiro",          "kiro",    [".kiro"]),
    ("VS Code",       "vscode",  [".github/copilot-instructions.md"]),
    ("DeerFlow",      "deerflow", ["deer_flow"]),
    ("Copilot CLI",   "copilot", [".claude"]),
]


def detect_ide():
    """检测IDE类型"""
    print("🔍 检测IDE类型...\n")

    cwd = Path.cwd()
    detected = []
    for name, key, markers in IDE_DETECT:
        for marker in markers:
            if (cwd / marker).exists():
                detected.append((name, key))
                break

    if detected:
        for name, _ in detected:
            print(f"✅ 检测到 {name}")
        return detected[0][1]

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
    while not book_name:
        print("❌ 书名不能为空")
        book_name = input("书名（如：废材逆天记）: ").strip()

    genre = input("题材（如：玄幻修仙、都市搞笑）: ").strip()
    while not genre:
        print("❌ 题材不能为空")
        genre = input("题材（如：玄幻修仙、都市搞笑）: ").strip()

    synopsis = input("一句话简介（如：废材逆袭成仙帝）: ").strip()
    while not synopsis:
        print("❌ 简介不能为空")
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
    while not name:
        print("❌ 主角姓名不能为空")
        name = input("主角姓名（如：林轩）: ").strip()

    contrast = input("核心反差点（如：表面废物实际天才）: ").strip()
    while not contrast:
        print("❌ 核心反差点不能为空")
        contrast = input("核心反差点（如：表面废物实际天才）: ").strip()

    goal = input("核心目标（如：成为仙帝）: ").strip()
    while not goal:
        print("❌ 核心目标不能为空")
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
    while not conflict:
        print("❌ 核心冲突不能为空")
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

    try:
        # 创建 .novel-maker 目录
        NOVEL_MAKER_dir = Path(".novel-maker")
        NOVEL_MAKER_dir.mkdir(exist_ok=True)

        # 创建 truth-files 目录
        truth_files_dir = NOVEL_MAKER_dir / "truth-files"
        truth_files_dir.mkdir(exist_ok=True)

        # 创建 memory 目录
        memory_dir = NOVEL_MAKER_dir / "memory"
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
        print(f"   .novel-maker/memory/constitution.md")
        print(f"   .novel-maker/truth-files/characters.md")
        print(f"   .novel-maker/truth-files/current-state.md")
        print(f"   .novel-maker/truth-files/world-setting.md")
        print(f"   .novel-maker/truth-files/pending-hooks.md")
        print(f"   .novel-maker/truth-files/power-system.md")

    except OSError as e:
        print(f"❌ 文件操作失败：{e}")
        print("   请检查磁盘空间和文件权限")
        sys.exit(1)


def print_next_steps():
    """打印下一步指引"""
    print("\n" + "=" * 60)
    print("  🎉 初始化完成！")
    print("=" * 60 + "\n")

    print("接下来，你可以：\n")
    print("  1. 生成大纲")
    print("     /novel-maker plan 帮我生成总大纲\n")
    print("  2. 开始写作")
    print("     /novel-maker write 写第一章\n")
    print("  3. 查看帮助")
    print("     /novel-maker help\n")
    print("  4. 查看快速上手教程")
    print("     参考 skill/docs/quickstart.md\n")


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
    parser = argparse.ArgumentParser(description="NovelMaker 交互式引导脚本")
    parser.add_argument("--ide", choices=["trae", "claude"], help="指定IDE类型")
    parser.add_argument("--auto", action="store_true", help="自动模式，使用默认配置")
    parser.add_argument("--verify", action="store_true", help="验证安装是否成功")
    parser.add_argument("--export", action="store_true", help="导出配置到文件")
    parser.add_argument("--import", dest="import_file", help="从文件导入配置")
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
    # 导入配置模式
    elif args.import_file:
        config = import_configuration(args.import_file)
        if not config:
            sys.exit(1)
    else:
        # 加载预设模板
        presets = load_presets()
        
        # 选择启动方式
        print("📋 选择启动方式：\n")
        print("  1. 使用预设模板（推荐新手）")
        print("  2. 自定义配置（完全控制）")
        print("  3. 从现有配置导入")
        print()
        
        choice = input("请选择 (1/2/3): ").strip()
        
        if choice == "1" and presets:
            config = select_preset_template(presets)
        elif choice == "3":
            config = import_configuration()
            if not config:
                print("❌ 导入失败，切换到自定义配置")
                config = custom_configuration()
        else:
            config = custom_configuration()

    # 确认配置
    if not confirm_config(config):
        print("\n❌ 已取消配置")
        sys.exit(0)

    # 生成配置文件
    generate_config_files(config)

    # 导出配置（可选）
    if args.export:
        export_configuration(config)

    # 打印下一步指引
    print_next_steps()


if __name__ == "__main__":
    main()
