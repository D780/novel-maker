# Data Agent 实体自动提取

## 系统原理

Data Agent 在写作过程中自动提取故事中的实体（角色、物品、地点、势力等），
并自动消歧、入库管理，确保所有实体都有唯一记录。

---

## 一、实体类型

### 1. 角色实体 (Character)

| 属性 | 类型 | 说明 | 示例 |
|------|------|------|------|
| id | String | 唯一标识符 | "C001", "C002" |
| name | String | 角色名 | "叶凡", "萧炎" |
| alias | String[] | 别名/称号 | ["叶天帝", "荒天帝"] |
| role | Enum | 角色类型 | 主角/配角/反派/龙套 |
| gender | Enum | 性别 | 男/女/未知 |
| age | Number | 年龄（故事内） | 18, 200 |
| status | Enum | 当前状态 | 活跃/死亡/失踪/沉睡 |
| faction | String | 所属势力 | "荒古世家", "宗门名" |
| power_level | String | 当前等级 | "炼气3层", "筑基初期" |
| personality | String[] | 性格特征 | ["谨慎", "果断"] |
| relationships | Object | 人际关系 | {"父亲": "角色ID", "师傅": "角色ID"} |
| items | String[] | 持有物品ID | ["I001", "I002"] |
| abilities | String[] | 掌握能力ID | ["A001"] |
| first_appearance | String | 首次出场章节 | "第3章" |
| last_appearance | String | 最近出场章节 | "第25章" |

### 2. 物品实体 (Item)

| 属性 | 类型 | 说明 | 示例 |
|------|------|------|------|
| id | String | 唯一标识符 | "I001" |
| name | String | 物品名 | "神秘玉佩" |
| type | Enum | 物品类型 | 法宝/丹药/材料/道具 |
| grade | String | 品级 | "黄阶上品", "仙器" |
| owner | String | 当前所有者ID | "C001" |
| origin | String | 来源 | "传承", "拍卖", "掉落" |
| abilities | String[] | 功能/效果 | ["提升修炼速度", "抵挡一次致命伤害"] |
| status | Enum | 当前状态 | 持有/已使用/已损毁/遗失 |
| description | String | 描述 | "一块刻有神秘纹路的玉佩" |
| hooks | String[] | 关联伏笔ID | ["H001"] |

### 3. 地点实体 (Location)

| 属性 | 类型 | 说明 | 示例 |
|------|------|------|------|
| id | String | 唯一标识符 | "L001" |
| name | String | 地点名 | "青云门" |
| type | Enum | 地点类型 | 宗门/城市/秘境/野外 |
| parent | String | 上级地点 | "L002" |
| level | String | 地点等级 | "一星", "三星" |
| faction | String | 控制势力 | "青云宗" |
| description | String | 描述 | "坐落于青云山之巅" |
| features | String[] | 特征 | ["灵气充裕", "有传送阵"] |
| danger_level | Enum | 危险等级 | 安全/低危/高危/死地 |

### 4. 势力实体 (Faction)

| 属性 | 类型 | 说明 | 示例 |
|------|------|------|------|
| id | String | 唯一标识符 | "F001" |
| name | String | 势力名 | "青云宗" |
| type | Enum | 势力类型 | 宗门/家族/帝国/组织 |
| level | String | 势力等级 | "一流", "二流" |
| members | String[] | 成员角色ID | ["C001", "C002"] |
| allies | String[] | 盟友势力ID | ["F002"] |
| enemies | String[] | 敌对势力ID | ["F003"] |
| territory | String[] | 领地地点ID | ["L001"] |
| leader | String | 领袖角色ID | "C001" |
| status | Enum | 势力状态 | 兴盛/稳定/衰落/灭亡 |

### 5. 能力实体 (Ability)

| 属性 | 类型 | 说明 | 示例 |
|------|------|------|------|
| id | String | 唯一标识符 | "A001" |
| name | String | 能力名 | "焚诀" |
| type | Enum | 能力类型 | 功法/武技/天赋/天赋神通 |
| grade | String | 等级 | "黄阶上品" |
| owner | String[] | 拥有者角色ID | ["C001"] |
| description | String | 描述 | "可以吞噬火焰提升的功法" |
| level | String | 修炼进度 | "入门", "小成", "大成", "圆满" |
| requirements | String[] | 修炼条件 | ["火属性灵根", "筑基期"] |

### 6. 事件实体 (Event)

| 属性 | 类型 | 说明 | 示例 |
|------|------|------|------|
| id | String | 唯一标识符 | "E001" |
| name | String | 事件名 | "外门大比" |
| type | Enum | 事件类型 | 比赛/战斗/突破/死亡 |
| chapter | String | 发生章节 | "第10章" |
| participants | String[] | 参与者角色ID | ["C001", "C002"] |
| result | String | 结果 | "主角获胜" |
| impact | String[] | 影响 | ["主角晋升内门", "反派记恨"] |

---

## 二、实体提取流程

### 自动提取

```
1. AI 生成章节内容
   ↓
2. NLP 识别实体：
   - 新角色名 → 创建角色实体
   - 新物品名 → 创建物品实体
   - 新地点名 → 创建地点实体
   - 新势力名 → 创建势力实体
   ↓
3. 实体消歧：
   - 同义词识别（别名/简称）
   - 同名异人区分
   - 实体合并
   ↓
4. 分配唯一 ID：
   - 角色：C001, C002...
   - 物品：I001, I002...
   - 地点：L001, L002...
   - 势力：F001, F002...
   - 能力：A001, A002...
   - 事件：E001, E002...
   ↓
5. 入库管理：
   - 添加到 truth-files/entities.md
   - 关联到角色档案
   - 关联到世界观
   ↓
6. 作者确认：
   - AI 提示新实体
   - 作者确认/修改/删除
```

### 手动管理

```
/novel-weaver entity list 列出所有实体
/novel-weaver entity type 列出指定类型实体
/novel-weaver entity show [ID] 显示实体详情
/novel-weaver entity add 手动添加实体
/novel-weaver entity update 更新实体
/novel-weaver entity delete 删除实体
/novel-weaver entity merge 合并重复实体
```

---

## 三、实体消歧规则

### 同义词识别

```
叶凡 = 叶天帝 = 荒天帝 → 合并为 C001（叶凡）
神秘玉佩 = 传承玉佩 = 古老玉佩 → 合并为 I001（神秘玉佩）
```

### 同名区分

```
"萧炎"（斗破苍穹）= C001
"萧炎"（同人）= C100
→ 根据上下文区分
```

### 实体变更追踪

```
每次实体状态变更都记录：
{
  "id": "C001",
  "changes": [
    {
      "field": "power_level",
      "old": "炼气3层",
      "new": "炼气4层",
      "chapter": "第15章",
      "reason": "突破"
    }
  ]
}
```

---

## 四、实体数据库

### 存储格式

```markdown
# 实体数据库

## 角色实体
| ID | 名字 | 类型 | 等级 | 状态 | 首次出场 |
|----|------|------|------|------|---------|
| C001 | 叶凡 | 主角 | 炼气3层 | 活跃 | 第1章 |
| C002 | 萧薰儿 | 配角 | 筑基初期 | 活跃 | 第2章 |

## 物品实体
| ID | 名字 | 类型 | 品级 | 所有者 | 状态 |
|----|------|------|------|--------|------|
| I001 | 神秘玉佩 | 法宝 | 未知 | C001 | 持有 |

## 地点实体
| ID | 名字 | 类型 | 控制势力 | 描述 |
|----|------|------|---------|------|
| L001 | 青云门 | 宗门 | F001 | 坐落于青云山 |

## 势力实体
| ID | 名字 | 类型 | 等级 | 领袖 | 状态 |
|----|------|------|------|------|------|
| F001 | 青云宗 | 宗门 | 一流 | C001 | 兴盛 |

## 能力实体
| ID | 名字 | 类型 | 等级 | 拥有者 | 进度 |
|----|------|------|------|--------|------|
| A001 | 焚诀 | 功法 | 黄阶上品 | C001 | 入门 |

## 事件实体
| ID | 名字 | 类型 | 章节 | 参与者 | 结果 |
|----|------|------|------|--------|------|
| E001 | 外门大比 | 比赛 | 第10章 | C001, C002 | C001胜 |
```

---

## 五、实体关系图谱

### 角色关系

```
C001（叶凡）
├── 父亲 → C010
├── 师傅 → C011
├── 恋人 → C002
├── 敌人 → C020
└── 持有 → I001（神秘玉佩）
```

### 势力关系

```
F001（青云宗）
├── 盟友 → F002
├── 敌人 → F003
├── 领地 → L001
└── 成员 → [C001, C002, C003]
```

---

## 六、使用场景

### 写作前

```
/novel-weaver entity list 角色  → 查看有哪些角色
/novel-weaver entity show C001 → 查看主角详细信息
```

### 写作中

```
AI 自动提取新实体 → 提示作者确认
作者确认 → 自动入库
```

### 写作后

```
/novel-weaver entity list 未使用 → 查看未使用的实体
/novel-weaver entity merge → 合并重复实体
/novel-weaver entity report → 生成实体报告
```

### 查找问题

```
/novel-weaver entity orphan → 查找孤立实体（无关联）
/novel-weaver entity conflict → 查找实体冲突
/novel-weaver entity timeline → 查看实体时间线
```
