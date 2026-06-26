#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单元测试脚本
测试所有辅助脚本的基本功能。

用法:
    python scripts/test_scripts.py
"""

import os
import sys
import json
import tempfile
import shutil
from pathlib import Path

# Add common to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'common'))

# Test results
test_results = {
    'passed': 0,
    'failed': 0,
    'errors': []
}


def test_passed(test_name):
    test_results['passed'] += 1
    print(f"  ✓ {test_name}")


def test_failed(test_name, error):
    test_results['failed'] += 1
    test_results['errors'].append({'test': test_name, 'error': str(error)})
    print(f"  ✗ {test_name}: {error}")


def create_test_chapter(filepath, title="测试章节", content=None):
    """Create a test chapter file."""
    if content is None:
        content = f"""# {title}

林风站在山巅，望着远方的城市。

"苏婉，你来了。"林风转身说道。

苏婉微微一笑："我当然会来。"

两人相视一笑，心中都明白彼此的心意。

突然，远处传来一声巨响，天空中出现了一道裂缝。

"不好！"林风脸色大变，"危机降临了！"

苏婉握紧手中的宝剑："我们一起面对！"

林风从怀中掏出一本古老的秘籍，这是师父留给他的传承。

"据说这本秘籍具有强大的力量，但需要足够的修为才能使用。"林风说道。

苏婉点头："我相信你一定能突破瓶颈。"

林风闭上眼睛，开始运功修炼。他的修为从筑基期开始提升...

一刻钟后，林风睁开眼睛，眼中闪过一丝精光。

"我突破了！现在是金丹期！"林风兴奋地说道。

苏婉为他高兴："太好了！"

但就在这时，一个神秘人出现在他们面前。

"你们以为这样就结束了吗？"神秘人冷笑道，"真正的危险才刚刚开始。"

林风和苏婉对视一眼，都看到了对方眼中的决心。

无论前方有什么危险，他们都会一起面对。

---

**下章预告**：神秘人的真实身份究竟是什么？林风能否保护苏婉？"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def create_test_truth_file(filepath, content):
    """Create a test truth file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


def test_scene_builder():
    """Test scene_builder.py"""
    print("\n=== 测试 scene_builder.py ===")
    try:
        from writer.scene_builder import build_scene, list_scene_types

        # Test list_scene_types
        result = list_scene_types()
        assert 'available_types' in result
        assert len(result['available_types']) > 0
        test_passed('list_scene_types')

        # Test build_scene
        result = build_scene('冲突', ['林风', '苏婉'], '紧张')
        assert 'scene_type' in result
        assert result['scene_type'] == '冲突'
        assert 'structure' in result
        assert len(result['structure']) > 0
        test_passed('build_scene with type, chars, emotion')

        # Test invalid type
        result = build_scene('invalid_type')
        assert 'error' in result
        test_passed('build_scene with invalid type')

    except Exception as e:
        test_failed('scene_builder', e)


def test_dialogue_checker():
    """Test dialogue_checker.py"""
    print("\n=== 测试 dialogue_checker.py ===")
    try:
        from auditor.dialogue_checker import check_dialogue_quality, extract_dialogues

        # Test extract_dialogues (using ASCII quotes which the regex also matches)
        text = '林风说道："你好。"苏婉回答："我很好。"'
        dialogues = extract_dialogues(text)
        assert len(dialogues) == 2
        test_passed('extract_dialogues')

        # Test check_dialogue_quality
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write('# 测试章节\n\n林风说道："你好。"苏婉回答："我很好。"')
            temp_file = f.name

        try:
            result = check_dialogue_quality(temp_file)
            assert 'dialogue_count' in result
            assert 'checks' in result
            test_passed('check_dialogue_quality')
        finally:
            os.unlink(temp_file)

    except Exception as e:
        test_failed('dialogue_checker', e)


def test_character_arc_tracker():
    """Test character_arc_tracker.py"""
    print("\n=== 测试 character_arc_tracker.py ===")
    try:
        from reviewer.character_arc_tracker import build_character_arc

        # Create temp directory with test chapters
        temp_dir = tempfile.mkdtemp()
        try:
            for i in range(3):
                create_test_chapter(os.path.join(temp_dir, f'第{i+1:02d}章.md'), f'第{i+1}章')

            result = build_character_arc(temp_dir, ['林风'])
            assert 'total_chapters_analyzed' in result
            assert result['total_chapters_analyzed'] == 3
            assert 'characters_tracked' in result
            test_passed('build_character_arc')
        finally:
            shutil.rmtree(temp_dir)

    except Exception as e:
        test_failed('character_arc_tracker', e)


def test_subplot_tracker():
    """Test subplot_tracker.py"""
    print("\n=== 测试 subplot_tracker.py ===")
    try:
        from reviewer.subplot_tracker import track_subplot_across_chapters

        # Create temp directory with test chapters
        temp_dir = tempfile.mkdtemp()
        try:
            for i in range(3):
                create_test_chapter(os.path.join(temp_dir, f'第{i+1:02d}章.md'), f'第{i+1}章')

            result = track_subplot_across_chapters(temp_dir)
            assert 'total_chapters_analyzed' in result
            assert 'subplots_detected' in result
            test_passed('track_subplot_across_chapters')
        finally:
            shutil.rmtree(temp_dir)

    except Exception as e:
        test_failed('subplot_tracker', e)


def test_chapter_transition():
    """Test chapter_transition.py"""
    print("\n=== 测试 chapter_transition.py ===")
    try:
        from auditor.chapter_transition import check_transition, list_chapters

        # Create temp directory with test chapters
        temp_dir = tempfile.mkdtemp()
        try:
            for i in range(3):
                create_test_chapter(os.path.join(temp_dir, f'第{i+1:02d}章.md'), f'第{i+1}章')

            chapter_files = list_chapters(temp_dir)
            assert len(chapter_files) == 3

            transitions = check_transition(chapter_files)
            assert len(transitions) == 2  # 3 chapters = 2 transitions
            test_passed('check_transition')
        finally:
            shutil.rmtree(temp_dir)

    except Exception as e:
        test_failed('chapter_transition', e)


def test_emotion_curve():
    """Test emotion_curve.py"""
    print("\n=== 测试 emotion_curve.py ===")
    try:
        from reviewer.emotion_curve import analyze_emotion_in_text, build_emotion_curve

        # Test analyze_emotion_in_text
        text = '林风很开心，苏婉很悲伤，两人心情复杂。'
        result = analyze_emotion_in_text(text)
        assert 'dominant' in result
        assert 'scores' in result
        test_passed('analyze_emotion_in_text')

        # Test build_emotion_curve
        temp_dir = tempfile.mkdtemp()
        try:
            for i in range(3):
                create_test_chapter(os.path.join(temp_dir, f'第{i+1:02d}章.md'), f'第{i+1}章')

            result = build_emotion_curve(temp_dir)
            assert 'total_chapters' in result
            assert 'curve' in result
            test_passed('build_emotion_curve')
        finally:
            shutil.rmtree(temp_dir)

    except Exception as e:
        test_failed('emotion_curve', e)


def test_foreshadowing_tracker():
    """Test foreshadowing_tracker.py"""
    print("\n=== 测试 foreshadowing_tracker.py ===")
    try:
        from reviewer.foreshadowing_tracker import track_foreshadowing_across_chapters

        # Create temp directory with test chapters
        temp_dir = tempfile.mkdtemp()
        try:
            for i in range(3):
                create_test_chapter(os.path.join(temp_dir, f'第{i+1:02d}章.md'), f'第{i+1}章')

            result = track_foreshadowing_across_chapters(temp_dir)
            assert 'total_chapters' in result
            assert 'total_setups' in result
            assert 'total_resolutions' in result
            test_passed('track_foreshadowing_across_chapters')
        finally:
            shutil.rmtree(temp_dir)

    except Exception as e:
        test_failed('foreshadowing_tracker', e)


def test_worldbuilding_checker():
    """Test worldbuilding_checker.py"""
    print("\n=== 测试 worldbuilding_checker.py ===")
    try:
        from auditor.worldbuilding_checker import check_worldbuilding_consistency

        # Create temp directory with test chapters
        temp_dir = tempfile.mkdtemp()
        truth_dir = tempfile.mkdtemp()
        try:
            for i in range(3):
                create_test_chapter(os.path.join(temp_dir, f'第{i+1:02d}章.md'), f'第{i+1}章')

            # Create truth file
            create_test_truth_file(
                os.path.join(truth_dir, 'power_system.md'),
                '# 力量体系\n\n- 筑基期\n- 金丹期\n- 元婴期'
            )

            result = check_worldbuilding_consistency(temp_dir, truth_dir)
            assert 'total_chapters' in result
            assert 'dimensions_checked' in result
            assert 'issues' in result
            test_passed('check_worldbuilding_consistency')
        finally:
            shutil.rmtree(temp_dir)
            shutil.rmtree(truth_dir)

    except Exception as e:
        test_failed('worldbuilding_checker', e)


def test_pacing_optimizer():
    """Test pacing_optimizer.py"""
    print("\n=== 测试 pacing_optimizer.py ===")
    try:
        from auditor.pacing_optimizer import analyze_pacing_with_suggestions

        # Create temp directory with test chapters
        temp_dir = tempfile.mkdtemp()
        try:
            for i in range(5):
                create_test_chapter(os.path.join(temp_dir, f'第{i+1:02d}章.md'), f'第{i+1}章')

            result = analyze_pacing_with_suggestions(temp_dir)
            assert 'total_chapters' in result
            assert 'pacing_distribution' in result
            assert 'suggestions' in result
            test_passed('analyze_pacing_with_suggestions')
        finally:
            shutil.rmtree(temp_dir)

    except Exception as e:
        test_failed('pacing_optimizer', e)


def main():
    print("=" * 60)
    print("NovelMaker 辅助脚本单元测试")
    print("=" * 60)

    # Run all tests
    test_scene_builder()
    test_dialogue_checker()
    test_character_arc_tracker()
    test_subplot_tracker()
    test_chapter_transition()
    test_emotion_curve()
    test_foreshadowing_tracker()
    test_worldbuilding_checker()
    test_pacing_optimizer()

    # Print summary
    print("\n" + "=" * 60)
    print(f"测试完成: {test_results['passed']}通过, {test_results['failed']}失败")
    print("=" * 60)

    if test_results['errors']:
        print("\n失败详情:")
        for error in test_results['errors']:
            print(f"  - {error['test']}: {error['error']}")

    return 0 if test_results['failed'] == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
