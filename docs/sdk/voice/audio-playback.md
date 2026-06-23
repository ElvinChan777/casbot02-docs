# 音频播放

## 播放接口

| 属性 | 值 |
|---|---|
| **通讯方式** | ROS2 Action |
| **Action 名称** | `/action_voice_play` |
| **Action 类型** | `crb_ros_msg/action/VoicePlay` |
| **依赖包** | `crb_ros_msg` |

## 音频文件要求

| 属性 | 要求 |
|---|---|
| 格式 | WAV |
| 编码 | Signed 16-bit PCM |
| 声道 | 单声道 |
| 采样率 | 16000 Hz |

## 存放路径

音频文件存放在 HRU 的以下目录：

```
/workspace/prod_hru/share/voice_interface/resource/voice_files/
```

## 命令行调用

```bash
ros2 action send_goal /action_voice_play crb_ros_msg/action/VoicePlay \
  '{"wav_path": "audio_name.wav"}'
```

## 语音合成

如需生成新的语音文件：

1. 浏览器登录扣子平台：[www.coze.cn](https://www.coze.cn)
2. 获取个人访问令牌
3. 使用语音合成功能下载音频
4. 拷贝音频到 HRU 指定目录
5. 使用 `ros2 action` 调用播放

<!-- TODO: 补充 Python/C++ 代码示例 -->
