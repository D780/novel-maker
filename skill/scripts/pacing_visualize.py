#!/usr/bin/env python3
"""
节奏可视化脚本

使用方式：
    python scripts/pacing_visualize.py --chapter novels/volume-01/chapters/ch01.md
    python scripts/pacing_visualize.py --volume novels/volume-01/
    python scripts/pacing_visualize.py --all novels/
"""

import argparse
import re
from pathlib import Path


# 情绪标记
EMOTION_MARKERS = {
    "爽": "💥",
    "感动": "❤️",
    "虐": "😢",
    "惊": "😱",
    "笑": "😂",
}

# 节奏标记
PACING_MARKERS = {
    "平淡": "🟢",
    "小高潮": "🟡",
    "大高潮": "🔴",
}


def analyze_chapter_pacing(chapter_content: str) -> list[str]:
    """分析章节节奏"""
    # 简单实现：根据关键词判断节奏
    markers = []

    # 检测高潮场景
    climax_keywords = ["大战", "突破", "对决", "爆发", "逆转"]
    if any(kw in chapter_content for kw in climax_keywords):
        markers.append("🔴")
    elif any(kw in chapter_content for kw in ["冲突", "紧张", "危险"]):
        markers.append("🟡")
    else:
        markers.append("🟢")

    return markers


def analyze_chapter_emotions(chapter_content: str) -> dict[str, int]:
    """分析章节情绪点"""
    emotions = {}

    for emotion, marker in EMOTION_MARKERS.items():
        count = chapter_content.count(emotion)
        if count > 0:
            emotions[emotion] = count

    return emotions


def generate_chapter_report(chapter_path: Path) -> str:
    """生成章节级节奏报告"""
    content = chapter_path.read_text(encoding="utf-8")
    pacing = analyze_chapter_pacing(content)
    emotions = analyze_chapter_emotions(content)

    report = f"## {chapter_path.stem}\n\n"
    report += f"节奏：{''.join(pacing)}\n"

    if emotions:
        report += "情绪点：\n"
        for emotion, count in emotions.items():
            report += f"  - {EMOTION_MARKERS[emotion]} {emotion}：{count}次\n"

    return report


def generate_volume_heatmap(volume_path: Path) -> str:
    """生成卷级热力图"""
    chapters = sorted(volume_path.glob("chapters/ch*.md"))

    if not chapters:
        return "未找到章节文件\n"

    report = f"# {volume_path.name} 节奏热力图\n\n"
    report += "章: "

    # 章节号
    for i in range(1, len(chapters) + 1):
        report += f"{i:02d} "
    report += "\n    "

    # 节奏标记
    for chapter in chapters:
        content = chapter.read_text(encoding="utf-8")
        pacing = analyze_chapter_pacing(content)
        report += f"{pacing[0]} "

    report += "\n"
    return report


def generate_emotion_stats(volume_path: Path) -> str:
    """生成多维度情绪统计"""
    chapters = sorted(volume_path.glob("chapters/ch*.md"))

    if not chapters:
        return "未找到章节文件\n"

    total_emotions = {}
    for chapter in chapters:
        content = chapter.read_text(encoding="utf-8")
        emotions = analyze_chapter_emotions(content)
        for emotion, count in emotions.items():
            total_emotions[emotion] = total_emotions.get(emotion, 0) + count

    report = f"# {volume_path.name} 情绪统计\n\n"
    chapter_count = len(chapters)

    for emotion, count in sorted(total_emotions.items(), key=lambda x: -x[1]):
        avg = chapter_count / count if count > 0 else 0
        report += f"- {EMOTION_MARKERS[emotion]} {emotion}：{count}次（平均{avg:.1f}章/次）\n"

    return report


def main():
    parser = argparse.ArgumentParser(description="节奏可视化脚本")
    parser.add_argument("--chapter", help="分析单个章节")
    parser.add_argument("--volume", help="分析整个卷")
    parser.add_argument("--all", help="分析所有卷")
    args = parser.parse_args()

    if args.chapter:
        chapter_path = Path(args.chapter)
        if chapter_path.exists():
            print(generate_chapter_report(chapter_path))
        else:
            print(f"文件不存在：{args.chapter}")

    elif args.volume:
        volume_path = Path(args.volume)
        if volume_path.exists():
            print(generate_volume_heatmap(volume_path))
            print(generate_emotion_stats(volume_path))
        else:
            print(f"目录不存在：{args.volume}")

    elif args.all:
        novels_path = Path(args.all)
        if novels_path.exists():
            for volume in sorted(novels_path.iterdir()):
                if volume.is_dir() and volume.name.startswith("volume"):
                    print(generate_volume_heatmap(volume))
                    print(generate_emotion_stats(volume))
        else:
            print(f"目录不存在：{args.all}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
