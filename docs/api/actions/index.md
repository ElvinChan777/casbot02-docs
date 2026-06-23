# ROS2 Action Types API Reference

Package: `crb_ros_msg`

This page documents all custom ROS2 action types defined in the `crb_ros_msg` package. Actions are used for long-running operations such as motion playback, behavior tree execution, and timed sleeps. Each action consists of three parts: a **Goal** (request sent by the client), a **Result** (returned on completion), and **Feedback** (intermediate updates during execution).

---

## ActionPlay

Plays a named motion sequence or cancels a running motion. This is the primary high-level action for triggering robot movements by name, with support for cancellation and reinforcement-learning-based motions.

### Goal

| Field | Type | Description |
|---|---|---|
| `start_time` | float64 | Playback start time offset (seconds) |
| `action_name` | string | Name of the motion to play |
| `cancel_action_name` | string | Name of the motion to run when cancelling |
| `rl_name` | string | Name of the reinforcement learning policy |

### Result

| Field | Type | Description |
|---|---|---|
| `if_success` | bool | Whether the motion completed successfully |

### Feedback

| Field | Type | Description |
|---|---|---|
| `action_index` | uint64 | Current action step index |
| `exec_time` | float64 | Elapsed execution time (seconds) |
| `state` | int32 | Current playback state (see below) |

**State values:**

| Value | Description |
|---|---|
| `0` | Not playing (idle) |
| `1` | Loading motion file |
| `2` | Motion playing |
| `3` | Motion finished |
| `4` | Motion cancelled |
| `5` | Cancel finished |

### CLI Example

```bash
ros2 action send_goal /ActionPlay crb_ros_msg/action/ActionPlay \
  "{start_time: 0.0, action_name: 'wave', cancel_action_name: 'idle', rl_name: ''}"
```

---

## ActionPlayerReset

Resets the action player to its initial state. Use this to clear any stuck or residual playback state before starting a new motion sequence.

### Goal

| Field | Type | Description |
|---|---|---|
| `rset` | bool | Trigger the reset (set to `true`) |

### Result

| Field | Type | Description |
|---|---|---|
| `res` | bool | Whether the reset succeeded |

### Feedback

| Field | Type | Description |
|---|---|---|
| `state` | int32 | Current reset state (see below) |

**State values:**

| Value | Description |
|---|---|
| `0` | Not playing (idle) |
| `1` | Loading / resetting |

### CLI Example

```bash
ros2 action send_goal /ActionPlayerReset crb_ros_msg/action/ActionPlayerReset "{rset: true}"
```

---

## BasicActionPlay

Plays a built-in gesture by symbolic name. This is a simplified variant of `ActionPlay` for common social gestures -- no motion file loading or RL policy is required.

### Goal

| Field | Type | Description |
|---|---|---|
| `type` | string | Gesture type identifier (see below) |

**Supported gesture types:**

| Value | Description |
|---|---|
| `thumb_up` | Thumbs-up gesture |
| `wave_hand` | Waving hand |
| `heart_gesture` | Heart / love gesture |
| `congratulation_gesture` | Congratulations / celebration |
| `v_gesture` | Victory / peace sign |

### Result

| Field | Type | Description |
|---|---|---|
| `if_success` | bool | Whether the gesture completed successfully |

### Feedback

| Field | Type | Description |
|---|---|---|
| `state` | int32 | Current playback state (see below) |

**State values:**

| Value | Description |
|---|---|
| `0` | Not playing (idle) |
| `1` | Loading gesture |
| `2` | Gesture playing |
| `3` | Gesture finished |

### CLI Example

```bash
ros2 action send_goal /BasicActionPlay crb_ros_msg/action/BasicActionPlay "{type: 'wave_hand'}"
```

---

## ExecuteTree

Executes a named behavior tree. Behavior trees are used for high-level task planning and decision-making. The action returns the final tree status and an optional message payload.

### Goal

| Field | Type | Description |
|---|---|---|
| `target_tree` | string | Name of the behavior tree to execute |
| `payload` | string | Optional implementation-dependent payload |

### Result

| Field | Type | Description |
|---|---|---|
| `node_status` | NodeStatus | Final status of the tree root node |
| `return_message` | string | Result payload or error message |

**`node_status` enum values (from `NodeStatus.msg`):**

| Value | Constant | Description |
|---|---|---|
| `0` | `IDLE` | Tree has not started or was reset |
| `1` | `RUNNING` | Tree is still executing (should not appear in result) |
| `2` | `SUCCESS` | Tree completed successfully |
| `3` | `FAILURE` | Tree completed with failure |
| `4` | `SKIPPED` | Tree execution was skipped |

### Feedback

| Field | Type | Description |
|---|---|---|
| `message` | string | Customizable progress message from the tree executor |

### CLI Example

```bash
ros2 action send_goal /ExecuteTree crb_ros_msg/action/ExecuteTree \
  "{target_tree: 'pick_and_place', payload: ''}"
```

---

## LogOutData

Starts or stops robot data logging. Use this action to control runtime data collection for diagnostics, recording, or post-analysis.

### Goal

| Field | Type | Description |
|---|---|---|
| `start_log` | bool | `true` to start logging, `false` to stop |

### Result

| Field | Type | Description |
|---|---|---|
| `start_log_res` | bool | Whether the logging state change succeeded |

### Feedback

| Field | Type | Description |
|---|---|---|
| `state` | int32 | Current logging state (see below) |

**State values:**

| Value | Description |
|---|---|
| `0` | Not active |
| `1` | Initializing / loading |

### CLI Example

```bash
# Start logging
ros2 action send_goal /LogOutData crb_ros_msg/action/LogOutData "{start_log: true}"

# Stop logging
ros2 action send_goal /LogOutData crb_ros_msg/action/LogOutData "{start_log: false}"
```

---

## Sleep

Pauses execution for a specified duration. Useful for inserting delays in action sequences or behavior trees. The feedback reports the number of elapsed cycles.

### Goal

| Field | Type | Description |
|---|---|---|
| `msec_timeout` | int32 | Sleep duration in milliseconds |

### Result

| Field | Type | Description |
|---|---|---|
| `done` | bool | `true` when the sleep duration has elapsed |

### Feedback

| Field | Type | Description |
|---|---|---|
| `cycle` | int32 | Number of timer cycles elapsed so far |

### CLI Example

```bash
# Sleep for 3000 ms (3 seconds)
ros2 action send_goal /Sleep crb_ros_msg/action/Sleep "{msec_timeout: 3000}"
```
