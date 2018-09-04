# -*- coding:utf8 -*-

import logging
import os
from datetime import datetime
import threading

class Log:
    def __init__(self):
        global proDir, resultPath, logPath

        proDir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        # print(proDir)

        resultPath = os.path.join(proDir, "TestResult\Log")
        # print(resultPath)
        if not os.path.exists(resultPath):
            os.mkdir(resultPath)

        logPath = os.path.join(resultPath, datetime.now().strftime("%Y%m%d"))
        # print(logPath)
        if not os.path.exists(logPath):
            os.mkdir(logPath)

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        filename = datetime.now().strftime("%H%M%S") + "_log.log"
        # print(filename)

        handler = logging.FileHandler(os.path.join(logPath, filename), encoding="utf-8")
        # formatter = logging.Formatter(r"%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        formatter = logging.Formatter(r"%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def get_logger(self):
        """
        get logger
        :return:
        """
        return self.logger

    def build_start_line(self, case_no):
        """
        write start line
        :return:
        """
        self.logger.info("--------" + case_no + " START--------")

    def build_end_line(self, case_no):
        """
        write end line
        :param case_no:
        :return:
        """
        self.logger.info("--------" + case_no + "--------")

    def build_case_line(self, case_name, code, msg):
        """
        write test case line
        :param case_name:
        :param code:
        :param msg:
        :return:
        """
        self.logger.info(case_name + " - Code:" + code + " - msg:" + msg)

    @staticmethod
    def get_report_path():
        """
        get file report path
        :return:
        """
        report_path = os.path.join(logPath, "report.html")
        return report_path

    @staticmethod
    def get_result_path(self):
        """
        get test result path
        :return:
        """
        return logPath

    def write_result(self, result):
        """
        result
        :param result:
        :return:
        """
        result_path = os.path.join(logPath, "result.txt")
        fb = open(result_path, "wb")
        try:
            fb.write(result)
        except FileNotFoundError as ex:
            self.logger.error(str(ex))

class MyLog:
    mylog = None
    mutex = threading.Lock()

    @staticmethod
    def get_log():
        if MyLog.mylog is None:
            MyLog.mutex.acquire()
            MyLog.mylog = Log()
            MyLog.mutex.release()
        return MyLog.mylog

if __name__ == "__main__":
    log = MyLog.get_log()
    logger = log.get_logger()
    logger.info("test info")
    logger.info("thread start")
