# 语音交互

本节介绍 CASBOT2 的语音交互接口，包括语音服务控制和音频播放。

## 语音服务

通过 `/voice_svr` 服务（类型 `crb_ros_msg/Voice`）与机器人的语音系统进行交互。该服务支持语音识别会话控制、文本提问和文本应答。

### Voice.srv 定义

```text
# Request
# rtc_start, rtc_stop, question, answer
string type

# text, object_string
string content_type

# xxxx, {"xx": "xxxxx", ...}
string content

---
# Response
bool success

# error description
string msg
```

### 请求字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `type` | `string` | 操作类型，见下方说明 |
| `content_type` | `string` | 内容类型，见下方说明 |
| `content` | `string` | 具体内容，格式取决于 `content_type` |

### 操作类型 (type)

| 值 | 说明 |
|----|------|
| `rtc_start` | 开启实时语音对话（Real-Time Conversation）会话 |
| `rtc_stop` | 关闭实时语音对话会话 |
| `question` | 向语音系统发送一条文本提问 |
| `answer` | 向语音系统发送一条文本应答 |

### 内容类型 (content_type)

| 值 | content 格式 | 说明 |
|----|-------------|------|
| `text` | 纯文本字符串 | 直接传递文本内容，如 `"你好"` |
| `object_string` | JSON 字符串 | 结构化内容，如 `{"key": "value"}` |

!!! tip "type 与 content_type 的关系"
    - `rtc_start` / `rtc_stop` 通常不需要 `content`，可留空
    - `question` / `answer` 需要填写 `content`，根据实际需求选择 `text` 或 `object_string`

---

### 发送文本提问

=== "Python"

    ```python
    import rclpy
    from rclpy.node import Node
    from crb_ros_msg.srv import Voice


    class VoiceQuestionNode(Node):
        def __init__(self):
            super().__init__('voice_question_node')
            self.cli = self.create_client(Voice, '/voice_svr')

        def ask_question(self, text: str):
            if not self.cli.wait_for_service(timeout_sec=3.0):
                self.get_logger().error('voice_svr 服务不可用')
                return None

            req = Voice.Request()
            req.type = 'question'
            req.content_type = 'text'
            req.content = text

            future = self.cli.call_async(req)
            rclpy.spin_until_future_complete(self, future)
            result = future.result()
            if result:
                self.get_logger().info(
                    f'voice_svr: success={result.success}, msg={result.msg}'
                )
            return result


    def main():
        rclpy.init()
        node = VoiceQuestionNode()
        node.ask_question('你好')
        node.destroy_node()
        rclpy.shutdown()


    if __name__ == '__main__':
        main()
    ```

=== "C++"

    ```cpp
    #include <rclcpp/rclcpp.hpp>
    #include <crb_ros_msg/srv/voice.hpp>

    #include <chrono>
    #include <string>

    using namespace std::chrono_literals;

    class VoiceQuestionNode : public rclcpp::Node
    {
    public:
      VoiceQuestionNode()
      : Node("voice_question_node")
      {
        cli_ = create_client<crb_ros_msg::srv::Voice>("/voice_svr");
      }

      void ask_question(const std::string & text)
      {
        if (!cli_->wait_for_service(3s)) {
          RCLCPP_ERROR(get_logger(), "voice_svr 服务不可用");
          return;
        }

        auto req = std::make_shared<crb_ros_msg::srv::Voice::Request>();
        req->type = "question";
        req->content_type = "text";
        req->content = text;

        auto future = cli_->async_send_request(req);
        rclcpp::spin_until_future_complete(this->shared_from_this(), future);
        if (fut.valid() && fut.wait_for(0s) == std::future_status::ready) {
          auto result = future.get();
          RCLCPP_INFO(get_logger(), "voice_svr: success=%s, msg=%s",
                      result->success ? "true" : "false",
                      result->msg.c_str());
        }
      }

    private:
      rclcpp::Client<crb_ros_msg::srv::Voice>::SharedPtr cli_;
    };

    int main(int argc, char ** argv)
    {
      rclcpp::init(argc, argv);
      auto node = std::make_shared<VoiceQuestionNode>();
      node->ask_question("你好");
      rclcpp::shutdown();
      return 0;
    }
    ```

---

### 开启 / 关闭实时语音对话

=== "Python"

    ```python
    import rclpy
    from rclpy.node import Node
    from crb_ros_msg.srv import Voice


    class VoiceRTCNode(Node):
        def __init__(self):
            super().__init__('voice_rtc_node')
            self.cli = self.create_client(Voice, '/voice_svr')

        def call_voice(self, vtype: str, content: str = ''):
            if not self.cli.wait_for_service(timeout_sec=3.0):
                self.get_logger().error('voice_svr 服务不可用')
                return None

            req = Voice.Request()
            req.type = vtype
            req.content_type = 'text'
            req.content = content

            future = self.cli.call_async(req)
            rclpy.spin_until_future_complete(self, future)
            return future.result()

        def start_rtc(self):
            res = self.call_voice('rtc_start')
            if res:
                self.get_logger().info(
                    f'rtc_start: success={res.success}, msg={res.msg}'
                )

        def stop_rtc(self):
            res = self.call_voice('rtc_stop')
            if res:
                self.get_logger().info(
                    f'rtc_stop: success={res.success}, msg={res.msg}'
                )


    def main():
        rclpy.init()
        node = VoiceRTCNode()
        node.start_rtc()
        # ... 进行语音对话 ...
        node.stop_rtc()
        node.destroy_node()
        rclpy.shutdown()


    if __name__ == '__main__':
        main()
    ```

=== "C++"

    ```cpp
    #include <rclcpp/rclcpp.hpp>
    #include <crb_ros_msg/srv/voice.hpp>

    #include <chrono>
    #include <string>

    using namespace std::chrono_literals;

    class VoiceRTCNode : public rclcpp::Node
    {
    public:
      VoiceRTCNode()
      : Node("voice_rtc_node")
      {
        cli_ = create_client<crb_ros_msg::srv::Voice>("/voice_svr");
      }

      bool call_voice(const std::string & vtype,
                      const std::string & content = "")
      {
        if (!cli_->wait_for_service(3s)) {
          RCLCPP_ERROR(get_logger(), "voice_svr 服务不可用");
          return false;
        }

        auto req = std::make_shared<crb_ros_msg::srv::Voice::Request>();
        req->type = vtype;
        req->content_type = "text";
        req->content = content;

        auto future = cli_->async_send_request(req);
        rclcpp::spin_until_future_complete(this->shared_from_this(), future);
        if (future.valid() && future.wait_for(0s) == std::future_status::ready) {
          auto result = future.get();
          RCLCPP_INFO(get_logger(), "%s: success=%s, msg=%s",
                      vtype.c_str(),
                      result->success ? "true" : "false",
                      result->msg.c_str());
          return result->success;
        }
        return false;
      }

    private:
      rclcpp::Client<crb_ros_msg::srv::Voice>::SharedPtr cli_;
    };

    int main(int argc, char ** argv)
    {
      rclcpp::init(argc, argv);
      auto node = std::make_shared<VoiceRTCNode>();
      node->call_voice("rtc_start");
      // ... 进行语音对话 ...
      node->call_voice("rtc_stop");
      rclcpp::shutdown();
      return 0;
    }
    ```

---

## 音频播放

通过 `/action_voice_play` Action（类型 `crb_ros_msg/VoicePlay`）让机器人播放指定的音频文件。该接口使用 ROS 2 Action 机制，支持目标反馈和结果回调。

### VoicePlay.Goal 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `wav_path` | `string` | 要播放的音频文件路径 |

### 发送音频播放目标

=== "Python"

    ```python
    import rclpy
    from rclpy.action import ActionClient
    from rclpy.node import Node
    from crb_ros_msg.action import VoicePlay


    class VoicePlayNode(Node):
        def __init__(self):
            super().__init__('voice_play_node')
            self.action_cli = ActionClient(
                self, VoicePlay, '/action_voice_play')

        def play_audio(self, wav_path: str):
            if not self.action_cli.wait_for_server(timeout_sec=3.0):
                self.get_logger().error('action_voice_play 服务不可用')
                return

            goal = VoicePlay.Goal()
            goal.wav_path = wav_path

            future = self.action_cli.send_goal_async(goal)
            rclpy.spin_until_future_complete(self, future)
            goal_handle = future.result()

            if not goal_handle.accepted:
                self.get_logger().warn('播放目标被拒绝')
                return

            self.get_logger().info(f'开始播放: {wav_path}')

            # 等待播放完成
            result_future = goal_handle.get_result_async()
            rclpy.spin_until_future_complete(self, result_future)
            self.get_logger().info('播放完成')


    def main():
        rclpy.init()
        node = VoicePlayNode()
        node.play_audio('test.wav')
        node.destroy_node()
        rclpy.shutdown()


    if __name__ == '__main__':
        main()
    ```

=== "C++"

    ```cpp
    #include <rclcpp/rclcpp.hpp>
    #include <rclcpp_action/rclcpp_action.hpp>
    #include <crb_ros_msg/action/voice_play.hpp>

    #include <chrono>
    #include <string>

    using VoicePlay = crb_ros_msg::action::VoicePlay;
    using namespace std::chrono_literals;

    class VoicePlayNode : public rclcpp::Node
    {
    public:
      VoicePlayNode()
      : Node("voice_play_node")
      {
        action_cli_ = rclcpp_action::create_client<VoicePlay>(
          this, "/action_voice_play");
      }

      void play_audio(const std::string & wav_path)
      {
        if (!action_cli_->wait_for_action_server(3s)) {
          RCLCPP_ERROR(get_logger(), "action_voice_play 服务不可用");
          return;
        }

        auto goal = VoicePlay::Goal();
        goal.wav_path = wav_path;

        auto send_future = action_cli_->async_send_goal(goal);
        rclcpp::spin_until_future_complete(this->shared_from_this(), send_future);
        auto goal_handle = send_future.get();

        if (!goal_handle) {
          RCLCPP_WARN(get_logger(), "播放目标被拒绝");
          return;
        }

        RCLCPP_INFO(get_logger(), "开始播放: %s", wav_path.c_str());

        // 等待播放完成
        auto result_future = action_cli_->async_get_result(goal_handle);
        rclcpp::spin_until_future_complete(
          this->shared_from_this(), result_future);
        RCLCPP_INFO(get_logger(), "播放完成");
      }

    private:
      rclcpp_action::Client<VoicePlay>::SharedPtr action_cli_;
    };

    int main(int argc, char ** argv)
    {
      rclcpp::init(argc, argv);
      auto node = std::make_shared<VoicePlayNode>();
      node->play_audio("test.wav");
      rclcpp::shutdown();
      return 0;
    }
    ```

---

## 接口速查表

| 功能 | 话题 / 服务 | 消息类型 | 方向 |
|------|------------|---------|------|
| 语音服务控制 | `/voice_svr` | `crb_ros_msg/Voice` | 开发者 -> 机器人 |
| 音频播放 | `/action_voice_play` | `crb_ros_msg/VoicePlay` | 开发者 -> 机器人 |
