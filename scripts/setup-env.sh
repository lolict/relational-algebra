#!/bin/bash
# =============================================================================
# 环境初始化脚本
# =============================================================================
# 用途：检查 Python 版本，安装依赖，验证环境
# 作者：莫刘连理萝莉兰零离

set -e

echo "============================================"
echo "  主体间关系代数 - 环境初始化"
echo "============================================"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 检查 Python 版本
echo -e "${YELLOW}[检查] Python 版本...${NC}"
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.8"

if command -v python3 &> /dev/null; then
    echo -e "${GREEN}✓ Python 已安装: $(python3 --version)${NC}"
else
    echo -e "${RED}✗ Python 3 未安装${NC}"
    exit 1
fi

# 检查 pip
echo -e "${YELLOW}[检查] pip...${NC}"
if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}✓ pip 已安装${NC}"
else
    echo -e "${RED}✗ pip 未安装${NC}"
    exit 1
fi

# 创建虚拟环境（可选）
if [ ! -d "venv" ] && [ ! -d ".venv" ]; then
    echo ""
    read -p "是否创建虚拟环境？(Y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        echo -e "${YELLOW}[创建] 虚拟环境...${NC}"
        python3 -m venv .venv
        source .venv/bin/activate
        echo -e "${GREEN}✓ 虚拟环境已创建并激活${NC}"
    fi
fi

# 安装依赖
echo ""
echo -e "${YELLOW}[安装] 项目依赖...${NC}"
pip install --upgrade pip
pip install -e .

# 安装开发依赖
echo ""
read -p "是否安装开发依赖（测试、类型检查等）？(y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    pip install -e ".[dev]"
    echo -e "${GREEN}✓ 开发依赖安装完成${NC}"
fi

# 验证安装
echo ""
echo -e "${YELLOW}[验证] 安装...${NC}"
python3 -c "
import relational_algebra
print(f'  版本: {relational_algebra.__version__}')
print(f'  作者: {relational_algebra.__author__}')
print('  模块列表:')
for name in relational_algebra.__all__:
    print(f'    - {name}')
"

echo ""
echo -e "${GREEN}============================================"
echo "  环境初始化完成！"
echo "============================================${NC}"
echo ""
echo "后续步骤："
echo "  1. 运行测试: python -m pytest"
echo "  2. 启动开发: 编辑 relational_algebra/ 目录下的代码"
echo ""
