# 五分钟上手

本页引导你从零运行第一个 CASBOT2 二开示例。

## 1. 克隆 SDK 仓库

```bash
git clone https://github.com/CasbotRobotics/casbot2-ros2-sdk.git
cd casbot2-ros2-sdk
```

## 2. 编译消息包

```bash
source /opt/ros/humble/setup.bash
colcon build --packages-select crb_ros_msg
source install/setup.bash
```

## 3. 运行 Python 示例

```bash
cd examples/python
colcon build --packages-select casbot2_py_demo
source install/setup.bash
ros2 run casbot2_py_demo control_demo
```

## 4. 运行 C++ 示例

```bash
cd examples/workflows/cpp/casbot_cpp_test
colcon build --packages-select casbot_cpp_test
source install/setup.bash
ros2 run casbot_cpp_test t01_get_state
```

## 5. 使用接口全覆盖工具

SDK 提供了一个命令行工具，可快速测试所有接口：

```bash
python3 examples/interfaces/python/all_interfaces_demo.py --help
```

示例：

```bash
# 查询机器人模式
python3 examples/interfaces/python/all_interfaces_demo.py get_robot_mode

# 发送行走指令（前进 2 秒）
python3 examples/interfaces/python/all_interfaces_demo.py pub_cmd_vel --vx 0.2 --wz 0.0 --seconds 2

# 执行挥手动作
python3 examples/interfaces/python/all_interfaces_demo.py basic_action_play --type wave_hand
```

## 下一步

- [接口总览](../guide/overview.md) — 了解所有可用接口
- [示例总览](../examples/demos/overview.md) — 查看更多示例
- [开机自检](../examples/scenarios/boot-check.md) — 实机调试前的检查流程
