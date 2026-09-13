# ROS2 예제

블로그 시리즈 「ROS2 입문」의 실습 코드다.

- 환경: Ubuntu 24.04 + ROS2 Jazzy
- 워크스페이스: `ros2_ws/`

## 패키지

| 패키지 | 빌드 타입 | 내용 |
|---|---|---|
| `tutorial_interfaces` | ament_cmake | 커스텀 메시지 `SensorReading` 정의 |
| `py_pubsub` | ament_python | 온도 센서 publisher / subscriber 노드 (2편), launch·파라미터 파일 (3편) |

## 빌드

```bash
cd ros2_ws
source /opt/ros/jazzy/setup.bash
colcon build
source install/setup.bash
```

커스텀 메시지를 쓰는 패키지가 있어 `tutorial_interfaces`가 먼저 빌드된다.

## 실행

터미널 두 개를 열고 각각 실행한다. 두 터미널 모두 `source install/setup.bash`가 필요하다.

```bash
# 터미널 1 - 온도 발행
ros2 run py_pubsub talker

# 터미널 2 - 온도 구독
ros2 run py_pubsub listener
```

파라미터를 바꿔서 실행할 수도 있다.

```bash
ros2 run py_pubsub talker --ros-args -p sensor_id:=sensor-99 -p warning_threshold:=25.0
```

## launch 로 한 번에 실행 (3편)

```bash
# 발행/구독 노드 동시 실행
ros2 launch py_pubsub temperature_launch.py

# 파라미터 파일 + 네임스페이스 + launch 인자
ros2 launch py_pubsub temperature_params_launch.py
ros2 launch py_pubsub temperature_params_launch.py room:=bedroom
ros2 launch py_pubsub temperature_params_launch.py --show-args
```

`config/temperature_params.yaml` 의 키가 `/**/temperature_publisher` 인 이유는 노드가 네임스페이스
(`living_room`, `bedroom` 등) 안에서 실행되기 때문이다. 키가 실제 노드 이름과 맞지 않으면 파라미터는
경고 없이 무시된다.

## 확인용 명령어

```bash
ros2 topic echo /temperature --once          # 흐르는 메시지 보기
ros2 interface show tutorial_interfaces/msg/SensorReading
ros2 param list /temperature_publisher
ros2 node info /temperature_publisher
```

## 관련 글

- [ROS2 입문 1편 - 설치하고 turtlesim으로 핵심 개념 잡기](https://blog.advenoh.pe.kr/)
- [ROS2 입문 2편 - rclpy로 첫 노드 만들기](https://blog.advenoh.pe.kr/)
