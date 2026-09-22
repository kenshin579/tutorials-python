# PX4 SITL 설치

PX4 비행 시뮬레이션(SITL) 실습 환경을 한 번에 까는 스크립트다.
세미나/실습 전에 노트북에 미리 깔아두는 용도다.

- 대상: Ubuntu 24.04 (Jazzy) / 22.04 (Humble)
- 구성: PX4-Autopilot + Gazebo Harmonic + QGroundControl + ROS2 브리지(uXRCE-DDS)
- 디스크 20GB, 시간 30~60분 정도 잡아야 한다.

## 실행

```bash
cd ros2/setup
./install_px4.sh                  # 전부
./install_px4.sh --no-ros2        # PX4 + QGC 만
PX4_REF=v1.16.0 ./install_px4.sh  # 버전 고정
```

세미나에서 특정 PX4 버전을 지정했다면 `PX4_REF` 로 맞춰야 한다. 기본값은 `main` 이다.
`px4_msgs` 의 메시지 정의는 PX4 펌웨어 버전과 짝이 맞아야 하고, 어긋나면 ROS2 토픽이
안 보이거나 값이 깨진다.

## 설치되는 것

| 구성 요소 | 위치 | 용도 |
|---|---|---|
| PX4-Autopilot | `~/PX4-Autopilot` | 비행제어 펌웨어 소스 + SITL |
| Gazebo Harmonic | apt (OSRF 저장소) | 물리 시뮬레이터 |
| QGroundControl | `~/Applications/QGroundControl.AppImage` | 지상관제 GUI |
| Micro XRCE-DDS Agent | `/usr/local/bin/MicroXRCEAgent` | PX4 ↔ ROS2 브리지 데몬 |
| px4_msgs, px4_ros_com | `~/ws_px4_ros2` | ROS2 메시지 정의와 예제 |

## 실행 방법

### SITL + Gazebo

```bash
cd ~/PX4-Autopilot
make px4_sitl gz_x500
```

`pxh>` 프롬프트가 뜨고 Gazebo 에 X500 쿼드콥터가 보이면 성공이다.

```
pxh> commander takeoff
pxh> commander land
pxh> commander mode auto:mission
```

기체 모델을 바꾸려면 `gz_x500` 대신 `gz_rc_cessna`(고정익), `gz_standard_vtol`(VTOL),
`gz_r1_rover`(지상차) 등을 쓴다. 목록은 `make px4_sitl list_config_targets`.

### QGroundControl

```bash
~/Applications/QGroundControl.AppImage
```

SITL 이 떠 있으면 UDP 14550 으로 자동 연결된다. 지도에서 웨이포인트를 찍고
Upload 하면 미션 비행을 볼 수 있다.

### ROS2 연동

터미널 세 개가 필요하다.

```bash
# 터미널 1 - 브리지 데몬
MicroXRCEAgent udp4 -p 8888

# 터미널 2 - SITL (uXRCE-DDS 클라이언트가 자동으로 붙는다)
cd ~/PX4-Autopilot && make px4_sitl gz_x500

# 터미널 3 - ROS2
source /opt/ros/jazzy/setup.bash
source ~/ws_px4_ros2/install/setup.bash
ros2 topic list | grep fmu
ros2 topic echo /fmu/out/vehicle_status
```

터미널 1 에 `create_participant`, `create_topic` 로그가 쭉 올라오면 브리지가 붙은 것이다.
`/fmu/out/...` 토픽이 안 보이면 SITL 보다 Agent 를 먼저 띄웠는지 확인한다.

## 알아둘 것

**ROS2 Jazzy 는 PX4 공식 지원이 아니다.** PX4 문서는 Humble(22.04) 기준이고 Jazzy 탭이
없다. `px4_msgs` 빌드와 uXRCE-DDS 브리지는 실제로 동작하지만, 문제가 생기면 공식 문서에
답이 없을 수 있다. 세미나가 Humble 전제라면 Docker 로 분리하는 편이 낫다.

**Gazebo 가 두 벌이 될 수 있다.** TurtleBot3 쪽에서 `ros-jazzy-ros-gz` 를 이미 깔았다면
ROS 저장소 경로로 Harmonic 이 들어와 있고, PX4 의 `ubuntu.sh` 는 OSRF 저장소에서 `gz-harmonic`
을 깐다. 같은 Harmonic 이라 보통은 공존하지만 apt 충돌이 나면 아래를 본다.

```bash
apt policy gz-harmonic
sudo apt install -f
```

**dialout 그룹은 재로그인해야 적용된다.** 실기 연결(USB) 전에 한 번 로그아웃했다 들어와야
한다. SITL 만 쓸 거면 상관없다.

**QoS 설정이 다르다.** PX4 는 BEST_EFFORT 로 발행하는데 ROS2 구독 기본값은 RELIABLE 이다.
직접 노드를 짤 때 `rclpy.qos.qos_profile_sensor_data` 같은 걸 안 쓰면 메시지가 안 온다.
이게 PX4-ROS2 연동에서 제일 자주 걸리는 함정이다.

## 트러블슈팅

| 증상 | 해결 |
|---|---|
| `empy` 관련 빌드 에러 | `pip install --user -U --break-system-packages empy==3.3.4` |
| Gazebo 창이 안 뜸 / 검음 | Wayland 문제. 로그인 화면에서 Xorg 세션 선택 |
| `gz sim` 이 즉시 죽음 | `killall -9 gz ruby px4` 후 재시도 |
| QGC AppImage 실행 안 됨 | `sudo apt install libfuse2t64` (24.04) |
| `/fmu/out/*` 토픽 없음 | Agent 를 SITL 보다 먼저 띄운다. 포트 8888 확인 |
| 토픽은 보이는데 echo 가 빔 | QoS 불일치. `ros2 topic echo --qos-reliability best_effort <topic>` |

## 참고

- [PX4 Ubuntu 개발환경](https://docs.px4.io/main/en/dev_setup/dev_env_linux_ubuntu)
- [PX4 ROS 2 User Guide](https://docs.px4.io/main/en/ros2/user_guide)
- [uXRCE-DDS 브리지](https://docs.px4.io/main/en/middleware/uxrce_dds)
- [QGroundControl 설치](https://docs.qgroundcontrol.com/Stable_V5.1/en/qgc-user-guide/getting_started/download_and_install.html)
