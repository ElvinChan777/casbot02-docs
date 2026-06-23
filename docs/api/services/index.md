# Services API Reference

ROS 2 service definitions for the `crb_ros_msg` package. Services provide a
request/response interface for one-shot operations such as querying robot state,
switching modes, triggering actions, and voice interaction.

All service types live in the `crb_ros_msg/srv` namespace.

---

## ActionEvent

Triggers a robot action event through the finite-state machine and optionally
blocks until the action completes.

**CLI example**

```bash
ros2 service call /action_event crb_ros_msg/srv/ActionEvent \
  "{event_id: 'evt_001', event_type: 'WAVE_HAND', blocking: true, param_json: '{}'}"
```

### Request

| Field | Type | Description |
|---|---|---|
| `event_id` | `string` | Unique identifier used for tracing and querying the event state |
| `event_type` | `string` | Name of the action to trigger (enum value) |
| `blocking` | `bool` | If `true`, the call blocks until the action finishes |
| `param_json` | `string` | JSON-encoded parameters for the action; may be empty |

### Response

| Field | Type | Description |
|---|---|---|
| `error_code` | `int32` | `0` on success, non-zero on failure |
| `current_state` | `string` | Current FSM state after the event |
| `source_event_id` | `string` | Event ID that is currently executing |
| `msg` | `string` | Human-readable error description |

---

## GetRobotMode

Queries the current robot operating mode. The request is empty.

**CLI example**

```bash
ros2 service call /get_robot_mode crb_ros_msg/srv/GetRobotMode
```

### Request

This service takes no request fields.

### Response

| Field | Type | Description |
|---|---|---|
| `mode` | `int32` | Numeric mode identifier (see [SwitchMode](#switchmode) for the enum) |
| `mode_name` | `string` | Human-readable mode name |

---

## GetRobotState

Starts or queries the robot state monitor.

**CLI example**

```bash
ros2 service call /get_robot_state crb_ros_msg/srv/GetRobotState "{start: true}"
```

### Request

| Field | Type | Description |
|---|---|---|
| `start` | `bool` | Whether to start the state monitor |

### Response

| Field | Type | Description |
|---|---|---|
| `state` | `uint8` | Current robot state code |

---

## SetRobotMode

Sets the robot to a specific operating mode by name.

**CLI example**

```bash
ros2 service call /set_robot_mode crb_ros_msg/srv/SetRobotMode "{mode_name: 'STAND'}"
```

### Request

| Field | Type | Description |
|---|---|---|
| `mode_name` | `string` | Target mode name. Valid values: `ZERO`, `STAND`, `WALK`, `TREAD` |

### Response

| Field | Type | Description |
|---|---|---|
| `success` | `bool` | `true` if the mode was set successfully |

---

## SwitchMode

Switches the robot operating mode with fine-grained control over upper and
lower body participation.

**Mode type enum**

| Value | Name | Description |
|---|---|---|
| 0 | `UNDEFINED` | Undefined / default |
| 1 | `DAMPING` | Damping mode |
| 2 | `READY` | Ready mode |
| 3 | `SPORT` | Sport / active mode |
| 4 | `ACTION_PLAY` | Action playback |
| 5 | `TELEOPERATION` | Teleoperation |
| 6 | `DEBUG` | Debug mode |

**CLI example**

```bash
ros2 service call /switch_mode crb_ros_msg/srv/SwitchMode \
  "{mode_type: 2, mode_name: 'READY', upper_body: true, lower_body: true}"
```

### Request

| Field | Type | Description |
|---|---|---|
| `mode_type` | `int32` | Numeric mode type from the enum above |
| `mode_name` | `string` | Human-readable mode name |
| `upper_body` | `bool` | Apply mode to upper body |
| `lower_body` | `bool` | Apply mode to lower body |

### Response

| Field | Type | Description |
|---|---|---|
| `success` | `bool` | `true` if the mode switch succeeded |
| `message` | `string` | Informational message (e.g. error details) |

---

## Voice

Sends voice-related commands for real-time communication, Q&A, and content
delivery.

**CLI example**

```bash
ros2 service call /voice crb_ros_msg/srv/Voice \
  "{type: 'question', content_type: 'text', content: 'What is the battery level?'}"
```

### Request

| Field | Type | Description |
|---|---|---|
| `type` | `string` | Command type: `rtc_start`, `rtc_stop`, `question`, `answer` |
| `content_type` | `string` | Content format: `text`, `object_string` |
| `content` | `string` | Payload text or JSON-encoded object |

### Response

| Field | Type | Description |
|---|---|---|
| `success` | `bool` | `true` if the voice command was processed successfully |
| `msg` | `string` | Human-readable error description |
