# -*- coding:cp936 -*-
# -------------------------------------------
# Name:              export_by_field
# Author:            Hygnic
# Created on:        2021/11/23 16:53
# Version:           
# Reference:         
"""
Description:         ��Ҫ�����и����ֶ����Ƶ������Ҫ����
�����Ե���
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


#<<<<<<<<<<<<<<<IMPORT SETTING>>>>>>>>>>>>>>

def field_value_shower(layer, field):
    """��ȡͼ����ĳ�����ֶε�����ֵ(û����ֵ����ʱ����)
    layer: mxd layer
    field: �ֶ�,ֻ��ѡһ���ֶ�
    """
    _list = []
    cursor = arcpy.da.SearchCursor(layer,field)
    for row in cursor:
        if row[0] not in _list:
            _list.append(row[0])
    del cursor
    return _list


def export_by_filed(layer, field, output_featurecalss, folder):
    """
    :param layer: {Strings} ͼ�����
    :param field: {Strings} �ֶ�
    :param output_featurecalss: {Strings} ����ļ���
    :param folder:{Boolean} �Ƿ��ÿ��������shp�����ļ���
    :return:
    """
    field_values = field_value_shower(layer, field)
    
    featurea_lyr = "featurea_lyr"
    arcpy.MakeFeatureLayer_management(layer, featurea_lyr)
    
    for value in field_values:
        
        # name+" LIKE '01%' "
        # arcpy.AddMessage( value)
        where_clause =  field + "=" + "'" + value + "'"
        # arcpy.AddMessage( where_clause)
        arcpy.SelectLayerByAttribute_management(featurea_lyr, "NEW_SELECTION", where_clause)
        
        if folder == "true":
            new_folder = os.path.join(output_featurecalss,value)
            if not os.path.exists(new_folder):
                os.makedirs(new_folder)
            
            out_feature_lyr = os.path.join(new_folder,value+".shp")
            arcpy.CopyFeatures_management(featurea_lyr, out_feature_lyr)
    
        else:
            out_feature_lyr = os.path.join(output_featurecalss,value+".shp")
            arcpy.CopyFeatures_management(featurea_lyr, out_feature_lyr)



if __name__ == '__main__':
    # һ
    arcpy.AddMessage("\n|---------------------------------|")
    arcpy.AddMessage(" -----  ������ GIS�� ����������  ----- ")
    arcpy.AddMessage("|---------------------------------|\n")
    
    arcpy.env.overwriteOutput = True
    argv = tuple(arcpy.GetParameterAsText(i)
                 for i in range(arcpy.GetArgumentCount()))
    for i in argv:
        arcpy.AddMessage(i)
    
    export_by_filed(*argv)


    # arcpy.env.overwriteOutput = True
    para1 = arcpy.GetParameterAsText(0)
    para2 = arcpy.GetParameterAsText(1)
    para3 = arcpy.GetParameterAsText(2)
    para4 = arcpy.GetParameterAsText(3)
    arcpy.AddMessage(">>>")
    arcpy.AddMessage(para1)
    arcpy.AddMessage(type(para1))
    
    arcpy.AddMessage(">>>")
    arcpy.AddMessage(para2)
    arcpy.AddMessage(type(para2))
    
    arcpy.AddMessage(">>>")
    arcpy.AddMessage(para3)
    arcpy.AddMessage(type(para3))
    
    arcpy.AddMessage(">>>")
    arcpy.AddMessage(para4)
    arcpy.AddMessage(type(para4))