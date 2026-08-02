# 贡献指南

感谢您对主体间关系代数项目的关注！我们欢迎各种形式的贡献。

## 如何贡献

### 1. 报告问题

如果您发现了 bug 或有功能建议，请：

1. 搜索现有 Issue，避免重复
2. 创建新 Issue，包含：
   - 清晰的标题和描述
   - 复现步骤
   - 期望行为 vs 实际行为
   - 环境信息（Python版本等）

### 2. 提交代码

#### 开发流程

1. **Fork 本仓库**
2. **克隆到本地**
   ```bash
   git clone https://github.com/your-username/relational-algebra.git
   cd relational-algebra
   ```
3. **创建功能分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或修复bug
   git checkout -b fix/issue-number
   ```
4. **安装开发环境**
   ```bash
   ./scripts/setup-env.sh
   pip install -e ".[dev]"
   ```
5. **进行开发**
   - 遵循现有代码风格
   - 添加必要的测试
   - 更新文档

6. **提交更改**
   ```bash
   git add .
   git commit -m "feat: 添加新功能描述"
   ```
   
   提交信息格式：
   - `feat:` 新功能
   - `fix:` 修复bug
   - `docs:` 文档更新
   - `style:` 代码格式（不影响功能）
   - `refactor:` 重构
   - `test:` 测试相关
   - `chore:` 构建/工具

7. **推送分支**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **创建 Pull Request**

### 3. 代码规范

#### Python 代码

- 遵循 PEP 8
- 使用类型注解
- 每行不超过 100 字符
- 使用中文注释和文档字符串

示例：
```python
def process_memory(
    pod: IsolationPod,
    channel: PerceptionChannel,
    intensity: float = 1.0
) -> MemoryPoint:
    """
    处理记忆的函数
    
    参数：
        pod: 目标隔离舱
        channel: 感知通道
        intensity: 记忆强度
    
    返回：
        新创建的 MemoryPoint
    """
    return pod.remember(
        content=None,
        description="",
        channels={channel},
        intensity=intensity,
    )
```

#### Git 提交

- 使用中文描述
- 简洁明了
- 参考上面的格式

### 4. 测试

所有新功能必须包含测试：

```python
def test_memory_channel():
    """测试记忆点通道功能"""
    pod = IsolationPod("test_pod", "TestUser")
    mp = pod.remember(
        description="测试记忆",
        channels={PerceptionChannel.SIGHT},
    )
    assert PerceptionChannel.SIGHT in mp.perception_channels
```

运行测试：
```bash
python -m pytest -v
```

### 5. 文档

- 更新对应的 .md 文件
- API 文档使用 docstring
- 复杂逻辑添加注释说明

## 分支策略

```
main          # 稳定版本
  ↑
develop       # 开发分支
  ↑
feature/*     # 功能分支
fix/*         # 修复分支
docs/*        # 文档分支
```

## 问题解答

如果您有任何问题，请：
- 查看 [README.md](./README.md)
- 查看 [协议文档](./docs/PROTOCOL_SPEC.md)
- 创建 Issue 提问

## 行为准则

请遵守我们的 [行为准则](./docs/CODE_OF_CONDUCT.md)。

感谢您的贡献！
