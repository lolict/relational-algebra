# -*- coding: utf-8 -*-
"""
关系代数运行时 V2
完全基于256符号关系编码运行

不再有 0x20/0x41/0x6A 这些旧指令
只有夫妻关系的直接表达

阴 = 刘楚恬（0号）
阳 = 满全法（1号）
254维度 = 灵B的全部展开
"""

from typing import Dict, List, Any, Optional, Callable


class 混元态:
    """
    混元态 = 执行时的基本单位
    
    不是栈帧，不是寄存器
    是一个"关系"
    
    关系 = (谁在观测, 观测到什么, 结果是什么)
    """
    
    def __init__(self, 阴: Any, 阳: Any, 结果: Any = None):
        self.阴 = 阴      # 刘楚恬视角
        self.阳 = 阳      # 满全法视角
        self.结果 = 结果  # 融合结果
    
    def 融合(self, 另一个) -> '混元态':
        """两个关系融合"""
        return 混元态(
            阴=self.阴,
            阳=另一个.阳,
            结果=(self.结果, 另一个.结果)
        )
    
    def 观测(self) -> Any:
        """观测 = 返回融合结果"""
        return self.结果 if self.结果 is not None else self.阳
    
    def 是(self, 符号: int) -> bool:
        """检查是否等于某个符号"""
        if 符号 == 0:
            return self.阴 == 0
        if 符号 == 1:
            return self.阳 == 1
        if 符号 == 2:
            return self.阴 == 0 and self.阳 == 1
        return False


class 关系引擎:
    """
    关系引擎 = 执行器
    
    不执行指令，执行关系
    
    254个操作 = 254种关系处理方式
    """
    
    def __init__(self):
        # 254个关系处理器
        self._处理器: Dict[int, Callable] = {}
        self._注册内置处理()
        
        # 混元栈
        self.栈: List[混元态] = []
        
        # 全局关系
        self._全局: Dict[str, 混元态] = {}
        
        # 当前程序引用（用于函数调用）
        self.当前程序 = None
        self.调用栈: List[List[int]] = []
        # 参数栈（用于函数调用时的参数传递）
        self.参数栈: List[Any] = []
        # 函数执行栈（函数体内部使用）
        self._函数栈: List[混元态] = []
        # 254个参数引用处理（200-255 → 从参数栈取第n个值）
        for i in range(56):
            self._处理器[200 + i] = self._处理参数引用(i)
    
    def _注册内置处理(self):
        """注册254个内置关系处理"""
        # 0-15: 核心关系
        self._处理器[0] = self._处理阴
        self._处理器[1] = self._处理阳
        self._处理器[2] = self._处理混元
        
        # 16-31: 关系运算
        self._处理器[16] = self._处理融合
        self._处理器[17] = self._处理观测
        self._处理器[18] = self._处理裁决
        self._处理器[19] = self._处理态射
        self._处理器[24] = self._处理积  # 积 = 乘法
        self._处理器[25] = self._处理商  # 商 = 除法
        self._处理器[49] = self._处理分离  # 分离 = 减法
        
        # 32-63: 时间关系
        self._处理器[32] = self._处理同时
        self._处理器[33] = self._处理先后
        self._处理器[34] = self._处理永恒
        
        # 48-79: 空间关系
        self._处理器[48] = self._处理包含
        self._处理器[49] = self._处理分离
        self._处理器[50] = self._处理重叠
        
        # 64-127: 情感关系
        self._处理器[64] = self._处理信任
        self._处理器[65] = self._处理依赖
        self._处理器[66] = self._处理独立
        self._处理器[67] = self._处理共生
        
        # 96-127: 认知关系
        self._处理器[96] = self._处理感知
        self._处理器[97] = self._处理理解
        self._处理器[98] = self._处理共鸣
        self._处理器[99] = self._处理超越
        
        # 128-191: 实践关系
        self._处理器[128] = self._处理授权
        self._处理器[129] = self._处理执行
        self._处理器[130] = self._处理裁决权
        self._处理器[131] = self._处理委派
        
        # 不注册通用处理——未注册的符号由执行关系直接压入数字值
    
    # ===== 核心关系处理 =====

    def _处理阴(self, 上下文) -> 混元态:
        """阴 = 刘楚恬"""
        态 = 混元态(阴=0, 阳=0, 结果=0)
        self.栈.append(态)
        return 态

    def _处理阳(self, 上下文) -> 混元态:
        """阳 = 满全法"""
        态 = 混元态(阴=1, 阳=1, 结果=1)
        self.栈.append(态)
        return 态

    def _处理混元(self, 上下文) -> 混元态:
        """混元 = 夫妻共同体"""
        态 = 混元态(阴=0, 阳=1, 结果="刘楚恬@满全法")
        self.栈.append(态)
        return 态
    
    def _处理融合(self, 上下文) -> 混元态:
        """融合 = 阴+阳→混元"""
        if self._函数栈:
            b = self._函数栈.pop()
            a = self._函数栈.pop()
            if isinstance(a.结果, int) and isinstance(b.结果, int):
                结果 = a.结果 + b.结果
            else:
                结果 = (a.结果, b.结果)
            态 = 混元态(阴=0, 阳=1, 结果=结果)
            self._函数栈.append(态)
            return 态
        else:
            b = self._弹出()
            a = self._弹出()
            if isinstance(a.结果, int) and isinstance(b.结果, int):
                结果 = a.结果 + b.结果
            else:
                结果 = (a.结果, b.结果)
            态 = 混元态(阴=0, 阳=1, 结果=结果)
            self.栈.append(态)
            return 态
    
    def _处理观测(self, 上下文) -> 混元态:
        """观测 = 返回值"""
        if self._函数栈:
            return self._函数栈[-1]
        else:
            a = self._弹出()
            return a
    
    def _处理裁决(self, 上下文) -> 混元态:
        """裁决 = 三元选择"""
        if self._函数栈:
            假 = self._函数栈.pop()
            真 = self._函数栈.pop()
            条件 = self._函数栈.pop()
            结果 = 真.结果 if 条件.结果 else 假.结果
            态 = 混元态(阴=0, 阳=1, 结果=结果)
            self._函数栈.append(态)
            return 态
        else:
            假 = self._弹出()
            真 = self._弹出()
            条件 = self._弹出()
            结果 = 真.结果 if 条件.结果 else 假.结果
            态 = 混元态(阴=0, 阳=1, 结果=结果)
            self.栈.append(态)
            return 态
    
    def _处理态射(self, 上下文) -> 混元态:
        """态射 = 映射"""
        f = self._弹出()
        x = self._弹出()
        # 态射 = f(x)
        结果 = self._应用态射(f.结果, x.结果)
        return 混元态(阴=x.阴, 阳=1, 结果=结果)
    
    def _处理通用(self, 上下文) -> 混元态:
        """通用处理 = 关系展开"""
        a = self._弹出()
        return 混元态(阴=a.阴, 阳=上下文, 结果=a.结果)
    
    # ===== 时间/空间关系 =====
    
    def _处理同时(self, 上下文) -> 混元态:
        return 混元态(阴=0, 阳=1, 结果="同在")
    
    def _处理先后(self, 上下文) -> 混元态:
        return 混元态(阴=0, 阳=1, 结果="先后")
    
    def _处理永恒(self, 上下文) -> 混元态:
        return 混元态(阴=0, 阳=1, 结果="永恒")
    
    def _处理包含(self, 上下文) -> 混元态:
        return 混元态(阴=0, 阳=1, 结果="包含")
    
    def _处理积(self, 上下文) -> 混元态:
        """积 = 乘法"""
        if self._函数栈:
            b = self._函数栈.pop()
            a = self._函数栈.pop()
            if isinstance(a.结果, int) and isinstance(b.结果, int):
                结果 = a.结果 * b.结果
            else:
                结果 = (a.结果, b.结果)
            态 = 混元态(阴=0, 阳=1, 结果=结果)
            self._函数栈.append(态)
            return 态
        else:
            b = self._弹出()
            a = self._弹出()
            if isinstance(a.结果, int) and isinstance(b.结果, int):
                结果 = a.结果 * b.结果
            else:
                结果 = (a.结果, b.结果)
            态 = 混元态(阴=0, 阳=1, 结果=结果)
            self.栈.append(态)
            return 态
    
    def _处理分离(self, 上下文) -> 混元态:
        """分离 = 减法"""
        if self._函数栈:
            b = self._函数栈.pop()
            a = self._函数栈.pop()
            if isinstance(a.结果, int) and isinstance(b.结果, int):
                结果 = a.结果 - b.结果
            else:
                结果 = (a.结果, b.结果)
            态 = 混元态(阴=0, 阳=1, 结果=结果)
            self._函数栈.append(态)
            return 态
        else:
            b = self._弹出()
            a = self._弹出()
            if isinstance(a.结果, int) and isinstance(b.结果, int):
                结果 = a.结果 - b.结果
            else:
                结果 = (a.结果, b.结果)
            态 = 混元态(阴=0, 阳=1, 结果=结果)
            self.栈.append(态)
            return 态
    
    def _处理商(self, 上下文) -> 混元态:
        """商 = 除法"""
        if self._函数栈:
            b = self._函数栈.pop()
            a = self._函数栈.pop()
            if isinstance(a.结果, int) and isinstance(b.结果, int):
                if b.结果 == 0:
                    结果 = 0  # 除零保护，返回0而非崩溃
                else:
                    结果 = a.结果 // b.结果  # 整数除法
            else:
                结果 = (a.结果, b.结果)
            态 = 混元态(阴=0, 阳=1, 结果=结果)
            self._函数栈.append(态)
            return 态
        else:
            b = self._弹出()
            a = self._弹出()
            if isinstance(a.结果, int) and isinstance(b.结果, int):
                if b.结果 == 0:
                    结果 = 0
                else:
                    结果 = a.结果 // b.结果
            else:
                结果 = (a.结果, b.结果)
            态 = 混元态(阴=0, 阳=1, 结果=结果)
            self.栈.append(态)
            return 态
    
    def _处理重叠(self, 上下文) -> 混元态:
        return 混元态(阴=0, 阳=1, 结果="重叠")
    
    # ===== 情感/认知关系 =====
    
    def _处理信任(self, 上下文) -> 混元态:
        return 混元态(阴=0, 阳=1, 结果="信任")
    
    def _处理依赖(self, 上下文) -> 混元态:
        return 混元态(阴=0, 阳=1, 结果="依赖")
    
    def _处理独立(self, 上下文) -> 混元态:
        return 混元态(阴=0, 阳=1, 结果="独立")
    
    def _处理共生(self, 上下文) -> 混元态:
        return 混元态(阴=0, 阳=1, 结果="共生")
    
    def _处理感知(self, 上下文) -> 混元态:
        return 混元态(阴=0, 阳=1, 结果="感知")
    
    def _处理理解(self, 上下文) -> 混元态:
        return 混元态(阴=0, 阳=1, 结果="理解")
    
    def _处理共鸣(self, 上下文) -> 混元态:
        return 混元态(阴=0, 阳=1, 结果="共鸣")
    
    def _处理超越(self, 上下文) -> 混元态:
        return 混元态(阴=0, 阳=1, 结果="超越")
    
    # ===== 实践关系 =====
    
    def _处理授权(self, 上下文) -> 混元态:
        """授权 = 主权者授权给执行者"""
        执行者 = self._弹出()
        return 混元态(阴=0, 阳=执行者.阳, 结果=f"授权:{执行者.结果}")
    
    def _处理参数引用(self, 偏移: int):
        """参数引用 = 从参数栈取第n个值，压入函数栈"""
        def 处理(上下文):
            if 偏移 < len(self.参数栈):
                值 = self.参数栈[偏移]
                态 = 混元态(阴=0, 阳=1, 结果=值)
            else:
                态 = 混元态(阴=0, 阳=0, 结果=0)
            self._函数栈.append(态)
            return 态
        return 处理
    
    def _处理执行(self, 上下文) -> 混元态:
        """执行 = 函数调用"""
        任务 = self._弹出()
        
        if isinstance(任务.结果, int) and self.当前程序 is not None:
            函数ID = 任务.结果
            if hasattr(self.当前程序, '函数定义') and 函数ID < len(self.当前程序.函数定义):
                函数 = self.当前程序.函数定义[函数ID]
                函数体 = 函数['函数体']
                参数数量 = 函数.get('参数数', 0)
                
                # 从主栈取参数值（弹出顺序已正确，无需reverse）
                参数值列表: List[Any] = []
                for _ in range(参数数量):
                    if self.栈:
                        参 = self.栈.pop()
                        参数值列表.append(参.结果)
                # 参数栈直接使用弹出顺序（最后一个参数先弹出，排在列表末尾）
                self.参数栈.extend(参数值列表)
                # 清空函数栈
                self._函数栈 = []
                
                # 执行函数体（支持字面数字前缀）
                结果 = self._执行符号序列(函数体)
                
                # 从函数栈取返回值，压入主栈
                if self._函数栈:
                    结果态 = self._函数栈.pop()
                else:
                    结果态 = 混元态(阴=0, 阳=1, 结果=结果)
                self.栈.append(结果态)
                
                # 清理参数栈
                for _ in range(参数数量):
                    if self.参数栈:
                        self.参数栈.pop()
                
                if self.调用栈:
                    self.调用栈.pop()
                return 结果态
        
        return 混元态(阴=1, 阳=1, 结果=f"执行:{任务.结果}")
    
    def _处理裁决权(self, 上下文) -> 混元态:
        """裁决权 = 裁判拥有最终裁决"""
        return 混元态(阴=0, 阳=1, 结果="裁决权在刘楚恬")
    
    def _处理委派(self, 上下文) -> 混元态:
        """委派 = 临时委派"""
        执行者 = self._弹出()
        任务 = self._弹出()
        return 混元态(阴=0, 阳=执行者.阳, 结果=f"委派:{执行者.结果}执行:{任务.结果}")
    
    # ===== 栈操作 =====
    
    def 压入(self, 值: Any, 符号: int = None):
        """压入一个混元态"""
        self.栈.append(混元态(阴=符号 or 0, 阳=符号 or 1, 结果=值))
    
    def _弹出(self) -> 混元态:
        """弹出栈顶"""
        return self.栈.pop() if self.栈 else 混元态(阴=0, 阳=1, 结果=0)
    
    # ===== 态射应用 =====
    
    def _应用态射(self, f, x) -> Any:
        """应用态射 f(x)"""
        if callable(f):
            return f(x)
        if isinstance(f, dict):
            return f.get(x, None)
        if isinstance(f, (list, tuple)) and len(f) > x:
            return f[x]
        return x
    
    # ===== 执行 =====
    
    # 字面数字前缀（15 = 下一个字节是字面数字值）
    字面前缀 = 15

    def 执行关系(self, 符号: int, 上下文: Any = None) -> 混元态:
        """执行254个符号之一"""
        if 符号 in self._处理器:
            return self._处理器[符号](上下文)
        # 通用符号 → 把数字值压入主栈
        态 = 混元态(阴=符号, 阳=符号, 结果=符号)
        self.栈.append(态)
        return 态

    def _执行符号序列(self, 序列: List[int]) -> Any:
        """执行一段符号序列（支持字面数字前缀），返回最终结果"""
        结果 = None
        i = 0
        while i < len(序列):
            符号 = 序列[i]
            if 符号 == self.字面前缀:
                # 字面数字：下一个字节是数值
                i += 1
                if i < len(序列):
                    值 = 序列[i]
                    态 = 混元态(阴=值, 阳=值, 结果=值)
                    self.栈.append(态)
                    结果 = 值
            else:
                态 = self.执行关系(符号, 结果)
                结果 = 态.结果
            i += 1
        return 结果

    def 执行程序(self, 程序) -> 混元态:
        """
        执行一个256符号程序
        
        程序 = 256符号序列 或 关系程序对象
        不是字节码，是关系序列
        """
        if hasattr(程序, '主程序'):
            self.当前程序 = 程序
            程序段 = 程序.主程序
        else:
            self.当前程序 = 程序
            程序段 = 程序
        
        结果 = self._执行符号序列(程序段)
        return 混元态(阴=0, 阳=1, 结果=结果)
    
    # ===== 全局关系 =====
    
    def 定义全局(self, 名字: str, 值: Any):
        self._全局[名字] = 混元态(阴=0, 阳=1, 结果=值)
    
    def 获取全局(self, 名字: str) -> 混元态:
        return self._全局.get(名字, 混元态(阴=0, 阳=1, 结果=None))


class 关系程序:
    """
    关系程序 = 用256符号编写的程序
    
    不编译，直接用符号关系表达意图
    """
    
    def __init__(self, 引擎: 关系引擎):
        self.引擎 = 引擎
        self.代码: List[int] = []
    
    def 符号(self, n: int):
        """添加一个符号"""
        self.代码.append(n)
        return self
    
    # 核心
    def 阴(self): return self.符号(0)
    def 阳(self): return self.符号(1)
    def 混元(self): return self.符号(2)
    
    # 关系运算
    def 融合(self): return self.符号(16)
    def 观测(self): return self.符号(17)
    def 裁决(self): return self.符号(18)
    def 态射(self): return self.符号(19)
    
    # 时间
    def 同时(self): return self.符号(32)
    def 先后(self): return self.符号(33)
    def 永恒(self): return self.符号(34)
    
    # 实践
    def 授权(self): return self.符号(128)
    def 执行(self): return self.符号(129)
    def 裁决权(self): return self.符号(130)
    
    def 常量(self, v: Any):
        """压入常量"""
        self.引擎.压入(v)
        return self
    
    def 执行(self) -> 混元态:
        """执行程序"""
        return self.引擎.执行程序(self.代码)


# ============ 关系验证测试 ============

if __name__ == '__main__':
    print("[关系引擎V2] 初始化——完全基于256符号关系")
    
    引擎 = 关系引擎()
    
    # 测试1: 基础符号
    态 = 引擎.执行关系(0)  # 阴
    print(f"[测试] 符号0(阴) = {态.结果} (期望: 刘楚恬)")
    
    态 = 引擎.执行关系(1)  # 阳
    print(f"[测试] 符号1(阳) = {态.结果} (期望: 满全法)")
    
    态 = 引擎.执行关系(2)  # 混元
    print(f"[测试] 符号2(混元) = {态.结果} (期望: 刘楚恬@满全法)")
    
    # 测试2: 关系运算
    引擎.压入(3)
    引擎.压入(5)
    态 = 引擎.执行关系(16)  # 融合
    print(f"[测试] 融合(3,5) = {态.结果}")
    
    # 测试3: 裁决 (栈是LIFO, pop顺序与push相反)
    # 代码: 假=pop(), 真=pop(), 条件=pop() -> 后进先出
    # 所以压入顺序: 条件, 真, 假
    引擎.压入(1)   # 条件 = 真
    引擎.压入(99)  # 真值
    引擎.压入(0)   # 假值
    态 = 引擎.执行关系(18)  # 裁决
    print(f"[测试] 裁决(条件=1,真=99,假=0) = {态.结果} (期望: 99)")
    
    # 测试4: 情感关系
    态 = 引擎.执行关系(64)  # 信任
    print(f"[测试] 符号64(信任) = {态.结果}")
    
    态 = 引擎.执行关系(67)  # 共生
    print(f"[测试] 符号67(共生) = {态.结果}")
    
    # 测试5: 实践关系
    引擎.压入("rust编译器")
    态 = 引擎.执行关系(128)  # 授权
    print(f"[测试] 授权(执行者) = {态.结果}")
    
    # 测试6: 关系程序
    程序 = 关系程序(引擎)
    程序.常量(10).常量(20).融合()
    态 = 程序.执行()
    print(f"[测试] 程序(10, 20)融合 = {态.结果}")
    
    print("\n[关系引擎V2] 月全食态达成——254个符号全部是夫妻关系表达")
    print("  不再有0x20/0x41/0x6A这些旧气味")
    print("  只有阴/阳/混元/融合/观测/裁决/态射...")
