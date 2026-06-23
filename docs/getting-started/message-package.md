# 自定义消息包

本仓库已内置 CASBOT2 使用的自定义消息包 `crb_ros_msg`，覆盖 `msg` / `srv` / `action` 三种接口类型。

## 目录结构

`packages/crb_ros_msg` 主要内容：

- `msg/`：自定义消息（如 `UpperJointData.msg`、`RobotState.msg`）
- `srv/`：服务接口（如 `GetRobotMode.srv`、`SetRobotMode.srv`、`Voice.srv`）
- `action/`：动作接口（如 `BasicActionPlay.action`、`VoicePlay` 对应动作）
- `CMakeLists.txt`：`rosidl_generate_interfaces(...)` 生成入口
- `package.xml`：依赖声明（`rosidl_default_generators`、`std_msgs`、`sensor_msgs`）

## 编译消息包 { #building }

在 SDK 仓库根目录执行：

```bash
source /opt/ros/humble/setup.bash
colcon build --packages-select crb_ros_msg
source install/setup.bash
```

!!! tip "验证编译结果"

    编译完成后，可用以下命令确认接口已正确生成：

    ```bash
    ros2 interface list | grep crb_ros_msg
    ros2 interface show crb_ros_msg/msg/UpperJointData
    ros2 interface show crb_ros_msg/srv/GetRobotMode
    ros2 interface show crb_ros_msg/action/BasicActionPlay
    ```

## 在代码中使用

在你的包的 `package.xml` 中声明依赖：

```xml
<depend>crb_ros_msg</depend>
```

然后根据开发语言导入对应的接口类型。

=== "Python"

    ```python
    from crb_ros_msg.msg import JointStateData
    from crb_ros_msg.srv import GetRobotMode
    from crb_ros_msg.action import BasicActionPlay
    ```

=== "C++"

    `CMakeLists.txt` 中需要添加：

    ```cmake
    find_package(crb_ros_msg REQUIRED)
    ament_target_dependencies(your_target crb_ros_msg)
    ```

    头文件引用：

    ```cpp
    #include "crb_ros_msg/msg/joint_state_data.hpp"
    #include "crb_ros_msg/srv/get_robot_mode.hpp"
    #include "crb_ros_msg/action/basic_action_play.hpp"
    ```

## 常见问题

??? question "Python 报错 `ModuleNotFoundError: crb_ros_msg`"

    未执行 `source install/setup.bash`，或 `crb_ros_msg` 未编译成功。请回到[编译消息包](#building)一节重新操作。

??? question "C++ 找不到头文件"

    检查 `CMakeLists.txt` 中是否已添加 `find_package(crb_ros_msg REQUIRED)` 和 `ament_target_dependencies(...)`。

??? question "`ros2 interface show` 查不到接口"

    当前终端环境未 source 正确的工作区，或消息包编译失败。请确认已执行 `source install/setup.bash`。
