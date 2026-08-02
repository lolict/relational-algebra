# 主体间关系代数/编程新范式

> **原创声明**：本项目是由莫刘连理萝莉兰零离独立构思、设计和实现的新型编程范式，尚未在工业界统一落地。

## 项目简介

主体间关系代数（Inter-Subjective Relational Algebra）是一种全新的编程范式，将人类认知过程中的"主体间性"概念形式化为可计算的数学体系。

### 核心架构

本项目包含三大核心架构：

#### 1. 认知隔离舱系统（Cognitive Isolation Pods）

每个隔离舱代表一个独立的认知主体，拥有：
- **私有记忆库**：按感知通道分类的记忆点
- **视角状态机**：待命/活跃/旁观/创造/体验/梦境
- **感知过滤**：基于通道的可观测性规则

```
┌─────────────────────────────────────────────┐
│           认知隔离舱 (Alice)                │
│  ┌─────────────────────────────────────┐   │
│  │  记忆点 1: [视觉][情感] 看到玫瑰     │   │
│  │  记忆点 2: [听觉][亲密] 听到脚步声   │   │
│  │  记忆点 3: [身体] 感到饥饿           │   │
│  └─────────────────────────────────────┘   │
│  视角状态: [活跃]                           │
└─────────────────────────────────────────────┘
        ↕ 感知总线
┌─────────────────────────────────────────────┐
│           认知隔离舱 (Bob)                  │
│  视角状态: [旁观]                           │
└─────────────────────────────────────────────┘
```

#### 2. 漏斗式编译架构（Funnel Compiler）

```
大开口（任意语言）→ 漏斗窄化 → 窄腰 IR → 自举编译 → 目标代码
    Python                  ↓
    JavaScript              统一中间表示（17种节点）
    Rust                    几何范畴论约束
    Haskell                 同伦等价压缩
    Go                      ↓
    ...                  小出口（零依赖字节码）
```

**漏斗前端**：自动识别编程语言，解析为标准化 AST

**窄腰 IR**：17 种不可再分的关系操作，覆盖所有语言语义

**自举编译器**：用关系代数自身实现，零外部依赖

#### 3. 认知相位分析（Cognitive Phase Analysis）

将主体认知映射为 8 维向量空间：

| 维度 | 说明 | 典型值 |
|------|------|--------|
| 创造 | 创意生成 | 0.0-1.0 |
| 分析 | 逻辑推理 | 0.0-1.0 |
| 感知 | 感觉输入 | 0.0-1.0 |
| 情感 | 情绪状态 | 0.0-1.0 |
| 社交 | 交互倾向 | 0.0-1.0 |
| 逻辑 | 理性思维 | 0.0-1.0 |
| 记忆 | 回忆检索 | 0.0-1.0 |
| 反思 | 元认知 | 0.0-1.0 |

### 技术特性

| 特性 | 说明 |
|------|------|
| 多语言统一 | 一次实现，多语言源码直接编译 |
| 自举编译 | 编译器本身用本范式实现 |
| 零依赖 | 编译产物无外部运行时依赖 |
| 认知建模 | 支持多主体认知状态模拟 |
| 感知总线 | 50 种感知通道的事件驱动通信 |

### 项目结构

```
relational_algebra/
├── __init__.py           # 包初始化
├── core.py               # 核心关系代数原语
├── cognitive_isolation.py # 认知隔离舱
├── perception_bus.py     # 感知总线
├── memory_point.py       # 记忆点（50通道）
├── phase_analyzer.py     # 认知相位分析
├── narrow_waist_ir.py     # 窄腰中间表示
├── funnel_frontend.py     # 漏斗前端
├── bootstrap_compiler.py  # 自举编译器
└── attribution.py         # 归属确定性
```

## 安装

```bash
pip install .
```

## 快速开始

```python
from relational_algebra import (
    IsolationPod,
    PerceptionBus,
    PerspectiveState,
    PerceptionChannel,
)

# 创建感知总线
bus = PerceptionBus()

# 创建两个隔离舱
alice = IsolationPod("alice", "Alice")
bob = IsolationPod("bob", "Bob")

# 注册到总线
bus.register(alice)
bus.register(bob)

# Alice 创建记忆
alice.remember(
    description="看到Bob在笑",
    channels={PerceptionChannel.SIGHT, PerceptionChannel.EMOTION},
    intensity=0.9
)

# 广播感知事件
bus.broadcast(
    source_pod_id="alice",
    description="分享我的快乐",
    channels={PerceptionChannel.EMOTION}
)

# 切换到体验视角
bob.switch_perspective(PerspectiveState.EXPERIENCER)

# Bob 回忆感知到的事件
memories = bob.recall(channels={PerceptionChannel.EMOTION})
print(f"Bob 回忆起了 {len(memories)} 条情感记忆")
```

## 文档

- [协议规范](./docs/PROTOCOL_SPEC.md) - 完整的协议文档
- [思想史与哲学基础](./docs/PHILOSOPHY.md) - 理论基础
- [时序因果7层](./docs/CAUSAL_LAYERS.md) - 因果结构
- [默认相位向量](./docs/PHASE_VECTOR.md) - 8维向量说明
- [归属确定性规则](./docs/ATTRIBUTION_RULES.md) - 归属协议

## 协议

本项目采用 **BSD-3-Clause 修改版协议**（见 LICENSE 文件），额外增加了主体间关系条款：

> **主体间关系条款**：
> 使用本协议实现的代码，在多个认知隔离舱之间进行交互时，
> 必须保留各舱室的认知边界，不得通过技术手段绕过感知过滤规则。

## 作者

**莫刘连理萝莉兰零离**

## 许可证

BSD-3-Clause-Modified（见 LICENSE 文件）
