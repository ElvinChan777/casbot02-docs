# 关节状态数据

## 接口定义

| 属性 | 值 |
|---|---|
| **通讯方式** | ROS2 Topic |
| **Topic 名称** | `/joint_states` |
| **消息类型** | `sensor_msgs/msg/JointState` |
| **方向** | CASBOT02 → 开发者 |
| **包含** | 腿部、手臂、腰部、头部、灵巧手所有关节 |

## 消息结构

```python
# sensor_msgs/msg/JointState 核心字段

std_msgs/Header header              # 时间戳

string[] name                       # 关节名称列表
float64[] position                  # 关节位置 (rad)
float64[] velocity                  # 关节速度 (rad/s)
float64[] effort                    # 关节力矩 (N·m)
```

## 代码示例

参见 [快速上手](../../getting-started/quickstart.md) 中的完整示例。

## 命令行查看

```bash
# 查看所有关节状态
ros2 topic echo /joint_states

# 仅查看关节名称
ros2 topic echo /joint_states --field name

# 查看发布频率
ros2 topic hz /joint_states
```
