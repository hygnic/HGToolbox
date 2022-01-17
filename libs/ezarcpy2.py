#!/usr/bin/env python
# -*- coding:utf-8 -*-
# ---------------------------------------------------------------------------
# Author: LiaoChenchen
# Created on: 2020/6/5 13:38
# Reference:
"""
Description: 快速添加标志牌shp,设置定义查询
*******************************FUNCTION*****************************************
*******************************FUNCTION*****************************************
*******************************FUNCTION:****************************************


Python2.7
	@@<Class> InitPath: initialize path, create gdb
	@@label: 是否显示图层且更改图层的标注
	@@add_field: 添加相同类型和长度的多个或者单个字段(如果存在相同名字的字段则不
								会添加字段)
	@@setZWMC: 根据LQDK图层中的LQLX字段赋予ZZMC1和ZZMC2
	@@merger_all: 一键快速合并一个图层的所有要素(添加一个字段，全部赋值为1，然后融合，
								最后删除该字段)
	@@merger_all_layers:在merger_all的基础上，先合并所有图层，然后融合所有要素。
	@@add_shp2mxd: 加载shp文件到mxd
	@@field_shower:获取图层中某单个字段的所有值(没多大价值，暂时留着)
	
	
*******************************FUNCTION*****************************************
*******************************FUNCTION*****************************************
*******************************FUNCTION*****************************************
Usage:
"""
# ---------------------------------------------------------------------------
from __future__ import absolute_import
from __future__ import unicode_literals
import arcpy
import random
import os
# from gpconfig import hyini


# class InitPath(object):
#     """初始化工作空间，创建gdb数据（如果没有）"""
#     def __new__(cls, *args, **kwargs):
#         if not hasattr(cls, "_instance"):
#             # if not cls._instance:
#             cls._instance = object.__new__(cls)
#         return cls._instance
#     def __init__(self):
#         """_________________________create folder____________________________"""
#         scratch_path = hyini.WORKSPACE_GDB
#         try:
#             if not os.path.isdir(scratch_path):
#                 os.makedirs(scratch_path)
#         except:
#             scratch_path = hyini.WORKSPACE_GDB2
#             if not os.path.isdir(scratch_path):
#                 os.makedirs(scratch_path)
#         """_________________________create folder____________________________"""
#         # make gdb
#         scratch_gdb = os.path.join(scratch_path, "Scratch.gdb")
#         if not arcpy.Exists(scratch_gdb):
#             arcpy.CreateFileGDB_management(scratch_path, "Scratch")
#         arcpy.env.workspace = scratch_path
#         arcpy.env.overwriteOutput = True
#
#         self.scratch_path = scratch_path
#         self.scratch_gdb = scratch_gdb
#
#     def __iter__(self):
#         # 用于拆包
#         return (i for i in (self.scratch_path, self.scratch_gdb))
#
#     def __getitem__(self, item):
#         return [self.scratch_path, self.scratch_gdb][item]

def label(layer,expression, show=True):
    """是否显示图层且更改图层的标注
     layer{Layer}: 图层对象
     expression{String}: 标注表达式:
      红色18号字体 "\"<CLR red=\'255\'><FNT size = \'18\'>\" + [BZPBH] + \"</FNT></CLR>\""
    return longName
        """
    if layer.supports("LABELCLASSES"):
        layer.showLabels = show
        for lblClass in layer.labelClasses:
            lblClass.expression = expression
        # print "Class Name:  " + lblClass.className
        # print "Expression:  " + lblClass.expression
        # print "SQL Query:   " + lblClass.SQLQuery
    else:
        print "Layer not support LabelClasses"
    return layer.longName


def add_field(layer, names, f_type, f_length=None, delete=True):
    """添加相同类型和长度的多个或者单个字段，只支持要素图层(如果存在相同名字的字段则不会添加字段)
      <特别注意因为字段类型和长度造成的后续错误>
      such as: add_field(layer_p,["ZWMC1","ZWMC2"],"TEXT",50)
    layer{String}: shp文件对象
      # TODO 按理应该可以使用图层对象，arcpy.mapping.Layer(path)，但是报错（arcgis10.3）
          # 已经解决： 因为arcpy.AddField_management 只支持要素图层，如果是shp文件地址的话
          # 需要使用arcpy.MakeFeatureLayer_management函数将要素类转为要素图层
    names: {List} 新增字段名称
    f_type: {String} 字段类型
    f_length: {Long} 字段长度
    delete: {Boolean} True 如果存在该字段，先删除再创建
    return: 返回当前的图层对象
    """
    the_fields = arcpy.ListFields(layer)
    for name in names:
        if not check_field_exit(the_fields, name):
            arcpy.AddField_management(layer, name, f_type, field_length=f_length)
            msg = "Created {0} field success".format(name.encode("utf8"))
            print msg
        else: # 存在该字段
            if delete:
                arcpy.DeleteField_management (layer, name)
                arcpy.AddField_management(layer, name, f_type, field_length=f_length)
            else:
                print "Field exist"
            
    return layer

def check_field_exit(field_obj, check_field):
    """
    检查图层是否存在该字段
    :param field_obj: field_obj = arcpy.ListFields(layer)
    :param check_field: field
    :return: {Bolean}
    """
    field_names = [i.name for i in field_obj] # field.aliasName
    return check_field in field_names

def field_chooser(field1, field2, field_obj):
    """
    判断图层中是存在field1字段还是field2字段，且返回该字段
    :param field_obj: 字段对象 该方法生成 fields = arcpy.ListFields(layer)
    :param field1: 字段 优先判断该字段
    :param field2: 字段
    :return:
    """
    field_names = [i.name for i in field_obj]
    if field1 in field_names:
        name = field1
    elif field2 in field_names:
        name = field2
    else:
        raise RuntimeError("{} and {} fields don't exist".format(field1, field2))
    return name




def setZWMC(layer, reference_field, target_field1, target_field2):
    """根据LQDK图层中的LQLX字段赋予ZZMC1和ZZMC2
      such as: setZWMC(layer, "LQLX", "ZWMC1", "ZWMC2")
    :param layer: 图层对象或者shp文件路径
    :param reference_field: LQLX字段
    :param target_field1: ZZMC1
    :param target_field2: ZZMC2
    :return:
    """
    in_fields = (reference_field, target_field1, target_field2)
    # LQLX匹配规则，LQLX代码表示的作物名称
    match_list = {
        11: (u"水稻", u""),
        12: (u"小麦", u""),
        13: (u"水稻", u"小麦"),
        14: (u"玉米", u""),
        15: (u"小麦", u"玉米"),
        25: (u"水稻", u"油菜")
    }
    with arcpy.da.UpdateCursor(layer, in_fields) as cursor:
        for row in cursor:
            LQLX = row[0]
            # match_list = match_list.iteritems()
            for m_key in match_list:
                if int(LQLX) == m_key:
                    # print "LQLX:",LQLX
                    # print "match_list.get:",match_list.get(m_key)[0]
                    # print "type:",type(match_list.get(m_key)[0])
                    # print "row[1]:",type(row[1])
                    row[1] = match_list.get(m_key)[0]
                    row[2] = match_list.get(m_key)[1]
                    cursor.updateRow(row)
                else:
                    # print "no match"
                    pass


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


def add_shp2mxd(mapdocument, shp_path, df_name=None, fresh=True):
    """加载shp文件到mxd
    import arcpy,os
    :param mapdocument: mxd对象（不是mxd文件地址）.
    :param shp_path: {String} file path.
    :param df_name: {String}dataframe name; default first dataframe.
    :param fresh: {Boll}; 刷新界面; default ture.
    :return: None
    """
    dataframe = arcpy.mapping.ListDataFrames(mapdocument, df_name)[0]
    layer = arcpy.mapping.Layer(shp_path)
    arcpy.mapping.AddLayer(dataframe, layer, "AUTO_ARRANGE")
    if fresh:
        arcpy.RefreshActiveView()  # 刷新地图和布局窗口
        arcpy.RefreshTOC()  # 刷新内容列表


def field_value_shower(layer, field):
    """获取图层中某单个字段的所有值(没多大价值，暂时留着)
    layer: mxd layer
    field: 字段,只能选一个字段
    """
    _list = []
    cursor = arcpy.da.SearchCursor(layer,field)
    for row in cursor:
        if row[0] not in _list:
            _list.append(row[0])
    del cursor
    return _list