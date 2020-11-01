#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    :
# @Author  :
# @File    : difference.py
# @Software: PyCharm
# @desc    : 对比接口excel， json更新

import xlrd, time, difflib, sys, os
from utils.logger import Log #, report_path
from runAll import report_path
from utils.logger import Log

log = Log()


def diff_excel(ori_path, tar_path, sub_name):
    """比较excel文件"""
    success = 0  # 匹配一致数量
    fail = 0  # 匹配不一致数量
    origin_xls = {}  # 存储源xls文件
    target_xls = {}  # 比对的xls文件
    wb_ori = xlrd.open_workbook(ori_path)  # 打开原始文件
    wb_tar = xlrd.open_workbook(tar_path)  # 打开目标文件
    log.info(':【开始比对】...' + '\n')  # 写入开始时间

    try:
        sheet_ori = wb_ori.sheet_by_name(sub_name)
        sheet_tar = wb_tar.sheet_by_name(sub_name)
        if sheet_ori.name == sheet_tar.name:
            # sheet表名
            if sheet_ori.name == sub_name:
                # 先将数存入dictionary中dictionary(rows:list)
                # 第一行存储表头
                # 源表取一行数据与目标表全表进行比对如果表中存在主键可以用主键进行索引
                # 数据从excel第3行开始
                for rows in range(1, sheet_ori.nrows):
                    orign_list = sheet_ori.row_values(rows)  # 源表i行数据
                    target_list = sheet_tar.row_values(rows)  # 目标表i行数据
                    origin_xls[rows] = orign_list  # 源表写入字典
                    target_xls[rows] = target_list  # 目标表写入字典
                if origin_xls[1] == target_xls[1]:
                    log.info('>>>>>>>>>>>>>>>>>>> 表头一致')
                for ori_num in origin_xls:
                    flag = 'false'  # 判断是否一致标志
                    for tar_num in target_xls:
                        if origin_xls[ori_num] == target_xls[tar_num]:
                            flag = 'true'
                            break  # 如果匹配到结果退出循环
                    if flag == 'true':  # 匹配上结果输出后台日志
                        success += 1
                    else:  # 匹配不上将源表中行记录写入log
                        fail += 1
                        data = origin_xls[ori_num]
                        logstr = '【不一致】row<' + str(ori_num) + '>:' + str(data)
                        log.info(logstr)
                logstr = '【比对完成】总记录数:{:d}条,一致:{:d}条,不一致:{:d}条'.format(ori_num, success, fail)
                log.info(logstr)
        else:
            errmsg = '【' + sub_name + '】子表名不一致'
            log.info(errmsg)
    except Exception as err:
        log.info(str(err))  # 输出异常


# 创建打开文件函数，并按换行符分割内容
def read_json(filename):
    try:
        with open(filename, 'r') as fileHandle:
            text = fileHandle.read().splitlines()
        return text
    except IOError as e:
        log.error("Read file Error:" + e)
        sys.exit()


# 比较两个文件并输出到html文件中
def diff_json(filename1, filename2, name):
    text1_lines = read_json(filename1)
    text2_lines = read_json(filename2)
    d = difflib.HtmlDiff()
    # context=True时只显示差异的上下文，默认显示5行，由numlines参数控制，context=False显示全文，差异部分颜色高亮，默认为显示全文
    result = d.make_file(text1_lines, text2_lines, filename1, filename2, context=True)
    # 内容保存到result.html文件中
    log.info('json数据比对结果写入html中.')
    with open(os.path.join(report_path, '{}_diff.html'.format(name)), 'w') as result_file:
        result_file.write(result)


if __name__ == '__main__':
    for i in ['前台api', '后台api']:
        diff_excel(r'E:\demo\case_generate\data_old\demo_api.xlsx',
                   'E:\demo\case_generate\data_new\demo_api.xlsx', '{}'.format(i))
    diff_json('E:\demo\case_generate\data_old\前台api_data.json',
              'E:\demo\case_generate\data_new\前台api_data.json', '')
