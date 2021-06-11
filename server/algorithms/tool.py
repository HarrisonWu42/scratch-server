# -*- coding: utf-8 -*- 
# @Time : 2021/5/11 12:34
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : tool.py 
# @Software: PyCharm


import os
import shutil
import zipfile
import numpy as np

def modify_file_type(file_path, srctype, drctype):
    """ 修改某个文件后缀名
    srctype: ".xxx"
    drctype: ".xxx"
    """
    portion = os.path.splitext(file_path)
    if portion[1] == srctype:
        old_name = portion[0] + srctype
        new_name = portion[0] + drctype
        os.rename(old_name, new_name)
    return new_name


def un_zip(file_name):
    """ 解压单个zip文件 """
    zip_file = zipfile.ZipFile(file_name)
    if os.path.isdir(file_name + "_files"):
        pass
    else:
        os.mkdir(file_name + "_files")
    for names in zip_file.namelist():
        zip_file.extract(names, file_name + "_files/")
    zip_file.close()
    return file_name + "_files/"


def copy_rename_file(file, new_dir_path, new_file_name):
    """ 复制某个文件并重命名
        file:      原始文件
        new_dir_path: 新文件目录
        new_file_name:   新文件名称
    """
    if not os.path.exists(new_dir_path):
        os.makedirs(new_dir_path)
    new_file = os.path.join(new_dir_path, new_file_name)
    shutil.copy(file, new_file)
    return new_file


def extract_sb3(file, drcdir, new_id):
    """ 提取某个sb3文件到某个文件夹下
        file: 文件路径
        drcdir: 目录路径，/结尾
        new_id: 数字
    """
    modify_file_type(file, ".sb3", ".zip")  # 修改后缀名
    portion = os.path.splitext(file)
    zip_file = portion[0] + ".zip"
    un_zip(zip_file)  # 解压
    dir_path = portion[0] + ".zip_files"
    new_file_name = str(new_id) + ".json"
    new_file_path = copy_rename_file(dir_path + "/project.json", drcdir, new_file_name)  # 复制并重命名
    shutil.rmtree(dir_path)  # 删除文件夹
    modify_file_type(zip_file, ".zip", ".sb3")
    return new_file_path


def cosine_similarity(x, y):
    num = x.dot(y.T)
    denom = np.linalg.norm(x) * np.linalg.norm(y)
    return num / denom