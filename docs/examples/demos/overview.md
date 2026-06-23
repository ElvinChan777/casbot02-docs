# Examples 导航

为便于查找，`examples` 按用途分为 4 层。

## 1) 场景化操作指引

| 说明 | 路径 |
|------|------|
| 开机自检 | `scenarios/boot_check.md` |
| 仿真联调流程 | `scenarios/simulation.md` |
| 实机联调流程 | `scenarios/real_robot.md` |

## 2) 接口全覆盖示例

| 说明 | 路径 |
|------|------|
| 所有用法总览 | `interfaces/README.md` |
| 统一命令行调用工具 | `interfaces/python/all_interfaces_demo.py` |

## 3) 自动化 Workflow 测试

| 语言 | 路径 | 说明 |
|------|------|------|
| Python | `workflows/python/casbot_py_test/` | t01 ~ t05 + test_flow |
| C++ | `workflows/cpp/casbot_cpp_test/` | t01 ~ t05 |

## 4) 基础 Demo 包

基础 Demo 包位于以下目录：

- C++：`cpp/casbot2_cpp_demo/`
- Python：`python/casbot2_py_demo/`

### Demo 入口一览

=== "C++"

    | 入口 |
    |------|
    | `basic_control_demo` |
    | `service_mode_demo` |
    | `debug_joint_demo` |
    | `monitor_topics_demo` |
    | `action_voice_demo` |

=== "Python"

    | 入口 |
    |------|
    | `control_demo` |
    | `service_mode_demo` |
    | `debug_joint_demo` |
    | `monitor_topics_demo` |
    | `action_voice_demo` |
