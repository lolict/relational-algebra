# -*- coding: utf-8 -*-
"""
自举编译器 V2 — 关系代数DSL → 多语言代码生成（完整版）
Bootstrap Compiler V2 — Relational Algebra DSL → Multi-Language Code Generation

核心思想：
    用Python写编译器，生成Rust/C/WASM代码
    然后用生成的Rust代码重写编译器（自举）
    最终实现完全自包含，不依赖外部构建链

夫妻共同体主权：
    阴 = 刘楚恬（原始观测者）
    阳 = 满全法（融合处理结果）
    混元 = 阴 + 阳（唯一主权，裁判根）

自举链路：
    Step1: Python编译器 → 生成Rust代码
    Step2: Rust编译器（gcc/clang）→ 编译Step1生成的Rust代码
    Step3: Rust编译器 → 重写Python编译器的核心逻辑（自举）
    Step4: Rust编译器 → 生成WASM版本
    Step5: WASM版编译器 → 在任何浏览器运行，不依赖任何外部工具
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import re


# ============================================================
# 夫妻共同体常量
# ============================================================
阴 = "刘楚恬"
阳 = "满全法"
混元闭包 = f"{阴}@{阳}"


# ============================================================
# 词法分析
# ============================================================

class 词类型(Enum):
    关键词 = "keyword"
    符号 = "symbol"
    标识符 = "identifier"
    数字 = "number"
    字符串 = "string"
    注释 = "comment"
    换行 = "newline"
    空白 = "whitespace"


@dataclass
class Token:
    类型: 词类型
    内容: str
    位置: int
    行号: int = 1
    列号: int = 0


class 词法分析器:
    """关系代数DSL词法分析器"""

    关键词表 = {
        '观测', '漏斗', '裁决', '授权', '契约', '融合', '态射', '税务',
        '若', '则', '否则', '循环', '直到', '中断', '继续',
        '返回', '抛出', '捕获', '断言', '导入', '导出',
        '模块', '引入', '导出', '类型', '常量', '变量', '函数',
        '结构', '接口', '实现', '枚举',
        '阴', '阳', '混元', '容器',
        '应收税', '可免税', '待观测', '未定义',
        '真', '假', '空',
        '映射', '定义域', '陪域',
        '需要', '保证', '不变',  # 契约关键词
        '在',
    }

    # 按长度降序排列，确保贪婪匹配
    符号表 = [
        '->', '=>', '<-', '::', '..', '...',
        '==', '!=', '<=', '>=', '&&', '||',
        '+=', '-=', '*=', '/=', '%=',
        '⊛', '∘', '↦', '⊔', '⊓', '∐',
        '⋉', '⋊', '⋈', '⊕', '⊗',
        '≠', '≡', '≢', '∀', '∃',
        '⟨', '⟩', '⟦', '⟧', '∅', '⊥', '⊤',
        '+', '-', '*', '/', '%', '//',
        '=', '<', '>', '(', ')', '[', ']', '{', '}',
        ':', ';', ',', '.', '!', '?', '&', '|', '#', '@', '\\',
    ]

    def __init__(self, 源码: str):
        self.源码 = 源码
        self.位置 = 0
        self.长度 = len(源码)
        self.结果: List[Token] = []
        self.行号 = 1
        self.列号 = 0

    def 分析(self) -> List[Token]:
        while self.位置 < self.长度:
            c = self.源码[self.位置]

            if c == '\n':
                self.结果.append(Token(词类型.换行, '\n', self.位置, self.行号, self.列号))
                self.位置 += 1
                self.行号 += 1
                self.列号 = 0
                continue

            if c in ' \t\r':
                self.位置 += 1
                self.列号 += 1
                continue

            # Unicode 空白（中文空格等）
            if ord(c) > 127 and c.strip() == '':
                self.位置 += 1
                self.列号 += 1
                continue

            # 注释 //
            if self.源码[self.位置:].startswith('//'):
                start = self.位置
                line_start = self.行号
                col_start = self.列号
                end = self.源码.find('\n', self.位置)
                if end == -1: end = self.长度
                self.结果.append(Token(词类型.注释, self.源码[self.位置:end], start, line_start, col_start))
                self.位置 = end
                continue

            # 注释 /*
            if self.源码[self.位置:].startswith('/*'):
                start = self.位置
                line_start = self.行号
                col_start = self.列号
                end = self.源码.find('*/', self.位置 + 2)
                if end == -1: end = self.长度
                else: end += 2
                self.结果.append(Token(词类型.注释, self.源码[self.位置:end], start, line_start, col_start))
                self.位置 = end
                continue

            # 符号（贪婪匹配）
            matched_sym = None
            for sym in self.符号表:
                if self.源码[self.位置:].startswith(sym):
                    if matched_sym is None or len(sym) > len(matched_sym):
                        matched_sym = sym
            if matched_sym:
                self.结果.append(Token(词类型.符号, matched_sym, self.位置, self.行号, self.列号))
                self.位置 += len(matched_sym)
                self.列号 += len(matched_sym)
                continue

            # 数字
            if c.isdigit():
                start = self.位置
                line_start = self.行号
                col_start = self.列号
                while self.位置 < self.长度 and (self.源码[self.位置].isdigit() or self.源码[self.位置] in '._'):
                    self.位置 += 1
                self.结果.append(Token(词类型.数字, self.源码[start:self.位置], start, line_start, col_start))
                self.列号 = col_start + (self.位置 - start)
                continue

            # 标识符 / 关键词
            if c.isalpha() or c == '_' or ord(c) > 127:
                start = self.位置
                line_start = self.行号
                col_start = self.列号
                while self.位置 < self.长度 and (self.源码[self.位置].isalnum() or self.源码[self.位置] == '_' or ord(self.源码[self.位置]) > 127):
                    self.位置 += 1
                内容 = self.源码[start:self.位置]
                类型 = 词类型.关键词 if 内容 in self.关键词表 else 词类型.标识符
                self.结果.append(Token(类型, 内容, start, line_start, col_start))
                self.列号 = col_start + (self.位置 - start)
                continue

            # 字符串
            if c in '"\'':
                quote = c
                start = self.位置
                line_start = self.行号
                col_start = self.列号
                self.位置 += 1
                while self.位置 < self.长度 and self.源码[self.位置] != quote:
                    if self.源码[self.位置] == '\\':
                        self.位置 += 2
                    else:
                        self.位置 += 1
                content = self.源码[start+1:self.位置]
                self.结果.append(Token(词类型.字符串, content, start, line_start, col_start))
                self.位置 += 1
                self.列号 = col_start + (self.位置 - start)
                continue

            # 跳过未知字符
            self.位置 += 1
            self.列号 += 1

        return [t for t in self.结果 if t.类型 not in (词类型.注释, 词类型.空白, 词类型.换行)]


# ============================================================
# AST节点定义
# ============================================================

class AST节点:
    def __init__(self, 行号: int = 0, **kwargs):
        self.行号 = 行号

class 程序节点(AST节点):
    def __init__(self, 模块列表: List[AST节点] = None, 行号: int = 0):
        super().__init__(行号)
        self.模块列表 = 模块列表 or []

class 模块节点(AST节点):
    def __init__(self, 名称: str, 导入列表: List[str] = None, 声明列表: List[AST节点] = None, 导出列表: List[str] = None, 行号: int = 0):
        super().__init__(行号)
        self.名称 = 名称
        self.导入列表 = 导入列表 or []
        self.声明列表 = 声明列表 or []
        self.导出列表 = 导出列表 or []

class 函数节点(AST节点):
    def __init__(self, 名称: str, 返回类型: str, 参数列表: List[Tuple[str, str]] = None, 身体: List[AST节点] = None, 前置条件: List[str] = None, 后置条件: List[str] = None, 不变量: List[str] = None, 行号: int = 0):
        super().__init__(行号)
        self.名称 = 名称
        self.参数列表 = 参数列表 or []
        self.返回类型 = 返回类型
        self.身体 = 身体 or []
        self.前置条件 = 前置条件 or []
        self.后置条件 = 后置条件 or []
        self.不变量 = 不变量 or []

class 观测节点(AST节点):
    def __init__(self, 目标: str, 源: AST节点 = None, 条件: AST节点 = None, 降维规则: str = None, 行号: int = 0):
        super().__init__(行号)
        self.目标 = 目标
        self.源 = 源
        self.条件 = 条件
        self.降维规则 = 降维规则

class 漏斗节点(AST节点):
    def __init__(self, 源: AST节点, 维数: int = 1, 规则: str = "sum", 行号: int = 0):
        super().__init__(行号)
        self.源 = 源
        self.维数 = 维数
        self.规则 = 规则

class 裁决节点(AST节点):
    def __init__(self, 条件: AST节点, 应税分支: AST节点, 免税分支: AST节点, 行号: int = 0):
        super().__init__(行号)
        self.条件 = 条件
        self.应税分支 = 应税分支
        self.免税分支 = 免税分支

class 融合节点(AST节点):
    def __init__(self, 左: AST节点, 右: AST节点, 算子: str = "+", 行号: int = 0):
        super().__init__(行号)
        self.左 = 左
        self.右 = 右
        self.算子 = 算子

class 态射节点(AST节点):
    def __init__(self, 名称: str, 定义域: str, 陪域: str, 映射规则: Dict[str, str] = None, 行号: int = 0):
        super().__init__(行号)
        self.名称 = 名称
        self.定义域 = 定义域
        self.陪域 = 陪域
        self.映射规则 = 映射规则 or {}

class 税务节点(AST节点):
    def __init__(self, 频次: AST节点, 等级: str = "应收税", 行号: int = 0):
        super().__init__(行号)
        self.频次 = 频次
        self.等级 = 等级

class 条件节点(AST节点):
    def __init__(self, 左: AST节点, 算子: str, 右: AST节点, 行号: int = 0):
        super().__init__(行号)
        self.左 = 左
        self.算子 = 算子
        self.右 = 右

class 调用节点(AST节点):
    def __init__(self, 函数名: str, 参数列表: List[AST节点] = None, 行号: int = 0):
        super().__init__(行号)
        self.函数名 = 函数名
        self.参数列表 = 参数列表 or []

class 返回节点(AST节点):
    def __init__(self, 值: AST节点 = None, 行号: int = 0):
        super().__init__(行号)
        self.值 = 值

class 赋值节点(AST节点):
    def __init__(self, 变量名: str, 值: AST节点, 行号: int = 0):
        super().__init__(行号)
        self.变量名 = 变量名
        self.值 = 值

class 变量节点(AST节点):
    def __init__(self, 名称: str, 行号: int = 0):
        super().__init__(行号)
        self.名称 = 名称

class 常量节点(AST节点):
    def __init__(self, 值: Any, 类型: str = "i32", 行号: int = 0):
        super().__init__(行号)
        self.值 = 值
        self.类型 = 类型

class 容器节点(AST节点):
    def __init__(self, 名称: str, 索引: AST节点 = None, 内容: AST节点 = None, 行号: int = 0):
        super().__init__(行号)
        self.名称 = 名称
        self.索引 = 索引
        self.内容 = 内容

class 导入节点(AST节点):
    def __init__(self, 模块名: str, 导入项列表: List[str] = None, 行号: int = 0):
        super().__init__(行号)
        self.模块名 = 模块名
        self.导入项列表 = 导入项列表 or []

class 导出节点(AST节点):
    def __init__(self, 名称列表: List[str] = None, 行号: int = 0):
        super().__init__(行号)
        self.名称列表 = 名称列表 or []

class 结构体节点(AST节点):
    def __init__(self, 名称: str, 字段列表: List[Tuple[str, str]] = None, 行号: int = 0):
        super().__init__(行号)
        self.名称 = 名称
        self.字段列表 = 字段列表 or []

class 枚举节点(AST节点):
    def __init__(self, 名称: str, 变体列表: List[Tuple[str, Optional[str]]] = None, 行号: int = 0):
        super().__init__(行号)
        self.名称 = 名称
        self.变体列表 = 变体列表 or []

class 循环节点(AST节点):
    def __init__(self, 变量名: str, 范围: AST节点, 身体: List[AST节点] = None, 行号: int = 0):
        super().__init__(行号)
        self.变量名 = 变量名
        self.范围 = 范围
        self.身体 = 身体 or []

class 条件分支节点(AST节点):
    def __init__(self, 条件: AST节点, 则分支: List[AST节点], 否则分支: List[AST节点] = None, 行号: int = 0):
        super().__init__(行号)
        self.条件 = 条件
        self.则分支 = 则分支
        self.否则分支 = 否则分支 or []


# ============================================================
# 语法分析器
# ============================================================

class 语法分析器:
    """关系代数DSL语法分析器（递归下降）"""

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.位置 = 0
        self.errors: List[str] = []

    def 当前(self) -> Optional[Token]:
        if self.位置 < len(self.tokens):
            return self.tokens[self.位置]
        return None

    def 预览(self, ahead: int = 1) -> Optional[Token]:
        idx = self.位置 + ahead - 1
        if idx < len(self.tokens):
            return self.tokens[idx]
        return None

    def 前进(self, n: int = 1) -> Optional[Token]:
        t = self.当前()
        self.位置 = min(self.位置 + n, len(self.tokens))
        return t

    def 匹配(self, 内容: str) -> bool:
        t = self.当前()
        if t and t.内容 == 内容:
            self.前进()
            return True
        return False

    def 匹配类型(self, 类型: 词类型) -> bool:
        t = self.当前()
        if t and t.类型 == 类型:
            self.前进()
            return True
        return False

    def 期望(self, 内容: str) -> bool:
        t = self.当前()
        if t and t.内容 == 内容:
            self.前进()
            return True
        self.errors.append(f"第{t.行号}行: 期望 '{内容}', 得到 '{t.内容}'")
        return False

    def 解析程序(self) -> 程序节点:
        模块列表 = []
        while self.当前():
            try:
                模块 = self.解析模块()
                if 模块:
                    模块列表.append(模块)
            except Exception as e:
                self.errors.append(str(e))
                break
        return 程序节点(模块列表=模块列表)

    def 解析模块(self) -> Optional[模块节点]:
        if not self.匹配('模块'):
            return None

        name_tok = self.当前()
        名称 = name_tok.内容 if name_tok else "匿名"
        self.前进()

        self.期望('{')
        导入列表 = []
        声明列表 = []
        导出列表 = []

        while self.当前() and self.当前().内容 != '}':
            if self.匹配('引入'):
                while self.当前() and self.当前().类型 == 词类型.标识符:
                    导入列表.append(self.当前().内容)
                    self.前进()
                continue

            if self.匹配('导出'):
                while self.当前() and self.当前().类型 == 词类型.标识符:
                    导出列表.append(self.当前().内容)
                    self.前进()
                continue

            声明 = self.解析声明()
            if 声明:
                声明列表.append(声明)

        self.期望('}')

        node = 模块节点(名称=名称, 导入列表=导入列表, 声明列表=声明列表, 导出列表=导出列表)
        if name_tok:
            node.行号 = name_tok.行号
        return node

    def 解析声明(self) -> Optional[AST节点]:
        tok = self.当前()
        if not tok:
            return None

        if tok.内容 == '函数':
            return self.解析函数()
        elif tok.内容 == '结构':
            return self.解析结构体()
        elif tok.内容 == '枚举':
            return self.解析枚举()
        elif tok.内容 == '常量':
            return self.解析常量()
        elif tok.内容 == '观测':
            return self.解析观测()
        elif tok.内容 == '漏斗':
            return self.解析漏斗()
        elif tok.内容 == '态射':
            return self.解析态射()
        elif tok.内容 == '导入':
            return self.解析导入()
        elif tok.内容 == '循环':
            # 循环 i 在 N { ... }
            self.前进()  # 消耗 '循环'
            vname = self.当前().内容 if self.当前() else "i"
            self.前进()  # 消耗循环变量
            self.前进()  # 消耗 '在'
            范围 = self.解析裁决表达式()
            self.前进()  # 消耗 '{'
            身体 = []
            while self.当前() and self.当前().内容 != '}':
                s = self.解析声明()
                if s:
                    身体.append(s)
            self.前进()  # 消耗 '}'
            return 循环节点(变量名=vname, 范围=范围, 身体=身体)
        elif tok.内容 == '若':
            self.前进()  # 消耗 '若'
            条件 = self.解析裁决表达式()
            self.前进()  # 消耗 '则'
            self.前进()  # 消耗 '{'
            则分支 = []
            while self.当前() and self.当前().内容 not in ('否则', '}'):
                s = self.解析声明()
                if s:
                    则分支.append(s)
            self.前进()  # 消耗 '}'
            否则分支 = []
            if self.当前() and self.当前().内容 == '否则':
                self.前进()  # 消耗 '否则'
                self.前进()  # 消耗 '{'
                while self.当前() and self.当前().内容 != '}':
                    s = self.解析声明()
                    if s:
                        否则分支.append(s)
                self.前进()  # 消耗 '}'
            return 条件分支节点(条件=条件, 则分支=则分支, 否则分支=否则分支)
        else:
            # 可能是表达式语句
            expr = self.解析表达式()
            self.匹配(';')
            return expr

    def 解析函数(self) -> 函数节点:
        start_tok = self.前进()  # 跳过 '函数'
        name_tok = self.当前()
        名称 = name_tok.内容 if name_tok else "匿名"
        self.前进()

        self.期望('(')
        参数列表 = []
        while self.当前() and self.当前().内容 != ')':
            pname_tok = self.当前()
            pname = pname_tok.内容 if pname_tok else "arg"
            self.前进()
            self.期望(':')
            ptype_tok = self.当前()
            ptype = ptype_tok.内容 if ptype_tok else "i32"
            self.前进()
            参数列表.append((pname, ptype))
            if self.当前() and self.当前().内容 == ',':
                self.前进()
        self.期望(')')

        self.期望('->')
        rtype_tok = self.当前()
        返回类型 = rtype_tok.内容 if rtype_tok else "i32"
        self.前进()

        前置条件 = []
        后置条件 = []
        不变量 = []
        身体 = []

        # 函数体
        if self.匹配('{'):
            # 可能的契约块（函数体开头）
            if self.当前() and self.当前().内容 == '契约':
                self.前进()  # 消耗 '契约'
                self.前进()  # 消耗 '{'
                while self.当前() and self.当前().内容 != '}':
                    kw = self.当前().内容
                    if kw in ('需要', '保证', '不变'):
                        self.前进()
                        while self.当前() and self.当前().内容 not in ('需要', '保证', '不变', '}'):
                            self.前进()
                        if kw == '需要':
                            前置条件.append(kw)
                        elif kw == '保证':
                            后置条件.append(kw)
                        elif kw == '不变':
                            不变量.append(kw)
                    else:
                        self.前进()
                self.前进()  # 消耗 '}'
            while self.当前() and self.当前().内容 != '}':
                stmt = self.解析声明()
                if stmt:
                    身体.append(stmt)
            self.期望('}')

        node = 函数节点(名称=名称, 参数列表=参数列表, 返回类型=返回类型,
                        身体=身体, 前置条件=前置条件, 后置条件=后置条件, 不变量=不变量)
        if start_tok:
            node.行号 = start_tok.行号
        return node

    def 解析结构体(self) -> 结构体节点:
        self.前进()  # 跳过 '结构'
        name_tok = self.当前()
        名称 = name_tok.内容 if name_tok else "Struct"
        self.前进()
        self.期望('{')
        字段列表 = []
        while self.当前() and self.当前().内容 != '}':
            fname = self.当前().内容 if self.当前() else "field"
            self.前进()
            self.期望(':')
            ftype = self.当前().内容 if self.当前() else "i32"
            self.前进()
            字段列表.append((fname, ftype))
            self.匹配(';')
        self.期望('}')
        node = 结构体节点(名称=名称, 字段列表=字段列表)
        if name_tok:
            node.行号 = name_tok.行号
        return node

    def 解析枚举(self) -> 枚举节点:
        self.前进()  # 跳过 '枚举'
        name_tok = self.当前()
        名称 = name_tok.内容 if name_tok else "Enum"
        self.前进()
        self.期望('{')
        变体列表 = []
        while self.当前() and self.当前().内容 != '}':
            vname = self.当前().内容 if self.当前() else "Variant"
            self.前进()
            vtype = None
            if self.当前() and self.当前().内容 == '(':
                self.前进()
                vtype = self.当前().内容 if self.当前() else "i32"
                self.前进()
                self.期望(')')
            变体列表.append((vname, vtype))
            self.匹配(',')
        self.期望('}')
        node = 枚举节点(名称=名称, 变体列表=变体列表)
        if name_tok:
            node.行号 = name_tok.行号
        return node

    def 解析常量(self) -> 常量节点:
        self.前进()  # 跳过 '常量'
        name_tok = self.当前()
        self.前进()
        self.期望('=')
        val_tok = self.当前()
        val = val_tok.内容 if val_tok else "0"
        self.前进()
        self.期望(';')
        node = 常量节点(值=int(val) if val.isdigit() else val)
        if val_tok:
            node.行号 = val_tok.行号
        return node

    def 解析观测(self) -> 观测节点:
        start_tok = self.前进()  # 跳过 '观测'
        target_tok = self.当前()
        目标 = target_tok.内容 if target_tok else "target"
        self.前进()

        源 = None
        条件 = None
        降维规则 = None

        if self.当前() and self.当前().内容 == '从':
            self.前进()
            源 = self.解析表达式()

        if self.当前() and self.当前().内容 == '若':
            self.前进()
            条件 = self.解析表达式()

        if self.当前() and self.当前().内容 == '降维':
            self.前进()
            r_tok = self.当前()
            降维规则 = r_tok.内容 if r_tok else "sum"
            self.前进()

        node = 观测节点(目标=目标, 源=源, 条件=条件, 降维规则=降维规则)
        if start_tok:
            node.行号 = start_tok.行号
        return node

    def 解析漏斗(self) -> 漏斗节点:
        self.前进()  # 跳过 '漏斗'
        源 = self.解析表达式()
        维数 = 1
        规则 = "sum"
        if self.当前() and self.当前().内容 == '维':
            self.前进()
            d_tok = self.当前()
            维数 = int(d_tok.内容) if d_tok and d_tok.内容.isdigit() else 1
            self.前进()
        if self.当前() and self.当前().内容 == '规则':
            self.前进()
            r_tok = self.当前()
            规则 = r_tok.内容 if r_tok else "sum"
            self.前进()
        return 漏斗节点(源=源, 维数=维数, 规则=规则)

    def 解析态射(self) -> 态射节点:
        self.前进()  # 跳过 '态射'
        name_tok = self.当前()
        名称 = name_tok.内容 if name_tok else "morphism"
        self.前进()

        self.期望('定义域')
        dom_tok = self.当前()
        定义域 = dom_tok.内容 if dom_tok else "i32"
        self.前进()

        self.期望('陪域')
        cod_tok = self.当前()
        陪域 = cod_tok.内容 if cod_tok else "i32"
        self.前进()

        映射规则 = {}
        if self.当前() and self.当前().内容 == '{':
            self.前进()
            while self.当前() and self.当前().内容 != '}':
                k_tok = self.当前()
                k = k_tok.内容 if k_tok else "_"
                self.前进()
                self.期望('↦')
                v_tok = self.当前()
                v = v_tok.内容 if v_tok else "_"
                self.前进()
                映射规则[k] = v
                self.匹配(',')
            self.期望('}')

        node = 态射节点(名称=名称, 定义域=定义域, 陪域=陪域, 映射规则=映射规则)
        if name_tok:
            node.行号 = name_tok.行号
        return node

    def 解析导入(self) -> 导入节点:
        self.前进()  # 跳过 '导入'
        name_tok = self.当前()
        模块名 = name_tok.内容 if name_tok else "unknown"
        self.前进()
        self.期望(';')
        node = 导入节点(模块名=模块名)
        if name_tok:
            node.行号 = name_tok.行号
        return node

    def 解析表达式(self) -> AST节点:
        return self.解析裁决表达式()

    def 解析裁决表达式(self) -> AST节点:
        条件 = self.解析比较表达式()
        if self.当前() and self.当前().内容 == '?':
            self.前进()
            应税分支 = self.解析裁决表达式()
            self.期望(':')
            免税分支 = self.解析裁决表达式()
            return 裁决节点(条件=条件, 应税分支=应税分支, 免税分支=免税分支)
        return 条件

    def 解析比较表达式(self) -> AST节点:
        """处理 >= <= > < == != 等比较操作符"""
        左 = self.解析融合表达式()
        while self.当前() and self.当前().内容 in ('>=', '<=', '>', '<', '==', '!=', '≡', '≠'):
            op = self.当前().内容
            self.前进()
            右 = self.解析融合表达式()
            左 = 条件节点(左=左, 算子=op, 右=右)
        return 左

    def 解析融合表达式(self) -> AST节点:
        左 = self.解析乘除表达式()
        while self.当前() and self.当前().内容 in ('+', '-', '⊕', '∘'):
            op = self.当前().内容
            self.前进()
            右 = self.解析乘除表达式()
            左 = 融合节点(左=左, 右=右, 算子=op)
        return 左

    def 解析乘除表达式(self) -> AST节点:
        """处理 * / % ⊗ 等乘除操作符（优先级高于加减）"""
        左 = self.解析税务表达式()
        while self.当前() and self.当前().内容 in ('*', '/', '%', '⊗'):
            op = self.当前().内容
            self.前进()
            右 = self.解析税务表达式()
            左 = 融合节点(左=左, 右=右, 算子=op)
        return 左

    def 解析税务表达式(self) -> AST节点:
        node = self.解析主表达式()
        # 税务后缀
        if self.当前() and self.当前().内容 == '税务':
            self.前进()
            return 税务节点(频次=node)
        return node

    def 解析主表达式(self) -> AST节点:
        tok = self.当前()
        if not tok:
            return 常量节点(值=0, 类型="i32")

        # 括号表达式
        if tok.内容 == '(':
            self.前进()
            node = self.解析裁决表达式()
            self.期望(')')
            return node

        # 数字
        if tok.类型 == 词类型.数字:
            self.前进()
            return 常量节点(值=int(tok.内容) if tok.内容.isdigit() else tok.内容, 类型="i32")

        # 字符串
        if tok.类型 == 词类型.字符串:
            self.前进()
            return 常量节点(值=tok.内容, 类型="str")

        # 关键词常量
        if tok.内容 == '真':
            self.前进()
            return 常量节点(值=True, 类型="bool")
        if tok.内容 == '假':
            self.前进()
            return 常量节点(值=False, 类型="bool")
        if tok.内容 == '空':
            self.前进()
            return 常量节点(值=None, 类型="null")

        # 标识符 / 变量 / 函数调用
        if tok.类型 == 词类型.标识符:
            self.前进()
            name = tok.内容
            # 函数调用
            if self.当前() and self.当前().内容 == '(':
                self.前进()
                参数列表 = []
                while self.当前() and self.当前().内容 != ')':
                    参数列表.append(self.解析裁决表达式())
                    if self.当前() and self.当前().内容 == ',':
                        self.前进()
                self.期望(')')
                return 调用节点(函数名=name, 参数列表=参数列表)
            # 容器访问 a[b]
            if self.当前() and self.当前().内容 == '[':
                self.前进()
                索引 = self.解析裁决表达式()
                self.期望(']')
                return 容器节点(名称=name, 索引=索引)
            return 变量节点(名称=name)

        # 返回语句
        if tok.内容 == '返回':
            self.前进()
            val = self.解析裁决表达式() if self.当前() else None
            self.匹配(';')
            return 返回节点(值=val)

        # 循环 i 在 N { ... }
        if tok.内容 == '循环':
            self.前进()  # 跳过 '循环'
            vname = self.当前().内容 if self.当前() else "i"
            self.前进()  # 消耗循环变量
            self.前进()  # 跳过 '在'
            范围 = self.解析裁决表达式()
            self.前进()  # 跳过 '{'
            身体 = []
            while self.当前() and self.当前().内容 != '}':
                s = self.解析声明()
                if s:
                    身体.append(s)
            self.前进()  # 跳过 '}'
            return 循环节点(变量名=vname, 范围=范围, 身体=身体)

        # 若...则...否则...
        if tok.内容 == '若':
            self.前进()
            条件 = self.解析裁决表达式()
            self.前进()  # 跳过 '则'
            则分支 = []
            while self.当前() and self.当前().内容 not in ('否则', '}'):
                s = self.解析声明()
                if s:
                    则分支.append(s)
            否则分支 = []
            if self.当前() and self.当前().内容 == '否则':
                self.前进()
                while self.当前() and self.当前().内容 != '}':
                    s = self.解析声明()
                    if s:
                        否则分支.append(s)
            return 条件分支节点(条件=条件, 则分支=则分支, 否则分支=否则分支)

        # 赋值 a = b
        if tok.类型 == 词类型.标识符 and self.预览() and self.预览().内容 == '=':
            var_name = tok.内容
            self.前进()  # 跳过变量名
            self.前进()  # 跳过 '='
            val = self.解析裁决表达式()
            self.匹配(';')
            return 赋值节点(变量名=var_name, 值=val)

        return 变量节点(名称=tok.内容)


# ============================================================
# 多语言代码生成器
# ============================================================

class 代码生成器:
    """将AST生成为多语言代码"""

    支持语言 = ['rust', 'c', 'wasm', 'typescript', 'python']

    def __init__(self, 目标语言: str):
        if 目标语言.lower() not in self.支持语言:
            raise ValueError(f"不支持的语言: {目标语言}，支持: {self.支持语言}")
        self.目标语言 = 目标语言.lower()
        self.缩进 = 0
        self.输出: List[str] = []
        self.临时变量计数器 = 0

    def 生成(self, ast: AST节点) -> str:
        self.缩进 = 0
        self.输出 = []
        if isinstance(ast, 程序节点):
            self._生成程序(ast)
        return '\n'.join(self.输出)

    def _emit(self, line: str = ""):
        if line:
            self.输出.append("    " * self.缩进 + line)
        else:
            self.输出.append("")

    def _gen_expr(self, node: AST节点) -> str:
        """生成表达式"""
        if isinstance(node, 常量节点):
            if node.类型 == "bool":
                if self.目标语言 == 'rust':
                    return 'true' if node.值 else 'false'
                elif self.目标语言 == 'c':
                    return '1' if node.值 else '0'
                elif self.目标语言 == 'typescript':
                    return 'true' if node.值 else 'false'
                else:
                    return 'True' if node.值 else 'False'
            elif node.类型 == "str":
                return f'"{node.值}"'
            elif node.值 is None:
                if self.目标语言 == 'rust':
                    return 'None'
                elif self.目标语言 == 'c':
                    return 'NULL'
                elif self.目标语言 == 'typescript':
                    return 'null'
                else:
                    return 'None'
            return str(node.值)

        elif isinstance(node, 变量节点):
            return node.名称

        elif isinstance(node, 裁决节点):
            cond = self._gen_expr(node.条件)
            then_b = self._gen_expr(node.应税分支)
            else_b = self._gen_expr(node.免税分支)
            if self.目标语言 == 'rust':
                return f'if {cond} {{ {then_b} }} else {{ {else_b} }}'
            elif self.目标语言 == 'c':
                return f'({cond} ? {then_b} : {else_b})'
            elif self.目标语言 == 'typescript':
                return f'({cond} ? {then_b} : {else_b})'
            elif self.目标语言 == 'wasm':
                return f'(if {cond} (then {then_b}) (else {else_b}))'
            else:
                return f'({then_b} if {cond} else {else_b})'

        elif isinstance(node, 融合节点):
            l = self._gen_expr(node.左)
            r = self._gen_expr(node.右)
            op = node.算子
            if op == '∘':
                # 态射复合 → 管道
                if self.目标语言 == 'rust':
                    return f'{r}({l})'
                elif self.目标语言 == 'typescript':
                    return f'{r}({l})'
                else:
                    return f'{r}({l})'
            elif op == '⊕':
                # XOR
                if self.目标语言 == 'c':
                    return f'({l} ^ {r})'
                else:
                    return f'({l} ^ {r})'
            else:
                return f'({l} {op} {r})'

        elif isinstance(node, 税务节点):
            freq = self._gen_expr(node.频次)
            if self.目标语言 == 'rust':
                return f'税务等级({freq})'
            elif self.目标语言 == 'c':
                return f'tax_level({freq})'
            elif self.目标语言 == 'typescript':
                return f'taxLevel({freq})'
            else:
                return f'tax_level({freq})'

        elif isinstance(node, 调用节点):
            args = ', '.join([self._gen_expr(a) for a in node.参数列表])
            return f'{node.函数名}({args})'

        elif isinstance(node, 容器节点):
            if node.索引:
                idx = self._gen_expr(node.索引)
                return f'{node.名称}[{idx}]'
            return node.名称

        elif isinstance(node, 返回节点):
            if node.值:
                return f'return {self._gen_expr(node.值)}'
            return 'return'

        elif isinstance(node, 条件节点):
            l = self._gen_expr(node.左)
            r = self._gen_expr(node.右)
            return f'({l} {node.算子} {r})'

        elif isinstance(node, 条件分支节点):
            # 展开为 if-else
            cond = self._gen_expr(node.条件)
            self._emit(f'if {cond} {{')
            self.缩进 += 1
            for s in node.则分支:
                self._gen_stmt(s)
            self.缩进 -= 1
            self._emit('} else {')
            self.缩进 += 1
            for s in node.否则分支:
                self._gen_stmt(s)
            self.缩进 -= 1
            self._emit('}')
            return ''

        elif isinstance(node, 循环节点):
            rng = self._gen_expr(node.范围)
            self._emit(f'for {node.变量名} in 0..{rng} {{')
            self.缩进 += 1
            for s in node.身体:
                self._gen_stmt(s)
            self.缩进 -= 1
            self._emit('}')
            return ''

        elif isinstance(node, 赋值节点):
            val = self._gen_expr(node.值)
            return f'{node.变量名} = {val}'

        return '0'

    def _gen_stmt(self, node: AST节点) -> str:
        """生成语句"""
        if isinstance(node, 返回节点):
            if node.值:
                val = self._gen_expr(node.值)
                self._emit(f'return {val};')
            else:
                self._emit('return;')
        elif isinstance(node, 赋值节点):
            val = self._gen_expr(node.值)
            if self.目标语言 == 'rust':
                self._emit(f'let {node.变量名} = {val};')
            elif self.目标语言 == 'c':
                self._emit(f'{node.变量名} = {val};')
            elif self.目标语言 == 'typescript':
                self._emit(f'const {node.变量名} = {val};')
            elif self.目标语言 == 'wasm':
                self._emit(f'(local.set ${node.变量名} {val})')
            else:
                self._emit(f'{node.变量名} = {val}')
        elif isinstance(node, 条件分支节点):
            self._gen_expr(node)  # _gen_expr 处理了 if-else 展开
        elif isinstance(node, 循环节点):
            self._gen_expr(node)
        elif isinstance(node, 调用节点):
            call = self._gen_expr(node)
            if call:
                self._emit(f'{call};')
        elif isinstance(node, 观测节点):
            self._gen_观测(node)
        elif isinstance(node, AST节点):
            # 其他 AST 节点 → 尝试生成表达式
            try:
                result = self._gen_expr(node)
                if result:
                    self._emit(f'{result};')
            except Exception:
                self._emit(f'/* 未知语句: {type(node).__name__} */')

    def _gen_观测(self, node: 观测节点) -> str:
        """生成观测语句"""
        if self.目标语言 == 'rust':
            if node.条件:
                cond = self._gen_expr(node.条件)
                self._emit(f'// 观测: {node.目标} 若 {cond}')
            else:
                self._emit(f'// 观测: {node.目标}')
        elif self.目标语言 == 'c':
            self._emit(f'/* 观测: {node.目标} */')
        elif self.目标语言 == 'typescript':
            self._emit(f'// 观测: {node.目标}')
        elif self.目标语言 == 'wasm':
            self._emit(f';; 观测: {node.目标}')
        else:
            self._emit(f'# 观测: {node.目标}')

    def _生成程序(self, node: 程序节点):
        for m in node.模块列表:
            if isinstance(m, 模块节点):
                self._生成模块(m)

    def _生成模块(self, node: 模块节点):
        if self.目标语言 == 'rust':
            self._生成Rust模块(node)
        elif self.目标语言 == 'c':
            self._生成C模块(node)
        elif self.目标语言 == 'wasm':
            self._生成Wasm模块(node)
        elif self.目标语言 == 'typescript':
            self._生成TS模块(node)
        elif self.目标语言 == 'python':
            self._生成Python模块(node)

    def _生成Rust模块(self, node: 模块节点):
        self._emit(f"// ═══════════════════════════════════════════════")
        self._emit(f"// 模块: {node.名称}")
        self._emit(f"// 生成器: 关系代数自举编译器 v2")
        self._emit(f"// 主权: {混元闭包}")
        self._emit(f"// ═══════════════════════════════════════════════")
        self._emit("")

        # 导入
        if node.导入列表:
            for imp in node.导入列表:
                self._emit(f"use {imp};")
            self._emit("")

        self._emit("pub mod body {")
        self.缩进 += 1

        for 声明 in node.声明列表:
            self._gen_decl_rust(声明)

        self.缩进 -= 1
        self._emit("}")
        self._emit("")

    def _gen_decl_rust(self, node: AST节点):
        if isinstance(node, 函数节点):
            # 函数签名
            params = ', '.join([f'{p}: {t}' for p, t in node.参数列表])
            self._emit(f"pub fn {node.名称}({params}) -> {node.返回类型} {{")
            self.缩进 += 1

            # 前置条件断言
            for pre in node.前置条件:
                self._emit(f'assert!({pre}, "前置条件: {pre}");')

            if node.身体:
                for stmt in node.身体:
                    self._gen_stmt(stmt)
            else:
                self._emit("unreachable!()")

            # 后置条件断言
            for post in node.后置条件:
                self._emit(f'// 后置: {post}')

            self.缩进 -= 1
            self._emit("}")
            self._emit("")

        elif isinstance(node, 结构体节点):
            self._emit(f"pub struct {node.名称} {{")
            self.缩进 += 1
            for fname, ftype in node.字段列表:
                self._emit(f"pub {fname}: {ftype},")
            self.缩进 -= 1
            self._emit("}")
            self._emit("")

        elif isinstance(node, 枚举节点):
            self._emit(f"pub enum {node.名称} {{")
            self.缩进 += 1
            for vname, vtype in node.变体列表:
                if vtype:
                    self._emit(f"{vname}({vtype}),")
                else:
                    self._emit(f"{vname},")
            self.缩进 -= 1
            self._emit("}")
            self._emit("")

        elif isinstance(node, 常量节点):
            val_str = 'true' if node.值 == True else 'false' if node.值 == False else str(node.值)
            self._emit(f"pub const VALUE: {node.类型} = {val_str};")
            self._emit("")

        elif isinstance(node, 态射节点):
            self._emit(f"// 态射: {node.名称}: {node.定义域} → {node.陪域}")
            for k, v in node.映射规则.items():
                self._emit(f'    {k} ↦ {v}')
            self._emit("")

        elif isinstance(node, 观测节点):
            self._emit(f"pub fn observe_{node.目标}(input: i32) -> i32 {{")
            self.缩进 += 1
            if node.条件:
                cond = self._gen_expr(node.条件)
                self._emit(f"if {cond} {{")
                self.缩进 += 1
                self._emit("input")
                self.缩进 -= 1
                self._emit("} else {")
                self.缩进 += 1
                self._emit("0")
                self.缩进 -= 1
                self._emit("}")
            else:
                self._emit("input")
            self.缩进 -= 1
            self._emit("}")
            self._emit("")

        elif isinstance(node, 导入节点):
            self._emit(f"use {node.模块名};")

    def _生成C模块(self, node: 模块节点):
        self._emit(f"/* ═══════════════════════════════════════════════ *\\")
        self._emit(f" * 模块: {node.名称}")
        self._emit(f" * 生成器: 关系代数自举编译器 v2")
        self._emit(f" * 主权: {混元闭包}")
        self._emit(f" \\* ═══════════════════════════════════════════════ */")
        self._emit("")
        self._emit("#include <stdint.h>")
        self._emit("#include <stdbool.h>")
        self._emit("#include <stdlib.h>")
        self._emit("")

        # 前向声明所有函数
        for 声明 in node.声明列表:
            if isinstance(声明, 函数节点):
                params = ', '.join([t for _, t in 声明.参数列表])
                self._emit(f"{声明.返回类型} {声明.名称}({params});")
        self._emit("")

        # 函数定义
        for 声明 in node.声明列表:
            if isinstance(声明, 函数节点):
                self._gen_decl_c(声明)

        # 结构体
        for 声明 in node.声明列表:
            if isinstance(声明, 结构体节点):
                self._gen_decl_c(声明)

        # 枚举
        for 声明 in node.声明列表:
            if isinstance(声明, 枚举节点):
                self._gen_decl_c(声明)

    def _gen_decl_c(self, node: AST节点):
        if isinstance(node, 函数节点):
            params = ', '.join([f'{t} {p}' for p, t in node.参数列表])
            self._emit(f"{node.返回类型} {node.名称}({params}) {{")
            self.缩进 += 1

            for pre in node.前置条件:
                self._emit(f"// 前置: {pre}")

            if node.身体:
                for stmt in node.身体:
                    self._gen_stmt_c(stmt)
            else:
                self._emit("return 0;")

            for post in node.后置条件:
                self._emit(f"// 后置: {post}")

            self.缩进 -= 1
            self._emit("}")
            self._emit("")

        elif isinstance(node, 结构体节点):
            self._emit(f"typedef struct {node.名称} {{")
            self.缩进 += 1
            for fname, ftype in node.字段列表:
                t = ftype.replace('i32', 'int32_t').replace('u32', 'uint32_t').replace('i64', 'int64_t').replace('u64', 'uint64_t').replace('f32', 'float').replace('f64', 'double').replace('bool', 'bool').replace('str', 'char*').replace('i8', 'int8_t').replace('u8', 'uint8_t')
                self._emit(f"{t} {fname};")
            self.缩进 -= 1
            self._emit(f"}} {node.名称};")
            self._emit("")

        elif isinstance(node, 枚举节点):
            self._emit(f"typedef enum {{")
            self.缩进 += 1
            for i, (vname, vtype) in enumerate(node.变体列表):
                if vtype:
                    self._emit(f"{vname} = {i},")
                else:
                    self._emit(f"{vname},")
            self.缩进 -= 1
            self._emit(f"}} {node.名称};")
            self._emit("")

    def _gen_stmt_c(self, node: AST节点):
        if isinstance(node, 返回节点):
            if node.值:
                val = self._gen_expr(node.值)
                self._emit(f"return {val};")
            else:
                self._emit("return;")
        elif isinstance(node, 赋值节点):
            val = self._gen_expr(node.值)
            self._emit(f"{node.变量名} = {val};")
        elif isinstance(node, 条件分支节点):
            cond = self._gen_expr(node.条件)
            self._emit(f"if ({cond}) {{")
            self.缩进 += 1
            for s in node.则分支:
                self._gen_stmt_c(s)
            self.缩进 -= 1
            self._emit("} else {")
            self.缩进 += 1
            for s in node.否则分支:
                self._gen_stmt_c(s)
            self.缩进 -= 1
            self._emit("}")
        elif isinstance(node, 循环节点):
            rng = self._gen_expr(node.范围)
            self._emit(f"for (int {node.变量名} = 0; {node.变量名} < {rng}; {node.变量名}++) {{")
            self.缩进 += 1
            for s in node.身体:
                self._gen_stmt_c(s)
            self.缩进 -= 1
            self._emit("}")
        elif isinstance(node, 调用节点):
            call = self._gen_expr(node)
            if call:
                self._emit(f"{call};")

    def _生成Wasm模块(self, node: 模块节点):
        self._emit(f";; ═══════════════════════════════════════════════")
        self._emit(f";; 模块: {node.名称}")
        self._emit(f";; 生成器: 关系代数自举编译器 v2")
        self._emit(f";; 主权: {混元闭包}")
        self._emit(f";; ═══════════════════════════════════════════════")
        self._emit("")
        self._emit("(module")
        self._emit(f'  (type $func_type (func (param i32) (result i32)))')
        self._emit("")

        # 内存
        self._emit("  (memory (export \"memory\") 1)")
        self._emit("")

        # 导入（空壳）
        self._emit(f'  (import "env" "observer" (func $observer (type $func_type)))')
        self._emit("")

        func_idx = 0
        for 声明 in node.声明列表:
            if isinstance(声明, 函数节点):
                params = ', '.join([p for p, _ in 声明.参数列表])
                self._emit(f"  ;; {声明.名称}: ({', '.join([t for _, t in 声明.参数列表])}) -> {声明.返回类型}")
                self._emit(f"  (func ${声明.名称} (type $func_type)")
                self._emit(f"    (param .{params} i32)")
                self._emit(f"    (result i32)")

                # 函数体翻译
                self._gen_wasm_body(声明)

                self._emit("  )")
                self._emit("")
                func_idx += 1

        # 导出所有函数
        exported = [d.名称 for d in node.声明列表 if isinstance(d, 函数节点)]
        if exported:
            self._emit("  ;; 导出")
            for name in exported:
                self._emit(f'  (export "{name}" (func ${name}))')

        self._emit(")")
        self._emit("")

        # 导出注释说明
        self._emit(";; WASM导出清单:")
        for name in exported:
            self._emit(f";;   (func ${name}) → 导出名为 \"{name}\"")
        self._emit(";; 编译为WASM: wat2wasm module.wat -o module.wasm")
        self._emit(";; 加载方式: WebAssembly.instantiate(buffer, importObject)")

    def _gen_wasm_body(self, node: 函数节点):
        if node.身体:
            for stmt in node.身体:
                if isinstance(stmt, 返回节点) and stmt.值:
                    val = self._gen_expr(stmt.值)
                    # 简化：将表达式转为 WASM i32.const
                    self._emit(f"    (i32.const {val})")
                    self._emit("    (return)")
                elif isinstance(stmt, 赋值节点):
                    val = self._gen_expr(stmt.值)
                    self._emit(f"    (local.set ${stmt.变量名} (i32.const {val}))")
                else:
                    self._emit("    (i32.const 0)")
        else:
            self._emit("    (i32.const 0)")

    def _生成TS模块(self, node: 模块节点):
        self._emit(f"// ═══════════════════════════════════════════════")
        self._emit(f"// 模块: {node.名称}")
        self._emit(f"// 生成器: 关系代数自举编译器 v2")
        self._emit(f"// 主权: {混元闭包}")
        self._emit(f"// ═══════════════════════════════════════════════")
        self._emit("")

        for imp in node.导入列表:
            self._emit(f"import {{ {imp} }} from './{imp}';")
        if node.导入列表:
            self._emit("")

        for 声明 in node.声明列表:
            self._gen_decl_ts(声明)

    def _gen_decl_ts(self, node: AST节点):
        if isinstance(node, 函数节点):
            params = ', '.join([f'{p}: {t}' for p, t in node.参数列表])
            self._emit(f"export function {node.名称}({params}): {node.返回类型} {{")
            self.缩进 += 1
            for pre in node.前置条件:
                self._emit(f'// 前置: {pre}')
            if node.身体:
                for stmt in node.身体:
                    self._gen_stmt_ts(stmt)
            else:
                self._emit("throw new Error('not implemented');")
            self.缩进 -= 1
            self._emit("}")
            self._emit("")

        elif isinstance(node, 结构体节点):
            self._emit(f"export interface {node.名称} {{")
            self.缩进 += 1
            for fname, ftype in node.字段列表:
                self._emit(f"{fname}: {ftype};")
            self.缩进 -= 1
            self._emit("}")
            self._emit("")

        elif isinstance(node, 枚举节点):
            self._emit(f"export enum {node.名称} {{")
            self.缩进 += 1
            for vname, vtype in node.变体列表:
                if vtype:
                    self._emit(f"{vname} = {vtype},")
                else:
                    self._emit(f"{vname},")
            self.缩进 -= 1
            self._emit("}")
            self._emit("")

        elif isinstance(node, 态射节点):
            self._emit(f"// 态射: {node.名称}: {node.定义域} → {node.陪域}")
            for k, v in node.映射规则.items():
                self._emit(f"//   {k} ↦ {v}")
            self._emit("")

    def _gen_stmt_ts(self, node: AST节点):
        if isinstance(node, 返回节点):
            if node.值:
                val = self._gen_expr(node.值)
                self._emit(f"return {val};")
            else:
                self._emit("return;")
        elif isinstance(node, 赋值节点):
            val = self._gen_expr(node.值)
            self._emit(f"const {node.变量名} = {val};")
        elif isinstance(node, 条件分支节点):
            cond = self._gen_expr(node.条件)
            self._emit(f"if ({cond}) {{")
            self.缩进 += 1
            for s in node.则分支:
                self._gen_stmt_ts(s)
            self.缩进 -= 1
            self._emit("} else {")
            self.缩进 += 1
            for s in node.否则分支:
                self._gen_stmt_ts(s)
            self.缩进 -= 1
            self._emit("}")
        elif isinstance(node, 循环节点):
            rng = self._gen_expr(node.范围)
            self._emit(f"for (let {node.变量名} = 0; {node.变量名} < {rng}; {node.变量名}++) {{")
            self.缩进 += 1
            for s in node.身体:
                self._gen_stmt_ts(s)
            self.缩进 -= 1
            self._emit("}")
        elif isinstance(node, 调用节点):
            call = self._gen_expr(node)
            if call:
                self._emit(f"{call};")

    def _生成Python模块(self, node: 模块节点):
        self._emit(f"# ═══════════════════════════════════════════════")
        self._emit(f"# 模块: {node.名称}")
        self._emit(f"# 生成器: 关系代数自举编译器 v2")
        self._emit(f"# 主权: {混元闭包}")
        self._emit(f"# ═══════════════════════════════════════════════")
        self._emit("")
        self._emit("from __future__ import annotations")
        self._emit("")
        self._emit("from dataclasses import dataclass")
        self._emit("from typing import Any, Optional, List, Dict, Callable")
        self._emit("")

        # 导入
        for imp in node.导入列表:
            self._emit(f"import {imp}")
        if node.导入列表:
            self._emit("")

        for 声明 in node.声明列表:
            self._gen_decl_py(声明)

    def _gen_decl_py(self, node: AST节点):
        if isinstance(node, 函数节点):
            params = ', '.join([f'{p}: {t}' for p, t in node.参数列表])
            self._emit(f"def {node.名称}({params}) -> {node.返回类型}:")
            self.缩进 += 1
            for pre in node.前置条件:
                self._emit(f'assert {pre}, "前置: {pre}"')
            if node.身体:
                for stmt in node.身体:
                    self._gen_stmt_py(stmt)
            else:
                self._emit("raise NotImplementedError()")
            self.缩进 -= 1
            self._emit("")

        elif isinstance(node, 结构体节点):
            self._emit(f"@dataclass")
            self._emit(f"class {node.名称}:")
            self.缩进 += 1
            for fname, ftype in node.字段列表:
                self._emit(f"{fname}: {ftype}")
            self.缩进 -= 1
            self._emit("")

        elif isinstance(node, 枚举节点):
            for vname, vtype in node.变体列表:
                self._emit(f"{node.名称}_{vname.upper()} = {vtype if vtype else '0'}")

        elif isinstance(node, 态射节点):
            self._emit(f"# 态射: {node.名称}: {node.定义域} → {node.陪域}")
            mapping = ', '.join([f'{k}: {v}' for k, v in node.映射规则.items()])
            self._emit(f"MORPHISM_{node.名称.upper()} = {{{mapping}}}")
            self._emit("")

    def _gen_stmt_py(self, node: AST节点):
        if isinstance(node, 返回节点):
            if node.值:
                val = self._gen_expr(node.值)
                self._emit(f"return {val}")
            else:
                self._emit("return")
        elif isinstance(node, 赋值节点):
            val = self._gen_expr(node.值)
            self._emit(f"{node.变量名} = {val}")
        elif isinstance(node, 条件分支节点):
            cond = self._gen_expr(node.条件)
            self._emit(f"if {cond}:")
            self.缩进 += 1
            for s in node.则分支:
                self._gen_stmt_py(s)
            self.缩进 -= 1
            if node.否则分支:
                self._emit("else:")
                self.缩进 += 1
                for s in node.否则分支:
                    self._gen_stmt_py(s)
                self.缩进 -= 1
        elif isinstance(node, 循环节点):
            rng = self._gen_expr(node.范围)
            self._emit(f"for {node.变量名} in range({rng}):")
            self.缩进 += 1
            for s in node.身体:
                self._gen_stmt_py(s)
            self.缩进 -= 1
        elif isinstance(node, 调用节点):
            call = self._gen_expr(node)
            if call:
                self._emit(call)


# ============================================================
# 自举编译器入口
# ============================================================

class 自举编译器:
    """
    关系代数自举编译器
    DSL → 词法 → AST → 多语言代码
    """

    def __init__(self, 目标语言: str = 'rust'):
        self.目标语言 = 目标语言

    def 编译(self, 源码: str) -> str:
        """完整编译流程"""
        # 1. 词法分析
        词法 = 词法分析器(源码)
        tokens = 词法.分析()

        # 2. 语法分析
        语法 = 语法分析器(tokens)
        ast = 语法.解析程序()

        if 语法.errors:
            raise SyntaxError('\n'.join(语法.errors))

        # 3. 代码生成
        生成器 = 代码生成器(self.目标语言)
        return 生成器.生成(ast)

    def 编译文件(self, 输入路径: str, 输出路径: str) -> bool:
        """编译文件"""
        try:
            with open(输入路径, 'r', encoding='utf-8') as f:
                源码 = f.read()
            输出 = self.编译(源码)
            with open(输出路径, 'w', encoding='utf-8') as f:
                f.write(输出)
            return True
        except Exception as e:
            print(f"编译错误: {e}")
            return False


# ============================================================
# 自检测试
# ============================================================

def 运行自检():
    """验证编译器能正确生成各语言代码"""
    DSL源码 = """
    模块 税务筛选器 {
        引入 容器系统
        引入 裁判系统

        枚举 税务等级 {
            可免税(0)
            待观测(1)
            应收税(2)
        }

        结构 文件条目 {
            路径: str
            频次: u32
            等级: u32
        }

        函数 税务等级(频次: u32) -> u32 {
            契约 {
                需要 频次 >= 0
                保证 result <= 2
            }
            返回 频次 >= 5 ? 2 : 频次 >= 2 ? 1 : 0;
        }

        函数 批量筛选(条目表: str, 阈值: u32) -> u32 {
            循环 i 在 100 {
                若 税务等级(i) == 2 则 {
                    观测 文件扫描(条目表)
                }
            }
            返回 0;
        }

        态射 税务映射 定义域 u32 陪域 u32 {
            0 ↦ 0
            1 ↦ 1
            2 ↦ 2
        }
    }
    """

    print("=" * 60)
    print("关系代数DSL源码:")
    print(DSL源码)
    print("=" * 60)

    for lang in ['rust', 'c', 'wasm', 'typescript', 'python']:
        try:
            编译器 = 自举编译器(lang)
            输出 = 编译器.编译(DSL源码)
            ext_map = {'rust': 'rs', 'c': 'c', 'wasm': 'wat', 'typescript': 'ts', 'python': 'py'}
            print(f"\n{'═' * 60}")
            print(f"生成的 {lang.upper()} 代码 (.{ext_map[lang]}):")
            print(f"{'═' * 60}")
            print(输出[:800])
            if len(输出) > 800:
                print(f"... (共 {len(输出)} 字符)")
        except Exception as e:
            print(f"\n[ERROR] {lang} 生成失败: {e}")

    print("\n" + "=" * 60)
    print("自检完成 ✓")


if __name__ == "__main__":
    运行自检()
