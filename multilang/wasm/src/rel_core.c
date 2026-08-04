// -*- coding: utf-8 -*-
// 关系代数核心 — WASM版
// 编译: wasm-pack build --target web
//
// 目标：在浏览器端直接运行，无需服务器
// 用途：用户本地执行，隐私保护，零依赖

#include <stdint.h>
#include <string.h>

// ============================================================
// WASM内存布局（256字节固定）
// ============================================================

// 地址0-1: 阴箱/阳箱标志
#define ADDR_YIN        0
#define ADDR_YANG       1
// 地址2-255: 254个容器
#define ADDR_CONTAINERS 2
#define CAPACITY        256

// WASM导出函数声明
__attribute__((visibility("default")))
void memory(uint32_t ptr, uint32_t size);

// ============================================================
// 状态向量（全局线性内存）
// ============================================================

static uint8_t  state_vector[CAPACITY];   // 256维状态向量
static uint32_t counters[CAPACITY];         // 计数器
static uint8_t  full_moon = 0;              // 月全食标志

// ============================================================
// 哈希函数
// ============================================================

static uint32_t wasm_hash(const char* s, uint32_t len) {
    uint32_t h = 0;
    for (uint32_t i = 0; i < len; i++) {
        h = h * 31 + (uint32_t)s[i];
    }
    return h;
}

// ============================================================
// 核心API（WASM导出）
// ============================================================

// 初始化状态向量
__attribute__((visibility("default")))
void wasm_init() {
    for (int i = 0; i < CAPACITY; i++) {
        state_vector[i] = 0;
        counters[i] = 0;
    }
    full_moon = 0;
}

// 编码观测记录（输入: id指针, id长度, 频次, 判定结果）
__attribute__((visibility("default")))
void wasm_encode(const char* id, uint32_t id_len, uint32_t freq, uint8_t judgment) {
    // 阴箱
    if (judgment != 1) {  // != EXEMPT
        state_vector[ADDR_YIN] = 1;
    }
    
    // 阳箱
    if (freq > 0) {
        state_vector[ADDR_YANG] = 1;
    }
    
    // 254容器分布
    uint32_t hash = wasm_hash(id, id_len);
    uint32_t base = hash % 254;
    for (int i = 0; i < 3; i++) {
        uint32_t idx = (base + i) % 254;
        uint32_t addr = ADDR_CONTAINERS + idx;
        state_vector[addr] = 1;
        counters[addr] += 1;
    }
    
    // 月全食判定
    uint32_t active = 0;
    for (int i = 0; i < 254; i++) {
        if (counters[ADDR_CONTAINERS + i] > 0) active++;
    }
    if (state_vector[ADDR_YIN] && state_vector[ADDR_YANG] && active >= 254) {
        full_moon = 1;
    }
}

// 获取状态向量（返回指针）
__attribute__((visibility("default")))
uint8_t* wasm_get_state() {
    return state_vector;
}

// 获取月全食状态
__attribute__((visibility("default")))
uint8_t wasm_full_moon() {
    return full_moon;
}

// 获取活跃容器数
__attribute__((visibility("default")))
uint32_t wasm_active_containers() {
    uint32_t cnt = 0;
    for (int i = 0; i < 254; i++) {
        if (counters[ADDR_CONTAINERS + i] > 0) cnt++;
    }
    return cnt;
}

// 漏斗降维：过滤高频词
// 输入: 频次数组指针, 长度, 阈值
// 返回: 满足条件的数量
__attribute__((visibility("default")))
uint32_t wasm_funnel_filter(const uint32_t* freqs, uint32_t len, uint32_t threshold) {
    uint32_t result = 0;
    for (uint32_t i = 0; i < len; i++) {
        if (freqs[i] >= threshold) result++;
    }
    return result;
}

// 统计锥收敛
// 输入: 密度数组指针, 长度, 阈值
// 返回: 满足条件的数量
__attribute__((visibility("default")))
uint32_t wasm_timecone_converge(const double* densities, uint32_t len, double threshold) {
    uint32_t result = 0;
    for (uint32_t i = 0; i < len; i++) {
        if (densities[i] >= threshold) result++;
    }
    return result;
}

// ============================================================
// JS互操作（WASM导入/导出）
// ============================================================

/*
// JavaScript调用示例:
// const wasm = await WebAssembly.instantiateStreaming(fetch('rel_core.wasm'));
// wasm.instance.exports.wasm_init();
// wasm.instance.exports.wasm_encode(idPtr, idLen, freq, judgment);
// const state = wasm.instance.exports.wasm_get_state();
// const fullMoon = wasm.instance.exports.wasm_full_moon();
//
// 完整JS包装器:
// const RelationalWasm = {
//   init() { wasm.instance.exports.wasm_init(); },
//   encode(id, freq, judgment) {
//     const encoder = new TextEncoder();
//     const buf = encoder.encode(id);
//     const ptr = wasm.wasm_alloc(buf.length + 1);
//     // ... 内存写入逻辑
//     wasm.instance.exports.wasm_encode(ptr, buf.length, freq, judgment);
//   },
//   getState() { return wasm.instance.exports.wasm_get_state(); },
//   isFullMoon() { return wasm.instance.exports.wasm_full_moon(); }
// };
*/
