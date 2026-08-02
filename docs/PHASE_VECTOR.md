# 默认相位向量说明

> 本文档详细描述认知相位分析中使用的8维向量空间的含义和使用方法。

## 1. 概述

相位向量（Phase Vector）是将主体认知状态映射为8维向量空间的数学表示，用于分析和比较不同认知状态。

## 2. 向量维度定义

### 2.1 向量结构

```python
PhaseVector:
    creation: float      # 0.0 - 1.0
    analysis: float      # 0.0 - 1.0
    perception: float    # 0.0 - 1.0
    emotion: float       # 0.0 - 1.0
    social: float         # 0.0 - 1.0
    logic: float          # 0.0 - 1.0
    memory: float          # 0.0 - 1.0
    reflection: float      # 0.0 - 1.0
```

### 2.2 各维度详细说明

| 维度 | 名称 | 含义 | 高值特征 | 低值特征 |
|------|------|------|----------|----------|
| 1 | 创造 (CREATION) | 创造性思维能力 | 创意丰富、想象活跃 | 循规蹈矩、模仿为主 |
| 2 | 分析 (ANALYSIS) | 分析性思维能力 | 逻辑严密、深入剖析 | 浅尝辄止、直觉判断 |
| 3 | 感知 (PERCEPTION) | 感知接收程度 | 敏锐观察、细节丰富 | 忽视细节、抽象思维 |
| 4 | 情感 (EMOTION) | 情感投入程度 | 情感充沛、易共情 | 理性冷静、情感隔离 |
| 5 | 社交 (SOCIAL) | 社交互动倾向 | 善于交际、团队协作 | 独来独往、个人主义 |
| 6 | 逻辑 (LOGIC) | 逻辑推理能力 | 条理清晰、推理严密 | 跳跃思维、情感驱动 |
| 7 | 记忆 (MEMORY) | 记忆检索活跃度 | 回忆丰富、关联广泛 | 遗忘迅速、关注当下 |
| 8 | 反思 (REFLECTION) | 元认知能力 | 自我审视、总结归纳 | 行动导向、不善反思 |

## 3. 向量可视化

### 3.1 雷达图表示

```
                         创造
                          ↑
                          
            分析 ←────────┼────────→ 感知
                          
                ↖         │         ↗
                          │
        逻辑 ─────────────┼──────────── 情感
                          │
                ↙         │         ↘
                          │
            记忆 ←────────┼────────→ 社交
                          │
                         反思
```

### 3.2 示例向量

```python
# 示例：创作模式
creative_phase = PhaseVector(
    creation=0.9,     # 高度创造
    analysis=0.4,     # 较少分析
    perception=0.6,   # 中等感知
    emotion=0.7,      # 情感丰富
    social=0.3,       # 较少社交
    logic=0.4,        # 较少逻辑
    memory=0.6,       # 中等记忆
    reflection=0.5     # 中等反思
)

# 示例：分析模式
analytical_phase = PhaseVector(
    creation=0.3,
    analysis=0.9,
    perception=0.5,
    emotion=0.2,
    social=0.3,
    logic=0.9,
    memory=0.7,
    reflection=0.8
)
```

## 4. 相似度计算

### 4.1 余弦相似度

```python
def cosine_similarity(v1: PhaseVector, v2: PhaseVector) -> float:
    """
    余弦相似度：-1 到 1，1 表示完全相同
    """
    dot = (
        v1.creation * v2.creation +
        v1.analysis * v2.analysis +
        v1.perception * v2.perception +
        v1.emotion * v2.emotion +
        v1.social * v2.social +
        v1.logic * v2.logic +
        v1.memory * v2.memory +
        v1.reflection * v2.reflection
    )
    
    norm1 = sqrt(sum(x**2 for x in v1.to_list()))
    norm2 = sqrt(sum(x**2 for x in v2.to_list()))
    
    return dot / (norm1 * norm2 + 1e-10)
```

### 4.2 欧氏距离

```python
def euclidean_distance(v1: PhaseVector, v2: PhaseVector) -> float:
    """
    欧氏距离：0 到 无穷大，0 表示完全相同
    """
    return sqrt(
        (v1.creation - v2.creation) ** 2 +
        (v1.analysis - v2.analysis) ** 2 +
        (v1.perception - v2.perception) ** 2 +
        (v1.emotion - v2.emotion) ** 2 +
        (v1.social - v2.social) ** 2 +
        (v1.logic - v2.logic) ** 2 +
        (v1.memory - v2.memory) ** 2 +
        (v1.reflection - v2.reflection) ** 2
    )
```

### 4.3 相似度解释

| 余弦相似度 | 欧氏距离 | 解释 |
|------------|----------|------|
| 1.0 | 0.0 | 完全相同 |
| 0.9 - 1.0 | 0.0 - 0.3 | 高度相似 |
| 0.7 - 0.9 | 0.3 - 0.7 | 中度相似 |
| 0.5 - 0.7 | 0.7 - 1.2 | 低度相似 |
| < 0.5 | > 1.2 | 显著不同 |

## 5. 默认相位模板

### 5.1 常用模板

```python
class DefaultPhases:
    """预定义的默认相位"""
    
    CREATIVE = PhaseVector(
        creation=0.8, analysis=0.4, perception=0.6,
        emotion=0.7, social=0.3, logic=0.4,
        memory=0.5, reflection=0.5
    )
    
    ANALYTICAL = PhaseVector(
        creation=0.3, analysis=0.9, perception=0.5,
        emotion=0.2, social=0.3, logic=0.9,
        memory=0.7, reflection=0.8
    )
    
    BALANCED = PhaseVector(
        creation=0.5, analysis=0.5, perception=0.5,
        emotion=0.5, social=0.5, logic=0.5,
        memory=0.5, reflection=0.5
    )
    
    EMOTIONAL = PhaseVector(
        creation=0.5, analysis=0.3, perception=0.7,
        emotion=0.9, social=0.6, logic=0.2,
        memory=0.6, reflection=0.4
    )
    
    LOGICAL = PhaseVector(
        creation=0.4, analysis=0.8, perception=0.5,
        emotion=0.2, social=0.3, logic=0.9,
        memory=0.5, reflection=0.7
    )
    
    SOCIAL = PhaseVector(
        creation=0.5, analysis=0.4, perception=0.6,
        emotion=0.6, social=0.9, logic=0.4,
        memory=0.5, reflection=0.4
    )
    
    REFLECTIVE = PhaseVector(
        creation=0.5, analysis=0.6, perception=0.5,
        emotion=0.4, social=0.4, logic=0.6,
        memory=0.7, reflection=0.9
    )
```

## 6. 相位比较分析

### 6.1 冲突检测

```python
def detect_conflicts(v1: PhaseVector, v2: PhaseVector, threshold: float = 0.5) -> List[Dict]:
    """
    检测两个相位之间的冲突
    
    冲突定义：同一维度差异 > threshold
    """
    conflicts = []
    dims = [
        ("创造", v1.creation, v2.creation),
        ("分析", v1.analysis, v2.analysis),
        ("感知", v1.perception, v2.perception),
        ("情感", v1.emotion, v2.emotion),
        ("社交", v1.social, v2.social),
        ("逻辑", v1.logic, v2.logic),
        ("记忆", v1.memory, v2.memory),
        ("反思", v1.reflection, v2.reflection),
    ]
    
    for name, val1, val2 in dims:
        if abs(val1 - val2) > threshold:
            conflicts.append({
                "dimension": name,
                "phase1_value": val1,
                "phase2_value": val2,
                "difference": abs(val1 - val2)
            })
    
    return conflicts
```

### 6.2 相位报告生成

```python
def generate_phase_report(vector: PhaseVector) -> str:
    """生成人类可读的相位报告"""
    dominant = vector.dominant_dimension()
    
    report = f"""
{'='*40}
认知相位分析报告
{'='*40}
主导维度: {dominant.value}
向量模长: {vector.magnitude():.3f}

各维度得分:
"""
    
    dims = vector.to_dict()
    for name, value in dims.items():
        bar = "█" * int(value * 10) + "░" * (10 - int(value * 10))
        report += f"  {name}: [{bar}] {value:.2f}\n"
    
    return report
```

## 7. 使用场景

### 7.1 认知状态追踪

```python
# 记录不同时刻的相位
phases = [
    analyzer.analyze_text("今天要写一篇创意文章"),
    analyzer.analyze_text("现在来分析一下数据结构"),
    analyzer.analyze_text("和大家一起讨论项目"),
]

# 比较相位变化
for i in range(len(phases) - 1):
    comparison = analyzer.compare_phases(phases[i], phases[i+1])
    print(f"相位{i} → 相位{i+1}: 相似度={comparison['cosine_similarity']:.2f}")
```

### 7.2 最优组合生成

```python
# 从多个候选相位中选择最优组合
candidates = [creative_phase, analytical_phase, emotional_phase]
optimal = analyzer.find_optimal_blend(candidates, weights=[0.5, 0.3, 0.2])
```

---

*本文档持续更新中*
