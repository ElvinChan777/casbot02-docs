"""自动生成 API 参考页面（可选）"""
import mkdocs_gen_files

# 此脚本可在后续接入 Doxygen / mkdocstrings-cpp 时扩展
# 当前为空占位，不影响构建

# TODO: 接入 crb_ros_msg 的消息定义自动生成
# 示例：
# import subprocess
# result = subprocess.run(
#     ["ros2", "interface", "package", "crb_ros_msg"],
#     capture_output=True, text=True
# )
# for interface in result.stdout.strip().split("\n"):
#     ... 生成对应 Markdown 页面
