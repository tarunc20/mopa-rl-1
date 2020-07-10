import re
from collections import OrderedDict

import numpy as np
from gym import spaces
from env.base import BaseEnv
from env.sawyer.sawyer import SawyerEnv
from env.robosuite.utils.transform_utils import *

class SawyerPickPlaceEnv(SawyerEnv):
    def __init__(self, **kwargs):
        super().__init__("sawyer_pick_place.xml", **kwargs)
        self._get_reference()

    # @property
    # def init_qpos(self):
    #     return np.array([-0.0305, -0.59325, 0.03043, 2.16124, 1.87488, 0, 0])

    def _get_reference(self):
        super()._get_reference()

        self.cube_body_id = self.sim.model.body_name2id("cube")
        self.cube_geom_id = self.sim.model.geom_name2id("cube")
        self.cube_site_id = self.sim.model.site_name2id("cube")


    def _reset(self):
        init_qpos = self.init_qpos + np.random.randn(self.init_qpos.shape[0]) * 0.02
        self.sim.data.qpos[self.ref_joint_pos_indexes] = init_qpos
        self.sim.data.qvel[self.ref_joint_vel_indexes] = 0.
        self.sim.data.qvel[self.ref_joint_vel_indexes] = 0.
        self.sim.forward()

        return self._get_obs()


    def initialize_joints(self):
        init_qpos = self.init_qpos + np.random.randn(self.init_qpos.shape[0]) * 0.02
        self.sim.data.qpos[self.ref_joint_pos_indexes] = init_qpos
        self.sim.data.qvel[self.ref_joint_vel_indexes] = 0.
        self.sim.forward()


    def compute_reward(self, action):
        reward_type = self._kwargs['reward_type']
        info = {}
        reward = 0

        if reward_type == 'dense':
            reach_multi = 0.6
            # right_gripper, left_gripper = self.sim.data.get_site_xpos('right_eef'), self.sim.data.get_site_xpos('left_eef')
            gripper_site_pos = self.sim.data.get_site_xpos("grip_site")
            cube_pos = np.array(self.sim.data.body_xpos[self.cube_body_id])
            gripper_to_cube = np.linalg.norm(cube_pos-gripper_site_pos)
            reward_reach = -gripper_to_cube*reach_multi
            reward += reward_reach
            info = dict(reward_reach=reward_reach)
        else:
            gripper_to_cube = np.linalg.norm(cube_pos-gripper_site_pos)
            reward_reach = -(gripper_to_cube > 0.15)
            reward += reward_reach
            info = dict(reward_reach=reward_reach)

        # if cube_to_target < self._kwargs['distance_threshold']:
        #     reward += self._kwargs['success_reward']
        #     self._success = True
        #     self._terminal = True

        return reward, info

    def _get_obs(self):
        di = super()._get_obs()
        cube_pos = np.array(self.sim.data.body_xpos[self.cube_body_id])
        cube_quat = convert_quat(
            np.array(self.sim.data.body_xquat[self.cube_body_id]), to="xyzw"
        )
        di["cube_pos"] = cube_pos
        di["cube_quat"] = cube_quat
        gripper_site_pos = np.array(self.sim.data.site_xpos[self.eef_site_id])
        di["gripper_to_cube"] = gripper_site_pos - cube_pos

        return di

    @property
    def static_geoms(self):
        return ['table_collision']

    @property
    def static_geom_ids(self):
        return [self.sim.model.geom_name2id(name) for name in self.static_geoms]

    @property
    def manipulation_geom(self):
        return ['cube']

    @property
    def manipulation_geom_ids(self):
        return [self.sim.model.geom_name2id(name) for name in self.manipulation_geom]

    @property
    def gripper_bodies(self):
        return ["clawGripper", "rightclaw", 'leftclaw', 'right_gripper_base', 'right_gripper', 'r_gripper_l_finger_tip', 'r_gripper_r_finger_tip']

    @property
    def gripper_target_bodies(self):
        return ["clawGripper_target", "rightclaw_target", 'leftclaw_target', 'right_gripper_base_target']

    @property
    def gripper_indicator_bodies(self):
        return ["clawGripper_indicator", "rightclaw_indicator", 'leftclaw_indicator', 'right_gripper_base_indicator']


    def _step(self, action, is_planner=False):
        """
        (Optional) does gripper visualization after actions.
        """
        assert len(action) == self.dof, "environment got invalid action dimension"

        if not is_planner or self._prev_state is None:
            self._prev_state = self.sim.data.qpos[self.ref_joint_pos_indexes].copy()

        if self._i_term is None:
            self._i_term = np.zeros_like(self.mujoco_robot.dof)

        if is_planner:
            rescaled_ac = np.clip(action[:self.robot_dof], -self._ac_scale, self._ac_scale)
        else:
            rescaled_ac = action[:self.robot_dof] * self._ac_scale
        desired_state = self._prev_state + rescaled_ac
        arm_action = desired_state
        gripper_action = self._gripper_format_action(np.array([action[-1]]))
        converted_action = np.concatenate([arm_action, gripper_action])

        n_inner_loop = int(self._frame_dt/self.dt)
        for _ in range(n_inner_loop):
            self.sim.data.qfrc_applied[self.ref_joint_vel_indexes] = self.sim.data.qfrc_bias[self.ref_joint_vel_indexes].copy()

            if self.use_robot_indicator:
                self.sim.data.qfrc_applied[
                    self.ref_indicator_joint_pos_indexes
                ] = self.sim.data.qfrc_bias[
                    self.ref_indicator_joint_pos_indexes
                ].copy()

            if self.use_target_robot_indicator:
                self.sim.data.qfrc_applied[
                    self.ref_target_indicator_joint_pos_indexes
                ] = self.sim.data.qfrc_bias[
                    self.ref_target_indicator_joint_pos_indexes
                ].copy()
            self._do_simulation(converted_action)

        self._prev_state = np.copy(desired_state)
        reward, info = self.compute_reward(action)

        return self._get_obs(), reward, self._terminal, info
