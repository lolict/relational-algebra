"""
关系代数/主体间关系编程范式
============================
一个基于认知隔离舱、感知总线和窄腰IR的原创编程范式。

核心模块：
  - core: 核心关系代数原语
  - cognitive_isolation: 认知隔离舱实现
  - perception_bus: 感知总线（50通道）
  - phase_analyzer: 认知相位分析器
  - narrow_waist_ir: 窄腰中间表示
  - funnel_frontend: 漏斗前端
  - bootstrap_compiler: 自举编译器
  - attribution: 归属确定性引擎

作者：莫刘连理萝莉兰零离
版本：0.1.0-alpha
"""

__version__ = "0.1.0-alpha"
__author__ = "莫刘连理萝莉兰零离"

from .core import Relation, Operator, Signature
from .cognitive_isolation import IsolationPod, PerspectiveState, PerceptionEvent
from .perception_bus import PerceptionBus
from .phase_analyzer import CognitivePhaseAnalyzer, PhaseVector
from .narrow_waist_ir import IRNode, IRNodeKind, NarrowWaistIR
from .funnel_frontend import FunnelFrontend, LanguageSignature
from .attribution import AttributionEngine, AttributionResult

__all__ = [
    # 核心原语
    "Relation",
    "Operator", 
    "Signature",
    # 隔离舱
    "IsolationPod",
    "PerspectiveState",
    "PerceptionEvent",
    # 感知总线
    "PerceptionBus",
    # 相位分析
    "CognitivePhaseAnalyzer",
    "PhaseVector",
    # 窄腰IR
    "IRNode",
    "IRNodeKind",
    "NarrowWaistIR",
    # 漏斗前端
    "FunnelFrontend",
    "LanguageSignature",
    # 归属
    "AttributionEngine",
    "AttributionResult",
]
