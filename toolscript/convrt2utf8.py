# -*- coding:cp936 -*-
# -------------------------------------------
# Name:              convrt2utf8
# Author:            Hygnic
# Created on:        2021/12/9 15:55
# Version:           
# Reference:
"""
Description:         ��� cpg �ļ�������shp���������
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
    arcpy.AddMessage("\n|---------------------------------|")
    arcpy.AddMessage(" -----  ������ GIS�� ����������  ----- ")
    arcpy.AddMessage("|---------------------------------|\n")

    infeature_lyr = arcpy.GetParameterAsText(0)
    infeature_lyr_list = infeature_lyr.split(";")
    
    # # ����·��
    # layer_path = ur"E:\�߱�׼ũ��\code_test\�ڽ�����Զ��2019������Ԥ����Ͷ�ʸ߱�׼ũ�ｨ����Ŀ������Ƭ����\5110242019001.shp"

    for layer_path in infeature_lyr_list:
        # arcpy.AddMessage(layer_path)
        layer = arcpy.mapping.Layer(layer_path)
        add_cpg(layer)