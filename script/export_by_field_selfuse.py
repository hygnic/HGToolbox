# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              export_by_field
# Author:            Hygnic
# Created on:        2021/11/23 16:53
# Version:           
# Reference:         
"""
Description:         从要素类中根据字段名称导出多个要素类
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

import ezarcpy2
import hybasic2
#<<<<<<<<<<<<<<<IMPORT SETTING>>>>>>>>>>>>>>

arcpy.env.overwriteOutput= True



def export_by_filed(layer, field, folder, output_featurecalss, update_cursor=False):
    """
    :param update_cursor: 更新地块编码
    :param folder:
    :param output_featurecalss: 输出文件夹
    :param layer: 图层对象
    :param field: 字段
    :return:
    """
    if update_cursor:
        update_BSM(layer, u"地块编码")
    
    field_values = ezarcpy2.field_value_shower(layer, field)
    
    featurea_lyr = "featurea_lyr"
    arcpy.MakeFeatureLayer_management(layer, featurea_lyr)
    
    for value in field_values:
        
        # name+" LIKE '01%' "
        where_clause =  field + "=" + "'" + value + "'"
        arcpy.SelectLayerByAttribute_management(featurea_lyr, "NEW_SELECTION", where_clause)
        
        if folder:
            new_folder = os.path.join(output_featurecalss,value)
            if not os.path.exists(new_folder):
                os.makedirs(new_folder)
            
            out_feature_lyr = os.path.join(new_folder,value+".shp")
            arcpy.CopyFeatures_management(featurea_lyr, out_feature_lyr)
    
        else:
            out_feature_lyr = os.path.join(output_featurecalss,value+".shp")
            arcpy.CopyFeatures_management(featurea_lyr, out_feature_lyr)


def update_BSM(layer, field):
    with arcpy.da.UpdateCursor(layer, [field,"OID@","CJQYDM"]) as cursor:
        for row in cursor:
            xjqydm = row[2][:9]
            bsm = xjqydm+str(row[1])
            row[0] = bsm
            cursor.updateRow(row)
    
    arcpy.DeleteField_management(layer,"CJQYDM")
    # arcpy.DeleteField_management(layer,"XJQYMC")


if __name__ == '__main__':
    # lyr_path = ur"E:\中江LQDK\成果数据\柏树乡\Export_Output.shp"
    # in_lyr = arcpy.mapping.Layer(lyr_path)
    # ouput_path = ur"E:\中江LQDK\成果数据\柏树乡"
    #
    # export_by_filed(in_lyr, "CJQYMC", True, ouput_path)


    
    # 导出乡镇
    # lyr_path = ur"D:\中江LQDK\fme处理数据.gdb\fme处理成果四"
    lyr_path = ur"E:\中江LQDK\fmec处理结果2.gdb\处理结果"
    in_lyr = arcpy.mapping.Layer(lyr_path)
    # ouput_path = ur"D:\中江LQDK\成果"
    ouput_path = ur"E:\中江LQDK\成果lcc"

    export_by_filed(in_lyr, "XJQYMC", True, ouput_path)

    # 导出村
    # 先获得乡镇矢量列表
    hybasic2._getall_items =[]
    xjqy_shps = hybasic2.getfiles(ouput_path, "shp")
    print xjqy_shps
    
    # sys.exit(1)
    
    for shp in xjqy_shps:
        in_lyr = arcpy.mapping.Layer(shp)
        # 获得乡镇shp所在的文件夹
        shp_dir = os.path.dirname(shp)
        # 获得名称
        name_with_suffix = os.path.basename(shp)
        pure_name = os.path.splitext(name_with_suffix)[0]
        
        # 根据乡镇名称再创建一个文件夹
        CJQY_folder = os.path.join(shp_dir, pure_name)
        print CJQY_folder
        if not os.path.exists(CJQY_folder):
            os.makedirs(CJQY_folder)
        export_by_filed(in_lyr, "CJQYMC", False, CJQY_folder, update_cursor=True)