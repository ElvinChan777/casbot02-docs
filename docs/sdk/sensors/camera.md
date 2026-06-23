# 相机数据

CASBOT02 配备多个相机，分布在头部、胸口和腹部。

## 相机列表

| 相机名称 | 位置 | 类型 |
|---|---|---|
| `camera_head` | 头部 | RGBD |
| `camera_chest` | 胸口 | RGBD |
| `camera_belly` | 腹部 | RGBD |
| `camera_stereo` | 头部 | 彩色双目 |
| `camera_fisheyes_front` | 前方 | 鱼眼 |
| `camera_fisheyes_back` | 后方 | 鱼眼 |

## Topic 接口

### 彩色图

| 属性 | 值 |
|---|---|
| Topic | `/camera_xxx/color/image_raw` |
| 压缩图 | `/camera_xxx/color/image_raw/compressed` |
| Camera Info | `/camera_xxx/color/camera_info`（仅 RGBD） |
| 消息类型 | `sensor_msgs/msg/Image` / `sensor_msgs/msg/CompressedImage` |
| 分辨率 | 1280×720 |

### 彩色图（小图）

| 属性 | 值 |
|---|---|
| Topic | `/camera_xxx/color/image_raw_mini` |
| 压缩图 | `/camera_xxx/color/image_raw_mini/compressed` |
| 分辨率 | 640×320 |

### 深度图（仅 RGBD 相机）

| 属性 | 值 |
|---|---|
| Topic | `/camera_xxx/depth/image_raw` |
| 压缩图 | `/camera_xxx/depth/image_raw/compressed` |
| Camera Info | `/camera_xxx/depth/camera_info` |
| 分辨率 | 1280×720 |

### 深度图小图（仅 RGBD 相机）

| 属性 | 值 |
|---|---|
| Topic | `/camera_xxx/depth/image_raw_mini` |
| 压缩图 | `/camera_xxx/depth/image_raw_mini/compressed` |
| 分辨率 | 640×320 |

## 代码示例

=== "Python"

    ```python
    import rclpy
    from rclpy.node import Node
    from sensor_msgs.msg import Image


    class CameraSubscriber(Node):
        def __init__(self):
            super().__init__('camera_subscriber')
            self.sub = self.create_subscription(
                Image,
                '/camera_head/color/image_raw',
                self.callback,
                10
            )

        def callback(self, msg: Image):
            self.get_logger().info(
                f'收到图像: {msg.width}x{msg.height}, '
                f'encoding={msg.encoding}'
            )
    ```

=== "C++"

    ```cpp
    #include <rclcpp/rclcpp.hpp>
    #include <sensor_msgs/msg/image.hpp>

    class CameraSubscriber : public rclcpp::Node {
    public:
        CameraSubscriber() : Node("camera_subscriber") {
            sub_ = create_subscription<sensor_msgs::msg::Image>(
                "/camera_head/color/image_raw", 10,
                [this](const sensor_msgs::msg::Image::SharedPtr msg) {
                    RCLCPP_INFO(get_logger(), "收到图像: %dx%d, encoding=%s",
                                msg->width, msg->height, msg->encoding.c_str());
                });
        }
    private:
        rclcpp::Subscription<sensor_msgs::msg::Image>::SharedPtr sub_;
    };
    ```

## 命令行查看

```bash
# 查看所有相机 topic
ros2 topic list | grep camera

# 查看头部彩色图
ros2 topic echo /camera_head/color/image_raw --no-arr

# 使用 rqt_image_view 查看图像
ros2 run rqt_image_view rqt_image_view /camera_head/color/image_raw
```
