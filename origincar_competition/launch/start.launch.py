import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python import get_package_share_directory
from launch_ros.descriptions import ParameterValue

def generate_launch_description():

    launch_args = [
        DeclareLaunchArgument('line_following_speed', default_value='0.65',
                              description='Speed for line following (m/s)'),
        DeclareLaunchArgument('line_kp', default_value='0.003225', # 1.0/320.0
                              description='Proportional gain for line following'),
        DeclareLaunchArgument('cone_avoidance_speed', default_value='0.4',
                              description='Base speed during cone avoidance (m/s)'),
        DeclareLaunchArgument('cone_detection_y_threshold', default_value='130.0',
                              description='Cone height (px) to trigger avoidance action'),
        DeclareLaunchArgument('cone_critical_y_threshold', default_value='250.0',
                              description='Cone height (px) for critical avoidance'),
        DeclareLaunchArgument('cone_avoidance_steering_gain', default_value='0.5',
                              description='Base steering gain for cone avoidance and recovery turn amplitude (rad/s)'),
        DeclareLaunchArgument('cone_lateral_offset_threshold', default_value='30.0',
                              description='Cone lateral offset tolerance for centered critical check (px)'),
        DeclareLaunchArgument('post_avoidance_forward_search_duration', default_value='0.5',
                              description='Duration to search forward after cone avoidance (seconds)'),
        DeclareLaunchArgument('post_avoidance_recovery_turn_duration', default_value='0.0', 
                              description='Max duration for recovery turn search (seconds, 0 for indefinite)'),
        DeclareLaunchArgument('recovery_turn_linear_speed_ratio', default_value='0.3',
                              description='Linear speed ratio for recovery turn (relative to line_following_speed)'),
        DeclareLaunchArgument('search_swing_frequency', default_value='0.3',
                              description='Frequency for S-swing search if no specific recovery direction (Hz)'),

    ]

    included_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('origincar_bringup'), 'launch', 'usb_websocket_display.launch.py')
        ]),
    )

    competition_node = Node(
        package="origincar_competition",
        executable="origincar_competition",
        name="complete_control_node",
        output='screen',
        arguments=['--ros-args', '--log-level', 'info'],
        parameters=[{
                'line_following_speed': ParameterValue(LaunchConfiguration('line_following_speed'), value_type=float),
                'line_kp': ParameterValue(LaunchConfiguration('line_kp'), value_type=float),
                'cone_avoidance_speed': ParameterValue(LaunchConfiguration('cone_avoidance_speed'), value_type=float),
                'cone_detection_y_threshold': ParameterValue(LaunchConfiguration('cone_detection_y_threshold'), value_type=float),
                'cone_critical_y_threshold': ParameterValue(LaunchConfiguration('cone_critical_y_threshold'), value_type=float),
                'cone_avoidance_steering_gain': ParameterValue(LaunchConfiguration('cone_avoidance_steering_gain'), value_type=float),
                'cone_lateral_offset_threshold': ParameterValue(LaunchConfiguration('cone_lateral_offset_threshold'), value_type=float),
                'post_avoidance_forward_search_duration': ParameterValue(LaunchConfiguration('post_avoidance_forward_search_duration'), value_type=float),
                'post_avoidance_recovery_turn_duration': ParameterValue(LaunchConfiguration('post_avoidance_recovery_turn_duration'), value_type=float),
                'recovery_turn_linear_speed_ratio': ParameterValue(LaunchConfiguration('recovery_turn_linear_speed_ratio'), value_type=float),
                'search_swing_frequency': ParameterValue(LaunchConfiguration('search_swing_frequency'), value_type=float),
            }],
    )

    return LaunchDescription(launch_args + [
        included_launch,
        competition_node
    ])