# 协议规范详述

> 本文档详细描述主体间关系代数协议的各个子协议。

## 目录

1. [认知隔离舱协议](#1-认知隔离舱协议)
2. [感知总线协议](#2-感知总线协议)
3. [窄腰IR协议](#3-窄腰ir协议)
4. [漏斗前端协议](#4-漏斗前端协议)
5. [自举编译协议](#5-自举编译协议)
6. [认知相位协议](#6-认知相位协议)
7. [归属确定性协议](#7-归属确定性协议)

---

## 1. 认知隔离舱协议

### 1.1 概述

认知隔离舱（Cognitive Isolation Pod）是主体间关系代数的基本执行单元，代表一个独立的认知主体。

### 1.2 视角状态机

隔离舱具有六种视角状态：

```
                    ┌─────────┐
                    │  待命   │ (IDLE)
                    │ (IDLE)  │
                    └────┬────┘
                         │
              切换请求    ▼
         ┌────────────────────────┐
         │                        │
         ▼                        ▼
    ┌─────────┐             ┌─────────┐
    │  活跃   │◄───────────►│  旁观   │
    │(ACTIVE) │   感知坍缩   │(OBSERVER│
    └────┬────┘             └────┬────┘
         │                        │
         │                        │
         ▼                        │
    ┌─────────┐                   │
    │  体验   │◄──────────────────┘
    │(EXPERI)│   感知事件触发
    └────┬────┘
         │
         ▼
    ┌─────────┐
    │  创造   │
    │(CREATOR)│
    └────┬────┘
         │
         ▼
    ┌─────────┐
    │  梦境   │
    │(DREAMING│
    └─────────┘
```

### 1.3 隔离边界规则

```
┌─────────────────────────────────────────────────────────────┐
│                      隔离舱 A                               │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ 私有记忆库                                            │  │
│  │ - 记忆点 1, 2, 3...                                 │  │
│  │ - 工作记忆                                            │  │
│  │ - 视角状态                                            │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                             │
│  感知过滤器 ──────────────────────────────────► [感知总线]  │
│  允许通道: {SIGHT, EMOTION, ...}                           │
└─────────────────────────────────────────────────────────────┘
```

**隔离原则**：
1. 私有记忆库不可被外部直接访问
2. 感知必须通过感知过滤器
3. 视角切换需要协调器授权

### 1.4 数据结构

```python
@dataclass
class IsolationPod:
    pod_id: str              # 唯一标识
    owner_name: str          # 拥有者名称
    memory_points: List[MemoryPoint]      # 私有记忆
    working_memory: Dict[str, Any]        # 工作记忆
    perspective_state: PerspectiveState   # 当前视角
    known_other_pods: Set[str]            # 已认知的其他舱
    perception_buffer: List[PerceptionEvent]  # 待处理感知
```

---

## 2. 感知总线协议

### 2.1 概述

感知总线（Perception Bus）是隔离舱之间的通信中介，实现"认知隔离被打破"的发生点。

### 2.2 50种感知通道

| 层次 | 通道 | 说明 |
|------|------|------|
| 基础感官 | SIGHT, HEARING, SMELL, TASTE, TOUCH | 视觉、听觉、嗅觉、味觉、触觉 |
| 身体状态 | HUNGER, THIRST, FATIGUE, SLEEP, PAIN, WARMTH, COLDNESS, ILLNESS, WEIGHT, BALANCE | 10种内感受 |
| 情感 | EMOTION, INTIMACY, DISTANCE, PLEASURE, BADNESS | 5种情感通道 |
| 抽象认知 | ETHICS, PSYCHOLOGY, PHYSIOLOGY, COMMON_SENSE, RIGHT_WRONG, QUANTITY, CLUMSINESS, HUMOR, BANTER, FUN, EMBARRASSMENT | 11种认知 |
| 场域 | FIELD, TIME_SPACE, ENVIRONMENT, TEMPERATURE, NATURE | 5种场域感知 |
| 社会想象 | FAMILY, PERSON, OBJECT, INSECT, GRASS, TREE, FLOWER, BEAST, FANTASY, TASTE_SENSE | 10种社会想象 |

### 2.3 emit_sync 广播语义

```
隔离舱 A ──emit_sync──► [感知总线] ──► 隔离舱 B (observable)
                               │
                               ├──► 隔离舱 C (observable)
                               │
                               └──► 隔离舱 D (not observable, 过滤)

规则：
1. 事件记录到 event_log
2. 每个隔离舱的 receive_perception() 被调用
3. 只有 is_observable_by() 返回 True 的舱收到事件
```

### 2.4 可观测性规则

```python
def is_observable_by(self, pod: IsolationPod) -> bool:
    # 规则1: 目标列表限制
    if self.target_pods and pod.pod_id not in self.target_pods:
        return False
    
    # 规则2: 视角过滤器
    if self.visibility_filter and not self.visibility_filter(pod):
        return False
    
    # 规则3: 自我不能感知自我
    return self.source_pod != pod.pod_id
```

---

## 3. 窄腰IR协议

### 3.1 概述

窄腰中间表示（Narrow-Waist IR）是统一的语义表示，所有语言通过漏斗压缩后都转换为这种表示。

### 3.2 几何范畴基础

```
几何原子：
⊙ POINT      - 零维点（单元/身份）
─ LINE       - 一维线段（态射）
▢ PLANE      - 二维关系面
⬡ VOLUME     - 三维关系体
↕ FIBER     - 纤维（垂直截面）
→ MORPHISM   - 态射（空间变换）
↚ CONTRAVARIANT - 反变态射
≅ EQUIVALENCE  - 同伦等价
```

### 3.3 17种IR节点类型

| 类别 | 节点 | 说明 |
|------|------|------|
| 存在性 | UNIT, VOID, WITNESS | 单元、空、同伦见证 |
| 空间变换 | PROJECT, INJECT, LIFT | 投影、注入、提升 |
| 关系构造 | PRODUCT, COPRODUCT, EXPONENTIAL, EQUALIZER, COEQUALIZER | 卡氏积、余积、指数、等化子 |
| 时间因果 | CAUSE, EFFECT, PARALLEL | 因、果、并行 |
| 范畴编织 | BRAID, TWIST, COHERENCE | 编织、扭转、协调 |

### 3.4 同伦等价类

```
漏斗压缩示意：

Python: def f(x): return x + 1
        ↓ 解析
AST: FunctionDef(name='f', body=[Return(x+1)])
        ↓ 转换
IR: PRODUCT(UNIT('f'), EXPONENTIAL(UNIT('x'), UNIT('x+1')))
        ↓ 同伦合并
同伦类: [所有一元函数] → 同一个等价类
```

---

## 4. 漏斗前端协议

### 4.1 语言识别

```python
@staticmethod
def detect(source_code: str, filename: str = "") -> str:
    """
    1. 扩展名匹配（优先级最高）
    2. 关键词扫描
    3. 返回得分最高的语言
    """
```

### 4.2 解析流程

```
源码 ──► 语言识别 ──► 语法解析 ──► 标准化AST ──► IR降维 ──► 窄腰IR
         │              │              │            │
    LanguageSignature  Parser    StandardAST    FunnelFrontend
```

### 4.3 支持的语言

| 语言 | 扩展名 | 特征关键词 |
|------|--------|-----------|
| Python | .py | def, import, self. |
| JavaScript | .js, .mjs | function, const, let |
| Rust | .rs | fn, let mut, impl |
| Go | .go | func, package, := |
| Haskell | .hs, .lhs | module, data, where |
| C | .c, .h | #include, int main |
| 关系代数 | .rel, .dl, .pl | INPUT, OUTPUT, :- |

---

## 5. 自举编译协议

### 5.1 编译链路

```
源语言 ──► 漏斗前端 ──► 窄腰IR ──► 语义分析 ──► 优化 ──► 字节码
                         │                          │
              NarrowWaistIR              BootstrapCompiler
```

### 5.2 字节码格式

```
字节码结构：
[opcode(1 byte)][operand(4 bytes)][0x00 separator]...

操作码映射：
0x01 UNIT    0x02 VOID     0x03 WITNESS
0x10 PROJECT  0x11 INJECT   0x12 LIFT
0x20 PRODUCT  0x21 COPRODUCT 0x22 EXPONENTIAL
0x30 CAUSE    0x31 EFFECT   0x32 PARALLEL
0x40 BRAID    0x41 TWIST    0x42 COHERENCE
```

---

## 6. 认知相位协议

### 6.1 8维向量空间

```python
@dataclass
class PhaseVector:
    creation: float      # 创造维度
    analysis: float      # 分析维度
    perception: float    # 感知维度
    emotion: float       # 情感维度
    social: float         # 社交维度
    logic: float          # 逻辑维度
    memory: float          # 记忆维度
    reflection: float      # 反思维度
```

### 6.2 相位相似度

```python
def cosine_similarity(self, other: PhaseVector) -> float:
    """余弦相似度：值越接近1表示越相似"""
    dot = sum(a*b for a, b in zip(self.to_list(), other.to_list()))
    norm = self.magnitude() * other.magnitude()
    return dot / (norm + 1e-10)

def distance_to(self, other: PhaseVector) -> float:
    """欧氏距离：值越小表示越接近"""
    return sqrt(sum((a-b)**2 for a, b in zip(self.to_list(), other.to_list())))
```

---

## 7. 归属确定性协议

### 7.1 三权分立

| 主体 | 标识 | 说明 |
|------|------|------|
| User | user | 用户原创贡献 |
| Agent | agent | AI代为生成 |
| Platform | platform | 平台自动功能 |
| Collaboration | collab | 协作生成 |

### 7.2 归属分析维度

```python
features = {
    "personal_pronouns": bool,   # 我、我的
    "informal_markers": bool,    # 哈、嘿
    "formal_markers": bool,      # 因此、综上所述
    "structure_markers": bool,   # 第一、第二
    "hedging": bool,             # 可能、也许
    "length": int,               # 文本长度
}
```

### 7.3 归属报告格式

```json
{
  "result_id": "attr_123456",
  "overall_source": "user",
  "overall_confidence": 0.85,
  "breakdown": {
    "user": 0.85,
    "agent": 0.10,
    "platform": 0.05
  },
  "summary": "主要是用户原创内容"
}
```

---

## 附录：协议版本

| 版本 | 日期 | 变更 |
|------|------|------|
| 0.1.0-alpha | 2024-XX-XX | 初始版本 |
