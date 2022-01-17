#!/usr/bin/env python
# -*- coding:cp936 -*-
# ---------------------------------------------------------------------------
# Author: LiaoChenchen
# Created on: 2020/4/8 16:33
# Reference:
"""
Description: # python2
һЩ�������ܰ������漰arcpy��أ���һ����


+++++++++++++++++++++++++++++++++++FUNCTION+++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++++FUNCTION:++++++++++++++++++++++++++++++++++++
Python2.7
	# export: export mxd to jpeg 001
	# HBgetfile: ��ȡ�ļ� �ݹ��ѯ getfile 002.0
	# HBfilter: �б�ɸѡ�����ݴ�С���ַ���ƥ�䣩 002.5
	# make_chunk: ���ݷַ������б�data_list���е�Ԫ��ƽ�����������б�
	# timewrap��timewrap_cpu: װ�κ����������������ʱ��
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

# arcpy ����JPEG���������ļ��л��ߵ���mxd
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
                # ExportToJEPG�ĵڶ��������ǵ���ͼƬ�����ƺ�Ŀ¼����
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
    �������һ���ļ��У��������ļ��У������еķ��Ϻ�׺��item
    ss = recur_search(u"G:/�߱�׼", "", True)
    ss = recur_search(u"G:/�߱�׼", "xlsx",True)
    ss = recur_search(u"G:/�߱�׼", ["xlsx","xls"],True)

    recur ʹ�õݹ飬�ر�ע�⣬������Ҫ̫��
    :param recur: bool �Ƿ����õݹ�
    :param dirs_p: dir address
    :param suffix: ��׺ str�����б� ������.
    :param counter: ���� ��������\t
    :return: list ����������ַ���б�
    """
    global _getall_items
    
    # global __getall_items
    for file_p in os.listdir(dirs_p):
        file_path = os.path.join(dirs_p, file_p)
        if os.path.isdir(file_path):
            try:
                # print("\t" * counter + "dir:", file_p
                print("\t*{0} dir: {1}".format(int(counter),file_p.encode("utf8"))) # ���ִ����ĵ����ļ��У�����encode�����
            except Exception:
                print("<<<{0}>>>".format(__name__),"HBgetfile error occured, skipped")
            # �ݹ�
            if recur:
                getfiles(file_path, suffix, recur, counter + 1)
        else:
            # print("\t"*counter+file_p
            if suffix:
                # ������׺
                if not isinstance(suffix, list):
                    # stage 1 ɸѡ��׺
                    base_name = os.path.basename(file_path)
                    name_and_suffix = os.path.splitext(base_name)
                    f_suffix = name_and_suffix[1][1:].lower()
                    # f_name = name_and_suffix[0]
                    if f_suffix == suffix:
                        print("\t" * counter, base_name)
                        _getall_items.append(file_path)
                # �����׺����б�
                else:
                    base_name = os.path.basename(file_path)
                    name_and_suffix = os.path.splitext(base_name)
                    f_suffix = name_and_suffix[1][1:]
                    # f_name = name_and_suffix[0]
                    if f_suffix in suffix:
                        print("\t" * counter, base_name)
                        _getall_items.append(file_path)
            # �޺�׺Ҫ�󣬻�ȡ�����ļ�
            else:
                _getall_items.append(file_path)
    print("$"*80)
    return _getall_items


def filter_file(raw_list,matchword,size_limit=None):					# 002.5
    """
    ʹ���ַ�ƥ����ļ���С������б�Ԫ���ǵ�ַ�Ļ������б��н���ɸѡ
    import os
    oo = filter_list(ss,u"����")
    oo = filter_list(ss,u"����",100)
    :param raw_list:
    :param size_limit: int �ų����ڸô�С���ļ� ������λ �ֽ�
    :param matchword: ƥ���ֶΣ�ɸѡ���ϸ�������Ԫ��
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
    """���б�data_list���е�Ԫ��ƽ�����������б�
        such as:
            i_list = [1, 34, 3, 67, 8, 98, 39, 98, 34, 3, 67, 8, 98, 39, 98, 34,
                 6, 67, 8, 98, 39, 98, 34, 3, 67, 8 , 34, 3, 67, 8, 98, 39, 98,
                 98, 39, 98, 34, 3, 67, 8, 98, 39, 98, 34, 3, 67, 8, 98, 39, 98,
                 8, 98, 39, 98, 34, 3, 67 ]
            result_list = data_distribute(i_list,6)

    data_list{List}: ��Ҫ�����б�
    chunk_num{Int}:  ����������б������
    :return{List}:  ���������б�һ�������������б���б�һ����Ϣ��ɵ��б�
    """
    msg_info = []
    def sub_list(main_list, l_len):
        """ѡ��
        :param main_list: {List} ���б����ǵ���Ҫ�б�
        :param l_len: {Int} ��Ƭ���ȣ�ʹ��pop����
        :return: {List} son ����һ�����б�
        """
        # son ���б�
        son = []
        for ii7 in xrange(l_len):
            son.append(main_list.pop())
        return son
    
    # ˳������Ϊpop()ȡ���һλ���ұ�pop(0)��
    data_list.reverse()
    # �����������б���б�
    result_groups = []
    lenn = len(data_list)
    # print("list_lence:", lenn
    # ��Ϊcore�飬slice_amountΪÿ�������
    slice_amount = lenn // chunk_num
    # print("slice_count:", slice_amount
    for i in xrange(chunk_num):
        # ��coreΪ���ȵ�һ����Ƭ
        l_slice = sub_list(data_list, slice_amount)
        # print("one_slice:", l_slice)
        result_groups.append(l_slice)
    # remained_item_amount ��Ҫ�����б���ʣ���Ԫ�صĸ���
    remained_item_amount = lenn - slice_amount * chunk_num
    msg1 = "remained_item:{0} ; remained_item_amount:{1}".format(
        data_list, remained_item_amount)
    # print(msg1)
    # ����Ҫ�б��е�ֵȡ��Ž���
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

# װ�κ��� �����������ʱ��
def timewrap(func):
    def inner():
        start = time.time()
        func()
        end = time.time()
        msg = 'Time consuming: {}'.format(end-start)
        print(msg)
    return inner

# װ�κ��� ����CPUִ��ʱ��
def timewrap_cpu(func):
    def inner():
        start = time.clock()
        func()
        end = time.clock()
        msg = 'CPU time consuming: {}'.format(end - start)
        print(msg)
    return inner


class HyTime(object):
    """ʱ�����ģ��"""
    def __init__(self):
        # ���ַ���ת��Ϊʱ���ʽ
        time2 = datetime.strptime("2019-9-1", "%Y-%m-%d")
    
    
    @property
    def time_now(self):
        now = datetime.now()
        # ��ʽ��ʱ�䣬ת��Ϊ�ַ���
        time_now_str = datetime.strftime(now, "%Y %m %d %H:%M:%S")
        # ���ص�ǰʱ���Լ���ǰʱ����ַ�������
        return now, time_now_str
    
    # ��¼����ʱ��
    def elapsed_time(self, early_time, after_time):
        """
        early_time(ʱ���ʽ):
        after_time(ʱ���ʽ):
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
