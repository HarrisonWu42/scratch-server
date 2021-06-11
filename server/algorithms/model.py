# -*- coding: utf-8 -*- 
# @Time : 2021/5/11 12:29
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : model.py
# @Software: PyCharm


import networkx as nx
import pandas as pd
import numpy as np
import os
import time
import torch
import xgboost as xgb

from server.algorithms import tool
from server.algorithms import build_graph
from server.algorithms.feature import cal_logicality, mccabe, halstead, key_variable_irrelevant_statistic

feature_names = ['similarity', 'op_amount', 'time', 'mccabe_score', 'num_ir_roles', 'num_ir_roles_bk', 'num_beast',
                 'num_bill', 'teacher_1', 'teacher_2', 'teacher_3', 'teacher_4', 'teacher_5', 'teacher_6', 'teacher_7',
                 'teacher_8', 'teacher_9', 'teacher_10', 'teacher_11', 'teacher_12', 'teacher_13', 'teacher_14',
                 'teacher_15', 'teacher_16', 'teacher_17', 'teacher_18', 'teacher_19', 'teacher_20', 'teacher_21',
                 'teacher_22', 'teacher_23', 'teacher_24', 'teacher_25', 'teacher_26', 'teacher_27', 'teacher_28',
                 'teacher_29', 'teacher_30', 'teacher_31', 'teacher_32', 'teacher_33', 'teacher_34', 'teacher_35',
                 'teacher_36', 'teacher_37', 'teacher_38', 'teacher_39', 'teacher_40', 'teacher_41', 'teacher_42',
                 'teacher_43', 'teacher_44', 'teacher_45', 'teacher_46', 'teacher_47', 'teacher_48', 'teacher_49',
                 'teacher_50', 'teacher_51', 'teacher_52', 'teacher_53', 'teacher_54', 'teacher_55', 'teacher_56',
                 'teacher_57', 'teacher_58', 'teacher_59', 'teacher_60', 'teacher_61', 'teacher_62', 'teacher_63',
                 'teacher_64', 'teacher_65', 'teacher_66', 'teacher_67', 'teacher_68', 'teacher_69', 'teacher_70',
                 'teacher_71', 'teacher_72', 'teacher_73', 'teacher_74', 'teacher_75', 'towards_1', 'towards_Griffin',
                 'towards_IMG_9434', 'towards_Story-M', 'towards_Watermelon', 'towards_\\', 'towards__mouse_',
                 'towards_`', 'towards_yu', 'towards_万圣节魔法剑', 'towards_冒险者', 'towards_冰雪女王', 'towards_刺猬',
                 'towards_勇者征途1', 'towards_单眼怪', 'towards_史蒂夫', 'towards_孙悟空', 'towards_小丑', 'towards_小男孩',
                 'towards_小码医生', 'towards_小码君扛大炮', 'towards_小码君走路动态', 'towards_小码酱', 'towards_尼', 'towards_巡航舰',
                 'towards_帅帅', 'towards_弓', 'towards_战甲小码君', 'towards_房子', 'towards_房门', 'towards_手电筒', 'towards_敌军集结',
                 'towards_方块', 'towards_方块兽', 'towards_方块兽2', 'towards_方块兽20', 'towards_方块兽3', 'towards_方怪兽',
                 'towards_正派主机', 'towards_武器', 'towards_比', 'towards_比利', 'towards_bill', 'towards_法师', 'towards_爱莎',
                 'towards_狮老大', 'towards_终结者', 'towards_苦力怕', 'towards_药丸', 'towards_西游记-唐僧正面', 'towards_西游记-孙悟空打斗',
                 'towards_西游记-孙悟空走路', 'towards_角色1', 'towards_轿车', 'towards_银角大王动态', 'towards_隆中对-诸葛亮',
                 'towards_魔力测评等级', 'condition_sensing_touching', 'exit_control_create_clone_of',
                 'exit_control_delete_this_clone', 'exit_control_forever', 'exit_control_if', 'exit_control_if_else',
                 'exit_control_repeat', 'exit_control_repeat_until', 'exit_control_stop', 'exit_control_wait',
                 'exit_control_wait_until', 'exit_data_changevariableby', 'exit_event_broadcast',
                 'exit_event_broadcastandwait', 'exit_looks_changesizeby', 'exit_looks_cleargraphiceffects',
                 'exit_looks_hide', 'exit_looks_nextbackdrop', 'exit_looks_nextcostume', 'exit_looks_say',
                 'exit_looks_sayforsecs', 'exit_looks_setsizeto', 'exit_looks_switchbackdropto',
                 'exit_looks_switchcostumeto', 'exit_looks_think', 'exit_motion_changexby', 'exit_motion_glidesecstoxy',
                 'exit_motion_glideto', 'exit_motion_goto', 'exit_motion_gotoxy', 'exit_motion_ifonedgebounce',
                 'exit_motion_movesteps', 'exit_motion_pointindirection', 'exit_motion_pointtowards',
                 'exit_motion_setrotationstyle', 'exit_motion_turnleft', 'exit_motion_turnright',
                 'exit_music_playDrumForBeats', 'exit_procedures_call', 'exit_sensing_askandwait',
                 'exit_sensing_resettimer', 'exit_sensing_setdragmode', 'exit_sound_changeeffectby',
                 'exit_sound_cleareffects', 'exit_sound_play', 'exit_sound_playuntildone', 'exit_sound_stopallsounds']

teacher_mapping = {'t_.2q.DFXMwjk': 'teacher_1', 't_.dN/flSB3g2': 'teacher_2', 't_.eIDM6ZS1dQ': 'teacher_3',
                   't_1rcCQwsOP2U': 'teacher_4', 't_3ZzJMSYNrgo': 'teacher_5', 't_3bm48b5xKd6': 'teacher_6',
                   't_3eRtiHC.98Q': 'teacher_7', 't_4RrJwIMaglI': 'teacher_8', 't_4sDzHTh1TNw': 'teacher_9',
                   't_7.wXeHPgdyQ': 'teacher_10', 't_7ynBMz8ZTso': 'teacher_11', 't_9NKJzu8PoTU': 'teacher_12',
                   't_9ZDDkZ6I5Kk': 'teacher_13', 't_ARwVOpkmPCc': 'teacher_14', 't_AzaQqoPXJto': 'teacher_15',
                   't_BIyF8JEclOs': 'teacher_16', 't_BWIMuf0PeJM': 'teacher_17', 't_BisPVC6XmJg': 'teacher_18',
                   't_C05BI7D8nyY': 'teacher_19', 't_DAF37ekDNHY': 'teacher_20', 't_DCZdjCi7qwk': 'teacher_21',
                   't_Dm2kYl4EiJY': 'teacher_22', 't_E/2vG/16qxQ': 'teacher_23', 't_FQKeKcrbXms': 'teacher_24',
                   't_GXSkccFHc96': 'teacher_25', 't_GbOANBmfk7I': 'teacher_26', 't_Gy/vC6ATFYU': 'teacher_27',
                   't_I3HescZaToo': 'teacher_28', 't_JAq0ghwB55M': 'teacher_29', 't_K/1JeC1JN/M': 'teacher_30',
                   't_K/F7O/p8zNQ': 'teacher_31', 't_KM6ASFicfuU': 'teacher_32', 't_KUcwWVNfzb6': 'teacher_33',
                   't_KcO2.bm6e1Q': 'teacher_34', 't_KsBH3MRyWhc': 'teacher_35', 't_L9d5NUScr76': 'teacher_36',
                   't_NLRNMeYUK.M': 'teacher_37', 't_QrlO4cBrcoU': 'teacher_38', 't_QwASayMWw5E': 'teacher_39',
                   't_RweehHMyce.': 'teacher_40', 't_VmRDiphrH8c': 'teacher_41', 't_Vs6ARLlhtZk': 'teacher_42',
                   't_WRhPSGeqgO6': 'teacher_43', 't_Y99a5Na80oQ': 'teacher_44', 't_YiLLWH8fAM2': 'teacher_45',
                   't_YtG6pezCdkc': 'teacher_46', 't_ZSNCfrNXJI2': 'teacher_47', 't_ZiEQ9DalamQ': 'teacher_48',
                   't_aT73mEM1yoE': 'teacher_49', 't_dQslQ3AgFdo': 'teacher_50', 't_ePCMhJXbvik': 'teacher_51',
                   't_gbzw9w4voD.': 'teacher_52', 't_iXxnrDYD07M': 'teacher_53', 't_ivczcy7lVWM': 'teacher_54',
                   't_jf/2PTdMmLI': 'teacher_55', 't_kWZDekgRcmo': 'teacher_56', 't_kmR0rg1jxZs': 'teacher_57',
                   't_lMqENkZtYFo': 'teacher_58', 't_lqf3tQSc5Lw': 'teacher_59', 't_mtP9ZakWfUY': 'teacher_60',
                   't_nP2kE9JFylQ': 'teacher_61', 't_o94f1meTD4A': 'teacher_62', 't_pFF2hJQD6Vo': 'teacher_63',
                   't_q0AtDLVEc2A': 'teacher_64', 't_r.yiEKcoW1g': 'teacher_65', 't_sAL5JVwiARQ': 'teacher_66',
                   't_sZMl2zo.JSs': 'teacher_67', 't_ssmnHMGfmik': 'teacher_68', 't_uLwbKu546y.': 'teacher_69',
                   't_vo2bZTvK74c': 'teacher_70', 't_w95.OqBwKNQ': 'teacher_71', 't_wRmWvW0jHRE': 'teacher_72',
                   't_wjHS.edGNw.': 'teacher_73', 't_wxLs4bqvSUM': 'teacher_74', 't_xLRsw0Z4gss': 'teacher_75'}


def cls(dir_path, user_id, project_id, project_name):
    file_path = dir_path + "/" + project_name + ".sb3"
    graph_path = dir_path + "/" + project_name + ".gexf"
    # project_path = dir_path + "/" + project_name + ".json"

    project_path = tool.extract_sb3(file_path, dir_path, project_name)  # 提取源代码文件
    G = build_graph.build_graph(project_path)  # 解析源代码为AST
    nx.write_gexf(G, graph_path)  # 将AST写入硬盘

    logicality = cal_logicality(G)
    complexity = mccabe(project_path)
    op_amount, time_consuming = halstead(project_path)
    towards, condition, exit_action, num_ir_roles, num_ir_roles_bk, num_beast, num_bill = key_variable_irrelevant_statistic(
        project_path)

    input = np.zeros((1, 187))

    teacher = "t_KM6ASFicfuU"

    # 预处理老师特征
    teacher = teacher_mapping[teacher]
    idx = feature_names.index(teacher)
    input[0, idx] = 1

    # 预处理关键变量towards特征
    if towards is not None:
        if towards in "比尔":
            towards = "bill"
        towards = "towards_" + towards
        if towards in feature_names:
            idx = feature_names.index(towards)
            input[0, idx] = 1

    # 预处理关键变量condition特征
    if condition is not None:
        if condition == "sensing_touchingobject":
            condition = "sensing_touching"
        condition = "condition_" + condition
        if condition in feature_names:
            idx = feature_names.index(condition)
            input[0, idx] = 1

    # 预处理关键变量exit_action特征
    if exit_action is not None:
        exit_action = "exit_" + exit_action
        if exit_action in feature_names:
            idx = feature_names.index(exit_action)
            input[0, idx] = 1

    input[0, 0] = logicality
    input[0, 1] = op_amount
    input[0, 2] = time_consuming
    input[0, 3] = complexity
    input[0, 4] = num_ir_roles
    input[0, 5] = num_ir_roles_bk
    input[0, 6] = num_beast
    input[0, 7] = num_bill

    xgb_model = xgb.Booster(model_file='D:/Workspace/Project/scratch-server/server/algorithms/xgb.model')
    input = xgb.DMatrix(input)
    score = xgb_model.predict(input)

    return score, logicality, op_amount, complexity, num_ir_roles, num_ir_roles_bk, num_beast, num_bill


