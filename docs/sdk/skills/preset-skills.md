# 预设技能

CASBOT02 内置多种预设技能（动作+音频组合），可通过 ROS2 Service 远程调用。

## 接口定义

| 属性 | 值 |
|---|---|
| **通讯方式** | ROS2 Service |
| **Service 名称** | `/casbot/event_service` |
| **Service 类型** | `crb_ros_msg/srv/ActionEvent` |
| **依赖包** | `crb_ros_msg` |

## 预设技能清单

| 技能名称 | `target_tree` | `payload` |
|---|---|---|
| 点赞 | `basic_action_play` | `{"action_type": "thumb_up"}` |
| 挥手 | `basic_action_play` | `{"action_type": "wave_hand"}` |
| 比心 | `basic_action_play` | `{"action_type": "heart_gesture"}` |
| 恭喜 | `basic_action_play` | `{"action_type": "congratulation_gesture"}` |
| 剪刀手/耶 | `basic_action_play` | `{"action_type": "v_gesture"}` |
| 握手 | `hand_shake` | `{}` |
| 自我介绍 | `self_introduction` | `{}` |
| 石头剪刀布 | `rock_paper_scissors` | `{"robot_gesture": "rock"}` |

!!! tip "石头剪刀布参数"
    `robot_gesture` 可选值：`rock`（石头）、`scissors`（剪刀）、`paper`（布）

## 代码示例

=== "Python"

    ```python
    import rclpy
    from rclpy.node import Node
    from crb_ros_msg.srv import ActionEvent
    import json


    class SkillCaller(Node):
        def __init__(self):
            super().__init__('skill_caller')
            self.client = self.create_client(
                ActionEvent, '/casbot/event_service')
            self.client.wait_for_service()

        def execute_skill(self, target_tree: str, action_type: str = ''):
            """执行预设技能"""
            req = ActionEvent.Request()
            req.event_id = ''
            req.event_type = 'ExecSkill'
            req.blocking = False

            payload = {"action_type": action_type} if action_type else {}
            param = {
                "payload": json.dumps(payload),
                "target_tree": target_tree
            }
            req.param_json = json.dumps(param)

            return self.client.call_async(req)


    def main():
        rclpy.init()
        node = SkillCaller()

        # 挥手
        future = node.execute_skill('basic_action_play', 'wave_hand')
        rclpy.spin_until_future_complete(node, future)
        node.get_logger().info(f'结果: {future.result()}')

        node.destroy_node()
        rclpy.shutdown()


    if __name__ == '__main__':
        main()
    ```

=== "C++"

    ```cpp
    #include <rclcpp/rclcpp.hpp>
    #include <crb_ros_msg/srv/action_event.hpp>
    #include <nlohmann/json.hpp>

    using json = nlohmann::json;

    class SkillCaller : public rclcpp::Node {
    public:
        SkillCaller() : Node("skill_caller") {
            client_ = create_client<crb_ros_msg::srv::ActionEvent>(
                "/casbot/event_service");
            client_->wait_for_service();
        }

        auto executeSkill(const std::string& targetTree,
                          const std::string& actionType = "") {
            auto req = std::make_shared<crb_ros_msg::srv::ActionEvent::Request>();
            req->event_id = "";
            req->event_type = "ExecSkill";
            req->blocking = false;

            json payload = actionType.empty()
                ? json::object()
                : json{{"action_type", actionType}};
            json param = {
                {"payload", payload.dump()},
                {"target_tree", targetTree}
            };
            req->param_json = param.dump();

            return client_->async_send_request(req);
        }

    private:
        rclcpp::Client<crb_ros_msg::srv::ActionEvent>::SharedPtr client_;
    };

    int main(int argc, char** argv) {
        rclcpp::init(argc, argv);
        auto node = std::make_shared<SkillCaller>();

        // 挥手
        auto future = node->executeSkill("basic_action_play", "wave_hand");
        rclcpp::spin_until_future_complete(node, future);

        rclcpp::shutdown();
        return 0;
    }
    ```

### 命令行测试

```bash
# 挥手
ros2 service call /casbot/event_service crb_ros_msg/srv/ActionEvent \
  '{"event_id":"","event_type":"ExecSkill","blocking":false,"param_json": "{\"payload\": \"{\\\"action_type\\\":\\\"wave_hand\\\"}\", \"target_tree\": \"basic_action_play\"}"}'

# 石头剪刀布（出石头）
ros2 service call /casbot/event_service crb_ros_msg/srv/ActionEvent \
  '{"event_id":"","event_type":"ExecSkill","blocking":false,"param_json": "{\"payload\": \"{\\\"robot_gesture\\\":\\\"rock\\\"}\", \"target_tree\": \"rock_paper_scissors\"}"}'
```
