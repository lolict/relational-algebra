# 变更日志

所有重要的项目变更都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)。

## [0.1.0-alpha] - 开发中

### Added

#### 核心模块
- `relational_algebra/__init__.py` - 包初始化，导出核心类型
- `relational_algebra/core.py` - 核心关系代数原语
  - `Relation` - 关系数据结构
  - `Operator` - 关系算子枚举（9种）
  - `Signature` - 算子签名
  - `RelationalAlgebraEngine` - 关系代数引擎

#### 认知隔离舱系统
- `relational_algebra/cognitive_isolation.py` - 认知隔离舱实现
  - `PerspectiveState` - 六种视角状态
  - `PerceptionEvent` - 感知事件
  - `IsolationPod` - 隔离舱主体
- `relational_algebra/memory_point.py` - 记忆点与感知通道
  - `PerceptionChannel` - 50种感知通道枚举
  - `MemoryPoint` - 记忆点数据结构
  - `TimeSlice` / `SpaceSlice` - 时空坐标
- `relational_algebra/perception_bus.py` - 感知总线
  - `PerceptionBus` - 隔离舱间通信中介

#### 编译架构
- `relational_algebra/narrow_waist_ir.py` - 窄腰中间表示
  - `IRNodeKind` - 17种IR节点类型
  - `IRNode` - IR节点数据结构
  - `HomotopyClass` - 同伦等价类
  - `NarrowWaistIR` - IR构建器
- `relational_algebra/funnel_frontend.py` - 漏斗前端
  - `LanguageSignature` - 语言签名识别
  - `FunnelFrontend` - 多语言解析器
- `relational_algebra/bootstrap_compiler.py` - 自举编译器
  - `BootstrapCompiler` - 自举编译链路

#### 分析工具
- `relational_algebra/phase_analyzer.py` - 认知相位分析
  - `PhaseVector` - 8维相位向量
  - `CognitivePhaseAnalyzer` - 相位分析器
- `relational_algebra/attribution.py` - 归属确定性
  - `AttributionEngine` - 归属分析
  - `AttributionResult` - 分析结果

#### 项目配置
- `setup.py` - 安装脚本
- `pyproject.toml` - 现代Python项目配置
- `package.json` - npm配置
- `.gitignore` - Git忽略规则
- `.vscode/settings.json` - VSCode配置
- `.vscode/tasks.json` - VSCode任务

#### 脚本
- `scripts/init-repo.sh` - Git仓库初始化
- `scripts/setup-env.sh` - 环境安装
- `scripts/deploy.sh` - 部署脚本
- `scripts/generate-docs.sh` - 文档生成

#### 文档
- `README.md` - 项目总览
- `PROTOCOL.md` - 协议规范
- `docs/PHILOSOPHY.md` - 哲学基础
- `docs/PROTOCOL_SPEC.md` - 协议详述
- `docs/CAUSAL_LAYERS.md` - 因果层级
- `docs/PHASE_VECTOR.md` - 相位向量
- `docs/ATTRIBUTION_RULES.md` - 归属规则
- `docs/CODE_OF_CONDUCT.md` - 行为准则

#### 数据
- `data/capability-matrix.csv` - 能力边界矩阵
- `data/phase-vectors.csv` - 相位向量数据
- `data/knowledge-plane-edges.csv` - 知识平面边

#### 图表
- `docs/assets/architecture-overview.svg` - 架构总览
- `docs/assets/phase-vector.svg` - 相位雷达图
- `docs/assets/causal-tree.svg` - 因果树

#### 技能定义
- `skills/relational-algebra-ide.skill.toml` - IDE技能
- `skills/cognitive-phase-analyzer.skill.toml` - 相位分析技能
- `skills/attribution-engine.skill.toml` - 归属引擎技能

### Changed

- 初始项目结构搭建

### Fixed

- N/A

### Deprecated

- N/A

### Removed

- N/A

### Security

- N/A

---

## 版本历史

| 版本 | 状态 | 日期 |
|------|------|------|
| 0.1.0-alpha | 开发中 | 2024-XX-XX |
