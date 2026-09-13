"""로봇이 원을 그리며 도는 상황을 가정하고 odom -> base_link 변환을 발행하는 노드."""

import math

import rclpy
from geometry_msgs.msg import TransformStamped
from rclpy.node import Node
from tf2_ros import TransformBroadcaster


def yaw_to_quaternion(yaw):
    """평면 위 회전(yaw)만 있는 경우의 쿼터니언을 구한다."""
    return (0.0, 0.0, math.sin(yaw / 2.0), math.cos(yaw / 2.0))


class OdomBroadcaster(Node):
    """반지름 2m 원을 도는 로봇의 위치를 TF로 계속 알린다."""

    def __init__(self):
        super().__init__('odom_broadcaster')

        self.declare_parameter('radius', 2.0)
        self.declare_parameter('angular_speed', 0.5)  # rad/s

        self.broadcaster = TransformBroadcaster(self)
        self.angle = 0.0
        self.period = 0.05  # 20Hz
        self.timer = self.create_timer(self.period, self.broadcast_transform)

        self.get_logger().info('odom -> base_link 변환 발행 시작')

    def broadcast_transform(self):
        radius = self.get_parameter('radius').value
        speed = self.get_parameter('angular_speed').value
        self.angle += speed * self.period

        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'odom'        # 부모 프레임
        t.child_frame_id = 'base_link'    # 자식 프레임

        t.transform.translation.x = radius * math.cos(self.angle)
        t.transform.translation.y = radius * math.sin(self.angle)
        t.transform.translation.z = 0.0

        # 로봇은 진행 방향을 바라본다
        qx, qy, qz, qw = yaw_to_quaternion(self.angle + math.pi / 2.0)
        t.transform.rotation.x = qx
        t.transform.rotation.y = qy
        t.transform.rotation.z = qz
        t.transform.rotation.w = qw

        self.broadcaster.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)
    node = OdomBroadcaster()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
