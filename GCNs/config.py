import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--device', type=str, default='0')
parser.add_argument('--device_ids', type=int, default=[0, 1, 2, 3], action="append")
parser.add_argument('--model', type=str, default='dcrnn')  # dcrnn tgcn agcrn a3tgcn
parser.add_argument('--epochs', type=int, default=200)
parser.add_argument('--batch_size', type=int, default=8)
parser.add_argument('--seed', type=int, default=0)
parser.add_argument('--lr', type=float, default=1e-3)
parser.add_argument('--node_feature_type', nargs='+', help='<Required> Set flag', default=['betweenness', 'closeness', 'degree'])
parser.add_argument('--topic_num', type=int, default=1)
parser.add_argument('--discard_index', type=int, default=0)
parser.add_argument('--num_training_clusters', type=int, default=100)
parser.add_argument('--cluster_dir', type=str, default='/Data2/yejin/blockchain_data/patents_co10/clusters.max_structured')
parser.add_argument('--topic_dir', type=str, default='/Data2/yejin/blockchain_data/patents_co10/4.topic_all_set.max_structured')
parser.add_argument('--media', type=str, default='patent')  # patent paper news

# model
parser.add_argument('--out_channels', type=int, default=32)
parser.add_argument('--out_size', type=int, default=1)
# filter size : DCRNN, AGCRN
parser.add_argument('--K', type=int, default=2)
# node embedding dimension AGCRN
parser.add_argument('--embedd_dim', type=int, default=4)
# A3TGCN
parser.add_argument('--periods', type=int, default=1)

# etc
parser.add_argument('--results_path', type=str, default='./results')

def get_config():
    return parser.parse_args()


def get_params(model):
    pp = 0
    for p in list(model.parameters()):
        nn = 1
        for s in list(p.size()):
            nn = nn * s
        pp += nn
    return pp
