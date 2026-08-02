# 主体间关系代数协议

> **原创声明**：本协议是由莫刘连理萝莉兰零离设计的原创协议，定义了主体间关系代数编程范式的核心规范。

## 目录

1. [协议概述](#1-协议概述)
2. [认知隔离舱协议](#2-认知隔离舱协议)
3. [感知总线协议](#3-感知总线协议)
4. [窄腰IR协议](#4-窄腰ir协议)
5. [漏斗前端协议](#5-漏斗前端协议)
6. [自举编译协议](#6-自举编译协议)
7. [认知相位协议](#7-认知相位协议)
8. [归属确定性协议](#8-归属确定性协议)
9. [许可证](#9-许可证)

---

## 1. 协议概述

### 1.1 协议目的

本协议定义了主体间关系代数（Inter-Subjective Relational Algebra）的基础规范，用于：

- 建模多个认知主体之间的交互
- 统一表示多语言编程范式
- 实现自举编译的零依赖运行时

### 1.2 核心原则

1. **认知隔离**：每个主体拥有独立的认知边界
2. **感知过滤**：通过通道机制控制信息流动
3. **窄腰统一**：所有语言收敛到统一的中间表示
4. **自举完备**：编译器用自身实现

---

## 2. 认知隔离舱协议

### 2.1 视角状态

隔离舱（IsolationPod）具有六种视角状态：

| 状态 | 标识 | 说明 |
|------|------|------|
| 待命 | IDLE | 休眠状态，不处理感知 |
| 活跃 | ACTIVE | 当前前台运行的视角 |
| 旁观 | OBSERVER | 观察其他隔离舱的活动 |
| 创造 | CREATOR | 正在生成新内容 |
| 体验 | EXPERIENCER | 正在经历/接收感知 |
| 梦境 | DREAMING | 回忆/幻想模式 |

### 2.2 隔离边界

```
┌─────────────────────────────────────────────────────────────┐
│                      隔离舱 A                                │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ 私有记忆库（不可被外部直接访问）                       │  │
│  │ - MemoryPoint[]                                      │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                             │
│  感知过滤器 ──► [感知总线]                                  │
└─────────────────────────────────────────────────────────────┘
```

### 2.3 状态转换规则

- 任何状态都可转换到 IDLE
- ACTIVE 可转换到 OBSERVER（感知坍缩触发）
- EXPERIENCER 可转换到 CREATOR（主动创造）
- DREAMING 可通过时间到期转换到 IDLE

---

## 3. 感知总线协议

### 3.1 50种感知通道

| 层次 | 数量 | 通道名称 |
|------|------|----------|
| 基础感官 | 5 | SIGHT, HEARING, SMELL, TASTE, TOUCH |
| 身体状态 | 10 | HUNGER, THIRST, FATIGUE, SLEEP, PAIN, WARMTH, COLDNESS, ILLNESS, WEIGHT, BALANCE |
| 情感 | 5 | EMOTION, INTIMACY, DISTANCE, PLEASURE, BADNESS |
| 抽象认知 | 11 | ETHICS, PSYCHOLOGY, PHYSIOLOGY, COMMON_SENSE, RIGHT_WRONG, QUANTITY, CLUMSINESS, HUMOR, BANTER, FUN, EMBARRASSMENT |
| 场域 | 5 | FIELD, TIME_SPACE, ENVIRONMENT, TEMPERATURE, NATURE |
| 社会想象 | 10 | FAMILY, PERSON, OBJECT, INSECT, GRASS, TREE, FLOWER, BEAST, FANTASY, TASTE_SENSE |

### 3.2 emit_sync 广播语义

```python
def emit_sync(event: PerceptionEvent) -> List[IsolationPod]:
    """
    同步广播流程：
    1. 记录到 event_log
    2. 对每个注册的隔离舱调用 receive_perception()
    3. 返回所有接收到的隔离舱列表
    """
```

### 3.3 可观测性规则

事件对隔离舱可见当且仅当：

1. 目标列表为空（广播）或包含该隔离舱
2. 通过视角过滤器
3. 源不是该隔离舱本身

---

## 4. 窄腰IR协议

### 4.1 几何原子

| 符号 | 名称 | 维度 |
|------|------|------|
| ⊙ | POINT | 零维 |
| ─ | LINE | 一维 |
| ▢ | PLANE | 二维 |
| ⬡ | VOLUME | 三维 |
| ↕ | FIBER | 纤维 |
| → | MORPHISM | 态射 |
| ↚ | CONTRAVARIANT | 反变 |
| ≅ | EQUIVALENCE | 同伦 |

### 4.2 17种IR节点类型

| 类别 | 节点 | 功能 |
|------|------|------|
| 存在性 | UNIT | 单元/身份 |
| | VOID | 空/未定义 |
| | WITNESS | 同伦见证 |
| 空间变换 | PROJECT | 投影（漏斗窄化） |
| | INJECT | 注入 |
| | LIFT | 提升 |
| 关系构造 | PRODUCT | 卡氏积（AND） |
| | COPRODUCT | 余积（OR） |
| | EXPONENTIAL | 指数（λ） |
| | EQUALIZER | 等化子 |
| | COEQUALIZER | 余等化子 |
| 时间因果 | CAUSE | 因果发射 |
| | EFFECT | 效果接收 |
| | PARALLEL | 并行 |
| 范畴编织 | BRAID | 编织（身份切换） |
| | TWIST | 扭转（视角反转） |
| | COHERENCE | 协调性约束 |

---

## 5. 漏斗前端协议

### 5.1 语言识别

支持的语言和识别特征：

| 语言 | 扩展名 | 特征关键词 |
|------|--------|-----------|
| Python | .py | def, import, self. |
| JavaScript | .js, .mjs | function, const, let |
| Rust | .rs | fn, let mut, impl |
| Go | .go | func, package, := |
| Haskell | .hs, .lhs | module, data, where |
| C | .c, .h | #include, int main |
| 关系代数 | .rel, .dl, .pl | INPUT, OUTPUT, :- |

### 5.2 编译流程

```
源码 → 语言识别 → 语法解析 → 标准化AST → IR降维 → 同伦合并 → 窄腰IR
```

---

## 6. 自举编译协议

### 6.1 编译链路

```
窄腰IR → 语义分析 → 优化遍 → 字节码生成
```

### 6.2 字节码格式

每条指令：`[opcode: 1 byte][operands: n bytes][separator: 0x00]`

操作码表（十六进制）：
- 0x01-0x03：存在性
- 0x10-0x12：空间变换
- 0x20-0x24：关系构造
- 0x30-0x32：时间因果
- 0x40-0x42：范畴编织

---

## 7. 认知相位协议

### 7.1 8维向量空间

| 维度 | 范围 | 说明 |
|------|------|------|
| 创造 | 0.0-1.0 | 创造性思维 |
| 分析 | 0.0-1.0 | 分析性思维 |
| 感知 | 0.0-1.0 | 感知接收 |
| 情感 | 0.0-1.0 | 情感投入 |
| 社交 | 0.0-1.0 | 社交倾向 |
| 逻辑 | 0.0-1.0 | 逻辑推理 |
| 记忆 | 0.0-1.0 | 记忆检索 |
| 反思 | 0.0-1.0 | 元认知 |

### 7.2 相似度计算

```python
cosine_similarity = dot(v1, v2) / (|v1| * |v2|)
euclidean_distance = sqrt(sum((a-b)^2))
```

---

## 8. 归属确定性协议

### 8.1 三权分立

| 来源 | 标识 | 权重基础 |
|------|------|----------|
| 用户 | user | 0.3 |
| AI | agent | 0.25 |
| 平台 | platform | 0.1 |
| 协作 | collab | 0.2 |

### 8.2 归属分解

```python
breakdown = {
    "user": 0.0-1.0,
    "agent": 0.0-1.0,
    "platform": 0.0-1.0,
}
# 三者之和为1.0
```

---

## 9. 许可证

本协议采用 **BSD-3-Clause 修改版**，额外包含主体间关系条款。

完整许可证文本请参阅 [LICENSE](../LICENSE) 文件。

---

*协议版本：0.1.0-alpha*
*最后更新：2024年*
