# 快速上手

5 分钟内跑通你的第一个 CASBOT02 二开程序。

## 目标

编写一个 Python 节点，订阅 CASBOT02 的关节状态并在终端打印。

## 步骤

### 1. 确认网络连通

```bash
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=<机器人 domain id>

# 应能看到 /joint_states 等 topic
ros2 topic list
```

### 2. 创建工作空间

```bash
mkdir -p ~/casbot_demo/src && cd ~/casbot_demo/src
ros2 pkg create --build-type ament_python casbot_demo --dependencies rclpy sensor_msgs
```

### 3. 编写订阅节点

创建 `casbot_demo/casbot_demo/joint_monitor.py`：

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState


class JointMonitor(Node):
    def __init__(self):
        super().__init__('joint_monitor')
        self.sub = self.create_subscription(
            JointState,
            '/joint_states',
            self.callback,
            10
        )
        self.get_logger().info('关节状态监听已启动')

    def callback(self, msg: JointState):
        for name, pos in zip(msg.name, msg.position):
            self.get_logger().info(f'{name}: {pos:.4f} rad')


def main():
    rclpy.init()
    node = JointMonitor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### 4. 构建运行

```bash
cd ~/casbot_demo
colcon build
source install/setup.bash
ros2 run casbot_demo joint_monitor
```

如果终端开始输出关节角度数据，恭喜你完成了第一个 CASBOT02 二开程序！

## 下一步

- [SDK 接口总览](../sdk/overview.md) — 了解所有可用接口
- [行走控制](../motion-control/walking.md) — 让机器人走路
- [预设技能](../sdk/skills/preset-skills.md) — 调用内置动作
