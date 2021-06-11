# -*- coding: utf-8 -*- 
# @Time : 2021/5/11 9:52
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : graph2vec.py 
# @Software: PyCharm

import pandas as pd
import numpy as np
import networkx as nx
import glob
import time
from karateclub.graph_embedding import Graph2Vec
import torch
import torch.nn as nn
import torch.nn.functional as F


def read_data(path):
	graph_list = glob.glob(path + "*.gexf")
	graphs = []
	dic = {}
	for i in range(len(graph_list)):
		gpath = graph_list[i]
		gid = graph_list[i].split('\\')[-1].split('.')[0]
		dic[gpath] = int(gid)
	dic_sorted = sorted(dic.items(), key=lambda item: item[1], reverse=True)  # 按value进行降序

	graph_paths = []
	for item in dic_sorted:
		graph_paths.append(item[0])

	for i in range(len(graph_paths)):
		gpath = graph_paths[i]
		graph = nx.read_gexf(gpath, node_type=int)
		# graph = dgl.DGLGraph(graph)
		graphs.append(graph)
	return graphs


def graph2vec(root, dimensions, epochs):
	data_path = root + "graph/"
	info_path = root + 'info.csv'
	info = pd.read_csv(info_path)
	labels = info['label'].values.flatten()
	graphs = read_data(data_path)

	graph_bases = []
	for i in range(14):
		graph_base_path = root + 'type1_base/base' + str(i+1) + '.gexf'
		g = nx.read_gexf(graph_base_path, node_type=int)
		graph_bases.append(g)

	all_graphs = graph_bases + graphs
	model = Graph2Vec(attributed=True, dimensions=dimensions, epochs=epochs)
	model.fit(all_graphs)

	embedding = model.get_embedding()

	torch.save(embedding, root + "/embedding/embedding_" + str(dimensions) + "_" + str(epochs) + ".pt")


if __name__ == "__main__":
	# Win目录
	root = "D:/Workspace/Project/Data/p4/"

	start = time.time()
	graph2vec(root, 8, 5)
	end = time.time()
	print("运行时间：%.2f s" % (end - start))