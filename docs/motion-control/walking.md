# 下肢行走控制

本页介绍 CASBOT02 下肢行走速度控制接口。

## 控制权切换

CASBOT02 的控制权需要通过手柄物理切换：

| 按键组合 | 模式 | 说明 |
|---|---|---|
| **RB + A** | 导航模式 | 可通过接口控制行走 |
| **RB + Y** | 遥控模式 | 手柄直接控制 |

!!! warning "前置条件"
    必须先通过手柄切换到**导航模式**，才能使用行走控制接口。

## 行走控制接口

| 属性 | 值 |
|---|---|
| **通讯方式** | ROS2 Topic |
| **Topic 名称** | `/navigation/cmd_vel` |
| **消息类型** | `geometry_msgs/msg/Twist` |
| **方向** | 开发者 → CASBOT02 |
| **频率** | 建议 10Hz 以上 |

### 速度参数

| 字段 | 含义 | 范围 |
|---|---|---|
| `linear.x` | 前后运动速度（前为正） | [-1.0, 1.0] m/s |
| `linear.y` | 左右平移速度（左为正） | [-1.0, 1.0] m/s |
| `angular.z` | 绕竖直轴旋转角速度（逆时针为正） | [-1.0, 1.0] rad/s |

!!! tip "速度限制"
    建议从小速度开始测试，逐步增加。最大速度取决于地面条件和机器人当前状态。

### 代码示例

=== "Python"

    ```python
    import rclpy
    from rclpy.node import Node
    from geometry_msgs.msg import Twist
    import time


    class WalkController(Node):
        """CASBOT02 行走控制示例节点"""

        def __init__(self):
            super().__init__('walk_controller')
            self.publisher_ = self.create_publisher(
                Twist,
                '/navigation/cmd_vel',
                10
            )
            self.get_logger().info('行走控制节点已启动')

        def walk_forward(self, speed: float = 0.3):
            """前进"""
            msg = Twist()
            msg.linear.x = speed
            self.publisher_.publish(msg)
            self.get_logger().info(f'前进 speed={speed}')

        def walk_backward(self, speed: float = 0.3):
            """后退"""
            msg = Twist()
            msg.linear.x = -speed
            self.publisher_.publish(msg)

        def strafe_left(self, speed: float = 0.2):
            """左移"""
            msg = Twist()
            msg.linear.y = speed
            self.publisher_.publish(msg)

        def rotate(self, angular_speed: float = 0.5):
            """原地旋转"""
            msg = Twist()
            msg.angular.z = angular_speed
            self.publisher_.publish(msg)

        def stop(self):
            """停止"""
            self.publisher_.publish(Twist())


    def main():
        rclpy.init()
        node = WalkController()

        # 前进 2 秒
        node.walk_forward(0.3)
        time.sleep(2.0)

        # 停止
        node.stop()

        node.destroy_node()
        rclpy.shutdown()


    if __name__ == '__main__':
        main()
    ```

=== "C++"

    ```cpp
    #include <rclcpp/rclcpp.hpp>
    #include <geometry_msgs/msg/twist.hpp>
    #include <chrono>

    using namespace std::chrono_literals;

    class WalkController : public rclcpp::Node {
    public:
        WalkController() : Node("walk_controller") {
            publisher_ = this->create_publisher<geometry_msgs::msg::Twist>(
                "/navigation/cmd_vel", 10);
            RCLCPP_INFO(get_logger(), "行走控制节点已启动");
        }

        void walkForward(double speed = 0.3) {
            auto msg = geometry_msgs::msg::Twist();
            msg.linear.x = speed;
            publisher_->publish(msg);
            RCLCPP_INFO(get_logger(), "前进 speed=%.2f", speed);
        }

        void walkBackward(double speed = 0.3) {
            auto msg = geometry_msgs::msg::Twist();
            msg.linear.x = -speed;
            publisher_->publish(msg);
        }

        void strafeLeft(double speed = 0.2) {
            auto msg = geometry_msgs::msg::Twist();
            msg.linear.y = speed;
            publisher_->publish(msg);
        }

        void rotate(double angularSpeed = 0.5) {
            auto msg = geometry_msgs::msg::Twist();
            msg.angular.z = angularSpeed;
            publisher_->publish(msg);
        }

        void stop() {
            publisher_->publish(geometry_msgs::msg::Twist());
        }

    private:
        rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;
    };

    int main(int argc, char** argv) {
        rclcpp::init(argc, argv);
        auto node = std::make_shared<WalkController>();

        // 前进 2 秒
        node->walkForward(0.3);
        rclcpp::sleep_for(2s);

        // 停止
        node->stop();

        rclcpp::shutdown();
        return 0;
    }
    ```

### 快速测试

使用命令行直接发送行走指令：

```bash
# 前进
ros2 topic pub --once /navigation/cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.3}}"

# 左移
ros2 topic pub --once /navigation/cmd_vel geometry_msgs/msg/Twist \
  "{linear: {y: 0.2}}"

# 原地旋转
ros2 topic pub --once /navigation/cmd_vel geometry_msgs/msg/Twist \
  "{angular: {z: 0.5}}"

# 停止
ros2 topic pub --once /navigation/cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.0, y: 0.0}, angular: {z: 0.0}}"
```
