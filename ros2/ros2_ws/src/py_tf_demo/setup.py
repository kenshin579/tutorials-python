import os
from glob import glob

from setuptools import find_packages, setup

package_name = 'py_tf_demo'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*_launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Frank Oh',
    maintainer_email='kenshin579@gmail.com',
    description='ROS2 입문 시리즈 4편 - TF2 좌표 변환 예제',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'odom_broadcaster = py_tf_demo.odom_broadcaster:main',
            'laser_static_broadcaster = py_tf_demo.laser_static_broadcaster:main',
            'tf_listener = py_tf_demo.tf_listener:main',
        ],
    },
)
