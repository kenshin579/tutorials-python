"""TF 브로드캐스터 둘과 리스너를 한 번에 실행한다."""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    odom_broadcaster = Node(
        package='py_tf_demo',
        executable='odom_broadcaster',
        name='odom_broadcaster',
        output='screen',
    )

    laser_broadcaster = Node(
        package='py_tf_demo',
        executable='laser_static_broadcaster',
        name='laser_static_broadcaster',
        output='screen',
    )

    listener = Node(
        package='py_tf_demo',
        executable='tf_listener',
        name='laser_pose_listener',
        output='screen',
    )

    return LaunchDescription([odom_broadcaster, laser_broadcaster, listener])
