# CASBOT02 二次开发文档

基于 MkDocs Material 构建的 CASBOT02 人形机器人二次开发在线文档。

## 本地开发

### 环境要求

- Python 3.11+
- pip

### 安装依赖

```bash
pip install -r requirements.txt
```

### 本地预览

```bash
mkdocs serve
```

浏览器打开 http://127.0.0.1:8000 查看文档。

### 构建静态站点

```bash
mkdocs build
```

构建产物输出到 `site/` 目录。

## 多版本管理

使用 [mike](https://github.com/jimporter/mike) 管理多版本文档：

```bash
# 安装 mike
pip install mike

# 发布 v1.0 版本
mike deploy v1.0

# 发布 v1.1 版本
mike deploy v1.1

# 设置默认版本
mike set-default --push v1.1

# 列出所有版本
mike list
```

## 目录结构

```
docs/
├── index.md                    # 首页
├── getting-started/            # 快速开始
│   ├── overview.md             # 系统概述
│   ├── environment-setup.md    # 环境搭建
│   ├── urdf.md                 # URDF 模型
│   └── quickstart.md           # 快速上手
├── hardware/                   # 硬件参考
│   ├── robot-structure.md      # 整机结构
│   ├── sensors.md              # 传感器
│   └── joints.md               # 关节参数
├── sdk/                        # SDK 接口
│   ├── overview.md             # SDK 总览
│   ├── voice/                  # 语音
│   ├── skills/                 # 技能
│   ├── sensors/                # 传感器数据
│   └── head-display.md         # 头显协议
├── motion-control/             # 运控开发
│   ├── walking.md              # 下肢行走
│   ├── upper-body.md           # 上身关节
│   ├── whole-body.md           # 全身关节
│   └── rl-control.md           # 强化学习
├── api/                        # API 参考
│   └── ros2-messages.md        # ROS2 消息类型
└── changelog.md                # 更新日志
```

## 贡献指南

1. Fork 本仓库
2. 创建功能分支：`git checkout -b docs/add-xxx`
3. 编辑 Markdown 文件
4. 本地预览确认无误
5. 提交 PR，RTD 会自动构建 PR 预览

## 技术栈

- [MkDocs](https://www.mkdocs.org/) — 静态站点生成器
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) — 主题
- [Read the Docs](https://readthedocs.org/) — 托管平台
- [mike](https://github.com/jimporter/mike) — 多版本管理
