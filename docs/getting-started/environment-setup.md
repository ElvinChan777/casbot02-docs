# 环境搭建

本页介绍 CASBOT02 二次开发所需的环境配置。

## 前置要求

| 项目 | 要求 |
|---|---|
| 操作系统 | Ubuntu 22.04 |
| ROS2 版本 | Humble Hawksbill |
| 编程语言 | Python 3.10+ 或 C++17 |
| 网络 | 与 CASBOT02 Orin 主控在同一局域网 |

## ROS2 Humble 安装

如果您尚未安装 ROS2 Humble，请参考官方文档：

```bash
# 设置源
sudo apt update && sudo apt install -y software-properties-common
sudo add-apt-repository universe

# 添加 ROS2 GPG key
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
  -o /usr/share/keyrings/ros-archive-keyring.gpg

# 添加 ROS2 仓库
echo "deb [arch=$(dpkg --print-architecture) \
  signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
  http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | \
  sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# 安装 ROS2 Humble
sudo apt update && sudo apt upgrade
sudo apt install ros-humble-desktop
```

## 依赖包安装

CASBOT02 的自定义 ROS2 消息包 `crb_ros_msg` 需要预先安装：

```bash
# TODO: 补充 crb_ros_msg 的安装方式
# 方式一：从 deb 包安装
# sudo apt install ros-humble-crb-ros-msg

# 方式二：从源码编译
# mkdir -p ~/casbot_ws/src && cd ~/casbot_ws/src
# git clone https://github.com/YOUR_ORG/crb_ros_msg.git
# cd .. && colcon build --packages-select crb_ros_msg
# source install/setup.bash
```

## 网络配置

CASBOT02 的 Orin 主控与开发机需在同一局域网。确认 ROS2 DDS 通信正常：

```bash
# 在开发机上
export ROS_DOMAIN_ID=<与机器人一致的 domain id>

# 验证通信
ros2 topic list
```

!!! tip "ROS_DOMAIN_ID"
    确保开发机与 CASBOT02 使用相同的 `ROS_DOMAIN_ID`，否则无法发现彼此的节点。

## 验证安装

```bash
# 检查 ROS2 环境
source /opt/ros/humble/setup.bash
ros2 --help

# 检查自定义消息
ros2 interface show crb_ros_msg/srv/Voice
ros2 interface show crb_ros_msg/srv/ActionEvent
```
