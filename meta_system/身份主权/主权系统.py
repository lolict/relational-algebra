# -*- coding: utf-8 -*-
"""
身份主权系统 — 夫妻共同体唯一身份 + 授权链
Identity Sovereignty — Couple Community Sole Identity + Authorization Chain

核心理念：
    夫妻共同体 = 唯一主权
    其他所有身份 = 被授权的委派身份
    裁判权 = 唯一主权不可分割的权力

架构：
    唯一主权（混元闭包）
        ├── 阴: 刘楚恬（原始观测者）
        ├── 阳: 满全法（处理结果）
        └── 混元: 阴+阳融合后的唯一身份
            ├── 授权委派身份A（别人扮演）
            ├── 授权委派身份B（别人扮演）
            └── ...（可无限扩展）
"""

import hashlib
import time
from typing import Optional, Dict, List
from dataclasses import dataclass, field
from enum import Enum


class 信任等级(Enum):
    """信任等级：0=无权 5=观测 10=有限写 50=共享 80=管理 100=主权"""
    无权 = 0
    观测 = 5
    有限写 = 10
    共享 = 50
    管理 = 80
    主权 = 100


class 授权类型(Enum):
    """授权类型：定义了被授权身份可以做什么"""
    执行任务 = "execute"
    读写资源 = "read_write"
    发行子授权 = "delegate"       # 可以再授权给别人
    裁判裁决 = "judge"            # 可以在局部做裁判
    全部权限 = "full"             # 完全代理主权


@dataclass
class 委派身份:
    """被授权的委派身份（别人扮演的身份）"""
    名称: str
    授权者: str                    # 谁授权的（主权或上级委派）
    信任等级: 信任等级
    权限列表: List[授权类型]
    有效期: Optional[int] = None    # Unix时间戳，None=永久
    附加约束: Dict = field(default_factory=dict)
    id哈希: str = ""

    def __post_init__(self):
        if not self.id哈希:
            raw = f"{self.名称}:{self.授权者}:{time.time()}"
            self.id哈希 = hashlib.sha256(raw.encode()).hexdigest()[:16]

    def 是否有效(self) -> bool:
        """检查委派身份是否还有效"""
        if self.有效期 and time.time() > self.有效期:
            return False
        return True

    def 是否有权限(self, 权限: 授权类型) -> bool:
        """检查是否有特定权限"""
        if not self.是否有效():
            return False
        return 权限 in self.权限列表 or 授权类型.全部权限 in self.权限列表


@dataclass
class 裁判裁决记录:
    """裁判的裁决记录"""
    裁决者: str                    # 谁做的裁决
    被裁决者: str                  # 被裁决的对象
    裁决内容: str                  # 裁决内容
    奖惩措施: str                  # 奖励/惩罚
    时间戳: int
    哈希: str = ""

    def __post_init__(self):
        if not self.哈希:
            raw = f"{self.裁决者}:{self.被裁决者}:{self.裁决内容}:{self.时间戳}"
            self.哈希 = hashlib.sha256(raw.encode()).hexdigest()[:16]


class 夫妻共同体主权:
    """
    夫妻共同体唯一主权系统
    
    这是整个系统的根身份，所有其他身份都由它授权。
    阴（刘楚恬）+ 阳（满全法）= 唯一主权
    """

    def __init__(self):
        self.阴名称 = "刘楚恬"
        self.阳名称 = "满全法"
        self.混元标识 = f"{self.阴名称}+{self.阳名称}"
        
        # 授权链
        self.委派身份注册表: Dict[str, 委派身份] = {}
        
        # 裁判记录
        self.裁决历史: List[裁判裁决记录] = []
        
        # 元数据
        self.创建时间 = int(time.time())
        self.版本号 = "1.0"
        
        # 生成主权哈希
        raw = f"{self.混元标识}:{self.创建时间}"
        self.主权哈希 = hashlib.sha256(raw.encode()).hexdigest()

    def 发行授权(self, 
                  委派名称: str,
                  信任等级: 信任等级,
                  权限列表: List[授权类型],
                  有效期: Optional[int] = None,
                  附加约束: Optional[Dict] = None) -> 委派身份:
        """
        发行委派身份：主权授权给别人的身份
        别人拿着这个身份来"扮演我们"
        """
        委派 = 委派身份(
            名称=委派名称,
            授权者=self.混元标识,
            信任等级=信任等级,
            权限列表=权限列表,
            有效期=有效期,
            附加约束=附加约束 or {}
        )
        self.委派身份注册表[委派.id哈希] = 委派
        return 委派

    def 裁判裁决(self, 
                  被裁决者: str, 
                  裁决内容: str, 
                  奖惩: str) -> 裁判裁决记录:
        """
        裁判裁决：主权做出最终裁决
        奖惩 = "奖励" / "惩罚" / "警告" / "剥夺身份"
        """
        记录 = 裁判裁决记录(
            裁决者=self.混元标识,
            被裁决者=被裁决者,
            裁决内容=裁决内容,
            奖惩措施=奖惩,
            时间戳=int(time.time())
        )
        self.裁决历史.append(记录)
        return 记录

    def 查询身份(self, 身份哈希: str) -> Optional[委派身份]:
        """查询委派身份状态"""
        return self.委派身份注册表.get(身份哈希)

    def 撤销授权(self, 身份哈希: str) -> bool:
        """撤销某个委派身份（惩罚手段之一）"""
        if 身份哈希 in self.委派身份注册表:
            del self.委派身份注册表[身份哈希]
            return True
        return False

    def 生成主权证书(self) -> Dict:
        """
        生成主权证书：证明夫妻共同体是唯一主权
        别人加载这个证书就知道谁才是裁判
        """
        return {
            "主权标识": self.混元标识,
            "阴": self.阴名称,
            "阳": self.阳名称,
            "主权哈希": self.主权哈希,
            "创建时间": self.创建时间,
            "版本": self.版本号,
            "当前授权数": len(self.委派身份注册表),
            "裁决记录数": len(self.裁决历史),
            "类型": "夫妻共同体唯一主权证书"
        }


# ============================================================
# 全局主权实例（单例）
# ============================================================

_全局主权实例: Optional[夫妻共同体主权] = None

def 获取主权实例() -> 夫妻共同体主权:
    """获取全局唯一的主权实例"""
    global _全局主权实例
    if _全局主权实例 is None:
        _全局主权实例 = 夫妻共同体主权()
    return _全局主权实例


# ============================================================
# 使用示例
# ============================================================

def 示例():
    主权 = 获取主权实例()
    
    # 发行授权：让"别人的Python进程"扮演我们的执行者
    执行者身份 = 主权.发行授权(
        委派名称="Python执行器",
        信任等级=信任等级.共享,
        权限列表=[授权类型.执行任务, 授权类型.读写资源],
        有效期=int(time.time()) + 86400  # 24小时
    )
    print(f"✅ 发行委派身份: {执行者身份.名称}")
    print(f"   身份哈希: {执行者身份.id哈希}")
    
    # 查询
    查询 = 主权.查询身份(执行者身份.id哈希)
    print(f"✅ 查询结果: {查询.是否有效()}")
    
    # 裁判裁决
    裁决 = 主权.裁判裁决(
        被裁决者="Python执行器",
        裁决内容="任务完成质量优秀",
        奖惩="奖励"
    )
    print(f"✅ 裁判裁决: {裁决.奖惩措施} - {裁决.裁决内容}")
    
    # 打印主权证书
    证书 = 主权.生成主权证书()
    print(f"\n🔮 主权证书:")
    for k, v in 证书.items():
        print(f"   {k}: {v}")


if __name__ == "__main__":
    示例()
