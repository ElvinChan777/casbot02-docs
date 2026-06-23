# 上身关节控制

## 调试模式

上身关节控制前需先申请上身调试模式。

| 属性 | 值 |
|---|---|
| **通讯方式** | ROS2 Service |
| **Service 名称** | `/motion/upper_body_debug` |
| **Service 类型** | `std_srvs/srv/SetBool` |

```bash
# 申请进入上身调试模式
ros2 service call /motion/upper_body_debug std_srvs/srv/SetBool "{data: true}"

# 退出上身调试模式
ros2 service call /motion/upper_body_debug std_srvs/srv/SetBool "{data: false}"
```

!!! danger "调试模式风险"
    进入调试模式后，机器人对上身关节的自主控制将被接管。请确保周围环境安全。

## 上身关节列表

| 部位 | 关节 |
|---|---|
| 头 | `head_yaw_joint`, `head_pitch_joint` |
| 腰 | `waist_yaw_joint` |
| 左臂 | `left_shoulder_pitch_joint`, `left_shoulder_roll_joint`, `left_shoulder_yaw_joint`, `left_elbow_pitch_joint`, `left_wrist_yaw_joint`, `left_wrist_pitch_joint`, `left_wrist_roll_joint` |
| 右臂 | `right_shoulder_pitch_joint`, `right_shoulder_roll_joint`, `right_shoulder_yaw_joint`, `right_elbow_pitch_joint`, `right_wrist_yaw_joint`, `right_wrist_pitch_joint`, `right_wrist_roll_joint` |
| 左手 | `left_thumb_metacarpal_joint`, `left_thumb_proximal_joint`, `left_index_proximal_joint`, `left_middle_proximal_joint`, `left_ring_proximal_joint`, `left_pinky_proximal_joint` |
| 右手 | `right_thumb_metacarpal_joint`, `right_thumb_proximal_joint`, `right_index_proximal_joint`, `right_middle_proximal_joint`, `right_ring_proximal_joint`, `right_pinky_proximal_joint` |

## 控制接口

| 属性 | 值 |
|---|---|
| **通讯方式** | ROS2 Topic |
| **Topic 名称** | `/upper_body_debug/joint_cmd` |
| **消息类型** | `crb_ros_msg/msg/UpperJointData` |

### 消息定义

```cpp
// UpperJointData.msg

std_msgs/Header header

# 执行时间, 单位秒
float32 time_ref

# 速度比例 [0.0, 1.0]
float32 vel_scale

sensor_msgs/JointState joint
```

### 代码示例

=== "Python"

    ```python
    import rclpy
    from rclpy.node import Node
    from crb_ros_msg.msg import UpperJointData
    from sensor_msgs.msg import JointState
    from builtin_interfaces.msg import Duration


    class UpperBodyController(Node):
        def __init__(self):
            super().__init__('upper_body_controller')
            self.pub = self.create_publisher(
                UpperJointData,
                '/upper_body_debug/joint_cmd',
                10
            )

        def move_joint(self, joint_name: str, position: float,
                       exec_time: float = 1.0):
            """控制单个关节运动到指定位置"""
            msg = UpperJointData()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.time_ref = exec_time
            msg.vel_scale = 0.5

            msg.joint.name = [joint_name]
            msg.joint.position = [position]

            self.pub.publish(msg)
    ```

=== "C++"

    ```cpp
    #include <rclcpp/rclcpp.hpp>
    #include <crb_ros_msg/msg/upper_joint_data.hpp>
    #include <sensor_msgs/msg/joint_state.hpp>

    class UpperBodyController : public rclcpp::Node {
    public:
        UpperBodyController() : Node("upper_body_controller") {
            pub_ = create_publisher<crb_ros_msg::msg::UpperJointData>(
                "/upper_body_debug/joint_cmd", 10);
        }

        void moveJoint(const std::string& name, double position,
                       float execTime = 1.0f) {
            auto msg = crb_ros_msg::msg::UpperJointData();
            msg.header.stamp = now();
            msg.time_ref = execTime;
            msg.vel_scale = 0.5f;

            msg.joint.name = {name};
            msg.joint.position = {position};

            pub_->publish(msg);
        }

    private:
        rclcpp::Publisher<crb_ros_msg::msg::UpperJointData>::SharedPtr pub_;
    };
    ```

!!! tip "多帧控制"
    可以单帧、离散多帧、连续帧发送 topic，对上身关节进行关节空间的位置控制。连续帧控制时建议保持稳定的发布频率。
