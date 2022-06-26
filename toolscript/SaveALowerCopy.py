# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              SaveALowerCopy
# Author:            Hygnic
# Created on:        2022/5/24 10:03
# Version:           
# Reference:         
"""
Description:         
Usage:               
"""
# -------------------------------------------
import arcpy, os, time


def log_printer(msg):
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    log_str = time_str+":"+msg
    # log_str = log_str.decode("cp936")
    print log_str
    arcpy.AddMessage(log_str)

arcpy.AddMessage("\n...")

path = arcpy.GetParameterAsText(0)

layoutdir = arcpy.GetParameterAsText(1)

arcpy.env.overwriteOutput = True

version = arcpy.GetParameterAsText(2)


#遍历目录下的MXD文档

for afile in os.listdir(path):
    
    if afile[-3:].lower()=='mxd':
        mxd=arcpy.mapping.MapDocument(os.path.join(path,afile))
        mxd.saveACopy (layoutdir+'\\'+afile[:-4]+'.mxd',version)
        log_printer(afile+": OK!")
        del mxd
        
arcpy.AddMessage("OK!\n")
















