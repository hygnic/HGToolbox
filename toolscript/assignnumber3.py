# -*- coding:cp936 -*-
# -------------------------------------------
# Name:              assinnumber
# Author:            Hygnic
# Created on:        2021/10/20 15:18
# Version:           
# Reference:         
"""
Description:         ����Ҫ�ر��
��ͬ���ֶ�ʹ��ͬһ�����룬��ͬ���������У��������У������1��ʼ
���ַ����и��������ͬһ���Եı������������û�������Ļ������ֵ�Ͳ�һ�����������˸�����
���� �����Ա���
Usage:               
"""
# -------------------------------------------
import arcpy
import random

def assign_number(input_feature, field, start_number, new_field):
    # field_name = u"���{}".format(random.randint())

    # start_number = "��1��"
    value_dict = {}
    # �½��ֶ�
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
    
    # �ȴ���һ���ֵ䣬���������õ����ݴ��ȥ��
    # Ȼ��ʹ���ֵ���������ֶΡ�
    
    with arcpy.da.UpdateCursor(input_feature, [field,new_field]) as cursor:
        for row in cursor:
            # if row[0] is None or row[0]== " " or row[0]== "":
            #     continue
            
            if row[0] in value_dict:
                row[1] = value_dict[row[0]]
                
            cursor.updateRow(row)
            
        
    # arcpy.AddMessage(value_dict)
    arcpy.RefreshActiveView()  # ˢ�µ�ͼ�Ͳ��ִ���
    arcpy.RefreshTOC()  # ˢ�������б�
    
    
if __name__ == '__main__':
    arcpy.AddMessage("\n|---------------------------------|")
    arcpy.AddMessage(" -----  ������ GIS�� ����������  ----- ")
    arcpy.AddMessage("|---------------------------------|\n")
    
    arcpy.env.overwriteOutput = True
    argv = tuple(arcpy.GetParameterAsText(i)
             for i in range(arcpy.GetArgumentCount()))

    assign_number(*argv)