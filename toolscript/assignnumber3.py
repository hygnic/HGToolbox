# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              assinnumber
# Author:            Hygnic
# Created on:        2021/10/20 15:18
# Version:           
# Reference:         
"""
Description:         用于要素编号
相同的字段使用同一个号码，不同的升序排列，跳过空行；号码从1开始
这种方法有个问题就是同一属性的必须连续，如果没有连续的话，编号值就不一样。这里解决了该问题
Usage:               
"""
# -------------------------------------------
import arcpy
import random

def assign_number(input_feature, field, start_number, new_field):
    # field_name = u"标号{}".format(random.randint())

    # start_number = "（1）"
    value_dict = {}
    # 新建字段
    arcpy.AddField_management(input_feature, new_field, "TEXT")
    with arcpy.da.UpdateCursor(input_feature, [field,new_field]) as cursor:
        count = 0
        for row in cursor:
            if row[0] is None or row[0]== " " or row[0]== "":
                # arcpy.AddMessage("None value here!")
                continue
            
            if row[0] not in value_dict:
                start_number = start_number.replace(str(count),str(count+1))
                value_dict[row[0]] = start_number
                count += 1

    for k,v in value_dict.items():
        arcpy.AddMessage(k)
        arcpy.AddMessage(v)
    
    del cursor
    
    # 先创建一个字典，将遍历后获得的数据存进去；
    # 然后使用字典遍历更新字段。
    
    with arcpy.da.UpdateCursor(input_feature, [field,new_field]) as cursor:
        for row in cursor:
            # if row[0] is None or row[0]== " " or row[0]== "":
            #     continue
            
            if row[0] in value_dict:
                row[1] = value_dict[row[0]]
                
            cursor.updateRow(row)
            
        
    # arcpy.AddMessage(value_dict)
    arcpy.RefreshActiveView()  # 刷新地图和布局窗口
    arcpy.RefreshTOC()  # 刷新内容列表
    
    
if __name__ == '__main__':
    arcpy.env.overwriteOutput = True
    argv = tuple(arcpy.GetParameterAsText(i)
             for i in range(arcpy.GetArgumentCount()))

    assign_number(*argv)