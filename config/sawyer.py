from util import str2bool


def add_arguments(parser):
    """
    Adds a list of arguments to argparser for the sawyer environment.
    """
    # sawyer
    parser.add_argument(
        "--reward_type", type=str, default="dense", choices=["dense", "sparse"]
    )
    parser.add_argument("--distance_threshold", type=float, default=0.06)
    parser.add_argument("--max_episode_steps", type=int, default=250)
    parser.add_argument(
        "--screen_width", type=int, default=500, help="width of camera image"
    )
    parser.add_argument(
        "--screen_height", type=int, default=500, help="height of camera image"
    )
    parser.add_argument("--camera_depth", type=str2bool, default=False)
    parser.add_argument("--camera_name", type=str, default="topview")

    # observations
    parser.add_argument(
        "--frame_skip", type=int, default=1, help="Numer of skip frames"
    )
    parser.add_argument("--action_repeat", type=int, default=5)
    parser.add_argument("--ctrl_reward_coef", type=float, default=0)

    parser.add_argument("--kp", type=float, default=40.0)  # 150.)
    parser.add_argument("--kd", type=float, default=8.0)  # 20.)
    parser.add_argument("--ki", type=float, default=0.0)  # 0.1)
    parser.add_argument("--frame_dt", type=float, default=0.15)  # 0.1)
    parser.add_argument("--use_robot_indicator", type=str2bool, default=True)
    parser.add_argument("--use_target_robot_indicator", type=str2bool, default=True)
    parser.add_argument(
        "--task_level", type=str, default="easy", choices=["easy", "hard"]
    )
    parser.add_argument("--success_reward", type=float, default=150.0)
    parser.add_argument("--range", type=float, default=0.1)
    parser.add_argument("--simple_planner_range", type=float, default=0.05)
    parser.add_argument("--timelimit", type=float, default=1.0)
    parser.add_argument("--simple_planner_timelimit", type=float, default=0.05)
    parser.add_argument("--contact_threshold", type=float, default=-0.002)
    parser.add_argument("--joint_margin", type=float, default=0.001)
    parser.add_argument("--step_size", type=float, default=0.02)


def get_default_config():
    """
    Gets default configurations for the Sawyer environment.
    """
    import argparse

    parser = argparse.ArgumentParser("Default Configuration for Sawyer Environment")
    add_argument(parser)

    parser.add_argument("--seed", type=int, default=1234)
    parser.add_argument("--debug", type=str2bool, default=False)

    config = parser.parse_args([])
    return config
