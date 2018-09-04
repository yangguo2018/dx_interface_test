# -*- coding:utf8 -*-

__author__ = "杨果"

from TestCase import DataRead
import json
import requests
import re
import demjson
from common.Log import MyLog

class Handle:

    # 处理前置setup
    def handle_setup(self):
        pass

    # 处理后置teardown，获取获取请求值，保存参数到全局变量中
    @staticmethod
    def handle_teardown(teardown, response):
        tearDown = json.loads(teardown)
        resPonse = json.loads(response)
        teardown_dict = {}
        # 判断返回值类型是list还是dict
        if isinstance(resPonse, list):
            for i in tearDown.keys():
                res_value = resPonse[int(i)]
                t_value = tearDown[i]
                for keys in t_value.keys():
                    teardown_dict[t_value[keys]] = res_value[keys]
        else:
            for i in tearDown.keys():
                value = resPonse[i]
                if isinstance(tearDown[i], dict):
                    for j in tearDown[i].keys():
                        if isinstance(value, list):
                            value2 = value[int(j)]
                            k = tearDown[i][j]
                            for l in k.keys():
                                m = k[l]
                                teardown_dict[m] = value2[l]
                        elif isinstance(value, dict):
                            value2 = value[j]
                            key = tearDown[i][j]
                            teardown_dict[key] = value2
                else:
                    key = tearDown[i]
                    teardown_dict[key] = value
        DataRead.set_global(teardown_dict)

    # 提交接口请求
    @staticmethod
    def handle_request(method, url, data, header=None):
        log = MyLog.get_log()
        logger = log.get_logger()

        if method == "post":
            if header == "":
                res = requests.post(url, data=data, verify=False)
            else:
                res = requests.post(url, json=data, headers=header, verify=False)
        elif method == "get":
            logger.info("get method url:%s" % url)
            res = requests.get(url, headers=header, verify=False)
        elif method == "put":
            logger.info("put method url:%s" % url)
            logger.info("put method data:%s" % data)
            logger.info("put method headers:%s" % header)
            res = requests.put(url, json=data, headers=header, verify=False)

        return res.status_code, res.content, res.headers

    # 处理body中参数
    @staticmethod
    def handle_param(data):
        log = MyLog.get_log()
        logger = log.get_logger()

        if "{" in data:
            param = re.findall('{(.*?)}', data)  # 正则匹配出参数

            for i in param:
                datayaml = DataRead.get_yaml()
                datavalue = data.replace("{"+i+"}", '"'+datayaml[i]+'"')
                data = datavalue
        logger.info("handle_param-data: %s && type(data):%s" % (data, type(data)))
        return demjson.decode(data)

    # 处理url中参数
    @staticmethod
    def handle_url(data):
        if "{" in data:
            param = re.findall('{(.*?)}', data)  # 正则匹配出参数
            for i in param:
                datayaml = DataRead.get_yaml()
                datavalue = data.replace("{"+i+"}", datayaml[i])
                data = datavalue
        return data

    # 处理前置header
    @staticmethod
    def handle_header(header):
        handle_head_name = header
        if handle_head_name == "admin_header":
                Header = DataRead.get_header("admin_token")
        elif handle_head_name == "user_header":
            Header = DataRead.get_header("user_token")
        elif handle_head_name == "doctor_header":
            Header = DataRead.get_header("doctor_token")
        elif handle_head_name == "check_header":
            Header = DataRead.get_header("check_token")

        return Header
