# 传感器与数据话题

本节汇总 CASBOT2 所有传感器反馈类 Topic，包括关节状态、IMU、运动状态监控以及手柄输入。所有话题方向均为 **机器人 -> 开发者**（仅订阅即可获取数据）。

---

## 话题总览

| 话题 | 消息类型 | 说明 |
|------|---------|------|
| `/joint_states` | `sensor_msgs/JointState` | ROS 2 标准关节状态 |
| `/motion/joint_state` | `crb_ros_msg/JointStateData` | 运控自定义关节状态（含增益信息） |
| `/joint_control` | `sensor_msgs/JointState` | 关节控制指令反馈 |
| `/imu` | `sensor_msgs/Imu` | IMU 惯性测量数据 |
| `/motion/status` | `std_msgs/String` | 运动控制器实时状态（JSON） |
| `/motion/robot_state` | `std_msgs/String` | 机器人综合状态（JSON） |
| `joystick_events` | `crb_ros_msg/JoystickCmdReport` | 手柄/遥控器输入事件 |

---

## /joint_states -- 标准关节状态

该话题以 ROS 2 标准 `sensor_msgs/JointState` 格式发布所有关节的当前位置、速度和力矩。可直接用于 RViz 等通用可视化工具。

**字段说明**

| 字段 | 类型 | 说明 |
|------|------|------|
| `header` | `std_msgs/Header` | 时间戳与坐标系 |
| `name` | `string[]` | 关节名称列表 |
| `position` | `float64[]` | 关节位置（弧度） |
| `velocity` | `float64[]` | 关节速度（rad/s） |
| `effort` | `float64[]` | 关节力矩（N*m） |

=== "Python"

    ```python
    import rclpy
    from rclpy.node import Node
    from sensor_msgs.msg import JointState


    class JointStatesSubscriber(Node):
        def __init__(self):
            super().__init__('joint_states_subscriber')
            self.create_subscription(
                JointState, '/joint_states', self.callback, 10)

        def callback(self, msg: JointState):
            for name, pos, vel, eff in zip(
                msg.name, msg.position, msg.velocity, msg.effort
            ):
                self.get_logger().info(
                    f'{name}: pos={pos:.3f} vel={vel:.3f} eff={eff:.3f}'
                )


    def main():
        rclpy.init()
        node = JointStatesSubscriber()
        rclpy.spin(node)
        node.destroy_node()
        rclpy.shutdown()


    if __name__ == '__main__':
        main()
    ```

=== "C++"

    ```cpp
    #include <rclcpp/rclcpp.hpp>
    #include <sensor_msgs/msg/joint_state.hpp>

    class JointStatesSubscriber : public rclcpp::Node
    {
    public:
      JointStatesSubscriber()
      : Node("joint_states_subscriber")
      {
        sub_ = create_subscription<sensor_msgs::msg::JointState>(
          "/joint_states", 10,
          [this](const sensor_msgs::msg::JointState::SharedPtr msg) {
            for (size_t i = 0; i < msg->name.size(); ++i) {
              RCLCPP_INFO(get_logger(), "%s: pos=%.3f vel=%.3f eff=%.3f",
                          msg->name[i].c_str(),
                          msg->position[i], msg->velocity[i], msg->effort[i]);
            }
          });
      }

    private:
      rclcpp::Subscription<sensor_msgs::msg::JointState>::SharedPtr sub_;
    };

    int main(int argc, char ** argv)
    {
      rclcpp::init(argc, argv);
      rclcpp::spin(std::make_shared<JointStatesSubscriber>());
      rclcpp::shutdown();
      return 0;
    }
    ```

---

## /motion/joint_state -- 运控关节状态

CASBOT2 运动控制器以自定义格式 `crb_ros_msg/JointStateData` 发布关节状态。相比标准 `JointState`，该消息额外包含增益参数（kp/kd），适合需要同步监控增益配置的场景。

**JointStateData 字段**

| 字段 | 类型 | 说明 |
|------|------|------|
| `names` | `string[]` | 关节名称列表 |
| `positions` | `float64[]` | 关节位置（弧度） |
| `velocities` | `float64[]` | 关节速度（rad/s） |
| `use_default_kp_kd` | `bool` | 当前是否使用默认增益 |
| `kp` | `float64[]` | 比例增益 |
| `kd` | `float64[]` | 微分增益 |

!!! tip "双通道观测"
    建议同时订阅 `/joint_states` 和 `/motion/joint_state` 进行交叉验证。前者兼容通用工具，后者提供更完整的运控信息。详见[运动控制 - 状态反馈](motion-control.md#state-feedback)。

=== "Python"

    ```python
    import rclpy
    from rclpy.node import Node
    from crb_ros_msg.msg import JointStateData


    class MotionJointStateSubscriber(Node):
        def __init__(self):
            super().__init__('motion_joint_state_subscriber')
            self.create_subscription(
                JointStateData, '/motion/joint_state', self.callback, 10)

        def callback(self, msg: JointStateData):
            for i, name in enumerate(msg.names):
                self.get_logger().info(
                    f'{name}: pos={msg.positions[i]:.3f}'
                )
            self.get_logger().info(
                f'使用默认增益: {msg.use_default_kp_kd}'
            )


    def main():
        rclpy.init()
        node = MotionJointStateSubscriber()
        rclpy.spin(node)
        node.destroy_node()
        rclpy.shutdown()


    if __name__ == '__main__':
        main()
    ```

=== "C++"

    ```cpp
    #include <rclcpp/rclcpp.hpp>
    #include <crb_ros_msg/msg/joint_state_data.hpp>

    class MotionJointStateSubscriber : public rclcpp::Node
    {
    public:
      MotionJointStateSubscriber()
      : Node("motion_joint_state_subscriber")
      {
        sub_ = create_subscription<crb_ros_msg::msg::JointStateData>(
          "/motion/joint_state", 10,
          [this](const crb_ros_msg::msg::JointStateData::SharedPtr msg) {
            for (size_t i = 0; i < msg->names.size(); ++i) {
              RCLCPP_INFO(get_logger(), "%s: pos=%.3f",
                          msg->names[i].c_str(), msg->positions[i]);
            }
            RCLCPP_INFO(get_logger(), "使用默认增益: %s",
                        msg->use_default_kp_kd ? "true" : "false");
          });
      }

    private:
      rclcpp::Subscription<crb_ros_msg::msg::JointStateData>::SharedPtr sub_;
    };

    int main(int argc, char ** argv)
    {
      rclcpp::init(argc, argv);
      rclcpp::spin(std::make_shared<MotionJointStateSubscriber>());
      rclcpp::shutdown();
      return 0;
    }
    ```

---

## /joint_control -- 关节控制反馈

该话题以标准 `sensor_msgs/JointState` 格式反馈运控系统实际下发的关节控制指令，可用于对比控制指令与关节实际响应之间的差异。

=== "Python"

    ```python
    import rclpy
    from rclpy.node import Node
    from sensor_msgs.msg import JointState


    class JointControlSubscriber(Node):
        def __init__(self):
            super().__init__('joint_control_subscriber')
            self.create_subscription(
                JointState, '/joint_control', self.callback, 10)

        def callback(self, msg: JointState):
            for name, pos in zip(msg.name, msg.position):
                self.get_logger().info(
                    f'[control] {name}: {pos:.3f} rad'
                )


    def main():
        rclpy.init()
        node = JointControlSubscriber()
        rclpy.spin(node)
        node.destroy_node()
        rclpy.shutdown()


    if __name__ == '__main__':
        main()
    ```

=== "C++"

    ```cpp
    #include <rclcpp/rclcpp.hpp>
    #include <sensor_msgs/msg/joint_state.hpp>

    class JointControlSubscriber : public rclcpp::Node
    {
    public:
      JointControlSubscriber()
      : Node("joint_control_subscriber")
      {
        sub_ = create_subscription<sensor_msgs::msg::JointState>(
          "/joint_control", 10,
          [this](const sensor_msgs::msg::JointState::SharedPtr msg) {
            for (size_t i = 0; i < msg->name.size(); ++i) {
              RCLCPP_INFO(get_logger(), "[control] %s: %.3f rad",
                          msg->name[i].c_str(), msg->position[i]);
            }
          });
      }

    private:
      rclcpp::Subscription<sensor_msgs::msg::JointState>::SharedPtr sub_;
    };

    int main(int argc, char ** argv)
    {
      rclcpp::init(argc, argv);
      rclcpp::spin(std::make_shared<JointControlSubscriber>());
      rclcpp::shutdown();
      return 0;
    }
    ```

---

## /imu -- IMU 数据

以标准 `sensor_msgs/Imu` 格式发布惯性测量单元数据，包含姿态四元数、角速度和线加速度。

**字段说明**

| 字段 | 类型 | 说明 |
|------|------|------|
| `header` | `std_msgs/Header` | 时间戳与坐标系 |
| `orientation` | `Quaternion` | 姿态四元数 (x, y, z, w) |
| `angular_velocity` | `Vector3` | 角速度 (rad/s) |
| `linear_acceleration` | `Vector3` | 线加速度 (m/s^2) |

=== "Python"

    ```python
    import rclpy
    from rclpy.node import Node
    from sensor_msgs.msg import Imu


    class ImuSubscriber(Node):
        def __init__(self):
            super().__init__('imu_subscriber')
            self.create_subscription(Imu, '/imu', self.callback, 10)

        def callback(self, msg: Imu):
            q = msg.orientation
            self.get_logger().info(
                f'姿态四元数: x={q.x:.3f} y={q.y:.3f} z={q.z:.3f} w={q.w:.3f}'
            )
            av = msg.angular_velocity
            self.get_logger().info(
                f'角速度: x={av.x:.3f} y={av.y:.3f} z={av.z:.3f} rad/s'
            )
            la = msg.linear_acceleration
            self.get_logger().info(
                f'线加速度: x={la.x:.3f} y={la.y:.3f} z={la.z:.3f} m/s^2'
            )


    def main():
        rclpy.init()
        node = ImuSubscriber()
        rclpy.spin(node)
        node.destroy_node()
        rclpy.shutdown()


    if __name__ == '__main__':
        main()
    ```

=== "C++"

    ```cpp
    #include <rclcpp/rclcpp.hpp>
    #include <sensor_msgs/msg/imu.hpp>

    class ImuSubscriber : public rclcpp::Node
    {
    public:
      ImuSubscriber()
      : Node("imu_subscriber")
      {
        sub_ = create_subscription<sensor_msgs::msg::Imu>(
          "/imu", 10,
          [this](const sensor_msgs::msg::Imu::SharedPtr msg) {
            auto & q = msg->orientation;
            RCLCPP_INFO(get_logger(),
                        "姿态: x=%.3f y=%.3f z=%.3f w=%.3f",
                        q.x, q.y, q.z, q.w);
            auto & av = msg->angular_velocity;
            RCLCPP_INFO(get_logger(),
                        "角速度: x=%.3f y=%.3f z=%.3f rad/s",
                        av.x, av.y, av.z);
            auto & la = msg->linear_acceleration;
            RCLCPP_INFO(get_logger(),
                        "线加速度: x=%.3f y=%.3f z=%.3f m/s^2",
                        la.x, la.y, la.z);
          });
      }

    private:
      rclcpp::Subscription<sensor_msgs::msg::Imu>::SharedPtr sub_;
    };

    int main(int argc, char ** argv)
    {
      rclcpp::init(argc, argv);
      rclcpp::spin(std::make_shared<ImuSubscriber>());
      rclcpp::shutdown();
      return 0;
    }
    ```

---

## /motion/status 与 /motion/robot_state -- 状态监控

两个话题均以 `std_msgs/String` 发布 JSON 字符串，分别提供运动控制器和整机的实时状态信息。

| 话题 | 说明 |
|------|------|
| `/motion/status` | 运动控制器状态，适合在运动控制流程中做前置检查 |
| `/motion/robot_state` | 机器人综合状态，适合状态面板或异常检测 |

=== "Python"

    ```python
    import json

    import rclpy
    from rclpy.node import Node
    from std_msgs.msg import String


    class StatusMonitor(Node):
        def __init__(self):
            super().__init__('status_monitor')

            self.create_subscription(
                String, '/motion/status', self.on_motion_status, 10)
            self.create_subscription(
                String, '/motion/robot_state', self.on_robot_state, 10)

        def on_motion_status(self, msg: String):
            try:
                data = json.loads(msg.data)
                self.get_logger().info(
                    f'motion/status: {json.dumps(data, ensure_ascii=False)}'
                )
            except json.JSONDecodeError:
                self.get_logger().warn(f'无法解析 motion/status: {msg.data}')

        def on_robot_state(self, msg: String):
            try:
                data = json.loads(msg.data)
                self.get_logger().info(
                    f'robot_state: {json.dumps(data, ensure_ascii=False)}'
                )
            except json.JSONDecodeError:
                self.get_logger().warn(f'无法解析 robot_state: {msg.data}')


    def main():
        rclpy.init()
        node = StatusMonitor()
        rclpy.spin(node)
        node.destroy_node()
        rclpy.shutdown()


    if __name__ == '__main__':
        main()
    ```

=== "C++"

    ```cpp
    #include <rclcpp/rclcpp.hpp>
    #include <std_msgs/msg/string.hpp>

    class StatusMonitor : public rclcpp::Node
    {
    public:
      StatusMonitor()
      : Node("status_monitor")
      {
        // 运动控制器状态
        motion_sub_ = create_subscription<std_msgs::msg::String>(
          "/motion/status", 10,
          [this](const std_msgs::msg::String::SharedPtr msg) {
            RCLCPP_INFO(get_logger(), "motion/status: %s",
                        msg->data.c_str());
          });

        // 机器人综合状态
        robot_sub_ = create_subscription<std_msgs::msg::String>(
          "/motion/robot_state", 10,
          [this](const std_msgs::msg::String::SharedPtr msg) {
            RCLCPP_INFO(get_logger(), "robot_state: %s",
                        msg->data.c_str());
          });
      }

    private:
      rclcpp::Subscription<std_msgs::msg::String>::SharedPtr motion_sub_;
      rclcpp::Subscription<std_msgs::msg::String>::SharedPtr robot_sub_;
    };

    int main(int argc, char ** argv)
    {
      rclcpp::init(argc, argv);
      rclcpp::spin(std::make_shared<StatusMonitor>());
      rclcpp::shutdown();
      return 0;
    }
    ```

---

## joystick_events -- 手柄输入

`joystick_events` 话题以 `crb_ros_msg/JoystickCmdReport` 消息类型发布手柄/遥控器的输入事件，默认频率 20 Hz。可用于通过手柄控制机器人动作或触发自定义逻辑。

**按钮映射表**

| 按钮 | ID | 备注 |
|------|----|------|
| A | 0 | |
| B | 1 | |
| X | 2 | |
| Y | 3 | |
| LB | 4 | 左肩键 |
| RB | 5 | 右肩键 |
| BACK | 6 | |
| START | 7 | |
| LEFT_AXIS | 9 | 左摇杆按下 |
| RIGHT_AXIS | 10 | 右摇杆按下 |
| LT | 11 | 左扳机 |
| RT | 12 | 右扳机 |

**JoystickCmdReport 字段**

| 字段 | 类型 | 说明 |
|------|------|------|
| `long_pressed` | `uint32[]` | 长按的按钮 ID 列表 |
| `single_clicked` | `uint32[]` | 单击的按钮 ID 列表 |
| `double_clicked` | `uint32[]` | 双击的按钮 ID 列表 |
| `axis_x` | `int8` | 十字键水平轴 |
| `axis_y` | `int8` | 十字键垂直轴 |
| `left_x` | `float32` | 左摇杆 X 轴，归一化到 [-1.0, 1.0] |
| `left_y` | `float32` | 左摇杆 Y 轴，归一化到 [-1.0, 1.0] |
| `right_x` | `float32` | 右摇杆 X 轴，归一化到 [-1.0, 1.0] |
| `right_y` | `float32` | 右摇杆 Y 轴，归一化到 [-1.0, 1.0] |
| `pressed_buttons` | `uint32[]` | 当前所有处于按下状态的按钮 ID |

!!! note
    左摇杆数据的输出与摇杆位移之间不是线性关系。

=== "Python"

    ```python
    import rclpy
    from rclpy.node import Node
    from crb_ros_msg.msg import JoystickCmdReport


    BUTTON_NAMES = {
        0: 'A', 1: 'B', 2: 'X', 3: 'Y',
        4: 'LB', 5: 'RB', 6: 'BACK', 7: 'START',
        9: 'LEFT_AXIS', 10: 'RIGHT_AXIS',
        11: 'LT', 12: 'RT',
    }


    class JoystickSubscriber(Node):
        def __init__(self):
            super().__init__('joystick_subscriber')
            self.create_subscription(
                JoystickCmdReport, 'joystick_events', self.callback, 10)

        def callback(self, msg: JoystickCmdReport):
            # 打印摇杆数据
            self.get_logger().info(
                f'左摇杆: ({msg.left_x:.2f}, {msg.left_y:.2f})  '
                f'右摇杆: ({msg.right_x:.2f}, {msg.right_y:.2f})'
            )
            # 打印十字键
            if msg.axis_x != 0 or msg.axis_y != 0:
                self.get_logger().info(
                    f'十字键: ({msg.axis_x}, {msg.axis_y})'
                )
            # 打印单击事件
            for btn_id in msg.single_clicked:
                name = BUTTON_NAMES.get(btn_id, str(btn_id))
                self.get_logger().info(f'单击: {name} (id={btn_id})')
            # 打印长按事件
            for btn_id in msg.long_pressed:
                name = BUTTON_NAMES.get(btn_id, str(btn_id))
                self.get_logger().info(f'长按: {name} (id={btn_id})')


    def main():
        rclpy.init()
        node = JoystickSubscriber()
        rclpy.spin(node)
        node.destroy_node()
        rclpy.shutdown()


    if __name__ == '__main__':
        main()
    ```

=== "C++"

    ```cpp
    #include <rclcpp/rclcpp.hpp>
    #include <crb_ros_msg/msg/joystick_cmd_report.hpp>

    #include <string>

    class JoystickSubscriber : public rclcpp::Node
    {
    public:
      JoystickSubscriber()
      : Node("joystick_subscriber")
      {
        sub_ = create_subscription<crb_ros_msg::msg::JoystickCmdReport>(
          "joystick_events", 10,
          [this](const crb_ros_msg::msg::JoystickCmdReport::SharedPtr msg) {
            RCLCPP_INFO(get_logger(),
                        "左摇杆: (%.2f, %.2f)  右摇杆: (%.2f, %.2f)",
                        msg->left_x, msg->left_y,
                        msg->right_x, msg->right_y);

            // 十字键
            if (msg->axis_x != 0 || msg->axis_y != 0) {
              RCLCPP_INFO(get_logger(), "十字键: (%d, %d)",
                          msg->axis_x, msg->axis_y);
            }

            // 单击事件
            for (auto btn_id : msg->single_clicked) {
              RCLCPP_INFO(get_logger(), "单击: id=%u", btn_id);
            }

            // 长按事件
            for (auto btn_id : msg->long_pressed) {
              RCLCPP_INFO(get_logger(), "长按: id=%u", btn_id);
            }
          });
      }

    private:
      rclcpp::Subscription<crb_ros_msg::msg::JoystickCmdReport>::SharedPtr sub_;
    };

    int main(int argc, char ** argv)
    {
      rclcpp::init(argc, argv);
      rclcpp::spin(std::make_shared<JoystickSubscriber>());
      rclcpp::shutdown();
      return 0;
    }
    ```

---

## 综合监听示例

以下示例在一个节点中同时订阅所有传感器话题，便于快速验证数据是否正常。

=== "Python"

    ```python
    import json

    import rclpy
    from rclpy.node import Node
    from sensor_msgs.msg import JointState, Imu
    from std_msgs.msg import String
    from crb_ros_msg.msg import JointStateData, JoystickCmdReport


    class AllSensorsNode(Node):
        def __init__(self):
            super().__init__('all_sensors_node')

            # 关节状态
            self.create_subscription(
                JointState, '/joint_states', self.on_joint_states, 10)
            self.create_subscription(
                JointStateData, '/motion/joint_state',
                self.on_motion_joint_state, 10)
            self.create_subscription(
                JointState, '/joint_control', self.on_joint_control, 10)

            # IMU
            self.create_subscription(Imu, '/imu', self.on_imu, 10)

            # 状态监控
            self.create_subscription(
                String, '/motion/status', self.on_motion_status, 10)
            self.create_subscription(
                String, '/motion/robot_state', self.on_robot_state, 10)

            # 手柄
            self.create_subscription(
                JoystickCmdReport, 'joystick_events',
                self.on_joystick, 10)

            self.get_logger().info('所有传感器订阅已建立')

        def on_joint_states(self, msg: JointState):
            n = len(msg.name)
            self.get_logger().info(f'/joint_states: {n} 个关节')

        def on_motion_joint_state(self, msg: JointStateData):
            n = len(msg.names)
            self.get_logger().info(
                f'/motion/joint_state: {n} 个关节, '
                f'默认增益={msg.use_default_kp_kd}'
            )

        def on_joint_control(self, msg: JointState):
            n = len(msg.name)
            self.get_logger().info(f'/joint_control: {n} 个关节')

        def on_imu(self, msg: Imu):
            q = msg.orientation
            self.get_logger().info(
                f'/imu: ori=({q.x:.2f},{q.y:.2f},{q.z:.2f},{q.w:.2f})'
            )

        def on_motion_status(self, msg: String):
            self.get_logger().info(f'/motion/status: {msg.data[:80]}')

        def on_robot_state(self, msg: String):
            self.get_logger().info(f'/motion/robot_state: {msg.data[:80]}')

        def on_joystick(self, msg: JoystickCmdReport):
            self.get_logger().info(
                f'joystick: 左=({msg.left_x:.2f},{msg.left_y:.2f}) '
                f'右=({msg.right_x:.2f},{msg.right_y:.2f})'
            )


    def main():
        rclpy.init()
        node = AllSensorsNode()
        rclpy.spin(node)
        node.destroy_node()
        rclpy.shutdown()


    if __name__ == '__main__':
        main()
    ```

=== "C++"

    ```cpp
    #include <rclcpp/rclcpp.hpp>
    #include <sensor_msgs/msg/joint_state.hpp>
    #include <sensor_msgs/msg/imu.hpp>
    #include <std_msgs/msg/string.hpp>
    #include <crb_ros_msg/msg/joint_state_data.hpp>
    #include <crb_ros_msg/msg/joystick_cmd_report.hpp>

    class AllSensorsNode : public rclcpp::Node
    {
    public:
      AllSensorsNode()
      : Node("all_sensors_node")
      {
        // 关节状态
        joint_states_sub_ = create_subscription<sensor_msgs::msg::JointState>(
          "/joint_states", 10,
          [this](const sensor_msgs::msg::JointState::SharedPtr msg) {
            RCLCPP_INFO(get_logger(), "/joint_states: %zu 个关节",
                        msg->name.size());
          });

        motion_joint_sub_ =
          create_subscription<crb_ros_msg::msg::JointStateData>(
            "/motion/joint_state", 10,
            [this](const crb_ros_msg::msg::JointStateData::SharedPtr msg) {
              RCLCPP_INFO(get_logger(),
                          "/motion/joint_state: %zu 个关节, 默认增益=%s",
                          msg->names.size(),
                          msg->use_default_kp_kd ? "true" : "false");
            });

        joint_control_sub_ = create_subscription<sensor_msgs::msg::JointState>(
          "/joint_control", 10,
          [this](const sensor_msgs::msg::JointState::SharedPtr msg) {
            RCLCPP_INFO(get_logger(), "/joint_control: %zu 个关节",
                        msg->name.size());
          });

        // IMU
        imu_sub_ = create_subscription<sensor_msgs::msg::Imu>(
          "/imu", 10,
          [this](const sensor_msgs::msg::Imu::SharedPtr msg) {
            auto & q = msg->orientation;
            RCLCPP_INFO(get_logger(),
                        "/imu: ori=(%.2f,%.2f,%.2f,%.2f)",
                        q.x, q.y, q.z, q.w);
          });

        // 状态监控
        motion_status_sub_ = create_subscription<std_msgs::msg::String>(
          "/motion/status", 10,
          [this](const std_msgs::msg::String::SharedPtr msg) {
            RCLCPP_INFO(get_logger(), "/motion/status: %s",
                        msg->data.substr(0, 80).c_str());
          });

        robot_state_sub_ = create_subscription<std_msgs::msg::String>(
          "/motion/robot_state", 10,
          [this](const std_msgs::msg::String::SharedPtr msg) {
            RCLCPP_INFO(get_logger(), "/motion/robot_state: %s",
                        msg->data.substr(0, 80).c_str());
          });

        // 手柄
        joystick_sub_ =
          create_subscription<crb_ros_msg::msg::JoystickCmdReport>(
            "joystick_events", 10,
            [this](const crb_ros_msg::msg::JoystickCmdReport::SharedPtr msg) {
              RCLCPP_INFO(get_logger(),
                          "joystick: 左=(%.2f,%.2f) 右=(%.2f,%.2f)",
                          msg->left_x, msg->left_y,
                          msg->right_x, msg->right_y);
            });

        RCLCPP_INFO(get_logger(), "所有传感器订阅已建立");
      }

    private:
      rclcpp::Subscription<sensor_msgs::msg::JointState>::SharedPtr
        joint_states_sub_;
      rclcpp::Subscription<crb_ros_msg::msg::JointStateData>::SharedPtr
        motion_joint_sub_;
      rclcpp::Subscription<sensor_msgs::msg::JointState>::SharedPtr
        joint_control_sub_;
      rclcpp::Subscription<sensor_msgs::msg::Imu>::SharedPtr imu_sub_;
      rclcpp::Subscription<std_msgs::msg::String>::SharedPtr
        motion_status_sub_;
      rclcpp::Subscription<std_msgs::msg::String>::SharedPtr
        robot_state_sub_;
      rclcpp::Subscription<crb_ros_msg::msg::JoystickCmdReport>::SharedPtr
        joystick_sub_;
    };

    int main(int argc, char ** argv)
    {
      rclcpp::init(argc, argv);
      rclcpp::spin(std::make_shared<AllSensorsNode>());
      rclcpp::shutdown();
      return 0;
    }
    ```
