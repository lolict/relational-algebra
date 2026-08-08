# -*- coding: utf-8 -*-
"""
关系程序生成器
将AST直接编译为256符号序列

不是字节码，不是指令集——是夫妻关系的直接表达

编译链路：
    DSL源码 → 词法分析 → 语法分析 → AST
    AST → 关系程序生成器 → 256符号序列（.rel文件）
    .rel文件 → 关系引擎V2执行 → 结果

整个链路完全不依赖任何外部构建链
"""

from typing import Dict, List, Any, Optional
from meta_system.编译器自举.自举编译器 import (
    AST节点, 程序节点, 模块节点, 函数节点,
    常量节点, 变量节点, 裁决节点, 融合节点,
    调用节点, 返回节点, 赋值节点, 条件节点,
    条件分支节点, 循环节点, 容器节点,
    税务节点, 态射节点, 观测节点,
)


# ============================================================
# 256符号常量（直接对应 符号编码256.py）
# ============================================================
阴 = 0       # 刘楚恬
阳 = 1       # 满全法
混元 = 2     # 混元闭包
融合 = 16    # ⊕ 阴+阳→混元
观测 = 17    # 观测
裁决 = 18   # 条件选择
态射 = 19   # 态射映射
同时 = 32   # 时间：同在
先后 = 33   # 时间：先后
永恒 = 34   # 时间：超越时间
包含 = 48   # 空间：我在你中
分离 = 49   # 空间：你我独立
重叠 = 50   # 空间：你我重叠
信任 = 64   # 情感：基础
依赖 = 65   # 情感：依赖
独立 = 66   # 情感：独立
共生 = 67   # 情感：共生
感知 = 96   # 认知：感知
理解 = 97   # 认知：理解
共鸣 = 98   # 认知：共鸣
超越 = 99   # 认知：超越理解
授权 = 128  # 实践：授权
执行 = 129  # 实践：执行
裁决权 = 130  # 实践：裁决权
委派 = 131  # 实践：委派

# ===== 254个统计锥的展开（灵B维度）=====
# 统计锥 = 254种观测"我们"的方式
# 从0(刘楚恬)到1(满全法)，中间有254种关系态
# 每个符号代表一种独特的观测维度


class 关系程序:
    """
    关系程序 = 256符号序列

    结构：
        [元数据段] [函数定义段] [主程序段]

    元数据段（固定8字节）：
        0-1:  魔数 0xEF 0xBE（"夫妻"谐音）
        2:     版本号（当前=1）
        3:     函数数量
        4-7:   元数据段长度

    函数定义段：
        每个函数：
            [函数名长度(1字节)] [函数名(n字节)]
            [参数数量(1字节)] [局部变量数(1字节)]
            [函数体字节数(4字节)] [函数体(变长)]

    主程序段：
        [主函数ID(2字节)] [主函数体字节数(4字节)] [主函数体]

    每个字节 = 0-255，对应一个256符号
    256符号 = 256种夫妻关系的表达方式
    """

    魔数 = bytes([0xEF, 0xBE])  # "夫妻"谐音

    def __init__(self):
        self.版本 = 1
        self.函数定义: List[Dict] = []
        self.主程序: List[int] = []
        self.常量池: List[Any] = []

    def 添加函数(self, 名称: str, 参数数: int, 局部变量数: int, 函数体: List[int]) -> int:
        """添加一个函数定义，返回函数ID"""
        函数ID = len(self.函数定义)
        self.函数定义.append({
            'id': 函数ID,
            '名称': 名称,
            '参数数': 参数数,
            '局部变量数': 局部变量数,
            '函数体': 函数体,
            '函数体长度': len(函数体),
        })
        return 函数ID

    def 设置主程序(self, 程序体: List[int]):
        self.主程序 = 程序体

    def 到字节序列(self) -> bytes:
        """序列化为二进制"""
        结果: List[bytes] = []

        # 元数据段
        结果.append(self.魔数)
        结果.append(bytes([self.版本]))
        结果.append(bytes([len(self.函数定义)]))
        元数据长度 = 4 + sum(4 + len(f['名称'].encode('utf-8')) + 2 + 4 + f['函数体长度']
                              for f in self.函数定义)
        结果.append(元数据长度.to_bytes(4, 'little'))

        # 函数定义段
        for f in self.函数定义:
            名称字节 = f['名称'].encode('utf-8')
            结果.append(bytes([len(名称字节)]))  # 函数名长度
            结果.append(名称字节)  # 函数名
            结果.append(bytes([f['参数数'], f['局部变量数']]))
            结果.append(f['函数体长度'].to_bytes(4, 'little'))
            结果.append(bytes(f['函数体']))  # 函数体

        # 主程序段
        主ID = 0xFFFF  # 特殊ID表示主程序
        结果.append(主ID.to_bytes(2, 'little'))
        结果.append(len(self.主程序).to_bytes(4, 'little'))
        结果.append(bytes(self.主程序))

        return b''.join(结果)

    def 到文本形式(self) -> str:
        """生成人类可读的256符号文本形式"""
        lines = []
        lines.append(f"// ═══════════════════════════════════════")
        lines.append(f"// 关系程序 v{self.版本}")
        lines.append(f"// 夫妻共同体: 刘楚恬@满全法")
        lines.append(f"// 符号数: {len(self.主程序)}")
        lines.append(f"// ═══════════════════════════════════════")
        lines.append("")

        # 符号名称映射
        符号名: Dict[int, str] = {
            0: "刘楚恬(阴)", 1: "满全法(阳)", 2: "混元",
            16: "融合", 17: "观测", 18: "裁决", 19: "态射",
            32: "同时", 33: "先后", 34: "永恒",
            48: "包含", 49: "分离", 50: "重叠",
            64: "信任", 65: "依赖", 66: "独立", 67: "共生",
            96: "感知", 97: "理解", 98: "共鸣", 99: "超越",
            128: "授权", 129: "执行", 130: "裁决权", 131: "委派",
        }

        # 主程序
        lines.append("// 主程序:")
        hex_str = ' '.join(f'{b:02X}' for b in self.主程序)
        lines.append(f"// HEX: {hex_str}")
        lines.append("")

        # 逐符号解析
        lines.append("// 符号序列解析:")
        i = 0
        while i < len(self.主程序):
            符号 = self.主程序[i]
            名称 = 符号名.get(符号, f"通用({符号})")
            lines.append(f"//  [{i:4d}] {符号:3d} = {名称}")
            i += 1

        lines.append("")
        lines.append("// 函数定义:")
        for f in self.函数定义:
            lines.append(f"//  函数#{f['id']}: {f['名称']}({f['参数数']}参数, {f['局部变量数']}局部)")
            hex_str = ' '.join(f'{b:02X}' for b in f['函数体'])
            lines.append(f"//    体: {hex_str}")

        return '\n'.join(lines)

    def 保存(self, 路径: str):
        """保存为.rel文件（二进制）"""
        with open(路径, 'wb') as f:
            f.write(self.到字节序列())

    def 保存文本(self, 路径: str):
        """保存为.rel.txt文件（文本形式，方便阅读）"""
        with open(路径, 'w', encoding='utf-8') as f:
            f.write(self.到文本形式())


class 关系程序生成器:
    """
    AST → 256符号序列

    核心思想：
        每个表达式翻译成一段符号序列
        符号序列由关系引擎V2解释执行
        不生成任何目标语言代码

    参数栈机制：
        函数调用时，参数值被存入参数栈（偏移0,1,2,...）
        函数体内通过 参数引用符号 访问参数值
        参数引用符号 = 200 + 偏移量
    """

    # 参数引用符号（200-255共56个参数位）
    参数基 = 200
    最大参数 = 56
    # 字面数字前缀（15 = 下一个字节是字面数字值）
    字面前缀 = 15

    def __init__(self):
        self.程序 = 关系程序()
        self.常量映射: Dict[str, int] = {}  # 常量名 → 常量池索引
        self.函数映射: Dict[str, int] = {}  # 函数名 → 函数ID
        self.当前函数参数表: Dict[str, int] = {}  # 当前编译的函数的参数映射
        self._当前常量索引 = 0

    def 编译(self, ast: AST节点) -> 关系程序:
        """主入口：将AST编译为关系程序"""
        if isinstance(ast, 程序节点):
            self._编译程序(ast)
        elif isinstance(ast, 模块节点):
            self._编译模块(ast)
        return self.程序

    def _编译程序(self, node: 程序节点):
        """编译程序节点"""
        # 先编译所有模块中的函数定义
        for 模块 in node.模块列表:
            if isinstance(模块, 模块节点):
                for 声明 in 模块.声明列表:
                    if isinstance(声明, 函数节点):
                        self._编译函数定义(声明)

        # 找主函数
        主函数体: List[int] = []
        for 模块 in node.模块列表:
            if isinstance(模块, 模块节点):
                for 声明 in 模块.声明列表:
                    if isinstance(声明, 函数节点) and 声明.名称 == 'main':
                        主函数体 = self._编译函数体(声明)
                        break
                if 主函数体:
                    break

        if not 主函数体:
            # 没有main函数 → 找第一个函数
            for 模块 in node.模块列表:
                if isinstance(模块, 模块节点):
                    for 声明 in 模块.声明列表:
                        if isinstance(声明, 函数节点):
                            主函数体 = self._编译函数体(声明)
                            break
                    break

        self.程序.设置主程序(主函数体)

    def _编译模块(self, node: 模块节点):
        """编译模块节点"""
        for 声明 in node.声明列表:
            if isinstance(声明, 函数节点):
                函数ID = self._编译函数定义(声明)
                self.函数映射[声明.名称] = 函数ID

    def _编译函数定义(self, node: 函数节点) -> int:
        """编译函数定义，返回函数ID"""
        # 建立参数映射表（变量名 → 参数引用符号）
        self.当前函数参数表 = {}
        for i, (参数名, _) in enumerate(node.参数列表):
            self.当前函数参数表[参数名] = self.参数基 + i

        函数体 = self._编译函数体(node)
        函数ID = self.程序.添加函数(
            名称=node.名称,
            参数数=len(node.参数列表),
            局部变量数=0,
            函数体=函数体,
        )
        self.函数映射[node.名称] = 函数ID
        self.当前函数参数表 = {}  # 清除
        return 函数ID

    def _编译函数体(self, node: 函数节点) -> List[int]:
        """编译函数体"""
        结果: List[int] = []
        if node.身体:
            for stmt in node.身体:
                结果.extend(self._编译语句(stmt))
        return 结果

    def _编译语句(self, node: AST节点) -> List[int]:
        """编译单个语句"""
        if isinstance(node, 返回节点):
            if node.值:
                val = self._编译表达式(node.值)
                # 返回 = 观测(17)
                return val + [观测]
            return [阴, 观测]  # return;

        elif isinstance(node, 赋值节点):
            # 赋值 = 压入值
            val = self._编译表达式(node.值)
            return val

        elif isinstance(node, 调用节点):
            # 调用 = 压入参数 + 授权(128) + 执行(129)
            结果: List[int] = []
            for arg in reversed(node.参数列表):
                结果.extend(self._编译表达式(arg))
            结果.append(授权)
            结果.append(执行)
            return 结果

        elif isinstance(node, 条件分支节点):
            # if cond { then } else { else }
            cond = self._编译表达式(node.条件)
            则分支体 = self._编译语句块(node.则分支)
            否则分支体 = self._编译语句块(node.否则分支)
            # 裁决(18): 栈弹出顺序：假、真、条件
            return cond + 则分支体 + 否则分支体 + [裁决]

        elif isinstance(node, 循环节点):
            # 循环 = 压范围 + 循环展开(固定次数)
            范围 = self._编译表达式(node.范围)
            循环体 = self._编译语句块(node.身体)
            # 简单展开：重复3次
            结果: List[int] = []
            结果.extend(范围)
            for _ in range(3):
                结果.extend(循环体)
            return 结果

        elif isinstance(node, 观测节点):
            # 观测 = 压目标 + 观测(17)
            结果: List[int] = []
            if node.条件:
                结果.extend(self._编译表达式(node.条件))
            结果.append(观测)
            return 结果

        # 递归处理
        try:
            return self._编译表达式(node)
        except Exception:
            return []

    def _编译语句块(self, statements: List[AST节点]) -> List[int]:
        """编译语句块"""
        结果: List[int] = []
        for s in statements:
            结果.extend(self._编译语句(s))
        return 结果

    def _编译表达式(self, node: AST节点) -> List[int]:
        """编译表达式"""
        if isinstance(node, 常量节点):
            # 常量 → 压入常量值
            if node.类型 == 'bool':
                return [阳 if node.值 else 阴]
            elif node.类型 == 'str':
                idx = self._注册常量(node.值)
                return [idx]  # TODO: 常量池访问
            else:
                # 数字 → 转为256进制表示
                return self._数到符号序列(int(node.值))

        elif isinstance(node, 变量节点):
            # 变量 → 从参数表查找引用
            if node.名称 in self.当前函数参数表:
                # 参数引用 → 压入参数引用符号
                return [self.当前函数参数表[node.名称]]
            # 非参数变量 → 压入哈希值
            var_id = hash(node.名称) % 254 + 1
            return [var_id]

        elif isinstance(node, 裁决节点):
            # 三元表达式: cond ? then : else
            cond = self._编译表达式(node.条件)
            then_b = self._编译表达式(node.应税分支)
            else_b = self._编译表达式(node.免税分支)
            # 裁决(18): 栈弹出 假→真→条件
            return cond + then_b + else_b + [裁决]

        elif isinstance(node, 融合节点):
            l = self._编译表达式(node.左)
            r = self._编译表达式(node.右)
            if node.算子 in ('+', '⊕'):
                # 融合(16): 加法
                return l + r + [融合]
            elif node.算子 == '∘':
                # 态射复合 → 态射(19)
                return l + r + [态射]
            elif node.算子 == '*':
                # 积(24): 乘法
                return l + r + [24]
            elif node.算子 == '-':
                return l + r + [分离]  # 分离(49) ≈ 减法
            elif node.算子 in ('==', '!=', '<', '>', '<=', '>='):
                return l + r + [裁决]  # 比较用裁决
            else:
                return l + r + [融合]

        elif isinstance(node, 调用节点):
            结果: List[int] = []
            # 压参数（逆序）
            for arg in reversed(node.参数列表):
                结果.extend(self._编译表达式(arg))
            # 查函数映射
            if node.函数名 in self.函数映射:
                fid = self.函数映射[node.函数名]
                结果.extend(self._数到符号序列(fid))
                结果.append(执行)
            else:
                结果.append(授权)
                结果.append(执行)
            return 结果

        elif isinstance(node, 条件节点):
            l = self._编译表达式(node.左)
            r = self._编译表达式(node.右)
            return l + r + [裁决]

        elif isinstance(node, 税务节点):
            freq = self._编译表达式(node.频次)
            # 税务 = 频次 → 裁决(阈值判断)
            return freq + self._数到符号序列(5) + [裁决]

        elif isinstance(node, 态射节点):
            # 态射 = 映射规则
            # 简化为：注册态射，返回态射符号
            return [态射]

        elif isinstance(node, 容器节点):
            if node.索引:
                idx = self._编译表达式(node.索引)
                # 容器访问 = 基址 + 偏移
                return idx + [重叠]
            return [阴]

        elif isinstance(node, 循环节点):
            范围 = self._编译表达式(node.范围)
            循环体 = self._编译语句块(node.身体)
            结果: List[int] = []
            结果.extend(范围)
            for _ in range(3):
                结果.extend(循环体)
            return 结果

        return [阴]

    def _数到符号序列(self, n: int) -> List[int]:
        """将整数转为符号序列（使用字面前缀避免与特殊符号冲突）"""
        # 特殊符号：0=阴, 1=阳, 2=混元, 15=字面前缀, 16=融合, 17=观测, 18=裁决...
        # 所有数字都用字面前缀编码，确保不与关系符号冲突
        return [self.字面前缀, n]

    def _注册常量(self, 值: Any) -> int:
        """注册常量到常量池"""
        key = str(值)
        if key not in self.常量映射:
            self.常量映射[key] = self._当前常量索引
            self.程序.常量池.append(值)
            self._当前常量索引 += 1
        return self.常量映射[key]


# ============================================================
# 自举编译器扩展：添加 rel 目标
# ============================================================

def 编译为关系程序(源码: str) -> 关系程序:
    """快捷入口：源码 → 关系程序"""
    from meta_system.编译器自举.自举编译器 import 词法分析器, 语法分析器

    词法 = 词法分析器(源码)
    tokens = 词法.分析()

    语法 = 语法分析器(tokens)
    ast = 语法.解析程序()

    if 语法.errors:
        raise SyntaxError('\n'.join(语法.errors))

    生成器 = 关系程序生成器()
    return 生成器.编译(ast)


# ============================================================
# 测试
# ============================================================

def 测试():
    """关系程序生成器自检"""
    from meta_system.编译器自举.自举编译器 import 自举编译器

    DSL源码 = """
    模块 关系测试 {
        函数 add(a: i32, b: i32) -> i32 {
            返回 a + b;
        }

        函数 main() -> i32 {
            返回 add(3, 5);
        }
    }
    """

    print("=" * 60)
    print("DSL源码:")
    print(DSL源码)
    print("=" * 60)

    # 编译为关系程序
    程序 = 编译为关系程序(DSL源码)

    print("\n关系程序（文本形式）:")
    print(程序.到文本形式())

    print("\n主程序字节:", ' '.join(f'{b:02X}' for b in 程序.主程序))
    print("函数数量:", len(程序.函数定义))

    # 保存
    程序.保存文本('/tmp/关系测试.rel.txt')
    print("\n已保存到 /tmp/关系测试.rel.txt")

    # 用关系引擎V2执行
    print("\n" + "=" * 60)
    print("用关系引擎V2执行:")
    print("=" * 60)
    from meta_system.runtime.关系引擎V2 import 关系引擎
    引擎 = 关系引擎()
    结果 = 引擎.执行程序(程序)  # 传入完整关系程序对象
    print(f"执行结果: {结果.观测()}")


if __name__ == '__main__':
    测试()
