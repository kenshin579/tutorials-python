"""온도 센서 값을 구독해서 경고를 출력하는 노드."""

import rclpy
from rclpy.node import Node

from tutorial_interfaces.msg import SensorReading


class TemperatureSubscriber(Node):
    """/temperature 토픽을 구독하고 경고 메시지를 남긴다."""

    def __init__(self):
        super().__init__('temperature_subscriber')

        self.subscription = self.create_subscription(
            SensorReading,
            'temperature',
            self.on_reading,
            10,
        )
        self.received_count = 0

        self.get_logger().info('온도 구독 노드 시작')

    def on_reading(self, msg):
        self.received_count += 1

        if msg.is_warning:
            self.get_logger().warning(
                f'[{self.received_count}] 경고! {msg.sensor_id} 온도 {msg.celsius}도'
            )
        else:
            self.get_logger().info(
                f'[{self.received_count}] 정상 {msg.sensor_id} 온도 {msg.celsius}도'
            )


def main(args=None):
    rclpy.init(args=args)
    node = TemperatureSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
