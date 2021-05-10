# -*- coding: utf-8 -*- 
# @Time : 2021/5/10 13:28
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : tool.py 
# @Software: PyCharm


import json
import pandas as pd
import numpy as np


def load_json(filepath):
    file = open(filepath, 'rb')
    data = json.load(file)
    return data


def write_json(data, filepath):
    with open(filepath, 'w') as f:
        json.dump(data, f)
