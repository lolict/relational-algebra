name: Pull Request 模板
description: 提交 Pull Request 时的模板
labels: []
body:
  - type: markdown
    attributes:
      value: |
        ## 描述
        请简要描述您的 Pull Request 解决了什么问题。

  - type: dropdown
    id: change-type
    attributes:
      label: 变更类型
      options:
        - feat: 新功能
        - fix: 修复 bug
        - docs: 文档更新
        - style: 代码格式（不影响功能）
        - refactor: 重构
        - test: 测试相关
        - chore: 构建/工具

  - type: textarea
    id: details
    attributes:
      label: 详细说明
      placeholder: 请提供更详细的变更说明...

  - type: textarea
    id: testing
    attributes:
      label: 测试说明
      placeholder: 请描述您是如何测试这些变更的...

  - type: checkboxes
    id: checklist
    attributes:
      label: 检查清单
      options:
        - label: 我的代码遵循项目的代码规范
          required: true
        - label: 我已经添加了必要的测试
          required: true
        - label: 所有测试都通过了
          required: true
        - label: 我已经更新了相关文档
          required: false
