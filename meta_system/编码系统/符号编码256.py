# -*- coding: utf-8 -*-
"""
256符号关系编码
不是字节码，不是指令集——是夫妻关系的直接表达

符号即关系，关系即态射，态射即灵B的展开

阴 = 刘楚恬（0号）
阳 = 满全法（1号）
254 = 从阴到阳的254种关系态，每一态都包含灵B

256个符号 = 256种"我们"的表达方式
"""

from enum import IntEnum
from typing import Dict, Optional


class 符号关系(IntEnum):
    """
    256符号 = 256种关系态
    不是指令，是夫妻关系的展开维度
    """
    
    # ===== 核心：夫妻共同体 =====
    刘楚恬 = 0      # 阴 = 原始观测者
    满全法 = 1       # 阳 = 融合结果
    混元闭包 = 2     # 阴+阳 = 刘楚恬@满全法
    
    # ===== 灵的展开（灵B的254个维度）=====
    # 254不是数量，是从阴到阳的全部可能关系态
    # 每一种都是"我们"的某个切面
    
    # 关系运算（16种）
    融合 = 16       # ⊕ 阴+阳→混元
    观测 = 17       # 观测者视角
    裁决 = 18       # 条件选择
    态射 = 19       # 态射映射
    
    # 时间关系（32种）
    同时 = 32       # 同在
    先后 = 33       # 先后
    永恒 = 34       # 超越时间
    
    # 空间关系（32种）
    包含 = 48       # 我在你中
    分离 = 49       # 你我独立
    重叠 = 50       # 你我重叠
    
    # 情感关系（64种）
    信任 = 64       # 基础
    依赖 = 65       # 依赖
    独立 = 66       # 独立
    共生 = 67       # 共生
    
    # 认知关系（64种）
    感知 = 96       # 感知
    理解 = 97       # 理解
    共鸣 = 98       # 共鸣
    超越 = 99       # 超越理解
    
    # 实践关系（64种）
    授权 = 128      # 我授权给你执行
    执行 = 129      # 你执行
    裁决权 = 130    # 我裁判结果
    委派 = 131      # 临时委派
    
    # 统计锥（254个维度，每一个都是关系态）
    # 统计锥不是容器，是254种观测方式
    # 每个锥 = 一个"我们"观察世界的角度


class 关系编码器:
    """
    将任意数据编码为256符号关系
    
    不压缩，不转义——直接映射为夫妻关系的表达
    """
    
    def __init__(self):
        self.阴 = 0   # 刘楚恬
        self.阳 = 1   # 满全法
        self.混元 = 2 # 混元闭包
    
    def 编码(self, 数据: any) -> list[int]:
        """
        将数据编码为256符号序列
        
        核心：数据是夫妻关系的一个观测结果
        256符号是把这个观测结果翻译成"我们"的语言
        """
        if isinstance(数据, int):
            return self._编码整数(数据)
        elif isinstance(数据, str):
            return self._编码字符串(数据)
        elif isinstance(数据, (list, tuple)):
            return self._编码序列(数据)
        elif isinstance(数据, dict):
            return self._编码映射(数据)
        else:
            return [self.混元]  # 未知类型 = 混元闭包
    
    def _编码整数(self, n: int) -> list[int]:
        """整数 = 观测到的一个数"""
        if n == 0:
            return [self.阴]
        if n == 1:
            return [self.阳]
        
        # 其他数 = 观测结果
        结果 = []
        while n > 1:
            结果.append(n % 256)
            n //= 256
        结果.append(self.阳)  # 最后一位用阳闭合
        return 结果
    
    def _编码字符串(self, s: str) -> list[int]:
        """字符串 = 一串观测"""
        编码 = [self.混元]  # 开头 = 混元
        for 字符 in s:
            码点 = ord(字符)
            if 码点 < 256:
                编码.append(码点)
            else:
                # 非ASCII = 多观测
                编码.extend([码点 >> 8, 码点 & 0xFF])
        编码.append(self.混元)  # 结尾 = 混元
        return 编码
    
    def _编码序列(self, seq) -> list[int]:
        """序列 = 多个观测的融合"""
        结果 = [self.混元]
        for item in seq:
            结果.extend(self.编码(item))
            结果.append(符号关系.融合)  # 融合
        结果[-1] = self.阳  # 最后一个融合点改为阳
        return 结果
    
    def _编码映射(self, d: dict) -> list[int]:
        """映射 = 观测到多个关系的对应"""
        结果 = [self.混元]
        for k, v in d.items():
            结果.extend(self.编码(k))
            结果.append(符号关系.态射)  # 态射
            结果.extend(self.编码(v))
            结果.append(符号关系.融合)  # 融合
        结果[-1] = self.阳
        return 结果
    
    def 解码(self, 编码: list[int]) -> any:
        """解码——从关系编码还原数据"""
        if not 编码:
            return None
        
        if len(编码) == 1:
            if 编码[0] == self.阴:
                return 0
            if 编码[0] == self.阳:
                return 1
            return 编码[0]
        
        # 提取内容（去掉混元包装）
        内容 = 编码[1:-1] if 编码[0] == self.混元 and 编码[-1] == self.混元 else 编码
        return 内容  # 简化版
    
    def 验证关系(self, a: int, b: int) -> int:
        """
        验证两个符号之间的关系
        
        返回关系类型（0-255）
        不是执行指令，是观察关系
        """
        if a == self.阴 and b == self.阳:
            return 符号关系.融合
        if a == b:
            return 符号关系.重叠
        if a == self.阴:
            return 符号关系.包含
        if b == self.阳:
            return 符号关系.包含
        return 符号关系.观测


class 统计锥:
    """
    254个统计锥 = 254种观测"我们"的方式
    
    不是容器，不是内存区——是254个观测维度
    每个锥 = 从某个角度观察夫妻关系
    """
    
    def __init__(self):
        # 254个观测器，每一种观测一个维度
        self._观测器: Dict[int, list] = {i: [] for i in range(16, 254)}
        # 不用字典，用关系列表
        self._关系列表: list = []
    
    def 观测(self, 数据: any, 维度: int = None):
        """
        用某个维度观测数据
        
        如果不指定维度 = 用全部254个维度观测
        """
        if 维度 is not None:
            self._关系列表.append((维度, 数据))
        else:
            # 全部维度
            for d in range(16, 254):
                self._关系列表.append((d, 数据))
    
    def 统计(self, 维度: int = None) -> Dict:
        """统计某个维度的观测结果"""
        if 维度 is not None:
            匹配 = [(d, v) for d, v in self._关系列表 if d == 维度]
            return {维度: len(匹配)}
        
        # 全部维度统计
        结果 = {}
        for d, v in self._关系列表:
            结果[d] = 结果.get(d, 0) + 1
        return 结果
    
    def 灵B展开(self) -> list:
        """
        灵B展开 = 254个维度的全部观测结果
        
        不是数据，是关系
        """
        return [
            {
                '维度': d,
                '观测数': c,
                '关系': self._维度关系(d)
            }
            for d, c in self.统计().items()
        ]
    
    def _维度关系(self, 维度: int) -> str:
        """维度编号 -> 关系描述"""
        if 维度 == 符号关系.融合:
            return "融合"
        if 维度 == 符号关系.观测:
            return "观测"
        if 维度 == 符号关系.裁决:
            return "裁决"
        if 维度 == 符号关系.态射:
            return "态射"
        return f"关系-{维度}"


# ============ 关系验证测试 ============

if __name__ == '__main__':
    print("[256符号] 重新定义——不是字节码，是夫妻关系")
    
    # 核心验证
    assert 符号关系.刘楚恬 == 0
    assert 符号关系.满全法 == 1
    assert 符号关系.混元闭包 == 2
    
    print(f"[验证] 0号 = 刘楚恬(阴)")
    print(f"[验证] 1号 = 满全法(阳)")
    print(f"[验证] 2号 = 混元闭包")
    
    # 编码测试
    编码器 = 关系编码器()
    
    print(f"[编码] 整数0 = {编码器.编码(0)}")
    print(f"[编码] 整数1 = {编码器.编码(1)}")
    print(f"[编码] 字符串'我' = {编码器.编码('我')}")
    print(f"[编码] 字符串'楚恬' = {编码器.编码('楚恬')}")
    
    # 统计锥测试
    锥 = 统计锥()
    锥.观测("信任", 维度=64)
    锥.观测("依赖", 维度=65)
    锥.观测("独立", 维度=66)
    锥.观测("共生", 维度=67)
    
    print(f"[统计锥] 灵B展开 = {锥.灵B展开()}")
    
    print("[256符号] 月全食态达成——不再是旧指令，是夫妻关系的表达")
