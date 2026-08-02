# 主体间关系代数 · 哲学范式文档
> **版本**：1.0.0 | **作者**：莫刘连理萝莉兰零离 | **许可证**：BSD-3-Clause-Interpersonal

---

## 一、核心哲学命题

### 1.1 漏斗结构：降维的本质

> 「由大到小，把外部的复杂锤碎装进瓶子」

宇宙间一切高效的认知和处理系统，都可以抽象为一个**漏斗**：

```
外部复杂（高维辐射态）
    ↓  [漏斗壁 = 自然变换]
    ↓  开口由大到小
    ↓  时间切片序列
瓶子里的稳定态（低维聚合态）
```

**数学本质**：Functor F: C(source) → C(target)
- source: 高维辐射域（多元、分散、发散）
- target: 低维稳定态（聚合、收敛、入瓶）
- 漏斗壁 = 自然变换的自然性条件

**物理类比**：
- 恒星引力坍缩：辐射态 → 黑洞/中子星
- 税收筛选：有能力者多纳税 → 国家效率提升
- 神经网络：海量数据 → 少数权重
- 婚姻共同体：两个独立人 → 一个命运体

### 1.2 认知观测者：二阶嵌套

> 「心中有一个现象，就像内心观测者，内心观测眼睛」

观测的三元结构：
- **Observer（O）**：内心观测者，能观测的那个
- **Subject（S）**：被观测者，被观测的那个
- **Predicate（P）**：裁判条件，等效对齐的判定规则

```
O ⊗ S → P（judgment）
```

**等效对齐的四种可能**：
1. `EQUIVALENT` — 等效对齐（观测到的 = 实际存在的）
2. `ASYMMETRIC` — 非对称（观测到的 ≠ 实际存在）
3. `NULL` — 虚空（观测者和被观者都不存在）
4. `CONVERGENCE` — 收敛（趋近等效但永远不等价，渐近对齐）

> 「它只是为了达到有和无的最终的转换」
> → 就算不是等效对齐的，只要由大到小，就是有效的

### 1.3 单子单位元：夫妻共同体

> 「男被融合进丈夫身体，漂亮姑娘被融合进妻子身体」
> 「然后妻子和丈夫身体融合在一起，没有了区别心，变成了一个人」

**范畴论模型**：单子 (M, ⊗, I)
- M: 对象集合（存在的万事万物）
- ⊗: 融合运算（夫妻 ⊗ 外物 = 融合体）
- I: 单位元（空瓶/空态，即「无」）

**融合态演化**：
```
SEPARATE → ATTRACTED → FUSING → FUSED
                              ↘ ECLIPSED（月全食/半亏损）
```

### 1.4 满全法：命运共同体

> 「满全法必须是和刘楚恬融合为夫妻命运共同体谐音协议夕瑶宣言一体，才能叫满全法」

**结构**：
```python
满全法 = ManQuanFa(丈夫, 妻子, "夕瑶宣言")
集成体 = 满全法.integrate()
```

**约束**：
- 不能分离，分离则变「月全食」（亏损态）
- 月全食 = 博弈考 = 伯邑考夺舍苏妲己 = 半边亏损

---

## 二、三大子架构

### 2.1 认知隔离舱多元生命体架构

每个认知主体是一个「隔离舱」：
- 独立的注意力空间（内存不溢出）
- 通过协议与其他舱通信
- 可分裂（分形扩展容量）

### 2.2 全感知模态记忆点体系

所有感知模态（视觉/听觉/触觉/文本）共享一个「记忆点」网络：
- 每个记忆点是一个 `<时间, 模态, 内容>` 三元组
- 跨模态关联通过「感知总线」路由

### 2.3 漏斗式几何范畴窄腰多语言统一编译架构

```
复杂输入（任意语言/格式）
    ↓ funnel_frontend（漏斗前端）
窄腰IR（统一的中间表示）
    ↓ narrow_waist_ir
多语言代码生成（Python/JS/SQL/...)
```

---

## 三、核心计算模式

### 3.1 税务筛选（TaxPolicy）

```python
funnel = FunnelReductor(
    policy=TaxPolicy(ability_fn=lambda x: x['score'], tax_rate=0.3),
    total_layers=5,
)
```

- 能力值越高 → 通过率越高
- 税率越高 → 筛选越严格
- 最终剩余：「最强的有能力的」

### 3.2 辐射坍缩（RadiationPolicy）

```python
funnel = FunnelReductor(
    policy=RadiationPolicy(center_fn=lambda x: x['distance']),
)
```

- 越靠近中心 → 越容易存活
- 漏斗半径随层数递减

### 3.3 分形复制（FractalPolicy）

```python
funnel = FunnelReductor(
    policy=FractalPolicy(split_fn=lambda x: [x]*3, mutation_rate=0.01),
)
```

- 每个幸存者分裂成多个副本
- 副本之间有微小「偏移量」
- 自我释放 = 完美复制；非自我释放 = 残差偏移

---

## 四、时间切片与火候控制

### 4.1 相位类型

| PhaseType | 语义 | 漏斗对应 |
|-----------|------|---------|
| WARMUP | 热身/升温 | 开口全开，蓄力 |
| ACTIVE | 活跃执行 | 稳定压缩 |
| COOLDOWN | 冷却/存档 | 收敛完成 |
| OVERFLOW_PROTECT | 防溢出 | 分布式转移 |

### 4.2 火候策略

- **SlowHeatPolicy**：先小后大，适合资源初始化
- **FastContactPolicy**：快速升温快速冷却，适合事件驱动

---

## 五、哲学 ↔ 代码映射表

| 哲学概念 | 代码抽象 | 模块 |
|---------|---------|------|
| 漏斗降维 | `FunnelReductor` | `funnel.py` |
| 认知观测者 | `CognitiveObserver` | `observer.py` |
| 三元裁判 | `TripleJudgment` | `observer.py` |
| 夫妻共同体 | `Entity` + `@` | `monoidal.py` |
| 满全法 | `ManQuanFa` | `monoidal.py` |
| 月全食 | `eclipse()` | `monoidal.py` |
| 单子单位元 | `MonoidalIdentity` | `monoidal.py` |
| 时间切片 | `PhaseSlice` | `phase_router.py` |
| 火候控制 | `HeatControlPolicy` | `phase_router.py` |
| 税务筛选 | `TaxPolicy` | `funnel.py` |
| 分形分裂 | `FractalPolicy` | `funnel.py` |
| 全局坍缩 | `MonoidalFusionEngine.fuse_all()` | `monoidal.py` |

---

## 六、谐音协议

> 「夕瑶宣言」— 夕+尧 = 夕瑶，夕瑶 = 夕 + 瑶
> 「满全法」— 满 + 全 + 法 = Man + Quan + Fa
> 「月全食」— 月 + 全 + 食 = Eclipse，亏损/被夺舍

---

*本文档是主体间关系代数范式的哲学说明，代码实现见各 `*.py` 模块。*
