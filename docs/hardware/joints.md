# 关节参数

本页列出 CASBOT02 所有关节的名称、限位和描述。

## 头部（2 DOF）

| 编号 | 关节名称 | 限位（弧度） | 描述 |
|:---:|---|---|---|
| 1 | `head_yaw_joint` | [-1.5708, 1.5708] | 头部偏航 |
| 2 | `head_pitch_joint` | [-0.2618, 0.5236] | 头部俯仰 |

## 腰部（1 DOF）

| 编号 | 关节名称 | 限位（弧度） | 描述 |
|:---:|---|---|---|
| 1 | `waist_yaw_joint` | [-1.5708, 1.5708] | 腰部偏航 |

## 手臂（单臂 7 DOF）

| 编号 | 左臂关节 | 右臂关节 | 限位（弧度） | 描述 |
|:---:|---|---|---|---|
| 1 | `left_shoulder_pitch_joint` | `right_shoulder_pitch_joint` | [-3.1416, 1.0472] | 肩膀俯仰 |
| 2 | `left_shoulder_roll_joint` | `right_shoulder_roll_joint` | L:[-0.3491, 3.1416] / R:[-3.1416, 0.3491] | 肩膀滚转 |
| 3 | `left_shoulder_yaw_joint` | `right_shoulder_yaw_joint` | [-1.5708, 1.5708] | 肩膀偏航 |
| 4 | `left_elbow_pitch_joint` | `right_elbow_pitch_joint` | [-1.8675, 0] | 手肘俯仰 |
| 5 | `left_wrist_yaw_joint` | `right_wrist_yaw_joint` | [-1.5708, 1.5708] | 手腕偏航 |
| 6 | `left_wrist_roll_joint` | `right_wrist_roll_joint` | L:[-1.0472, 1.5708] / R:[-1.5708, 1.0472] | 手腕滚转（选装） |
| 7 | `left_wrist_pitch_joint` | `right_wrist_pitch_joint` | [-1.0472, 1.0472] | 手腕俯仰（选装） |

## 腿部（单腿 6 DOF）

| 编号 | 左腿关节 | 右腿关节 | 限位（弧度） | 描述 |
|:---:|---|---|---|---|
| 1 | `left_leg_pelvic_pitch_joint` | `right_leg_pelvic_pitch_joint` | [-1.9199, 1.5708] | 髋部旋转 |
| 2 | `left_leg_pelvic_roll_joint` | `right_leg_pelvic_roll_joint` | L:[-0.1745, 1.5708] / R:[-1.5708, 0.1745] | 髋部滚转 |
| 3 | `left_leg_pelvic_yaw_joint` | `right_leg_pelvic_yaw_joint` | [-1.5708, 1.5708] | 髋部偏航 |
| 4 | `left_leg_knee_pitch_joint` | `right_leg_knee_pitch_joint` | [0, 2.5307] | 膝盖俯仰 |
| 5 | `left_leg_ankle_pitch_joint` | `right_leg_ankle_pitch_joint` | [-0.8727, 0.5061] | 脚踝俯仰 |
| 6 | `left_leg_ankle_roll_joint` | `right_leg_ankle_roll_joint` | [-0.5061, 0.5061] | 脚踝滚转 |

!!! danger "安全警告"
    关节限位为硬件物理极限。实际控制时建议留出安全余量，避免运行到极限位置。

## 灵巧手（单手 6 主动 DOF）

| 编号 | 左手关节 | 右手关节 | 描述 |
|:---:|---|---|---|
| 1 | `left_thumb_metacarpal_joint` | `right_thumb_metacarpal_joint` | 拇指掌骨 |
| 2 | `left_thumb_proximal_joint` | `right_thumb_proximal_joint` | 拇指近端 |
| 3 | `left_index_proximal_joint` | `right_index_proximal_joint` | 食指近端 |
| 4 | `left_middle_proximal_joint` | `right_middle_proximal_joint` | 中指近端 |
| 5 | `left_ring_proximal_joint` | `right_ring_proximal_joint` | 无名指近端 |
| 6 | `left_pinky_proximal_joint` | `right_pinky_proximal_joint` | 小指近端 |

!!! note "被动关节"
    灵巧手的每个手指还有一个被动关节（distal joint），通过机械联动随主动关节运动，不单独控制。
