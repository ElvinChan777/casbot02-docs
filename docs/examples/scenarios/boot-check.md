# 开机自检

## 目标

确认机器人或仿真进程启动后，ROS 2 通道、关键服务和关键话题全部可用。

## 步骤

### 1. Source 环境

```bash
source /opt/ros/humble/setup.bash
source /workspace/prod_casbot02_basic/install/setup.bash 2>/dev/null || true
source /workspace/HLmotion/setup.bash 2>/dev/null || source /workspace/hl_motion/setup.bash 2>/dev/null || true
```

### 2. 基础诊断

```bash
ros2 doctor --report
ros2 topic list
ros2 service list
```

### 3. 核心接口检查

!!! warning "安全提示"

    在执行核心接口检查前，请确保机器人处于安全位置，或仿真环境已正确启动。
    调用运动相关服务可能触发关节动作，请远离机械臂运动范围。

```bash
ros2 service call get_robot_mode crb_ros_msg/srv/GetRobotMode "{}"
ros2 service call get_robot_state_srv_hl crb_ros_msg/srv/GetRobotState "{start: true}"
ros2 topic info /joint_states
ros2 topic info /navigation/cmd_vel
```

### 4. 建议执行 workflow 自检脚本

- Python：`../workflows/python/casbot_py_test/t01_get_state.py`
- C++：`../workflows/cpp/casbot_cpp_test/src/t01_get_state.cpp`（先编译）

!!! tip "提示"

    自检脚本可快速验证基本通信链路是否畅通，建议在每次启动后优先执行。

## 判定标准

| 检查项 | 预期结果 |
|--------|----------|
| 核心服务调用 | 返回正常 |
| `/joint_states` | 有持续数据输出 |
| 模式切换服务 | 可用且返回成功 |

!!! note "说明"

    如果以上任一项未通过，请参考故障排查章节或检查日志输出，确认相关节点是否正常启动。
