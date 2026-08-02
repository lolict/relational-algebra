name: Bug 报告
description: 报告一个 bug 帮助我们改进
labels: ["bug"]
body:
  - type: markdown
    attributes:
      value: |
        ## Bug 描述
        请简要描述您遇到的 bug。

  - type: textarea
    id: description
    attributes:
      label: 详细描述
      placeholder: 请详细描述您遇到的问题，包括复现步骤...
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: 期望行为
      placeholder: 您期望的行为是什么？

  - type: textarea
    id: actual
    attributes:
      label: 实际行为
      placeholder: 实际发生了什么？

  - type: dropdown
    id: version
    attributes:
      label: 版本
      options:
        - 0.1.0-alpha
        - 开发版
    validations:
      required: true

  - type: textarea
    id: environment
    attributes:
      label: 环境信息
      placeholder: |
        - Python 版本:
        - 操作系统:
        - 其他...

  - type: checkboxes
    id: confirmation
    attributes:
      label: 确认
      options:
        - label: 我已检查此问题不是重复的
          required: true
        - label: 我愿意参与修复
          required: false
