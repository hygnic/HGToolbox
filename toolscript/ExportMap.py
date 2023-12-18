# -*- coding:cp936 -*-
# -------------------------------------------
# Name:              ExportMap
# Author:            Hygnic
# Created on:        2022/5/23 10:17
# Version:           
# Reference:         
"""
Description:         ��ѡ���ļ���������������ͼ
���� ������ͼ����
Usage:               
"""
# -------------------------------------------
import arcpy
import os
import time

arcpy.env.overwriteOutput = True


def log_printer(msg):
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    log_str = time_str+":"+msg
    # log_str = log_str.encode("utf8")
    print log_str
    # arcpy.AddMessage(type(time_str))
    # arcpy.AddMessage(type(log_str))
    arcpy.AddMessage(log_str)
    
    # return log_str
    # log_file = open("log.txt", "a")
    # log_file.write(log_str+"\n")
    # log_file.close()


def export(path, res):
    """
    ������MXD�ĵ�����ΪJPEGͼƬ
    :param path: mxd�ļ���Ŀ¼ string
    :param res: �ֱ��� int
    :return:
    """
    arcpy.AddMessage("\n...")
    for afile in os.listdir(path):
        if afile[-3:].lower() == 'mxd':
            mxd1 = arcpy.mapping.MapDocument(os.path.join(path, afile))
            arcpy.mapping.ExportToJPEG(mxd1,
                                       os.path.join(path, afile[:-3] + 'jpg'), resolution = res)
            del mxd1
            log_printer(afile+": OK!")
        else:
            # log_printer(afile+"��MXD�ļ�,����\n")
            print u"\n��MXD�ļ�,����"
    arcpy.AddMessage("OK!\n")

if __name__ == '__main__':
    arcpy.AddMessage("\n|---------------------------------|")
    arcpy.AddMessage(" -----  ������ GIS�� ����������  ----- ")
    arcpy.AddMessage("|---------------------------------|\n")
    
    export(arcpy.GetParameterAsText(0), int(arcpy.GetParameterAsText(1)))