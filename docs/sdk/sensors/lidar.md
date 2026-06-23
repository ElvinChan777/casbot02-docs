# 激光雷达数据

## 接口定义

| 属性 | 值 |
|---|---|
| **通讯方式** | ROS2 Topic |
| **Topic 名称** | `/rslidar_points` |
| **消息类型** | `sensor_msgs/msg/PointCloud2` |
| **雷达型号** | 速腾聚创 Airy |
| **连接位置** | 导航控制模块 |

!!! note "网络拓扑"
    激光雷达连接在导航控制模块上。由于导航控制模块与 Orin 通过交换机在同一局域网，二开程序也可直接访问雷达数据。

## 代码示例

=== "Python"

    ```python
    import rclpy
    from rclpy.node import Node
    from sensor_msgs.msg import PointCloud2


    class LidarSubscriber(Node):
        def __init__(self):
            super().__init__('lidar_subscriber')
            self.sub = self.create_subscription(
                PointCloud2,
                '/rslidar_points',
                self.callback,
                10
            )

        def callback(self, msg: PointCloud2):
            self.get_logger().info(
                f'点云: {msg.width}x{msg.height}, '
                f'point_step={msg.point_step}'
            )
    ```

=== "C++"

    ```cpp
    #include <rclcpp/rclcpp.hpp>
    #include <sensor_msgs/msg/point_cloud2.hpp>

    class LidarSubscriber : public rclcpp::Node {
    public:
        LidarSubscriber() : Node("lidar_subscriber") {
            sub_ = create_subscription<sensor_msgs::msg::PointCloud2>(
                "/rslidar_points", 10,
                [this](const sensor_msgs::msg::PointCloud2::SharedPtr msg) {
                    RCLCPP_INFO(get_logger(), "点云: %dx%d",
                                msg->width, msg->height);
                });
        }
    private:
        rclcpp::Subscription<sensor_msgs::msg::PointCloud2>::SharedPtr sub_;
    };
    ```

## 自行安装驱动

如需将激光雷达直接连接到 Orin，可参照速腾官方 SDK 安装驱动：

GitHub 仓库：[https://github.com/RoboSense-LiDAR/rslidar_sdk](https://github.com/RoboSense-LiDAR/rslidar_sdk)

<!-- TODO: 补充驱动安装步骤 -->
