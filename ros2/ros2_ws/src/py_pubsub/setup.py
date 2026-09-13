from setuptools import find_packages, setup

package_name = 'py_pubsub'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Frank Oh',
    maintainer_email='kenshin579@gmail.com',
    description='ROS2 입문 시리즈 2편 - rclpy publisher/subscriber 예제',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'talker = py_pubsub.temperature_publisher:main',
            'listener = py_pubsub.temperature_subscriber:main',
        ],
    },
)
