# -*- coding:cp936 -*-
# -------------------------------------------
# Name:              auto_rename
# Author:            Hygnic
# Created on:        2021/12/27 13:49
# Version:           
# Reference:         
"""
Description:         �� arcmap ��������б��ж��ͬ����Ҫ��ͼ��ʱ��
                    ���޷�ʹ�úϲ����ܵģ���ʾ���������ظ������롣
                    �����б�ȥ����
Usage:               
"""
# -------------------------------------------
import arcpy
import random



# if __name__ == '__main__':
arcpy.AddMessage("\n|---------------------------------|")
arcpy.AddMessage(" -----  ������ GIS�� ����������  ----- ")
arcpy.AddMessage("|---------------------------------|\n")

mxd1 = arcpy.mapping.MapDocument('current')
df = arcpy.mapping.ListDataFrames(mxd1)[0]



infeature_lyr = arcpy.GetParameterAsText(0)
arcpy.AddMessage(infeature_lyr)
infeature_lyr_list = infeature_lyr.split(";")


for lyr in infeature_lyr_list:
    layer = arcpy.mapping.Layer(lyr)
    new_name = "layer_{}".format(random.randint(10000,99999))
    layer.name = new_name
    # arcpy.mapping.RemoveLayer(df, layer)
    # arcpy.mapping.AddLayer(df, layer)
    arcpy.RefreshTOC()