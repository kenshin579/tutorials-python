"""발행 노드와 구독 노드를 한 번에 실행하는 가장 단순한 launch 파일."""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    talker = Node(
        package='py_pubsub',
        executable='talker',
        name='temperature_publisher',
        output='screen',
    )

    listener = Node(
        package='py_pubsub',
        executable='listener',
        name='temperature_subscriber',
        output='screen',
    )

    return LaunchDescription([talker, listener])
