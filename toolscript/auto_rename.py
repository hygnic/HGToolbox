# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              auto_rename
# Author:            Hygnic
# Created on:        2021/12/27 13:49
# Version:           
# Reference:         
"""
Description:         当 arcmap 左侧内容列表有多个同名的要素图层时，
                    是无法使用合并功能的，提示：不允许重复的输入。
Usage:               
"""
# -------------------------------------------
import arcpy
import random



if __name__ == '__main__':
    infeature_lyr = arcpy.GetParameterAsText(0)
    infeature_lyr_list = infeature_lyr.split(";")

    mxd = arcpy.mapping.MapDocument("CURRENT")
    df = arcpy.mapping.ListDataFrames(mxd)[0]
    
    for lyr in infeature_lyr_list:
        layer = arcpy.mapping.Layer(lyr)
        new_name = "layer_{}".format(random.randint(10000,99999))
        layer.name = new_name
        # arcpy.mapping.RemoveLayer(df, layer)
        # arcpy.mapping.AddLayer(df, layer)
        arcpy.RefreshTOC()