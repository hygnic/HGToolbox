# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              ExportMap
# Author:            Hygnic
# Created on:        2022/5/23 10:17
# Version:           
# Reference:         
"""
Description:         从选中文件夹中批量导出地图
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
    批量将MXD文档导出为JPEG图片
    :param path: mxd文件夹目录 string
    :param res: 分辨率 int
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
            # log_printer(afile+"非MXD文件,跳过\n")
            print u"\n非MXD文件,跳过"
    arcpy.AddMessage("OK!\n")

if __name__ == '__main__':
    export(arcpy.GetParameterAsText(0), int(arcpy.GetParameterAsText(1)))