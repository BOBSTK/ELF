#!/bin/bash

<<<<<<< HEAD
game=./rts/game_MC/game model=actor_critic model_file=./rts/game_MC/model python3 train.py --batchsize 64 --freq_update 1 --players --keys_in_reply V "type=AI_NN,fs=50,args=backup/AI_SIMPLE|start/500|decay/0.99;type=AI_SIMPLE,fs=20" --num_games 1024 --tqdm --T 20 --additional_labels id,last_terminal --trainer_stats winrate  "$@"


=======
game=./rts/game_MC/game model=actor_critic model_file=./rts/game_MC/model python3 train.py --batchsize 64 --freq_update 1 --players "type=AI_NN,fs=50,args=backup/AI_SIMPLE|start/500|decay/0.99;type=AI_SIMPLE,fs=20" --num_games 1024 --tqdm --T 20 --additional_labels id,last_terminal --trainer_stats winrate --keys_in_reply V "$@"
>>>>>>> 2f09f9674bb84c434124a61e9f45347b48980e60
