"""온도 센서 값을 주기적으로 발행하는 노드."""

import random

import rclpy
from rclpy.node import Node

from tutorial_interfaces.msg import SensorReading


class TemperaturePublisher(Node):
    """가짜 온도 센서 값을 /temperature 토픽으로 발행한다."""

    def __init__(self):
        super().__init__('temperature_publisher')

        # 파라미터 선언 (실행 중에도 바꿀 수 있는 설정값)
        self.declare_parameter('sensor_id', 'sensor-01')
        self.declare_parameter('publish_period', 1.0)
        self.declare_parameter('warning_threshold', 30.0)

        self.publisher_ = self.create_publisher(SensorReading, 'temperature', 10)

        period = self.get_parameter('publish_period').value
        self.timer = self.create_timer(period, self.publish_reading)

        self.get_logger().info(f'온도 센서 노드 시작 (주기 {period}초)')

    def publish_reading(self):
        celsius = round(random.uniform(20.0, 35.0), 2)
        threshold = self.get_parameter('warning_threshold').value

        msg = SensorReading()
        msg.sensor_id = self.get_parameter('sensor_id').value
        msg.celsius = celsius
        msg.is_warning = celsius > threshold

        self.publisher_.publish(msg)
        self.get_logger().info(f'발행: {msg.sensor_id} {msg.celsius}도 (경고: {msg.is_warning})')


def main(args=None):
    rclpy.init(args=args)
    node = TemperaturePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
