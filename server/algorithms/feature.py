# -*- coding: utf-8 -*- 
# @Time : 2021/5/11 14:09
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : feature.py 
# @Software: PyCharm


import networkx as nx
import pandas as pd
import numpy as np
import os
import time
import torch

from server.algorithms import tool
from server.algorithms import build_graph
from server.algorithms.graph2vec import read_data

# 判断同构
# nx.is_isomorphic(G1, G2)  # 如果图G1和G2是同构的，则返回True，否则返回False 0.34s
# nx.could_be_isomorphic(G1, G2)  # 如果图绝对不是同构的，则返回False 0.11s
# nx.fast_could_be_isomorphic(G1, G2)  # 如果图绝对不是同构的，则返回False 0.09s
# nx.faster_could_be_isomorphic(G1, G2)  # 如果图绝对不是同构的，则返回False 0.03s
from server.tool import load_json


def which_is_isomorphic(G, graphs, method):
	isomorphic = []
	idx = 0
	for Ge in graphs:
		if method is "is":
			ret = nx.is_isomorphic(G, Ge)
		elif method is "could_be":
			ret = nx.could_be_isomorphic(G, Ge)
		elif method is "fast_could_be":
			ret = nx.fast_could_be_isomorphic(G, Ge)
		elif method is "faster_could_be":
			ret = nx.faster_could_be_isomorphic(G, Ge)

		if ret is True:
			isomorphic.append(idx)
		idx += 1
	return isomorphic


# 计算逻辑性
def cal_logicality(G):
	embedding_path = "D:/Workspace/Project/scratch-server/server/algorithms/embedding_64_200.pt"
	embeddings = torch.load(embedding_path)

	data_path = "D:/Workspace/Project_server_backup/p4/graph/"

	graphs = read_data(data_path)
	graph_bases = []
	for i in range(14):
		graph_base_path = "D:/Workspace/Project_server_backup/p4/type1_base/base" + str(i + 1) + '.gexf'
		g = nx.read_gexf(graph_base_path, node_type=int)
		graph_bases.append(g)
	all_graphs = graph_bases + graphs

	isomorphics = which_is_isomorphic(G, all_graphs, "faster_could_be")

	G_embedding = np.zeros((64,))
	if len(isomorphics) > 0:
		for idx in isomorphics:
			G_embedding += embeddings[idx]
		G_embedding = G_embedding / len(isomorphics)

	base_embeddings = embeddings[0:14]

	logicalities = []
	for base_embedding in base_embeddings:
		similarity = tool.cosine_similarity(G_embedding, base_embedding)
		logicalities.append(similarity)
	logicality = max(logicalities)
	return logicality


# 通过McCabe计算复杂度
def mccabe(filepath):
	scode = load_json(filepath)

	score = 1
	targets = scode['targets']
	for e in targets:
		name = e['name']
		blocks = e['blocks']

		for k, v in blocks.items():
			try:
				opcode = v['opcode']
				if opcode == "operator_and":
					score += 1
				elif opcode == "operator_or":
					score += 1
				elif opcode == "control_repeat":
					score += 1
				elif opcode == "control_forever":
					score += 1
				elif opcode == "control_if":
					score += 1
				elif opcode == "control_if_else":
					score += 2
				elif opcode == "control_repeat_until":
					score += 1
			except:
				pass
	return score


# 通过halstead计算工作量
def halstead(filepath):
	scode = load_json(filepath)

	N1 = 0  # 唯一操作数总数
	N2 = 0  # 唯一操作符总数
	n1 = 0  # 操作数总数
	n2 = 0  # 操作符总数
	opcode_set = set()
	opnum_set = set()

	targets = scode['targets']
	for e in targets:
		name = e['name']
		blocks = e['blocks']

		for k, v in blocks.items():
			try:
				opcode = v['opcode']
				n2 += 1
				opcode_set.add(opcode)
			except:
				pass
			try:
				inputs = v['inputs']
				n1 += len(inputs)
				for input in inputs:
					opnum_set.add(input)
			except:
				pass
	# print(n1, "", n2)
	N1 = len(opnum_set)
	N2 = len(opcode_set)
	N = N1 + N2
	n = n1 + n2
	if n != 0:
		V = N * np.log2(n)
		D = (n1 / 2) * (N2 / n2)
		E = D * V
		T = E / 18.0
		T_correct = 1.42 * T + 1250
		O = 0.007 * E + 46
	else:
		O = 0
		T = 0

	op_amount = O
	time_consuming = T
	return op_amount, time_consuming


# 提取关键变量和任务不相关统计量
def key_variable_irrelevant_statistic(filepath):
	scode = load_json(filepath)

	targets = scode['targets']

	targets_name_true = ["Stage", "比尔", "方块兽"]
	towards_cond = None
	condition_opcode = None
	fks_if_substack_opcode = None
	targets_num = len(targets)  # 特征: targets_num
	cnt_false_targets = 0  # 非需要使用的精灵数量
	cnt_false_targets_blocks = 0
	cnt_bill = 0
	cnt_bill_bk = 0
	cnt_bill_bk_type = 0
	cnt_fks = 0
	cnt_fks_bk = 0
	cnt_fks_bk_type = 0
	cnt_fks_while = 0
	cnt_fks_if = 0

	targets_name = set()

	for e in targets:
		name = e['name']
		targets_name.add(name)
		blocks = e['blocks']
		block_num = len(blocks)

		# opcode的种类
		opcode_set = set()
		for k, v in blocks.items():
			try:
				opcode = v['opcode']
				opcode_set.add(opcode)
			except:
				pass

		# 非所需要的精灵和个数
		is_need = False  # 判断是否所需：可能会出现类似于卡尔1，卡尔2的情况，都认为是所需
		for target_true in targets_name_true:
			if name in target_true:
				is_need = True
		if is_need is False:
			cnt_false_targets += 1  # 特征
			cnt_false_targets_blocks += block_num  # 特征

		if name == "Stage":
			num_stage_bk = block_num  # 特征：Stage的block数量
		elif name in "比尔":
			cnt_bill += 1
			cnt_bill_bk += block_num  # 特征：比尔的block数量
			cnt_bill_bk_type = len(opcode_set)
		elif name in "方块兽":
			cnt_fks += 1
			cnt_fks_bk += block_num  # 特征：方块兽的block数量
			cnt_fks_bk_type = len(opcode_set)

			for k, v in blocks.items():
				opcode = v['opcode']
				if opcode == "control_forever":
					cnt_fks_while += 1
				if opcode == "motion_pointtowards_menu":
					fields = v['fields']
					towards = fields['TOWARDS']
					towards_cond = towards[0]  # 关键变量1
				if opcode == "control_if":
					cnt_fks_if += 1
					inputs = v['inputs']
					if 'CONDITION' in inputs.keys():
						condition_k = inputs['CONDITION']
						if condition_k[0] == 2:
							condition_bk = blocks[condition_k[1]]
							condition_opcode = condition_bk['opcode']  # 关键变量2
					if 'SUBSTACK' in inputs.keys():
						substack_k = inputs['SUBSTACK']
						if substack_k[0] != 1:
							substack_bk = blocks[substack_k[1]]
							fks_if_substack_opcode = substack_bk['opcode']  # 关键变量3

	return towards_cond, condition_opcode, fks_if_substack_opcode, cnt_false_targets, cnt_false_targets_blocks, cnt_fks, cnt_bill
