python -m rl.main --env reacher-obstacle-pixel-v0 --hrl True --log_root_dir ./logs --wandb False --prefix pix_mp_test --max_global_step 6000000 --meta_update_target both --ll_type mp --planner_type rrt --planner_objective state_const_integral --range 30 --threshold 0.1 --timelimit 2. --evaluate_interval 1 --hl_type subgoal --policy cnn --gpu 0
# --debug True
