# -*- coding:utf8 -*-

__author__ = "杨果"

from common.Log import MyLog
import unittest
from TestCase import Handle, DataRead
from parameterized import parameterized
import traceback

# 设定输出的用例报告中的用例名格式
def custom_name_func(testcase_func=None, param_num=None, param=None):
    # log = MyLog.get_log()
    # logger = log.get_logger()
    # logger.info("testcase_func is %s，%s", testcase_func, param_num)
    return "%s_%s_%s" % ("test", str(param.args[0]), str(param.args[3]))

class TestMain(unittest.TestCase):

    """主流程测试"""
    # 初始化运行
    @classmethod
    def setUpClass(cls):
        print("----Test Start----")
        cls._handle = Handle.Handle()
        setup_data = DataRead.get_xls("dict", u"dx_interauto_qa_case.xls", "setup")
        DataRead.set_global(setup_data)

    case = DataRead.get_xls("list", u"dx_interauto_qa_case.xls", "main")    # 获取用例文件中的用例（Excel文件名,sheet名）

    # 参数化数据，将获取的用例参数化读取；testcase_func_name参数化用例名称
    @parameterized.expand(case, testcase_func_name=custom_name_func)
    def test_main(self, case_id, setup, header, case_name, url, method, path, param, teardown, test_assert):
        log = MyLog.get_log()
        logger = log.get_logger()

        try:
            # print 用来将case_id 输出到报告中
            print("case_%s" % case_id)
            # print("setup is %s" % setup)
            print("case_name is %s" % case_name)
            # print("test_assert is %s" % test_assert)
            # print("yaml_data:%s" % DataRead.get_yaml())

            self.path = self._handle.handle_url(path)
            self.url = "%s%s" % (url, self.path)
            # 判断param中是否有参数化
            if "{" in param:
                self.param = self._handle.handle_param(param)
            else:
                self.param = param

            # 判断是否有前置header需求
            if header != "":
                self.header = self._handle.handle_header(header)
            else:
                self.header = header
            print("url:%s" % self.url)
            print("--------------------------------------------")

            res_code, res_content, res_headers = self._handle.handle_request(method, self.url, self.param, self.header)  # 提交接口数据
            print("res_code:%s & type:%s" % (res_code, type(res_code)))
            print("res_content:%s" % res_content)
            print("res.headers:%s" % res_headers)

            assert 200 <= res_code < 300

            if teardown != "":
                self._handle.handle_teardown(teardown, res_content)

        except Exception as e:
            logger.error('traceback.print_exc():%s,%s' % (traceback.print_exc(), e))
            logger.info('traceback.print_exc():%s,%s' % (traceback.format_exc(), e))

            logger.info("case_%s" % case_id)
            logger.info("case_name is %s" % case_name)
            logger.info("url:%s" % self.url)
            logger.info("--------------------------------------------")
            logger.info("res_code:%s & type:%s" % (res_code, type(res_code)))
            logger.info("res_content:%s" % res_content)
            logger.info("res.headers:%s" % res_headers)
            self.assertTrue(0)

    @classmethod
    def tearDownClass(cls):
        log = MyLog.get_log()
        logger = log.get_logger()
        logger.info(DataRead.get_yaml())
        DataRead.del_yaml()
        print("----Test Over----")
