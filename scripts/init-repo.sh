#!/bin/bash
# =============================================================================
# 仓库初始化脚本
# =============================================================================
# 用途：初始化 Git 仓库，添加远程仓库，执行初始提交
# 作者：莫刘连理萝莉兰零离

set -e  # 遇到错误立即退出

echo "============================================"
echo "  主体间关系代数 - 仓库初始化"
echo "============================================"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查是否已在 Git 仓库中
if [ -d ".git" ]; then
    echo -e "${YELLOW}警告：当前目录已经是一个 Git 仓库${NC}"
    read -p "是否要重新初始化？(y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "取消初始化"
        exit 0
    fi
    rm -rf .git
fi

# 获取用户输入的远程仓库URL
REMOTE_URL=${1:-""}
if [ -z "$REMOTE_URL" ]; then
    echo "请输入远程仓库URL（例如：https://github.com/user/repo.git）"
    read -p "远程仓库URL: " REMOTE_URL
fi

# 初始化仓库
echo -e "${GREEN}[1/5] 初始化 Git 仓库...${NC}"
git init

# 配置提交者信息（如果未设置）
if [ -z "$(git config user.name)" ]; then
    echo "请设置提交者用户名"
    read -p "用户名: " USER_NAME
    git config user.name "$USER_NAME"
fi

if [ -z "$(git config user.email)" ]; then
    echo "请设置提交者邮箱"
    read -p "邮箱: " USER_EMAIL
    git config user.email "$USER_EMAIL"
fi

# 添加所有文件
echo -e "${GREEN}[2/5] 暂存所有文件...${NC}"
git add .

# 创建初始提交
echo -e "${GREEN}[3/5] 创建初始提交...${NC}"
git commit -m "初始提交：主体间关系代数编程范式

- 认知隔离舱实现 (CognitiveIsolationPod)
- 感知总线 (PerceptionBus) - 50种感知通道
- 窄腰中间表示 (Narrow-Waist IR)
- 漏斗前端 (Funnel Frontend)
- 自举编译器 (Bootstrap Compiler)
- 认知相位分析器 (CognitivePhaseAnalyzer)
- 归属确定性引擎 (AttributionEngine)

作者：莫刘连理萝莉兰零离"

# 添加远程仓库
if [ -n "$REMOTE_URL" ]; then
    echo -e "${GREEN}[4/5] 添加远程仓库...${NC}"
    git remote add origin "$REMOTE_URL"
    echo "远程仓库已添加: origin -> $REMOTE_URL"
fi

# 显示状态
echo -e "${GREEN}[5/5] 完成！${NC}"
echo ""
echo "============================================"
echo "  Git 仓库初始化完成"
echo "============================================"
echo ""
echo "常用命令："
echo "  查看状态: git status"
echo "  查看历史: git log --oneline"
echo "  推送代码: git push -u origin main"
echo "  查看差异: git diff"
echo ""
