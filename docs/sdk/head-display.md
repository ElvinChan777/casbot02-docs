# 头显通讯协议

CASBOT02 的面部显示模块通过 **UART + RS485 总线** 控制，支持 ASCII 字符显示和预设图片显示。

## 通信机制

| 属性 | 说明 |
|---|---|
| 通信模式 | 主从模式（Orin 发送指令，头显模块响应） |
| 物理接口 | UART + RS485 总线 |
| 数据格式 | 字节流传输，无校验位 |
| 指令长度 | 3 ~ 255 字节 |
| ROS2 Topic | `/rcu/mcu/serial_face` |
| 消息类型 | `std_msgs/msg/String` |

## 显示模式

| 模式 | 模式码 | 说明 |
|---|---|---|
| ASCII 字符显示 | `0x01` | 显示标准 ASCII 字符 |
| 预设图片显示 | `0x02` | 显示 MCU FLASH 中预存的图片 |

## 数据帧结构

所有指令帧遵循统一格式：

| 字节位置 | 字段 | 说明 |
|---|---|---|
| Byte 0 | `dev_id` | 设备 ID |
| Byte 1 | `disp_mode` | 显示模式 |
| Byte 2+ | 数据段 | 随模式变化 |

## Mode 1：ASCII 字符显示

### 结构体定义

```c
// 1字节对齐
typedef struct {
    uint8_t dev_id;     // 设备 ID, 0x00
    uint8_t disp_mode;  // 显示模式, 0x01
    uint8_t red;        // 字符颜色-红通道 (0~0xFF)
    uint8_t green;      // 字符颜色-绿通道 (0~0xFF)
    uint8_t blue;       // 字符颜色-蓝通道 (0~0xFF)
    uint8_t offset_x;   // 起始 X 坐标（左下角为原点）
    char str[];         // 可变长 ASCII 字符串（'\0' 结尾）
} s_Mode0Frame_t;
```

### 规格

| 属性 | 值 |
|---|---|
| 支持字符 | ASCII 32~112（空格 ~ 波浪号） |
| 字符点阵 | 8×13 像素（宽×高） |
| 字符间距 | 无额外间距，连续右移 8 像素 |
| 超出范围 | 自动截断 |

## Mode 2：预设图片显示

### 结构体定义

```c
// 1字节对齐
typedef struct {
    uint8_t dev_id;     // 设备 ID, 0x01
    uint8_t disp_mode;  // 显示模式, 0x02
    uint8_t index;      // 图片索引 (0=清屏, 1~BMP_NUM)
    uint8_t rev[3];     // 图片显示颜色 (red/green/blue)
} s_Mode1or2Frame_t;
```

### 规格

| 属性 | 值 |
|---|---|
| 图片格式 | 1-bit 单色位图 |
| 图片尺寸 | 112×13 像素 |
| 显示位置 | 固定左上角 (X=0, Y=0) |
| 清屏指令 | `index = 0` |

## 使用示例

### 显示 ASCII 字符串

显示 "Welcome to Uart"，X 坐标 0，颜色 0x0F0F0F：

```bash
ros2 topic pub /rcu/mcu/serial_face std_msgs/msg/String \
  "{data: '0100000F0F0F0000000057656C636F6D6520746F205561727400'}" --once
```

### 清屏

```bash
ros2 topic pub /rcu/mcu/serial_face std_msgs/msg/String \
  "{data: '01010000'}" --once
```

### 显示预设图片

显示图片索引 01，颜色红色 (0x0F0000)：

```bash
ros2 topic pub /rcu/mcu/serial_face std_msgs/msg/String \
  "{data: '0101010F00000000'}" --once
```

<!-- TODO: 补充预设图片枚举表 -->
