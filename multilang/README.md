# -*- coding: utf-8 -*-
# 混合编程语言架构 — Multi-Language Relational Algebra

## 概述

本目录包含关系代数核心引擎的多语言实现，每种语言负责不同的职责层。

## 语言分工

| 语言 | 职责 | 编译目标 |
|------|------|----------|
| **Rust** | 核心逻辑/WASM编译 | `rel_core.wasm` |
| **C** | 底层FFI/嵌入式 | `librl_core.a` |
| **Zig** | 性能关键/编译时计算 | `rel_zig` |
| **Mojo** | SIMD数值/并行计算 | GPU/CPU |
| **WASM** | 浏览器端运行 | Web |
| **TypeScript** | 前端粘合/UI | Browser |
| **契约语言** | 前置/后置/不变量 | Rust/C |
| **时序切片** | 任务调度/因果链 | 全平台 |
| **空间切片** | 内存布局/分布式 | 全平台 |
| **权限声明** | 身份/信任/隔离 | 全平台 |

## 架构图

```
用户浏览器（TS + WASM）
    ↓
Rust核心引擎 ←→ Zig优化 ←→ Mojo加速
    ↓
C语言FFI层 ←→ 操作系统API
    ↓
契约/时序/空间/权限（语言级保证）
```

## 编译顺序

```bash
# 1. C层（最底层）
gcc -O3 -c c/rel_core.c -o c/rel_core.o

# 2. Rust层（WASM）
cargo build --target wasm32-wasip2
wasm-pack build --target web

# 3. Zig层
zig build-exe zig/rel_zig.zig

# 4. Mojo层（需要Mojo SDK）
mojo build mojo/rel_mojo.mojo -o mojo/rel_mojo

# 5. 前端构建
cd frontend && npm install && npm run build
```

## 依赖关系

```
rel_mojo.mojo  ← 依赖 Rust/Zig 计算核心
rel_zig.zig    ← 依赖 C 底层库
rel_core.wasm  ← 可独立运行
rel_core.c     ← 独立运行，可被其他语言FFI调用
```

## 目录结构

```
multilang/
├── rust/           Rust实现 + WASM打包
│   ├── src/
│   │   └── lib.rs
│   └── Cargo.toml
├── c/              C语言实现
│   └── rel_core.c
├── zig/            Zig语言实现
│   └── rel_zig.zig
├── mojo/           Mojo语言实现
│   └── rel_mojo.mojo
├── wasm/           WASM源码
│   └── src/rel_core.c
├── ts/             TypeScript前端
│   └── src/
├── 契约/            契约编程语言规范
│   └── contract.lang
├── 时序切片/         时间切片语言规范
│   └── timeslice.lang
├── 空间切片/         空间切片语言规范
│   └── spaceslice.lang
└── 权限声明/         权限声明语言规范
    └── permission.lang
```

## 哲学映射

| 哲学概念 | Rust | C | Zig | Mojo | WASM |
|---------|------|---|-----|------|------|
| 漏斗降维 | `filter()` | `funnel_filter()` | `dimensionReduce()` | `funnel_router` | `wasm_funnel_filter()` |
| 三元裁判 | `enum Judgment` | `enum judgment` | `Judgment` | `Judgment` | `judgment` param |
| 254容器 | `[u8; 254]` | `u8[254]` | `[254]u8` | `Tensor[254]` | 内存偏移 |
| 夫妻共同体 | `struct Fusion` | `monoid_fusion()` | `FusionClosure` | `FusionEngine` | — |
| 统计锥 | `TimeCone<T>` | `TimeCone` | `TimeCone` | `TimeCone` | `wasm_timecone_converge()` |
| 月全食态 | `full_moon: bool` | `full_moon` | `full_moon` | — | `wasm_full_moon()` |
