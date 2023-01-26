discard_index=0

seed=0
for node_feature_type in degree; do #  betweenness closeness degree
  for model in dcrnn tgcn agcrn a3tgcn; do                # 'dcrnn' 'tgcn' 'agcrn' 'a3tgcn'
    for epochs in 200; do
      for device in 2; do
        for lr in 1e-3; do
          python3 -u main.py --seed $seed --model $model --node_feature_type $node_feature_type --epochs $epochs --device $device --lr $lr
        done
      done
    done
  done
done
