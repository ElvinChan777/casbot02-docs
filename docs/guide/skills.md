# 技能与动作

本节介绍 CASBOT2 的技能与动作控制接口，包括基础动作播放、高级动作播放、行为树执行以及事件触发服务。

## 前置条件

在执行动作指令之前，请确认：

1. 已通过 `/set_robot_mode` 切换到合适的基础模式（如 `STAND`）
2. 机器人处于安全站立状态，周围有足够空间执行动作

详见[模式与状态](mode-and-state.md)。

---

## BasicActionPlay

通过 `/basic_action_play` Action（类型 `crb_ros_msg/BasicActionPlay`）让机器人执行预置的基础动作。该接口适用于简单手势的快速调用，无需额外参数配置。

### BasicActionPlay.Goal 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `action_type` | `string` | 预置动作类型，见下方列表 |

### 预置动作类型

| action_type | 说明 |
|-------------|------|
| `thumb_up` | 竖起大拇指 |
| `wave_hand` | 挥手打招呼 |
| `heart_gesture` | 双手比心 |
| `congratulation_gesture` | 恭喜/祝贺手势 |
| `v_gesture` | 比 V 手势 |

=== "Python"

    ```python
    import rclpy
    from rclpy.action import ActionClient
    from rclpy.node import Node
    from crb_ros_msg.action import BasicActionPlay


    class BasicActionNode(Node):
        def __init__(self):
            super().__init__('basic_action_node')
            self.action_cli = ActionClient(
                self, BasicActionPlay, '/basic_action_play')

        def play_action(self, action_type: str):
            if not self.action_cli.wait_for_server(timeout_sec=3.0):
                self.get_logger().error('/basic_action_play 服务不可用')
                return

            goal = BasicActionPlay.Goal()
            goal.action_type = action_type

            future = self.action_cli.send_goal_async(goal)
            rclpy.spin_until_future_complete(self, future)
            goal_handle = future.result()

            if not goal_handle.accepted:
                self.get_logger().warn('动作目标被拒绝')
                return

            self.get_logger().info(f'开始执行动作: {action_type}')

            # 等待动作完成
            result_future = goal_handle.get_result_async()
            rclpy.spin_until_future_complete(self, result_future)
            self.get_logger().info('动作执行完成')


    def main():
        rclpy.init()
        node = BasicActionNode()

        # 执行预置动作
        node.play_action('thumb_up')
        node.play_action('wave_hand')

        node.destroy_node()
        rclpy.shutdown()


    if __name__ == '__main__':
        main()
    ```

=== "C++"

    ```cpp
    #include <rclcpp/rclcpp.hpp>
    #include <rclcpp_action/rclcpp_action.hpp>
    #include <crb_ros_msg/action/basic_action_play.hpp>

    #include <chrono>
    #include <string>

    using BasicActionPlay = crb_ros_msg::action::BasicActionPlay;
    using namespace std::chrono_literals;

    class BasicActionNode : public rclcpp::Node
    {
    public:
      BasicActionNode()
      : Node("basic_action_node")
      {
        action_cli_ = rclcpp_action::create_client<BasicActionPlay>(
          this, "/basic_action_play");
      }

      void play_action(const std::string & action_type)
      {
        if (!action_cli_->wait_for_action_server(3s)) {
          RCLCPP_ERROR(get_logger(), "/basic_action_play 服务不可用");
          return;
        }

        auto goal = BasicActionPlay::Goal();
        goal.action_type = action_type;

        auto send_future = action_cli_->async_send_goal(goal);
        rclcpp::spin_until_future_complete(this->shared_from_this(), send_future);
        auto goal_handle = send_future.get();

        if (!goal_handle) {
          RCLCPP_WARN(get_logger(), "动作目标被拒绝");
          return;
        }

        RCLCPP_INFO(get_logger(), "开始执行动作: %s", action_type.c_str());

        // 等待动作完成
        auto result_future = action_cli_->async_get_result(goal_handle);
        rclcpp::spin_until_future_complete(
          this->shared_from_this(), result_future);
        RCLCPP_INFO(get_logger(), "动作执行完成");
      }

    private:
      rclcpp_action::Client<BasicActionPlay>::SharedPtr action_cli_;
    };

    int main(int argc, char ** argv)
    {
      rclcpp::init(argc, argv);
      auto node = std::make_shared<BasicActionNode>();

      // 执行预置动作
      node->play_action("thumb_up");
      node->play_action("wave_hand");

      rclcpp::shutdown();
      return 0;
    }
    ```

---

## ActionPlay

通过 `/action_play` Action（类型 `crb_ros_msg/ActionPlay`）播放高级动作。与 `BasicActionPlay` 不同，`ActionPlay` 支持指定动作起始时间、动作名称、取消动作名以及强化学习策略名称，适用于需要精细控制的复杂动作场景。

### ActionPlay.Goal 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `start_time` | `float64` | 动作起始时间（秒），用于延迟播放或从指定时间点开始 |
| `action_name` | `string` | 要播放的动作名称 |
| `cancel_action_name` | `string` | 取消当前动作后执行的过渡动作名称，留空则直接停止 |
| `rl_name` | `string` | 强化学习策略名称，用于指定动作执行所使用的控制策略 |

=== "Python"

    ```python
    import rclpy
    from rclpy.action import ActionClient
    from rclpy.node import Node
    from crb_ros_msg.action import ActionPlay


    class ActionPlayNode(Node):
        def __init__(self):
            super().__init__('action_play_node')
            self.action_cli = ActionClient(
                self, ActionPlay, '/action_play')

        def play_action(self, action_name: str, rl_name: str,
                        start_time: float = 0.0,
                        cancel_action_name: str = ''):
            if not self.action_cli.wait_for_server(timeout_sec=3.0):
                self.get_logger().error('/action_play 服务不可用')
                return

            goal = ActionPlay.Goal()
            goal.start_time = start_time
            goal.action_name = action_name
            goal.cancel_action_name = cancel_action_name
            goal.rl_name = rl_name

            future = self.action_cli.send_goal_async(goal)
            rclpy.spin_until_future_complete(self, future)
            goal_handle = future.result()

            if not goal_handle.accepted:
                self.get_logger().warn('动作目标被拒绝')
                return

            self.get_logger().info(
                f'开始播放动作: {action_name} (策略: {rl_name})')

            # 等待动作完成
            result_future = goal_handle.get_result_async()
            rclpy.spin_until_future_complete(self, result_future)
            self.get_logger().info('动作播放完成')


    def main():
        rclpy.init()
        node = ActionPlayNode()

        # 播放高级动作
        node.play_action(
            action_name='walk_forward',
            rl_name='default_walk_policy',
            start_time=0.0,
            cancel_action_name='stand_still'
        )

        node.destroy_node()
        rclpy.shutdown()


    if __name__ == '__main__':
        main()
    ```

=== "C++"

    ```cpp
    #include <rclcpp/rclcpp.hpp>
    #include <rclcpp_action/rclcpp_action.hpp>
    #include <crb_ros_msg/action/action_play.hpp>

    #include <chrono>
    #include <string>

    using ActionPlay = crb_ros_msg::action::ActionPlay;
    using namespace std::chrono_literals;

    class ActionPlayNode : public rclcpp::Node
    {
    public:
      ActionPlayNode()
      : Node("action_play_node")
      {
        action_cli_ = rclcpp_action::create_client<ActionPlay>(
          this, "/action_play");
      }

      void play_action(const std::string & action_name,
                       const std::string & rl_name,
                       double start_time = 0.0,
                       const std::string & cancel_action_name = "")
      {
        if (!action_cli_->wait_for_action_server(3s)) {
          RCLCPP_ERROR(get_logger(), "/action_play 服务不可用");
          return;
        }

        auto goal = ActionPlay::Goal();
        goal.start_time = start_time;
        goal.action_name = action_name;
        goal.cancel_action_name = cancel_action_name;
        goal.rl_name = rl_name;

        auto send_future = action_cli_->async_send_goal(goal);
        rclcpp::spin_until_future_complete(this->shared_from_this(), send_future);
        auto goal_handle = send_future.get();

        if (!goal_handle) {
          RCLCPP_WARN(get_logger(), "动作目标被拒绝");
          return;
        }

        RCLCPP_INFO(get_logger(), "开始播放动作: %s (策略: %s)",
                    action_name.c_str(), rl_name.c_str());

        // 等待动作完成
        auto result_future = action_cli_->async_get_result(goal_handle);
        rclcpp::spin_until_future_complete(
          this->shared_from_this(), result_future);
        RCLCPP_INFO(get_logger(), "动作播放完成");
      }

    private:
      rclcpp_action::Client<ActionPlay>::SharedPtr action_cli_;
    };

    int main(int argc, char ** argv)
    {
      rclcpp::init(argc, argv);
      auto node = std::make_shared<ActionPlayNode>();

      // 播放高级动作
      node->play_action(
        "walk_forward",
        "default_walk_policy",
        0.0,
        "stand_still"
      );

      rclcpp::shutdown();
      return 0;
    }
    ```

---

## ExecuteTree

通过 `/execute_tree` Action（类型 `crb_ros_msg/ExecuteTree`）让机器人执行行为树。行为树是一种结构化的决策与控制框架，可将多个动作、条件判断和控制流组合为复杂的技能逻辑。

### ExecuteTree.Goal 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `tree_name` | `string` | 要执行的行为树名称 |

=== "Python"

    ```python
    import rclpy
    from rclpy.action import ActionClient
    from rclpy.node import Node
    from crb_ros_msg.action import ExecuteTree


    class ExecuteTreeNode(Node):
        def __init__(self):
            super().__init__('execute_tree_node')
            self.action_cli = ActionClient(
                self, ExecuteTree, '/execute_tree')

        def execute(self, tree_name: str):
            if not self.action_cli.wait_for_server(timeout_sec=3.0):
                self.get_logger().error('/execute_tree 服务不可用')
                return

            goal = ExecuteTree.Goal()
            goal.tree_name = tree_name

            future = self.action_cli.send_goal_async(goal)
            rclpy.spin_until_future_complete(self, future)
            goal_handle = future.result()

            if not goal_handle.accepted:
                self.get_logger().warn('行为树目标被拒绝')
                return

            self.get_logger().info(f'开始执行行为树: {tree_name}')

            # 等待执行完成
            result_future = goal_handle.get_result_async()
            rclpy.spin_until_future_complete(self, result_future)
            self.get_logger().info('行为树执行完成')


    def main():
        rclpy.init()
        node = ExecuteTreeNode()

        # 执行行为树
        node.execute('greeting_tree')

        node.destroy_node()
        rclpy.shutdown()


    if __name__ == '__main__':
        main()
    ```

=== "C++"

    ```cpp
    #include <rclcpp/rclcpp.hpp>
    #include <rclcpp_action/rclcpp_action.hpp>
    #include <crb_ros_msg/action/execute_tree.hpp>

    #include <chrono>
    #include <string>

    using ExecuteTree = crb_ros_msg::action::ExecuteTree;
    using namespace std::chrono_literals;

    class ExecuteTreeNode : public rclcpp::Node
    {
    public:
      ExecuteTreeNode()
      : Node("execute_tree_node")
      {
        action_cli_ = rclcpp_action::create_client<ExecuteTree>(
          this, "/execute_tree");
      }

      void execute(const std::string & tree_name)
      {
        if (!action_cli_->wait_for_action_server(3s)) {
          RCLCPP_ERROR(get_logger(), "/execute_tree 服务不可用");
          return;
        }

        auto goal = ExecuteTree::Goal();
        goal.tree_name = tree_name;

        auto send_future = action_cli_->async_send_goal(goal);
        rclcpp::spin_until_future_complete(this->shared_from_this(), send_future);
        auto goal_handle = send_future.get();

        if (!goal_handle) {
          RCLCPP_WARN(get_logger(), "行为树目标被拒绝");
          return;
        }

        RCLCPP_INFO(get_logger(), "开始执行行为树: %s", tree_name.c_str());

        // 等待执行完成
        auto result_future = action_cli_->async_get_result(goal_handle);
        rclcpp::spin_until_future_complete(
          this->shared_from_this(), result_future);
        RCLCPP_INFO(get_logger(), "行为树执行完成");
      }

    private:
      rclcpp_action::Client<ExecuteTree>::SharedPtr action_cli_;
    };

    int main(int argc, char ** argv)
    {
      rclcpp::init(argc, argv);
      auto node = std::make_shared<ExecuteTreeNode>();

      // 执行行为树
      node->execute("greeting_tree");

      rclcpp::shutdown();
      return 0;
    }
    ```

---

## ActionEvent 事件触发服务

通过 `/casbot/event_service` 服务（类型 `crb_ros_msg/ActionEvent`）以事件方式触发机器人技能。与 Action 接口不同，事件服务以"发即忘"的方式通知技能系统执行指定事件，无需等待动作执行完成。

### ActionEvent.srv 定义

```text
# Request
string event_name    # 要触发的事件名称

---
# Response
bool success         # 事件是否成功接收
string msg           # 附加信息或错误描述
```

### 请求字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `event_name` | `string` | 要触发的事件名称，如 `"start_dance"`、`"stop_current"` |

### 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `success` | `bool` | 事件是否被成功接收 |
| `msg` | `string` | 附加信息或错误描述 |

!!! tip "Action vs Service 的选择"
    - **Action**（`/basic_action_play`、`/action_play`、`/execute_tree`）：适用于需要等待执行完成、获取执行反馈的场景
    - **Service**（`/casbot/event_service`）：适用于快速触发事件、不需要等待动作完成的场景

=== "Python"

    ```python
    import rclpy
    from rclpy.node import Node
    from crb_ros_msg.srv import ActionEvent


    class EventServiceNode(Node):
        def __init__(self):
            super().__init__('event_service_node')
            self.cli = self.create_client(ActionEvent, '/casbot/event_service')

        def trigger_event(self, event_name: str):
            if not self.cli.wait_for_service(timeout_sec=3.0):
                self.get_logger().error('/casbot/event_service 服务不可用')
                return None

            req = ActionEvent.Request()
            req.event_name = event_name

            future = self.cli.call_async(req)
            rclpy.spin_until_future_complete(self, future)
            result = future.result()
            if result:
                self.get_logger().info(
                    f'事件 [{event_name}]: '
                    f'success={result.success}, msg={result.msg}'
                )
            return result


    def main():
        rclpy.init()
        node = EventServiceNode()

        # 触发事件
        node.trigger_event('start_dance')
        node.trigger_event('stop_current')

        node.destroy_node()
        rclpy.shutdown()


    if __name__ == '__main__':
        main()
    ```

=== "C++"

    ```cpp
    #include <rclcpp/rclcpp.hpp>
    #include <crb_ros_msg/srv/action_event.hpp>

    #include <chrono>
    #include <string>

    using namespace std::chrono_literals;

    class EventServiceNode : public rclcpp::Node
    {
    public:
      EventServiceNode()
      : Node("event_service_node")
      {
        cli_ = create_client<crb_ros_msg::srv::ActionEvent>(
          "/casbot/event_service");
      }

      bool trigger_event(const std::string & event_name)
      {
        if (!cli_->wait_for_service(3s)) {
          RCLCPP_ERROR(get_logger(), "/casbot/event_service 服务不可用");
          return false;
        }

        auto req = std::make_shared<crb_ros_msg::srv::ActionEvent::Request>();
        req->event_name = event_name;

        auto future = cli_->async_send_request(req);
        rclcpp::spin_until_future_complete(this->shared_from_this(), future);
        if (future.valid() && future.wait_for(0s) == std::future_status::ready) {
          auto result = future.get();
          RCLCPP_INFO(get_logger(), "事件 [%s]: success=%s, msg=%s",
                      event_name.c_str(),
                      result->success ? "true" : "false",
                      result->msg.c_str());
          return result->success;
        }
        return false;
      }

    private:
      rclcpp::Client<crb_ros_msg::srv::ActionEvent>::SharedPtr cli_;
    };

    int main(int argc, char ** argv)
    {
      rclcpp::init(argc, argv);
      auto node = std::make_shared<EventServiceNode>();

      // 触发事件
      node->trigger_event("start_dance");
      node->trigger_event("stop_current");

      rclcpp::shutdown();
      return 0;
    }
    ```

---

## 接口速查表

| 功能 | 话题 / 服务 | 消息类型 | 方向 |
|------|------------|---------|------|
| 基础动作播放 | `/basic_action_play` | `crb_ros_msg/BasicActionPlay` | 开发者 -> 机器人 |
| 高级动作播放 | `/action_play` | `crb_ros_msg/ActionPlay` | 开发者 -> 机器人 |
| 行为树执行 | `/execute_tree` | `crb_ros_msg/ExecuteTree` | 开发者 -> 机器人 |
| 事件触发 | `/casbot/event_service` | `crb_ros_msg/ActionEvent` | 开发者 -> 机器人 |
