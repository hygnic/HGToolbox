#!/usr/bin/env python
# -*- coding:cp936 -*-
# ---------------------------------------------------------------------------
# Author: LiaoChenchen
# Created on: 2020/4/8 16:33
# Reference:
"""
Description: # python2
一些基础功能包，不涉及arcpy相关（不一定）


+++++++++++++++++++++++++++++++++++FUNCTION+++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++++FUNCTION:++++++++++++++++++++++++++++++++++++
Python2.7
	# export: export mxd to jpeg 001
	# HBgetfile: 获取文件 递归查询 getfile 002.0
	# HBfilter: 列表筛选（根据大小和字符串匹配） 002.5
	# make_chunk: 数据分发，将列表（data_list）中的元素平均分配多个子列表
	# timewrap、timewrap_cpu: 装饰函数，计算程序运行时间
+++++++++++++++++++++++++++++++++++FUNCTION+++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++++FUNCTION+++++++++++++++++++++++++++++++++++++
Usage:
"""
# ---------------------------------------------------------------------------
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
import arcpy
import os
import time
from datetime import datetime

# arcpy 导出JPEG，适用于文件夹或者单个mxd
def export(path, resolution):										 # 001
    arcpy.env.overwriteOutput = True
    if not os.path.isdir(path) and path[-3:].lower() == 'mxd':
        print("file")
        mxd1 = arcpy.mapping.MapDocument(path)
        print('exporting...')
        arcpy.mapping.ExportToJPEG(
            mxd1, os.path.abspath(path[:-3] + 'jpg'), resolution=resolution)
        a = os.path.split(path)
        print(a[1]+" finished")
    else:
        print("folder")
        for afile in os.listdir(path):
            if afile[-3:].lower() == 'mxd':
                mxd1 = arcpy.mapping.MapDocument(os.path.join(path, afile))
                print('exporting...')
                # ExportToJEPG的第二个参数是导出图片的名称和目录设置
                arcpy.mapping.ExportToJPEG(
                    mxd1, os.path.join(path, afile[:-3] + 'jpg'), resolution=resolution
                )
                print(afile + ' finished')
                print("\n----------------")
                del mxd1
            else:
                pass


_getall_items = []
def getfiles(dirs_p, suffix, recur=True, counter=0): 				 # 002.0
    """
    import os
    遍历获得一个文件夹（包含子文件夹）下所有的符合后缀的item
    ss = recur_search(u"G:/高标准", "", True)
    ss = recur_search(u"G:/高标准", "xlsx",True)
    ss = recur_search(u"G:/高标准", ["xlsx","xls"],True)

    recur 使用递归，特别注意，层数不要太多
    :param recur: bool 是否启用递归
    :param dirs_p: dir address
    :param suffix: 后缀 str或者列表 不包含.
    :param counter: 计数 用于缩进\t
    :return: list 返回完整地址的列表
    """
    global _getall_items
    
    # global __getall_items
    for file_p in os.listdir(dirs_p):
        file_path = os.path.join(dirs_p, file_p)
        if os.path.isdir(file_path):
            try:
                # print("\t" * counter + "dir:", file_p
                print("\t*{0} dir: {1}".format(int(counter),file_p.encode("utf8"))) # 出现带中文的子文件夹，不带encode会出错
            except Exception:
                print("<<<{0}>>>".format(__name__),"HBgetfile error occured, skipped")
            # 递归
            if recur:
                getfiles(file_path, suffix, recur, counter + 1)
        else:
            # print("\t"*counter+file_p
            if suffix:
                # 单个后缀
                if not isinstance(suffix, list):
                    # stage 1 筛选后缀
                    base_name = os.path.basename(file_path)
                    name_and_suffix = os.path.splitext(base_name)
                    f_suffix = name_and_suffix[1][1:].lower()
                    # f_name = name_and_suffix[0]
                    if f_suffix == suffix:
                        print("\t" * counter, base_name)
                        _getall_items.append(file_path)
                # 多个后缀组成列表
                else:
                    base_name = os.path.basename(file_path)
                    name_and_suffix = os.path.splitext(base_name)
                    f_suffix = name_and_suffix[1][1:]
                    # f_name = name_and_suffix[0]
                    if f_suffix in suffix:
                        print("\t" * counter, base_name)
                        _getall_items.append(file_path)
            # 无后缀要求，获取所有文件
            else:
                _getall_items.append(file_path)
    print("$"*80)
    return _getall_items


def filter_file(raw_list,matchword,size_limit=None):					# 002.5
    """
    使用字符匹配和文件大小（如果列表元素是地址的话）对列表中进行筛选
    import os
    oo = filter_list(ss,u"评估")
    oo = filter_list(ss,u"评估",100)
    :param raw_list:
    :param size_limit: int 排除等于该大小的文件 计量单位 字节
    :param matchword: 匹配字段，筛选符合该条件的元素
    :return: list
    """
    _bridge_list = []
    if matchword:
        for a_raw in raw_list:
            if matchword in os.path.basename(a_raw):
                _bridge_list.append(a_raw)
        raw_list = _bridge_list
    if size_limit:
        _bridge_list = []
        _bridge_list = [x for x in raw_list if os.path.getsize(x) != size_limit]
    print("after filter:", len(_bridge_list))
    return _bridge_list


def make_chunk(data_list, chunk_num):
    """将列表（data_list）中的元素平均分配多个子列表
        such as:
            i_list = [1, 34, 3, 67, 8, 98, 39, 98, 34, 3, 67, 8, 98, 39, 98, 34,
                 6, 67, 8, 98, 39, 98, 34, 3, 67, 8 , 34, 3, 67, 8, 98, 39, 98,
                 98, 39, 98, 34, 3, 67, 8, 98, 39, 98, 34, 3, 67, 8, 98, 39, 98,
                 8, 98, 39, 98, 34, 3, 67 ]
            result_list = data_distribute(i_list,6)

    data_list{List}: 主要数据列表
    chunk_num{Int}:  组块数（子列表个数）
    :return{List}:  返回两个列表：一个包含所有子列表的列表，一个信息组成的列表
    """
    msg_info = []
    def sub_list(main_list, l_len):
        """选择
        :param main_list: {List} 父列表，我们的主要列表
        :param l_len: {Int} 切片长度，使用pop方法
        :return: {List} son 返回一个子列表
        """
        # son 子列表
        son = []
        for ii7 in xrange(l_len):
            son.append(main_list.pop())
        return son
    
    # 顺序反向，因为pop()取最后一位，且比pop(0)快
    data_list.reverse()
    # 包含所有子列表的列表
    result_groups = []
    lenn = len(data_list)
    # print("list_lence:", lenn
    # 分为core组，slice_amount为每组的数量
    slice_amount = lenn // chunk_num
    # print("slice_count:", slice_amount
    for i in xrange(chunk_num):
        # 以core为长度的一个切片
        l_slice = sub_list(data_list, slice_amount)
        # print("one_slice:", l_slice)
        result_groups.append(l_slice)
    # remained_item_amount 主要数据列表中剩余的元素的个数
    remained_item_amount = lenn - slice_amount * chunk_num
    msg1 = "remained_item:{0} ; remained_item_amount:{1}".format(
        data_list, remained_item_amount)
    # print(msg1)
    # 将主要列表中的值取完才结束
    while data_list:
        for i in xrange(remained_item_amount):
            item = data_list.pop()
            result_groups[i].append(item)
    # print("result_groups:",result_groups
    j = 0
    for i in result_groups:
        i_len = len(i)
        info = "Chunk's count: {}".format(i_len)
        print(info)
        msg_info.append(info)
        j += i_len
    info = "total: {}".format(j)
    print(info)
    print("@" * 50)
    msg_info.append(info)
    return result_groups, msg_info

# 装饰函数 计算程序运行时间
def timewrap(func):
    def inner():
        start = time.time()
        func()
        end = time.time()
        msg = 'Time consuming: {}'.format(end-start)
        print(msg)
    return inner

# 装饰函数 计算CPU执行时间
def timewrap_cpu(func):
    def inner():
        start = time.clock()
        func()
        end = time.clock()
        msg = 'CPU time consuming: {}'.format(end - start)
        print(msg)
    return inner


class HyTime(object):
    """时间管理模块"""
    def __init__(self):
        # 将字符串转换为时间格式
        time2 = datetime.strptime("2019-9-1", "%Y-%m-%d")
    
    
    @property
    def time_now(self):
        now = datetime.now()
        # 格式化时间，转换为字符串
        time_now_str = datetime.strftime(now, "%Y %m %d %H:%M:%S")
        # 返回当前时间以及当前时间的字符串数据
        return now, time_now_str
    
    # 记录运行时间
    def elapsed_time(self, early_time, after_time):
        """
        early_time(时间格式):
        after_time(时间格式):
        :return:
        """
        delta_time = (after_time-early_time) # -408 days, 13:40:14.996000 <type 'datetime.timedelta'>
        day = delta_time.days # # -408 <type 'int'>
        hours = round(delta_time.seconds/3600,3)
        total_seconds = delta_time.total_seconds()
        elapsed_time = "Elapsed_time: {0} day, {1} hours (Totally: {2} second)".format(day,hours,total_seconds)
        return elapsed_time


class HyMath(object):
    def __init__(self):
        pass
