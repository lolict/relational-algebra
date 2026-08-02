#!/bin/bash
# =============================================================================
# 部署脚本
# =============================================================================
# 用途：将代码推送到远程仓库
# 作者：莫刘连理萝莉兰零离

set -e

echo "============================================"
echo "  主体间关系代数 - 部署脚本"
echo "============================================"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 检查是否有未提交的更改
if [ -n "$(git status --porcelain)" ]; then
    echo -e "${YELLOW}警告：存在未提交的更改${NC}"
    git status --short
    echo ""
    read -p "是否先提交这些更改？(Y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        echo "请输入提交信息："
        read COMMIT_MSG
        git add .
        git commit -m "$COMMIT_MSG"
    fi
fi

# 获取分支名
BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "当前分支: $BRANCH"

# 推送到远程
echo ""
echo -e "${YELLOW}推送代码到远程仓库...${NC}"
git push -u origin "$BRANCH"

echo ""
echo -e "${GREEN}============================================"
echo "  部署完成！"
echo "============================================${NC}"
