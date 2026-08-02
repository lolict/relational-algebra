name: 功能请求
description: 为项目提出新功能或改进建议
labels: ["enhancement"]
body:
  - type: markdown
    attributes:
      value: |
        ## 功能描述
        请描述您想要的功能或改进。

  - type: textarea
    id: feature-description
    attributes:
      label: 功能详细描述
      placeholder: 请详细描述您期望的功能...
    validations:
      required: true

  - type: textarea
    id: use-case
    attributes:
      label: 使用场景
      placeholder: 这个功能将在什么场景下使用？

  - type: textarea
    id: alternatives
    attributes:
      label: 替代方案
      placeholder: 您考虑过其他替代方案吗？

  - type: checkboxes
    id: confirmation
    attributes:
      label: 确认
      options:
        - label: 我已检查此功能请求不是重复的
          required: true
        - label: 我愿意帮助实现此功能
          required: false
