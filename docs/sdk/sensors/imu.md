# IMU 数据

## 接口定义

| 属性 | 值 |
|---|---|
| **通讯方式** | ROS2 Topic |
| **Topic 名称** | `/imu` |
| **消息类型** | `sensor_msgs/msg/Imu` |
| **方向** | CASBOT02 → 开发者 |
| **用途** | 姿态估算、运动状态分析（如平衡控制） |

## 消息结构

```python
# sensor_msgs/msg/Imu 核心字段

std_msgs/Header header          # 时间戳和坐标系

geometry_msgs/Quaternion orientation         # 四元数姿态
float64[9] orientation_covariance            # 姿态协方差

geometry_msgs/Vector3 angular_velocity       # 角速度 (rad/s)
float64[9] angular_velocity_covariance       # 角速度协方差

geometry_msgs/Vector3 linear_acceleration    # 线加速度 (m/s²)
float64[9] linear_acceleration_covariance    # 加速度协方差
```

## 代码示例

=== "Python"

    ```python
    import rclpy
    from rclpy.node import Node
    from sensor_msgs.msg import Imu
    import math


    class ImuMonitor(Node):
        def __init__(self):
            super().__init__('imu_monitor')
            self.sub = self.create_subscription(
                Imu, '/imu', self.callback, 10)

        def callback(self, msg: Imu):
            q = msg.orientation
            # 四元数转欧拉角（简化）
            pitch = math.asin(2.0 * (q.w * q.y - q.z * q.x))
            roll = math.atan2(
                2.0 * (q.w * q.x + q.y * q.z),
                1.0 - 2.0 * (q.x * q.x + q.y * q.y))
            yaw = math.atan2(
                2.0 * (q.w * q.z + q.x * q.y),
                1.0 - 2.0 * (q.y * q.y + q.z * q.z))

            self.get_logger().info(
                f'姿态 roll={math.degrees(roll):.1f}° '
                f'pitch={math.degrees(pitch):.1f}° '
                f'yaw={math.degrees(yaw):.1f}°'
            )
    ```

=== "C++"

    ```cpp
    #include <rclcpp/rclcpp.hpp>
    #include <sensor_msgs/msg/imu.hpp>
    #include <cmath>

    class ImuMonitor : public rclcpp::Node {
    public:
        ImuMonitor() : Node("imu_monitor") {
            sub_ = create_subscription<sensor_msgs::msg::Imu>(
                "/imu", 10,
                [this](const sensor_msgs::msg::Imu::SharedPtr msg) {
                    auto q = msg->orientation;
                    double pitch = asin(2.0 * (q.w * q.y - q.z * q.x));
                    RCLCPP_INFO(get_logger(), "pitch=%.1f°",
                                pitch * 180.0 / M_PI);
                });
        }
    private:
        rclcpp::Subscription<sensor_msgs::msg::Imu>::SharedPtr sub_;
    };
    ```

## 命令行查看

```bash
ros2 topic echo /imu
ros2 topic hz /imu    # 查看发布频率
```
