# -*- coding:utf8 -*-
import os
import codecs
import configparser

configDir = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), "ConfigFile")
# print(configDir)
configPath = os.path.join(configDir, "config.ini")
# print(configPath)

def getFileName(path):
    # 获取指定目录下的所有指定后缀的文件名
    file_list = os.listdir(path)
    config_file = []
    for i in file_list:
        if os.path.splitext(i)[1] == ".ini":
            config_file.append(i)
        return config_file

class Config:
    def __init__(self):
        fd = open(configPath, encoding="utf8")
        data = fd.read()
        if data[:3] == codecs.BOM_UTF8:
            data = data[3:]
            file = codecs.open(configPath, "w")
            file.write(data)
            file.close()
        fd.close()

        self.cf = configparser.ConfigParser()
        self.cf.read(configPath)

    def getconfigvalue(self, name):
        valuess = self.cf.get("config", name)
        return valuess

    def getcmdvalue(self, name):
        valuess = self.cf.get("cmd", name)
        return valuess

    def setconfigvalue(self, sectionss, name, valuea):
        self.cf.set(sectionss, name, valuea)
        fp = open(configPath, "w")
        self.cf.write(fp)

    def get_email(self, name):
        emailvalue = self.cf.get("EMAIL", name)
        return emailvalue

    def get_http(self, name):
        httpvalue = self.cf.get("HTTP", name)
        return httpvalue

    def get_headers(self, name):
        value = self.cf.get("HEADERS", name)
        return value

    def set_headers(self, name, value):
        self.cf.set("HEADERS", name, value)
        with open(configPath, 'w+') as f:
            self.cf.write(f)

    def get_url(self, name):
        urlvalue = self.cf.get("URL", name)
        return urlvalue

    def get_db(self, name):
        dbvalue = self.cf.get("DATABASE", name)
        return dbvalue

    def get_log(self, name):
        logvalue = self.cf.get("log", name)
        return logvalue


    def get_config_value(self, config_item, config_item_name):
        """
        取配置文件中配置项的值
        :param config_item: 配置名称
        :param config_item_name: 配置项名称
        :return: 配置项的值
        """
        config_item_value = self.cf.get(config_item, config_item_name)
        return config_item_value

if __name__ == "__main__":
    config = Config()
    # config.setconfigvalue("log", "name", "yangguo")
    # values = config.get_log("name")
    # print(values)

    config_value = config.get_config_value("EMAIL", "mail_host")
    print("【mail_host】 : 【%s】" % config_value)