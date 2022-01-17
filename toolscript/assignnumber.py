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
这种方法有个问题就是同一属性的必须连续，如果没有连续的话，编号值就不一样。
Usage:               
"""
# -------------------------------------------
import arcpy
import random

def assign_number(input_feature, field, start_number, new_field):
    # field_name = u"标号{}".format(random.randint())

    # start_number = "（1）"
    
    # 新建字段
    arcpy.AddField_management(input_feature, new_field, "TEXT")
    with arcpy.da.UpdateCursor(input_feature, [field,new_field]) as cursor:
        count = 1
        first_value = "Start"
        for row in cursor:
            if row[0] is None or row[0]== " " or row[0]== "":
                # arcpy.AddMessage("None value here!")
                continue
                
            # 处理第一行的情况
            
            if first_value == "Start":
                first_value = row[0]
                # row[1] = str(count)
                row[1] = start_number
            
            # 第二行会到这里
            
            elif first_value == row[0]:
                # row[1] = str(count)
                row[1] = start_number
            
            elif first_value != row[0]:
                first_value = row[0]
                start_number = start_number.replace(str(count),str(count+1))
                count+=1
                # row[1] = str(count)
                row[1] = start_number
            cursor.updateRow(row)


if __name__ == '__main__':
    arcpy.env.overwriteOutput = True
    argv = tuple(arcpy.GetParameterAsText(i)
             for i in range(arcpy.GetArgumentCount()))

    assign_number(*argv)