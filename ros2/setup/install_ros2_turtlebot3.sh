#!/usr/bin/env bash
# ROS 2 + TurtleBot3(Gazebo) 원샷 설치 스크립트
# 사용법:  chmod +x ros2_turtlebot3_setup.sh && ./ros2_turtlebot3_setup.sh
# 여러 번 실행해도 안전합니다(idempotent).

set -Eeuo pipefail

WS="${HOME}/turtlebot3_ws"
LOG="${HOME}/ros2_setup.log"

c_i() { printf '\033[1;34m[%s]\033[0m %s\n' "$(date +%H:%M:%S)" "$*"; }
c_ok(){ printf '\033[1;32m  OK\033[0m %s\n' "$*"; }
c_w() { printf '\033[1;33m  !!\033[0m %s\n' "$*"; }
die() { printf '\033[1;31m[FAIL]\033[0m %s\n' "$*" >&2; exit 1; }

trap 'die "line $LINENO 에서 실패했습니다. 로그: $LOG"' ERR
exec > >(tee -a "$LOG") 2>&1

echo "================ $(date) ================"

# ---------- 0. 환경 점검 ----------
c_i "환경 점검"
[[ "$(uname -s)" == "Linux" ]] || die "Linux 전용 스크립트입니다."
[[ $EUID -ne 0 ]] || die "root로 실행하지 마세요. 일반 사용자로 실행하면 필요할 때 sudo를 씁니다."

. /etc/os-release
CODENAME="${UBUNTU_CODENAME:-${VERSION_CODENAME:-}}"
case "$CODENAME" in
  noble)  ROS_DISTRO=jazzy  ;;   # Ubuntu 24.04
  jammy)  ROS_DISTRO=humble ;;   # Ubuntu 22.04
  *) die "지원하지 않는 배포판입니다: ${PRETTY_NAME:-unknown} (noble/jammy만 지원). Docker 사용을 권장합니다." ;;
esac
c_ok "${PRETTY_NAME}  ->  ROS 2 ${ROS_DISTRO}"

ARCH="$(dpkg --print-architecture)"
[[ "$ARCH" == "amd64" || "$ARCH" == "arm64" ]] || die "지원하지 않는 아키텍처: $ARCH"

# 디스크 여유 공간 (넉넉히 10GB 권장)
AVAIL_GB=$(df -BG --output=avail "$HOME" | tail -1 | tr -dc '0-9')
(( AVAIL_GB >= 8 )) || die "디스크 여유 공간이 ${AVAIL_GB}GB 뿐입니다. 최소 8GB 필요."
c_ok "디스크 여유 ${AVAIL_GB}GB"

c_i "sudo 권한 확인 (비밀번호를 한 번만 입력하면 끝까지 진행됩니다)"
sudo -v
# 설치가 오래 걸리므로 sudo 타임아웃 갱신을 백그라운드로 유지
while true; do sudo -n true; sleep 50; kill -0 "$$" 2>/dev/null || exit; done 2>/dev/null &
SUDO_KEEPALIVE=$!
trap 'kill "$SUDO_KEEPALIVE" 2>/dev/null || true' EXIT

# ---------- 1. 로케일 ----------
c_i "로케일 설정"
sudo apt-get update -qq
sudo apt-get install -y -qq locales curl gnupg lsb-release software-properties-common
sudo locale-gen en_US en_US.UTF-8 >/dev/null
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
c_ok "en_US.UTF-8"

# ---------- 2. apt 저장소 ----------
if [[ -f /etc/apt/sources.list.d/ros2.sources || -f /etc/apt/sources.list.d/ros2.list ]]; then
  c_ok "ROS 2 apt 저장소 이미 등록됨"
else
  c_i "ROS 2 apt 저장소 등록 (ros2-apt-source .deb 방식)"
  sudo add-apt-repository -y universe >/dev/null
  RAS_VER="$(curl -fsSL https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest \
              | grep -F '"tag_name"' | awk -F'"' '{print $4}')"
  [[ -n "$RAS_VER" ]] || die "ros-apt-source 최신 버전을 가져오지 못했습니다. 네트워크를 확인하세요."
  curl -fsSL -o /tmp/ros2-apt-source.deb \
    "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${RAS_VER}/ros2-apt-source_${RAS_VER}.${CODENAME}_all.deb"
  sudo dpkg -i /tmp/ros2-apt-source.deb
  rm -f /tmp/ros2-apt-source.deb
  c_ok "ros-apt-source ${RAS_VER}"
fi

sudo apt-get update -qq

# ---------- 3. ROS 2 본체 ----------
if [[ -f "/opt/ros/${ROS_DISTRO}/setup.bash" ]]; then
  c_ok "ROS 2 ${ROS_DISTRO} 이미 설치됨"
else
  c_i "ROS 2 ${ROS_DISTRO} desktop 설치 (수 분 소요)"
  sudo apt-get install -y ros-${ROS_DISTRO}-desktop ros-dev-tools
  c_ok "ros-${ROS_DISTRO}-desktop"
fi

# shellcheck disable=SC1090
source "/opt/ros/${ROS_DISTRO}/setup.bash"

# ---------- 4. TurtleBot3 의존 패키지 ----------
c_i "TurtleBot3 / Gazebo 패키지 설치"
PKGS=(
  ros-${ROS_DISTRO}-turtlebot3
  ros-${ROS_DISTRO}-turtlebot3-msgs
  ros-${ROS_DISTRO}-dynamixel-sdk
  ros-${ROS_DISTRO}-nav2-bringup
  ros-${ROS_DISTRO}-cartographer-ros
  python3-colcon-common-extensions
  python3-rosdep
  git
)
if [[ "$ROS_DISTRO" == "jazzy" ]]; then
  PKGS+=( ros-jazzy-ros-gz )                     # Gazebo Harmonic
else
  PKGS+=( ros-humble-gazebo-ros-pkgs )           # Gazebo Classic
fi

# 배포판마다 apt 에 없는 패키지가 있다(예: Jazzy 의 cartographer_ros).
# 하나가 없다고 전체가 죽으면 안 되므로 개별 설치하고 실패는 모아서 보고한다.
INSTALLED=0; SKIPPED=0; FAILED_PKGS=()
for p in "${PKGS[@]}"; do
  if dpkg -s "$p" >/dev/null 2>&1; then
    SKIPPED=$((SKIPPED+1)); continue
  fi
  if sudo apt-get install -y -qq "$p" >/dev/null 2>&1; then
    INSTALLED=$((INSTALLED+1))
  else
    FAILED_PKGS+=("$p")
  fi
done
c_ok "설치 ${INSTALLED} / 기존 ${SKIPPED} / 실패 ${#FAILED_PKGS[@]}"
if (( ${#FAILED_PKGS[@]} )); then
  c_w "apt 에서 찾지 못한 패키지: ${FAILED_PKGS[*]}"
  c_w "시뮬레이션 실행에는 대부분 지장 없다. 계속 진행한다."
fi

# 시뮬레이션에 반드시 필요한 것만 별도로 확인한다.
for p in ros-${ROS_DISTRO}-turtlebot3-msgs; do
  dpkg -s "$p" >/dev/null 2>&1 || die "필수 패키지 $p 설치 실패. apt 저장소 상태를 확인하세요."
done

# ---------- 5. rosdep ----------
c_i "rosdep 초기화"
[[ -f /etc/ros/rosdep/sources.list.d/20-default.list ]] || sudo rosdep init >/dev/null 2>&1 || true
rosdep update --rosdistro "$ROS_DISTRO" >/dev/null 2>&1 || c_w "rosdep update 실패 (계속 진행)"
c_ok "rosdep"

# ---------- 6. 워크스페이스 ----------
c_i "워크스페이스 ${WS}"
mkdir -p "${WS}/src"
cd "${WS}/src"
if [[ -d turtlebot3_simulations/.git ]]; then
  git -C turtlebot3_simulations fetch --depth 1 origin "$ROS_DISTRO"
  git -C turtlebot3_simulations reset --hard FETCH_HEAD
  c_ok "turtlebot3_simulations 갱신"
else
  git clone --depth 1 -b "$ROS_DISTRO" https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git
  c_ok "turtlebot3_simulations 클론"
fi

cd "$WS"
rosdep install --from-paths src --ignore-src -r -y >/dev/null 2>&1 || c_w "rosdep install 일부 실패 (계속 진행)"

c_i "colcon build (수 분 소요)"
colcon build --symlink-install
c_ok "빌드 완료"

# ---------- 7. 환경변수 ----------
c_i "~/.bashrc 설정"
add_line() {
  grep -qxF "$1" "${HOME}/.bashrc" || echo "$1" >> "${HOME}/.bashrc"
}
add_line "# --- ROS 2 (added by ros2_turtlebot3_setup.sh) ---"
add_line "source /opt/ros/${ROS_DISTRO}/setup.bash"
add_line "source ${WS}/install/setup.bash"
add_line "export TURTLEBOT3_MODEL=burger"
add_line "export ROS_DOMAIN_ID=30"
c_ok ".bashrc 갱신"

# ---------- 8. 검증 ----------
c_i "설치 검증"
# shellcheck disable=SC1090
source "${WS}/install/setup.bash"
export TURTLEBOT3_MODEL=burger

command -v ros2 >/dev/null || die "ros2 명령을 찾을 수 없습니다."
ros2 pkg list | grep -qx turtlebot3_gazebo || die "turtlebot3_gazebo 패키지가 없습니다."
ros2 pkg list | grep -qx turtlebot3_teleop || c_w "turtlebot3_teleop 없음"
c_ok "ROS 2 ${ROS_DISTRO} / $(ros2 pkg list | wc -l) packages"

# talker/listener 통신 테스트 (10초)
c_i "pub/sub 통신 테스트"
( ros2 run demo_nodes_cpp talker >/dev/null 2>&1 & echo $! > /tmp/.tb3_talker.pid )
sleep 3
if timeout 8 ros2 topic echo /chatter --once >/dev/null 2>&1; then
  c_ok "DDS 통신 정상"
else
  c_w "통신 테스트 실패 — 방화벽 또는 ROS_DOMAIN_ID 충돌 가능성"
fi
kill "$(cat /tmp/.tb3_talker.pid)" 2>/dev/null || true
rm -f /tmp/.tb3_talker.pid

cat <<'DONE'

============================================================
 설치 완료
============================================================

새 터미널을 열고 (또는 `source ~/.bashrc`) 아래를 실행하세요.

  터미널 A — 시뮬레이터
      ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py

  터미널 B — 키보드 조종  (w/x 전후, a/d 회전, s 정지)
      ros2 run turtlebot3_teleop teleop_keyboard

  터미널 C — 시각화 (선택)
      rviz2

모델 변경:  export TURTLEBOT3_MODEL=waffle      (burger | waffle | waffle_pi)
다른 월드:  empty_world.launch.py / turtlebot3_house.launch.py

첫 실행은 Gazebo Fuel에서 모델을 받느라 1~2분 멈춰 있을 수 있습니다. 정상입니다.

로그: ~/ros2_setup.log
============================================================
DONE
