import os

from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    # Find installed rover_gazebo package
    pkg_rover_gazebo = get_package_share_directory('rover_gazebo')

    # Agricultural Gazebo world
    world_file = os.path.join(
        pkg_rover_gazebo,
        'worlds',
        'agri_world.sdf'
    )

    # Rover Gazebo model
    rover_model = os.path.join(
        pkg_rover_gazebo,
        'models',
        'wave_rover',
        'model.sdf'
    )

    # ---------------------------------------------------------
    # Gazebo environment
    #
    # ROS Rolling provides its own Gazebo configuration paths.
    # Add the system Gazebo configuration directory so that
    # Gazebo Harmonic / gz-sim8 can also be discovered.
    # ---------------------------------------------------------

    gz_config_path = os.environ.get('GZ_CONFIG_PATH', '')

    if gz_config_path:
        gz_config_path = '/usr/share/gz:' + gz_config_path
    else:
        gz_config_path = '/usr/share/gz'

    gz_resource_path = os.environ.get('GZ_SIM_RESOURCE_PATH', '')

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

    # Start Gazebo with agricultural world
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

    # Spawn rover after Gazebo has started
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

    return LaunchDescription([
        gazebo,
        spawn_rover
    ])
