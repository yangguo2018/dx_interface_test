# -*- coding:utf8 -*-

__author = "杨果"

import os
from xlrd import open_workbook
from xlutils.copy import copy
import datetime
import yaml
from common.Log import MyLog
import sys
from xml.etree import ElementTree
import demjson

upPath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# print(upPath)
dirPath = os.path.join(upPath, "TestData")
# print(dirPath)
# yamlpath = os.path.join(upPath, "TestData", "g_data.yaml")
# print(yamlpath)

def get_xlspath(xls_name):
    if not os.path.exists(dirPath):
        os.mkdir(dirPath)
    xlspath = os.path.join(dirPath, xls_name)
    # print(xlspath)
    if not os.path.exists(xlspath):
        log = MyLog.get_log()
        logger = log.get_logger()
        logger.info("文件路径 【%s】 不存在！" % xlspath)
        sys.exit(1)
    return xlspath

def get_yamlpath():
    if not os.path.exists(dirPath):
        os.mkdir(dirPath)
    yamlpath = os.path.join(dirPath, "g_data.yaml")
    # print(yamlpath)
    if not os.path.exists(yamlpath):
        log = MyLog.get_log()
        logger = log.get_logger()
        logger.info("文件路径 【%s】 不存在！" % yamlpath)
        sys.exit(1)
    return yamlpath

# 从excel文件中读取测试用例
def get_xls(data_type, xls_name, sheet_name):
    # get xls file's path
    xlsPath = get_xlspath(xls_name)
    # open xls file
    file = open_workbook(xlsPath)
    if sheet_name not in file.sheet_names():
        log = MyLog.get_log()
        logger = log.get_logger()
        logger.info("sheet页的名字 【%s】 不存在！" % sheet_name)
        sys.exit(1)
    # get sheet by name
    sheet = file.sheet_by_name(sheet_name)
    # get one sheet's rows
    nrow = sheet.nrows
    # 判断需要list还是dict的数据返回
    if data_type == "list":
        cls = []
        for i in range(nrow):
            if sheet.row_values(i)[0] != u"id" and sheet.row_values(i)[0] != u'module' and sheet.row_values(i)[0] != u'name':
                cls.append(sheet.row_values(i))
    elif data_type == "dict":
        cls = {}
        for i in range(nrow):
            if sheet.row_values(i)[0] != u'id' and sheet.row_values(i)[0] != u'module' and sheet.row_values(i)[0] != u'name':
                cls.setdefault(sheet.row_values(i)[0], sheet.row_values(i)[1])

    if sheet_name == "setup":
        num = cls["num"]
        newfile = copy(file)
        newsheet = newfile.get_sheet(0)
        newsheet.write(1, 1, int(int(num) + 1))
        newsheet.write(3, 1, int(int(cls['user_phone']) + 1))

        newfile.save(xlsPath)

        cls = handle_setup_data(cls)

    return cls

def handle_setup_data(cls):
    num = int(cls['num'])
    user_phone = cls['user_phone']
    startDate = datetime.datetime.now().strftime('%Y-%m-%d')
    user_name = "%s%s" % (cls['user_name'], num)
    StartDateTime = "%s %s" % (startDate, cls['StartDateTime'])
    EndDateTime = "%s %s" % (startDate, cls['EndDateTime'])
    cls['num'] = str(num)
    cls['user_name'] = str(user_name)
    cls['startDate'] = str(startDate)
    cls['endDate'] = str(startDate)
    cls['StartDateTime'] = str(StartDateTime)
    cls['EndDateTime'] = str(EndDateTime)
    cls['user_phone'] = str(int(user_phone))

    return cls

# 从yaml文件中读取数据
def get_yaml():
    yamlpath = get_yamlpath()
    # 读取文件
    f = open(yamlpath, "r")
    # 读取
    data = yaml.load(f)
    f.close()

    return data

def set_yaml(data):
    yamlpath = get_yamlpath()
    # 追加文件
    f = open(yamlpath, 'w')
    # 将data写入到yaml文件中
    # data = '"%s":"%s"'% (key,value)
    yaml.dump(data, f)
    f.close()

# 清除yaml中的数据
def del_yaml():
    yamlpath = get_yamlpath()
    f = open(yamlpath, 'w')
    f.truncate()
    f.close()

# 将初始值添加到全局变量中
def set_global(data):
    yamldata = get_yaml()
    if yamldata is None:
        yamldata = data
    else:
        yamldata.update(data)
    set_yaml(yamldata)

# 组合header，返回header
def get_header(key):
    yamldata = get_yaml()
    token = yamldata[key]
    header = "{'Authorization': 'Bearer %s'}" % token
    return demjson.decode(header)

# 从xml文件中读取sql语句
def set_xml():
    database = {}
    sql_path = os.path.join(upPath, "ConfigFile", "sql.xml")
    # print(sql_path)

    log = MyLog.get_log()
    logger = log.get_logger()
    if not os.path.exists(sql_path):
        logger.info("文件路径 【%s】 不存在！" % sql_path)

    if len(database) == 0:
        tree = ElementTree.parse(sql_path)
        for db in tree.findall("database"):
            db_name = db.get("name")
            # print("db_name is %s" % db_name)
            table = {}
            for tb in db.getchildren():
                table_name = tb.get("name")
                # print("table_name is %s" % table_name)
                sql = {}
                for data in tb.getchildren():
                    sql_id = data.get("id")
                    # print("sql_id is %s" % sql_id)
                    sql[sql_id] = data.text
                    # print("sql is %s" % sql)
                table[table_name] = sql
                # print("table is %s" % table)
            database[db_name] = table
        # print(database)
        return database

def get_xml_dict(database_name, table_name):
    database = set_xml()
    database_dict = database.get(database_name).get(table_name)
    return database_dict

def get_sql(database_name, table_name, sql_id):
    db = get_xml_dict(database_name, table_name)
    sql = str(db.get(sql_id)).strip()
    return sql

if __name__ == "__main__":
    # xls_data = get_xls("dict", u"dx_interauto_qa_case.xls", "setup")
    # print(xls_data)
    sqldict = str(get_xml_dict("Members", "rs_member")).replace("\\n", "").replace(" ", "")
    print("sqldict is 【%s】" % sqldict)
    sqls = get_sql("Members", "rs_member", "select_member")
    print("=========================================================")
    print("select_member is 【%s】" % sqls)
