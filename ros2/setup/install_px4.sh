#!/usr/bin/env bash
# PX4 SITL + Gazebo Harmonic + QGroundControl (+ ROS2 브리지) 설치 스크립트
#
# 사용법:
#   ./install_px4.sh                     # 전부 설치 (ROS2 브리지 포함)
#   ./install_px4.sh --no-ros2           # PX4 + QGC 만
#   PX4_REF=v1.16.0 ./install_px4.sh     # PX4 버전 고정 (세미나 지정 버전이 있으면 이렇게)
#
# 여러 번 실행해도 안전하다.

set -Eeuo pipefail

PX4_DIR="${HOME}/PX4-Autopilot"
PX4_REF="${PX4_REF:-main}"
ROS_WS="${HOME}/ws_px4_ros2"
AGENT_DIR="${HOME}/Micro-XRCE-DDS-Agent"
AGENT_REF="v2.4.2"
QGC_DIR="${HOME}/Applications"
LOG="${HOME}/px4_setup.log"
WITH_ROS2=1

for a in "$@"; do
  case "$a" in
    --no-ros2) WITH_ROS2=0 ;;
    -h|--help) sed -n '2,12p' "$0"; exit 0 ;;
    *) echo "알 수 없는 옵션: $a"; exit 1 ;;
  esac
done

c_i() { printf '\033[1;34m[%s]\033[0m %s\n' "$(date +%H:%M:%S)" "$*"; }
c_ok(){ printf '\033[1;32m  OK\033[0m %s\n' "$*"; }
c_w() { printf '\033[1;33m  !!\033[0m %s\n' "$*"; }
die() { printf '\033[1;31m[FAIL]\033[0m %s\n' "$*" >&2; exit 1; }

trap 'die "line $LINENO 에서 실패. 로그: $LOG"' ERR
exec > >(tee -a "$LOG") 2>&1
echo "================ $(date) ================"

# ---------- 0. 환경 점검 ----------
c_i "환경 점검"
[[ $EUID -ne 0 ]] || die "root 로 실행하지 마세요."
. /etc/os-release
CODENAME="${UBUNTU_CODENAME:-${VERSION_CODENAME:-}}"
case "$CODENAME" in
  noble|jammy) ;;
  *) die "지원하지 않는 배포판: ${PRETTY_NAME:-unknown} (24.04 / 22.04 만 지원)" ;;
esac

AVAIL_GB=$(df -BG --output=avail "$HOME" | tail -1 | tr -dc '0-9')
(( AVAIL_GB >= 20 )) || die "디스크 여유 ${AVAIL_GB}GB. PX4 빌드에 최소 20GB 필요."
c_ok "${PRETTY_NAME} / 디스크 ${AVAIL_GB}GB / PX4 ref=${PX4_REF}"

# Gazebo 중복 설치 경고 (TurtleBot3 용 ros_gz 가 이미 있을 수 있다)
if dpkg -l 2>/dev/null | grep -q "ros-.*-ros-gz"; then
  c_w "ros-*-ros-gz 가 이미 설치돼 있습니다."
  c_w "PX4 는 OSRF 저장소의 gz-harmonic 을 씁니다. 같은 Harmonic 이라 보통 공존하지만,"
  c_w "충돌이 나면 'sudo apt install -f' 또는 ros_gz 제거 후 재설치가 필요할 수 있습니다."
fi

c_i "sudo 권한 확인 (비밀번호는 한 번만)"
sudo -v
while true; do sudo -n true; sleep 50; kill -0 "$$" 2>/dev/null || exit; done 2>/dev/null &
SUDO_KEEPALIVE=$!
trap 'kill "$SUDO_KEEPALIVE" 2>/dev/null || true' EXIT

sudo apt-get update -qq
sudo apt-get install -y -qq git curl wget build-essential cmake python3-pip

# ---------- 1. PX4-Autopilot 소스 ----------
if [[ -d "${PX4_DIR}/.git" ]]; then
  c_i "PX4-Autopilot 이미 있음 — ${PX4_REF} 로 갱신"
  git -C "$PX4_DIR" fetch --all --tags --prune
  git -C "$PX4_DIR" checkout "$PX4_REF"
  git -C "$PX4_DIR" pull --ff-only 2>/dev/null || true
  git -C "$PX4_DIR" submodule update --init --recursive
else
  c_i "PX4-Autopilot 클론 (수 분, 약 3GB)"
  git clone https://github.com/PX4/PX4-Autopilot.git --recursive "$PX4_DIR"
  git -C "$PX4_DIR" checkout "$PX4_REF"
  git -C "$PX4_DIR" submodule update --init --recursive
fi
c_ok "$(git -C "$PX4_DIR" describe --tags --always)"

# ---------- 2. 의존성 설치 ----------
c_i "PX4 의존성 설치 (ubuntu.sh — 10분 이상 걸릴 수 있음)"
bash "${PX4_DIR}/Tools/setup/ubuntu.sh"
c_ok "ubuntu.sh 완료"

# empy 버전이 맞지 않으면 빌드가 깨진다
c_i "Python 의존성"
pip install --user -U --break-system-packages empy==3.3.4 pyros-genmsg setuptools >/dev/null 2>&1 \
  || pip install --user -U empy==3.3.4 pyros-genmsg setuptools >/dev/null 2>&1 \
  || c_w "pip 설치 실패 — 빌드 중 empy 오류가 나면 수동 설치 필요"
c_ok "empy 3.3.4"

# ---------- 3. SITL 빌드 ----------
c_i "PX4 SITL 빌드 (수 분)"
cd "$PX4_DIR"
make px4_sitl
c_ok "SITL 빌드 완료"

# ---------- 4. QGroundControl ----------
c_i "QGroundControl"
sudo usermod -aG dialout "$(id -un)"
sudo systemctl mask --now ModemManager.service >/dev/null 2>&1 || true
# 24.04 는 libfuse2t64, 22.04 는 libfuse2
for p in libfuse2t64 libfuse2; do
  sudo apt-get install -y -qq "$p" >/dev/null 2>&1 && break
done
sudo apt-get install -y -qq libxcb-xinerama0 libxkbcommon-x11-0 libxcb-cursor0 >/dev/null 2>&1 || true

mkdir -p "$QGC_DIR"
QGC_BIN="${QGC_DIR}/QGroundControl.AppImage"
if [[ -x "$QGC_BIN" ]]; then
  c_ok "QGroundControl 이미 있음 (${QGC_BIN})"
else
  ARCH_TAG="x86_64"; [[ "$(uname -m)" == "aarch64" ]] && ARCH_TAG="aarch64"
  if wget -q --show-progress -O "$QGC_BIN" \
      "https://d176tv9ibo4jno.cloudfront.net/latest/QGroundControl-${ARCH_TAG}.AppImage"; then
    chmod +x "$QGC_BIN"
    c_ok "QGroundControl 내려받음"
  else
    rm -f "$QGC_BIN"
    c_w "QGC 다운로드 실패 — https://qgroundcontrol.com 에서 직접 받으세요"
  fi
fi

# ---------- 5. ROS2 브리지 (선택) ----------
if (( WITH_ROS2 )); then
  if [[ -z "${ROS_DISTRO:-}" ]]; then
    for d in jazzy humble; do
      [[ -f "/opt/ros/$d/setup.bash" ]] && { ROS_DISTRO="$d"; break; }
    done
  fi
  if [[ -z "${ROS_DISTRO:-}" ]]; then
    c_w "ROS2 를 찾지 못해 브리지 설치를 건너뜁니다."
  else
    # shellcheck disable=SC1090
    source "/opt/ros/${ROS_DISTRO}/setup.bash"
    c_i "ROS2 ${ROS_DISTRO} 브리지 설치"

    # Micro XRCE-DDS Agent
    if command -v MicroXRCEAgent >/dev/null 2>&1; then
      c_ok "MicroXRCEAgent 이미 설치됨"
    else
      c_i "Micro-XRCE-DDS-Agent ${AGENT_REF} 빌드"
      [[ -d "${AGENT_DIR}/.git" ]] || git clone -b "$AGENT_REF" \
        https://github.com/eProsima/Micro-XRCE-DDS-Agent.git "$AGENT_DIR"
      mkdir -p "${AGENT_DIR}/build"
      cd "${AGENT_DIR}/build"
      cmake .. >/dev/null
      make -j"$(nproc)"
      sudo make install
      sudo ldconfig /usr/local/lib/
      c_ok "MicroXRCEAgent"
    fi

    # px4_msgs / px4_ros_com
    c_i "px4_msgs / px4_ros_com 빌드"
    mkdir -p "${ROS_WS}/src"
    cd "${ROS_WS}/src"
    for r in px4_msgs px4_ros_com; do
      if [[ -d "${r}/.git" ]]; then
        git -C "$r" pull --ff-only 2>/dev/null || c_w "$r 갱신 생략"
      else
        git clone "https://github.com/PX4/${r}.git"
      fi
    done
    cd "$ROS_WS"
    colcon build
    c_ok "ROS2 워크스페이스 ${ROS_WS}"
  fi
fi

# ---------- 6. 검증 ----------
c_i "검증"
[[ -f "${PX4_DIR}/build/px4_sitl_default/bin/px4" ]] || die "px4 바이너리가 없습니다."
command -v gz >/dev/null 2>&1 && c_ok "gz $(gz sim --versions 2>/dev/null | head -1)" || c_w "gz 명령 없음"
[[ -x "$QGC_BIN" ]] && c_ok "QGC AppImage" || c_w "QGC 없음"
if (( WITH_ROS2 )) && [[ -f "${ROS_WS}/install/setup.bash" ]]; then
  c_ok "px4_msgs / px4_ros_com 빌드됨"
fi

cat <<DONE

============================================================
 설치 완료
============================================================

[1] SITL + Gazebo 띄우기
      cd ${PX4_DIR}
      make px4_sitl gz_x500

    pxh> 프롬프트가 뜨고 Gazebo 에 쿼드콥터가 보이면 정상이다.
    이륙/착륙:
      pxh> commander takeoff
      pxh> commander land

[2] QGroundControl
      ${QGC_BIN}

    SITL 이 떠 있으면 자동으로 붙는다(UDP 14550).

[3] ROS2 브리지 (터미널 3개)
      MicroXRCEAgent udp4 -p 8888
      cd ${PX4_DIR} && make px4_sitl gz_x500
      source /opt/ros/\${ROS_DISTRO}/setup.bash
      source ${ROS_WS}/install/setup.bash
      ros2 topic list | grep fmu          # /fmu/out/... 토픽이 보여야 한다
      ros2 topic echo /fmu/out/vehicle_status

주의: dialout 그룹이 적용되려면 한 번 로그아웃했다 로그인해야 한다.

로그: ${LOG}
============================================================
DONE
