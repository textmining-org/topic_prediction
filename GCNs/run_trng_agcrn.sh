seed=0
num_train_clusters=100
num_valid_clusters=20
num_test_clusters=20
lr=1e-3
batch_size=64
seq_len=12
pred_len=1
desc='desc'

epochs=100
patience=10

device=0
media=patents # patents papers news
cluster_dir='/Data2/yejin/blockchain_data_2024/'$media'_co10/5.random_cluster/clusters.max_structured.time_split'
results_path='./results/joi_2024'
metrics_file='metrics_trng_agcrn.csv'

model=agcrn
lr=1e-2
for num_train_clusters in 100 500 1000 4000 8000; do # 100 500 1000 2000 4000 6000 8000
  for num_valid_clusters in 2000; do                           # 1000 2000
    for num_test_clusters in 2000; do                          # 1000 2000
      for node_feature_type in "betweenness closeness" "betweenness degree" "closeness degree" "betweenness closeness degree" "betweenness" "degree" "closeness"; do
        for K in 1 2 3; do
          for embedd_dim in 4 8 16 32; do
            for out_channels in 4 8 16 32; do
              for pred_len in 3 6 12; do # 1 3 6 9 12
                python3 -u main_trng_loader.py --seed $seed \
                  --cluster_dir $cluster_dir \
                  --model $model \
                  --node_feature_type $node_feature_type \
                  --epochs $epochs \
                  --patience $patience \
                  --device $device \
                  --num_train_clusters $num_train_clusters \
                  --num_valid_clusters $num_valid_clusters \
                  --num_test_clusters $num_test_clusters \
                  --lr $lr \
                  --media $media \
                  --batch_size $batch_size \
                  --seq_len $seq_len \
                  --pred_len $pred_len \
                  --early_stop \
                  --results_path $results_path \
                  --metrics_file $metrics_file \
                  --out_channels $out_channels \
                  --K $K \
                  --embedd_dim $embedd_dim \
                  --desc $desc >trng_$media'_'$model.log
              done
            done
          done
        done
      done
    done
  done
done
