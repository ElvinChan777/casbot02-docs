# URDF 模型

CASBOT02 的 URDF（Unified Robot Description Format）模型用于描述机器人的物理结构，是进行运动学计算、碰撞检测和仿真可视化的基础。

!!! warning "获取方式"
    URDF 模型文件需要**联系销售获取**。如有需要请联系您的销售代表。

## 用途

| 场景 | 说明 |
|---|---|
| **RViz 可视化** | 在 RViz 中查看机器人模型和关节状态 |
| **运动学计算** | 使用 KDL / Pinocchio 进行正逆运动学求解 |
| **仿真** | 在 Gazebo / Isaac Sim 中搭建仿真环境 |
| **碰撞检测** | 基于 URDF 中的几何信息进行碰撞检测 |
| **运动规划** | 配合 MoveIt2 进行路径规划 |

## 基本使用

```bash
# 在 RViz 中查看 URDF
ros2 launch urdf_tutorial display.launch.py model:=casbot02.urdf
```

<!-- TODO: 补充更多 URDF 使用示例和注意事项 -->
