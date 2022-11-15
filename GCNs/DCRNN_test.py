# https://pytorch-geometric-temporal.readthedocs.io/en/latest/index.html
import torch
import torch.nn.functional as F
from torch_geometric_temporal.nn.recurrent import DCRNN
from torch_geometric_temporal.signal import DynamicGraphTemporalSignal
from torch_geometric_temporal.signal import temporal_signal_split
from tqdm import tqdm
import numpy as np

from preprocessed.utils import get_node_targets, get_node_features, get_edge_indices, get_edge_weights, refine_graph_data
from torch_geometric_temporal.dataset import ChickenpoxDatasetLoader

class RecurrentGCN(torch.nn.Module):
    def __init__(self, node_features):
        super(RecurrentGCN, self).__init__()
        self.recurrent = DCRNN(node_features, 32, 1)
        self.linear = torch.nn.Linear(32, 1)

    def forward(self, x, edge_index, edge_weight):
        h = self.recurrent(x, edge_index, edge_weight)
        h = F.relu(h)
        h = self.linear(h)
        return h


#########################
# 1. Data preprocessing
# - networkx graph → DynamicGraphTemporalSignal
# - 기간 : 18개월 (2017-01 ~ 2018-06)
# - node : 600개
# - node features : 1개 (FIXME 현재 random value)
# - node targets : 1개 (word count)
# - edge indices : 36개 (시점 0)
# - edge weights : 36개 (시점 0, co-occurrence)
#########################


media = 'patents' # patents template
topic_num = 1

# node targets(label)
node_targets = get_node_targets(media, topic_num)
print(f'node targets: {node_targets.shape}')

number_of_nodes = node_targets[0].shape[0]
number_of_features = 1

# edge indices and weights
edge_indices = get_edge_indices(media, topic_num, bidirectional=False)
edge_weights = get_edge_weights(media, topic_num, bidirectional=False)

# node features
node_features = get_node_features(media, topic_num)
# node_features = np.random.rand(len(edge_indices), number_of_nodes, number_of_features)
print(f'node feature: {node_features.shape}')

# refine graph data : remove empty edge indices and its edge and node information
node_targets, node_features, edge_indices, edge_weights = refine_graph_data(node_targets, node_features, edge_indices, edge_weights)

dataset = DynamicGraphTemporalSignal(edge_indices, edge_weights, node_features, node_targets)

#########################
# 2. Model training
#########################
train_dataset, test_dataset = temporal_signal_split(dataset, train_ratio=0.2)
model = RecurrentGCN(node_features=number_of_features)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

model.train()
for epoch in tqdm(range(200)):
    cost = 0
    for time, snapshot in enumerate(train_dataset):
        # print(snapshot.x.shape)
        # print(snapshot.edge_index.max())
        # batch = snapshot.edge_index.new_zeros(snapshot.edge_index.max().item() + 1)
        y_hat = model(snapshot.x, snapshot.edge_index, snapshot.edge_attr)
        cost = cost + torch.mean((y_hat - snapshot.y) ** 2)
    cost = cost / (time + 1)
    cost.backward()
    optimizer.step()
    optimizer.zero_grad()

#########################
# 3. Model testing
#########################
model.eval()
cost = 0
for time, snapshot in enumerate(test_dataset):
    y_hat = model(snapshot.x, snapshot.edge_index, snapshot.edge_attr)
    cost = cost + torch.mean((y_hat - snapshot.y) ** 2)
cost = cost / (time + 1)
cost = cost.item()
print("MSE: {:.4f}".format(cost))
