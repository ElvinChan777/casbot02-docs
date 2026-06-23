# 接口全覆盖示例

本文档给出 CASBOT2 常用接口的"可执行示例入口"。
配套脚本：`python/all_interfaces_demo.py`

## 使用前准备

```bash
source /opt/ros/humble/setup.bash
source /workspace/prod_casbot02_basic/install/setup.bash 2>/dev/null || true
source /workspace/HLmotion/setup.bash 2>/dev/null || source /workspace/hl_motion/setup.bash 2>/dev/null || true
```

如果你在本仓库内开发，建议先编译自定义消息包：

```bash
colcon build --packages-select crb_ros_msg
source install/setup.bash
```

---

## 1. 模式与状态类 Service

### `get_robot_mode`

查询当前机器人模式。

```bash
python3 examples/interfaces/python/all_interfaces_demo.py get_robot_mode
```

### `/set_robot_mode`

切换机器人模式（`ZERO` / `STAND` / `WALK`）。

```bash
python3 examples/interfaces/python/all_interfaces_demo.py set_robot_mode --mode WALK
```

### `get_robot_state_srv_hl`

查询机器人运行状态。

```bash
python3 examples/interfaces/python/all_interfaces_demo.py get_robot_state
```

### `/motion/switch_nav_mode`

开关导航模式。

```bash
python3 examples/interfaces/python/all_interfaces_demo.py switch_nav_mode --enable true
```

### `/switch_teleoperation`

开关遥操作模式。

```bash
python3 examples/interfaces/python/all_interfaces_demo.py switch_teleoperation --enable true
```

### `/switch_autonomous`

开关自主模式。

```bash
python3 examples/interfaces/python/all_interfaces_demo.py switch_autonomous --enable true
```

### `/motion/upper_body_debug`

开关上半身调试模式。

```bash
python3 examples/interfaces/python/all_interfaces_demo.py upper_body_debug --enable true
```

### `/motion/whole_body_debug`

开关全身调试模式。

```bash
python3 examples/interfaces/python/all_interfaces_demo.py whole_body_debug --enable true
```

---

## 2. 控制类 Topic

### `/navigation/cmd_vel`

发布速度控制指令（平移 `vx` + 偏航 `wz`）。

```bash
python3 examples/interfaces/python/all_interfaces_demo.py pub_cmd_vel \
  --vx 0.2 --wz 0.0 --seconds 2
```

### `/upper_body_debug/joint_cmd`

发布上半身关节控制指令（`UpperJointData`）。

```bash
python3 examples/interfaces/python/all_interfaces_demo.py pub_upper_cmd \
  --names left_shoulder_pitch_joint,right_shoulder_pitch_joint \
  --positions 0.05,0.05 --vel-scale 0.05
```

### `/motion/joint_cmd`

发布全身关节控制指令（`JointStateData`）。

```bash
python3 examples/interfaces/python/all_interfaces_demo.py pub_whole_cmd \
  --names head_yaw_joint,head_pitch_joint \
  --positions 0.1,-0.05
```

---

## 3. 订阅类 Topic

### `/motion/joint_state`

订阅运动层关节状态。

```bash
python3 examples/interfaces/python/all_interfaces_demo.py sub_motion_joint_state --seconds 3
```

### `/joint_states`

订阅标准 `JointState`。

```bash
python3 examples/interfaces/python/all_interfaces_demo.py sub_joint_states --seconds 3
```

### `/joint_control`

订阅关节控制反馈。

```bash
python3 examples/interfaces/python/all_interfaces_demo.py sub_joint_control --seconds 3
```

### `/motion/status` + `/motion/robot_state`

订阅运动状态与机器人状态。

```bash
python3 examples/interfaces/python/all_interfaces_demo.py sub_status --seconds 3
```

### `/imu`

订阅 IMU 数据（也可使用 `/motion/imu`）。

```bash
python3 examples/interfaces/python/all_interfaces_demo.py sub_imu --topic /imu --seconds 3
```

---

## 4. 动作与应用接口

### `basic_action_play`

播放预设基础动作（`BasicActionPlay`）。

```bash
python3 examples/interfaces/python/all_interfaces_demo.py basic_action_play --type wave_hand
```

### `/voice_svr`

语音服务（`Voice` Service），支持 RTC 启动与问答。

```bash
python3 examples/interfaces/python/all_interfaces_demo.py voice_service --type rtc_start
python3 examples/interfaces/python/all_interfaces_demo.py voice_service --type question --content "你好"
```

### `/action_voice_play`

语音播放动作（`VoicePlay` Action）。

```bash
python3 examples/interfaces/python/all_interfaces_demo.py voice_play --wav test.wav
```

### `/casbot/event_service`

事件技能触发（`ActionEvent`）。

```bash
python3 examples/interfaces/python/all_interfaces_demo.py event_skill --action-type wave_hand
```
