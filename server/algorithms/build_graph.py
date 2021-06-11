# -*- coding: utf-8 -*- 
# @Time : 2021/1/9 22:14
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : build_graph.py
# @Software: PyCharm

from server.tool import load_json, write_json
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import glob
from tqdm import tqdm


def build_graph(filepath):
    sb3 = load_json(filepath)
    targets = sb3['targets']
    monitors = sb3['monitors']
    extensions = sb3['extensions']
    meta = sb3['meta']

    G = nx.Graph(name="graph")  # 创建无向图

    stage_num = 0
    role_num = 0
    id = 0
    id2blockid = dict()
    blockid2id = dict()

    # 为所有Stage, role, block 构建映射
    for target in targets:
        isStage = target['isStage']
        if isStage is True:
            stage_num += 1
            name = target['name']
            if name not in blockid2id.keys():
                id2blockid[id] = name
                blockid2id[name] = id
                id += 1

            # Stage也有block
            blocks = target['blocks']
            for block_id in blocks:
                block = blocks[block_id]
                if block_id not in blockid2id.keys() and isinstance(block, dict):
                    id2blockid[id] = block_id
                    blockid2id[block_id] = id
                    id += 1
        else:
            role_num += 1
            name = target['name']
            if name not in blockid2id.keys():
                id2blockid[id] = name
                blockid2id[name] = id
                id += 1

            # Role's blocks
            blocks = target['blocks']
            for block_id in blocks:
                block = blocks[block_id]
                if block_id not in blockid2id.keys() and isinstance(block, dict):
                    id2blockid[id] = block_id
                    blockid2id[block_id] = id
                    id += 1

    # 构建Graph
    for target in targets:
        isStage = target['isStage']
        if isStage == True:
            name = target['name']
            stage_id = blockid2id[name]
            G.add_node(stage_id, id=stage_id, feature=name, name=name, opcode="stage")  # 舞臺加入Graph

            blocks = target['blocks']
            for block_id in blocks:
                block = blocks[block_id]
                if isinstance(block, dict):
                    id = blockid2id[block_id]
                    opcode = block['opcode']
                    next = block['next']
                    parent = block['parent']
                    isToplevel = block['topLevel']
                    if isToplevel is True:
                        G.add_node(id, id=id, name=block_id, feature=opcode, opcode=opcode, parent=stage_id)
                        G.add_edge(stage_id, id)
                    else:
                        if parent is None:
                            G.add_node(id, id=id, name=block_id, feature=opcode, opcode=opcode, parent=stage_id)
                            G.add_edge(stage_id, id)
                        else:
                            parent_id = blockid2id[parent]
                            G.add_node(id, id=id, name=block_id, feature=opcode, opcode=opcode, parent=parent_id)
                            G.add_edge(parent_id, id)
        else:
            name = target['name']
            role_id = blockid2id[name]
            G.add_node(role_id, id=role_id, name=name, feature=name, opcode="role", parent=stage_id)  # 將角色加入Graph
            G.add_edge(stage_id, role_id)

            blocks = target['blocks']
            for block_id in blocks:

                block = blocks[block_id]
                if isinstance(block, dict):
                    id = blockid2id[block_id]
                    opcode = block['opcode']
                    next = block['next']
                    parent = block['parent']
                    isToplevel = block['topLevel']
                    if isToplevel is True:
                        G.add_node(id, id=id, name=block_id, feature=opcode, opcode=opcode, parent=role_id)
                        G.add_edge(role_id, id)
                    else:
                        if parent is None:
                            G.add_node(id, id=id, name=block_id, feature=opcode, opcode=opcode, parent=role_id)
                            G.add_edge(role_id, id)
                        else:
                            parent_id = blockid2id[parent]
                            G.add_node(id, id=id, name=block_id, feature=opcode, opcode=opcode, parent=parent_id)
                            G.add_edge(parent_id, id)
    return G