# -*- coding: utf-8 -*-
"""
局部文件系统关系代数处理器
将文件系统映射为关系代数运算空间
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Set, Tuple
import re


@dataclass
class 文件节点:
    路径: str
    内容: str
    行数: int = 0
    词种: Set[str] = None
    
    def __post_init__(self):
        if self.词种 is None:
            self.词种 = set()


class 局部文件系统关系代数处理器:
    """
    局部文件系统 → 关系代数映射
    
    阴 = 文件路径（原始观测）
    阳 = 词频统计（融合结果）
    混元闭包 = 词种集合（融合态）
    """
    
    def __init__(self, 根目录: str):
        self.根目录 = Path(根目录)
        self.文件列表: List[文件节点] = []
        self.词频表: Dict[str, int] = {}
        self.词种集: Set[str] = set()
        self._已扫描 = False
    
    def 扫描(self) -> int:
        """递归扫描目录下所有文本文件"""
        文档计数 = 0
        for 文件 in self.根目录.rglob("*"):
            if 文件.is_file() and self._是文本文件(文件):
                try:
                    内容 = 文件.read_text(encoding='utf-8', errors='ignore')
                    节点 = 文件节点(路径=str(文件), 内容=内容, 行数=len(内容.splitlines()))
                    self.文件列表.append(节点)
                    self._融合词频(内容)
                    文档计数 += 1
                except Exception:
                    pass
        self._已扫描 = True
        return 文档计数
    
    def 漏斗(self, 最小频次: int = 1) -> Dict[str, int]:
        """漏斗运算：按最小频次过滤"""
        return {词: 频 for 词, 频 in self.词频表.items() if 频 >= 最小频次}
    
    def 观测(self, 词: str) -> Dict[str, int]:
        """观测单个词在各文档中的分布"""
        结果 = {}
        for 节点 in self.文件列表:
            if 词 in 节点.内容:
                结果[节点.路径] = 结果.get(节点.路径, 0) + 1
        return 结果
    
    def 词种数(self) -> int:
        return len(self.词种集)
    
    def 总频次(self) -> int:
        return sum(self.词频表.values())
    
    def 文档数(self) -> int:
        return len(self.文件列表)
    
    def _是文本文件(self, 路径: Path) -> bool:
        后缀 = 路径.suffix.lower()
        return 后缀 in ['.txt', '.md', '.py', '.js', '.ts', '.json', '.yaml', '.yml', 
                       '.toml', '.ini', '.cfg', '.conf', '.log', '.csv', '.html', 
                       '.css', '.xml', '.sql', '.sh', '.bat', '.ps1', '.c', '.cpp',
                       '.h', '.hpp', '.rs', '.go', '.java', '.kt', '.swift']
    
    def _融合词频(self, 内容: str):
        """融合词频：正则分词"""
        词表 = re.findall(r'[\w\u4e00-\u9fff]+', 内容)
        for 词 in 词表:
            if len(词) >= 2:  # 过滤单字
                self.词频表[词] = self.词频表.get(词, 0) + 1
                self.词种集.add(词)
