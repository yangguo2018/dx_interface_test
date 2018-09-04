# -*- coding:utf8 -*-

from common import Config
from common.Log import MyLog
import pymysql

class MysqlDB:
    global host, username, password, port, database, configItem
    config = Config()
    host = config.get_db("host")
    username = config.get_db("username")
    password = config.get_db("password")
    port = config.get_db("port")
    database = config.get_db("database")
    configItem = {
        "host": host,
        "username": username,
        "password": password,
        "port": port,
        "database": database
    }

    def __init__(self):
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        self.db = None
        self.cursor = None
        self.fetchall = None
        self.fetchone = None

    def connectDB(self):
        try:
            # conn to DB
            self.db = pymysql.connect(**configItem)
            # create cursor
            self.cursor = self.db.cursor()
            self.logger.info("Connect DB successfully!")
        except ConnectionError as ex:
            self.logger.info(str(ex))

    def executeSQL(self, sql, params):
        self.connectDB()
        # executing sql
        self.cursor.execute(sql, params)
        # executing by committing to DB
        self.db.commit()
        return self.cursor

    def get_all(self, cursor):
        self.fetchall = cursor.fetchall()
        return self.fetchall

    def get_one(self, cursor):
        self.fetchone = cursor.fetchone()
        return self.fetchone

    def closeDB(self):
        # close db
        self.db.close()
        self.logger.info("Database closed!")

if __name__ == "__main__":
    mysql = MysqlDB()
    # mysql.executeSQL()
