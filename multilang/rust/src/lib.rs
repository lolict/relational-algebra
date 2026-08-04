// -*- coding: utf-8 -*-
//! 关系代数核心引擎 — Rust/WASM版
//! 
//! 目标：编译为WASM，运行在浏览器端
//! 编译：cargo build --target wasm32-wasip2 或 wasm-pack
//!
//! 哲学对应：
//! - 漏斗降维  = FilterMap + reduce
//! - 三元裁判  = TriState<Accept/Reject/Pending>
//! - 254容器   = [u8; 254] 固定长度数组
//! - 夫妻共同体 = Monoid<Yin, Yang>
//! - 统计锥    = TimeCone<T>

use std::collections::{HashMap, HashSet};
use std::hash::Hash;

// ============================================================
// 核心类型定义
// ============================================================

/// 二元观测：存在/虚无
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum 二元 {
    阴,  // 虚无/间接存在
    阳,  // 存在/直接观测
}

/// 三元裁判：裁决结果
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum 裁判 {
    应收税,   // 高价值，接受
    可免税,   // 低价值，拒绝
    待观测,   // 不确定，继续观测
}

/// 观测者记录
#[derive(Debug, Clone)]
pub struct 观测者<T: Clone + Hash + Eq> {
    pub id: String,
    pub 内容: T,
    pub 时间戳: u64,
    pub 频次: u32,
    pub 标签: HashSet<String>,
    pub 裁判结果: 裁判,
    pub 间接存在密度: f64,
}

/// 统计锥：时间累积的视角切片
#[derive(Debug, Clone)]
pub struct 统计锥<T: Clone> {
    pub 时间片: Vec<观测者<T>>,
    pub 累积权重: f64,
    pub 当前容器索引: usize,
}

impl<T: Clone + Hash + Eq> 统计锥<T> {
    pub fn 新() -> Self {
        统计锥 {
            时间片: Vec::new(),
            累积权重: 0.0,
            当前容器索引: 0,
        }
    }

    /// 添加观测记录，推进统计锥
    pub fn 观测(&mut self, 记录: 观测者<T>) {
        self.累积权重 += 记录.间接存在密度;
        self.时间片.push(记录);
    }

    /// 漏斗降维：收敛到核心观测
    pub fn 收敛(&self, 阈值: f64) -> Vec<&观测者<T>> {
        self.时间片
            .iter()
            .filter(|r| r.间接存在密度 >= 阈值)
            .collect()
    }
}

// ============================================================
// 254二进制容器系统
// ============================================================

/// 256容器：阴(0) + 阳(1) + 254统计位
#[derive(Debug, Clone)]
pub struct 容器系统 {
    阴箱: u32,                  // 阴观测计数
    阳箱: u32,                  // 阳观测计数
    容器: [u32; 254],          // 254个统计容器
    满全态: bool,               // 是否达成月全食
}

impl 容器系统 {
    pub fn 新() -> Self {
        容器系统 {
            阴箱: 0,
            阳箱: 0,
            容器: [0u32; 254],
            满全态: false,
        }
    }

    /// 税务筛选：根据频次判断应税等级
    pub fn 税务等级(频次: u32) -> 裁判 {
        if 频次 >= 5 { 裁判::应收税 }
        else if 频次 <= 1 { 裁判::可免税 }
        else { 裁判::待观测 }
    }

    /// 编码观测者到256容器
    pub fn 编码(&mut self, 记录: &观测者<String>) -> [u8; 256] {
        let mut 向量 = [0u8; 256];
        
        // 阴箱
        if 记录.裁判结果 != 裁判::可免税 {
            向量[0] = 1;
            self.阴箱 += 1;
        }
        
        // 阳箱
        向量[1] = if 记录.频次 > 0 { 1 } else { 0 };
        if 向量[1] == 1 { self.阳箱 += 1; }
        
        // 254容器：根据哈希分布
        let hash = self._简单哈希(&记录.id);
        let base = (hash % 254) as usize;
        for i in 0..3 {
            let idx = (base + i) % 254;
            向量[2 + idx] = 1;
            self.容器[idx] += 1;
        }
        
        // 月全食判定
        self.满全态 = self.阴箱 > 0 && self.阳箱 > 0 
                      && self.容器.iter().sum::<u32>() >= 254;
        
        向量
    }

    fn _简单哈希(&self, s: &str) -> usize {
        s.bytes().fold(0usize, |acc, b| acc.wrapping_mul(31).wrapping_add(b as usize))
    }

    pub fn 是否月全食(&self) -> bool { self.满全态 }
    pub fn 活跃容器数(&self) -> usize {
        self.容器.iter().filter(|&&x| x > 0).count()
    }
}

// ============================================================
// 夫妻共同体融合引擎
// ============================================================

/// 融合状态：阴（原始数据）+ 阳（处理结果）
#[derive(Debug, Clone)]
pub struct 融合状态 {
    pub 阴态: HashMap<String, u32>,      // 原始词频
    pub 阳态: HashMap<String, HashMap<String, u32>>,  // 文档→词频
    pub 混元闭包: HashMap<String, f64>,   // 融合后的权重
}

impl 融合状态 {
    pub fn 新() -> Self {
        融合状态 {
            阴态: HashMap::new(),
            阳态: HashMap::new(),
            混元闭包: HashMap::new(),
        }
    }

    /// 阴 + 阳 = 混元闭包（满全法融合）
    pub fn 融合(&mut self) {
        // 阴态权重
        let 阴权重: f64 = self.阴态.values().map(|&v| v as f64).sum();
        // 阳态权重
        let 阳权重: f64 = self.阳态.values()
            .flat_map(|m| m.values())
            .map(|&v| v as f64)
            .sum();
        
        // 混元闭包 = 阴 × 阳 的交叉权重
        for (词, 阴频) in &self.阴态 {
            for (_, 阳映射) in &self.阳态 {
                if let Some(&阳频) = 阳映射.get(词) {
                    let 权重 = (*阴频 as f64) * (阳频 as f64) / (阴权重 * 阳权重).max(1.0);
                    *self.混元闭包.entry(词.clone()).or_insert(0.0) += 权重;
                }
            }
        }
    }
}

// ============================================================
// 漏斗路由器
// ============================================================

pub struct 漏斗路由器 {
    pub 高频阈值: u32,
    pub 低频阈值: u32,
}

impl 漏斗路由器 {
    pub fn 新(高频: u32, 低频: u32) -> Self {
        漏斗路由器 { 高频阈值: 高频, 低频阈值: 低频 }
    }

    /// 降维：海量词频 → 核心税务词
    pub fn 降维(&self, 词频: &HashMap<String, u32>) -> (HashSet<String>, HashSet<String>) {
        let 应税: HashSet<String> = 词频.iter()
            .filter(|(_, &v)| v >= self.高频阈值)
            .map(|(k, _)| k.clone())
            .collect();
        let 免税: HashSet<String> = 词频.iter()
            .filter(|(_, &v)| v <= self.低频阈值)
            .map(|(k, _)| k.clone())
            .collect();
        (应税, 免税)
    }
}

// ============================================================
// WASM导出接口
// ============================================================

#[cfg(target_arch = "wasm32")]
extern "C" {
    #[wasm_bindgen]
    fn 报告状态(状态: &str);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn 测试月全食态() {
        let mut 容器 = 容器系统::新();
        let 记录 = 观测者 {
            id: "测试".to_string(),
            内容: "内容".to_string(),
            时间戳: 1,
            频次: 10,
            标签: HashSet::new(),
            裁判结果: 裁判::应收税,
            间接存在密度: 0.8,
        };
        容器.编码(&记录);
        assert!(容器.阴箱 > 0);
        assert!(容器.阳箱 > 0);
    }

    #[test]
    fn 测试统计锥收敛() {
        let mut 锥 = 统计锥::新();
        for i in 0..5 {
            锥.观测(观测者 {
                id: format!("doc_{}", i),
                内容: format!("内容{}", i),
                时间戳: i,
                频次: i as u32,
                标签: HashSet::new(),
                裁判结果: 裁判::应收税,
                间接存在密度: 0.5 + (i as f64) * 0.1,
            });
        }
        let 核心 = 锥.收敛(0.7);
        assert!(核心.len() >= 1);
    }
}
