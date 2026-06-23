# CASBOT02 二次开发文档

CASBOT02 人形机器人的 ROS2 二次开发在线文档。

**文档站点**：https://casbot02.readthedocs.io

## 内容概览

| 板块 | 说明 |
|---|---|
| [快速开始](docs/getting-started/) | 环境搭建、URDF 模型、5 分钟上手示例 |
| [硬件参考](docs/hardware/) | 整机结构、传感器感知范围、关节参数 |
| [SDK 接口](docs/sdk/) | 语音对话、预设技能、传感器数据、头显协议 |
| [运控开发](docs/motion-control/) | 行走控制、上身/全身关节控制、强化学习 |
| [API 参考](docs/api/) | ROS2 自定义消息类型速查 |

## 依赖包

CASBOT02 的 ROS2 自定义消息/服务/动作类型定义在 `crb_ros_msg` 包中。

## 贡献文档

```bash
# 安装依赖
pip install -r requirements.txt

# 本地预览（http://127.0.0.1:8000）
mkdocs serve

# 编辑 docs/ 下的 Markdown 文件后提交 PR
git checkout -b docs/your-topic
# 编辑...
git push origin docs/your-topic
```

PR 提交后 RTD 会自动构建预览，确认无误后合并到 main 即可上线。
