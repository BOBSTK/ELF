game=./rts/game_MC/game model=actor_critic model_file=./rts/game_MC/model_unit_cmd python3 train.py --batchsize 8 --freq_update 50 --players "type=AI_NN,fs=50;type=AI_SIMPLE,fs=20" --num_games 256 --tqdm --T 10 --additional_labels id,last_terminal --trainer_stats winrate --use_unit_action --keys_in_reply V "$@"

