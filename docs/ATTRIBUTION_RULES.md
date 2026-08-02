# 归属确定性规则手册

> 本文档描述主体间关系代数中"谁创造了什么"的归属确定性协议。

## 1. 概述

归属确定性（Attribution Certainty）协议用于确定创作内容的来源——用户原创、AI生成还是平台功能。

### 1.1 三权分立原则

```
┌─────────────────────────────────────────────────────────────┐
│                      归属来源                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐                │
│   │  User   │    │  Agent  │    │ Platform│                │
│   │  用户   │    │ AI代理  │    │  平台   │                │
│   │         │    │         │    │         │                │
│   │ 原创贡献│    │ 代为生成│    │ 自动功能│                │
│   └────┬────┘    └────┬────┘    └────┬────┘                │
│        │              │              │                      │
│        └──────────────┼──────────────┘                      │
│                       ▼                                     │
│              ┌────────────────┐                             │
│              │ Collaboration │                             │
│              │    协作生成    │                             │
│              └────────────────┘                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 2. 归属来源枚举

### 2.1 AttributionSource

```python
class AttributionSource(Enum):
    """归属来源"""
    USER = "user"           # 用户原创
    AGENT = "agent"         # Agent生成
    PLATFORM = "platform"   # 平台功能
    COLLABORATION = "collab"  # 协作生成
    UNKNOWN = "unknown"      # 未知
```

### 2.2 AttributionLevel

```python
class AttributionLevel(Enum):
    """确定性级别"""
    CERTAIN = "certain"     # 确定 (>0.7)
    PROBABLE = "probable"   # 可能 (0.5-0.7)
    POSSIBLE = "possible"   # 也许 (0.3-0.5)
    UNLIKELY = "unlikely"   # 不太可能 (<0.3)
```

## 3. 分析特征

### 3.1 用户词汇特征

| 特征类型 | 关键词/模式 | 归属得分变化 |
|----------|-------------|--------------|
| 人称代词 | 我、我的、咱们 | +0.3 (user) |
| 非正式语体 | 哈、嘿、哇、啦 | +0.2 (user) |
| 具体知识 | 行业专有词汇 | +0.1 (user) |
| 个人经历 | "我记得..."、"我曾经..." | +0.15 (user) |

### 3.2 Agent词汇特征

| 特征类型 | 关键词/模式 | 归属得分变化 |
|----------|-------------|--------------|
| 正式标记 | 因此、综上所述、首先 | +0.25 (agent) |
| 结构标记 | 第一、第二、另一方面 | +0.25 (agent) |
| 模糊词 | 可能、也许、或许 | +0.2 (agent) |
| 过度解释 | 详细的背景介绍 | +0.15 (agent) |

### 3.3 上下文因素

```python
context_features = {
    "is_generation_request": bool,   # 用户请求生成
    "is_original_idea": bool,        # 用户声明原创
    "has_citation": bool,            # 有引用标注
    "is_technical": bool,            # 技术性内容
    "is_personal": bool,            # 个人内容
}
```

## 4. 归属分析流程

### 4.1 分析步骤

```
输入内容 ──► 特征提取 ──► 得分计算 ──► 归属确定 ──► 报告生成
                │              │              │
         ┌─────┴─────┐   ┌────┴────┐    ┌────┴────┐
         │ 词汇统计  │   │ 加权求和│    │ 阈值判断│
         │ 句式分析  │   │ 归一化  │    │ 级别确定│
         └───────────┘   └─────────┘    └─────────┘
```

### 4.2 得分计算公式

```python
def compute_scores(features: dict) -> dict:
    scores = {"user": 0.0, "agent": 0.0, "platform": 0.0}
    
    # 用户特征
    if features.get("has_personal_pronouns"):
        scores["user"] += 0.3
    if features.get("has_informal"):
        scores["user"] += 0.2
    if features.get("has_personal_experience"):
        scores["user"] += 0.15
    
    # Agent特征
    if features.get("has_formal_markers"):
        scores["agent"] += 0.25
    if features.get("has_structure_markers"):
        scores["agent"] += 0.25
    if features.get("has_hedging"):
        scores["agent"] += 0.2
    
    # 上下文因素
    if features.get("is_generation_request"):
        scores["agent"] += 0.3
    if features.get("is_original_idea"):
        scores["user"] += 0.3
    
    # 归一化
    total = sum(scores.values())
    if total > 0:
        scores = {k: v/total for k, v in scores.items()}
    
    # 协作得分
    scores["collab"] = min(0.5, scores["user"] * scores["agent"] * 4)
    
    return scores
```

## 5. 归属分解

### 5.1 百分比分解

```python
breakdown = {
    "user": 0.0-1.0,      # 用户贡献占比
    "agent": 0.0-1.0,     # Agent贡献占比
    "platform": 0.0-1.0,  # 平台贡献占比
}
# 三者之和为 1.0
```

### 5.2 解释标准

| user比例 | agent比例 | 解释 |
|----------|-----------|------|
| > 0.7 | < 0.2 | 主要是用户原创 |
| 0.4-0.7 | 0.2-0.4 | 用户与AI协作 |
| < 0.3 | > 0.6 | 主要是AI生成 |
| > 0.8 | < 0.1 | 完全用户原创 |

## 6. 归属报告格式

### 6.1 JSON格式

```json
{
  "result_id": "attr_1234567890",
  "overall_source": "user",
  "overall_confidence": 0.85,
  "breakdown": {
    "user": 0.85,
    "agent": 0.10,
    "platform": 0.05
  },
  "summary": "主要是用户原创内容",
  "tags": [
    {
      "tag_id": "main",
      "source": "user",
      "confidence": 0.85,
      "description": "主要内容归属 (user: 0.85)"
    }
  ]
}
```

### 6.2 人类可读报告

```
============================================
           归属确定性分析报告
============================================

总体归属：用户原创
置信度：85%

归属分解：
  用户: 85% ███████████████░░░
  AI:   10% ███░░░░░░░░░░░░░░░
  平台:  5% █░░░░░░░░░░░░░░░░░

============================================
```

## 7. 特殊规则

### 7.1 显式声明规则

```python
explicit_declarations = {
    # 用户明确声明的情况
    "这是我想出来的": ("user", 0.95),
    "帮我写": ("agent", 0.9),
    "AI帮我生成的": ("agent", 0.85),
    "平台自动推荐": ("platform", 0.9),
}
```

### 7.2 长度调整规则

```python
def adjust_by_length(scores: dict, text_length: int) -> dict:
    """根据文本长度调整得分"""
    if text_length > 2000:  # 长文本
        scores["agent"] *= 1.2  # AI倾向生成长文本
        scores["user"] *= 0.9
    elif text_length < 50:   # 短文本
        scores["user"] *= 1.1  # 用户倾向短文本
        scores["agent"] *= 0.95
    return scores
```

### 7.3 主题相关性规则

```python
def adjust_by_topic(scores: dict, topics: List[str], user_topics: List[str]) -> dict:
    """根据话题相关性调整"""
    relevant_topics = set(topics) & set(user_topics)
    if relevant_topics:
        scores["user"] *= 1.1  # 用户对熟悉话题更可能原创
    return scores
```

## 8. 使用示例

### 8.1 基本使用

```python
from relational_algebra import AttributionEngine

engine = AttributionEngine()

# 分析内容归属
content = "我觉得这个项目的架构设计很有意思..."
result = engine.analyze(content)

print(f"归属：{result.overall_source.value}")
print(f"置信度：{result.overall_confidence:.0%}")
print(f"用户贡献：{result.user_contribution_ratio():.0%}")
```

### 8.2 带上下文的分析

```python
context = {
    "is_generation_request": False,
    "is_original_idea": True,
    "user_id": "alice",
}

result = engine.analyze(
    content="这是我最近研究的新想法...",
    context=context,
    user_id="alice"
)
```

---

*本文档持续更新中*
