"""odom 기준으로 라이다가 지금 어디에 있는지 주기적으로 조회하는 노드."""

import math

import rclpy
from rclpy.node import Node
from tf2_ros import LookupException, ConnectivityException, ExtrapolationException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener


class LaserPoseListener(Node):
    """odom -> laser 변환을 조회해서 라이다의 절대 위치를 출력한다."""

    def __init__(self):
        super().__init__('laser_pose_listener')

        # reference_frame: 어느 좌표계 기준으로 볼 것인가
        # child_frame: 위치를 알고 싶은 대상
        self.declare_parameter('reference_frame', 'odom')
        self.declare_parameter('child_frame', 'laser')

        self.buffer = Buffer()
        self.listener = TransformListener(self.buffer, self)
        self.timer = self.create_timer(1.0, self.lookup_pose)

    def lookup_pose(self):
        reference = self.get_parameter('reference_frame').value
        child = self.get_parameter('child_frame').value

        try:
            # 첫 인자가 기준 좌표계, 두 번째가 대상이다
            # rclpy.time.Time() 은 "가장 최근 값" 을 뜻한다
            tf = self.buffer.lookup_transform(reference, child, rclpy.time.Time())
        except (LookupException, ConnectivityException, ExtrapolationException) as e:
            self.get_logger().warning(f'{reference} -> {child} 변환을 아직 찾을 수 없다: {e}')
            return

        x = tf.transform.translation.x
        y = tf.transform.translation.y
        z = tf.transform.translation.z
        distance = math.sqrt(x * x + y * y)

        self.get_logger().info(
            f'{child} 위치: x={x:.2f} y={y:.2f} z={z:.2f} '
            f'({reference} 원점에서 {distance:.2f}m)'
        )


def main(args=None):
    rclpy.init(args=args)
    node = LaserPoseListener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
