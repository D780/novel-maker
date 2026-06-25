# 常见问题

## 安装问题

### Q: 安装后 AI 没识别到技能？

**解决方案：**
1. 确认路径正确（注意是 `skills/novel-maker/` 不是直接 `skills/`）
2. 确认 `SKILL.md` 存在于目录根
3. 重启 IDE 会话
4. 输入 `/novel-maker help` 手动触发

### Q: npx novel-maker 运行失败？

**解决方案：**
1. 检查 Node.js 版本（需要 >= 16.0.0）
2. 检查网络连接
3. 尝试使用管理员权限运行
4. 使用手动安装方式

### Q: 可以全局安装吗？

**解决方案：**
可以。全局路径一般为 `~/.<ide>/skills/novel-maker/`，所有项目都能使用。

## 使用问题

### Q: 生成的内容不符合预期？

**解决方案：**
1. 检查创作宪法是否完善
2. 提供更具体的写作指引
3. 使用 `/novel-maker review` 检查问题
4. 调整文风设置

### Q: 字数不达标怎么办？

**解决方案：**
- AI 会自动扩写，直到达标
- 也可以手动使用 `/novel-maker expand` 扩写
- 检查字数设置是否合理

### Q: 如何切换文风？

**解决方案：**
```
/novel-maker style 换辰东风格
```

### Q: 如何查看当前设定？

**解决方案：**
```
/novel-maker memory 主角什么等级
```

## 高级问题

### Q: 如何自定义情绪标签？

**解决方案：**
1. 编辑 `.novel-maker/memory/constitution.md`
2. 修改情绪标签配置
3. 重启 IDE 会话

### Q: 如何导入现有小说？

**解决方案：**
1. 将小说内容放入 `novels/` 目录
2. 运行 `/novel-maker memory` 更新记忆
3. 运行 `/novel-maker review` 检查一致性

### Q: 脚本需要额外安装依赖吗？

**解决方案：**
不需要。所有 Python 脚本只使用标准库（`os`、`re`、`json`、`argparse`、`pathlib`）。

### Q: 这个技能仓库和 MCP 有什么区别？

**解决方案：**
MCP 是外部服务接口协议，需要运行额外进程；Skill 是纯 Markdown 指令包，零依赖、零配置、无需启动，开箱即用。
