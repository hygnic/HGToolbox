# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              convrt2utf8
# Author:            Hygnic
# Created on:        2021/12/9 15:55
# Version:           
# Reference:
"""
Description:         添加 cpg 文件来修正shp乱码的问题
Usage:               
"""
# -------------------------------------------

import arcpy
import os

def add_cpg(layer_obj):
    lyr_file = layer_obj.workspacePath
    lyr_name = layer_obj.datasetName
    cpg_file = os.path.join(lyr_file,lyr_name+".cpg")
    with open(cpg_file,"w") as f:
        f.write("utf8")
        

if __name__ == '__main__':
    infeature_lyr = arcpy.GetParameterAsText(0)
    infeature_lyr_list = infeature_lyr.split(";")
    
    # # 测试路径
    # layer_path = ur"E:\高标准农田\code_test\内江市威远县2019年中央预算内投资高标准农田建设项目（东联片区）\5110242019001.shp"

    for layer_path in infeature_lyr_list:
        # arcpy.AddMessage(layer_path)
        layer = arcpy.mapping.Layer(layer_path)
        add_cpg(layer)