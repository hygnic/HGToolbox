# -*- coding:cp936 -*-
# -------------------------------------------
# Name:              merge_all_of_all
# Author:            Hygnic
# Created on:        2021/11/30 16:49
# Version:           
# Reference:         
"""
Description:         ��һ���������ͼ��ϲ���һ��ͼ��
                    ���ںϳ�һ���飬���������ص���������Ϣ
                    ��ȫ�ϲ� ȥ���ص�
Usage:               
"""
# -------------------------------------------
#<<<<<<<<<<<<<<<IMPORT SETTING>>>>>>>>>>>>>>
from __future__ import absolute_import
import arcpy
import sys
import os

#------------��ӻ�������
Script_dir = os.path.dirname(__file__)
Base_dir = os.path.dirname(Script_dir)
Libs_dir = os.path.join(Base_dir, "libs")
sys.path.append(Libs_dir)
#------------

def merger_all(layer, outputclass= "dissolve_all"):
    """
    һ�����ٺϲ�һ��ͼ�������Ҫ��(���һ���ֶΣ�ȫ����ֵΪ1��Ȼ���ںϣ����ɾ��
    ���ֶ�)
        <�ر�ע���ºϳɵ�ͼ�����ƣ��Ƿ�Ḳ��>
    layer(String): shp����lyr�ļ���ַ������ͼ�����
    return: �ϲ������ͼ�� Ĭ�Ϸ���ͼ������Ϊ newlayer_945
    """
    arcpy.env.addOutputsToMap = True
    arcpy.env.overwriteOutput = True
    # �ж��Ƿ�������ֶ�
    all_fields = arcpy.ListFields(layer)
    all_name = [i.name for i in all_fields]
    # for f in all_fields:
    # 	print f.name #Todo  neme �� aliasName ���صĶ�һ����Ϊʲô
    # print f.aliasName
    
    field_name = "test1f2lcc"
    if field_name not in all_name:
        arcpy.AddField_management(layer, field_name, "LONG")
    cursor = arcpy.da.UpdateCursor(layer, field_name)
    for row in cursor:
        row[0] = "1"
        cursor.updateRow(row)
    del cursor
    new_ly = outputclass
    arcpy.Dissolve_management(layer, new_ly ,field_name)
    arcpy.DeleteField_management(new_ly, field_name)
    return new_ly


def merger_all_layers(layers, result_lyr):
    """
    �����ͼ��ϲ���Ȼ������ȫ�ںϣ��������Կ��������ص�
    :param layers: {Str} ���Ҫ������ɵĵ�ַ ; �ָ�
    :param result_lyr: {Layer} �������Ҫ����
    :return:
    """
    arcpy.env.workspace = arcpy.env.scratchGDB
    arcpy.env.overwriteOutput = True
    # separate layers each
    # arcpy.AddMessage(type(layers))
    # arcpy.AddMessage(layers)
    layers_list = layers.split(";")
    # layers_list = layers
    # mergered_lyr = "in_memory/mergered_lyr"
    mergered_lyr = "mergered_lyr"
    
    # ��ͼ�����Ƴ��ֿո�ʱ���ָ��ĵ����������� ����NAME '",
    # ������Ҫȥ������������
    layers_list = [xxx.strip("'") if " " in xxx and "'" in xxx else xxx for xxx in layers_list]
    
    # arcpy.AddMessage("oooooooooo")
    # for aa_layer in layers_list:
    #     if " " in aa_layer and "'" in aa_layer:
    #         aa_layer = aa_layer.strip("'")
    #         arcpy.AddMessage(aa_layer)
    # #     arcpy.AddMessage(aa_layer)
    # #     arcpy.AddMessage(type(aa_layer))
    # # arcpy.AddMessage(layers_list)
    # arcpy.AddMessage("oooooooooo")
    # return 1
    
    arcpy.Merge_management(layers_list, mergered_lyr)
    mergered_dissolved_lyr = result_lyr
    merger_all(mergered_lyr, mergered_dissolved_lyr)
    arcpy.Delete_management(mergered_lyr)
    return mergered_dissolved_lyr



#<<<<<<<<<<<<<<<IMPORT SETTING>>>>>>>>>>>>>>
arcpy.AddMessage("\n|---------------------------------|")
arcpy.AddMessage(" -----  ������ GIS�� ����������  ----- ")
arcpy.AddMessage("|---------------------------------|\n")

layers = arcpy.GetParameterAsText(0)
output = arcpy.GetParameterAsText(1)

arcpy.env.overwriteOutput = True
merger_all_layers(layers, output)

