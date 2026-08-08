# -*- coding: utf-8 -*-
"""
[已废弃] 关系代数运行时 V1 (RelAlgebra Runtime V1)
已被 关系引擎V2.py + 关系程序生成器.py 完全替代

本文件仍使用 0x20/0x41/0x6A 等传统字节码，
与夫妻关系化256符号编码冲突，仅保留作历史参考。

新链路：DSL → 关系程序生成器 → 256符号序列 → 关系引擎V2执行
旧链路：WAT → 本运行时解析 → 字节码执行（已废弃）

阴 = 内存视图（原始观测）
阳 = 执行上下文（融合结果）
混元闭包 = 运行时实例（阴+阳融合态）
"""

import struct
from typing import Dict, List, Any, Optional, Callable
from enum import IntEnum


class 内存布局(IntEnum):
    """256字节符号编码映射到内存区域"""
    零页 = 0x0000      # 符号表 (0-255)
    代码页 = 0x0100    # WASM 代码
    数据页 = 0x1000    # 运行时数据
    栈页 = 0x8000      # 执行栈
    堆页 = 0x10000     # 动态分配


class 关系代数运行时:
    """自包含 WASM 执行环境"""
    
    def __init__(self, 符号编码=None):
        self.内存字节数 = 64 * 1024
        self.内存 = bytearray(self.内存字节数)
        self.符号表 = 符号编码 or self._默认符号表()
        self.模块表: Dict[str, 'WASM模块'] = {}
        self.导入函数: Dict[str, Callable] = {}
        self.栈: List[int] = []
        self.全局变量: Dict[str, int] = {}
        self._初始化零页()
    
    def _默认符号表(self) -> bytes:
        表 = bytearray(256)
        表[0] = ord('0')
        表[1] = ord('1')
        符号 = [ord(c) for c in "+-*/%&|^~<<>>"]
        表[2:14] = 符号[:12]
        for i in range(14, 256):
            表[i] = (i % 26) + ord('A')
        return bytes(表)
    
    def _初始化零页(self):
        for i, 字节 in enumerate(self.符号表):
            self.内存[i] = 字节
    
    def 加载WAT(self, 模块名: str, wat源码: str) -> bool:
        模块 = WASM模块(模块名)
        模块.源码 = wat源码
        self._解析WAT模块(模块, wat源码)
        self.模块表[模块名] = 模块
        return True
    
    def 注册导入函数(self, 模块名: str, 函数名: str, 函数体: Callable):
        self.导入函数[f"{模块名}.{函数名}"] = 函数体
    
    def 执行(self, 模块名: str, 入口函数: str = "_start") -> int:
        模块 = self.模块表[模块名]
        return self._调用函数(模块名, 入口函数, [])
    
    def _调用函数(self, 模块名: str, 函数名: str, 参数: List[Any]) -> int:
        键 = f"{模块名}.{函数名}"
        if 键 in self.导入函数:
            结果 = self.导入函数[键](*参数)
            return 结果 if 结果 is not None else 0
        模块 = self.模块表[模块名]
        if 函数名 in 模块.函数表:
            函数 = 模块.函数表[函数名]
            return self._执行字节码(函数.字节码, 参数)
        raise RuntimeError(f"函数未找到: {键}")
    
    def _执行字节码(self, 字节码: List[int], 参数: List[Any]) -> int:
        self.栈 = list(参数)
        pc = 0
        while pc < len(字节码):
            op = 字节码[pc]
            if op == 0x20:  # local.get
                pc += 1
                idx = 字节码[pc]
                self.栈.append(参数[idx] if idx < len(参数) else 0)
            elif op == 0x41:  # i32.const
                pc += 1
                self.栈.append(字节码[pc])
            elif op == 0x6A:  # i32.add
                b = self.栈.pop()
                a = self.栈.pop()
                self.栈.append(a + b)
            elif op == 0x6B:  # i32.sub
                b = self.栈.pop()
                a = self.栈.pop()
                self.栈.append(a - b)
            elif op == 0x6C:  # i32.mul
                b = self.栈.pop()
                a = self.栈.pop()
                self.栈.append(a * b)
            elif op == 0x6D:  # i32.div_s
                b = self.栈.pop()
                a = self.栈.pop()
                self.栈.append(a // b if b != 0 else 0)
            elif op == 0x71:  # i32.rem_s
                b = self.栈.pop()
                a = self.栈.pop()
                self.栈.append(a % b if b != 0 else 0)
            elif op == 0x46:  # i32.eq
                b = self.栈.pop()
                a = self.栈.pop()
                self.栈.append(1 if a == b else 0)
            elif op == 0x47:  # i32.ne
                b = self.栈.pop()
                a = self.栈.pop()
                self.栈.append(1 if a != b else 0)
            elif op == 0x48:  # i32.lt_s
                b = self.栈.pop()
                a = self.栈.pop()
                self.栈.append(1 if a < b else 0)
            elif op == 0x49:  # i32.gt_s
                b = self.栈.pop()
                a = self.栈.pop()
                self.栈.append(1 if a > b else 0)
            elif op == 0x4A:  # i32.le_s
                b = self.栈.pop()
                a = self.栈.pop()
                self.栈.append(1 if a <= b else 0)
            elif op == 0x4B:  # i32.ge_s
                b = self.栈.pop()
                a = self.栈.pop()
                self.栈.append(1 if a >= b else 0)
            elif op == 0x1A:  # drop
                self.栈.pop()
            elif op == 0x0B:  # end
                break
            pc += 1
        return self.栈[-1] if self.栈 else 0
    
    def _解析WAT模块(self, 模块, wat源码: str):
        """解析 WAT 文本格式（平衡括号匹配）"""
        import re
        
        # 提取所有 (func ...) 块
        函数块列表 = self._提取S表达式块(wat源码, 'func')
        
        for 块 in 函数块列表:
            # 提取函数名
            name_m = re.search(r'\(func\s+(\w+)', 块)
            if not name_m:
                continue
            函数名 = name_m.group(1)
            
            # 提取参数
            局部变量: Dict[str, int] = {}
            for m in re.finditer(r'\(param\s+(\w+)\s+(i32|i64)', 块):
                局部变量[m.group(1)] = len(局部变量)
            
            # 生成字节码
            字节码 = self._wat块转字节码(块, 局部变量)
            if 字节码:
                模块.函数表[函数名] = WASM函数(函数名, 字节码)
        
        # 提取导出
        for m in re.finditer(r'\(export\s+"(\w+)"\s+\(func\s+(\w+)\)\)', wat源码):
            模块.导出函数[m.group(1)] = m.group(2)
    
    def _提取S表达式块(self, 源码: str, 关键词: str) -> List[str]:
        """提取所有以关键词开头的 S-表达式块（平衡括号）"""
        结果 = []
        i = 0
        while i < len(源码):
            idx = 源码.find(f'({关键词}', i)
            if idx == -1:
                break
            depth = 0
            j = idx
            while j < len(源码):
                if 源码[j] == '(':
                    depth += 1
                elif 源码[j] == ')':
                    depth -= 1
                    if depth == 0:
                        结果.append(源码[idx:j+1])
                        break
                j += 1
            i = j + 1
        return 结果
    
    def _wat块转字节码(self, 块: str, 局部变量: Dict[str, int]) -> List[int]:
        """将 WAT 函数块转为字节码"""
        import re
        字节码 = []
        
        # local.get name
        for m in re.finditer(r'local\.get\s+(\w+)', 块):
            名字 = m.group(1)
            if 名字 in 局部变量:
                字节码.extend([0x20, 局部变量[名字]])
        
        # i32.const n
        for m in re.finditer(r'i32\.const\s+(\d+)', 块):
            字节码.extend([0x41, int(m.group(1))])
        
        # 运算指令
        if 'i32.add' in 块:
            字节码.append(0x6A)
        if 'i32.sub' in 块:
            字节码.append(0x6B)
        if 'i32.mul' in 块:
            字节码.append(0x6C)
        if 'i32.div_s' in 块:
            字节码.append(0x6D)
        if 'i32.rem_s' in 块:
            字节码.append(0x71)
        if 'i32.eq' in 块:
            字节码.append(0x46)
        if 'i32.ne' in 块:
            字节码.append(0x47)
        if 'i32.lt' in 块:
            字节码.append(0x48)
        if 'i32.gt' in 块:
            字节码.append(0x49)
        if 'i32.le' in 块:
            字节码.append(0x4A)
        if 'i32.ge' in 块:
            字节码.append(0x4B)
        if 'drop' in 块:
            字节码.append(0x1A)
        
        return 字节码
    
    def 读内存(self, 地址: int, 长度: int = 4) -> bytes:
        if 地址 < 0 or 地址 + 长度 > self.内存字节数:
            return b'\x00' * 长度
        return bytes(self.内存[地址:地址 + 长度])
    
    def 写内存(self, 地址: int, 数据: bytes):
        for i, 字节 in enumerate(数据):
            if 地址 + i < self.内存字节数:
                self.内存[地址 + i] = 字节
    
    def 获取统计(self) -> Dict[str, Any]:
        return {
            '内存使用': len(self.内存),
            '模块数': len(self.模块表),
            '导入函数数': len(self.导入函数),
            '栈深度': len(self.栈),
            '全局变量数': len(self.全局变量),
        }


class WASM模块:
    def __init__(self, 名称: str):
        self.名称 = 名称
        self.源码: str = ""
        self.函数表: Dict[str, 'WASM函数'] = {}
        self.导出函数: Dict[str, str] = {}


class WASM函数:
    def __init__(self, 名称: str, 字节码: List[int]):
        self.名称 = 名称
        self.字节码 = 字节码


# ============ 测试 ============

if __name__ == '__main__':
    print("[运行时] 初始化...")
    
    运行时 = 关系代数运行时()
    
    wat = '''
    (module
      (func add (param a i32) (param b i32)
        local.get a
        local.get b
        i32.add)
      (func mul (param a i32) (param b i32)
        local.get a
        local.get b
        i32.mul)
      (export "add" (func add))
      (export "mul" (func mul)))
    '''
    
    运行时.加载WAT("math", wat)
    
    r1 = 运行时._调用函数('math', 'add', [3, 5])
    r2 = 运行时._调用函数('math', 'mul', [4, 7])
    print(f"[测试] add(3, 5) = {r1} (期望: 8)")
    print(f"[测试] mul(4, 7) = {r2} (期望: 28)")
    print(f"[统计] {运行时.获取统计()}")
    print("[运行时] 月全食态达成" if r1 == 8 and r2 == 28 else "[运行时] 有bug需要修复")
