# CASBOT2 二次开发文档

CASBOT2 人形机器人的 ROS 2 二次开发文档。本仓库基于 CasbotRobotics 官方 SDK 构建。

[:material-rocket-launch: 快速开始](getting-started/quickstart.md){ .md-button .md-button--primary }
[:material-api: 接口总览](guide/overview.md){ .md-button }
[:material-github: GitHub 仓库](https://github.com/CasbotRobotics/casbot2-ros2-sdk){ .md-button }

---

## 核心接口一览

| 类型 | 名称 | 接口类型 | 说明 |
|---|---|---|---|
| Service | get_robot_mode | crb_ros_msg/srv/GetRobotMode | 查询当前机器人模式 |
| Service | /set_robot_mode | crb_ros_msg/srv/SetRobotMode | 设置机器人模式 (ZERO/STAND/WALK) |
| Service | /motion/upper_body_debug | std_srvs/srv/SetBool | 上身调试模式开关 |
| Service | /motion/whole_body_debug | std_srvs/srv/SetBool | 全身调试模式开关 |
| Service | /motion/switch_nav_mode | std_srvs/srv/SetBool | 导航模式开关 |
| Service | /voice_svr | crb_ros_msg/srv/Voice | 语音对话 |
| Service | /casbot/event_service | crb_ros_msg/srv/ActionEvent | 技能触发 |
| Topic | /navigation/cmd_vel | geometry_msgs/msg/Twist | 行走速度控制 |
| Topic | /upper_body_debug/joint_cmd | crb_ros_msg/msg/UpperJointData | 上身关节控制 |
| Topic | /motion/joint_cmd | crb_ros_msg/msg/JointStateData | 全身关节控制 |
| Topic | /motion/joint_state | crb_ros_msg/msg/JointStateData | 全身关节状态反馈 |
| Topic | /joint_states | sensor_msgs/msg/JointState | 标准关节状态 |
| Action | /basic_action_play | crb_ros_msg/action/BasicActionPlay | 预设动作播放 |
| Action | /action_voice_play | crb_ros_msg/action/VoicePlay | 音频播放 |

---

## 安全提示

!!! danger "调试安全须知"
    - 首次联调请从**低速、小幅度**关节指令开始
    - 每次发控制命令前先**确认当前模式**
    - 调试模式需有**安全员在场**，确保急停可用

---

## 环境要求

| 项目 | 要求 |
|---|---|
| 操作系统 | Ubuntu 22.04 |
| ROS2 版本 | Humble Hawksbill |
| 依赖包 | crb_ros_msg (仓库内置) |
| SDK 源码 | [casbot2-ros2-sdk](https://github.com/CasbotRobotics/casbot2-ros2-sdk) |
