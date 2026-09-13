"""로봇 몸체에 고정된 라이다 위치를 static TF로 한 번만 발행하는 노드."""

import math

import rclpy
from geometry_msgs.msg import TransformStamped
from rclpy.node import Node
from tf2_ros import StaticTransformBroadcaster


class LaserStaticBroadcaster(Node):
    """base_link -> laser 변환을 발행한다. 값이 변하지 않으므로 static 이다."""

    def __init__(self):
        super().__init__('laser_static_broadcaster')

        self.broadcaster = StaticTransformBroadcaster(self)

        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'base_link'
        t.child_frame_id = 'laser'

        # 로봇 중심에서 앞으로 20cm, 위로 30cm 지점에 라이다가 달려 있다
        t.transform.translation.x = 0.2
        t.transform.translation.y = 0.0
        t.transform.translation.z = 0.3
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = 0.0
        t.transform.rotation.w = 1.0

        self.broadcaster.sendTransform(t)
        self.get_logger().info('base_link -> laser static 변환 발행 완료')


def main(args=None):
    rclpy.init(args=args)
    node = LaserStaticBroadcaster()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
