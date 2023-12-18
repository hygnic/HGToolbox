# -*- coding:cp936 -*-
# -------------------------------------------
# Name:              merge_all_of_all
# Author:            Hygnic
# Created on:        2021/11/30 16:49
# Version:           
# Reference:         
"""
Description:         将一个（多个）图层合并成一个图层
                    并融合成一整块，消除所有重叠和属性信息
                    完全合并 去除重叠
Usage:               
"""
# -------------------------------------------
#<<<<<<<<<<<<<<<IMPORT SETTING>>>>>>>>>>>>>>
from __future__ import absolute_import
import arcpy
import sys
import os

#------------添加环境变量
Script_dir = os.path.dirname(__file__)
Base_dir = os.path.dirname(Script_dir)
Libs_dir = os.path.join(Base_dir, "libs")
sys.path.append(Libs_dir)
#------------

def merger_all(layer, outputclass= "dissolve_all"):
    """
    一键快速合并一个图层的所有要素(添加一个字段，全部赋值为1，然后融合，最后删除
    该字段)
        <特别注意新合成的图层名称，是否会覆盖>
    layer(String): shp或者lyr文件地址，或者图层对象
    return: 合并后的新图层 默认返回图层名字为 newlayer_945
    """
    arcpy.env.addOutputsToMap = True
    arcpy.env.overwriteOutput = True
    # 判断是否有这个字段
    all_fields = arcpy.ListFields(layer)
    all_name = [i.name for i in all_fields]
    # for f in all_fields:
    # 	print f.name #Todo  neme 和 aliasName 返回的都一样，为什么
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
    将多个图层合并，然后再完全融合，这样可以快速消除重叠
    :param layers: {Str} 多个要素类组成的地址 ; 分隔
    :param result_lyr: {Layer} 最后的输出要素类
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
    
    # 当图层名称出现空格时，分割后的单个名称如下 “‘NAME '",
    # 所以需要去除两个单引号
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
arcpy.AddMessage(" -----  工具由 GIS荟 制作并发布  ----- ")
arcpy.AddMessage("|---------------------------------|\n")

layers = arcpy.GetParameterAsText(0)
output = arcpy.GetParameterAsText(1)

arcpy.env.overwriteOutput = True
merger_all_layers(layers, output)

