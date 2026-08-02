#!/bin/bash
# =============================================================================
# 文档自动生成脚本
# =============================================================================
# 用途：自动生成 API 文档
# 作者：莫刘连理萝莉兰零离

set -e

echo "============================================"
echo "  主体间关系代数 - 文档生成"
echo "============================================"

# 创建文档目录
mkdir -p docs/api
mkdir -p docs/source

# 使用 pdoc 生成 API 文档
echo "生成 API 文档..."
python3 -m pdoc \
    --output-dir docs/api \
    --force \
    relational_algebra

# 复制 README 作为索引
if [ -f "README.md" ]; then
    cp README.md docs/index.md
fi

echo ""
echo "文档已生成到 docs/api/ 目录"
echo "打开 docs/api/index.html 查看"
