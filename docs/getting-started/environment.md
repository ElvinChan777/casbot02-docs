# 环境准备

## 系统要求

| 项目 | 要求 |
|---|---|
| 操作系统 | Ubuntu 22.04 |
| ROS2 版本 | Humble Hawksbill |
| 编程语言 | Python 3.10+ 或 C++17 |

## ROS2 环境初始化

每次打开新终端，需执行以下初始化：

```bash
source /opt/ros/humble/setup.bash
source /workspace/prod_casbot02_basic/install/setup.bash 2>/dev/null || true
source /workspace/HLmotion/setup.bash 2>/dev/null || source /workspace/hl_motion/setup.bash 2>/dev/null || true
```

!!! tip "建议"
    将上述命令添加到 `~/.bashrc` 中，避免每次手动执行。

## 编译自定义消息包

SDK 仓库已内置 `crb_ros_msg` 消息包，编译即可使用：

```bash
cd casbot2-ros2-sdk
source /opt/ros/humble/setup.bash
colcon build --packages-select crb_ros_msg
source install/setup.bash
```

验证安装：

```bash
ros2 interface list | grep crb_ros_msg
ros2 interface show crb_ros_msg/msg/UpperJointData
ros2 interface show crb_ros_msg/srv/GetRobotMode
```

## 基础检查

```bash
ros2 doctor --report
ros2 topic list
ros2 service list | grep -E "motion|robot_mode|robot_state"
```
