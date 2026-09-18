# ROS2 + TurtleBot3 설치

ROS2 설치부터 TurtleBot3 Gazebo 시뮬레이션 실행까지 한 번에 처리하는 스크립트다.
새 장비에 환경을 다시 깔 때 이 폴더만 있으면 된다.

- 대상: Ubuntu 24.04 (Jazzy) / Ubuntu 22.04 (Humble) 자동 판별
- 시뮬레이터: Gazebo Harmonic (Jazzy) / Gazebo Classic (Humble)
- 여러 번 실행해도 안전하다. 이미 깔린 단계는 건너뛴다.

## 실행

```bash
cd setup
./install_ros2_turtlebot3.sh
```

`sudo` 비밀번호를 처음에 한 번만 물어보고, 그 뒤로는 끝까지 자동으로 진행된다.
전체 로그는 `~/ros2_setup.log` 에 남는다.

## 스크립트가 하는 일

| 단계 | 내용 |
|---|---|
| 0 | OS 코드네임으로 ROS 배포판 결정, 아키텍처·디스크 여유(8GB) 확인 |
| 1 | 로케일 `en_US.UTF-8` 설정 |
| 2 | `ros2-apt-source` .deb 방식으로 apt 저장소 등록 |
| 3 | `ros-<distro>-desktop` + `ros-dev-tools` 설치 |
| 4 | turtlebot3, nav2, cartographer, ros_gz 등 패키지 설치 |
| 5 | `rosdep init` / `rosdep update` |
| 6 | `~/turtlebot3_ws` 에 `turtlebot3_simulations` 클론 후 `colcon build` |
| 7 | `~/.bashrc` 에 source 구문과 환경변수 추가 |
| 8 | 패키지 존재 확인 + talker/listener 로 DDS 통신 검증 |

`~/.bashrc` 에 추가되는 줄은 아래 네 개다. 중복 추가되지 않는다.

```bash
source /opt/ros/jazzy/setup.bash
source ~/turtlebot3_ws/install/setup.bash
export TURTLEBOT3_MODEL=burger
export ROS_DOMAIN_ID=30
```

TurtleBot3 워크스페이스를 `~/turtlebot3_ws` 로 따로 둔 이유는 `turtlebot3_simulations` 가
외부 저장소라 이 repo 의 `ros2_ws` 와 섞으면 안 되기 때문이다.

## 설치 후 실행

새 터미널을 열거나 `source ~/.bashrc` 한 뒤,

```bash
# 터미널 1 - 시뮬레이터
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py

# 터미널 2 - 키보드 조종 (w/x 전후, a/d 회전, s 정지)
ros2 run turtlebot3_teleop teleop_keyboard

# 터미널 3 - 시각화 (선택)
rviz2
```

모델은 `burger`(LDS만), `waffle`(+카메라), `waffle_pi` 중에 고른다.

```bash
export TURTLEBOT3_MODEL=waffle
```

월드는 `turtlebot3_world.launch.py` 외에 `empty_world.launch.py`,
`turtlebot3_house.launch.py` 가 있다.

## 확인용 명령어

```bash
ros2 topic list                      # /cmd_vel, /odom, /scan 이 보여야 한다
ros2 topic echo /cmd_vel             # teleop 이 실제로 발행하는지
ros2 topic hz /scan                  # LiDAR 주기 (burger 기준 약 5Hz)
ros2 node list
```

## 자주 걸리는 부분

| 증상 | 원인 / 해결 |
|---|---|
| 첫 실행이 1~2분 멈춤 | Gazebo Fuel 에서 모델 내려받는 중이다. 정상이다. |
| Gazebo 창이 검게만 뜸 | 하이브리드 그래픽 문제. `export LIBGL_ALWAYS_SOFTWARE=1` 로 확인 후 NVIDIA 면 `sudo prime-select nvidia` |
| teleop 을 눌러도 안 움직임 | 터미널 포커스가 teleop 창에 있어야 한다. `ros2 topic echo /cmd_vel` 로 발행 여부 확인 |
| 다른 PC 의 토픽이 섞임 | `ROS_DOMAIN_ID` 를 서로 다르게 (0~101) |
| `ros2` 명령을 못 찾음 | 새 터미널마다 source 필요. `.bashrc` 에 들어갔는지 확인 |
| `rosdep` 실패 | `sudo rosdep init && rosdep update` 수동 실행 후 스크립트 재실행 |

## 참고

- [ROS 2 Jazzy - Ubuntu Debian 설치](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html)
- [ROBOTIS e-Manual - TurtleBot3 Simulation](https://emanual.robotis.com/docs/en/platform/turtlebot3/simulation/)
