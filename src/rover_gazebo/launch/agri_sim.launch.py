import os

from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    # =========================================================
    # Package paths
    # =========================================================

    pkg_rover_gazebo = get_package_share_directory('rover_gazebo')

    world_file = os.path.join(
        pkg_rover_gazebo,
        'worlds',
        'agri_world.sdf'
    )

    rover_model = os.path.join(
        pkg_rover_gazebo,
        'models',
        'wave_rover',
        'model.sdf'
    )

    # =========================================================
    # Gazebo environment
    # =========================================================

    gz_config_path = os.environ.get('GZ_CONFIG_PATH', '')

    if gz_config_path:
        gz_config_path = '/usr/share/gz:' + gz_config_path
    else:
        gz_config_path = '/usr/share/gz'

    gz_resource_path = os.environ.get(
        'GZ_SIM_RESOURCE_PATH',
        ''
    )

    models_path = os.path.join(
        pkg_rover_gazebo,
        'models'
    )

    if gz_resource_path:
        gz_resource_path = models_path + ':' + gz_resource_path
    else:
        gz_resource_path = models_path

    gazebo_environment = os.environ.copy()

    gazebo_environment['GZ_CONFIG_PATH'] = gz_config_path
    gazebo_environment['GZ_SIM_RESOURCE_PATH'] = gz_resource_path

    # =========================================================
    # Start Gazebo
    # =========================================================

    gazebo = ExecuteProcess(
        cmd=[
            'gz',
            'sim',
            '-r',
            world_file
        ],
        output='screen',
        additional_env=gazebo_environment
    )

    # =========================================================
    # Spawn rover
    # =========================================================

    spawn_rover = TimerAction(
        period=3.0,
        actions=[
            ExecuteProcess(
                cmd=[
                    'gz',
                    'service',
                    '-s',
                    '/world/agri_world/create',
                    '--reqtype',
                    'gz.msgs.EntityFactory',
                    '--reptype',
                    'gz.msgs.Boolean',
                    '--timeout',
                    '1000',
                    '--req',
                    'sdf_filename: "' + rover_model +
                    '", name: "wave_rover", '
                    'pose: {position: {x: -8, y: -8, z: 0.10}, '
                    'orientation: {x: 0, y: 0, z: 0, w: 1}}'
                ],
                output='screen',
                additional_env=gazebo_environment
            )
        ]
    )

    # =========================================================
    # Gazebo -> ROS LiDAR bridge
    # =========================================================

    lidar_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan'
        ],
        output='screen'
    )

    # =========================================================
    # Gazebo -> ROS rover TF bridge
    # =========================================================

    tf_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/model/wave_rover/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V'
        ],
        output='screen'
    )

    # =========================================================
    # Static transform:
    # base_link -> LiDAR
    # =========================================================

    lidar_static_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=[
            '--x', '0.45',
            '--y', '0',
            '--z', '1.20',
            '--roll', '0',
            '--pitch', '0',
            '--yaw', '0',
            '--frame-id', 'base_link',
            '--child-frame-id',
            'wave_rover/base_link/front_lidar'
        ],
        output='screen'
    )

    # =========================================================
    # Start ROS components after rover has spawned
    # =========================================================

    start_ros_components = TimerAction(
        period=5.0,
        actions=[
            lidar_bridge,
            tf_bridge,
            lidar_static_tf
        ]
    )

    # =========================================================
    # Launch everything
    # =========================================================

    return LaunchDescription([
        gazebo,
        spawn_rover,
        start_ros_components
    ])
