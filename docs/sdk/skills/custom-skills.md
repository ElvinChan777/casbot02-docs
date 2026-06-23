# 技能定制

CASBOT02 支持自定义技能，每个技能包含**动作数据**（.data）和**音频文件**（.wav）两个元素。

## 文件格式

### 动作数据（.data）

| 属性 | 要求 |
|---|---|
| 格式 | CSV 文本，61 列数据，逗号分隔 |
| 帧率 | 50 Hz |
| 存放路径（Orin） | `/workspace/prod_casbot02_basic/share/crb_resources/resources/motion/` |

!!! warning "帧间距限制"
    旧版程序相邻帧之间无插值，因此相邻帧手臂末端笛卡尔空间距离不能过大。

### 数据列定义

| 列范围 | 内容 | 说明 |
|---|---|---|
| 1-12 | Base 数据 | 平移(1-3) + 旋转(4-6) + 线速度(7-9) + 角速度(10-12) |
| 13-18 | 左腿关节 (1-6) | pelvic pitch/roll/yaw, knee pitch, ankle pitch/roll |
| 19-24 | 右腿关节 (1-6) | 同上 |
| 25-31 | 左臂关节 (1-7) | shoulder pitch/roll/yaw, elbow pitch, wrist yaw/pitch/roll |
| 32-38 | 右臂关节 (1-7) | 同上 |
| 39-48 | 左手手指 (1-10) | 含被动关节 |
| 49-58 | 右手手指 (1-10) | 含被动关节 |
| 59-60 | 头部 (1-2) | head_yaw, head_pitch |
| 61 | 腰部 | waist_yaw |

### 音频文件（.wav）

| 属性 | 要求 |
|---|---|
| 格式 | WAV |
| 声道 | 单声道 |
| 采样率 | 16000 Hz |
| 存放路径（HRU） | `/workspace/prod_hru/share/crb_resources/resources/voice_files_cn/`（中文）<br>`/workspace/prod_hru/share/crb_resources/resources/voice_files_en/`（英文） |

## 定制流程

### 1. 生成动作数据

基于动画设计软件或 RViz 生成 CASBOT02 的上身运动轨迹数据，按上述 .data 格式保存。

### 2. 生成音频文件

通过扣子平台（[coze.cn](https://www.coze.cn)）的语音合成功能生成音频，按格式要求保存。

### 3. 部署文件

```bash
# 动作数据 → Orin
scp test.data orin:/workspace/prod_casbot02_basic/share/crb_resources/resources/motion/

# 音频文件 → HRU
scp test.wav hru:/workspace/prod_hru/share/crb_resources/resources/voice_files_cn/
```

### 4. 调用技能

当机器人处于准备模式或运动模式时：

```bash
ros2 service call /casbot/event_service crb_ros_msg/srv/ActionEvent \
  '{"event_id":"","event_type":"ExecSkill","blocking":false,"param_json": "{\"payload\": \"{\\\"action_type\\\":\\\"test\\\"}\", \"target_tree\": \"basic_action_play\"}"}'
```

<!-- TODO: 补充 RViz 生成轨迹数据的详细教程 -->
