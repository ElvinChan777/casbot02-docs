# 语音对话

CASBOT02 支持实时语音对话和文本问答两种交互方式。

## 实时对话

通过 ROS2 Service 控制实时对话功能的开启和关闭。

| 属性 | 值 |
|---|---|
| **通讯方式** | ROS2 Service |
| **Service 名称** | `/voice_svr` |
| **Service 类型** | `crb_ros_msg/srv/Voice` |
| **依赖包** | `crb_ros_msg` |

### 接口参数

| 字段 | 类型 | 说明 |
|---|---|---|
| `type` | string | 操作类型：`rtc_start` / `rtc_stop` / `question` / `answer` |
| `content_type` | string | 内容类型：`text` / `object_string`（answer 时使用） |
| `content` | string | 文本内容 |

### 代码示例

=== "Python"

    ```python
    import rclpy
    from rclpy.node import Node
    from crb_ros_msg.srv import Voice


    class VoiceClient(Node):
        def __init__(self):
            super().__init__('voice_client')
            self.client = self.create_client(Voice, '/voice_svr')
            self.client.wait_for_service()

        def start_realtime(self):
            """开启实时对话"""
            req = Voice.Request()
            req.type = 'rtc_start'
            req.content_type = ''
            req.content = ''
            return self.client.call_async(req)

        def stop_realtime(self):
            """关闭实时对话"""
            req = Voice.Request()
            req.type = 'rtc_stop'
            req.content_type = ''
            req.content = ''
            return self.client.call_async(req)

        def ask_question(self, text: str):
            """文本提问"""
            req = Voice.Request()
            req.type = 'question'
            req.content_type = 'text'
            req.content = text
            return self.client.call_async(req)

        def send_answer(self, text: str):
            """发送回答（让机器人说出指定内容）"""
            req = Voice.Request()
            req.type = 'answer'
            req.content_type = 'object_string'
            req.content = text
            return self.client.call_async(req)
    ```

=== "C++"

    ```cpp
    #include <rclcpp/rclcpp.hpp>
    #include <crb_ros_msg/srv/voice.hpp>

    class VoiceClient : public rclcpp::Node {
    public:
        VoiceClient() : Node("voice_client") {
            client_ = create_client<crb_ros_msg::srv::Voice>("/voice_svr");
            client_->wait_for_service();
        }

        auto startRealtime() {
            auto req = std::make_shared<crb_ros_msg::srv::Voice::Request>();
            req->type = "rtc_start";
            return client_->async_send_request(req);
        }

        auto stopRealtime() {
            auto req = std::make_shared<crb_ros_msg::srv::Voice::Request>();
            req->type = "rtc_stop";
            return client_->async_send_request(req);
        }

        auto askQuestion(const std::string& text) {
            auto req = std::make_shared<crb_ros_msg::srv::Voice::Request>();
            req->type = "question";
            req->content_type = "text";
            req->content = text;
            return client_->async_send_request(req);
        }

        auto sendAnswer(const std::string& text) {
            auto req = std::make_shared<crb_ros_msg::srv::Voice::Request>();
            req->type = "answer";
            req->content_type = "object_string";
            req->content = text;
            return client_->async_send_request(req);
        }

    private:
        rclcpp::Client<crb_ros_msg::srv::Voice>::SharedPtr client_;
    };
    ```

### 命令行测试

```bash
# 开启实时对话
ros2 service call /voice_svr crb_ros_msg/srv/Voice \
  "{type: 'rtc_start', content_type: '', content: ''}"

# 关闭实时对话
ros2 service call /voice_svr crb_ros_msg/srv/Voice \
  "{type: 'rtc_stop', content_type: '', content: ''}"

# 文本提问
ros2 service call /voice_svr crb_ros_msg/srv/Voice \
  "{type: 'question', content_type: 'text', content: '你好，你叫什么名字'}"

# 文本回答（让机器人说话）
ros2 service call /voice_svr crb_ros_msg/srv/Voice \
  "{type: 'answer', content_type: 'object_string', content: '我叫CASBOT02,很高兴见到你'}"
```

## MIC / Speaker 硬件

CASBOT02 的麦克风和扬声器连接在 HRU 上，为一体式设备。

<!-- TODO: 迁移 MIC/Speaker lsusb 截图 -->
