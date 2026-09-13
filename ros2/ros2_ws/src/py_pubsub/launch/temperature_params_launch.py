"""파라미터 파일, 네임스페이스, 리맵핑, launch 인자를 함께 쓰는 launch 파일."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    config = os.path.join(
        get_package_share_directory('py_pubsub'),
        'config',
        'temperature_params.yaml',
    )

    # 실행할 때 값을 바꿀 수 있는 launch 인자
    room_arg = DeclareLaunchArgument(
        'room',
        default_value='living_room',
        description='센서를 배치할 방 이름 (네임스페이스로 쓰인다)',
    )
    room = LaunchConfiguration('room')

    talker = Node(
        package='py_pubsub',
        executable='talker',
        name='temperature_publisher',
        namespace=room,
        parameters=[config],
        output='screen',
    )

    listener = Node(
        package='py_pubsub',
        executable='listener',
        name='temperature_subscriber',
        namespace=room,
        output='screen',
    )

    # 같은 노드를 다른 네임스페이스로 하나 더 띄운다 (멀티 센서)
    kitchen_talker = Node(
        package='py_pubsub',
        executable='talker',
        name='temperature_publisher',
        namespace='kitchen',
        parameters=[{
            'sensor_id': 'kitchen-01',
            'publish_period': 2.0,
            'warning_threshold': 26.0,
        }],
        output='screen',
    )

    return LaunchDescription([room_arg, talker, listener, kitchen_talker])
