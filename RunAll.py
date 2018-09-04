# -*- coding:utf8 -*-

__author__ = "杨果"

import os
import unittest
from common import HTMLTestRunner, SendEmail

cur_path = os.path.dirname(os.path.realpath(__file__))
# print(cur_path)

class RunAll:
    @staticmethod
    def add_case(case_name="TestCase", rule="Test_*.py"):
        case_path = os.path.join(cur_path, case_name)
        # print(case_path)
        if not os.path.exists(case_path):
            os.mkdir(case_path)
        discover = unittest.defaultTestLoader.discover(case_path, pattern=rule, top_level_dir=None)
        # print(discover)
        return discover

    @staticmethod
    def run_case(inner_all_case, reportName="TestResult"):
        reportPath = os.path.join(cur_path, reportName)
        # print(reportPath)

        if not os.path.exists(reportPath):
            os.mkdir(reportPath)
        resultDirPath = os.path.join(reportPath, "result")
        if not os.path.exists(resultDirPath):
            os.mkdir(resultDirPath)

        resultPath = os.path.join(resultDirPath, "result.html")
        fp = open(resultPath, "wb")
        runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u"接口自动化测试报告", description=u"用例执行情况")
        runner.run(inner_all_case)
        fp.close()

if __name__ == "__main__":
    runall = RunAll()
    # 加载用例
    all_case = runall.add_case()
    # 执行用例
    runall.run_case(all_case)
    # 发送邮件
    sendEmail = SendEmail.SendEmail.send_mail()
