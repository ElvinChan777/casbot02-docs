# 全身关节控制

## 调试模式

| 属性 | 值 |
|---|---|
| **通讯方式** | ROS2 Service |
| **Service 名称** | `/motion/whole_body_debug` |
| **Service 类型** | `std_srvs/srv/SetBool` |

```bash
# 申请进入全身调试模式
ros2 service call /motion/whole_body_debug std_srvs/srv/SetBool "{data: true}"

# 退出全身调试模式
ros2 service call /motion/whole_body_debug std_srvs/srv/SetBool "{data: false}"
```

!!! danger "全身调试模式"
    全身调试模式将接管所有关节的自主控制（包括下肢），请务必确保机器人处于安全环境（如吊装状态）。

## 控制接口

<!-- TODO: 补充全身关节控制的具体接口定义和代码示例 -->

全身关节控制包含头部、腰部、双臂、灵巧手、双腿所有关节。

<!-- TODO: 从飞书文档迁移完整内容 -->
