#<!/bin/bash -x

prefix="MoPA-SAC"
gpu=$1
seed=$2
algo='sac'
env="sawyer-push-obstacle-v2"
max_episode_step="250"
debug="True"
reward_type='sparse'
# log_root_dir="/data/jun/projects/hrl-planner/logs"
log_root_dir="./logs"
mopa="True"
reuse_data="True"
action_range="0.1"
stochastic_eval="True"
find_collision_free="True"
vis_replay="True"
plot_type='3d'
use_smdp_update="True"
use_discount_meta="True"
step_size="0.02"
success_reward="150.0"
max_reuse_data='15'
reward_scale="0.2"
use_ik_target="True"
ik_target="grip_site"
omega='0.05'

python -m rl.main \
    --log_root_dir $log_root_dir \
    --wandb True \
    --prefix $prefix \
    --env $env \
    --gpu $gpu \
    --max_episode_step $max_episode_step \
    --debug $debug \
    --algo $algo \
    --seed $seed \
    --reward_type $reward_type \
    --mopa $mopa \
    --reuse_data_type $reuse_data_type \
    --action_range $action_range \
    --stochastic_eval $stochastic_eval \
    --find_collision_free $find_collision_free \
    --vis_replay $vis_replay \
    --plot_type $plot_type \
    --use_smdp_update $use_smdp_update \
    --step_size $step_size \
    --success_reward $success_reward \
    --max_reuse_data $max_reuse_data \
    --reward_scale $reward_scale \
    --use_ik_target $use_ik_target \
    --ik_target $ik_target \
    --use_discount_meta $use_discount_meta \
    --omega $omega
