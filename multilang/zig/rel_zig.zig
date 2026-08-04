// -*- coding: utf-8 -*-
//! 关系代数核心 — Zig语言版
//!
//! 用途：高性能/编译时检查/ WASM打包
//! 编译：zig build-exe rel_zig.zig
//!
//! Zig哲学：没有隐藏控制流，没有隐藏内存分配，编译期计算

const std = @import("std");
const fmt = std.fmt;

// ============================================================
// 常量定义
// ============================================================
const CAPACITY_CONTAINERS: usize = 254;
const CAPACITY_TOTAL: usize = 256;
const YIN_BOX: usize = 0;
const YANG_BOX: usize = 1;

// ============================================================
// 核心枚举
// ============================================================

pub const Judgment = enum(u2) {
    taxable = 0,  // 应收税
    exempt = 1,   // 可免税
    pending = 2,  // 待观测
};

pub const Polarity = enum(u1) {
    yin = 0,  // 虚无
    yang = 1, // 存在
};

// ============================================================
// 数据结构
// ============================================================

pub fn Observer(comptime T: type) type {
    return struct {
        id: []const u8,
        content: T,
        timestamp: u64,
        frequency: u32,
        judgment: Judgment,
        density: f64,
    };
}

pub fn ContainerSystem(comptime T: type) type {
    return struct {
        const Self = @This();
        
        yin_box: u32 = 0,
        yang_box: u32 = 0,
        containers: [CAPACITY_CONTAINERS]u32 = [_]u32{0} ** CAPACITY_CONTAINERS,
        state_vector: [CAPACITY_TOTAL]u8 = [_]u8{0} ** CAPACITY_TOTAL,
        full_moon: bool = false,
        
        pub fn encode(self: *Self, obs: Observer(T)) void {
            // 阴箱
            if (obs.judgment != .exempt) {
                self.state_vector[YIN_BOX] = 1;
                self.yin_box += 1;
            }
            
            // 阳箱
            if (obs.frequency > 0) {
                self.state_vector[YANG_BOX] = 1;
                self.yang_box += 1;
            }
            
            // 254容器分布
            const hash = Self.simpleHash(obs.id);
            const base = hash % CAPACITY_CONTAINERS;
            inline for (0..3) |i| {
                const idx = (base + i) % CAPACITY_CONTAINERS;
                self.state_vector[2 + idx] = 1;
                self.containers[idx] += 1;
            }
            
            // 月全食判定
            var active: usize = 0;
            for (self.containers) |c| if (c > 0) active += 1;
            self.full_moon = self.yin_box > 0 and self.yang_box > 0 and active >= CAPACITY_CONTAINERS;
        }
        
        pub fn judgeTax(frequency: u32) Judgment {
            if (frequency >= 5) return .taxable;
            if (frequency <= 1) return .exempt;
            return .pending;
        }
        
        fn simpleHash(s: []const u8) usize {
            var h: usize = 0;
            for (s) |b| h = h.* +% @as(usize, b);
            return h;
        }
        
        pub fn activeCount(self: *const Self) usize {
            var count: usize = 0;
            for (self.containers) |c| if (c > 0) count += 1;
            return count;
        }
    };
}

// 统计锥
pub fn TimeCone(comptime T: type, comptime max_size: usize) type {
    return struct {
        const Self = @This();
        
        records: [max_size]?*const Observer(T) = [_]?*const Observer(T){null} ** max_size,
        count: usize = 0,
        accumulated_weight: f64 = 0.0,
        
        pub fn push(self: *Self, obs: *const Observer(T)) void {
            if (self.count < max_size) {
                self.records[self.count] = obs;
                self.count += 1;
                self.accumulated_weight += obs.density;
            }
        }
        
        pub fn converge(self: *const Self, threshold: f64) []const *const Observer(T) {
            var result: [max_size]*const Observer(T) = undefined;
            var len: usize = 0;
            for (self.records[0..self.count]) |opt_obs| {
                if (opt_obs) |obs| {
                    if (obs.density >= threshold) {
                        result[len] = obs;
                        len += 1;
                    }
                }
            }
            return result[0..len];
        }
    };
}

// ============================================================
// 漏斗降维路由器
// ============================================================

pub fn FunnelRouter(comptime T: type) type {
    return struct {
        const Self = @This();
        
        high_threshold: u32,
        low_threshold: u32,
        
        pub fn dimensionReduce(
            self: *const Self,
            word_freqs: []const struct { word: []const u8, freq: u32 }
        ) struct { taxable: []const []const u8, exempt: []const []const u8 } {
            var taxable_list: [1024][]const u8 = undefined;
            var exempt_list: [1024][]const u8 = undefined;
            var t_len: usize = 0;
            var e_len: usize = 0;
            
            for (word_freqs) |wf| {
                if (wf.freq >= self.high_threshold) {
                    taxable_list[t_len] = wf.word;
                    t_len += 1;
                }
                if (wf.freq <= self.low_threshold) {
                    exempt_list[e_len] = wf.word;
                    e_len += 1;
                }
            }
            
            return .{
                .taxable = taxable_list[0..t_len],
                .exempt = exempt_list[0..e_len],
            };
        }
    };
}

// ============================================================
// 夫妻共同体融合
// ============================================================

pub const FusionClosure = struct {
    yin_weights: std.AutoHashMap([]const u8, f64),
    yang_weights: std.AutoHashMap([]const u8, f64),
    monoid_closure: std.AutoHashMap([]const u8, f64),
    
    pub fn fuse(self: *FusionClosure) void {
        var yin_total: f64 = 0.0;
        var yang_total: f64 = 0.0;
        
        var yin_iter = self.yin_weights.valueIterator();
        while (yin_iter.next()) |v| yin_total += v.*;
        
        var yang_iter = self.yang_weights.valueIterator();
        while (yang_iter.next()) |v| yang_total += v.*;
        
        // 混元闭包 = 阴 × 阳的交叉权重
        var yin_iter2 = self.yin_weights.iterator();
        while (yin_iter2.next()) |entry| {
            const word = entry.key_ptr.*;
            const yin_w = entry.value_ptr.*;
            if (self.yang_weights.get(word)) |yang_w| {
                const closure_w = (yin_w * yang_w) / @max(yin_total * yang_total, 1.0);
                self.monoid_closure.put(word, closure_w) catch {};
            }
        }
    }
};

// ============================================================
// 主函数
// ============================================================

pub fn main() void {
    std.debug.print("🔮 关系代数核心引擎 — Zig版\n", .{});
    std.debug.print("================================\n", .{});
    
    // 容器系统
    var cs = ContainerSystem([]const u8){};
    
    // 创建观测记录
    const obs1 = Observer([]const u8){
        .id = "doc_zig",
        .content = "Zig高性能引擎",
        .timestamp = 1,
        .frequency = 10,
        .judgment = .taxable,
        .density = 0.8,
    };
    const obs2 = Observer([]const u8){
        .id = "doc_rust",
        .content = "Rust安全系统",
        .timestamp = 2,
        .frequency = 3,
        .judgment = .pending,
        .density = 0.5,
    };
    
    cs.encode(obs1);
    cs.encode(obs2);
    
    std.debug.print("阴箱: {d} | 阳箱: {d} | 月全食: {!}\n", .{
        cs.yin_box, cs.yang_box, cs.full_moon,
    });
    std.debug.print("活跃容器: {d}/254\n", .{cs.activeCount()});
    
    // 漏斗降维
    var router = FunnelRouter([]const u8){ .high_threshold = 5, .low_threshold = 1 };
    const word_freqs = [_]struct { word: []const u8, freq: u32 }{
        .{ .word = "关系", .freq = 10 },
        .{ .word = "代数", .freq = 8 },
        .{ .word = "观测", .freq = 3 },
        .{ .word = "测试", .freq = 1 },
    };
    const result = router.dimensionReduce(&word_freqs);
    std.debug.print("应税词: {d} | 免税词: {d}\n", .{
        result.taxable.len, result.exempt.len,
    });
    
    std.debug.print("✅ Zig引擎运行正常\n", .{});
}

test "container_moon" {
    var cs = ContainerSystem(u8){};
    const obs = Observer(u8){
        .id = "test",
        .content = 0,
        .timestamp = 1,
        .frequency = 10,
        .judgment = .taxable,
        .density = 0.8,
    };
    cs.encode(obs);
    try std.testing.expect(cs.yin_box > 0);
    try std.testing.expect(cs.yang_box > 0);
}
