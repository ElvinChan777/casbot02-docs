# 运动控制

本节介绍 CASBOT2 的运动控制接口，包括导航速度控制、上身/全身关节调试控制、增益配置及状态反馈。

## 前置条件

在发布任何运动控制指令之前，请确认：

1. 已通过 `/set_robot_mode` 切换到合适的基础模式（如 `STAND` 或 `WALK`）
2. 已通过对应的调试模式 Service 开启控制权限
3. 已监听 `/motion/joint_state` 或 `/joint_states` 获取当前状态

详见[模式与状态](mode-and-state.md)。

---

## 导航速度控制

通过 `/navigation/cmd_vel` 话题（类型 `geometry_msgs/Twist`）向机器人发送行走速度指令。

**活跃字段**

| 字段 | 说明 |
|------|------|
| `linear.x` | 前进/后退线速度（m/s），正值前进 |
| `angular.z` | 转向角速度（rad/s），正值左转 |

!!! warning "linear.y 未接通"
    当前版本中 `linear.y` 没有接入控制通路，发送横向速度不会产生任何效果。如需平移运动，请通过旋转 + 前进组合实现。

**典型使用流程**

1. 通过 `/motion/switch_nav_mode` 启用导航模式
2. 持续发布 `/navigation/cmd_vel` 控制行走
3. 停止时发送零速度指令或停止发布

=== "Python"

    ```python
    import rclpy
    from rclpy.node import Node
    from geometry_msgs.msg import Twist
    from std_srvs.srv import SetBool


    class NavVelocityNode(Node):
        def __init__(self):
            super().__init__('nav_velocity_node')
            self.pub = self.create_publisher(Twist, '/navigation/cmd_vel', 10)

        def enable_nav_mode(self):
            cli = self.create_client(SetBool, '/motion/switch_nav_mode')
            cli.wait_for_service()
            req = SetBool.Request()
            req.data = True
            future = cli.call_async(req)
            rclpy.spin_until_future_complete(self, future)
            return future.result().success

        def send_velocity(self, linear_x: float, angular_z: float,
                          duration: float = 2.0):
            """持续发送速度指令 duration 秒，然后停止。"""
            import time
            msg = Twist()
            msg.linear.x = linear_x
            # msg.linear.y = 0.0  -- 未接通，无效
            msg.angular.z = angular_z

            rate = self.create_rate(10)  # 10 Hz
            end = time.time() + duration
            while time.time() < end and rclpy.ok():
                self.pub.publish(msg)
                rate.sleep()

            # 发送零速度停止
            self.pub.publish(Twist())
            self.get_logger().info('已发送停止指令')


    def main():
        rclpy.init()
        node = NavVelocityNode()
        node.enable_nav_mode()
        node.send_velocity(linear_x=0.2, angular_z=0.0, duration=2.0)
        node.destroy_node()
        rclpy.shutdown()


    if __name__ == '__main__':
        main()
    ```

=== "C++"

    ```cpp
    #include <rclcpp/rclcpp.hpp>
    #include <geometry_msgs/msg/twist.hpp>
    #include <std_srvs/srv/set_bool.hpp>

    #include <chrono>

    using namespace std::chrono_literals;

    class NavVelocityNode : public rclcpp::Node
    {
    public:
      NavVelocityNode()
      : Node("nav_velocity_node")
      {
        pub_ = create_publisher<geometry_msgs::msg::Twist>(
          "/navigation/cmd_vel", 10);
      }

      bool enable_nav_mode()
      {
        auto client =
          create_client<std_srvs::srv::SetBool>("/motion/switch_nav_mode");
        if (!client->wait_for_service(3s)) {
          RCLCPP_ERROR(get_logger(), "switch_nav_mode 服务不可用");
          return false;
        }
        auto req = std::make_shared<std_srvs::srv::SetBool::Request>();
        req->data = true;
        auto future = client->async_send_request(req);
        rclcpp::spin_until_future_complete(this->shared_from_this(), future);
        return future.get()->success;
      }

      void send_velocity(double linear_x, double angular_z,
                          double duration_sec = 2.0)
      {
        geometry_msgs::msg::Twist msg;
        msg.linear.x = linear_x;
        // msg.linear.y = 0.0;  -- 未接通，无效
        msg.angular.z = angular_z;

        auto end = std::chrono::steady_clock::now() +
                   std::chrono::duration<double>(duration_sec);
        rclcpp::Rate rate(10);  // 10 Hz
        while (rclcpp::ok() && std::chrono::steady_clock::now() < end) {
          pub_->publish(msg);
          rate.sleep();
        }

        // 发送零速度停止
        pub_->publish(geometry_msgs::msg::Twist{});
        RCLCPP_INFO(get_logger(), "已发送停止指令");
      }

    private:
      rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr pub_;
    };

    int main(int argc, char ** argv)
    {
      rclcpp::init(argc, argv);
      auto node = std::make_shared<NavVelocityNode>();
      node->enable_nav_mode();
      node->send_velocity(0.2, 0.0, 2.0);
      rclcpp::shutdown();
      return 0;
    }
    ```

---

## 上身调试模式

上身调试模式允许开发者直接控制上半身各关节的角度。适用于上肢动作调试和手势开发。

### 开启调试模式

通过 `/motion/upper_body_debug` 服务（类型 `std_srvs/SetBool`）开启或关闭上身调试：

| data | 效果 |
|------|------|
| `true` | 进入上身调试模式，接收关节指令 |
| `false` | 退出上身调试模式 |

### 发送关节指令

进入调试模式后，通过 `/upper_body_debug/joint_cmd` 话题发布 `UpperJointData` 消息控制关节。

**UpperJointData 字段**

| 字段 | 类型 | 说明 |
|------|------|------|
| `names` | `string[]` | 关节名称列表 |
| `positions` | `float64[]` | 关节目标角度（弧度） |
| `use_default_kp_kd` | `bool` | 是否使用默认增益（见[增益控制](#gain-control)） |
| `kp` | `float64[]` | 比例增益（仅 `use_default_kp_kd=false` 时需要） |
| `kd` | `float64[]` | 微分增益（仅 `use_default_kp_kd=false` 时需要） |

=== "Python"

    ```python
    import rclpy
    from rclpy.node import Node
    from std_srvs.srv import SetBool
    from crb_ros_msg.msg import UpperJointData
    import math


    class UpperBodyDebugNode(Node):
        def __init__(self):
            super().__init__('upper_body_debug_node')
            self.pub = self.create_publisher(
                UpperJointData, '/upper_body_debug/joint_cmd', 10)

        def enable_debug(self, on: bool = True):
            cli = self.create_client(SetBool, '/motion/upper_body_debug')
            cli.wait_for_service()
            req = SetBool.Request()
            req.data = on
            future = cli.call_async(req)
            rclpy.spin_until_future_complete(self, future)
            res = future.result()
            action = '开启' if on else '关闭'
            self.get_logger().info(
                f'上身调试模式 {action}: {"成功" if res.success else "失败"}'
            )

        def send_joint_cmd(self):
            msg = UpperJointData()
            msg.names = ['left_shoulder_pitch', 'left_shoulder_roll',
                         'left_elbow_pitch']
            msg.positions = [0.5, 0.2, -0.3]  # 弧度
            msg.use_default_kp_kd = True       # 使用默认增益
            self.pub.publish(msg)
            self.get_logger().info('已发送上身关节指令')


    def main():
        rclpy.init()
        node = UpperBodyDebugNode()
        node.enable_debug(True)
        node.send_joint_cmd()
        # ... 持续发送或执行其他控制
        node.enable_debug(False)
        node.destroy_node()
        rclpy.shutdown()


    if __name__ == '__main__':
        main()
    ```

=== "C++"

    ```cpp
    #include <rclcpp/rclcpp.hpp>
    #include <std_srvs/srv/set_bool.hpp>
    #include <crb_ros_msg/msg/upper_joint_data.hpp>

    #include <chrono>
    #include <vector>
    #include <string>

    using namespace std::chrono_literals;

    class UpperBodyDebugNode : public rclcpp::Node
    {
    public:
      UpperBodyDebugNode()
      : Node("upper_body_debug_node")
      {
        pub_ = create_publisher<crb_ros_msg::msg::UpperJointData>(
          "/upper_body_debug/joint_cmd", 10);
      }

      bool enable_debug(bool on = true)
      {
        auto client =
          create_client<std_srvs::srv::SetBool>("/motion/upper_body_debug");
        if (!client->wait_for_service(3s)) {
          RCLCPP_ERROR(get_logger(), "upper_body_debug 服务不可用");
          return false;
        }
        auto req = std::make_shared<std_srvs::srv::SetBool::Request>();
        req->data = on;
        auto future = client->async_send_request(request);
        rclcpp::spin_until_future_complete(this->shared_from_this(), future);
        return future.get()->success;
      }

      void send_joint_cmd()
      {
        crb_ros_msg::msg::UpperJointData msg;
        msg.names = {"left_shoulder_pitch", "left_shoulder_roll",
                     "left_elbow_pitch"};
        msg.positions = {0.5, 0.2, -0.3};  // 弧度
        msg.use_default_kp_kd = true;       // 使用默认增益
        pub_->publish(msg);
        RCLCPP_INFO(get_logger(), "已发送上身关节指令");
      }

    private:
      rclcpp::Publisher<crb_ros_msg::msg::UpperJointData>::SharedPtr pub_;
    };

    int main(int argc, char ** argv)
    {
      rclcpp::init(argc, argv);
      auto node = std::make_shared<UpperBodyDebugNode>();
      node->enable_debug(true);
      node->send_joint_cmd();
      // ... 持续发送或执行其他控制
      node->enable_debug(false);
      rclcpp::shutdown();
      return 0;
    }
    ```

---

## 全身调试模式

全身调试模式允许开发者同时控制上半身和下半身的全部关节，适用于全身协调运动开发。

### 开启调试模式

通过 `/motion/whole_body_debug` 服务（类型 `std_srvs/SetBool`）开启或关闭全身调试：

| data | 效果 |
|------|------|
| `true` | 进入全身调试模式，接收全身关节指令 |
| `false` | 退出全身调试模式 |

### 发送关节指令

进入调试模式后，通过 `/motion/joint_cmd` 话题发布 `JointStateData` 消息控制全身关节。

**JointStateData 字段**

| 字段 | 类型 | 说明 |
|------|------|------|
| `names` | `string[]` | 关节名称列表 |
| `positions` | `float64[]` | 关节目标角度（弧度） |
| `velocities` | `float64[]` | 关节目标速度（可选） |
| `use_default_kp_kd` | `bool` | 是否使用默认增益 |
| `kp` | `float64[]` | 比例增益（仅 `use_default_kp_kd=false` 时需要） |
| `kd` | `float64[]` | 微分增益（仅 `use_default_kp_kd=false` 时需要） |

=== "Python"

    ```python
    import rclpy
    from rclpy.node import Node
    from std_srvs.srv import SetBool
    from crb_ros_msg.msg import JointStateData


    class WholeBodyDebugNode(Node):
        def __init__(self):
            super().__init__('whole_body_debug_node')
            self.pub = self.create_publisher(
                JointStateData, '/motion/joint_cmd', 10)

        def enable_debug(self, on: bool = True):
            cli = self.create_client(SetBool, '/motion/whole_body_debug')
            cli.wait_for_service()
            req = SetBool.Request()
            req.data = on
            future = cli.call_async(req)
            rclpy.spin_until_future_complete(self, future)
            res = future.result()
            action = '开启' if on else '关闭'
            self.get_logger().info(
                f'全身调试模式 {action}: {"成功" if res.success else "失败"}'
            )

        def send_joint_cmd(self):
            msg = JointStateData()
            msg.names = ['left_hip_pitch', 'left_knee_pitch',
                         'left_shoulder_pitch', 'left_elbow_pitch']
            msg.positions = [-0.2, 0.4, 0.5, -0.3]  # 弧度
            msg.use_default_kp_kd = True              # 使用默认增益
            self.pub.publish(msg)
            self.get_logger().info('已发送全身关节指令')


    def main():
        rclpy.init()
        node = WholeBodyDebugNode()
        node.enable_debug(True)
        node.send_joint_cmd()
        node.enable_debug(False)
        node.destroy_node()
        rclpy.shutdown()


    if __name__ == '__main__':
        main()
    ```

=== "C++"

    ```cpp
    #include <rclcpp/rclcpp.hpp>
    #include <std_srvs/srv/set_bool.hpp>
    #include <crb_ros_msg/msg/joint_state_data.hpp>

    #include <chrono>
    #include <vector>
    #include <string>

    using namespace std::chrono_literals;

    class WholeBodyDebugNode : public rclcpp::Node
    {
    public:
      WholeBodyDebugNode()
      : Node("whole_body_debug_node")
      {
        pub_ = create_publisher<crb_ros_msg::msg::JointStateData>(
          "/motion/joint_cmd", 10);
      }

      bool enable_debug(bool on = true)
      {
        auto client =
          create_client<std_srvs::srv::SetBool>("/motion/whole_body_debug");
        if (!client->wait_for_service(3s)) {
          RCLCPP_ERROR(get_logger(), "whole_body_debug 服务不可用");
          return false;
        }
        auto req = std::make_shared<std_srvs::srv::SetBool::Request>();
        req->data = on;
        auto future = client->async_send_request(req);
        rclcpp::spin_until_future_complete(this->shared_from_this(), future);
        return future.get()->success;
      }

      void send_joint_cmd()
      {
        crb_ros_msg::msg::JointStateData msg;
        msg.names = {"left_hip_pitch", "left_knee_pitch",
                     "left_shoulder_pitch", "left_elbow_pitch"};
        msg.positions = {-0.2, 0.4, 0.5, -0.3};  // 弧度
        msg.use_default_kp_kd = true;              // 使用默认增益
        pub_->publish(msg);
        RCLCPP_INFO(get_logger(), "已发送全身关节指令");
      }

    private:
      rclcpp::Publisher<crb_ros_msg::msg::JointStateData>::SharedPtr pub_;
    };

    int main(int argc, char ** argv)
    {
      rclcpp::init(argc, argv);
      auto node = std::make_shared<WholeBodyDebugNode>();
      node->enable_debug(true);
      node->send_joint_cmd();
      node->enable_debug(false);
      rclcpp::shutdown();
      return 0;
    }
    ```

---

## 增益控制 { #gain-control }

`UpperJointData` 和 `JointStateData` 消息均包含增益（kp/kd）控制字段，用于调节关节的刚度和阻尼特性。

### 使用默认增益

将 `use_default_kp_kd` 设为 `true` 时，系统使用出厂默认的 kp/kd 参数，无需手动填写：

```python
msg.use_default_kp_kd = True
# 不需要设置 msg.kp 和 msg.kd
```

适合大多数常规场景，推荐初次调试时使用。

### 自定义增益

将 `use_default_kp_kd` 设为 `false` 时，**必须**提供 `kp` 和 `kd` 数组，且长度须与 `names`/`positions` 一致：

```python
msg.names = ['left_shoulder_pitch', 'left_shoulder_roll']
msg.positions = [0.5, 0.2]
msg.use_default_kp_kd = False
msg.kp = [80.0, 60.0]   # 比例增益
msg.kd = [5.0, 4.0]     # 微分增益
```

| 参数 | 作用 | 过高风险 | 过低风险 |
|------|------|---------|---------|
| `kp` | 位置跟踪刚度 | 震荡、过冲 | 响应迟缓、跟踪误差大 |
| `kd` | 速度阻尼 | 关节僵硬、噪声放大 | 超调、振荡 |

!!! tip "调参建议"
    - 从较小的 kp 值开始，逐步增大直到跟踪误差可接受
    - 适当增加 kd 抑制震荡，但不要过大
    - 调参过程中请确保有人在紧急停止按钮附近

---

## 状态反馈 { #state-feedback }

CASBOT2 通过两个通道发布关节状态，建议同时监听以获得最完整的反馈信息。

### 双通道对比

| Topic | 消息类型 | 说明 |
|-------|---------|------|
| `/motion/joint_state` | `crb_ros_msg/JointStateData` | CASBOT2 自定义格式，包含位置、速度、增益等详细信息 |
| `/joint_states` | `sensor_msgs/JointState` | ROS 2 标准格式，兼容 RViz 等通用工具 |

=== "Python"

    ```python
    import rclpy
    from rclpy.node import Node
    from crb_ros_msg.msg import JointStateData
    from sensor_msgs.msg import JointState


    class JointStateMonitor(Node):
        def __init__(self):
            super().__init__('joint_state_monitor')

            # 通道 1: CASBOT2 自定义格式
            self.create_subscription(
                JointStateData, '/motion/joint_state',
                self.on_motion_joint_state, 10)

            # 通道 2: ROS 2 标准格式
            self.create_subscription(
                JointState, '/joint_states',
                self.on_joint_states, 10)

        def on_motion_joint_state(self, msg: JointStateData):
            for name, pos in zip(msg.names, msg.positions):
                self.get_logger().info(f'[motion] {name}: {pos:.3f} rad')

        def on_joint_states(self, msg: JointState):
            for name, pos in zip(msg.name, msg.position):
                self.get_logger().info(f'[standard] {name}: {pos:.3f} rad')


    def main():
        rclpy.init()
        node = JointStateMonitor()
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
    #include <sensor_msgs/msg/joint_state.hpp>

    class JointStateMonitor : public rclcpp::Node
    {
    public:
      JointStateMonitor()
      : Node("joint_state_monitor")
      {
        // 通道 1: CASBOT2 自定义格式
        motion_sub_ = create_subscription<crb_ros_msg::msg::JointStateData>(
          "/motion/joint_state", 10,
          [this](const crb_ros_msg::msg::JointStateData::SharedPtr msg) {
            for (size_t i = 0; i < msg->names.size(); ++i) {
              RCLCPP_INFO(get_logger(), "[motion] %s: %.3f rad",
                          msg->names[i].c_str(), msg->positions[i]);
            }
          });

        // 通道 2: ROS 2 标准格式
        standard_sub_ = create_subscription<sensor_msgs::msg::JointState>(
          "/joint_states", 10,
          [this](const sensor_msgs::msg::JointState::SharedPtr msg) {
            for (size_t i = 0; i < msg->name.size(); ++i) {
              RCLCPP_INFO(get_logger(), "[standard] %s: %.3f rad",
                          msg->name[i].c_str(), msg->position[i]);
            }
          });
      }

    private:
      rclcpp::Subscription<crb_ros_msg::msg::JointStateData>::SharedPtr
        motion_sub_;
      rclcpp::Subscription<sensor_msgs::msg::JointState>::SharedPtr
        standard_sub_;
    };

    int main(int argc, char ** argv)
    {
      rclcpp::init(argc, argv);
      rclpy::spin(std::make_shared<JointStateMonitor>());
      rclcpp::shutdown();
      return 0;
    }
    ```

---

## 安全建议

!!! danger "调试安全守则"

    1. **低速起步** -- 导航速度从 0.1 m/s 开始，逐步提高；关节角度增量不超过 0.1 rad/步
    2. **默认增益优先** -- 首次调试务必使用 `use_default_kp_kd=true`，确认基本行为正常后再尝试自定义增益
    3. **双通道观测** -- 同时监听 `/motion/joint_state` 和 `/joint_states`，交叉验证关节反馈是否一致
    4. **紧急停止** -- 确保有人能在异常情况下立即通过急停按钮或发送零速度指令停止机器人
    5. **模式顺序** -- 先开启调试模式再发布指令，先停止指令再关闭调试模式
    6. **避免指令丢失** -- 持续以固定频率（建议 10-50 Hz）发布指令，避免单次发送后长时间不更新导致关节保持上一条指令的力矩
    7. **linear.y 无效** -- `/navigation/cmd_vel` 的 `linear.y` 当前未接通，不要依赖该字段做横向运动规划

---

## 接口速查表

| 功能 | 话题 / 服务 | 消息类型 | 方向 |
|------|------------|---------|------|
| 导航速度 | `/navigation/cmd_vel` | `geometry_msgs/Twist` | 开发者 -> 机器人 |
| 上身调试开关 | `/motion/upper_body_debug` | `std_srvs/SetBool` | 开发者 -> 机器人 |
| 上身关节控制 | `/upper_body_debug/joint_cmd` | `crb_ros_msg/UpperJointData` | 开发者 -> 机器人 |
| 全身调试开关 | `/motion/whole_body_debug` | `std_srvs/SetBool` | 开发者 -> 机器人 |
| 全身关节控制 | `/motion/joint_cmd` | `crb_ros_msg/JointStateData` | 开发者 -> 机器人 |
| 关节状态反馈 | `/motion/joint_state` | `crb_ros_msg/JointStateData` | 机器人 -> 开发者 |
| 标准关节状态 | `/joint_states` | `sensor_msgs/JointState` | 机器人 -> 开发者 |
