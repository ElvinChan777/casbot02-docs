# CASBOT02 ROS2 消息类型参考

CASBOT02 的所有自定义消息类型定义在 `crb_ros_msg` 包中。

## 自定义消息

| 类型 | 完整路径 | 用途 |
|---|---|---|
| `UpperJointData` | `crb_ros_msg/msg/UpperJointData` | 上身关节控制 |

## 自定义服务

| 类型 | 完整路径 | 用途 |
|---|---|---|
| `Voice` | `crb_ros_msg/srv/Voice` | 语音对话 |
| `ActionEvent` | `crb_ros_msg/srv/ActionEvent` | 技能执行 |

## 自定义动作

| 类型 | 完整路径 | 用途 |
|---|---|---|
| `VoicePlay` | `crb_ros_msg/action/VoicePlay` | 音频播放 |

## 使用的消息类型（ROS2 标准）

| 类型 | 用途 | 相关页面 |
|---|---|---|
| `geometry_msgs/msg/Twist` | 行走速度控制 | [下肢行走](../motion-control/walking.md) |
| `sensor_msgs/msg/JointState` | 关节状态 | [关节状态](../sdk/sensors/joint-states.md) |
| `sensor_msgs/msg/Image` | 相机图像 | [相机数据](../sdk/sensors/camera.md) |
| `sensor_msgs/msg/Imu` | IMU 数据 | [IMU](../sdk/sensors/imu.md) |
| `sensor_msgs/msg/PointCloud2` | 点云数据 | [激光雷达](../sdk/sensors/lidar.md) |
| `std_srvs/srv/SetBool` | 调试模式开关 | [上身关节](../motion-control/upper-body.md) |
| `std_msgs/msg/String` | 头显控制 | [头显协议](../sdk/head-display.md) |

<!-- TODO: 自动生成 crb_ros_msg 的完整接口定义 -->
